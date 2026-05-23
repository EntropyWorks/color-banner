import pytest
from color_banner.color import PALETTES, parse_hex


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
            parse_hex(stop)  # raises ValueError if invalid
