from datetime import datetime, time
from os.path import dirname
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse
from webbrowser import open as open_webbrowser

from dotenv import load_dotenv
from typer import Argument, Option, colors, confirm, progressbar, secho
from typer.main import Typer

from ecoindex_cli.files import write_results_to_csv
from ecoindex_cli.recursive import Crawler
from ecoindex_cli.report.report import generate_report
from ecoindex_cli.scrap import get_page_analysis

app = Typer(help="Ecoindex cli to make analysis of webpages")
load_dotenv()


@app.command()
def analyze(
    url: Optional[List[str]] = Option(default=None, help="List of urls to analyze"),
    window_size: Optional[List[str]] = Option(
        default=["1920,1080"],
        help="You can set multiple window sizes to make ecoindex test. You have to use the format `width,height` in pixel",
    ),
    recursive: Optional[bool] = Option(
        default=False,
        help="You can make a recursive analysis of a website. In this case, just provide one root url. Be carreful with this option. Can take a loooong long time !",
    ),
    urls_file: Optional[str] = Option(
        default=None,
        help="If you want to analyze multiple urls, you can also set them in a file and provide the file name",
    ),
    html_report: Optional[bool] = Option(
        default=False, help="You can generate a html report of the analysis"
    ),
):
    """
    Make an ecoindex analysis of given webpages or website. You
    can generate a csv files with the results or an html report
    """

    urls = set()
    time_now = datetime.now()

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
                    if url:
                        results.append(get_page_analysis(url=url, window_size=w_s))
                    progress.update(1)

        output_folder = f"output/{domain}/{time_now}"
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        output_filename = f"{output_folder}/results.csv"
        write_results_to_csv(filename=output_filename, results=results)
        secho(f"🙌️ File {output_filename} written !", fg=colors.GREEN)

        if html_report:
            generate_report(
                results_file=output_filename,
                output_path=output_folder,
                domain=domain,
                date=time_now,
            )
            secho(
                f"🦄️ Amazing! A report has been generated to `{Path(__file__).parent.absolute()}/{output_folder}/report.html`"
            )
            open_webbrowser(
                f"file://{Path(__file__).parent.absolute()}/{output_folder}/report.html"
            )
    else:
        secho("🔥 You must provide an url...", fg=colors.RED)


@app.command()
def report(
    results_file: str = Argument(
        ..., help="Filename of the results you want to generate a report for"
    ),
    domain: str = Argument(
        ...,
        help="You have to explicitly tell what is the domain of this result analysis from",
    ),
    output_folder: Optional[str] = Option(
        default=None,
        help="By default, we generate the report in the same folder of the results file, but you can provide another folder",
    ),
):
    """
    If you already performed an ecoindex analysis and have your results,
    you can simply generate an html report using this command
    """
    output_folder = output_folder if output_folder else dirname(results_file)

    generate_report(
        results_file=results_file,
        output_path=output_folder,
        domain=domain,
        date=datetime.now(),
    )
    secho(f"🦄️ Amazing! A report has been generated to `{output_folder}/report.html`")
    open_webbrowser(f"file:///{output_folder}/report.html")


if __name__ == "__main__":
    app()
