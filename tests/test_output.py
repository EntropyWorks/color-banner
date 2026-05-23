import base64
import re
import subprocess

import pytest

from color_banner.output import write_ansi_file, write_ansi_files_all, write_shell_export, write_stdout

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


def test_write_shell_export_no_command_substitution(tmp_path):
    """base64 decode pipes directly to stdout — no $() to strip trailing newlines."""
    out = tmp_path / "splash.sh"
    write_shell_export(SAMPLE_LINES, str(out), VERSION)
    content = out.read_text(encoding="utf-8")
    assert "$(printf" not in content
    assert "| base64 -d" in content


def test_write_shell_export_preserves_trailing_newline(tmp_path):
    """Banner output ends with a newline so the shell prompt appears on its own line."""
    out = tmp_path / "splash.sh"
    write_shell_export(SAMPLE_LINES, str(out), VERSION)
    result = subprocess.run(["bash", str(out)], capture_output=True)
    assert result.stdout.endswith(b"\n"), "banner output missing trailing newline"


def test_write_shell_export_contains_base64_guard(tmp_path):
    """Generated script checks base64 availability and returns 1 if missing."""
    out = tmp_path / "splash.sh"
    write_shell_export(SAMPLE_LINES, str(out), VERSION)
    content = out.read_text(encoding="utf-8")
    assert "command -v base64" in content
    assert "return 1" in content


def test_write_shell_export_invalid_function_name_raises(tmp_path):
    """write_shell_export rejects names that are not valid bash identifiers."""
    out = tmp_path / "splash.sh"
    bad_names = [
        "foo bar",       # space
        "123bad",        # starts with digit
        "foo;bar",       # semicolon
        "foo\nbar",      # newline
        "foo$(evil)",    # command substitution
        "",              # empty
        "foo-bar",       # hyphen (invalid in bash identifiers)
    ]
    for name in bad_names:
        with pytest.raises(ValueError, match="invalid function name"):
            write_shell_export(SAMPLE_LINES, str(out), VERSION, function_name=name)


def test_write_shell_export_valid_function_names(tmp_path):
    """write_shell_export accepts any valid bash identifier."""
    valid_names = ["show_banner", "_splash", "banner123", "MY_BANNER", "_"]
    for name in valid_names:
        out = tmp_path / f"{name}.sh"
        write_shell_export(SAMPLE_LINES, str(out), VERSION, function_name=name)
        assert name + "()" in out.read_text(encoding="utf-8")


def test_write_ansi_file_creates_parent_dirs(tmp_path):
    """write_ansi_file creates parent directories automatically."""
    deep_path = tmp_path / "a" / "b" / "c" / "banner.ans"
    write_ansi_file(["line1", "line2"], str(deep_path), "0.1.0")
    assert deep_path.exists()
    content = deep_path.read_text()
    assert "line1" in content


def test_write_ansi_files_all_creates_dir(tmp_path):
    """write_ansi_files_all creates the output directory if missing."""
    out_dir = tmp_path / "banners"
    assert not out_dir.exists()
    write_ansi_files_all([], str(out_dir), "0.1.0")
    assert out_dir.is_dir()


def test_write_ansi_files_all_creates_files(tmp_path):
    """write_ansi_files_all writes NNN-fontname.ans files."""
    out_dir = tmp_path / "out"
    font_banners = [
        (1, "slant", ["line1", "line2"]),
        (42, "ogre", ["banner42"]),
    ]
    write_ansi_files_all(font_banners, str(out_dir), "0.1.0")
    assert (out_dir / "001-slant.ans").exists()
    assert (out_dir / "042-ogre.ans").exists()


def test_write_ansi_files_all_content(tmp_path):
    """Each .ans file contains the banner lines, attribution, and font header."""
    out_dir = tmp_path / "out"
    write_ansi_files_all(
        [(5, "banner", ["hello", "world"])], str(out_dir), "0.2.0"
    )
    content = (out_dir / "005-banner.ans").read_text()
    assert "hello" in content
    assert "world" in content
    assert "color-banner" in content
    assert "# Font: banner (#005)" in content
