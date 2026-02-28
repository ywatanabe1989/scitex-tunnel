#!/usr/bin/env python3
"""Tests for scitex-tunnel CLI."""

from unittest.mock import patch

from click.testing import CliRunner

from scitex_tunnel.cli import main


class TestCLI:
    """CLI command tests."""

    def test_help(self):
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "setup" in result.output
        assert "remove" in result.output
        assert "status" in result.output

    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_setup_help(self):
        runner = CliRunner()
        result = runner.invoke(main, ["setup", "--help"])
        assert result.exit_code == 0
        assert "--port" in result.output
        assert "--bastion" in result.output
        assert "--secret-key" in result.output

    def test_remove_help(self):
        runner = CliRunner()
        result = runner.invoke(main, ["remove", "--help"])
        assert result.exit_code == 0
        assert "--port" in result.output

    def test_status_help(self):
        runner = CliRunner()
        result = runner.invoke(main, ["status", "--help"])
        assert result.exit_code == 0
        assert "--port" in result.output

    @patch("scitex_tunnel.status")
    def test_status_invocation(self, mock_status):
        mock_status.return_value = {
            "success": True,
            "stdout": "active tunnels",
            "stderr": "",
        }
        runner = CliRunner()
        result = runner.invoke(main, ["status"])
        assert result.exit_code == 0
        assert "active tunnels" in result.output

    def test_setup_missing_required(self):
        runner = CliRunner()
        result = runner.invoke(main, ["setup"])
        assert result.exit_code != 0

    def test_remove_missing_required(self):
        runner = CliRunner()
        result = runner.invoke(main, ["remove"])
        assert result.exit_code != 0


# EOF
