from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from multiprocessing import cpu_count
from os.path import dirname
from pathlib import Path
from typing import List
from webbrowser import open as open_webbrowser

from click.exceptions import Exit
from click_spinner import spinner
from pydantic.error_wrappers import ValidationError
from typer import Argument, Option, colors, confirm, progressbar, secho
from typer.main import Typer

from ecoindex_cli.cli.arguments_handler import (
    get_file_prefix_input_file_logger_file,
    get_url_from_args,
    get_urls_from_file,
    get_urls_recursive,
    get_window_sizes_from_args,
)
from ecoindex_cli.cli.helper import run_page_analysis
from ecoindex_cli.enums import ExportFormat, Language
from ecoindex_cli.files import write_results_to_file, write_urls_to_file
from ecoindex_cli.logger import Logger
from ecoindex_cli.report.report import Report

app = Typer(help="Ecoindex cli to make analysis of webpages")


@app.command()
def analyze(
    url: List[str] = Option(default=None, help="List of urls to analyze"),
    window_size: List[str] = Option(
        default=["1920,1080"],
        help="You can set multiple window sizes to make ecoindex test. You have to use the format `width,height` in pixel",
    ),
    recursive: bool = Option(
        default=False,
        help="You can make a recursive analysis of a website. In this case, just provide one root url. Be carreful with this option. Can take a loooong long time !",
    ),
    urls_file: str = Option(
        default=None,
        help="If you want to analyze multiple urls, you can also set them in a file and provide the file name",
    ),
    html_report: bool = Option(
        default=False,
        help="You can generate a html report of the analysis",
    ),
    output_file: Path = Option(
        default=None,
        help="You can define an output file for the csv results. If you generate an HTML report, this option is ignored",
    ),
    no_interaction: bool = Option(
        default=False,
        help="Answer 'yes' to all questions",
    ),
    max_workers: int = Option(
        default=None,
        help="You can define the number of workers to use for the analysis. Default is the number of cpu cores",
    ),
    export_format: ExportFormat = Option(
        default=ExportFormat.csv.value,
        help="You can export the results in json or csv. Default is csv. If you generate an HTML report, this option is ignored",
        case_sensitive=False,
    ),
    html_report_language: Language = Option(
        default=Language.en.value,
        help="You can define the language of the html report. Default is english",
        case_sensitive=False,
    ),
    chrome_version: int = Option(
        default=None,
        help="Main chrome version used for chromedriver. By default, chromedriver tries to use latest version of chrome, but if you have a specific version installed you can specify using it (IE `107`)",
    ),
):
    """
    Make an ecoindex analysis of given webpages or website. You
    can generate a csv files with the results or an html report
    """
    if recursive and not no_interaction:
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
            (
                file_prefix,
                input_file,
                logger_file,
            ) = get_file_prefix_input_file_logger_file(urls=urls)

        elif url:
            urls = get_url_from_args(urls_arg=url)
            (
                file_prefix,
                input_file,
                logger_file,
            ) = get_file_prefix_input_file_logger_file(urls=urls)

        elif urls_file:
            urls = get_urls_from_file(urls_file=urls_file)
            (
                file_prefix,
                input_file,
                logger_file,
            ) = get_file_prefix_input_file_logger_file(urls=urls, urls_file=urls_file)

        else:
            secho("🔥 You must provide an url...", fg=colors.RED)
            raise Exit(code=1)

        if input_file:
            write_urls_to_file(file_prefix=file_prefix, urls=urls)
            secho(f"📁️ Urls recorded in file `{input_file}`")

        if logger_file:
            log = Logger(filename=logger_file)

    except (ValidationError) as e:
        secho(str(e), fg=colors.RED)
        raise Exit(code=1)

    if not no_interaction:
        confirm(
            text=f"There are {len(urls)} url(s), do you want to process?",
            abort=True,
            default=True,
        )

    max_workers = max_workers if max_workers else cpu_count()
    results = []

    secho(
        f"{len(urls)} urls for {len(window_sizes)} window size with {max_workers} maximum workers",
        fg=colors.GREEN,
    )

    with progressbar(
        length=len(urls) * len(window_sizes),
        label="Processing",
        show_percent=True,
        show_pos=True,
    ) as progress:
        error_found = False
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_analysis = {}

            for url in urls:
                for window_size in window_sizes:
                    future_to_analysis[
                        executor.submit(
                            run_page_analysis, url, window_size, chrome_version
                        )
                    ] = (url, window_size, chrome_version)

            for future in as_completed(future_to_analysis):
                try:
                    results.append(future.result())
                except Exception as e:
                    error_found = True
                    log.error(f" -- {url} -- {e.msg if hasattr(e, 'msg') else e}")

                progress.update(1)

        if error_found:
            secho(
                f"\nErrors found: please look at {log.path}/{log.file_name})",
                fg=colors.RED,
            )

    time_now = datetime.now()

    output_folder = (
        f"/tmp/ecoindex-cli/output/{file_prefix}/{time_now.strftime('%Y-%d-%m_%H%M%S')}"
    )
    output_filename = f"{output_folder}/results.{export_format.value}"

    if output_file and not html_report:
        output_filename = output_file.resolve()
        output_folder = output_filename.parent

    Path(output_folder).mkdir(parents=True, exist_ok=True)
    write_results_to_file(
        filename=output_filename, results=results, export_format=export_format
    )
    secho(f"🙌️ File {output_filename} written !", fg=colors.GREEN)
    if html_report:
        Report(
            results_file=output_filename,
            output_path=output_folder,
            domain=file_prefix,
            date=time_now,
            language=html_report_language,
        ).create_report()

        secho(
            f"🦄️ Amazing! A report has been generated to {output_folder}/index.html",
            fg=colors.GREEN,
        )
        open_webbrowser(f"file://{output_folder}/index.html")


@app.command()
def report(
    results_file: str = Argument(
        ..., help="Filename of the results you want to generate a report for"
    ),
    domain: str = Argument(
        ...,
        help="You have to explicitly tell what is the domain of this result analysis from",
    ),
    output_folder: str = Option(
        default=None,
        help="By default, we generate the report in the same folder of the results file, but you can provide another folder",
    ),
    html_report_language: Language = Option(
        default=Language.en.value,
        help="You can define the language of the html report. Default is english",
        case_sensitive=False,
    ),
):
    """
    If you already performed an ecoindex analysis and have your results,
    you can simply generate an html report using this command
    """
    output_folder = output_folder if output_folder else dirname(results_file)

    Report(
        results_file=results_file,
        output_path=output_folder,
        domain=domain,
        date=datetime.now(),
        language=html_report_language,
    ).create_report()

    secho(
        f"🦄️ Amazing! A report has been generated to {output_folder}/index.html",
        fg=colors.GREEN,
    )
    open_webbrowser(f"file:///{output_folder}/index.html")


if __name__ == "__main__":
    app()
