# HTML Export Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add `--save-html FILE` (full standalone HTML page) and `--html-snippet` (print `<pre>` snippet to stdout) output modes to color-banner.

**Architecture:** A private `_ansi_to_html_spans()` helper in `output.py` converts the existing ANSI-escaped lines from `painter.paint()` into inline-styled HTML spans. Two new public functions (`write_html_file`, `write_html_snippet`) wrap that helper. The CLI wires up two new flags and paints HTML lines separately to ensure color is always present regardless of `--no-color`.

**Tech Stack:** Python stdlib only (`re`, `html.escape`). Run tests with `uv run pytest`. Run CLI with `uv run color-banner`.

---

### Task 1: HTML conversion functions in output.py

**Files:**
- Modify: `src/color_banner/output.py`
- Modify: `tests/test_output.py`

- [ ] **Step 1: Write failing tests**

Add to the bottom of `tests/test_output.py`. The existing import line at the top reads:
`from color_banner.output import write_ansi_file, write_ansi_files_all, write_shell_export, write_stdout`
— leave it unchanged; the new tests import the new symbols directly.

```python
from color_banner.output import _ansi_to_html_spans, write_html_file, write_html_snippet

COLORED_LINE = "\x1b[38;2;255;0;128mH\x1b[0m \x1b[38;2;0;128;255mi\x1b[0m"


def test_ansi_to_html_spans_wraps_in_pre():
    result = _ansi_to_html_spans([""])
    assert result.startswith("<pre>")
    assert result.endswith("</pre>")


def test_ansi_to_html_spans_colored_char():
    result = _ansi_to_html_spans(["\x1b[38;2;255;0;128mH\x1b[0m"])
    assert '<span style="color:rgb(255,0,128)">H</span>' in result


def test_ansi_to_html_spans_space_passthrough():
    result = _ansi_to_html_spans([" "])
    assert "<span" not in result
    assert " " in result


def test_ansi_to_html_spans_escapes_lt_gt_amp():
    result = _ansi_to_html_spans(["<>&"])
    assert "&lt;" in result
    assert "&gt;" in result
    assert "&amp;" in result


def test_write_html_file_creates_file(tmp_path):
    out = tmp_path / "banner.html"
    write_html_file([COLORED_LINE], str(out), VERSION)
    assert out.exists()


def test_write_html_file_has_doctype(tmp_path):
    out = tmp_path / "banner.html"
    write_html_file([COLORED_LINE], str(out), VERSION)
    assert "<!DOCTYPE html>" in out.read_text(encoding="utf-8")


def test_write_html_file_contains_colored_span(tmp_path):
    out = tmp_path / "banner.html"
    write_html_file(["\x1b[38;2;255;0;128mH\x1b[0m"], str(out), VERSION)
    assert '<span style="color:rgb(255,0,128)">H</span>' in out.read_text(encoding="utf-8")


def test_write_html_file_has_dark_background(tmp_path):
    out = tmp_path / "banner.html"
    write_html_file([COLORED_LINE], str(out), VERSION)
    assert "#1a1a1a" in out.read_text(encoding="utf-8")


def test_write_html_file_creates_parent_dirs(tmp_path):
    deep = tmp_path / "a" / "b" / "banner.html"
    write_html_file([COLORED_LINE], str(deep), VERSION)
    assert deep.exists()


def test_write_html_file_contains_attribution(tmp_path):
    out = tmp_path / "banner.html"
    write_html_file([COLORED_LINE], str(out), VERSION)
    content = out.read_text(encoding="utf-8")
    assert "Calligraphy" in content
    assert "GeopJr" in content


def test_write_html_snippet_prints_pre(capsys):
    write_html_snippet([COLORED_LINE])
    out = capsys.readouterr().out
    assert "<pre>" in out
    assert "</pre>" in out


def test_write_html_snippet_contains_span(capsys):
    write_html_snippet(["\x1b[38;2;255;0;128mH\x1b[0m"])
    out = capsys.readouterr().out
    assert '<span style="color:rgb(255,0,128)">H</span>' in out
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
uv run pytest tests/test_output.py::test_ansi_to_html_spans_wraps_in_pre tests/test_output.py::test_write_html_file_creates_file tests/test_output.py::test_write_html_snippet_prints_pre -v
```

Expected: FAIL with `ImportError: cannot import name '_ansi_to_html_spans'`

- [ ] **Step 3: Add the three new functions to output.py**

Add `from html import escape as _html_escape` to the imports at the top of `src/color_banner/output.py` (after the existing `import re` line).

Then add a new compiled regex and three functions at the end of the file:

```python
_ANSI_SPAN_RE = re.compile(r"\x1b\[38;2;(\d+);(\d+);(\d+)m([^\x1b]*)\x1b\[0m")


def _ansi_to_html_spans(lines: list[str]) -> str:
    """Convert ANSI-colored lines to an HTML <pre> block with inline-styled spans."""
    html_lines = []
    for line in lines:
        out = ""
        pos = 0
        for m in _ANSI_SPAN_RE.finditer(line):
            if m.start() > pos:
                out += _html_escape(line[pos:m.start()])
            r, g, b, ch = m.group(1), m.group(2), m.group(3), m.group(4)
            out += f'<span style="color:rgb({r},{g},{b})">{_html_escape(ch)}</span>'
            pos = m.end()
        if pos < len(line):
            out += _html_escape(line[pos:])
        html_lines.append(out)
    return "<pre>" + "\n".join(html_lines) + "</pre>"


def write_html_file(lines: list[str], path: str, version: str) -> None:
    """Write a self-contained HTML page with the colored banner to path.

    Parent directories are created automatically.
    Raises OSError on write failure.
    """
    pre = _ansi_to_html_spans(lines)
    page = (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        f"<!-- Generated by color-banner {version} -->\n"
        f"<!-- {_ATTRIBUTION_LINE1} -->\n"
        f"<!-- {_ATTRIBUTION_LINE2} -->\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<style>\n"
        "  body { background: #1a1a1a; margin: 2rem; }\n"
        "  pre { font-family: monospace; font-size: 1rem; line-height: 1.3; }\n"
        "</style>\n"
        "</head>\n"
        "<body>\n"
        f"{pre}\n"
        "</body>\n"
        "</html>\n"
    )
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(page)


def write_html_snippet(lines: list[str]) -> None:
    """Print an HTML <pre> snippet of the colored banner to stdout."""
    print(_ansi_to_html_spans(lines))
```

- [ ] **Step 4: Run output tests**

```bash
uv run pytest tests/test_output.py -v
```

Expected: all tests PASS (no regressions, all new tests green).

- [ ] **Step 5: Commit**

```bash
git add src/color_banner/output.py tests/test_output.py
git commit -m "feat: add HTML conversion functions to output.py"
```

---

### Task 2: Wire up --save-html and --html-snippet in the CLI

**Files:**
- Modify: `src/color_banner/cli.py`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write failing CLI tests**

Add to the bottom of `tests/test_cli.py`:

```python
def test_save_html_creates_file(tmp_path):
    out = tmp_path / "banner.html"
    result = run(["Hello", "--palette", "neon", "--save-html", str(out)])
    assert result.returncode == 0
    assert out.exists()
    assert '<span style="color:rgb(' in out.read_text(encoding="utf-8")


def test_save_html_is_valid_html(tmp_path):
    out = tmp_path / "banner.html"
    run(["Hello", "--palette", "neon", "--save-html", str(out)])
    content = out.read_text(encoding="utf-8")
    assert "<!DOCTYPE html>" in content
    assert "<pre>" in content


def test_save_html_suppresses_stdout(tmp_path):
    out = tmp_path / "banner.html"
    result = run(["Hello", "--palette", "neon", "--save-html", str(out)])
    assert result.returncode == 0
    assert result.stdout == ""


def test_html_snippet_prints_to_stdout():
    result = run(["Hello", "--palette", "neon", "--html-snippet"])
    assert result.returncode == 0
    assert "<pre>" in result.stdout
    assert '<span style="color:rgb(' in result.stdout


def test_html_snippet_suppresses_ansi_stdout():
    result = run(["Hello", "--palette", "neon", "--html-snippet"])
    assert "\x1b[" not in result.stdout


def test_save_html_and_save_together(tmp_path):
    html_out = tmp_path / "banner.html"
    ans_out = tmp_path / "banner.ans"
    result = run([
        "Hi", "--palette", "neon",
        "--save-html", str(html_out),
        "--save", str(ans_out),
    ])
    assert result.returncode == 0
    assert html_out.exists()
    assert ans_out.exists()


def test_html_snippet_always_has_color():
    """--no-color must not strip color from --html-snippet output."""
    result = run(["Hello", "--palette", "neon", "--html-snippet", "--no-color"])
    assert result.returncode == 0
    assert '<span style="color:rgb(' in result.stdout


def test_save_html_always_has_color(tmp_path):
    """--no-color must not strip color from --save-html output."""
    out = tmp_path / "banner.html"
    run(["Hello", "--palette", "neon", "--save-html", str(out), "--no-color"])
    assert '<span style="color:rgb(' in out.read_text(encoding="utf-8")
```

- [ ] **Step 2: Run tests to confirm they fail**

```bash
uv run pytest tests/test_cli.py::test_save_html_creates_file tests/test_cli.py::test_html_snippet_prints_to_stdout -v
```

Expected: FAIL with `error: unrecognized arguments: --save-html` (exit code 2).

- [ ] **Step 3: Add --save-html and --html-snippet arguments to cli.py**

In `src/color_banner/cli.py`, update the output options group. Find the block that adds `--no-color` (around line 58) and add the two new flags after `--export` and before `--no-color`:

```python
    out_group.add_argument(
        "--save-html", metavar="FILE",
        help="write self-contained HTML page (open in browser)",
    )
    out_group.add_argument(
        "--html-snippet", action="store_true",
        help="print <pre> HTML snippet to stdout",
    )
```

- [ ] **Step 4: Update the output import in cli.py**

Find the import line near the top of `src/color_banner/cli.py`:

```python
from color_banner.output import write_ansi_file, write_ansi_files_all, write_shell_export, write_stdout
```

Replace it with:

```python
from color_banner.output import write_ansi_file, write_ansi_files_all, write_html_file, write_html_snippet, write_shell_export, write_stdout
```

- [ ] **Step 5: Add HTML output handling to the main() output block**

Find the output block at the bottom of `main()` in `src/color_banner/cli.py`. It currently reads:

```python
    file_no_color = args.no_color
    lines_for_file = paint(rows, stops, args.direction, no_color=file_no_color)

    try:
        if args.save:
            write_ansi_file(lines_for_file, args.save, __version__)
        if args.export:
            write_shell_export(
                lines_for_file, args.export, __version__, args.function_name
            )
        if not args.save and not args.export:
            stdout_no_color = args.no_color or not sys.stdout.isatty()
            lines_for_stdout = paint(
                rows, stops, args.direction, no_color=stdout_no_color
            )
            write_stdout(lines_for_stdout)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
```

Replace it with:

```python
    file_no_color = args.no_color
    lines_for_file = paint(rows, stops, args.direction, no_color=file_no_color)
    # HTML outputs always include color regardless of --no-color
    lines_for_html = paint(rows, stops, args.direction, no_color=False)

    try:
        if args.save:
            write_ansi_file(lines_for_file, args.save, __version__)
        if args.export:
            write_shell_export(
                lines_for_file, args.export, __version__, args.function_name
            )
        if args.save_html:
            write_html_file(lines_for_html, args.save_html, __version__)
        if args.html_snippet:
            write_html_snippet(lines_for_html)
        if not args.save and not args.export and not args.save_html and not args.html_snippet:
            stdout_no_color = args.no_color or not sys.stdout.isatty()
            lines_for_stdout = paint(
                rows, stops, args.direction, no_color=stdout_no_color
            )
            write_stdout(lines_for_stdout)
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
```

- [ ] **Step 6: Run the new CLI tests**

```bash
uv run pytest tests/test_cli.py::test_save_html_creates_file tests/test_cli.py::test_save_html_is_valid_html tests/test_cli.py::test_save_html_suppresses_stdout tests/test_cli.py::test_html_snippet_prints_to_stdout tests/test_cli.py::test_html_snippet_suppresses_ansi_stdout tests/test_cli.py::test_save_html_and_save_together tests/test_cli.py::test_html_snippet_always_has_color tests/test_cli.py::test_save_html_always_has_color -v
```

Expected: all 8 tests PASS.

- [ ] **Step 7: Run the full test suite**

```bash
uv run pytest -v
```

Expected: all tests PASS. No regressions.

- [ ] **Step 8: Smoke-test manually**

```bash
uv run color-banner "Hello" --palette synthwave --save-html /tmp/test-banner.html
uv run color-banner "Hello" --palette dracula --html-snippet
uv run color-banner "Hello" --palette neon --save-html /tmp/test-nc.html --no-color
```

Expected:
- `/tmp/test-banner.html` opens in a browser showing a colored banner on a dark background
- `--html-snippet` prints `<pre>...</pre>` with color spans to stdout
- `/tmp/test-nc.html` still has color spans despite `--no-color`

- [ ] **Step 9: Commit**

```bash
git add src/color_banner/cli.py tests/test_cli.py
git commit -m "feat: add --save-html and --html-snippet output flags"
```
