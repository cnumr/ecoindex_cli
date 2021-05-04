from datetime import datetime
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

from click.exceptions import BadParameter, Exit
from dotenv import load_dotenv
from typer import Option, colors, confirm, progressbar, secho
from typer.main import Typer
from validators.utils import ValidationFailure

from ecoindex_cli.arguments_handler import (
    get_url_from_args,
    get_urls_from_file,
    get_urls_recursive,
)
from ecoindex_cli.files import write_results_to_csv, write_urls_to_file
from ecoindex_cli.scrap import get_page_analysis
from ecoindex_cli.validators import validate_window_size

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
    if recursive:
        confirm(
            text="You are about to perform a recursive website scraping. This can take a long time. Are you sure to want to proceed?",
            abort=True,
            default=True,
        )

    try:
        validate_window_size(window_size)

        urls = set()
        if url:
            urls = get_url_from_args(urls_arg=url)
        elif urls_file:
            urls = get_urls_from_file(urls_file=urls_file)
        elif recursive and url:
            secho(f"⏲️ Crawling root url {url[0]} -> Wait a minute!", fg=colors.MAGENTA)
            urls = get_urls_recursive(main_url=url[0])

        else:
            secho("🔥 You must provide an url...", fg=colors.RED)
            raise Exit(code=1)

        domain = urlparse(next(iter(urls))).netloc
        write_urls_to_file(domain=domain, urls=urls)
        secho(f"📁️ Urls recorded in file `input/{domain}.csv`")

    except (BadParameter) as e:
        secho(e.format_message(), fg=colors.RED)
        raise Exit(code=1)

    confirm(
        text=f"There are {len(urls)} url(s), do you want to process?",
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

    time_now = datetime.now()
    output_folder = f"output/{domain}/{time_now}"
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    output_filename = f"{output_folder}/results.csv"
    write_results_to_csv(filename=output_filename, results=results)
    secho(f"🙌️ File {output_filename} written !", fg=colors.GREEN)


if __name__ == "__main__":
    app()
