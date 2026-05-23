# color-banner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a standalone `color-banner` CLI tool that renders text as 24-bit true-color figlet ASCII banners, saveable as ANSI files or base64-encoded shell snippets.

> **NixOS note:** If Python package issues arise during development, escape to `distrobox enter debian-toolbox` and restart Claude Code from that shell.

**Architecture:** Thin fork of Calligraphy's concept — pyfiglet renders ASCII rows, a pure color engine computes gradients, a painter wraps chars in ANSI escapes, and an output module handles stdout / file / shell export. No circular dependencies; color.py and painter.py are pure functions with no I/O.

**Tech Stack:** Python ≥ 3.11, pyfiglet, pytest, uv (package manager)

---

## File Map

| File | Responsibility |
|------|---------------|
| `pyproject.toml` | Packaging, entry point, deps, dev deps |
| `LICENSE` | GPL v3 full text |
| `CREDITS.md` | Attribution to Calligraphy / GeopJr |
| `README.md` | Usage docs |
| `src/color_banner/__init__.py` | Package init, `__version__` |
| `src/color_banner/color.py` | `PALETTES`, `parse_hex`, `lerp_color`, `gradient_color`, `resolve_stops` |
| `src/color_banner/renderer.py` | `render(text, font) → list[str]`, `list_fonts() → list[str]` |
| `src/color_banner/painter.py` | `paint(rows, stops, direction, no_color) → list[str]` |
| `src/color_banner/output.py` | `write_stdout`, `write_ansi_file`, `write_shell_export` |
| `src/color_banner/cli.py` | `main()` — argparse, wires all modules |
| `tests/test_color.py` | Tests for color.py |
| `tests/test_renderer.py` | Tests for renderer.py |
| `tests/test_painter.py` | Tests for painter.py |
| `tests/test_output.py` | Tests for output.py |
| `tests/test_cli.py` | Integration tests via subprocess |

---

## Task 1: Project Scaffold

**Files:**
- Create: `pyproject.toml`
- Create: `src/color_banner/__init__.py`
- Create: `LICENSE`
- Create: `CREDITS.md`
- Create: `README.md`
- Create: `tests/__init__.py`

- [ ] **Step 1: Initialise the project with uv**

```bash
cd /path/to/color-banner
uv init --lib --name color-banner --python 3.11
```

This creates a basic pyproject.toml and src/ layout. We'll overwrite it in the next step.

- [ ] **Step 2: Write pyproject.toml**

Replace the generated `pyproject.toml` with:

```toml
[project]
name = "color-banner"
version = "0.1.0"
description = "Colorful figlet ASCII banners for terminals, CICD pipelines, and shell splash screens"
readme = "README.md"
license = { text = "GPL-3.0-or-later" }
requires-python = ">=3.11"
dependencies = [
    "pyfiglet>=1.0.2",
]

[project.scripts]
color-banner = "color_banner.cli:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/color_banner"]

[dependency-groups]
dev = [
    "pytest>=8.0",
]
```

- [ ] **Step 3: Write `src/color_banner/__init__.py`**

```python
# SPDX-License-Identifier: GPL-3.0-or-later
# Based on Calligraphy by GeopJr <https://codeberg.org/GeopJr/Calligraphy>
# Originally by Gregor "gregorni" Niehl

__version__ = "0.1.0"
```

- [ ] **Step 4: Write `CREDITS.md`**

```markdown
# Credits

color-banner is inspired by and based on the concept from
[Calligraphy](https://codeberg.org/GeopJr/Calligraphy)
by GeopJr and originally by Gregor "gregorni" Niehl.

Calligraphy is licensed under GPL v3. color-banner is therefore
also licensed under GPL v3.

The figlet font rendering relies on [pyfiglet](https://github.com/pwaller/pyfiglet).
```

- [ ] **Step 5: Write `LICENSE`**

Download the GPL v3 full text:

```bash
curl -o LICENSE https://www.gnu.org/licenses/gpl-3.0.txt
```

- [ ] **Step 6: Write a skeleton `README.md`**

```markdown
# color-banner

Render text as colorful 24-bit figlet ASCII banners in the terminal.
Inspired by [Calligraphy](https://codeberg.org/GeopJr/Calligraphy) by GeopJr.

## Install

```bash
uv tool install color-banner
```

## Usage

```bash
# print to terminal
color-banner "Hello" --palette neon --direction tb

# save a cat-able ANSI file
color-banner "Deploy v2" --palette fire --direction diag --save splash.ans
cat splash.ans

# export a self-contained shell function
color-banner "Deploy v2" --palette fire --export splash.sh
bash splash.sh

# custom hex gradient
color-banner "Hello" --gradient "#ff0080" "#7b2fff" "#00d4ff" --direction lr

# list available palettes
color-banner --list-palettes

# list available fonts
color-banner --list-fonts
```

## License

GPL v3. See [CREDITS.md](CREDITS.md) for attribution.
```

- [ ] **Step 7: Create `tests/__init__.py`** (empty file)

```bash
touch tests/__init__.py
```

- [ ] **Step 8: Install deps**

```bash
uv sync --dev
```

Expected: no errors, `pyfiglet` and `pytest` installed into `.venv/`.

- [ ] **Step 9: Verify pytest runs (empty suite)**

```bash
uv run pytest
```

Expected output contains: `no tests ran` or `0 passed`.

- [ ] **Step 10: Commit**

```bash
git add pyproject.toml src/ tests/ LICENSE CREDITS.md README.md
git commit -m "chore: project scaffold"
```

---

## Task 2: color.py — Hex Parsing and Palettes

**Files:**
- Create: `src/color_banner/color.py`
- Create: `tests/test_color.py`

- [ ] **Step 1: Write the failing tests for `parse_hex`**

Create `tests/test_color.py`:

```python
import pytest
from color_banner.color import PALETTES, parse_hex


def test_parse_hex_valid():
    assert parse_hex("#ff0080") == (255, 0, 128)


def test_parse_hex_lowercase():
    assert parse_hex("#aabbcc") == (170, 187, 204)


def test_parse_hex_black():
    assert parse_hex("#000000") == (0, 0, 0)


def test_parse_hex_white():
    assert parse_hex("#ffffff") == (255, 255, 255)


def test_parse_hex_invalid_no_hash():
    with pytest.raises(ValueError, match="expected #RRGGBB"):
        parse_hex("ff0080")


def test_parse_hex_invalid_too_short():
    with pytest.raises(ValueError, match="expected #RRGGBB"):
        parse_hex("#ff00")


def test_parse_hex_invalid_chars():
    with pytest.raises(ValueError, match="expected #RRGGBB"):
        parse_hex("#gggggg")


def test_palettes_all_have_at_least_two_stops():
    for name, stops in PALETTES.items():
        assert len(stops) >= 2, f"palette '{name}' has fewer than 2 stops"


def test_palettes_all_stops_are_valid_hex():
    for name, stops in PALETTES.items():
        for stop in stops:
            parse_hex(stop)  # raises ValueError if invalid
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_color.py -v
```

Expected: `ModuleNotFoundError` or `ImportError` — `color_banner.color` does not exist yet.

- [ ] **Step 3: Write `src/color_banner/color.py` with `parse_hex` and `PALETTES`**

```python
# SPDX-License-Identifier: GPL-3.0-or-later
# Based on Calligraphy by GeopJr <https://codeberg.org/GeopJr/Calligraphy>
# Originally by Gregor "gregorni" Niehl
from __future__ import annotations

PALETTES: dict[str, list[str]] = {
    "neon":    ["#ff00ff", "#7700ff", "#00bbff", "#00ffdd"],
    "sunset":  ["#ff6b35", "#f7931e", "#ffd700", "#ff4e50"],
    "ocean":   ["#006994", "#0099cc", "#00d4aa", "#00ff88"],
    "fire":    ["#ff0000", "#ff8800", "#ffcc00", "#ffff00"],
    "ice":     ["#88d8ff", "#44aaff", "#0066ff", "#0033cc"],
    "rainbow": ["#ff0000", "#ff8800", "#ffff00", "#00cc00", "#0044ff", "#8800ff"],
}


def parse_hex(hex_str: str) -> tuple[int, int, int]:
    """Parse '#RRGGBB' to (r, g, b). Raises ValueError on bad input."""
    s = hex_str.strip()
    if not (s.startswith("#") and len(s) == 7):
        raise ValueError(f"invalid color '{hex_str}': expected #RRGGBB")
    try:
        r = int(s[1:3], 16)
        g = int(s[3:5], 16)
        b = int(s[5:7], 16)
    except ValueError:
        raise ValueError(f"invalid color '{hex_str}': expected #RRGGBB")
    return (r, g, b)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_color.py -v
```

Expected: `9 passed`.

- [ ] **Step 5: Commit**

```bash
git add src/color_banner/color.py tests/test_color.py
git commit -m "feat: add color.py with parse_hex and PALETTES"
```

---

## Task 3: color.py — Gradient Math

**Files:**
- Modify: `src/color_banner/color.py`
- Modify: `tests/test_color.py`

- [ ] **Step 1: Replace `tests/test_color.py` with the full expanded version**

Overwrite the entire file with all tests (hex parsing from Task 2 + new gradient tests):

```python
import pytest
from color_banner.color import (
    PALETTES,
    gradient_color,
    lerp_color,
    parse_hex,
    resolve_stops,
)


def test_parse_hex_valid():
    assert parse_hex("#ff0080") == (255, 0, 128)


def test_parse_hex_lowercase():
    assert parse_hex("#aabbcc") == (170, 187, 204)


def test_parse_hex_black():
    assert parse_hex("#000000") == (0, 0, 0)


def test_parse_hex_white():
    assert parse_hex("#ffffff") == (255, 255, 255)


def test_parse_hex_invalid_no_hash():
    with pytest.raises(ValueError, match="expected #RRGGBB"):
        parse_hex("ff0080")


def test_parse_hex_invalid_too_short():
    with pytest.raises(ValueError, match="expected #RRGGBB"):
        parse_hex("#ff00")


def test_parse_hex_invalid_chars():
    with pytest.raises(ValueError, match="expected #RRGGBB"):
        parse_hex("#gggggg")


def test_palettes_all_have_at_least_two_stops():
    for name, stops in PALETTES.items():
        assert len(stops) >= 2, f"palette '{name}' has fewer than 2 stops"


def test_palettes_all_stops_are_valid_hex():
    for name, stops in PALETTES.items():
        for stop in stops:
            parse_hex(stop)


def test_lerp_color_at_zero():
    assert lerp_color((0, 0, 0), (255, 255, 255), 0.0) == (0, 0, 0)


def test_lerp_color_at_one():
    assert lerp_color((0, 0, 0), (255, 255, 255), 1.0) == (255, 255, 255)


def test_lerp_color_midpoint():
    # 254/2 = 127
    assert lerp_color((0, 0, 0), (254, 254, 254), 0.5) == (127, 127, 127)


def test_gradient_color_at_zero_returns_first_stop():
    assert gradient_color(0.0, ["#ff0000", "#0000ff"]) == (255, 0, 0)


def test_gradient_color_at_one_returns_last_stop():
    assert gradient_color(1.0, ["#ff0000", "#0000ff"]) == (0, 0, 255)


def test_gradient_color_midpoint_black_to_white():
    assert gradient_color(0.5, ["#000000", "#ffffff"]) == (127, 127, 127)


def test_gradient_color_clamps_below_zero():
    stops = ["#ff0000", "#0000ff"]
    assert gradient_color(-1.0, stops) == gradient_color(0.0, stops)


def test_gradient_color_clamps_above_one():
    stops = ["#ff0000", "#0000ff"]
    assert gradient_color(2.0, stops) == gradient_color(1.0, stops)


def test_gradient_color_three_stops_at_midpoint():
    # 3 stops: t=0.5 → seg=1.0, idx=min(1,1)=1, local_t=0.0 → exactly stop[1]
    stops = ["#000000", "#808080", "#ffffff"]
    assert gradient_color(0.5, stops) == parse_hex("#808080")


def test_resolve_stops_uses_named_palette():
    assert resolve_stops("neon", None) == PALETTES["neon"]


def test_resolve_stops_uses_gradient_list():
    assert resolve_stops(None, ["#ff0000", "#0000ff"]) == ["#ff0000", "#0000ff"]


def test_resolve_stops_defaults_to_neon_when_neither_given():
    assert resolve_stops(None, None) == PALETTES["neon"]


def test_resolve_stops_unknown_palette_raises():
    with pytest.raises(ValueError, match="unknown palette"):
        resolve_stops("notapalette", None)


def test_resolve_stops_gradient_single_stop_raises():
    with pytest.raises(ValueError, match="at least 2 color stops"):
        resolve_stops(None, ["#ff0000"])


def test_resolve_stops_gradient_invalid_hex_raises():
    with pytest.raises(ValueError, match="expected #RRGGBB"):
        resolve_stops(None, ["#ff0000", "bad"])
```

- [ ] **Step 2: Run tests to verify the new ones fail**

```bash
uv run pytest tests/test_color.py -v
```

Expected: the first 9 tests pass, the new gradient tests fail with `ImportError`.

- [ ] **Step 3: Add gradient functions to `src/color_banner/color.py`**

Append to the end of the existing `color.py` (after `parse_hex`):

```python
def lerp_color(
    c1: tuple[int, int, int],
    c2: tuple[int, int, int],
    t: float,
) -> tuple[int, int, int]:
    """Linearly interpolate between two RGB tuples at position t ∈ [0.0, 1.0]."""
    return (
        round(c1[0] + (c2[0] - c1[0]) * t),
        round(c1[1] + (c2[1] - c1[1]) * t),
        round(c1[2] + (c2[2] - c1[2]) * t),
    )


def gradient_color(t: float, stops: list[str]) -> tuple[int, int, int]:
    """Map t ∈ [0.0, 1.0] to an RGB tuple across a list of hex color stops.

    The stop list is divided into (len(stops) - 1) equal segments.
    t is clamped to [0.0, 1.0].
    """
    t = max(0.0, min(1.0, t))
    n = len(stops)
    if n == 1:
        return parse_hex(stops[0])
    seg = (n - 1) * t
    idx = min(int(seg), n - 2)
    local_t = seg - idx
    return lerp_color(parse_hex(stops[idx]), parse_hex(stops[idx + 1]), local_t)


def resolve_stops(palette: str | None, gradient: list[str] | None) -> list[str]:
    """Return the hex stop list from a palette name or raw gradient list.

    Falls back to the 'neon' palette if both are None.
    Raises ValueError for unknown palettes or invalid gradient specs.
    """
    if gradient is not None:
        if len(gradient) < 2:
            raise ValueError("--gradient requires at least 2 color stops")
        for stop in gradient:
            parse_hex(stop)  # validate up front; raises ValueError on bad input
        return gradient
    if palette is not None:
        if palette not in PALETTES:
            available = ", ".join(PALETTES.keys())
            raise ValueError(f"unknown palette '{palette}'. Available: {available}")
        return PALETTES[palette]
    return PALETTES["neon"]
```

- [ ] **Step 4: Run all color tests**

```bash
uv run pytest tests/test_color.py -v
```

Expected: `24 passed`.

- [ ] **Step 5: Commit**

```bash
git add src/color_banner/color.py tests/test_color.py
git commit -m "feat: add gradient math to color.py"
```

---

## Task 4: renderer.py

**Files:**
- Create: `src/color_banner/renderer.py`
- Create: `tests/test_renderer.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_renderer.py`:

```python
import pytest
from color_banner.renderer import list_fonts, render


def test_render_returns_list_of_strings():
    rows = render("Hi")
    assert isinstance(rows, list)
    assert all(isinstance(r, str) for r in rows)


def test_render_output_is_nonempty():
    rows = render("Hi")
    assert len(rows) > 0


def test_render_no_trailing_empty_rows():
    rows = render("Hi")
    assert rows[-1].strip() != ""


def test_render_custom_font():
    rows = render("Hi", font="ogre")
    assert len(rows) > 0


def test_render_unknown_font_raises():
    with pytest.raises(ValueError, match="unknown font"):
        render("Hi", font="this_font_does_not_exist_xyz")


def test_list_fonts_returns_sorted_list():
    fonts = list_fonts()
    assert isinstance(fonts, list)
    assert len(fonts) > 0
    assert fonts == sorted(fonts)


def test_list_fonts_includes_slant():
    assert "slant" in list_fonts()


def test_list_fonts_includes_ogre():
    assert "ogre" in list_fonts()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_renderer.py -v
```

Expected: `ImportError` — `color_banner.renderer` does not exist yet.

- [ ] **Step 3: Write `src/color_banner/renderer.py`**

```python
# SPDX-License-Identifier: GPL-3.0-or-later
# Based on Calligraphy by GeopJr <https://codeberg.org/GeopJr/Calligraphy>
# Originally by Gregor "gregorni" Niehl
from __future__ import annotations

import pyfiglet


def render(text: str, font: str = "slant") -> list[str]:
    """Render text as figlet ASCII art rows.

    Returns a list of strings (one per row) with trailing empty rows stripped.
    Raises ValueError for unknown font names.
    """
    try:
        raw = pyfiglet.figlet_format(text, font=font)
    except pyfiglet.FontNotFound:
        raise ValueError(
            f"unknown font '{font}'. Run --list-fonts to see available fonts"
        )
    rows = raw.split("\n")
    while rows and rows[-1].strip() == "":
        rows.pop()
    return rows


def list_fonts() -> list[str]:
    """Return all available pyfiglet font names, sorted alphabetically."""
    return sorted(pyfiglet.FigletFont.getFonts())
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_renderer.py -v
```

Expected: `8 passed`.

- [ ] **Step 5: Commit**

```bash
git add src/color_banner/renderer.py tests/test_renderer.py
git commit -m "feat: add renderer.py wrapping pyfiglet"
```

---

## Task 5: painter.py

**Files:**
- Create: `src/color_banner/painter.py`
- Create: `tests/test_painter.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_painter.py`:

```python
from color_banner.painter import paint

SIMPLE_ROWS = ["##", "##"]   # 2 rows × 2 cols, all non-space
SPACE_ROWS  = ["  ", "  "]   # all spaces


def test_no_color_returns_rows_unchanged():
    rows = ["hello", "world"]
    assert paint(rows, ["#ff0000", "#0000ff"], "lr", no_color=True) == rows


def test_spaces_produce_no_escape_codes():
    result = paint(SPACE_ROWS, ["#ff0000", "#0000ff"], "lr")
    for line in result:
        assert "\x1b[" not in line


def test_non_space_chars_contain_foreground_escape():
    result = paint(SIMPLE_ROWS, ["#ff0000", "#0000ff"], "lr")
    for line in result:
        assert "\x1b[38;2;" in line


def test_non_space_chars_contain_reset():
    result = paint(SIMPLE_ROWS, ["#ff0000", "#0000ff"], "lr")
    for line in result:
        assert "\x1b[0m" in line


def test_lr_single_column_uses_first_stop():
    # single-column → max_cols=1 → t=0 → first stop #ff0000 → rgb(255,0,0)
    result = paint(["X"], ["#ff0000", "#0000ff"], "lr")
    assert "\x1b[38;2;255;0;0mX\x1b[0m" in result[0]


def test_tb_first_row_uses_first_stop():
    # 3 rows, tb: row 0 → t=0 → first stop #ff0000
    result = paint(["X", "X", "X"], ["#ff0000", "#0000ff"], "tb")
    assert "\x1b[38;2;255;0;0m" in result[0]


def test_tb_last_row_uses_last_stop():
    # 3 rows, tb: row 2 → t=1 → last stop #0000ff
    result = paint(["X", "X", "X"], ["#ff0000", "#0000ff"], "tb")
    assert "\x1b[38;2;0;0;255m" in result[2]


def test_bt_is_reverse_of_tb():
    rows = ["X", "X", "X"]
    tb = paint(rows, ["#ff0000", "#0000ff"], "tb")
    bt = paint(rows, ["#ff0000", "#0000ff"], "bt")
    assert tb[0] == bt[2]
    assert tb[2] == bt[0]


def test_diag_produces_distinct_colors_across_rows():
    rows = ["XX", "XX"]
    result = paint(rows, ["#ff0000", "#0000ff"], "diag")
    # row 0 and row 1 have different t values so they should differ
    assert result[0] != result[1]


def test_returns_same_row_count():
    rows = ["abc", "def", "ghi"]
    assert len(paint(rows, ["#ff0000", "#0000ff"], "lr")) == 3
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_painter.py -v
```

Expected: `ImportError` — `color_banner.painter` does not exist yet.

- [ ] **Step 3: Write `src/color_banner/painter.py`**

```python
# SPDX-License-Identifier: GPL-3.0-or-later
# Based on Calligraphy by GeopJr <https://codeberg.org/GeopJr/Calligraphy>
# Originally by Gregor "gregorni" Niehl
from __future__ import annotations

from color_banner.color import gradient_color

DIRECTIONS = ("lr", "tb", "bt", "diag")


def paint(
    rows: list[str],
    stops: list[str],
    direction: str,
    no_color: bool = False,
) -> list[str]:
    """Apply a gradient to ASCII art rows and return ANSI-escaped lines.

    - Spaces are left uncolored (no escape codes emitted).
    - Each non-space character is wrapped in a 24-bit foreground escape:
      \\x1b[38;2;{r};{g};{b}m{char}\\x1b[0m
    - When no_color is True, rows are returned unchanged.

    direction values:
      lr   — gradient sweeps left to right across each row
      tb   — gradient sweeps top to bottom (same color per row)
      bt   — gradient sweeps bottom to top (same color per row)
      diag — gradient sweeps diagonally (t = (row + col) / (rows + cols - 2))
    """
    if no_color:
        return list(rows)

    num_rows = len(rows)
    max_cols = max((len(row) for row in rows), default=1)
    denom_tb   = max(num_rows - 1, 1)
    denom_lr   = max(max_cols - 1, 1)
    denom_diag = max(num_rows + max_cols - 2, 1)

    result: list[str] = []
    for row_idx, row in enumerate(rows):
        parts: list[str] = []
        for col_idx, ch in enumerate(row):
            if ch == " ":
                parts.append(ch)
                continue

            if direction == "lr":
                t = col_idx / denom_lr
            elif direction == "tb":
                t = row_idx / denom_tb
            elif direction == "bt":
                t = 1.0 - row_idx / denom_tb
            else:  # diag
                t = (row_idx + col_idx) / denom_diag

            r, g, b = gradient_color(t, stops)
            parts.append(f"\x1b[38;2;{r};{g};{b}m{ch}\x1b[0m")

        result.append("".join(parts))
    return result
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_painter.py -v
```

Expected: `10 passed`.

- [ ] **Step 5: Commit**

```bash
git add src/color_banner/painter.py tests/test_painter.py
git commit -m "feat: add painter.py — apply gradient colors to ASCII rows"
```

---

## Task 6: output.py

**Files:**
- Create: `src/color_banner/output.py`
- Create: `tests/test_output.py`

- [ ] **Step 1: Write failing tests**

Create `tests/test_output.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_output.py -v
```

Expected: `ImportError` — `color_banner.output` does not exist yet.

- [ ] **Step 3: Write `src/color_banner/output.py`**

```python
# SPDX-License-Identifier: GPL-3.0-or-later
# Based on Calligraphy by GeopJr <https://codeberg.org/GeopJr/Calligraphy>
# Originally by Gregor "gregorni" Niehl
from __future__ import annotations

import base64

_ATTRIBUTION = (
    "Based on Calligraphy by GeopJr <https://codeberg.org/GeopJr/Calligraphy>\n"
    '# Originally by Gregor "gregorni" Niehl — Licensed under GPL v3'
)


def write_stdout(lines: list[str]) -> None:
    """Print lines to stdout joined by newlines."""
    print("\n".join(lines))


def write_ansi_file(lines: list[str], path: str, version: str) -> None:
    """Write ANSI-escaped lines to a file with an attribution header.

    The resulting file can be replayed with: cat <path>
    Raises OSError on write failure.
    """
    header = (
        f"# Generated by color-banner {version}\n"
        f"# {_ATTRIBUTION}\n"
        f"# cat this file to display the banner\n"
    )
    content = header + "\n".join(lines) + "\n"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def write_shell_export(
    lines: list[str],
    path: str,
    version: str,
    function_name: str = "show_banner",
) -> None:
    """Write a self-contained bash function that replays the banner.

    The ANSI output is base64-encoded and embedded inline.
    Raises OSError on write failure.
    """
    ansi_bytes = ("\n".join(lines) + "\n").encode("utf-8")
    b64 = base64.b64encode(ansi_bytes).decode("ascii")
    script = (
        f"#!/usr/bin/env bash\n"
        f"# Generated by color-banner {version}\n"
        f"# {_ATTRIBUTION}\n"
        f"# Paste this function into your script or .bashrc\n"
        f"{function_name}() {{\n"
        f"  printf '%s' \"$(printf '%s' '{b64}' | base64 -d)\"\n"
        f"}}\n"
        f"{function_name}\n"
    )
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(script)
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
uv run pytest tests/test_output.py -v
```

Expected: `13 passed`.

- [ ] **Step 5: Commit**

```bash
git add src/color_banner/output.py tests/test_output.py
git commit -m "feat: add output.py — stdout, --save, --export"
```

---

## Task 7: cli.py and Integration Tests

**Files:**
- Create: `src/color_banner/cli.py`
- Create: `tests/test_cli.py`

- [ ] **Step 1: Write failing integration tests**

Create `tests/test_cli.py`:

```python
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
    assert result.returncode != 0
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
uv run pytest tests/test_cli.py -v
```

Expected: most tests fail with non-zero exit code because `color-banner` command doesn't exist.

- [ ] **Step 3: Write `src/color_banner/cli.py`**

```python
# SPDX-License-Identifier: GPL-3.0-or-later
# Based on Calligraphy by GeopJr <https://codeberg.org/GeopJr/Calligraphy>
# Originally by Gregor "gregorni" Niehl
from __future__ import annotations

import argparse
import sys

from color_banner import __version__
from color_banner.color import PALETTES, resolve_stops
from color_banner.output import write_ansi_file, write_shell_export, write_stdout
from color_banner.painter import paint
from color_banner.renderer import list_fonts, render


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="color-banner",
        description="Render text as a colorful figlet ASCII banner.",
    )
    parser.add_argument("text", nargs="?", metavar="TEXT", help="Text to render")

    font_group = parser.add_argument_group("font options")
    font_group.add_argument(
        "-f", "--font", default="slant", metavar="FONT",
        help="figlet font name (default: slant)",
    )
    font_group.add_argument(
        "--list-fonts", action="store_true",
        help="print all available font names and exit",
    )

    color_group = parser.add_argument_group("color options")
    mx = color_group.add_mutually_exclusive_group()
    mx.add_argument(
        "--palette", metavar="NAME",
        help="built-in palette name (neon, sunset, ocean, fire, ice, rainbow)",
    )
    mx.add_argument(
        "--gradient", nargs="+", metavar="HEX",
        help="2–8 hex color stops e.g. --gradient '#ff0080' '#00d4ff'",
    )
    color_group.add_argument(
        "--direction", default="lr", choices=["lr", "tb", "bt", "diag"],
        help="gradient direction: lr|tb|bt|diag (default: lr)",
    )

    out_group = parser.add_argument_group("output options")
    out_group.add_argument(
        "--save", metavar="FILE",
        help="write ANSI escape file (cat-able)",
    )
    out_group.add_argument(
        "--export", metavar="FILE",
        help="write self-contained shell function (.sh)",
    )
    out_group.add_argument(
        "--function-name", default="show_banner", metavar="NAME",
        help="function name for --export (default: show_banner)",
    )
    out_group.add_argument(
        "--no-color", action="store_true",
        help="plain text output, no ANSI codes",
    )

    parser.add_argument(
        "--list-palettes", action="store_true",
        help="print built-in palette names and their hex stops",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}",
    )

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.list_fonts:
        print("\n".join(list_fonts()))
        return

    if args.list_palettes:
        for name, stops in PALETTES.items():
            print(f"{name}: {' → '.join(stops)}")
        return

    if not args.text:
        parser.error("TEXT is required")

    # Resolve color stops — args.gradient is list[str] | None
    try:
        stops = resolve_stops(args.palette, args.gradient)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    # Render ASCII art
    try:
        rows = render(args.text, font=args.font)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    # File output always gets ANSI (unless --no-color); stdout respects TTY
    file_no_color = args.no_color
    lines_for_file = paint(rows, stops, args.direction, no_color=file_no_color)

    try:
        if args.save:
            write_ansi_file(lines_for_file, args.save, __version__)
        if args.export:
            write_shell_export(
                lines_for_file, args.export, __version__, args.function_name
            )
        if not args.save and not args.export:
            stdout_no_color = args.no_color or not sys.stdout.isatty()
            lines_for_stdout = paint(
                rows, stops, args.direction, no_color=stdout_no_color
            )
            write_stdout(lines_for_stdout)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
```

- [ ] **Step 4: Run the integration tests**

```bash
uv run pytest tests/test_cli.py -v
```

Expected: `17 passed`.

- [ ] **Step 5: Run the full test suite**

```bash
uv run pytest -v
```

Expected: all tests pass (color + renderer + painter + output + cli).

- [ ] **Step 6: Smoke test in the terminal**

```bash
uv run color-banner "Fox and Dog" --palette neon --direction tb
uv run color-banner "Hello" --gradient "#ff0080" "#7b2fff" "#00d4ff" --direction diag
uv run color-banner --list-palettes
```

Verify colored output renders correctly in your terminal.

- [ ] **Step 7: Commit**

```bash
git add src/color_banner/cli.py tests/test_cli.py
git commit -m "feat: add cli.py — wire all modules, complete color-banner command"
```

---

## Task 8: Final Polish

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Add `.gitignore`**

```bash
cat > .gitignore << 'EOF'
.venv/
__pycache__/
*.pyc
*.egg-info/
dist/
.superpowers/
EOF
git add .gitignore
```

- [ ] **Step 2: Replace `README.md` with the final version**

```markdown
# color-banner

> Inspired by [Calligraphy](https://codeberg.org/GeopJr/Calligraphy) by GeopJr
> and originally by Gregor "gregorni" Niehl. Licensed under GPL v3.

Render text as colorful 24-bit figlet ASCII banners in the terminal.
Designed for CICD pipelines, shell startup screens, and BBS-style splash screens.

## Install

```bash
uv tool install color-banner
```

## Usage

```
color-banner TEXT [options]

font options:
  -f, --font FONT         figlet font name (default: slant)
  --list-fonts            print all available font names and exit

color options (mutually exclusive):
  --palette NAME          built-in palette: neon sunset ocean fire ice rainbow
  --gradient HEX [HEX …]  2–8 hex color stops e.g. --gradient '#ff0080' '#00d4ff'
  --direction DIR         gradient direction: lr|tb|bt|diag (default: lr)

output options:
  --save FILE             write ANSI escape file (cat-able)
  --export FILE           write self-contained shell function (.sh)
  --function-name NAME    function name for --export (default: show_banner)
  --no-color              plain text, no ANSI codes

info:
  --list-palettes         print palette names and hex stops
  -v, --version           show version and exit
```

## Examples

```bash
# print to terminal
color-banner "Fox and Dog" --palette neon --direction tb

# save a cat-able ANSI file
color-banner "Deploy v2" --palette fire --direction diag --save splash.ans
cat splash.ans

# export a portable shell function for CI pipelines
color-banner "Deploy v2" --palette fire --export splash.sh
bash splash.sh

# custom hex gradient, diagonal sweep
color-banner "Hello" --gradient "#ff0080" "#7b2fff" "#00d4ff" --direction diag

# plain figlet text, no color (pipe-safe)
color-banner "Hello" --font ogre --no-color

# list all built-in palettes
color-banner --list-palettes

# list all figlet fonts
color-banner --list-fonts
```

## Embedding in a CI pipeline

Generate the splash once and commit the `.sh` file:

```bash
color-banner "🚀 Deploying" --palette sunset --export .ci/splash.sh
```

Then in your pipeline script:

```bash
source .ci/splash.sh
show_banner
```

## License

GPL v3 — see [LICENSE](LICENSE) and [CREDITS.md](CREDITS.md).
```

- [ ] **Step 3: Final test run**

```bash
uv run pytest -v
```

Expected: all tests pass.

- [ ] **Step 4: Final commit**

```bash
git add README.md .gitignore
git commit -m "docs: complete README and add .gitignore"
```
