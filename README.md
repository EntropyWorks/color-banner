# color-banner

Render text as colorful 24-bit figlet ASCII banners in the terminal.
Inspired by [Calligraphy](https://codeberg.org/GeopJr/Calligraphy) by GeopJr.

## Install

```bash
uv tool install color-banner
```

## Usage

```bash
# print to terminal
color-banner "Hello" --palette neon --direction tb

# save a cat-able ANSI file
color-banner "Deploy v2" --palette fire --direction diag --save splash.ans
cat splash.ans

# export a self-contained shell function
color-banner "Deploy v2" --palette fire --export splash.sh
bash splash.sh

# custom hex gradient
color-banner "Hello" --gradient "#ff0080" "#7b2fff" "#00d4ff" --direction lr

# list available palettes
color-banner --list-palettes

# list available fonts
color-banner --list-fonts
```

## License

GPL v3. See [CREDITS.md](CREDITS.md) for attribution.
