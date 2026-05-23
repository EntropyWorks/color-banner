import pytest
from color_banner.renderer import (
    is_font_readable,
    list_fonts,
    numbered_fonts,
    readable_fonts,
    render,
    resolve_font_identifier,
)


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


# --- is_font_readable ---

def test_is_font_readable_slant():
    """slant is a clean, standard font — must be readable."""
    assert is_font_readable("slant") is True


def test_is_font_readable_doh():
    """doh renders 75 rows — must be unreadable (too tall)."""
    assert is_font_readable("doh") is False


def test_is_font_readable_term():
    """term passes text through as a single short line — must be unreadable."""
    assert is_font_readable("term") is False


def test_is_font_readable_morse():
    """morse outputs a single dot-dash line — must be unreadable."""
    assert is_font_readable("morse") is False


def test_is_font_readable_eftipiti():
    """eftipiti only has uppercase glyphs — must be readable (rescued by HELLO WORLD)."""
    assert is_font_readable("eftipiti") is True


def test_is_font_readable_all_three_phrases_checked():
    """A font unreadable with mixed but readable with upper is marked readable."""
    # eftipiti: 2 rows with 'Hello World', 3 rows with 'HELLO WORLD'
    from color_banner.renderer import render, _rows_pass_thresholds
    assert not _rows_pass_thresholds(render("Hello World", font="eftipiti"))
    assert _rows_pass_thresholds(render("HELLO WORLD", font="eftipiti"))


def test_is_font_readable_unknown_font():
    """Unknown font name returns False (not raises)."""
    assert is_font_readable("__not_a_real_font__") is False


# --- readable_fonts ---

def test_readable_fonts_is_subset_of_numbered():
    """readable_fonts() is a strict subset of numbered_fonts()."""
    all_nums = {n for n, _ in numbered_fonts()}
    readable_nums = {n for n, _ in readable_fonts()}
    assert readable_nums < all_nums


def test_readable_fonts_excludes_doh():
    """doh (too tall) must not appear in readable_fonts()."""
    names = {name for _, name in readable_fonts()}
    assert "doh" not in names


def test_readable_fonts_excludes_term():
    """term (plain passthrough) must not appear in readable_fonts()."""
    names = {name for _, name in readable_fonts()}
    assert "term" not in names


def test_readable_fonts_includes_slant():
    """slant must appear in readable_fonts()."""
    names = {name for _, name in readable_fonts()}
    assert "slant" in names


def test_readable_fonts_includes_ogre():
    """ogre must appear in readable_fonts()."""
    names = {name for _, name in readable_fonts()}
    assert "ogre" in names


def test_readable_fonts_preserves_original_numbering():
    """Numbers in readable_fonts() match the original 1-based positions from numbered_fonts()."""
    num_map = {name: n for n, name in numbered_fonts()}
    for n, name in readable_fonts():
        assert n == num_map[name]


# --- render() width parameter ---

def test_render_default_width_is_80():
    """render() at default width=80 wraps long text; width=200 keeps it on one pass."""
    # 'block' font renders 'Hello World' as ~90 chars wide — wraps at 80, fits at 200
    rows_80 = render("Hello World", font="block")
    rows_wide = render("Hello World", font="block", width=200)
    assert len(rows_80) > len(rows_wide)


def test_render_narrow_width_increases_row_count():
    """render() with a narrow width produces more rows than the default."""
    rows_default = render("Hello World", font="big")
    rows_narrow = render("Hello World", font="big", width=40)
    assert len(rows_narrow) > len(rows_default)


def test_render_width_zero_means_no_wrap():
    """render() with width=0 never wraps (same result as very large width)."""
    rows_nowrap = render("Hello World", font="big", width=0)
    rows_huge = render("Hello World", font="big", width=32767)
    assert rows_nowrap == rows_huge


def test_render_width_does_not_change_short_text():
    """Short text that fits in 80 cols is unaffected by wider width."""
    rows_default = render("Hi", font="slant")
    rows_wide = render("Hi", font="slant", width=200)
    assert rows_default == rows_wide
