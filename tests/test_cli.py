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


def test_export_invalid_function_name_exits_nonzero(tmp_path):
    """--function-name with shell metacharacters exits with code 1."""
    out = tmp_path / "splash.sh"
    result = run(["Hi", "--export", str(out), "--function-name", "foo bar"])
    assert result.returncode == 1
    assert "invalid function name" in result.stderr


def test_export_function_name_newline_rejected(tmp_path):
    """--function-name with a newline is rejected."""
    out = tmp_path / "splash.sh"
    result = run(["Hi", "--export", str(out), "--function-name", "foo\nbar"])
    assert result.returncode == 1
    assert "invalid function name" in result.stderr


def test_export_function_name_starts_with_digit_rejected(tmp_path):
    """--function-name starting with a digit is rejected."""
    out = tmp_path / "splash.sh"
    result = run(["Hi", "--export", str(out), "--function-name", "123bad"])
    assert result.returncode == 1
    assert "invalid function name" in result.stderr


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


# --- --width ---

def test_width_flag_prevents_wrapping(tmp_path):
    """--width 200 prevents line-wrapping that occurs at the default 80."""
    # 'block' font renders 'Hello World' wider than 80 cols — wraps by default
    out_80 = tmp_path / "w80.ans"
    out_200 = tmp_path / "w200.ans"
    run(["Hello World", "--font", "block", "--no-color", "--save", str(out_80)])
    run(["Hello World", "--font", "block", "--no-color", "--width", "200", "--save", str(out_200)])
    lines_80 = [l for l in out_80.read_text().splitlines() if not l.startswith("#") and l.strip()]
    lines_200 = [l for l in out_200.read_text().splitlines() if not l.startswith("#") and l.strip()]
    assert len(lines_80) > len(lines_200)


def test_width_zero_never_wraps(tmp_path):
    """--width 0 produces same output as --width 32767."""
    out_0 = tmp_path / "w0.ans"
    out_huge = tmp_path / "whuge.ans"
    run(["Hello World", "--font", "block", "--no-color", "--width", "0", "--save", str(out_0)])
    run(["Hello World", "--font", "block", "--no-color", "--width", "32767", "--save", str(out_huge)])
    # Strip headers and compare content lines
    def content_lines(p):
        return [l for l in p.read_text().splitlines() if not l.startswith("#")]
    assert content_lines(out_0) == content_lines(out_huge)


def test_width_invalid_value():
    """--width with a non-integer value exits with code 2 (argparse error)."""
    result = run(["Hello", "--width", "abc"])
    assert result.returncode == 2


def test_width_negative_value():
    """--width with a negative number exits with code 1."""
    result = run(["Hello", "--width", "-5"])
    assert result.returncode == 1
    assert "width" in result.stderr


# --- --all readable ---

def test_all_readable_is_subset_of_all():
    """--all readable renders fewer fonts than --all."""
    from color_banner.renderer import list_fonts, readable_fonts
    result_all = run(["X", "--all", "--no-color"])
    result_readable = run(["X", "--all", "readable", "--no-color"])
    all_headers = [l for l in result_all.stdout.splitlines()
                   if l.startswith("--- ") and l.endswith(" ---")]
    readable_headers = [l for l in result_readable.stdout.splitlines()
                        if l.startswith("--- ") and l.endswith(" ---")]
    assert len(readable_headers) < len(all_headers)
    assert len(readable_headers) == len(readable_fonts())


def test_all_readable_excludes_doh():
    """--all readable must not render the 'doh' font (75 rows, too tall)."""
    result = run(["X", "--all", "readable", "--no-color"])
    assert "doh" not in result.stdout


def test_all_readable_includes_slant():
    """--all readable must include the 'slant' font."""
    result = run(["X", "--all", "readable", "--no-color"])
    assert "slant" in result.stdout


def test_all_no_arg_still_renders_all():
    """--all (no filter) still renders all fonts."""
    from color_banner.renderer import list_fonts
    result = run(["X", "--all", "--no-color"])
    headers = [l for l in result.stdout.splitlines()
               if l.startswith("--- ") and l.endswith(" ---")]
    assert len(headers) == len(list_fonts())


def test_all_invalid_filter():
    """--all with an unrecognised filter exits with code 1."""
    result = run(["X", "--all", "garbage"])
    assert result.returncode == 1
    assert "readable" in result.stderr


# --- --save-all DIR --readable ---

def test_save_all_readable_creates_fewer_files(tmp_path):
    """--save-all DIR --readable creates fewer files than --save-all DIR."""
    from color_banner.renderer import list_fonts, readable_fonts
    all_dir = tmp_path / "all"
    readable_dir = tmp_path / "readable"
    run(["Hi", "--save-all", str(all_dir), "--no-color"])
    run(["Hi", "--save-all", str(readable_dir), "--readable", "--no-color"])
    assert len(list(readable_dir.glob("*.ans"))) < len(list(all_dir.glob("*.ans")))
    assert len(list(readable_dir.glob("*.ans"))) == len(readable_fonts())


def test_save_all_readable_excludes_doh(tmp_path):
    """--save-all DIR --readable must not save the 'doh' font."""
    out_dir = tmp_path / "out"
    run(["Hi", "--save-all", str(out_dir), "--readable", "--no-color"])
    names = [f.name for f in out_dir.glob("*.ans")]
    assert not any("doh" in n for n in names)


def test_save_all_readable_preserves_original_numbers(tmp_path):
    """Font numbers in --save-all --readable files match original numbering."""
    from color_banner.renderer import numbered_fonts
    num_map = {name: f"{n:03d}" for n, name in numbered_fonts()}
    out_dir = tmp_path / "out"
    run(["Hi", "--save-all", str(out_dir), "--readable", "--no-color"])
    for f in out_dir.glob("*.ans"):
        parts = f.stem.split("-", 1)
        file_num, font_name = parts[0], parts[1]
        assert num_map[font_name] == file_num
