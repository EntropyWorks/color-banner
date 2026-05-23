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
