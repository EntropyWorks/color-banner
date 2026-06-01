from color_banner.painter import paint

SIMPLE_ROWS = ["##", "##"]   # 2 rows × 2 cols, all non-space
SPACE_ROWS  = ["  ", "  "]   # all spaces


def test_no_color_returns_rows_unchanged():
    rows = ["hello", "world"]
    assert paint(rows, ["#ff0000", "#0000ff"], "lr", no_color=True) == rows


def test_spaces_produce_no_escape_codes():
    result = paint(SPACE_ROWS, ["#ff0000", "#0000ff"], "lr")
    for line in result:
        assert "\x1b[" not in line


def test_non_space_chars_contain_foreground_escape():
    result = paint(SIMPLE_ROWS, ["#ff0000", "#0000ff"], "lr")
    for line in result:
        assert "\x1b[38;2;" in line


def test_non_space_chars_contain_reset():
    result = paint(SIMPLE_ROWS, ["#ff0000", "#0000ff"], "lr")
    for line in result:
        assert "\x1b[0m" in line


def test_lr_single_column_uses_first_stop():
    # single-column → max_cols=1 → t=0 → first stop #ff0000 → rgb(255,0,0)
    result = paint(["X"], ["#ff0000", "#0000ff"], "lr")
    assert "\x1b[38;2;255;0;0mX\x1b[0m" in result[0]


def test_tb_first_row_uses_first_stop():
    # 3 rows, tb: row 0 → t=0 → first stop #ff0000
    result = paint(["X", "X", "X"], ["#ff0000", "#0000ff"], "tb")
    assert "\x1b[38;2;255;0;0m" in result[0]


def test_tb_last_row_uses_last_stop():
    # 3 rows, tb: row 2 → t=1 → last stop #0000ff
    result = paint(["X", "X", "X"], ["#ff0000", "#0000ff"], "tb")
    assert "\x1b[38;2;0;0;255m" in result[2]


def test_bt_is_reverse_of_tb():
    rows = ["X", "X", "X"]
    tb = paint(rows, ["#ff0000", "#0000ff"], "tb")
    bt = paint(rows, ["#ff0000", "#0000ff"], "bt")
    assert tb[0] == bt[2]
    assert tb[2] == bt[0]


def test_diag_produces_distinct_colors_across_rows():
    rows = ["XX", "XX"]
    result = paint(rows, ["#ff0000", "#0000ff"], "diag")
    # row 0 and row 1 have different t values so they should differ
    assert result[0] != result[1]


def test_returns_same_row_count():
    rows = ["abc", "def", "ghi"]
    assert len(paint(rows, ["#ff0000", "#0000ff"], "lr")) == 3


# --- Feature 2: --bg-color ---

def test_paint_bg_color_applied_to_chars():
    rows = ["H"]
    stops = ["#ff0000", "#0000ff"]
    lines = paint(rows, stops, "lr", bg_color="#1a1a1a")
    assert "\x1b[48;2;26;26;26m" in lines[0]


def test_paint_bg_color_applied_to_spaces():
    rows = [" "]
    stops = ["#ff0000", "#0000ff"]
    lines = paint(rows, stops, "lr", bg_color="#ffffff")
    assert "\x1b[48;2;255;255;255m" in lines[0]
    assert " " in lines[0]


def test_paint_no_color_ignores_bg_color():
    rows = ["Hi"]
    stops = ["#ff0000", "#0000ff"]
    lines = paint(rows, stops, "lr", no_color=True, bg_color="#ff0000")
    assert "\x1b[" not in lines[0]


def test_paint_bg_color_none_unchanged():
    rows = ["H"]
    stops = ["#ff0000", "#0000ff"]
    without_bg = paint(rows, stops, "lr", bg_color=None)
    assert "\x1b[48;2;" not in without_bg[0]
