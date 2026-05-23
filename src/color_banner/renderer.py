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
