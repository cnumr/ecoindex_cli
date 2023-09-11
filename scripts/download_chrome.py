import argparse
from enum import Enum

import requests
from pydantic import BaseModel
from tqdm import tqdm


class VersionPosition(BaseModel):
    version: str | None = None
    position: str | None = None


class MetaData(BaseModel):
    name: str
    media_link: str


class FileType(Enum):
    CHROME = "chrome"
    CHROMEDRIVER = "chromedriver"


class ChromiumDownloader:
    def __init__(self, main_version: str | None = None) -> None:
        self._main_version = main_version
        self.chrome_link = None
        self.chromedriver_link = None
        self.version_position = None

    def download_file(self, file_name: str, file_type: FileType):
        if not self.version_position:
            self._find_chrome_position()
        if not self.chrome_link or not self.chromedriver_link:
            self._get_chrome_and_chromedriver_links()

        if file_type == FileType.CHROMEDRIVER:
            if self.chromedriver_link is None:
                raise Exception("chromedriver_link is None")

            url = self.chromedriver_link

        if file_type == FileType.CHROME:
            if self.chrome_link is None:
                raise Exception("chrome_link is None")

            url = self.chrome_link

        resp = requests.get(url, stream=True)
        total = int(resp.headers.get("content-length", 0))
        with open(file_name, "wb") as file, tqdm(
            desc=file_name,
            total=total,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in resp.iter_content(chunk_size=1096):
                size = file.write(data)
                bar.update(size)
        chrome_response = requests.get(url)
        if chrome_response.status_code != 200:
            raise Exception(f"Failed to fetch {self.chrome_link}")

        return self

    def _find_chrome_position(self) -> VersionPosition:
        response = requests.get(
            "https://vikyd.github.io/download-chromium-history-version/json/ver-pos-os/version-position-Linux_x64.json"
        )
        if response.status_code != 200:
            raise Exception("Failed to fetch version-position-Linux_x64.json")

        version_position = response.json()
        for version, position in version_position.items():
            if self._main_version is None or version.startswith(self._main_version):
                self.version_position = VersionPosition(
                    version=version, position=position
                )
                return

        raise Exception(
            f"Failed to find {self._main_version} in version-position-Linux_x64.json"
        )

    def _get_chrome_and_chromedriver_links(self):
        response = requests.get(
            f"https://www.googleapis.com/storage/v1/b/chromium-browser-snapshots/o?delimiter=/&prefix=Linux_x64/{self.version_position.position}/"
        )
        if response.status_code != 200:
            raise Exception(
                f"Failed to fetch {self.version_position.position}-Linux_x64.json"
            )

        for metadata in response.json()["items"]:
            if "chrome-" in metadata["name"]:
                self.chrome_link = metadata["mediaLink"]

            if "chromedriver" in metadata["name"]:
                self.chromedriver_link = metadata["mediaLink"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--main-version",
        default=None,
    )
    parser.add_argument("--chrome-filename", type=str, default="/tmp/chrome-linux.zip")
    parser.add_argument(
        "--chromedriver-filename",
        type=str,
        default="/tmp/chromedriver-linux.zip",
    )
    args = parser.parse_args()

    print("Retrieving chrome and chromedriver:")
    print(f"main-version: {args.main_version}")
    print(f"chrome-filename: {args.chrome_filename}")
    print(f"chromedriver-filename: {args.chromedriver_filename}")

    ChromiumDownloader(args.main_version).download_file(
        args.chromedriver_filename, FileType.CHROMEDRIVER
    ).download_file(args.chrome_filename, FileType.CHROME)
