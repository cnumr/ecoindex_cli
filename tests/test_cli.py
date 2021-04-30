from cli import app
from click.core import invoke_param_callback
from typer.testing import CliRunner

runner = CliRunner()


def test_no_args():
    result = runner.invoke(app=app, args=[])
    assert result.exit_code == 1
    assert "🔥 You must provide an url..." in result.stdout


def test_not_valid_url():
    invalid_url = "url"
    result = runner.invoke(app=app, args=["--url", invalid_url])
    assert result.exit_code == 1
    assert f"🔥 {invalid_url} is not a valid url" in result.stdout


def test_one_invalid_url():
    valid_url = "https://www.test.com"
    invalid_url = "http://dummy"
    result = runner.invoke(app=app, args=["--url", valid_url, "--url", invalid_url])
    assert result.exit_code == 1
    assert f"🔥 {invalid_url} is not a valid url" in result.stdout


def test_string_window_size():
    invalid_window_size = "window"
    result = runner.invoke(app=app, args=["--window-size", invalid_window_size])
    assert result.exit_code == 1
    assert (
        f"🔥 ('{invalid_window_size}',) is not a valid window_size. Must be of type ('1920,1080',...)"
        in result.stdout
    )


def test_one_invalid_window_size_():
    valid_window_size = "1920,1080"
    invalid_window_size = "1920,height"
    result = runner.invoke(
        app=app,
        args=["--window-size", valid_window_size, "--window-size", invalid_window_size],
    )
    assert result.exit_code == 1
    assert (
        f"🔥 ('{valid_window_size}', '{invalid_window_size}') is not a valid window_size. Must be of type ('1920,1080',...)"
        in result.stdout
    )


def test_abort_process():
    result = runner.invoke(app=app, args=["--url", "https://www.test.com"], input="n\n")
    assert result.exit_code == 1
    assert "Aborted!" in result.stdout
