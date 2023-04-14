from os import remove

from typer.testing import CliRunner

from ecoindex_cli.cli.app import app

runner = CliRunner()


def test_analyze_no_args():
    result = runner.invoke(app=app, args=["analyze"])
    assert result.exit_code == 1
    assert "🔥 You must provide an url..." in result.stdout


def test_analyze_not_valid_url():
    invalid_url = "url"
    result = runner.invoke(app=app, args=["analyze", "--url", invalid_url])
    assert result.exit_code == 1
    assert (
        "invalid or missing URL scheme (type=value_error.url.scheme)" in result.stdout
    )


def test_analyze_one_invalid_url():
    valid_url = "https://www.test.com"
    invalid_url = "http://dummy"
    result = runner.invoke(
        app=app, args=["analyze", "--url", valid_url, "--url", invalid_url]
    )
    assert result.exit_code == 1
    assert (
        "1 validation error for GetUrlFromArgs\nurls_arg -> 1\n  URL host invalid, top level domain required (type=value_error.url.host)\n"
        in result.stdout
    )


def test_analyze_one_valid_url():
    domain = "www.test.com"
    valid_url = f"https://{domain}"
    result = runner.invoke(app=app, args=["analyze", "--url", valid_url], input="n\n")
    assert "There are 1 url(s), do you want to process?" in result.stdout
    assert result.exit_code == 1
    assert "Aborted" in result.stdout
    assert f"📁️ Urls recorded in file `input/{domain}.csv`"
    remove(f"/tmp/ecoindex-cli/input/{domain}.csv")


def test_analyze_string_window_size():
    invalid_window_size = "window"
    result = runner.invoke(
        app=app, args=["analyze", "--window-size", invalid_window_size]
    )
    assert result.exit_code == 1
    assert (
        f"🔥 `{invalid_window_size}` is not a valid window size. Must be of type `1920,1080`"
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
        f"🔥 `{invalid_window_size}` is not a valid window size. Must be of type `1920,1080`"
        in result.stdout
    )


def test_analyze_abort_recursive():
    result = runner.invoke(app=app, args=["analyze", "--recursive"], input="n\n")
    assert (
        "You are about to perform a recursive website scraping. This can take a long time. Are you sure to want to proceed?"
        in result.stdout
    )
    assert "Aborted" in result.stdout
    assert result.exit_code == 1


def test_no_interaction():
    result = runner.invoke(app=app, args=["analyze", "--recursive", "--no-interaction"])
    assert "[Y/n]" not in result.stdout
    assert result.exit_code == 1


def test_unauthorized_export_format():
    result = runner.invoke(app=app, args=["analyze", "--export-format", "txt"])
    assert result.exit_code == 2
    assert "'txt' is not one of 'csv', 'json'." in result.stdout
