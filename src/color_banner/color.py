# SPDX-License-Identifier: Apache-2.0
# Inspired by Calligraphy by GeopJr <https://codeberg.org/GeopJr/Calligraphy>
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


def lerp_color(
    c1: tuple[int, int, int],
    c2: tuple[int, int, int],
    t: float,
) -> tuple[int, int, int]:
    """Linearly interpolate between two RGB tuples at position t ∈ [0.0, 1.0]."""
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
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
        if len(gradient) > 8:
            raise ValueError("--gradient accepts at most 8 color stops")
        for stop in gradient:
            parse_hex(stop)  # validate up front; raises ValueError on bad input
        return gradient
    if palette is not None:
        if palette not in PALETTES:
            available = ", ".join(PALETTES.keys())
            raise ValueError(f"unknown palette '{palette}'. Available: {available}")
        return PALETTES[palette]
    return PALETTES["neon"]
