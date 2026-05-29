# Design: Add 9 New Color Palettes

**Date:** 2026-05-29  
**Status:** Approved

## Summary

Add 9 new named palettes to `color.py` and update the `--palette` help text in `cli.py`. No other changes required — all existing infrastructure (rendering, `--list-palettes`, validation error messages) already derives from the `PALETTES` dict dynamically.

## New Palettes

| Name | Stops | Inspiration |
|------|-------|-------------|
| `dracula` | `#bd93f9 → #ff79c6 → #8be9fd → #50fa7b` | Dracula IDE theme |
| `nord` | `#5e81ac → #81a1c1 → #88c0d0 → #8fbcbb` | Nord terminal theme |
| `monokai` | `#f92672 → #fd971f → #e6db74 → #a6e22e` | Monokai (Sublime Text) |
| `gruvbox` | `#cc241d → #d65d0e → #d79921 → #98971a` | Gruvbox Vim theme |
| `catppuccin` | `#cba6f7 → #f38ba8 → #fab387 → #a6e3a1` | Catppuccin Mocha |
| `tokyo` | `#7aa2f7 → #bb9af7 → #9ece6a → #73daca` | Tokyo Night |
| `vaporwave` | `#ff71ce → #b967ff → #01cdfe → #05ffa1` | Vaporwave aesthetic |
| `aurora` | `#a3be8c → #88c0d0 → #b48ead → #ebcb8b` | Northern lights |
| `zebra` | `#111111 → #e0e0e0 → #ffffff → #e0e0e0` | Black/silver/white |

## Changes

### `src/color_banner/color.py`

Append 9 entries to the `PALETTES` dict. No other changes to this file.

### `src/color_banner/cli.py`

Update the `--palette` argument help string from the hardcoded list of 6 names to:

```
"built-in palette name (see --list-palettes for all options)"
```

One line change.

## Out of Scope

- No changes to rendering logic, gradient engine, output formats, or test infrastructure beyond adding palette coverage.
- The `--list-palettes` command, error messages for unknown palettes, and all other palette-adjacent code require no changes.
