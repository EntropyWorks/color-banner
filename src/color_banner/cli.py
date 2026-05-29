# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import argparse
import sys

from color_banner import __version__
from color_banner.color import PALETTES, resolve_stops
from color_banner.output import write_ansi_file, write_ansi_files_all, write_shell_export, write_stdout
from color_banner.painter import paint
from color_banner.renderer import (
    numbered_fonts,
    readable_fonts,
    render,
    resolve_font_identifier,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="color-banner",
        description="Render text as a colorful figlet ASCII banner.",
    )
    parser.add_argument("text", nargs="?", metavar="TEXT", help="Text to render")

    font_group = parser.add_argument_group("font options")
    font_group.add_argument(
        "-f", "--font", default="slant", metavar="FONT",
        help="figlet font name (default: slant)",
    )
    font_group.add_argument(
        "--list-fonts", nargs="?", const="all", metavar="FILTER",
        help="print font names and exit; use 'readable' to show only clean-rendering fonts",
    )
    font_group.add_argument(
        "--all", nargs="?", const="all", metavar="FILTER",
        help="render banner for every font; use 'readable' to skip unreadable fonts",
    )
    font_group.add_argument(
        "--readable", action="store_true",
        help="filter --save-all to readable fonts only",
    )
    font_group.add_argument(
        "--width", type=int, default=80, metavar="N",
        help="terminal width for line-wrapping (default: 80; 0 = never wrap)",
    )

    color_group = parser.add_argument_group("color options")
    mx = color_group.add_mutually_exclusive_group()
    mx.add_argument(
        "--palette", metavar="NAME",
        help="built-in palette name (see --list-palettes for all options)",
    )
    mx.add_argument(
        "--gradient", nargs="+", metavar="HEX",
        help="2-8 hex color stops e.g. --gradient '#ff0080' '#00d4ff'",
    )
    color_group.add_argument(
        "--direction", default="lr", choices=["lr", "tb", "bt", "diag"],
        help="gradient direction: lr|tb|bt|diag (default: lr)",
    )

    out_group = parser.add_argument_group("output options")
    out_group.add_argument(
        "--save", metavar="FILE",
        help="write ANSI escape file (cat-able)",
    )
    out_group.add_argument(
        "--save-all", metavar="DIR",
        help="save banner for every font into DIR as NNN-fontname.ans",
    )
    out_group.add_argument(
        "--export", metavar="FILE",
        help="write self-contained shell function (.sh)",
    )
    out_group.add_argument(
        "--function-name", default="show_banner", metavar="NAME",
        help="function name for --export (default: show_banner)",
    )
    out_group.add_argument(
        "--no-color", action="store_true",
        help="plain text output, no ANSI codes",
    )

    parser.add_argument(
        "--list-palettes", action="store_true",
        help="print built-in palette names and their hex stops",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}",
    )

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    # Validate --width early so it applies to all code paths
    if args.width < 0:
        print("error: --width must be 0 (no wrap) or a positive integer", file=sys.stderr)
        sys.exit(1)

    if args.list_fonts is not None:
        _VALID_FILTERS = ("all", "readable")
        if args.list_fonts not in _VALID_FILTERS:
            print(
                f"error: --list-fonts: unknown filter '{args.list_fonts}'. "
                f"Valid options: readable, or omit for all.",
                file=sys.stderr,
            )
            sys.exit(1)
        font_list = readable_fonts() if args.list_fonts == "readable" else numbered_fonts()
        for num, name in font_list:
            print(f"{num:03d} {name}")
        return

    if args.list_palettes:
        for name, stops in PALETTES.items():
            print(f"{name}: {' -> '.join(stops)}")
        return

    if args.all is not None:
        _VALID_FILTERS = ("all", "readable")
        if args.all not in _VALID_FILTERS:
            print(
                f"error: --all: unknown filter '{args.all}'. "
                f"Valid options: readable, or omit for all.",
                file=sys.stderr,
            )
            sys.exit(1)
        if not args.text:
            print("error: TEXT is required", file=sys.stderr)
            sys.exit(1)
        try:
            stops = resolve_stops(args.palette, args.gradient)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            sys.exit(1)
        font_list = readable_fonts() if args.all == "readable" else numbered_fonts()
        stdout_no_color = args.no_color or not sys.stdout.isatty()
        for num, font_name in font_list:
            print(f"--- {num:03d} {font_name} ---")
            try:
                rows = render(args.text, font=font_name, width=args.width)
            except ValueError:
                continue
            lines = paint(rows, stops, args.direction, no_color=stdout_no_color)
            write_stdout(lines)
            print()
        return

    if args.save_all:
        if not args.text:
            print("error: TEXT is required", file=sys.stderr)
            sys.exit(1)
        try:
            stops = resolve_stops(args.palette, args.gradient)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            sys.exit(1)
        font_list = readable_fonts() if args.readable else numbered_fonts()
        font_banners = []
        for num, font_name in font_list:
            try:
                rows = render(args.text, font=font_name, width=args.width)
            except ValueError:
                continue
            lines = paint(rows, stops, args.direction, no_color=args.no_color)
            font_banners.append((num, font_name, lines))
        try:
            write_ansi_files_all(font_banners, args.save_all, __version__)
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            sys.exit(1)
        return

    if not args.text:
        print("error: TEXT is required", file=sys.stderr)
        sys.exit(1)

    # Resolve color stops — args.gradient is list[str] | None (nargs="+")
    try:
        stops = resolve_stops(args.palette, args.gradient)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    # Resolve font number or name
    try:
        font = resolve_font_identifier(args.font)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    # Validate --function-name early so the error is reported before any rendering
    if args.export:
        from color_banner.output import _VALID_FUNCTION_NAME
        if not _VALID_FUNCTION_NAME.match(args.function_name):
            print(
                f"error: invalid function name '{args.function_name}': "
                "must be a valid bash identifier (letters, digits, underscores; "
                "cannot start with a digit)",
                file=sys.stderr,
            )
            sys.exit(1)

    # Render ASCII art
    try:
        rows = render(args.text, font=font, width=args.width)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    # File output always gets ANSI (unless --no-color explicitly set)
    # Stdout auto-detects TTY and strips ANSI when piped
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
