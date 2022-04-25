# Ecoindex-Cli

[![Quality check](https://github.com/cnumr/ecoindex_cli/workflows/Quality%20checks/badge.svg)](https://github.com/cnumr/ecoindex_cli/actions/workflows/quality.yml)
[![PyPI version](https://badge.fury.io/py/ecoindex-cli.svg)](https://badge.fury.io/py/ecoindex-cli)

This tool provides an easy way to analyze websites with [Ecoindex](http://www.ecoindex.fr) from your local computer. You have the ability to:

- Make the analysis on multiple pages
- Define multiple screen resolution
- Make a recursive analysis from a given website

This CLI is built on top of [ecoindex-python](https://pypi.org/project/ecoindex/) with [Typer](https://typer.tiangolo.com/)

The output is always a CSV file with the results of the analysis.

> **Current limitation:** This does not work well with SPA.

## Requirements

- Python ^3.8
- [pip](https://pip.pypa.io/en/stable/)

## Setup

```bash
pip install --user -U ecoindex-cli
```

## Use case

The cli gets 2 commands: `analyze` and `report` which can be used separately:

```bash
ecoindex-cli --help                                
```

```bash
Usage: ecoindex-cli [OPTIONS] COMMAND [ARGS]...

  Ecoindex cli to make analysis of webpages

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  analyze  Make an ecoindex analysis of given webpages or website.
  report   If you already performed an ecoindex analysis and have your...
```

### Make a simple analysis

You give just one web url

```bash
ecoindex-cli analyze --url http://www.ecoindex.fr
```

<details><summary>Result</summary>

```bash
There are 1 url(s), do you want to process? [Y/n]:
1 urls for 1 window size
Processing  [####################################]  100%
🙌️ File /tmp/ecoindex-cli/output/www.ecoindex.fr/2021-04-20 16:44:33.468755/results.csv written !
```

</details>

> This makes an analysis with a screen resolution of 1920x1080px by default

### Set the output file

You can define the csv output file

```bash
ecoindex-cli analyze --url http://www.ecoindex.fr --output-file ~/ecoindex-results/ecoindex.csv
```

<details><summary>Result</summary>

```bash
📁️ Urls recorded in file `input/www.ecoindex.fr.csv`
There are 1 url(s), do you want to process? [Y/n]:
1 urls for 1 window size
Processing  [####################################]  100%
🙌️ File /home/vvatelot/ecoindex-results/ecoindex.csv written !
```

</details>

### Multiple url analysis

```bash
ecoindex-cli analyze --url http://www.ecoindex.fr --url https://www.greenit.fr/
```

<details><summary>Result</summary>

```bash
There are 2 url(s), do you want to process? [Y/n]:
2 urls for 1 window size
Processing  [####################################]  100%
🙌️ File /tmp/ecoindex-cli/output/www.ecoindex.fr/2021-04-20 16:45:24.458052/results.csv written !
```

</details>

### Provide urls from a file

You can use a file with given urls that you want to analyze: One url per line. This is helpful if you want to play the same scenario recurrently.

```bash
ecoindex-cli analyze --urls-file input/ecoindex.csv
```

<details><summary>Result</summary>

```bash
There are 2 url(s), do you want to process? [Y/n]:
2 urls for 1 window size
Processing  [####################################]  100%
🙌️ File /tmp/ecoindex-cli/output/www.ecoindex.fr/2021-04-20 16:45:24.458052/results.csv written !
```

</details>

### Make a recursive analysis

You can make a recursive analysis of a given webiste. This means that the app will try to find out all the pages into your website and launch an analysis on all those web pages. ⚠️ This can process for a very long time! **Use it at your own risks!**

```bash
ecoindex-cli analyze --url http://www.ecoindex.fr --recursive
```

<details><summary>Result</summary>

```bash
⏲️ Crawling root url http://www.ecoindex.fr -> Wait a minute !
📁️ Urls recorded in file `/tmp/ecoindex-cli/input/www.ecoindex.fr.csv`
There are 3 url(s), do you want to process? [Y/n]:
3 urls for 1 window size
Processing  [####################################]  100%
🙌️ File /tmp/ecoindex-cli/output/www.ecoindex.fr/2021-04-20 16:47:29.072472/results.csv written !
```

</details>

### Disable console interaction

You can disable confirmations, and force the app to answer yes to all of them. It can be useful if you need to start the app from another script, or if you have no time to wait it to finish.

```bash
ecoindex-cli analyze --url http://www.ecoindex.fr --recursive --no-interaction
```

<details><summary>Result</summary>

```bash
⏲️ Crawling root url http://www.ecoindex.fr -> Wait a minute !
📁️ Urls recorded in file `/tmp/ecoindex-cli/input/www.ecoindex.fr.csv`
3 urls for 1 window size
Processing  [####################################]  100%
🙌️ File /tmp/ecoindex-cli/output/www.ecoindex.fr/2021-11-04 08:19:13.410571/results.csv written !
```

</details>

### Set other screen resolutions

You can provide other screen resolutions. By default, the screen resolution is `1920x1080px` but you can provide other resolution for example if you want to test ecoindex for mobile.

```bash
ecoindex-cli analyze --url http://www.ecoindex.fr --window-size 1920,1080 --window-size 386,540
```

<details><summary>Result</summary>

```bash
There are 1 url(s), do you want to process? [Y/n]:
1 urls for 2 window size
Processing  [####################################]  100%
🙌️ File /tmp/ecoindex-cli/output/www.ecoindex.fr/2021-04-21 21:22:44.309077/results.csv written !
```

</details>

### Generate a html report

You can generate a html report easily at the end of the analysis. You just have to add the option `--html-report`.

```bash
ecoindex-cli analyze --url http://www.ecoindex.fr --recursive --html-report
```

<details><summary>Result</summary>

```bash
⏲️ Crawling root url http://www.ecoindex.fr -> Wait a minute !
📁️ Urls recorded in file `input/www.ecoindex.fr.csv`
There are 3 url(s), do you want to process? [Y/n]:
3 urls for 1 window size
Processing  [####################################]  100%
🙌️ File output/www.ecoindex.fr/2021-04-21 21:21:27.629691/results.csv written !
🦄️ Amazing! A report has been generated to `/tmp/ecoindex-cli/output/www.ecoindex.fr/2021-04-21 21:21:27.629691/report.html`
```

</details>

Here is a sample result:
![Sample report](doc/report.png)

### Only generate a report from existing result file

If you already performed an anlayzis and (for example), forgot to generate the html report, you do not need to re-run a full analyzis, you can simply request a report from your result file :

```bash
ecoindex-cli report "/tmp/ecoindex-cli/output/www.ecoindex.fr/2021-05-06 19:13:55.735935/results.csv" "www.synchrone.fr"
```

<details><summary>Result</summary>

```bash
🦄️ Amazing! A report has been generated to `/tmp/ecoindex-cli/output/www.ecoindex.fr/2021-05-06 19:13:55.735935/report.html`
```

</details>


## Results example

The result of the analysis is a CSV file which can be easily used for further analysis:

```csv
size,nodes,requests,grade,score,ges,water,url,date,resolution,page_type
119.095,45,8,A,89,1.22,1.83,http://www.ecoindex.fr,2021-04-20 16:45:28.570179,"1920,1080",
769.252,730,94,D,41,2.18,3.27,https://www.greenit.fr/,2021-04-20 16:45:32.199242,"1920,1080",website
```

Where:

- `size` is the size of the page and of the downloaded elements of the page in KB
- `nodes` is the number of the DOM elements in the page
- `requests` is the number of external requests made by the page
- `grade` is the corresponding ecoindex grade of the page (from A to G)
- `score` is the corresponding ecoindex score of the page (0 to 100)
- `ges` is the equivalent of greenhouse gases emission (in `gCO2e`) of the page
- `water`is the equivalent water consumption (in `cl`) of the page
- `url` is the analysed page url
- `date` is the datetime of the page analysis
- `resolution` is the screen resolution used for the page analysis (`width,height`)
- `page_type` is the type of the page, based ton the [opengraph type tag](https://ogp.me/#types)

## Testing

In order to develop or test, you have to use [Poetry](https://python-poetry.org/), install the dependencies and execute a poetry shell:

```bash
poetry install && \
poetry shell
```

We use Pytest to run unit tests for this project. The test suite are in the `tests` folder. Just execute :

```bash
pytest --cov-report term-missing:skip-covered --cov=. --cov-config=.coveragerc tests
```

> This runs pytest and also generate a [coverage report](https://pytest-cov.readthedocs.io/en/latest/) (terminal and html)

## [Contributing](CONTRIBUTING.md)

## [Code of conduct](CODE_OF_CONDUCT.md)
