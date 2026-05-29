# Design: HTML Export

**Date:** 2026-05-29  
**Status:** Approved

## Summary

Add two new output modes to color-banner:

- `--save-html FILE` — writes a full self-contained HTML page with the colored banner
- `--html-snippet` — prints a `<pre>` HTML snippet to stdout

Both use a shared ANSI-to-HTML converter. No changes to `painter.py`, `color.py`, or the rendering pipeline.

## Architecture

All write operations live in `output.py`. The new HTML functions follow the same pattern as `write_ansi_file` and `write_shell_export`: they accept `list[str]` of already-painted ANSI lines and convert them to the target format.

```
painter.paint() → list[str] (ANSI lines)
                      │
          ┌───────────┼───────────────┐
          ▼           ▼               ▼
  write_ansi_file  write_html_file  write_html_snippet
                      └──────┬───────┘
                   _ansi_to_html_spans()
```

## Changes

### `src/color_banner/output.py`

**`_ansi_to_html_spans(lines: list[str]) -> str`** — private helper.

- Iterates each line character by character (or via regex on the escape sequence `\x1b[38;2;R;G;Bm{char}\x1b[0m`)
- Non-colored characters (spaces and reset-stripped text) are HTML-escaped (`<`, `>`, `&`)
- Colored characters become `<span style="color:rgb(R,G,B)">{escaped_char}</span>`
- Lines joined with `\n` inside a `<pre>` element
- Returns the full `<pre>...</pre>` string

**`write_html_file(lines: list[str], path: str, version: str) -> None`**

Wraps the `<pre>` in a minimal self-contained HTML page:
- `<!DOCTYPE html>` + `<meta charset="utf-8">`
- Dark background: `background:#1a1a1a`, monospace font, padding
- Attribution in an HTML comment in the `<head>`
- No external dependencies (no CDN, no JS)
- Parent directories created automatically
- Raises `OSError` on write failure

**`write_html_snippet(lines: list[str]) -> None`**

Calls `_ansi_to_html_spans()` and prints the `<pre>` block to stdout.

### `src/color_banner/cli.py`

Two new flags in the output options group:

```
--save-html FILE     write self-contained HTML page (dark background, open in browser)
--html-snippet       print <pre> HTML snippet to stdout
```

**Interaction with existing flags:**
- `--save-html` can be combined with `--save`, `--export`, and/or `--html-snippet` in one invocation
- `--html-snippet` counts as an explicit output action: if any of `--save`, `--export`, `--save-html`, or `--html-snippet` are set, the default ANSI stdout is skipped (matching current behavior where `--save` suppresses stdout)
- `--no-color` applies to ANSI outputs only; HTML outputs always include color (they are inherently color-capable)

### `tests/test_output.py`

New tests:
- `_ansi_to_html_spans` converts a single colored character to a `<span style="color:rgb(...)">` element
- `_ansi_to_html_spans` passes spaces through without a span
- `_ansi_to_html_spans` HTML-escapes `<`, `>`, `&` in bare characters
- `write_html_file` creates file with valid HTML structure (`<!DOCTYPE`, `<html`, `<pre`)
- `write_html_file` creates parent directories automatically
- `write_html_snippet` prints a `<pre>` block to stdout (captured via `capsys`)

### `tests/test_cli.py`

New tests:
- `--save-html FILE` creates an HTML file containing `<span style="color:rgb`
- `--html-snippet` prints a `<pre>` block to stdout
- `--save-html` and `--save` can be used together (both files created)
- `--html-snippet` combined with `--save` suppresses ANSI stdout but prints HTML snippet

## Out of Scope

- No `--save-html-all` (parallel to `--save-all`) — can be added later if needed
- No CSS class-based output (inline styles only, for portability)
- No syntax highlighting beyond the gradient colors already in the banner
