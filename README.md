# Ecoindex-Cli 
![GitHub branch checks state](https://img.shields.io/github/workflow/status/cnumr/ecoindex_cli/Quality%20checks)

This tool provides an easy way to analyze websites with [Ecoindex](http://www.ecoindex.fr) from your local computer. You have the ability to make the analysis on multiple pages with multiple screen resolution. You can also make a recursive analysis from a given website.

This CLI is built on top of [ecoindex-python](https://pypi.org/project/ecoindex/).

The output is always a CSV file with the results of the analysis.

## Requirements

- Python ^3.8
- [Poetry](https://python-poetry.org/)
- Google Chrome installed on your computer

## Setup

- Get the source
- Get [Chromedriver](https://chromedriver.chromium.org/downloads) corresponding to your google chrome version, install it in your PATH and then configure [.env](.env) file
- Install the command: `poetry install`
- You're good to go

## Use case

```
➜ ecoindex-cli --help
Usage: ecoindex-cli [OPTIONS]

Options:
  --url TEXT                      List of urls to analyze
  --window-size TEXT              You can set multiple window sizes to make
                                  ecoindex test. You have to use the format
                                  `width,height` in pixel  [default:
                                  1920,1080]

  --recursive / --no-recursive    You can make a recursive analysis of a
                                  website. In this case, just provide one root
                                  url. Be carreful with this option. Can take
                                  a loooong long time !  [default: False]

  --urls-file TEXT                If you want to analyze multiple urls, you
                                  can also set them in a file and provide the
                                  file name

  --html-report / --no-html-report
                                  You can generate a html report of the
                                  analysis  [default: False]

  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.
```

### Make a simple analysis

You give just one web url

```shell
➜ ecoindex-cli --url http://www.ecoindex.fr
There are 1 url(s), do you want to process? [Y/n]:
1 urls for 1 window size
Processing  [####################################]  100%
🙌️ File output/www.ecoindex.fr/2021-04-20 16:44:33.468755/results.csv written !
```

> This makes an analysis with a screen resolution of 1920x1080px by default

### Multiple url analysis

```shell
➜ ecoindex-cli --url http://www.ecoindex.fr --url https://www.greenit.fr/
There are 2 url(s), do you want to process? [Y/n]:
2 urls for 1 window size
Processing  [####################################]  100%
🙌️ File output/www.ecoindex.fr/2021-04-20 16:45:24.458052/results.csv written !
```

### Provide urls from a file

You can use a file with given urls that you want to analyze: One url per line. This is helpful if you want to play the same scenario recurrently.

```shell
➜ ecoindex-cli --url http://www.ecoindex.fr --url https://www.greenit.fr/
There are 2 url(s), do you want to process? [Y/n]:
2 urls for 1 window size
Processing  [####################################]  100%
🙌️ File output/www.ecoindex.fr/2021-04-20 16:45:24.458052/results.csv written !
```

### Make a recursive analysis

You can make a recursive analysis of a given webiste. This means that the app will try to find out all the pages into your website and launch an analysis on all those web pages. ⚠️ This can process for a very long time! **Use it at your own risks!**

```shell
➜ ecoindex-cli --url http://www.ecoindex.fr --recursive
⏲️ Crawling root url http://www.ecoindex.fr -> Wait a minute !
📁️ Urls recorded in file `input/www.ecoindex.fr.csv`
There are 3 url(s), do you want to process? [Y/n]:
3 urls for 1 window size
Processing  [####################################]  100%
🙌️ File output/www.ecoindex.fr/2021-04-20 16:47:29.072472/results.csv written !
```

### Set other screen resolutions

You can provide other screen resolutions. By default, the screen resolution is `1920x1080px` but you can provide other resolution for example if you want to test ecoindex for mobile.

```shell
➜ ecoindex-cli --url http://www.ecoindex.fr --window-size 1920,1080 --window-size 386,540
There are 1 url(s), do you want to process? [Y/n]:
1 urls for 2 window size
Processing  [####################################]  100%
🙌️ File output/www.ecoindex.fr/2021-04-20 16:48:16.252714/results.csv written !
```

### Generate a html report

You can generate a html report easily at the end of the analysis. You just have to add the option `--html-report`.

```shell
➜ ecoindex-cli --url http://www.ecoindex.fr --recursive --html-report
1 urls for 2 window size
Processing  [####################################]  100%
🙌️ File export-2021-01-14 11:26:53.368510.csv written !
```

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

## TODO

- [ ] Tests
- [ ] Use Async capability for crawling and analysis
- [ ] Is there a way to wait for the end of the page loading?
- [ ] Chromedriver for windows?
