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
