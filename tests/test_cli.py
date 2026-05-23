import subprocess
import sys
from pathlib import Path

import pytest


def run(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run color-banner via uv and return the completed process."""
    return subprocess.run(
        ["uv", "run", "color-banner", *args],
        capture_output=True,
        text=True,
        **kwargs,
    )


def test_version_flag():
    result = run(["--version"])
    assert result.returncode == 0
    assert "0.1.0" in result.stdout


def test_list_palettes():
    result = run(["--list-palettes"])
    assert result.returncode == 0
    for name in ("neon", "sunset", "ocean", "fire", "ice", "rainbow"):
        assert name in result.stdout


def test_list_fonts():
    result = run(["--list-fonts"])
    assert result.returncode == 0
    assert "slant" in result.stdout
    assert "ogre" in result.stdout


def test_basic_render_exits_zero():
    result = run(["Hello", "--palette", "neon", "--no-color"])
    assert result.returncode == 0
    assert len(result.stdout.strip()) > 0


def test_stdout_has_ansi_codes_when_palette_given(tmp_path):
    # write to a file so we can inspect without TTY detection stripping codes
    out = tmp_path / "banner.ans"
    result = run(["Hello", "--palette", "neon", "--save", str(out)])
    assert result.returncode == 0
    content = out.read_text(encoding="utf-8")
    assert "\x1b[38;2;" in content


def test_direction_tb(tmp_path):
    out = tmp_path / "banner.ans"
    result = run(["Hi", "--palette", "fire", "--direction", "tb", "--save", str(out)])
    assert result.returncode == 0
    content = out.read_text(encoding="utf-8")
    assert "\x1b[38;2;" in content


def test_direction_bt(tmp_path):
    out = tmp_path / "banner.ans"
    result = run(["Hi", "--palette", "fire", "--direction", "bt", "--save", str(out)])
    assert result.returncode == 0


def test_direction_diag(tmp_path):
    out = tmp_path / "banner.ans"
    result = run(["Hi", "--palette", "neon", "--direction", "diag", "--save", str(out)])
    assert result.returncode == 0


def test_custom_gradient(tmp_path):
    out = tmp_path / "banner.ans"
    result = run(["Hi", "--gradient", "#ff0080", "#00d4ff", "--save", str(out)])
    assert result.returncode == 0
    content = out.read_text(encoding="utf-8")
    assert "\x1b[38;2;" in content


def test_no_color_flag_produces_no_ansi():
    result = run(["Hello", "--no-color"])
    assert result.returncode == 0
    assert "\x1b[" not in result.stdout


def test_export_produces_valid_shell(tmp_path):
    out = tmp_path / "splash.sh"
    result = run(["Hi", "--palette", "neon", "--export", str(out)])
    assert result.returncode == 0
    check = subprocess.run(["bash", "-n", str(out)], capture_output=True, text=True)
    assert check.returncode == 0


def test_export_custom_function_name(tmp_path):
    out = tmp_path / "splash.sh"
    result = run(
        ["Hi", "--palette", "neon", "--export", str(out),
         "--function-name", "my_banner"]
    )
    assert result.returncode == 0
    assert "my_banner()" in out.read_text(encoding="utf-8")


def test_unknown_palette_exits_nonzero():
    result = run(["Hello", "--palette", "notapalette"])
    assert result.returncode == 1
    assert "unknown palette" in result.stderr


def test_unknown_font_exits_nonzero():
    result = run(["Hello", "--font", "notafont_xyz"])
    assert result.returncode == 1
    assert "unknown font" in result.stderr


def test_gradient_invalid_hex_exits_nonzero():
    result = run(["Hello", "--gradient", "#ff0000", "notahex"])
    assert result.returncode == 1
    assert "expected #RRGGBB" in result.stderr


def test_gradient_single_stop_exits_nonzero():
    result = run(["Hello", "--gradient", "#ff0000"])
    assert result.returncode == 1
    assert "at least 2 color stops" in result.stderr


def test_missing_text_exits_nonzero():
    result = run([])
    assert result.returncode == 1
    assert "TEXT is required" in result.stderr


def test_piped_stdout_strips_ansi_codes():
    # When stdout is piped (non-TTY), ANSI codes should be auto-stripped.
    # subprocess.run with capture_output=True is always non-TTY.
    # Use --palette without --no-color to confirm TTY detection (not the flag) strips it.
    result = run(["Hello", "--palette", "neon"])
    assert result.returncode == 0
    assert "\x1b[" not in result.stdout


def test_save_and_export_simultaneously(tmp_path):
    ans_out = tmp_path / "banner.ans"
    sh_out = tmp_path / "splash.sh"
    result = run([
        "Hi", "--palette", "neon",
        "--save", str(ans_out),
        "--export", str(sh_out),
    ])
    assert result.returncode == 0
    assert ans_out.exists()
    assert sh_out.exists()
    assert "\x1b[38;2;" in ans_out.read_text(encoding="utf-8")
    check = subprocess.run(["bash", "-n", str(sh_out)], capture_output=True, text=True)
    assert check.returncode == 0
