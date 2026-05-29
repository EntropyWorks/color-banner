# Design: Add 17 New Color Palettes

**Date:** 2026-05-29  
**Status:** Approved

## Summary

Add 17 new named palettes to `color.py` and update the `--palette` help text in `cli.py`. No other changes required — all existing infrastructure (rendering, `--list-palettes`, validation error messages) already derives from the `PALETTES` dict dynamically.

## New Palettes

### Simple (4 stops) — editor/terminal themes

| Name | Stops |
|------|-------|
| `dracula` | `#bd93f9 → #ff79c6 → #8be9fd → #50fa7b` |
| `nord` | `#5e81ac → #81a1c1 → #88c0d0 → #8fbcbb` |
| `monokai` | `#f92672 → #fd971f → #e6db74 → #a6e22e` |
| `gruvbox` | `#cc241d → #d65d0e → #d79921 → #98971a` |
| `catppuccin` | `#cba6f7 → #f38ba8 → #fab387 → #a6e3a1` |
| `tokyo` | `#7aa2f7 → #bb9af7 → #9ece6a → #73daca` |
| `vaporwave` | `#ff71ce → #b967ff → #01cdfe → #05ffa1` |
| `aurora` | `#a3be8c → #88c0d0 → #b48ead → #ebcb8b` |
| `zebra` | `#111111 → #e0e0e0 → #ffffff → #e0e0e0` |

### Complex (6–8 stops) — rich gradients

| Name | Stops |
|------|-------|
| `synthwave` | `#f72585 → #b5179e → #7209b7 → #3a0ca3 → #4361ee → #4cc9f0` |
| `inferno` | `#000004 → #420a68 → #932667 → #dd513a → #fca50a → #f8df25 → #fcffa4` |
| `plasma` | `#0d0887 → #6a00a8 → #b12a90 → #e16462 → #fca636 → #f0f921` |
| `galaxy` | `#0b0c2a → #1b1464 → #6a0dad → #c71585 → #ff69b4 → #ffd700 → #fff8e7` |
| `tropical` | `#ff6b6b → #ff8e53 → #ffd700 → #56ab2f → #00c9ff → #4776e6` |
| `pride` | `#ff0000 → #ff8c00 → #ffff00 → #00aa00 → #0000ff → #8b00ff` |
| `deepsea` | `#000033 → #000066 → #003399 → #0066cc → #0099cc → #33cccc → #66ffcc → #ccffff` |
| `lava` | `#1a0000 → #5c0000 → #cc0000 → #ff4500 → #ff8c00 → #ffd700` |

## Changes

### `src/color_banner/color.py`

Append 17 entries to the `PALETTES` dict. No other changes to this file.

### `src/color_banner/cli.py`

Update the `--palette` argument help string from the hardcoded list of 6 names to:

```
"built-in palette name (see --list-palettes for all options)"
```

One line change.

## Out of Scope

- No changes to rendering logic, gradient engine, output formats, or test infrastructure beyond adding palette coverage.
- The `--list-palettes` command, error messages for unknown palettes, and all other palette-adjacent code require no changes.
