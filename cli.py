from datetime import datetime
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

from click.exceptions import Exit
from dotenv import load_dotenv
from typer import Option, colors, confirm, progressbar, secho
from typer.main import Typer
from validators import url as validate_url

from ecoindex_cli.files import write_results_to_csv
from ecoindex_cli.recursive import Crawler
from ecoindex_cli.scrap import get_page_analysis
from ecoindex_cli.validator import window_size as validate_window_size

app = Typer()
load_dotenv()


@app.command()
def main(
    url: Optional[List[str]] = Option(None, help="List of urls to analyze"),
    window_size: Optional[List[str]] = Option(
        ["1920,1080"],
        help="You can set multiple window sizes to make ecoindex test. You have to use the format `width,height` in pixel",
    ),
    recursive: Optional[bool] = Option(
        False,
        help="You can make a recursive analysis of a website. In this case, just provide one root url. Be carreful with this option. Can take a loooong long time !",
    ),
    urls_file: Optional[str] = Option(
        None,
        help="If you want to analyze multiple urls, you can also set them in a file and provide the file name",
    ),
):

    urls = set()
    time_now = datetime.now()

    if not validate_window_size(window_size):
        secho(
            f"🔥 {window_size} is not a valid window_size. Must be of type ('1920,1080',...)",
            fg=colors.RED,
        )
        raise Exit(code=1)

    if url:
        urls = set(url)

    if urls_file:
        with open(urls_file) as fp:
            urls = [url.replace("\n", "") for url in fp.readlines()]

    if urls:
        parsed_url = urlparse(next(iter(urls)))
        domain = parsed_url.netloc

    if recursive and urls:
        main_url = f"{parsed_url.scheme}://{domain}"
        secho(f"⏲️ Crawling root url {main_url} -> Wait a minute !", fg=colors.MAGENTA)
        crawler = Crawler()
        urls = crawler.crawl(url=main_url)
        with open(file=f"input/{domain}.csv", mode="w") as urls_file:
            for url in urls:
                urls_file.write(f"{url}\n")
        secho(f"📁️ Urls recorded in file `input/{domain}.csv`")

    if urls:
        for url in urls:
            if not validate_url(url):
                secho(f"🔥 {url} is not a valid url", fg=colors.RED)
                raise Exit(code=1)
        confirm(
            f"There are {len(urls)} url(s), do you want to process?",
            abort=True,
            default=True,
        )
        results = []
        secho(f"{len(urls)} urls for {len(window_size)} window size", fg=colors.GREEN)
        with progressbar(
            length=len(urls) * len(window_size),
            label="Processing",
        ) as progress:
            for url in urls:
                for w_s in window_size:
                    if url:
                        results.append(get_page_analysis(url=url, window_size=w_s))
                    progress.update(1)

        output_folder = f"output/{domain}/{time_now}"
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        output_filename = f"{output_folder}/results.csv"
        write_results_to_csv(filename=output_filename, results=results)
        secho(f"🙌️ File {output_filename} written !", fg=colors.GREEN)

    else:
        secho("🔥 You must provide an url...", fg=colors.RED)
        raise Exit(code=1)


if __name__ == "__main__":
    app()
