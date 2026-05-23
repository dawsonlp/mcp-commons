"""
Tests for setup_logging (stderr default + new kwargs) and run_cli.
"""

import logging
import sys

import pytest

from mcp_commons import run_cli, setup_logging


@pytest.fixture
def clean_root():
    """Snapshot root logger handlers; clear inside the test body to defeat
    pytest's LogCaptureHandler, then restore on teardown."""
    root = logging.root
    original_handlers = list(root.handlers)
    original_level = root.level

    def clear():
        root.handlers.clear()

    yield clear
    root.handlers.clear()
    root.handlers.extend(original_handlers)
    root.setLevel(original_level)


class TestSetupLogging:
    def test_default_stream_is_stderr(self, clean_root):
        clean_root()
        setup_logging()
        handler = logging.root.handlers[0]
        assert isinstance(handler, logging.StreamHandler)
        assert handler.stream is sys.stderr

    def test_explicit_stdout(self, clean_root):
        clean_root()
        setup_logging(stream=sys.stdout)
        handler = logging.root.handlers[0]
        assert isinstance(handler, logging.StreamHandler)
        assert handler.stream is sys.stdout

    def test_log_file_attaches_file_handler(self, clean_root, tmp_path):
        log_path = tmp_path / "x.log"
        clean_root()
        setup_logging(log_file=log_path)
        handler = logging.root.handlers[0]
        assert isinstance(handler, logging.FileHandler)
        assert handler.baseFilename == str(log_path)

        logging.getLogger("test").warning("hello")
        for h in logging.root.handlers:
            h.flush()
        assert log_path.exists()
        assert "hello" in log_path.read_text()

    def test_transport_kwarg_accepted(self, clean_root):
        # Forward-compat smoke test — currently ignored, must not raise.
        clean_root()
        setup_logging(transport="stdio")
        clean_root()
        setup_logging(transport="sse")
        clean_root()
        setup_logging(transport=None)


class _RunMcpServerStub:
    """Records the kwargs passed to run_mcp_server without actually running."""

    def __init__(self):
        self.calls: list[dict] = []

    def __call__(self, **kwargs):
        self.calls.append(kwargs)


@pytest.fixture
def stub_run(monkeypatch):
    stub = _RunMcpServerStub()
    monkeypatch.setattr("mcp_commons.server.run_mcp_server", stub)
    return stub


class TestRunCliHelp:
    @pytest.mark.parametrize("flag", ["help", "--help", "-h"])
    def test_help_returns_without_running(self, flag, stub_run, capsys):
        run_cli("srv", {}, argv=[flag])
        assert stub_run.calls == []
        out = capsys.readouterr().out
        assert "srv" in out

    def test_no_args_prints_help(self, stub_run, capsys):
        run_cli("srv", {}, argv=[])
        assert stub_run.calls == []
        assert "srv" in capsys.readouterr().out


class TestRunCliErrors:
    def test_bogus_transport_exits_2(self, stub_run):
        with pytest.raises(SystemExit) as exc:
            run_cli("srv", {}, argv=["bogus"])
        assert exc.value.code == 2
        assert stub_run.calls == []

    def test_missing_transport_value_exits_2(self, stub_run):
        with pytest.raises(SystemExit) as exc:
            run_cli("srv", {}, argv=["--transport"])
        assert exc.value.code == 2
        assert stub_run.calls == []

    def test_streamable_http_rejected_by_default(self, stub_run):
        with pytest.raises(SystemExit) as exc:
            run_cli("srv", {}, argv=["streamable-http"])
        assert exc.value.code == 2


class TestRunCliSuccess:
    def test_stdio_no_host_port(self, stub_run):
        run_cli("srv", {"t": {}}, argv=["stdio"])
        assert len(stub_run.calls) == 1
        kwargs = stub_run.calls[0]
        assert kwargs["transport"] == "stdio"
        assert kwargs["server_name"] == "srv"
        assert "host" not in kwargs
        assert "port" not in kwargs

    def test_sse_includes_host_port(self, stub_run):
        run_cli("srv", {"t": {}}, argv=["sse"], host="0.0.0.0", port=9000)
        kwargs = stub_run.calls[0]
        assert kwargs["transport"] == "sse"
        assert kwargs["host"] == "0.0.0.0"
        assert kwargs["port"] == 9000

    def test_two_token_transport_form(self, stub_run):
        run_cli("srv", {}, argv=["--transport", "stdio"])
        kwargs = stub_run.calls[0]
        assert kwargs["transport"] == "stdio"
        assert "host" not in kwargs

    def test_streamable_http_accepted_when_whitelisted(self, stub_run):
        run_cli(
            "srv",
            {},
            argv=["streamable-http"],
            transports=("stdio", "sse", "streamable-http"),
        )
        kwargs = stub_run.calls[0]
        assert kwargs["transport"] == "streamable-http"
        assert kwargs["host"] == "localhost"
        assert kwargs["port"] == 7501
