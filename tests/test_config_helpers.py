"""
Tests for config-file discovery helpers (find_server_config + create_config
auto-discovery).
"""

from pathlib import Path

import pytest

from mcp_commons import MCPConfig, create_config, find_server_config


@pytest.fixture
def fake_home(tmp_path, monkeypatch):
    """Redirect Path.home() to a tmp dir so the lookup is hermetic."""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    return home


@pytest.fixture
def fake_cwd(tmp_path, monkeypatch):
    """Redirect Path.cwd() to a tmp dir so the lookup is hermetic."""
    cwd = tmp_path / "cwd"
    cwd.mkdir()
    monkeypatch.setattr(Path, "cwd", classmethod(lambda cls: cwd))
    return cwd


class TestFindServerConfig:
    """Lookup order: mcp-manager → extras → XDG → CWD → None."""

    def test_returns_none_when_no_candidate_exists(self, fake_home, fake_cwd):
        assert find_server_config("nope") is None

    def test_finds_mcp_manager_path(self, fake_home, fake_cwd):
        target = (
            fake_home
            / ".config"
            / "mcp-manager"
            / "servers"
            / "worldcontext"
            / "config.yaml"
        )
        target.parent.mkdir(parents=True)
        target.write_text("server: {}\n")

        result = find_server_config("worldcontext")
        assert result == target

    def test_skips_missing_and_picks_next_existing(self, fake_home, fake_cwd):
        # mcp-manager path missing; XDG path present
        xdg = fake_home / ".config" / "worldcontext" / "config.yaml"
        xdg.parent.mkdir(parents=True)
        xdg.write_text("server: {}\n")

        result = find_server_config("worldcontext")
        assert result == xdg

    def test_extra_locations_consulted_after_mcp_manager_before_xdg(
        self, fake_home, fake_cwd, tmp_path
    ):
        # mcp-manager path missing; extra location present; XDG also present.
        # Extras should win over XDG.
        extra = tmp_path / "custom" / "config.yaml"
        extra.parent.mkdir(parents=True)
        extra.write_text("server: {}\n")

        xdg = fake_home / ".config" / "worldcontext" / "config.yaml"
        xdg.parent.mkdir(parents=True)
        xdg.write_text("server: {}\n")

        result = find_server_config("worldcontext", extra_locations=[extra])
        assert result == extra

    def test_mcp_manager_wins_over_extras(self, fake_home, fake_cwd, tmp_path):
        target = (
            fake_home
            / ".config"
            / "mcp-manager"
            / "servers"
            / "worldcontext"
            / "config.yaml"
        )
        target.parent.mkdir(parents=True)
        target.write_text("server: {}\n")

        extra = tmp_path / "custom" / "config.yaml"
        extra.parent.mkdir(parents=True)
        extra.write_text("server: {}\n")

        result = find_server_config("worldcontext", extra_locations=[extra])
        assert result == target

    def test_falls_back_to_cwd_last(self, fake_home, fake_cwd):
        cwd_config = fake_cwd / "config.yaml"
        cwd_config.write_text("server: {}\n")

        result = find_server_config("worldcontext")
        assert result == cwd_config

    def test_custom_filename(self, fake_home, fake_cwd):
        target = (
            fake_home
            / ".config"
            / "mcp-manager"
            / "servers"
            / "mcpservercreator"
            / ".env"
        )
        target.parent.mkdir(parents=True)
        target.write_text("FOO=bar\n")

        result = find_server_config("mcpservercreator", filename=".env")
        assert result == target


class TestCreateConfigServerNameDiscovery:
    """Verify the new server_name kwarg in create_config."""

    def test_loads_from_mcp_manager_path(self, fake_home, fake_cwd):
        target = (
            fake_home / ".config" / "mcp-manager" / "servers" / "x" / "config.yaml"
        )
        target.parent.mkdir(parents=True)
        target.write_text("server:\n  name: from-file\n")

        config = create_config(server_name="x")
        assert isinstance(config, MCPConfig)
        assert config.get("server", "name") == "from-file"

    def test_no_file_anywhere_yields_empty_config(self, fake_home, fake_cwd):
        config = create_config(server_name="x")
        assert isinstance(config, MCPConfig)
        assert config.get("server", "name") is None

    def test_explicit_config_file_wins_over_server_name(
        self, fake_home, fake_cwd, tmp_path
    ):
        # File at the mcp-manager path:
        mcp_target = (
            fake_home / ".config" / "mcp-manager" / "servers" / "x" / "config.yaml"
        )
        mcp_target.parent.mkdir(parents=True)
        mcp_target.write_text("server:\n  name: from-mcp-manager\n")

        # File passed explicitly:
        explicit = tmp_path / "explicit.yaml"
        explicit.write_text("server:\n  name: from-explicit\n")

        config = create_config(config_file=str(explicit), server_name="x")
        assert config.get("server", "name") == "from-explicit"
