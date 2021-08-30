from datetime import datetime
from os.path import dirname
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse
from webbrowser import open as open_webbrowser

from click.exceptions import Exit
from click_spinner import spinner
from ecoindex.scrap import get_page_analysis
from ecoindex_cli.cli.arguments_handler import (
    get_url_from_args,
    get_urls_from_file,
    get_urls_recursive,
    get_window_sizes_from_args,
)
from ecoindex_cli.files import write_results_to_file, write_urls_to_file
from ecoindex_cli.report.report import generate_report
from pydantic.error_wrappers import ValidationError
from typer import Argument, Option, colors, confirm, progressbar, secho
from typer.main import Typer

app = Typer(help="Ecoindex cli to make analysis of webpages")


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
    output_file: Optional[Path] = Option(
        default=None, help="You can define an output file for the csv results"
    ),
):
    """
    Make an ecoindex analysis of given webpages or website. You
    can generate a csv files with the results or an html report
    """

    if recursive:
        confirm(
            text="You are about to perform a recursive website scraping. This can take a long time. Are you sure to want to proceed?",
            abort=True,
            default=True,
        )

    try:
        window_sizes = get_window_sizes_from_args(window_size)

        urls = set()
        if url and recursive:
            secho(f"⏲️ Crawling root url {url[0]} -> Wait a minute!", fg=colors.MAGENTA)
            with spinner():
                urls = get_urls_recursive(main_url=url[0])
        elif url:
            urls = get_url_from_args(urls_arg=url)
        elif urls_file:
            urls = get_urls_from_file(urls_file=urls_file)

        else:
            secho("🔥 You must provide an url...", fg=colors.RED)
            raise Exit(code=1)

        domain = urlparse(next(iter(urls))).netloc
        write_urls_to_file(domain=domain, urls=urls)
        secho(f"📁️ Urls recorded in file `/tmp/ecoindex-cli/input/{domain}.csv`")

    except (ValidationError) as e:
        secho(str(e), fg=colors.RED)
        raise Exit(code=1)

    confirm(
        text=f"There are {len(urls)} url(s), do you want to process?",
        abort=True,
        default=True,
    )

    results = []
    secho(f"{len(urls)} urls for {len(window_sizes)} window size", fg=colors.GREEN)
    with progressbar(
        length=len(urls) * len(window_sizes),
        label="Processing",
    ) as progress:
        for url in urls:
            for w_s in window_sizes:
                if url:
                    results.append(get_page_analysis(url=url.strip(), window_size=w_s))
                progress.update(1)

    time_now = datetime.now()

    output_folder = f"/tmp/ecoindex-cli/output/{domain}/{time_now}"
    output_filename = f"{output_folder}/results.csv"

    if output_file:
        output_filename = output_file
        output_folder = dirname(output_filename)

    Path(output_folder).mkdir(parents=True, exist_ok=True)
    write_results_to_file(filename=output_filename, results=results)
    secho(f"🙌️ File {output_filename} written !", fg=colors.GREEN)
    if html_report:
        generate_report(
            results_file=output_filename,
            output_path=output_folder,
            domain=domain,
            date=time_now,
        )
        secho(
            f"🦄️ Amazing! A report has been generated to `{output_folder}/report.html`"
        )
        open_webbrowser(f"file://{output_folder}/report.html")


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
