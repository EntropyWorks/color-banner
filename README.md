
# color-banner
![color-banner](assets/banner.png)

> Built on the shoulders of [FIGlet](http://www.figlet.org/) (Glenn Chappell & Ian Chai, 1991),
> [pyfiglet](https://github.com/pwaller/pyfiglet) (Christopher Jones, Stefano Rivera, Peter Waller), and
> [Calligraphy](https://codeberg.org/GeopJr/Calligraphy) (GeopJr / Gregor "gregorni" Niehl).
> Licensed under Apache 2.0.

Render text as colorful 24-bit figlet ASCII banners in the terminal.
Designed for CICD pipelines, shell startup screens, and BBS-style splash screens.

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

<details>
<summary><strong>ansi_regular</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_regular neon](assets/examples/ansi_regular_neon.png) | ![ansi_regular sunset](assets/examples/ansi_regular_sunset.png) | ![ansi_regular ocean](assets/examples/ansi_regular_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_regular fire](assets/examples/ansi_regular_fire.png) | ![ansi_regular ice](assets/examples/ansi_regular_ice.png) | ![ansi_regular rainbow](assets/examples/ansi_regular_rainbow.png) |

</details>

<details>
<summary><strong>ansi_shadow</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![ansi_shadow neon](assets/examples/ansi_shadow_neon.png) | ![ansi_shadow sunset](assets/examples/ansi_shadow_sunset.png) | ![ansi_shadow ocean](assets/examples/ansi_shadow_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![ansi_shadow fire](assets/examples/ansi_shadow_fire.png) | ![ansi_shadow ice](assets/examples/ansi_shadow_ice.png) | ![ansi_shadow rainbow](assets/examples/ansi_shadow_rainbow.png) |

</details>

<details>
<summary><strong>bigmono12</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono12 neon](assets/examples/bigmono12_neon.png) | ![bigmono12 sunset](assets/examples/bigmono12_sunset.png) | ![bigmono12 ocean](assets/examples/bigmono12_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono12 fire](assets/examples/bigmono12_fire.png) | ![bigmono12 ice](assets/examples/bigmono12_ice.png) | ![bigmono12 rainbow](assets/examples/bigmono12_rainbow.png) |

</details>

<details>
<summary><strong>bigmono9</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![bigmono9 neon](assets/examples/bigmono9_neon.png) | ![bigmono9 sunset](assets/examples/bigmono9_sunset.png) | ![bigmono9 ocean](assets/examples/bigmono9_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bigmono9 fire](assets/examples/bigmono9_fire.png) | ![bigmono9 ice](assets/examples/bigmono9_ice.png) | ![bigmono9 rainbow](assets/examples/bigmono9_rainbow.png) |

</details>

<details>
<summary><strong>bloody</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![bloody neon](assets/examples/bloody_neon.png) | ![bloody sunset](assets/examples/bloody_sunset.png) | ![bloody ocean](assets/examples/bloody_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![bloody fire](assets/examples/bloody_fire.png) | ![bloody ice](assets/examples/bloody_ice.png) | ![bloody rainbow](assets/examples/bloody_rainbow.png) |

</details>

<details>
<summary><strong>delta_corps_priest_1</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![delta_corps_priest_1 neon](assets/examples/delta_corps_priest_1_neon.png) | ![delta_corps_priest_1 sunset](assets/examples/delta_corps_priest_1_sunset.png) | ![delta_corps_priest_1 ocean](assets/examples/delta_corps_priest_1_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![delta_corps_priest_1 fire](assets/examples/delta_corps_priest_1_fire.png) | ![delta_corps_priest_1 ice](assets/examples/delta_corps_priest_1_ice.png) | ![delta_corps_priest_1 rainbow](assets/examples/delta_corps_priest_1_rainbow.png) |

</details>

<details>
<summary><strong>dos_rebel</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![dos_rebel neon](assets/examples/dos_rebel_neon.png) | ![dos_rebel sunset](assets/examples/dos_rebel_sunset.png) | ![dos_rebel ocean](assets/examples/dos_rebel_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![dos_rebel fire](assets/examples/dos_rebel_fire.png) | ![dos_rebel ice](assets/examples/dos_rebel_ice.png) | ![dos_rebel rainbow](assets/examples/dos_rebel_rainbow.png) |

</details>

<details>
<summary><strong>double_blocky</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![double_blocky neon](assets/examples/double_blocky_neon.png) | ![double_blocky sunset](assets/examples/double_blocky_sunset.png) | ![double_blocky ocean](assets/examples/double_blocky_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![double_blocky fire](assets/examples/double_blocky_fire.png) | ![double_blocky ice](assets/examples/double_blocky_ice.png) | ![double_blocky rainbow](assets/examples/double_blocky_rainbow.png) |

</details>

<details>
<summary><strong>electronic</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![electronic neon](assets/examples/electronic_neon.png) | ![electronic sunset](assets/examples/electronic_sunset.png) | ![electronic ocean](assets/examples/electronic_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![electronic fire](assets/examples/electronic_fire.png) | ![electronic ice](assets/examples/electronic_ice.png) | ![electronic rainbow](assets/examples/electronic_rainbow.png) |

</details>

<details>
<summary><strong>elite</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![elite neon](assets/examples/elite_neon.png) | ![elite sunset](assets/examples/elite_sunset.png) | ![elite ocean](assets/examples/elite_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![elite fire](assets/examples/elite_fire.png) | ![elite ice](assets/examples/elite_ice.png) | ![elite rainbow](assets/examples/elite_rainbow.png) |

</details>

<details>
<summary><strong>future</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![future neon](assets/examples/future_neon.png) | ![future sunset](assets/examples/future_sunset.png) | ![future ocean](assets/examples/future_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![future fire](assets/examples/future_fire.png) | ![future ice](assets/examples/future_ice.png) | ![future rainbow](assets/examples/future_rainbow.png) |

</details>

<details>
<summary><strong>mono12</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![mono12 neon](assets/examples/mono12_neon.png) | ![mono12 sunset](assets/examples/mono12_sunset.png) | ![mono12 ocean](assets/examples/mono12_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono12 fire](assets/examples/mono12_fire.png) | ![mono12 ice](assets/examples/mono12_ice.png) | ![mono12 rainbow](assets/examples/mono12_rainbow.png) |

</details>

<details>
<summary><strong>mono9</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![mono9 neon](assets/examples/mono9_neon.png) | ![mono9 sunset](assets/examples/mono9_sunset.png) | ![mono9 ocean](assets/examples/mono9_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![mono9 fire](assets/examples/mono9_fire.png) | ![mono9 ice](assets/examples/mono9_ice.png) | ![mono9 rainbow](assets/examples/mono9_rainbow.png) |

</details>

<details>
<summary><strong>pagga</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![pagga neon](assets/examples/pagga_neon.png) | ![pagga sunset](assets/examples/pagga_sunset.png) | ![pagga ocean](assets/examples/pagga_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![pagga fire](assets/examples/pagga_fire.png) | ![pagga ice](assets/examples/pagga_ice.png) | ![pagga rainbow](assets/examples/pagga_rainbow.png) |

</details>

<details>
<summary><strong>smmono12</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono12 neon](assets/examples/smmono12_neon.png) | ![smmono12 sunset](assets/examples/smmono12_sunset.png) | ![smmono12 ocean](assets/examples/smmono12_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono12 fire](assets/examples/smmono12_fire.png) | ![smmono12 ice](assets/examples/smmono12_ice.png) | ![smmono12 rainbow](assets/examples/smmono12_rainbow.png) |

</details>

<details>
<summary><strong>smmono9</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![smmono9 neon](assets/examples/smmono9_neon.png) | ![smmono9 sunset](assets/examples/smmono9_sunset.png) | ![smmono9 ocean](assets/examples/smmono9_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![smmono9 fire](assets/examples/smmono9_fire.png) | ![smmono9 ice](assets/examples/smmono9_ice.png) | ![smmono9 rainbow](assets/examples/smmono9_rainbow.png) |

</details>

<details>
<summary><strong>thick</strong></summary>

| neon | sunset | ocean |
|------|--------|-------|
| ![thick neon](assets/examples/thick_neon.png) | ![thick sunset](assets/examples/thick_sunset.png) | ![thick ocean](assets/examples/thick_ocean.png) |

| fire | ice | rainbow |
|------|-----|---------|
| ![thick fire](assets/examples/thick_fire.png) | ![thick ice](assets/examples/thick_ice.png) | ![thick rainbow](assets/examples/thick_rainbow.png) |

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
