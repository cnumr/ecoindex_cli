from pathlib import Path

from ecoindex_cli.enums import Languages
from ecoindex_cli.files import get_translations
from jinja2 import Environment, FileSystemLoader
from matplotlib import pyplot
from pandas import read_csv
from pandas.core.frame import DataFrame


def prepare_graph(title: str, xlabel: str, ylabel: str) -> None:
    pyplot.clf()
    pyplot.title(title)
    pyplot.ylabel(ylabel=ylabel)
    pyplot.xlabel(xlabel=xlabel)


def create_histogram(
    dataframe: DataFrame,
    property: str,
    title: str,
    xlabel: str,
    ylabel: str,
    output_path: str,
) -> None:
    prepare_graph(title=title, xlabel=xlabel, ylabel=ylabel)
    ax = dataframe[property].plot.hist()
    fig = ax.get_figure()
    fig.savefig(f"{output_path}/{property}.svg")


def create_grade_chart(
    dataframe: DataFrame,
    output_path: str,
    translations: dict,
) -> None:
    prepare_graph(
        title=translations["histograms"]["grade"]["title"],
        xlabel=translations["histograms"]["grade"]["xlabel"],
        ylabel=translations["histograms"]["grade"]["ylabel"],
    )

    dataframe_result = DataFrame(
        data=[0, 0, 0, 0, 0, 0, 0], index=["A", "B", "C", "D", "E", "F", "G"]
    )

    dataframe_grouped_by_grade = dataframe.groupby(["grade"])["grade"].count()

    for grade in dataframe_result.index:
        if grade in dataframe_grouped_by_grade.index:
            dataframe_result[0][grade] += dataframe_grouped_by_grade[grade]

    ax = dataframe_result[0].plot.bar(
        color=[
            "#349A47",
            "#51B84B",
            "#CADB2A",
            "#F6EB15",
            "#FECD06",
            "#F99839",
            "#ED2124",
        ]
    )
    fig = ax.get_figure()
    fig.savefig(f"{output_path}/grade.svg")


def generate_report(
    results_file: str,
    output_path: str,
    file_prefix: str,
    date: str,
    language: Languages,
) -> None:
    df = read_csv(results_file)
    env = Environment(loader=FileSystemLoader(f"{Path(__file__).parent.absolute()}"))
    template = env.get_template("template.html")
    translations = get_translations(language=language)

    create_histogram(
        dataframe=df,
        property="size",
        title=translations["histograms"]["size"]["title"],
        xlabel=translations["histograms"]["size"]["xlabel"],
        ylabel=translations["histograms"]["size"]["ylabel"],
        output_path=output_path,
    )
    create_histogram(
        dataframe=df,
        property="nodes",
        title=translations["histograms"]["nodes"]["title"],
        xlabel=translations["histograms"]["nodes"]["xlabel"],
        ylabel=translations["histograms"]["nodes"]["ylabel"],
        output_path=output_path,
    )
    create_histogram(
        dataframe=df,
        property="requests",
        title=translations["histograms"]["requests"]["title"],
        xlabel=translations["histograms"]["requests"]["xlabel"],
        ylabel=translations["histograms"]["requests"]["ylabel"],
        output_path=output_path,
    )
    create_grade_chart(
        dataframe=df,
        output_path=output_path,
        translations=translations,
    )

    template_vars = {
        "site": file_prefix,
        "date": date,
        "nb_page": len(df.index),
        "all_data": df.to_html(
            columns=[
                "url",
                "page_type",
                "score",
                "size",
                "nodes",
                "requests",
                "water",
                "ges",
            ],
            classes="table is-hoverable is-fullwidth is-bordered",
        ),
        "summary": df[["score", "size", "nodes", "requests", "ges", "water"]]
        .describe()
        .loc[["mean", "min", "max"]]
        .round(2)
        .to_html(classes="table is-hoverable is-fullwidth is-bordered"),
        "best": df.nlargest(n=10, columns="score")[
            ["url", "score", "size", "nodes", "requests"]
        ].to_html(classes="table is-hoverable is-fullwidth is-bordered"),
        "worst": df.nsmallest(n=10, columns="score")[
            ["url", "score", "size", "nodes", "requests"]
        ].to_html(classes="table is-hoverable is-fullwidth is-bordered"),
    }
    html_out = template.render({**template_vars, **translations})

    with open(f"{output_path}/index.html", "w") as f:
        f.write(html_out)
