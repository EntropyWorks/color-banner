# color-banner

<p align="center">
  <img src="https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/banner.png" alt="color-banner">
</p>

<p align="center">
  <a href="https://pypi.org/project/color-banner/"><img src="https://img.shields.io/pypi/v/color-banner" alt="PyPI version"></a>
  <a href="https://pypi.org/project/color-banner/"><img src="https://img.shields.io/pypi/pyversions/color-banner" alt="Python versions"></a>
  <a href="https://github.com/EntropyWorks/color-banner/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/color-banner" alt="License"></a>
</p>

> Built on the shoulders of [FIGlet](http://www.figlet.org/) (Glenn Chappell & Ian Chai, 1991),
> [pyfiglet](https://github.com/pwaller/pyfiglet) (Christopher Jones, Stefano Rivera, Peter Waller), and
> [Calligraphy](https://codeberg.org/GeopJr/Calligraphy) (GeopJr / Gregor "gregorni" Niehl).
> Licensed under Apache 2.0.

Render text as colorful 24-bit figlet ASCII banners in the terminal.
Designed for CI/CD pipelines, shell startup screens, and BBS-style splash screens.

- [Requirements](#requirements)
- [Install](#install)
- [Usage](#usage)
- [Examples](#examples)
- [Fonts](#fonts)
- [Embedding in a CI pipeline](#embedding-in-a-ci-pipeline)
- [Gallery](#gallery)
- [License](#license)
- [Credits](#credits)

## Requirements

- **Python 3.11+**
- **[pyfiglet](https://github.com/pwaller/pyfiglet) ≥ 1.0.2** — installed automatically as a dependency
- **A 24-bit colour terminal** — required for gradients to render correctly; most modern terminal emulators (iTerm2, GNOME Terminal, Windows Terminal, kitty, Alacritty, etc.) support this; classic xterm and some CI log viewers do not
- **`base64`** (GNU coreutils or macOS built-in) — only needed for the `--export` feature; not required for normal use

## Install

**From PyPI:**

```bash
uv tool install color-banner
```

**From source** (local development):

```bash
git clone https://github.com/EntropyWorks/color-banner
cd color-banner
uv tool install --editable .
```

The editable install means code changes take effect immediately without reinstalling.
To reinstall after pulling updates: `uv tool install --editable .` again, or
`uv tool uninstall color-banner` then reinstall.

## Usage

```
color-banner TEXT [options]

font options:
  -f, --font FONT         figlet font name or 3-digit number (default: slant)
  --list-fonts [FILTER]   list fonts; use 'readable' to filter to clean-rendering fonts
  --all                   render banner for every font (numbered header before each)
  --width N               terminal width for line-wrapping (default: 80; 0 = never wrap)

color options (mutually exclusive):
  --palette NAME          built-in palette name or 'random'; see --list-palettes for all 23
  --gradient HEX [HEX …]  2–8 hex color stops e.g. --gradient '#ff0080' '#00d4ff'
  --direction DIR         gradient direction: lr|tb|bt|diag (default: lr)
  --bg-color HEX          24-bit background color e.g. --bg-color '#1a1a1a'

output options:
  --save FILE             write ANSI escape file (cat-able); parent dirs auto-created
  --save-all DIR          save a banner per font into DIR as NNN-fontname.ans
  --export FILE           write self-contained shell function (.sh)
  --function-name NAME    function name for --export (default: show_banner)
  --save-html FILE        write self-contained HTML page (open in browser)
  --html-snippet          print <pre> HTML snippet to stdout
  --no-color              plain text, no ANSI codes

info:
  --list-palettes         print palette names and hex stops
  --preview-palettes      print palette names rendered in their own colors
  -v, --version           show version and exit
```

## Examples

```bash
# print to terminal
color-banner "Fox and Dog" --palette neon --direction tb

# widen the canvas to avoid line-wrapping with large fonts
color-banner "Fox and Dog" --palette sunset --width 0

# save a cat-able ANSI file (parent directories created automatically)
color-banner "Deploy v2" --palette fire --direction diag --save .ci/banners/splash.ans
cat .ci/banners/splash.ans

# export a portable shell function for CI pipelines
color-banner "Deploy v2" --palette fire --export splash.sh
bash splash.sh

# custom hex gradient, diagonal sweep
color-banner "Hello" --gradient "#ff0080" "#7b2fff" "#00d4ff" --direction diag

# plain figlet text, no color (pipe-safe)
color-banner "Hello" --font ogre --no-color

# list all built-in palettes (23 total: editor themes, rich gradients, and classics)
color-banner --list-palettes

# preview palettes rendered in their own colors
color-banner --preview-palettes

# pick a random palette on each run
color-banner "Hello" --palette random

# add a dark background behind the banner
color-banner "Hello" --palette synthwave --bg-color '#1a1a1a'

# save a browser-viewable HTML page
color-banner "Hello" --palette dracula --save-html banner.html

# print a <pre> HTML snippet to stdout (pipe into a webpage, etc.)
color-banner "Hello" --palette synthwave --html-snippet
```

## Palettes

23 built-in palettes across three categories:

**Editor / terminal themes** (4 stops)

| Name | Colors |
|------|--------|
| `dracula` | purple → pink → cyan → green |
| `nord` | steel blue → periwinkle → sky → teal |
| `monokai` | pink → orange → yellow → lime |
| `gruvbox` | crimson → burnt orange → harvest yellow → olive |
| `catppuccin` | mauve → dusty rose → peach → mint |
| `tokyo` | cornflower → violet → lime → teal |
| `vaporwave` | hot pink → purple → electric cyan → mint |
| `aurora` | sage → sky blue → soft purple → gold |
| `zebra` | near-black → silver → white → silver |

**Rich multi-stop gradients** (6–8 stops)

| Name | Feel |
|------|------|
| `synthwave` | hot pink → deep purple → electric blue |
| `inferno` | black → purple → crimson → orange → incandescent yellow |
| `plasma` | deep indigo → magenta → salmon → neon yellow |
| `galaxy` | deep space → violet → pink → gold → starlight |
| `tropical` | coral → tangerine → lime → turquoise → ocean blue |
| `pride` | full rainbow in flag order |
| `deepsea` | midnight navy → sapphire → teal → seafoam |
| `lava` | near-black red → deep crimson → amber → gold |

**Classics** (original 6)

`neon` · `sunset` · `ocean` · `fire` · `ice` · `rainbow`

Run `color-banner --list-palettes` to see all hex stops.

## Fonts

pyfiglet ships 571 fonts. Use `--list-fonts` to browse them:

```bash
# all fonts with 3-digit index numbers
color-banner --list-fonts

# only the ~514 fonts that render cleanly on a standard terminal
color-banner --list-fonts readable
```

Font numbers are stable — you can use them instead of the name with `--font`:

```bash
# these are equivalent
color-banner "Hello" --font slant
color-banner "Hello" --font 432
```

### Preview every font at once

```bash
# print all banners to stdout
color-banner "Hello" --all --palette neon

# save every font as a numbered .ans file for offline browsing
color-banner "Hello" --palette neon --save-all ./font-preview
ls font-preview/
# 001-1943____.ans  002-1row.ans  003-3-d.ans …
cat font-preview/432-slant.ans
```

## Embedding in a CI pipeline

Generate the splash once and commit the `.sh` file:

```bash
color-banner "🚀 Deploying" --palette sunset --export .ci/splash.sh
```

Then in your pipeline script:

```bash
source .ci/splash.sh
show_banner
```

## Gallery

### Showcase

| neon | sunset | ocean |
|------|--------|-------|
| ![future neon](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_neon_lr.png) | ![dos_rebel sunset](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_sunset_lr.png) | ![electronic ocean](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bloody fire](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_fire_lr.png) | ![thick ice](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_ice_lr.png) | ![pagga rainbow](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_rainbow_lr.png) |

### All fonts

Each section below shows all six built-in palettes rendered with that font.
Click a font name to expand.

> **Note:** This is a small sample of the 571 bundled fonts — many others produce
> great results too. Not every font works well with color-banner; some render
> cleanly only with uppercase input, and others may produce garbled output
> regardless. Use `--list-fonts readable` to get a pre-filtered list of fonts
> that tend to render reliably. (Work is ongoing to improve the readability
> filter so it catches more edge cases, including uppercase-only fonts.)

<details>
<summary><strong>ansi_regular</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_regular neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_neon_lr.png) | ![ansi_regular sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_sunset_lr.png) | ![ansi_regular ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_regular fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_fire_lr.png) | ![ansi_regular ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_ice_lr.png) | ![ansi_regular rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_regular neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_neon_tb.png) | ![ansi_regular sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_sunset_tb.png) | ![ansi_regular ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_regular fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_fire_tb.png) | ![ansi_regular ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_ice_tb.png) | ![ansi_regular rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_regular neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_neon_bt.png) | ![ansi_regular sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_sunset_bt.png) | ![ansi_regular ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_regular fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_fire_bt.png) | ![ansi_regular ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_ice_bt.png) | ![ansi_regular rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_regular neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_neon_diag.png) | ![ansi_regular sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_sunset_diag.png) | ![ansi_regular ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_regular fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_fire_diag.png) | ![ansi_regular ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_ice_diag.png) | ![ansi_regular rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_regular_rainbow_diag.png) |

</details>

<details>
<summary><strong>ansi_shadow</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_shadow neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_neon_lr.png) | ![ansi_shadow sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_sunset_lr.png) | ![ansi_shadow ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_shadow fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_fire_lr.png) | ![ansi_shadow ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_ice_lr.png) | ![ansi_shadow rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_shadow neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_neon_tb.png) | ![ansi_shadow sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_sunset_tb.png) | ![ansi_shadow ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_shadow fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_fire_tb.png) | ![ansi_shadow ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_ice_tb.png) | ![ansi_shadow rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_shadow neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_neon_bt.png) | ![ansi_shadow sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_sunset_bt.png) | ![ansi_shadow ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_shadow fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_fire_bt.png) | ![ansi_shadow ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_ice_bt.png) | ![ansi_shadow rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_shadow neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_neon_diag.png) | ![ansi_shadow sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_sunset_diag.png) | ![ansi_shadow ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_shadow fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_fire_diag.png) | ![ansi_shadow ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_ice_diag.png) | ![ansi_shadow rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/ansi_shadow_rainbow_diag.png) |

</details>

<details>
<summary><strong>bigmono12</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono12 neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_neon_lr.png) | ![bigmono12 sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_sunset_lr.png) | ![bigmono12 ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono12 fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_fire_lr.png) | ![bigmono12 ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_ice_lr.png) | ![bigmono12 rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono12 neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_neon_tb.png) | ![bigmono12 sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_sunset_tb.png) | ![bigmono12 ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono12 fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_fire_tb.png) | ![bigmono12 ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_ice_tb.png) | ![bigmono12 rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono12 neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_neon_bt.png) | ![bigmono12 sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_sunset_bt.png) | ![bigmono12 ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono12 fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_fire_bt.png) | ![bigmono12 ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_ice_bt.png) | ![bigmono12 rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono12 neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_neon_diag.png) | ![bigmono12 sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_sunset_diag.png) | ![bigmono12 ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono12 fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_fire_diag.png) | ![bigmono12 ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_ice_diag.png) | ![bigmono12 rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono12_rainbow_diag.png) |

</details>

<details>
<summary><strong>bigmono9</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono9 neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_neon_lr.png) | ![bigmono9 sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_sunset_lr.png) | ![bigmono9 ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono9 fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_fire_lr.png) | ![bigmono9 ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_ice_lr.png) | ![bigmono9 rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono9 neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_neon_tb.png) | ![bigmono9 sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_sunset_tb.png) | ![bigmono9 ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono9 fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_fire_tb.png) | ![bigmono9 ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_ice_tb.png) | ![bigmono9 rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono9 neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_neon_bt.png) | ![bigmono9 sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_sunset_bt.png) | ![bigmono9 ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono9 fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_fire_bt.png) | ![bigmono9 ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_ice_bt.png) | ![bigmono9 rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono9 neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_neon_diag.png) | ![bigmono9 sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_sunset_diag.png) | ![bigmono9 ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono9 fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_fire_diag.png) | ![bigmono9 ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_ice_diag.png) | ![bigmono9 rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bigmono9_rainbow_diag.png) |

</details>

<details>
<summary><strong>bloody</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![bloody neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_neon_lr.png) | ![bloody sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_sunset_lr.png) | ![bloody ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bloody fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_fire_lr.png) | ![bloody ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_ice_lr.png) | ![bloody rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![bloody neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_neon_tb.png) | ![bloody sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_sunset_tb.png) | ![bloody ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bloody fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_fire_tb.png) | ![bloody ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_ice_tb.png) | ![bloody rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![bloody neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_neon_bt.png) | ![bloody sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_sunset_bt.png) | ![bloody ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bloody fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_fire_bt.png) | ![bloody ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_ice_bt.png) | ![bloody rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![bloody neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_neon_diag.png) | ![bloody sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_sunset_diag.png) | ![bloody ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bloody fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_fire_diag.png) | ![bloody ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_ice_diag.png) | ![bloody rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/bloody_rainbow_diag.png) |

</details>

<details>
<summary><strong>delta_corps_priest_1</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![delta_corps_priest_1 neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_neon_lr.png) | ![delta_corps_priest_1 sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_sunset_lr.png) | ![delta_corps_priest_1 ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![delta_corps_priest_1 fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_fire_lr.png) | ![delta_corps_priest_1 ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_ice_lr.png) | ![delta_corps_priest_1 rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![delta_corps_priest_1 neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_neon_tb.png) | ![delta_corps_priest_1 sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_sunset_tb.png) | ![delta_corps_priest_1 ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![delta_corps_priest_1 fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_fire_tb.png) | ![delta_corps_priest_1 ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_ice_tb.png) | ![delta_corps_priest_1 rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![delta_corps_priest_1 neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_neon_bt.png) | ![delta_corps_priest_1 sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_sunset_bt.png) | ![delta_corps_priest_1 ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![delta_corps_priest_1 fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_fire_bt.png) | ![delta_corps_priest_1 ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_ice_bt.png) | ![delta_corps_priest_1 rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![delta_corps_priest_1 neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_neon_diag.png) | ![delta_corps_priest_1 sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_sunset_diag.png) | ![delta_corps_priest_1 ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![delta_corps_priest_1 fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_fire_diag.png) | ![delta_corps_priest_1 ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_ice_diag.png) | ![delta_corps_priest_1 rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/delta_corps_priest_1_rainbow_diag.png) |

</details>

<details>
<summary><strong>dos_rebel</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![dos_rebel neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_neon_lr.png) | ![dos_rebel sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_sunset_lr.png) | ![dos_rebel ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![dos_rebel fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_fire_lr.png) | ![dos_rebel ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_ice_lr.png) | ![dos_rebel rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![dos_rebel neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_neon_tb.png) | ![dos_rebel sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_sunset_tb.png) | ![dos_rebel ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![dos_rebel fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_fire_tb.png) | ![dos_rebel ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_ice_tb.png) | ![dos_rebel rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![dos_rebel neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_neon_bt.png) | ![dos_rebel sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_sunset_bt.png) | ![dos_rebel ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![dos_rebel fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_fire_bt.png) | ![dos_rebel ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_ice_bt.png) | ![dos_rebel rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![dos_rebel neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_neon_diag.png) | ![dos_rebel sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_sunset_diag.png) | ![dos_rebel ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![dos_rebel fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_fire_diag.png) | ![dos_rebel ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_ice_diag.png) | ![dos_rebel rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/dos_rebel_rainbow_diag.png) |

</details>

<details>
<summary><strong>double_blocky</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![double_blocky neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_neon_lr.png) | ![double_blocky sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_sunset_lr.png) | ![double_blocky ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![double_blocky fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_fire_lr.png) | ![double_blocky ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_ice_lr.png) | ![double_blocky rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![double_blocky neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_neon_tb.png) | ![double_blocky sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_sunset_tb.png) | ![double_blocky ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![double_blocky fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_fire_tb.png) | ![double_blocky ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_ice_tb.png) | ![double_blocky rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![double_blocky neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_neon_bt.png) | ![double_blocky sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_sunset_bt.png) | ![double_blocky ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![double_blocky fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_fire_bt.png) | ![double_blocky ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_ice_bt.png) | ![double_blocky rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![double_blocky neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_neon_diag.png) | ![double_blocky sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_sunset_diag.png) | ![double_blocky ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![double_blocky fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_fire_diag.png) | ![double_blocky ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_ice_diag.png) | ![double_blocky rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/double_blocky_rainbow_diag.png) |

</details>

<details>
<summary><strong>electronic</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![electronic neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_neon_lr.png) | ![electronic sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_sunset_lr.png) | ![electronic ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![electronic fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_fire_lr.png) | ![electronic ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_ice_lr.png) | ![electronic rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![electronic neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_neon_tb.png) | ![electronic sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_sunset_tb.png) | ![electronic ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![electronic fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_fire_tb.png) | ![electronic ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_ice_tb.png) | ![electronic rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![electronic neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_neon_bt.png) | ![electronic sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_sunset_bt.png) | ![electronic ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![electronic fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_fire_bt.png) | ![electronic ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_ice_bt.png) | ![electronic rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![electronic neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_neon_diag.png) | ![electronic sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_sunset_diag.png) | ![electronic ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![electronic fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_fire_diag.png) | ![electronic ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_ice_diag.png) | ![electronic rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/electronic_rainbow_diag.png) |

</details>

<details>
<summary><strong>elite</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![elite neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_neon_lr.png) | ![elite sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_sunset_lr.png) | ![elite ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![elite fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_fire_lr.png) | ![elite ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_ice_lr.png) | ![elite rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![elite neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_neon_tb.png) | ![elite sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_sunset_tb.png) | ![elite ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![elite fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_fire_tb.png) | ![elite ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_ice_tb.png) | ![elite rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![elite neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_neon_bt.png) | ![elite sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_sunset_bt.png) | ![elite ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![elite fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_fire_bt.png) | ![elite ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_ice_bt.png) | ![elite rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![elite neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_neon_diag.png) | ![elite sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_sunset_diag.png) | ![elite ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![elite fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_fire_diag.png) | ![elite ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_ice_diag.png) | ![elite rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/elite_rainbow_diag.png) |

</details>

<details>
<summary><strong>future</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![future neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_neon_lr.png) | ![future sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_sunset_lr.png) | ![future ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![future fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_fire_lr.png) | ![future ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_ice_lr.png) | ![future rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![future neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_neon_tb.png) | ![future sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_sunset_tb.png) | ![future ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![future fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_fire_tb.png) | ![future ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_ice_tb.png) | ![future rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![future neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_neon_bt.png) | ![future sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_sunset_bt.png) | ![future ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![future fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_fire_bt.png) | ![future ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_ice_bt.png) | ![future rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![future neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_neon_diag.png) | ![future sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_sunset_diag.png) | ![future ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![future fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_fire_diag.png) | ![future ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_ice_diag.png) | ![future rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/future_rainbow_diag.png) |

</details>

<details>
<summary><strong>mono12</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono12 neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_neon_lr.png) | ![mono12 sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_sunset_lr.png) | ![mono12 ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono12 fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_fire_lr.png) | ![mono12 ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_ice_lr.png) | ![mono12 rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono12 neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_neon_tb.png) | ![mono12 sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_sunset_tb.png) | ![mono12 ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono12 fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_fire_tb.png) | ![mono12 ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_ice_tb.png) | ![mono12 rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono12 neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_neon_bt.png) | ![mono12 sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_sunset_bt.png) | ![mono12 ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono12 fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_fire_bt.png) | ![mono12 ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_ice_bt.png) | ![mono12 rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono12 neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_neon_diag.png) | ![mono12 sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_sunset_diag.png) | ![mono12 ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono12 fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_fire_diag.png) | ![mono12 ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_ice_diag.png) | ![mono12 rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono12_rainbow_diag.png) |

</details>

<details>
<summary><strong>mono9</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono9 neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_neon_lr.png) | ![mono9 sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_sunset_lr.png) | ![mono9 ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono9 fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_fire_lr.png) | ![mono9 ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_ice_lr.png) | ![mono9 rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono9 neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_neon_tb.png) | ![mono9 sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_sunset_tb.png) | ![mono9 ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono9 fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_fire_tb.png) | ![mono9 ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_ice_tb.png) | ![mono9 rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono9 neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_neon_bt.png) | ![mono9 sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_sunset_bt.png) | ![mono9 ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono9 fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_fire_bt.png) | ![mono9 ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_ice_bt.png) | ![mono9 rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono9 neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_neon_diag.png) | ![mono9 sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_sunset_diag.png) | ![mono9 ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono9 fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_fire_diag.png) | ![mono9 ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_ice_diag.png) | ![mono9 rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/mono9_rainbow_diag.png) |

</details>

<details>
<summary><strong>pagga</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![pagga neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_neon_lr.png) | ![pagga sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_sunset_lr.png) | ![pagga ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![pagga fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_fire_lr.png) | ![pagga ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_ice_lr.png) | ![pagga rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![pagga neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_neon_tb.png) | ![pagga sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_sunset_tb.png) | ![pagga ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![pagga fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_fire_tb.png) | ![pagga ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_ice_tb.png) | ![pagga rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![pagga neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_neon_bt.png) | ![pagga sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_sunset_bt.png) | ![pagga ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![pagga fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_fire_bt.png) | ![pagga ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_ice_bt.png) | ![pagga rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![pagga neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_neon_diag.png) | ![pagga sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_sunset_diag.png) | ![pagga ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![pagga fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_fire_diag.png) | ![pagga ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_ice_diag.png) | ![pagga rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/pagga_rainbow_diag.png) |

</details>

<details>
<summary><strong>smmono12</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono12 neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_neon_lr.png) | ![smmono12 sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_sunset_lr.png) | ![smmono12 ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono12 fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_fire_lr.png) | ![smmono12 ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_ice_lr.png) | ![smmono12 rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono12 neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_neon_tb.png) | ![smmono12 sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_sunset_tb.png) | ![smmono12 ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono12 fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_fire_tb.png) | ![smmono12 ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_ice_tb.png) | ![smmono12 rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono12 neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_neon_bt.png) | ![smmono12 sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_sunset_bt.png) | ![smmono12 ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono12 fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_fire_bt.png) | ![smmono12 ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_ice_bt.png) | ![smmono12 rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono12 neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_neon_diag.png) | ![smmono12 sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_sunset_diag.png) | ![smmono12 ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono12 fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_fire_diag.png) | ![smmono12 ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_ice_diag.png) | ![smmono12 rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono12_rainbow_diag.png) |

</details>

<details>
<summary><strong>smmono9</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono9 neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_neon_lr.png) | ![smmono9 sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_sunset_lr.png) | ![smmono9 ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono9 fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_fire_lr.png) | ![smmono9 ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_ice_lr.png) | ![smmono9 rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono9 neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_neon_tb.png) | ![smmono9 sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_sunset_tb.png) | ![smmono9 ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono9 fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_fire_tb.png) | ![smmono9 ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_ice_tb.png) | ![smmono9 rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono9 neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_neon_bt.png) | ![smmono9 sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_sunset_bt.png) | ![smmono9 ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono9 fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_fire_bt.png) | ![smmono9 ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_ice_bt.png) | ![smmono9 rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono9 neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_neon_diag.png) | ![smmono9 sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_sunset_diag.png) | ![smmono9 ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono9 fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_fire_diag.png) | ![smmono9 ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_ice_diag.png) | ![smmono9 rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/smmono9_rainbow_diag.png) |

</details>

<details>
<summary><strong>thick</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![thick neon lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_neon_lr.png) | ![thick sunset lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_sunset_lr.png) | ![thick ocean lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![thick fire lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_fire_lr.png) | ![thick ice lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_ice_lr.png) | ![thick rainbow lr](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![thick neon tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_neon_tb.png) | ![thick sunset tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_sunset_tb.png) | ![thick ocean tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![thick fire tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_fire_tb.png) | ![thick ice tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_ice_tb.png) | ![thick rainbow tb](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![thick neon bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_neon_bt.png) | ![thick sunset bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_sunset_bt.png) | ![thick ocean bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![thick fire bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_fire_bt.png) | ![thick ice bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_ice_bt.png) | ![thick rainbow bt](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![thick neon diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_neon_diag.png) | ![thick sunset diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_sunset_diag.png) | ![thick ocean diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![thick fire diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_fire_diag.png) | ![thick ice diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_ice_diag.png) | ![thick rainbow diag](https://raw.githubusercontent.com/EntropyWorks/color-banner/main/assets/examples/thick_rainbow_diag.png) |

</details>


## License

Apache 2.0 — see [LICENSE](LICENSE), [NOTICE](NOTICE), and [CREDITS.md](CREDITS.md).

## Credits

The rendering engine is [pyfiglet](https://github.com/pwaller/pyfiglet) by Peter Waller,
a pure-Python port of [FIGlet](http://www.figlet.org/) — the original ASCII art renderer
created by Glenn Chappell and Ian Chai in 1991. The 571 bundled fonts and the `.flf` font
format originate from the FIGlet project.

The concept and design are inspired by
[Calligraphy](https://codeberg.org/GeopJr/Calligraphy) by GeopJr,
originally by Gregor "gregorni" Niehl.

See [CREDITS.md](CREDITS.md) for full details and [NOTICE](NOTICE) for the
third-party attribution notices required by Apache 2.0.
