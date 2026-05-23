import base64
import re
import subprocess

import pytest

from color_banner.output import write_ansi_file, write_shell_export, write_stdout

SAMPLE_LINES = [
    "\x1b[38;2;255;0;0mH\x1b[0m",
    "\x1b[38;2;0;0;255mi\x1b[0m",
]
VERSION = "0.1.0"


def test_write_stdout_prints_lines(capsys):
    write_stdout(["line one", "line two"])
    captured = capsys.readouterr()
    assert "line one" in captured.out
    assert "line two" in captured.out


def test_write_ansi_file_creates_file(tmp_path):
    out = tmp_path / "banner.ans"
    write_ansi_file(SAMPLE_LINES, str(out), VERSION)
    assert out.exists()


def test_write_ansi_file_preserves_ansi_codes(tmp_path):
    out = tmp_path / "banner.ans"
    write_ansi_file(SAMPLE_LINES, str(out), VERSION)
    content = out.read_text(encoding="utf-8")
    assert "\x1b[38;2;255;0;0m" in content
    assert "\x1b[38;2;0;0;255m" in content


def test_write_ansi_file_contains_attribution(tmp_path):
    out = tmp_path / "banner.ans"
    write_ansi_file(SAMPLE_LINES, str(out), VERSION)
    content = out.read_text(encoding="utf-8")
    assert "Calligraphy" in content
    assert "GeopJr" in content


def test_write_ansi_file_roundtrip(tmp_path):
    out = tmp_path / "banner.ans"
    write_ansi_file(SAMPLE_LINES, str(out), VERSION)
    content = out.read_text(encoding="utf-8")
    for line in SAMPLE_LINES:
        assert line in content


def test_write_shell_export_creates_file(tmp_path):
    out = tmp_path / "splash.sh"
    write_shell_export(SAMPLE_LINES, str(out), VERSION)
    assert out.exists()


def test_write_shell_export_has_shebang(tmp_path):
    out = tmp_path / "splash.sh"
    write_shell_export(SAMPLE_LINES, str(out), VERSION)
    assert out.read_text(encoding="utf-8").startswith("#!/usr/bin/env bash")


def test_write_shell_export_contains_attribution(tmp_path):
    out = tmp_path / "splash.sh"
    write_shell_export(SAMPLE_LINES, str(out), VERSION)
    content = out.read_text(encoding="utf-8")
    assert "Calligraphy" in content
    assert "GeopJr" in content


def test_write_shell_export_default_function_name(tmp_path):
    out = tmp_path / "splash.sh"
    write_shell_export(SAMPLE_LINES, str(out), VERSION)
    content = out.read_text(encoding="utf-8")
    assert "show_banner()" in content


def test_write_shell_export_custom_function_name(tmp_path):
    out = tmp_path / "splash.sh"
    write_shell_export(SAMPLE_LINES, str(out), VERSION, function_name="my_splash")
    content = out.read_text(encoding="utf-8")
    assert "my_splash()" in content
    assert "show_banner" not in content


def test_write_shell_export_base64_decodes_to_original(tmp_path):
    out = tmp_path / "splash.sh"
    write_shell_export(SAMPLE_LINES, str(out), VERSION)
    content = out.read_text(encoding="utf-8")
    match = re.search(r"printf '%s' '([A-Za-z0-9+/=]+)'", content)
    assert match, "could not find base64 blob in export"
    decoded = base64.b64decode(match.group(1)).decode("utf-8")
    for line in SAMPLE_LINES:
        assert line in decoded


def test_write_shell_export_passes_bash_syntax_check(tmp_path):
    out = tmp_path / "splash.sh"
    write_shell_export(SAMPLE_LINES, str(out), VERSION)
    result = subprocess.run(
        ["bash", "-n", str(out)], capture_output=True, text=True
    )
    assert result.returncode == 0, f"bash -n failed:\n{result.stderr}"
