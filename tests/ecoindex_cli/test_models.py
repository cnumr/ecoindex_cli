from pydantic.error_wrappers import ValidationError
from pytest import raises

from ecoindex_cli.models import Page, Result


def test_model_page():
    logs = ["Logs of my page"]
    outer_html = "Html of my page"
    nodes = ["node1", "node2", "node3"]

    page = Page(
        logs=logs,
        outer_html=outer_html,
        nodes=nodes,
    )

    assert page.logs == logs
    assert page.outer_html == outer_html
    assert page.nodes == nodes

    with raises(ValidationError):
        Page(logs=logs)


def test_result_model():
    result = Result(size=2500, nodes=500, requests=100)
    assert result.score is None
    assert result.page_type is None
    assert result.size == 2500
    assert result.nodes == 500
    assert result.requests == 100
