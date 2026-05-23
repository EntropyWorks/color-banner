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
