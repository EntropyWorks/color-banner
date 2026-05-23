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


def numbered_fonts() -> list[tuple[int, str]]:
    """Return (number, font_name) pairs, 1-based, sorted alphabetically."""
    return [(i + 1, name) for i, name in enumerate(list_fonts())]


def resolve_font_identifier(identifier: str) -> str:
    """Resolve a font name or numeric string to a font name.

    If identifier is all digits, treat as 1-based index into sorted font list.
    Otherwise return unchanged (font name validation happens in render()).
    Raises ValueError if number is out of range.
    """
    if identifier.isdigit():
        n = int(identifier)
        fonts = list_fonts()
        if not 1 <= n <= len(fonts):
            raise ValueError(
                f"font number {n} out of range (1-{len(fonts)}). "
                "Run --list-fonts to see available fonts"
            )
        return fonts[n - 1]
    return identifier
