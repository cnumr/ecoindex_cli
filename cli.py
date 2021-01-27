from datetime import datetime
from typing import List, Optional
from urllib.parse import urlparse

from dotenv import load_dotenv
from typer import Option, colors, confirm, progressbar, secho
from typer.main import Typer

from ecoindex_cli.files import write_results_to_csv
from ecoindex_cli.recursive import Crawler
from ecoindex_cli.scrap import get_page_analysis

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

    if url:
        urls = set(url)

    if urls_file:
        with open(urls_file) as fp:
            urls = [url.replace("\n", "") for url in fp.readlines()]

    if recursive and urls:
        parsed_url = urlparse(next(iter(urls)))
        main_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        secho(f"⏲️ Crawling root url {main_url} -> Wait a minute !", fg=colors.MAGENTA)
        crawler = Crawler()
        urls = crawler.crawl(url=main_url)
        with open(file="urls.csv", mode="w") as urls_file:
            for url in urls:
                urls_file.write(f"{url}\n")

    process_urls = confirm(
        f"There are {len(urls)} url(s), do you want to process?",
        abort=True,
        default=True,
    )

    if urls and process_urls:
        results = []
        secho(f"{len(urls)} urls for {len(window_size)} window size", fg=colors.GREEN)
        with progressbar(
            length=len(urls) * len(window_size),
            label="Processing",
        ) as progress:
            for url in urls:
                for w_s in window_size:
                    results.append(get_page_analysis(url=url, window_size=w_s))
                    progress.update(1)

        output_filename = f"export-{time_now}.csv"
        write_results_to_csv(filename=output_filename, results=results)
        secho(f"🙌️ File {output_filename} written !", fg=colors.GREEN)

    else:
        secho("🔥 You must provide an url...", fg=colors.RED)


if __name__ == "__main__":
    app()
