from datetime import datetime
from pathlib import Path

from ecoindex_cli.enums import GlobalMedian, Language, Target
from ecoindex_cli.files import get_translations
from jinja2 import Environment, FileSystemLoader
from matplotlib import pyplot
from pandas import read_csv
from pandas.core.frame import DataFrame


class Report:
    def __init__(
        self,
        date: datetime,
        domain: str,
        language: Language,
        output_path: str,
        results_file: Path,
    ) -> None:
        self.dataframe = read_csv(results_file)
        self.date = date
        self.domain = domain
        self.language = language
        self.output_path = output_path
        self.translations = get_translations(language=language)

    def create_report(self) -> None:
        self.create_histogram(
            property="requests",
            target=Target.requests.value,
            global_median=GlobalMedian.requests.value,
        )
        self.create_histogram(
            property="size",
            target=Target.size.value,
            global_median=GlobalMedian.size.value,
        )
        self.create_histogram(
            property="nodes",
            target=Target.nodes.value,
            global_median=GlobalMedian.nodes.value,
        )
        self.create_grade_chart()
        self.create_report_file()

    def prepare_graph(self, property: str) -> None:
        pyplot.clf()
        pyplot.title(label=self.translations["histograms"][property]["title"])
        pyplot.xlabel(xlabel=self.translations["histograms"][property]["xlabel"])
        pyplot.ylabel(ylabel=self.translations["histograms"][property]["ylabel"])

    def create_histogram(
        self,
        property: str,
        target: int,
        global_median: int,
    ) -> None:
        median = round(self.dataframe[property].median())
        self.prepare_graph(property=property)
        ax = self.dataframe[property].plot.hist(label="_nolegend_")
        ax.axvline(
            median, color="blue", label=f"{self.translations['my_median']}: {median}"
        )
        ax.axvline(
            x=target,
            color="red",
            linestyle=":",
            label=f"{self.translations['target_median']}: {target}",
        )
        ax.axvline(
            x=global_median,
            color="black",
            linestyle=":",
            label=f"{self.translations['global_median']}: {global_median}",
        )
        pyplot.legend()
        fig = ax.get_figure()
        fig.savefig(f"{self.output_path}/{property}.svg")

    def create_grade_chart(self) -> None:
        self.prepare_graph(property="grade")

        dataframe_result = DataFrame(
            data=[0, 0, 0, 0, 0, 0, 0], index=["A", "B", "C", "D", "E", "F", "G"]
        )

        dataframe_grouped_by_grade = self.dataframe.groupby(["grade"])["grade"].count()

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
        fig.savefig(f"{self.output_path}/grade.svg")

    def get_property_comment(self, global_median: int, property: str) -> str:
        if self.dataframe[property].median() <= global_median:
            return (
                f"<span style='color:green'>{self.translations['good_result']} <b>{round(self.dataframe[property].median(), 2)}</b> "
                f"{self.translations['better_than']} <b>{global_median}</b></span>"
            )

        return (
            f"<span style='color:red'>{self.translations['bad_result']} <b>{round(self.dataframe[property].median(), 2)}</b> "
            f"{self.translations['worse_than']} <b>{global_median}</b></span>"
        )

    def create_report_file(self) -> None:
        template_vars = {
            "site": self.domain,
            "date": self.date,
            "nb_page": len(self.dataframe.index),
            "all_data": self.dataframe.to_html(
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
            "summary": self.dataframe[
                ["score", "size", "nodes", "requests", "ges", "water"]
            ]
            .describe(percentiles=[0.5])
            .loc[["mean", "50%", "min", "max"]]
            .round(2)
            .to_html(classes="table is-hoverable is-fullwidth is-bordered"),
            "best": self.dataframe.nlargest(n=10, columns="score")[
                ["url", "score", "size", "nodes", "requests"]
            ].to_html(classes="table is-hoverable is-fullwidth is-bordered"),
            "worst": self.dataframe.nsmallest(n=10, columns="score")[
                ["url", "score", "size", "nodes", "requests"]
            ].to_html(classes="table is-hoverable is-fullwidth is-bordered"),
            "size_comment": self.get_property_comment(
                global_median=GlobalMedian.size.value,
                property="size",
            ),
            "nodes_comment": self.get_property_comment(
                global_median=GlobalMedian.nodes.value,
                property="nodes",
            ),
            "requests_comment": self.get_property_comment(
                global_median=GlobalMedian.requests.value,
                property="requests",
            ),
        }

        env = Environment(
            loader=FileSystemLoader(f"{Path(__file__).parent.absolute()}")
        )
        template = env.get_template("template.html")
        html_out = template.render({**template_vars, **self.translations})

        with open(f"{self.output_path}/index.html", "w") as f:
            f.write(html_out)
