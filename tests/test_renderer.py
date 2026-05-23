import pytest
from color_banner.renderer import list_fonts, numbered_fonts, render, resolve_font_identifier


def test_render_returns_list_of_strings():
    rows = render("Hi")
    assert isinstance(rows, list)
    assert all(isinstance(r, str) for r in rows)


def test_render_output_is_nonempty():
    rows = render("Hi")
    assert len(rows) > 0


def test_render_no_trailing_empty_rows():
    rows = render("Hi")
    assert rows[-1].strip() != ""


def test_render_custom_font():
    rows = render("Hi", font="ogre")
    assert len(rows) > 0


def test_render_unknown_font_raises():
    with pytest.raises(ValueError, match="unknown font"):
        render("Hi", font="this_font_does_not_exist_xyz")


def test_list_fonts_returns_sorted_list():
    fonts = list_fonts()
    assert isinstance(fonts, list)
    assert len(fonts) > 0
    assert fonts == sorted(fonts)


def test_list_fonts_includes_slant():
    assert "slant" in list_fonts()


def test_list_fonts_includes_ogre():
    assert "ogre" in list_fonts()


def test_numbered_fonts_count():
    assert len(numbered_fonts()) == len(list_fonts())

def test_numbered_fonts_are_1_based():
    first_num, first_name = numbered_fonts()[0]
    assert first_num == 1
    assert first_name == list_fonts()[0]

def test_numbered_fonts_last_entry():
    fonts = numbered_fonts()
    last_num, last_name = fonts[-1]
    assert last_num == len(fonts)
    assert last_name == list_fonts()[-1]

def test_resolve_font_identifier_by_name():
    assert resolve_font_identifier("slant") == "slant"

def test_resolve_font_identifier_by_number_first():
    expected = list_fonts()[0]
    assert resolve_font_identifier("1") == expected

def test_resolve_font_identifier_by_number_padded():
    expected = list_fonts()[0]
    assert resolve_font_identifier("001") == expected

def test_resolve_font_identifier_by_number_last():
    fonts = list_fonts()
    assert resolve_font_identifier(str(len(fonts))) == fonts[-1]

def test_resolve_font_identifier_out_of_range():
    total = len(list_fonts())
    with pytest.raises(ValueError, match="out of range"):
        resolve_font_identifier(str(total + 1))

def test_resolve_font_identifier_zero_raises():
    with pytest.raises(ValueError, match="out of range"):
        resolve_font_identifier("0")
