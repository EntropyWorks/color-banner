# color-banner

<p align="center">
  <img src="assets/banner.png" alt="color-banner">
</p>
> Built on the shoulders of [FIGlet](http://www.figlet.org/) (Glenn Chappell & Ian Chai, 1991),
> [pyfiglet](https://github.com/pwaller/pyfiglet) (Christopher Jones, Stefano Rivera, Peter Waller), and
> [Calligraphy](https://codeberg.org/GeopJr/Calligraphy) (GeopJr / Gregor "gregorni" Niehl).
> Licensed under Apache 2.0.

Render text as colorful 24-bit figlet ASCII banners in the terminal.
Designed for CICD pipelines, shell startup screens, and BBS-style splash screens.

- [Install](#install)
- [Usage](#usage)
- [Examples](#examples)
- [Fonts](#fonts)
- [Embedding in a CI pipeline](#embedding-in-a-ci-pipeline)
- [Gallery](#gallery)
- [License](#license)
- [Credits](#credits)

## Install

**From PyPI** (once published):

```bash
uv tool install color-banner
```

**From source** (local development):

```bash
git clone <repo-url>
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
  --palette NAME          built-in palette: neon sunset ocean fire ice rainbow
  --gradient HEX [HEX …]  2–8 hex color stops e.g. --gradient '#ff0080' '#00d4ff'
  --direction DIR         gradient direction: lr|tb|bt|diag (default: lr)

output options:
  --save FILE             write ANSI escape file (cat-able); parent dirs auto-created
  --save-all DIR          save a banner per font into DIR as NNN-fontname.ans
  --export FILE           write self-contained shell function (.sh)
  --function-name NAME    function name for --export (default: show_banner)
  --no-color              plain text, no ANSI codes

info:
  --list-palettes         print palette names and hex stops
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

# list all built-in palettes
color-banner --list-palettes
```

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
| ![ansi_regular neon lr](assets/examples/ansi_regular_neon_lr.png) | ![ansi_regular sunset lr](assets/examples/ansi_regular_sunset_lr.png) | ![ansi_regular ocean lr](assets/examples/ansi_regular_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_regular fire lr](assets/examples/ansi_regular_fire_lr.png) | ![ansi_regular ice lr](assets/examples/ansi_regular_ice_lr.png) | ![ansi_regular rainbow lr](assets/examples/ansi_regular_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_regular neon tb](assets/examples/ansi_regular_neon_tb.png) | ![ansi_regular sunset tb](assets/examples/ansi_regular_sunset_tb.png) | ![ansi_regular ocean tb](assets/examples/ansi_regular_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_regular fire tb](assets/examples/ansi_regular_fire_tb.png) | ![ansi_regular ice tb](assets/examples/ansi_regular_ice_tb.png) | ![ansi_regular rainbow tb](assets/examples/ansi_regular_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_regular neon bt](assets/examples/ansi_regular_neon_bt.png) | ![ansi_regular sunset bt](assets/examples/ansi_regular_sunset_bt.png) | ![ansi_regular ocean bt](assets/examples/ansi_regular_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_regular fire bt](assets/examples/ansi_regular_fire_bt.png) | ![ansi_regular ice bt](assets/examples/ansi_regular_ice_bt.png) | ![ansi_regular rainbow bt](assets/examples/ansi_regular_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_regular neon diag](assets/examples/ansi_regular_neon_diag.png) | ![ansi_regular sunset diag](assets/examples/ansi_regular_sunset_diag.png) | ![ansi_regular ocean diag](assets/examples/ansi_regular_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_regular fire diag](assets/examples/ansi_regular_fire_diag.png) | ![ansi_regular ice diag](assets/examples/ansi_regular_ice_diag.png) | ![ansi_regular rainbow diag](assets/examples/ansi_regular_rainbow_diag.png) |

</details>

<details>
<summary><strong>ansi_shadow</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_shadow neon lr](assets/examples/ansi_shadow_neon_lr.png) | ![ansi_shadow sunset lr](assets/examples/ansi_shadow_sunset_lr.png) | ![ansi_shadow ocean lr](assets/examples/ansi_shadow_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_shadow fire lr](assets/examples/ansi_shadow_fire_lr.png) | ![ansi_shadow ice lr](assets/examples/ansi_shadow_ice_lr.png) | ![ansi_shadow rainbow lr](assets/examples/ansi_shadow_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_shadow neon tb](assets/examples/ansi_shadow_neon_tb.png) | ![ansi_shadow sunset tb](assets/examples/ansi_shadow_sunset_tb.png) | ![ansi_shadow ocean tb](assets/examples/ansi_shadow_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_shadow fire tb](assets/examples/ansi_shadow_fire_tb.png) | ![ansi_shadow ice tb](assets/examples/ansi_shadow_ice_tb.png) | ![ansi_shadow rainbow tb](assets/examples/ansi_shadow_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_shadow neon bt](assets/examples/ansi_shadow_neon_bt.png) | ![ansi_shadow sunset bt](assets/examples/ansi_shadow_sunset_bt.png) | ![ansi_shadow ocean bt](assets/examples/ansi_shadow_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_shadow fire bt](assets/examples/ansi_shadow_fire_bt.png) | ![ansi_shadow ice bt](assets/examples/ansi_shadow_ice_bt.png) | ![ansi_shadow rainbow bt](assets/examples/ansi_shadow_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_shadow neon diag](assets/examples/ansi_shadow_neon_diag.png) | ![ansi_shadow sunset diag](assets/examples/ansi_shadow_sunset_diag.png) | ![ansi_shadow ocean diag](assets/examples/ansi_shadow_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_shadow fire diag](assets/examples/ansi_shadow_fire_diag.png) | ![ansi_shadow ice diag](assets/examples/ansi_shadow_ice_diag.png) | ![ansi_shadow rainbow diag](assets/examples/ansi_shadow_rainbow_diag.png) |

</details>

<details>
<summary><strong>bigmono12</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono12 neon lr](assets/examples/bigmono12_neon_lr.png) | ![bigmono12 sunset lr](assets/examples/bigmono12_sunset_lr.png) | ![bigmono12 ocean lr](assets/examples/bigmono12_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono12 fire lr](assets/examples/bigmono12_fire_lr.png) | ![bigmono12 ice lr](assets/examples/bigmono12_ice_lr.png) | ![bigmono12 rainbow lr](assets/examples/bigmono12_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono12 neon tb](assets/examples/bigmono12_neon_tb.png) | ![bigmono12 sunset tb](assets/examples/bigmono12_sunset_tb.png) | ![bigmono12 ocean tb](assets/examples/bigmono12_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono12 fire tb](assets/examples/bigmono12_fire_tb.png) | ![bigmono12 ice tb](assets/examples/bigmono12_ice_tb.png) | ![bigmono12 rainbow tb](assets/examples/bigmono12_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono12 neon bt](assets/examples/bigmono12_neon_bt.png) | ![bigmono12 sunset bt](assets/examples/bigmono12_sunset_bt.png) | ![bigmono12 ocean bt](assets/examples/bigmono12_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono12 fire bt](assets/examples/bigmono12_fire_bt.png) | ![bigmono12 ice bt](assets/examples/bigmono12_ice_bt.png) | ![bigmono12 rainbow bt](assets/examples/bigmono12_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono12 neon diag](assets/examples/bigmono12_neon_diag.png) | ![bigmono12 sunset diag](assets/examples/bigmono12_sunset_diag.png) | ![bigmono12 ocean diag](assets/examples/bigmono12_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono12 fire diag](assets/examples/bigmono12_fire_diag.png) | ![bigmono12 ice diag](assets/examples/bigmono12_ice_diag.png) | ![bigmono12 rainbow diag](assets/examples/bigmono12_rainbow_diag.png) |

</details>

<details>
<summary><strong>bigmono9</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono9 neon lr](assets/examples/bigmono9_neon_lr.png) | ![bigmono9 sunset lr](assets/examples/bigmono9_sunset_lr.png) | ![bigmono9 ocean lr](assets/examples/bigmono9_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono9 fire lr](assets/examples/bigmono9_fire_lr.png) | ![bigmono9 ice lr](assets/examples/bigmono9_ice_lr.png) | ![bigmono9 rainbow lr](assets/examples/bigmono9_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono9 neon tb](assets/examples/bigmono9_neon_tb.png) | ![bigmono9 sunset tb](assets/examples/bigmono9_sunset_tb.png) | ![bigmono9 ocean tb](assets/examples/bigmono9_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono9 fire tb](assets/examples/bigmono9_fire_tb.png) | ![bigmono9 ice tb](assets/examples/bigmono9_ice_tb.png) | ![bigmono9 rainbow tb](assets/examples/bigmono9_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono9 neon bt](assets/examples/bigmono9_neon_bt.png) | ![bigmono9 sunset bt](assets/examples/bigmono9_sunset_bt.png) | ![bigmono9 ocean bt](assets/examples/bigmono9_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono9 fire bt](assets/examples/bigmono9_fire_bt.png) | ![bigmono9 ice bt](assets/examples/bigmono9_ice_bt.png) | ![bigmono9 rainbow bt](assets/examples/bigmono9_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono9 neon diag](assets/examples/bigmono9_neon_diag.png) | ![bigmono9 sunset diag](assets/examples/bigmono9_sunset_diag.png) | ![bigmono9 ocean diag](assets/examples/bigmono9_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono9 fire diag](assets/examples/bigmono9_fire_diag.png) | ![bigmono9 ice diag](assets/examples/bigmono9_ice_diag.png) | ![bigmono9 rainbow diag](assets/examples/bigmono9_rainbow_diag.png) |

</details>

<details>
<summary><strong>bloody</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![bloody neon lr](assets/examples/bloody_neon_lr.png) | ![bloody sunset lr](assets/examples/bloody_sunset_lr.png) | ![bloody ocean lr](assets/examples/bloody_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bloody fire lr](assets/examples/bloody_fire_lr.png) | ![bloody ice lr](assets/examples/bloody_ice_lr.png) | ![bloody rainbow lr](assets/examples/bloody_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![bloody neon tb](assets/examples/bloody_neon_tb.png) | ![bloody sunset tb](assets/examples/bloody_sunset_tb.png) | ![bloody ocean tb](assets/examples/bloody_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bloody fire tb](assets/examples/bloody_fire_tb.png) | ![bloody ice tb](assets/examples/bloody_ice_tb.png) | ![bloody rainbow tb](assets/examples/bloody_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![bloody neon bt](assets/examples/bloody_neon_bt.png) | ![bloody sunset bt](assets/examples/bloody_sunset_bt.png) | ![bloody ocean bt](assets/examples/bloody_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bloody fire bt](assets/examples/bloody_fire_bt.png) | ![bloody ice bt](assets/examples/bloody_ice_bt.png) | ![bloody rainbow bt](assets/examples/bloody_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![bloody neon diag](assets/examples/bloody_neon_diag.png) | ![bloody sunset diag](assets/examples/bloody_sunset_diag.png) | ![bloody ocean diag](assets/examples/bloody_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bloody fire diag](assets/examples/bloody_fire_diag.png) | ![bloody ice diag](assets/examples/bloody_ice_diag.png) | ![bloody rainbow diag](assets/examples/bloody_rainbow_diag.png) |

</details>

<details>
<summary><strong>delta_corps_priest_1</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![delta_corps_priest_1 neon lr](assets/examples/delta_corps_priest_1_neon_lr.png) | ![delta_corps_priest_1 sunset lr](assets/examples/delta_corps_priest_1_sunset_lr.png) | ![delta_corps_priest_1 ocean lr](assets/examples/delta_corps_priest_1_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![delta_corps_priest_1 fire lr](assets/examples/delta_corps_priest_1_fire_lr.png) | ![delta_corps_priest_1 ice lr](assets/examples/delta_corps_priest_1_ice_lr.png) | ![delta_corps_priest_1 rainbow lr](assets/examples/delta_corps_priest_1_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![delta_corps_priest_1 neon tb](assets/examples/delta_corps_priest_1_neon_tb.png) | ![delta_corps_priest_1 sunset tb](assets/examples/delta_corps_priest_1_sunset_tb.png) | ![delta_corps_priest_1 ocean tb](assets/examples/delta_corps_priest_1_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![delta_corps_priest_1 fire tb](assets/examples/delta_corps_priest_1_fire_tb.png) | ![delta_corps_priest_1 ice tb](assets/examples/delta_corps_priest_1_ice_tb.png) | ![delta_corps_priest_1 rainbow tb](assets/examples/delta_corps_priest_1_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![delta_corps_priest_1 neon bt](assets/examples/delta_corps_priest_1_neon_bt.png) | ![delta_corps_priest_1 sunset bt](assets/examples/delta_corps_priest_1_sunset_bt.png) | ![delta_corps_priest_1 ocean bt](assets/examples/delta_corps_priest_1_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![delta_corps_priest_1 fire bt](assets/examples/delta_corps_priest_1_fire_bt.png) | ![delta_corps_priest_1 ice bt](assets/examples/delta_corps_priest_1_ice_bt.png) | ![delta_corps_priest_1 rainbow bt](assets/examples/delta_corps_priest_1_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![delta_corps_priest_1 neon diag](assets/examples/delta_corps_priest_1_neon_diag.png) | ![delta_corps_priest_1 sunset diag](assets/examples/delta_corps_priest_1_sunset_diag.png) | ![delta_corps_priest_1 ocean diag](assets/examples/delta_corps_priest_1_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![delta_corps_priest_1 fire diag](assets/examples/delta_corps_priest_1_fire_diag.png) | ![delta_corps_priest_1 ice diag](assets/examples/delta_corps_priest_1_ice_diag.png) | ![delta_corps_priest_1 rainbow diag](assets/examples/delta_corps_priest_1_rainbow_diag.png) |

</details>

<details>
<summary><strong>dos_rebel</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![dos_rebel neon lr](assets/examples/dos_rebel_neon_lr.png) | ![dos_rebel sunset lr](assets/examples/dos_rebel_sunset_lr.png) | ![dos_rebel ocean lr](assets/examples/dos_rebel_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![dos_rebel fire lr](assets/examples/dos_rebel_fire_lr.png) | ![dos_rebel ice lr](assets/examples/dos_rebel_ice_lr.png) | ![dos_rebel rainbow lr](assets/examples/dos_rebel_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![dos_rebel neon tb](assets/examples/dos_rebel_neon_tb.png) | ![dos_rebel sunset tb](assets/examples/dos_rebel_sunset_tb.png) | ![dos_rebel ocean tb](assets/examples/dos_rebel_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![dos_rebel fire tb](assets/examples/dos_rebel_fire_tb.png) | ![dos_rebel ice tb](assets/examples/dos_rebel_ice_tb.png) | ![dos_rebel rainbow tb](assets/examples/dos_rebel_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![dos_rebel neon bt](assets/examples/dos_rebel_neon_bt.png) | ![dos_rebel sunset bt](assets/examples/dos_rebel_sunset_bt.png) | ![dos_rebel ocean bt](assets/examples/dos_rebel_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![dos_rebel fire bt](assets/examples/dos_rebel_fire_bt.png) | ![dos_rebel ice bt](assets/examples/dos_rebel_ice_bt.png) | ![dos_rebel rainbow bt](assets/examples/dos_rebel_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![dos_rebel neon diag](assets/examples/dos_rebel_neon_diag.png) | ![dos_rebel sunset diag](assets/examples/dos_rebel_sunset_diag.png) | ![dos_rebel ocean diag](assets/examples/dos_rebel_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![dos_rebel fire diag](assets/examples/dos_rebel_fire_diag.png) | ![dos_rebel ice diag](assets/examples/dos_rebel_ice_diag.png) | ![dos_rebel rainbow diag](assets/examples/dos_rebel_rainbow_diag.png) |

</details>

<details>
<summary><strong>double_blocky</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![double_blocky neon lr](assets/examples/double_blocky_neon_lr.png) | ![double_blocky sunset lr](assets/examples/double_blocky_sunset_lr.png) | ![double_blocky ocean lr](assets/examples/double_blocky_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![double_blocky fire lr](assets/examples/double_blocky_fire_lr.png) | ![double_blocky ice lr](assets/examples/double_blocky_ice_lr.png) | ![double_blocky rainbow lr](assets/examples/double_blocky_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![double_blocky neon tb](assets/examples/double_blocky_neon_tb.png) | ![double_blocky sunset tb](assets/examples/double_blocky_sunset_tb.png) | ![double_blocky ocean tb](assets/examples/double_blocky_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![double_blocky fire tb](assets/examples/double_blocky_fire_tb.png) | ![double_blocky ice tb](assets/examples/double_blocky_ice_tb.png) | ![double_blocky rainbow tb](assets/examples/double_blocky_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![double_blocky neon bt](assets/examples/double_blocky_neon_bt.png) | ![double_blocky sunset bt](assets/examples/double_blocky_sunset_bt.png) | ![double_blocky ocean bt](assets/examples/double_blocky_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![double_blocky fire bt](assets/examples/double_blocky_fire_bt.png) | ![double_blocky ice bt](assets/examples/double_blocky_ice_bt.png) | ![double_blocky rainbow bt](assets/examples/double_blocky_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![double_blocky neon diag](assets/examples/double_blocky_neon_diag.png) | ![double_blocky sunset diag](assets/examples/double_blocky_sunset_diag.png) | ![double_blocky ocean diag](assets/examples/double_blocky_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![double_blocky fire diag](assets/examples/double_blocky_fire_diag.png) | ![double_blocky ice diag](assets/examples/double_blocky_ice_diag.png) | ![double_blocky rainbow diag](assets/examples/double_blocky_rainbow_diag.png) |

</details>

<details>
<summary><strong>electronic</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![electronic neon lr](assets/examples/electronic_neon_lr.png) | ![electronic sunset lr](assets/examples/electronic_sunset_lr.png) | ![electronic ocean lr](assets/examples/electronic_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![electronic fire lr](assets/examples/electronic_fire_lr.png) | ![electronic ice lr](assets/examples/electronic_ice_lr.png) | ![electronic rainbow lr](assets/examples/electronic_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![electronic neon tb](assets/examples/electronic_neon_tb.png) | ![electronic sunset tb](assets/examples/electronic_sunset_tb.png) | ![electronic ocean tb](assets/examples/electronic_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![electronic fire tb](assets/examples/electronic_fire_tb.png) | ![electronic ice tb](assets/examples/electronic_ice_tb.png) | ![electronic rainbow tb](assets/examples/electronic_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![electronic neon bt](assets/examples/electronic_neon_bt.png) | ![electronic sunset bt](assets/examples/electronic_sunset_bt.png) | ![electronic ocean bt](assets/examples/electronic_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![electronic fire bt](assets/examples/electronic_fire_bt.png) | ![electronic ice bt](assets/examples/electronic_ice_bt.png) | ![electronic rainbow bt](assets/examples/electronic_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![electronic neon diag](assets/examples/electronic_neon_diag.png) | ![electronic sunset diag](assets/examples/electronic_sunset_diag.png) | ![electronic ocean diag](assets/examples/electronic_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![electronic fire diag](assets/examples/electronic_fire_diag.png) | ![electronic ice diag](assets/examples/electronic_ice_diag.png) | ![electronic rainbow diag](assets/examples/electronic_rainbow_diag.png) |

</details>

<details>
<summary><strong>elite</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![elite neon lr](assets/examples/elite_neon_lr.png) | ![elite sunset lr](assets/examples/elite_sunset_lr.png) | ![elite ocean lr](assets/examples/elite_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![elite fire lr](assets/examples/elite_fire_lr.png) | ![elite ice lr](assets/examples/elite_ice_lr.png) | ![elite rainbow lr](assets/examples/elite_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![elite neon tb](assets/examples/elite_neon_tb.png) | ![elite sunset tb](assets/examples/elite_sunset_tb.png) | ![elite ocean tb](assets/examples/elite_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![elite fire tb](assets/examples/elite_fire_tb.png) | ![elite ice tb](assets/examples/elite_ice_tb.png) | ![elite rainbow tb](assets/examples/elite_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![elite neon bt](assets/examples/elite_neon_bt.png) | ![elite sunset bt](assets/examples/elite_sunset_bt.png) | ![elite ocean bt](assets/examples/elite_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![elite fire bt](assets/examples/elite_fire_bt.png) | ![elite ice bt](assets/examples/elite_ice_bt.png) | ![elite rainbow bt](assets/examples/elite_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![elite neon diag](assets/examples/elite_neon_diag.png) | ![elite sunset diag](assets/examples/elite_sunset_diag.png) | ![elite ocean diag](assets/examples/elite_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![elite fire diag](assets/examples/elite_fire_diag.png) | ![elite ice diag](assets/examples/elite_ice_diag.png) | ![elite rainbow diag](assets/examples/elite_rainbow_diag.png) |

</details>

<details>
<summary><strong>future</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![future neon lr](assets/examples/future_neon_lr.png) | ![future sunset lr](assets/examples/future_sunset_lr.png) | ![future ocean lr](assets/examples/future_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![future fire lr](assets/examples/future_fire_lr.png) | ![future ice lr](assets/examples/future_ice_lr.png) | ![future rainbow lr](assets/examples/future_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![future neon tb](assets/examples/future_neon_tb.png) | ![future sunset tb](assets/examples/future_sunset_tb.png) | ![future ocean tb](assets/examples/future_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![future fire tb](assets/examples/future_fire_tb.png) | ![future ice tb](assets/examples/future_ice_tb.png) | ![future rainbow tb](assets/examples/future_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![future neon bt](assets/examples/future_neon_bt.png) | ![future sunset bt](assets/examples/future_sunset_bt.png) | ![future ocean bt](assets/examples/future_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![future fire bt](assets/examples/future_fire_bt.png) | ![future ice bt](assets/examples/future_ice_bt.png) | ![future rainbow bt](assets/examples/future_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![future neon diag](assets/examples/future_neon_diag.png) | ![future sunset diag](assets/examples/future_sunset_diag.png) | ![future ocean diag](assets/examples/future_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![future fire diag](assets/examples/future_fire_diag.png) | ![future ice diag](assets/examples/future_ice_diag.png) | ![future rainbow diag](assets/examples/future_rainbow_diag.png) |

</details>

<details>
<summary><strong>mono12</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono12 neon lr](assets/examples/mono12_neon_lr.png) | ![mono12 sunset lr](assets/examples/mono12_sunset_lr.png) | ![mono12 ocean lr](assets/examples/mono12_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono12 fire lr](assets/examples/mono12_fire_lr.png) | ![mono12 ice lr](assets/examples/mono12_ice_lr.png) | ![mono12 rainbow lr](assets/examples/mono12_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono12 neon tb](assets/examples/mono12_neon_tb.png) | ![mono12 sunset tb](assets/examples/mono12_sunset_tb.png) | ![mono12 ocean tb](assets/examples/mono12_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono12 fire tb](assets/examples/mono12_fire_tb.png) | ![mono12 ice tb](assets/examples/mono12_ice_tb.png) | ![mono12 rainbow tb](assets/examples/mono12_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono12 neon bt](assets/examples/mono12_neon_bt.png) | ![mono12 sunset bt](assets/examples/mono12_sunset_bt.png) | ![mono12 ocean bt](assets/examples/mono12_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono12 fire bt](assets/examples/mono12_fire_bt.png) | ![mono12 ice bt](assets/examples/mono12_ice_bt.png) | ![mono12 rainbow bt](assets/examples/mono12_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono12 neon diag](assets/examples/mono12_neon_diag.png) | ![mono12 sunset diag](assets/examples/mono12_sunset_diag.png) | ![mono12 ocean diag](assets/examples/mono12_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono12 fire diag](assets/examples/mono12_fire_diag.png) | ![mono12 ice diag](assets/examples/mono12_ice_diag.png) | ![mono12 rainbow diag](assets/examples/mono12_rainbow_diag.png) |

</details>

<details>
<summary><strong>mono9</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono9 neon lr](assets/examples/mono9_neon_lr.png) | ![mono9 sunset lr](assets/examples/mono9_sunset_lr.png) | ![mono9 ocean lr](assets/examples/mono9_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono9 fire lr](assets/examples/mono9_fire_lr.png) | ![mono9 ice lr](assets/examples/mono9_ice_lr.png) | ![mono9 rainbow lr](assets/examples/mono9_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono9 neon tb](assets/examples/mono9_neon_tb.png) | ![mono9 sunset tb](assets/examples/mono9_sunset_tb.png) | ![mono9 ocean tb](assets/examples/mono9_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono9 fire tb](assets/examples/mono9_fire_tb.png) | ![mono9 ice tb](assets/examples/mono9_ice_tb.png) | ![mono9 rainbow tb](assets/examples/mono9_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono9 neon bt](assets/examples/mono9_neon_bt.png) | ![mono9 sunset bt](assets/examples/mono9_sunset_bt.png) | ![mono9 ocean bt](assets/examples/mono9_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono9 fire bt](assets/examples/mono9_fire_bt.png) | ![mono9 ice bt](assets/examples/mono9_ice_bt.png) | ![mono9 rainbow bt](assets/examples/mono9_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![mono9 neon diag](assets/examples/mono9_neon_diag.png) | ![mono9 sunset diag](assets/examples/mono9_sunset_diag.png) | ![mono9 ocean diag](assets/examples/mono9_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono9 fire diag](assets/examples/mono9_fire_diag.png) | ![mono9 ice diag](assets/examples/mono9_ice_diag.png) | ![mono9 rainbow diag](assets/examples/mono9_rainbow_diag.png) |

</details>

<details>
<summary><strong>pagga</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![pagga neon lr](assets/examples/pagga_neon_lr.png) | ![pagga sunset lr](assets/examples/pagga_sunset_lr.png) | ![pagga ocean lr](assets/examples/pagga_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![pagga fire lr](assets/examples/pagga_fire_lr.png) | ![pagga ice lr](assets/examples/pagga_ice_lr.png) | ![pagga rainbow lr](assets/examples/pagga_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![pagga neon tb](assets/examples/pagga_neon_tb.png) | ![pagga sunset tb](assets/examples/pagga_sunset_tb.png) | ![pagga ocean tb](assets/examples/pagga_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![pagga fire tb](assets/examples/pagga_fire_tb.png) | ![pagga ice tb](assets/examples/pagga_ice_tb.png) | ![pagga rainbow tb](assets/examples/pagga_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![pagga neon bt](assets/examples/pagga_neon_bt.png) | ![pagga sunset bt](assets/examples/pagga_sunset_bt.png) | ![pagga ocean bt](assets/examples/pagga_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![pagga fire bt](assets/examples/pagga_fire_bt.png) | ![pagga ice bt](assets/examples/pagga_ice_bt.png) | ![pagga rainbow bt](assets/examples/pagga_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![pagga neon diag](assets/examples/pagga_neon_diag.png) | ![pagga sunset diag](assets/examples/pagga_sunset_diag.png) | ![pagga ocean diag](assets/examples/pagga_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![pagga fire diag](assets/examples/pagga_fire_diag.png) | ![pagga ice diag](assets/examples/pagga_ice_diag.png) | ![pagga rainbow diag](assets/examples/pagga_rainbow_diag.png) |

</details>

<details>
<summary><strong>smmono12</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono12 neon lr](assets/examples/smmono12_neon_lr.png) | ![smmono12 sunset lr](assets/examples/smmono12_sunset_lr.png) | ![smmono12 ocean lr](assets/examples/smmono12_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono12 fire lr](assets/examples/smmono12_fire_lr.png) | ![smmono12 ice lr](assets/examples/smmono12_ice_lr.png) | ![smmono12 rainbow lr](assets/examples/smmono12_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono12 neon tb](assets/examples/smmono12_neon_tb.png) | ![smmono12 sunset tb](assets/examples/smmono12_sunset_tb.png) | ![smmono12 ocean tb](assets/examples/smmono12_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono12 fire tb](assets/examples/smmono12_fire_tb.png) | ![smmono12 ice tb](assets/examples/smmono12_ice_tb.png) | ![smmono12 rainbow tb](assets/examples/smmono12_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono12 neon bt](assets/examples/smmono12_neon_bt.png) | ![smmono12 sunset bt](assets/examples/smmono12_sunset_bt.png) | ![smmono12 ocean bt](assets/examples/smmono12_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono12 fire bt](assets/examples/smmono12_fire_bt.png) | ![smmono12 ice bt](assets/examples/smmono12_ice_bt.png) | ![smmono12 rainbow bt](assets/examples/smmono12_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono12 neon diag](assets/examples/smmono12_neon_diag.png) | ![smmono12 sunset diag](assets/examples/smmono12_sunset_diag.png) | ![smmono12 ocean diag](assets/examples/smmono12_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono12 fire diag](assets/examples/smmono12_fire_diag.png) | ![smmono12 ice diag](assets/examples/smmono12_ice_diag.png) | ![smmono12 rainbow diag](assets/examples/smmono12_rainbow_diag.png) |

</details>

<details>
<summary><strong>smmono9</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono9 neon lr](assets/examples/smmono9_neon_lr.png) | ![smmono9 sunset lr](assets/examples/smmono9_sunset_lr.png) | ![smmono9 ocean lr](assets/examples/smmono9_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono9 fire lr](assets/examples/smmono9_fire_lr.png) | ![smmono9 ice lr](assets/examples/smmono9_ice_lr.png) | ![smmono9 rainbow lr](assets/examples/smmono9_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono9 neon tb](assets/examples/smmono9_neon_tb.png) | ![smmono9 sunset tb](assets/examples/smmono9_sunset_tb.png) | ![smmono9 ocean tb](assets/examples/smmono9_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono9 fire tb](assets/examples/smmono9_fire_tb.png) | ![smmono9 ice tb](assets/examples/smmono9_ice_tb.png) | ![smmono9 rainbow tb](assets/examples/smmono9_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono9 neon bt](assets/examples/smmono9_neon_bt.png) | ![smmono9 sunset bt](assets/examples/smmono9_sunset_bt.png) | ![smmono9 ocean bt](assets/examples/smmono9_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono9 fire bt](assets/examples/smmono9_fire_bt.png) | ![smmono9 ice bt](assets/examples/smmono9_ice_bt.png) | ![smmono9 rainbow bt](assets/examples/smmono9_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono9 neon diag](assets/examples/smmono9_neon_diag.png) | ![smmono9 sunset diag](assets/examples/smmono9_sunset_diag.png) | ![smmono9 ocean diag](assets/examples/smmono9_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono9 fire diag](assets/examples/smmono9_fire_diag.png) | ![smmono9 ice diag](assets/examples/smmono9_ice_diag.png) | ![smmono9 rainbow diag](assets/examples/smmono9_rainbow_diag.png) |

</details>

<details>
<summary><strong>thick</strong></summary>

**→ left to right**

| neon | sunset | ocean |
|------|--------|-------|
| ![thick neon lr](assets/examples/thick_neon_lr.png) | ![thick sunset lr](assets/examples/thick_sunset_lr.png) | ![thick ocean lr](assets/examples/thick_ocean_lr.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![thick fire lr](assets/examples/thick_fire_lr.png) | ![thick ice lr](assets/examples/thick_ice_lr.png) | ![thick rainbow lr](assets/examples/thick_rainbow_lr.png) |

**↓ top to bottom**

| neon | sunset | ocean |
|------|--------|-------|
| ![thick neon tb](assets/examples/thick_neon_tb.png) | ![thick sunset tb](assets/examples/thick_sunset_tb.png) | ![thick ocean tb](assets/examples/thick_ocean_tb.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![thick fire tb](assets/examples/thick_fire_tb.png) | ![thick ice tb](assets/examples/thick_ice_tb.png) | ![thick rainbow tb](assets/examples/thick_rainbow_tb.png) |

**↑ bottom to top**

| neon | sunset | ocean |
|------|--------|-------|
| ![thick neon bt](assets/examples/thick_neon_bt.png) | ![thick sunset bt](assets/examples/thick_sunset_bt.png) | ![thick ocean bt](assets/examples/thick_ocean_bt.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![thick fire bt](assets/examples/thick_fire_bt.png) | ![thick ice bt](assets/examples/thick_ice_bt.png) | ![thick rainbow bt](assets/examples/thick_rainbow_bt.png) |

**⤢ diagonal**

| neon | sunset | ocean |
|------|--------|-------|
| ![thick neon diag](assets/examples/thick_neon_diag.png) | ![thick sunset diag](assets/examples/thick_sunset_diag.png) | ![thick ocean diag](assets/examples/thick_ocean_diag.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![thick fire diag](assets/examples/thick_fire_diag.png) | ![thick ice diag](assets/examples/thick_ice_diag.png) | ![thick rainbow diag](assets/examples/thick_rainbow_diag.png) |

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
