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


# Thresholds used by is_font_readable().  Tuned against pyfiglet's full font
# catalogue using "Hello World" as the test phrase.
_READABILITY_TEST_TEXT = "Hello World"
_READABLE_MIN_ROWS = 3    # single/two-liners are encoding fonts (morse, binary…)
_READABLE_MAX_ROWS = 25   # anything taller scrolls off a standard terminal
_READABLE_MAX_WIDTH = 200  # wider than this wraps on most terminals
_READABLE_MIN_DENSITY = 0.05  # ratio of non-space chars; below this is near-empty


def is_font_readable(font_name: str) -> bool:
    """Return True if *font_name* produces a clean, terminal-friendly banner.

    Renders :data:`_READABILITY_TEST_TEXT` and checks:

    * **Row count** — between :data:`_READABLE_MIN_ROWS` and
      :data:`_READABLE_MAX_ROWS` (inclusive).  Fonts below the minimum are
      typically encoding pass-throughs (morse, binary, hex); fonts above the
      maximum scroll off any standard terminal before finishing.
    * **Width** — at most :data:`_READABLE_MAX_WIDTH` characters.  Wider
      output wraps on standard 80- or 120-column terminals.
    * **Density** — at least :data:`_READABLE_MIN_DENSITY` of the total
      character cells are non-space.  Near-empty output means the font
      doesn't support the test characters.

    Returns ``False`` for unknown font names instead of raising.
    """
    try:
        rows = render(_READABILITY_TEST_TEXT, font=font_name)
    except ValueError:
        return False
    if not rows:
        return False
    widths = [len(r) for r in rows]
    max_w = max(widths)
    num_rows = len(rows)
    total_chars = sum(widths)
    printable = sum(1 for r in rows for c in r if c not in " \t")
    density = printable / total_chars if total_chars else 0
    return (
        _READABLE_MIN_ROWS <= num_rows <= _READABLE_MAX_ROWS
        and max_w <= _READABLE_MAX_WIDTH
        and density >= _READABLE_MIN_DENSITY
    )


def readable_fonts() -> list[tuple[int, str]]:
    """Return (number, font_name) pairs for fonts that pass readability checks.

    Numbers are the original 1-based positions from :func:`numbered_fonts` —
    ``--font 042`` still refers to the same font whether or not that font
    appears in the readable subset.
    """
    return [(n, name) for n, name in numbered_fonts() if is_font_readable(name)]


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
