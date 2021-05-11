from os import getcwd, remove

from cli import analyze, app
from typer.testing import CliRunner

runner = CliRunner()


def test_analyze_no_args():
    result = runner.invoke(app=app, args=["analyze"])
    assert result.exit_code == 1
    assert "🔥 You must provide an url..." in result.stdout


def test_analyze_not_valid_url():
    invalid_url = "url"
    result = runner.invoke(app=app, args=["analyze", "--url", invalid_url])
    assert result.exit_code == 1
    assert f"🔥 {invalid_url} is not a valid url" in result.stdout


def test_analyze_one_invalid_url():
    valid_url = "https://www.test.com"
    invalid_url = "http://dummy"
    result = runner.invoke(
        app=app, args=["analyze", "--url", valid_url, "--url", invalid_url]
    )
    assert result.exit_code == 1
    assert f"🔥 {invalid_url} is not a valid url" in result.stdout


def test_analyze_one_valid_url():
    domain = "www.test.com"
    valid_url = f"https://{domain}"
    result = runner.invoke(app=app, args=["analyze", "--url", valid_url], input="n\n")
    assert "There are 1 url(s), do you want to process?" in result.stdout
    assert result.exit_code == 1
    assert "Aborted!" in result.stdout
    assert f"📁️ Urls recorded in file `input/{domain}.csv`"
    remove(f"{getcwd()}/input/{domain}.csv")


def test_analyze_string_window_size():
    invalid_window_size = "window"
    result = runner.invoke(
        app=app, args=["analyze", "--window-size", invalid_window_size]
    )
    assert result.exit_code == 1
    assert (
        f"Invalid value: 🔥 {invalid_window_size} is not a valid window size. Must be of type 1920,1080"
        in result.stdout
    )


def test_analyze_one_invalid_window_size():
    valid_window_size = "1920,1080"
    invalid_window_size = "1920,height"
    result = runner.invoke(
        app=app,
        args=[
            "analyze",
            "--window-size",
            valid_window_size,
            "--window-size",
            invalid_window_size,
        ],
    )
    assert result.exit_code == 1
    assert (
        f"Invalid value: 🔥 {invalid_window_size} is not a valid window size. Must be of type 1920,1080"
        in result.stdout
    )


def test_analyze_abort_recursive():
    result = runner.invoke(app=app, args=["analyze", "--recursive"], input="n\n")
    assert (
        "You are about to perform a recursive website scraping. This can take a long time. Are you sure to want to proceed?"
        in result.stdout
    )
    assert "Aborted!" in result.stdout
    assert result.exit_code == 1
