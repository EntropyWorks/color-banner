# New Palettes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add 17 new named palettes (9 simple 4-stop editor themes + 8 complex 6–8 stop gradients) to color-banner.

**Architecture:** All palette data lives in the `PALETTES` dict in `src/color_banner/color.py`. Everything else — rendering, `--list-palettes`, validation error messages — already derives from that dict dynamically. Only two files need to change: `color.py` (add entries) and `cli.py` (update one help string).

**Tech Stack:** Python, uv (`uv run pytest` to run tests, `uv run color-banner` to run the CLI)

---

### Task 1: Add 17 new palettes to PALETTES and update help text

**Files:**
- Modify: `src/color_banner/color.py:4-11`
- Modify: `src/color_banner/cli.py:51`

- [ ] **Step 1: Write failing tests**

Add these tests to `tests/test_color.py`. The first checks every new palette is present in `PALETTES`; the second verifies that `--list-palettes` output includes all palette names dynamically (replacing the hardcoded check).

```python
# At the bottom of tests/test_color.py

NEW_PALETTE_NAMES = [
    "dracula", "nord", "monokai", "gruvbox", "catppuccin",
    "tokyo", "vaporwave", "aurora", "zebra",
    "synthwave", "inferno", "plasma", "galaxy",
    "tropical", "pride", "deepsea", "lava",
]

@pytest.mark.parametrize("name", NEW_PALETTE_NAMES)
def test_new_palette_exists(name):
    assert name in PALETTES, f"palette '{name}' missing from PALETTES"

@pytest.mark.parametrize("name", NEW_PALETTE_NAMES)
def test_new_palette_has_valid_hex_stops(name):
    stops = PALETTES[name]
    assert len(stops) >= 2
    for stop in stops:
        parse_hex(stop)  # raises ValueError on bad input
```

Also add this to `tests/test_cli.py` to replace the brittle hardcoded list check (keep the old `test_list_palettes` in place — it still passes):

```python
def test_list_palettes_includes_all_palette_names():
    from color_banner.color import PALETTES
    result = run(["--list-palettes"])
    assert result.returncode == 0
    for name in PALETTES:
        assert name in result.stdout, f"palette '{name}' missing from --list-palettes output"
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
uv run pytest tests/test_color.py::test_new_palette_exists tests/test_color.py::test_new_palette_has_valid_hex_stops tests/test_cli.py::test_list_palettes_includes_all_palette_names -v
```

Expected: all 35 new tests FAIL with `KeyError` or `AssertionError`.

- [ ] **Step 3: Add the 17 palettes to color.py**

Replace the `PALETTES` dict in `src/color_banner/color.py` with:

```python
PALETTES: dict[str, list[str]] = {
    # --- originals ---
    "neon":       ["#ff00ff", "#7700ff", "#00bbff", "#00ffdd"],
    "sunset":     ["#ff6b35", "#f7931e", "#ffd700", "#ff4e50"],
    "ocean":      ["#006994", "#0099cc", "#00d4aa", "#00ff88"],
    "fire":       ["#ff0000", "#ff8800", "#ffcc00", "#ffff00"],
    "ice":        ["#88d8ff", "#44aaff", "#0066ff", "#0033cc"],
    "rainbow":    ["#ff0000", "#ff8800", "#ffff00", "#00cc00", "#0044ff", "#8800ff"],
    # --- editor / terminal themes (4 stops) ---
    "dracula":    ["#bd93f9", "#ff79c6", "#8be9fd", "#50fa7b"],
    "nord":       ["#5e81ac", "#81a1c1", "#88c0d0", "#8fbcbb"],
    "monokai":    ["#f92672", "#fd971f", "#e6db74", "#a6e22e"],
    "gruvbox":    ["#cc241d", "#d65d0e", "#d79921", "#98971a"],
    "catppuccin": ["#cba6f7", "#f38ba8", "#fab387", "#a6e3a1"],
    "tokyo":      ["#7aa2f7", "#bb9af7", "#9ece6a", "#73daca"],
    "vaporwave":  ["#ff71ce", "#b967ff", "#01cdfe", "#05ffa1"],
    "aurora":     ["#a3be8c", "#88c0d0", "#b48ead", "#ebcb8b"],
    "zebra":      ["#111111", "#e0e0e0", "#ffffff", "#e0e0e0"],
    # --- rich multi-stop gradients (6–8 stops) ---
    "synthwave":  ["#f72585", "#b5179e", "#7209b7", "#3a0ca3", "#4361ee", "#4cc9f0"],
    "inferno":    ["#000004", "#420a68", "#932667", "#dd513a", "#fca50a", "#f8df25", "#fcffa4"],
    "plasma":     ["#0d0887", "#6a00a8", "#b12a90", "#e16462", "#fca636", "#f0f921"],
    "galaxy":     ["#0b0c2a", "#1b1464", "#6a0dad", "#c71585", "#ff69b4", "#ffd700", "#fff8e7"],
    "tropical":   ["#ff6b6b", "#ff8e53", "#ffd700", "#56ab2f", "#00c9ff", "#4776e6"],
    "pride":      ["#ff0000", "#ff8c00", "#ffff00", "#00aa00", "#0000ff", "#8b00ff"],
    "deepsea":    ["#000033", "#000066", "#003399", "#0066cc", "#0099cc", "#33cccc", "#66ffcc", "#ccffff"],
    "lava":       ["#1a0000", "#5c0000", "#cc0000", "#ff4500", "#ff8c00", "#ffd700"],
}
```

- [ ] **Step 4: Update --palette help text in cli.py**

In `src/color_banner/cli.py`, find the `--palette` argument (around line 51) and change:

```python
        help="built-in palette name (neon, sunset, ocean, fire, ice, rainbow)",
```

to:

```python
        help="built-in palette name (see --list-palettes for all options)",
```

- [ ] **Step 5: Run all new tests**

```bash
uv run pytest tests/test_color.py::test_new_palette_exists tests/test_color.py::test_new_palette_has_valid_hex_stops tests/test_cli.py::test_list_palettes_includes_all_palette_names -v
```

Expected: all 35 tests PASS.

- [ ] **Step 6: Run the full test suite**

```bash
uv run pytest -v
```

Expected: all tests PASS. No regressions.

- [ ] **Step 7: Smoke-test a few new palettes manually**

```bash
uv run color-banner "Hello" --palette dracula --no-color
uv run color-banner "Hello" --palette inferno --no-color
uv run color-banner "Hello" --palette deepsea --no-color
uv run color-banner --list-palettes
```

Expected: banners render without error; `--list-palettes` shows all 23 palettes.

- [ ] **Step 8: Commit**

```bash
git add src/color_banner/color.py src/color_banner/cli.py tests/test_color.py tests/test_cli.py
git commit -m "feat: add 17 new palettes (editor themes + rich multi-stop gradients)"
```
