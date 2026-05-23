# SPDX-License-Identifier: GPL-3.0-or-later
# Based on Calligraphy by GeopJr <https://codeberg.org/GeopJr/Calligraphy>
# Originally by Gregor "gregorni" Niehl
from __future__ import annotations

import argparse
import sys

from color_banner import __version__
from color_banner.color import PALETTES, resolve_stops
from color_banner.output import write_ansi_file, write_shell_export, write_stdout
from color_banner.painter import paint
from color_banner.renderer import list_fonts, render


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
        "--list-fonts", action="store_true",
        help="print all available font names and exit",
    )

    color_group = parser.add_argument_group("color options")
    mx = color_group.add_mutually_exclusive_group()
    mx.add_argument(
        "--palette", metavar="NAME",
        help="built-in palette name (neon, sunset, ocean, fire, ice, rainbow)",
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

    if args.list_fonts:
        print("\n".join(list_fonts()))
        return

    if args.list_palettes:
        for name, stops in PALETTES.items():
            print(f"{name}: {' -> '.join(stops)}")
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

    # Render ASCII art
    try:
        rows = render(args.text, font=args.font)
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
