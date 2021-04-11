from sptest import __main__, __version__
from typer.testing import CliRunner

runner = CliRunner()


def test_version():
    assert __version__ == "0.1.0"


def test_servers():
    result = runner.invoke(__main__.app, ["servers", "--server-limit=1", "--ping-num=1"])
    assert result.exit_code == 0
    assert "check" in result.stdout
    assert "Server list sorted by latency_median" in result.stdout
