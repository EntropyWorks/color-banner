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


def test_list_fonts_numbered_format():
    """--list-fonts prints '001 fontname' format."""
    result = run(["--list-fonts"])
    lines = result.stdout.strip().splitlines()
    assert lines[0].startswith("001 ")
    from color_banner.renderer import list_fonts
    total = len(list_fonts())
    assert lines[-1].startswith(f"{total:03d} ")

def test_list_fonts_number_count():
    """--list-fonts line count equals total pyfiglet fonts."""
    from color_banner.renderer import list_fonts
    result = run(["--list-fonts"])
    lines = result.stdout.strip().splitlines()
    assert len(lines) == len(list_fonts())


def test_font_by_number():
    """--font 001 renders same as --font <first_font>."""
    from color_banner.renderer import list_fonts
    first_font = list_fonts()[0]
    result_by_name = run(["Hello", "--font", first_font, "--no-color"])
    result_by_num = run(["Hello", "--font", "001", "--no-color"])
    assert result_by_num.stdout == result_by_name.stdout


def test_font_by_zero_padded_number():
    """--font 001 matches --font 1."""
    result_1 = run(["Hello", "--font", "1", "--no-color"])
    result_001 = run(["Hello", "--font", "001", "--no-color"])
    assert result_1.stdout == result_001.stdout


def test_font_by_number_out_of_range():
    """--font 9999 exits with code 1 and mentions 'out of range'."""
    result = run(["Hello", "--font", "9999"])
    assert result.returncode == 1
    assert "out of range" in result.stderr


def test_all_flag_renders_multiple_fonts():
    """--all renders banners for all fonts."""
    result = run(["Hi", "--all", "--no-color"])
    assert result.returncode == 0
    assert "--- 001 " in result.stdout
    assert "--- 002 " in result.stdout

def test_all_flag_requires_text():
    """--all without TEXT exits with code 1."""
    result = run(["--all", "--no-color"])
    assert result.returncode == 1
    assert "TEXT is required" in result.stderr


def test_all_flag_header_format():
    """--all output has '--- NNN fontname ---' headers for every font."""
    result = run(["X", "--all", "--no-color"])
    lines = result.stdout.splitlines()
    headers = [l for l in lines if l.startswith("--- ") and l.endswith(" ---")]
    from color_banner.renderer import list_fonts
    assert len(headers) == len(list_fonts())
    assert headers[0].startswith("--- 001 ")
    assert headers[0].endswith(" ---")


def test_save_all_creates_files(tmp_path):
    """--save-all DIR creates NNN-fontname.ans files."""
    out_dir = tmp_path / "all_banners"
    result = run(["Hi", "--save-all", str(out_dir), "--no-color"])
    assert result.returncode == 0
    files = sorted(out_dir.glob("*.ans"))
    from color_banner.renderer import list_fonts
    assert len(files) == len(list_fonts())
    assert files[0].name.startswith("001-")

def test_save_all_requires_text(tmp_path):
    """--save-all without TEXT exits with code 1."""
    out_dir = tmp_path / "banners"
    result = run(["--save-all", str(out_dir)])
    assert result.returncode == 1
    assert "TEXT is required" in result.stderr


def test_save_all_creates_deep_dirs(tmp_path):
    """--save-all auto-creates nested output directory."""
    out_dir = tmp_path / "a" / "b" / "c" / "banners"
    result = run(["Hi", "--save-all", str(out_dir), "--no-color"])
    assert result.returncode == 0
    assert out_dir.is_dir()


# --- --list-fonts readable ---

def test_list_fonts_readable_is_subset():
    """--list-fonts readable returns fewer fonts than --list-fonts."""
    all_result = run(["--list-fonts"])
    readable_result = run(["--list-fonts", "readable"])
    assert readable_result.returncode == 0
    all_lines = all_result.stdout.strip().splitlines()
    readable_lines = readable_result.stdout.strip().splitlines()
    assert len(readable_lines) < len(all_lines)


def test_list_fonts_readable_excludes_doh():
    """--list-fonts readable must not include 'doh' (75 rows)."""
    result = run(["--list-fonts", "readable"])
    assert "doh" not in result.stdout


def test_list_fonts_readable_excludes_term():
    """--list-fonts readable must not include 'term' (plain passthrough)."""
    result = run(["--list-fonts", "readable"])
    assert " term" not in result.stdout


def test_list_fonts_readable_includes_slant():
    """--list-fonts readable must include 'slant'."""
    result = run(["--list-fonts", "readable"])
    assert "slant" in result.stdout


def test_list_fonts_readable_preserves_original_numbers():
    """Numbers in --list-fonts readable match the full --list-fonts numbering."""
    full = {line.split()[1]: line.split()[0]
            for line in run(["--list-fonts"]).stdout.strip().splitlines()}
    for line in run(["--list-fonts", "readable"]).stdout.strip().splitlines():
        num, name = line.split(None, 1)
        assert full[name] == num, f"{name}: expected {full[name]}, got {num}"


def test_list_fonts_invalid_filter():
    """--list-fonts with an unrecognised filter exits with code 1."""
    result = run(["--list-fonts", "garbage"])
    assert result.returncode == 1
    assert "readable" in result.stderr
