import pytest
from color_banner.renderer import list_fonts, render


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
