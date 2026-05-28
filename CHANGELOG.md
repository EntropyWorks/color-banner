# Changelog

## [0.2.0](https://github.com/EntropyWorks/color-banner/compare/v0.1.0...v0.2.0) (2026-05-28)


### Features

* --all readable and --save-all --readable filters ([4873797](https://github.com/EntropyWorks/color-banner/commit/487379731d0046cff1852eacbe3f992f649d42e2))
* --list-fonts readable filter ([f0e2509](https://github.com/EntropyWorks/color-banner/commit/f0e25095b79325e1ad8fe2b52b71747015db865f))
* --width N controls line-wrap width (0 = never wrap) ([e44edec](https://github.com/EntropyWorks/color-banner/commit/e44edec16d0db93afd25113601352753973947fa))
* add cli.py — wire all modules, complete color-banner command ([51e9023](https://github.com/EntropyWorks/color-banner/commit/51e902331ab09387d705043c9d7f2cc80d413426))
* add color.py with parse_hex and PALETTES ([ce40e42](https://github.com/EntropyWorks/color-banner/commit/ce40e4215fceddee18eae4a65130fce3839100bf))
* add gradient math to color.py ([c40dfdb](https://github.com/EntropyWorks/color-banner/commit/c40dfdbbd2cbb19b90761895c93a12c8a7c781a8))
* add output.py — stdout, --save, --export ([adc8239](https://github.com/EntropyWorks/color-banner/commit/adc823979e947e5f138d0f99a5dba924de0a94a0))
* add painter.py — apply gradient colors to ASCII rows ([c240d96](https://github.com/EntropyWorks/color-banner/commit/c240d96c208328d435049da9019b9a4378dddf59))
* add renderer.py wrapping pyfiglet ([4445eb4](https://github.com/EntropyWorks/color-banner/commit/4445eb4a197c70d21682813a71e1bec9e17a6bf2))
* auto-create parent directories in write_ansi_file ([dd7320e](https://github.com/EntropyWorks/color-banner/commit/dd7320e9e289b5672e4e30c03c0681e24652f9d3))
* font numbering, --all, --save-all, auto-mkdir ([0809425](https://github.com/EntropyWorks/color-banner/commit/08094258c308f72cea4c670815399080c8ec0d92))
* test readability across mixed/upper/lower case phrases ([c3e9131](https://github.com/EntropyWorks/color-banner/commit/c3e913186058f45cb442530dc91b16bdcc76d218))


### Bug Fixes

* address code review findings — gradient max validation, TTY test, exit codes, attribution cleanup ([487a5dd](https://github.com/EntropyWorks/color-banner/commit/487a5dd833e93ba7206b77f2c89ddf722c636d99))
* correct generated .sh file security issues ([76764f8](https://github.com/EntropyWorks/color-banner/commit/76764f8f48fbbe3362d859962e5f807408bd7525))
* move release-please-config.json to repo root (required default location) ([c00155f](https://github.com/EntropyWorks/color-banner/commit/c00155f46885c84edc21ebfb0c341b135bc2938a))


### Documentation

* add all 4 gradient directions to gallery (408 examples total) ([a0a1474](https://github.com/EntropyWorks/color-banner/commit/a0a14740bbcfaeb6cc62aaccad0ccd4d94d4f922))
* add banner image (thick font, neon palette) ([abe3621](https://github.com/EntropyWorks/color-banner/commit/abe362137c27093afad2a338449bc685ab08acb5))
* add CI/CD design spec ([095e81e](https://github.com/EntropyWorks/color-banner/commit/095e81efa436857b7cc609663e300883db37adff))
* add CI/CD implementation plan ([f7f7a59](https://github.com/EntropyWorks/color-banner/commit/f7f7a59c4afb5d031c0fc49246f855456552b923))
* add Claude Code attribution to CREDITS.md ([0221f09](https://github.com/EntropyWorks/color-banner/commit/0221f097c62aee4eace16d38f7fbb23713601f0b))
* add color-banner design spec ([69a35d9](https://github.com/EntropyWorks/color-banner/commit/69a35d92e89615a04ae5ec6e0bd73d8b2beefa91))
* add color-banner implementation plan ([8274d64](https://github.com/EntropyWorks/color-banner/commit/8274d64922f8a48aa99840a9926f172fd2d007f0))
* add font/palette example images (17 fonts × 6 palettes) ([d40f362](https://github.com/EntropyWorks/color-banner/commit/d40f36297ffc3e1b0c5a449cab33b82308afc728))
* add gallery section with all 17 fonts × 6 palettes ([4cdda40](https://github.com/EntropyWorks/color-banner/commit/4cdda40a6d950bbbb422a1074a604755a3c45442))
* add local/editable install instructions to README ([1f01aec](https://github.com/EntropyWorks/color-banner/commit/1f01aec29b6539cbf010ab3708e19401dc02ba46))
* add note to gallery about font compatibility and readability filter ([fe691be](https://github.com/EntropyWorks/color-banner/commit/fe691beeb8ef33c7272fbf8eea5e602a3993c27c))
* add Requirements section to README ([2e3d4dc](https://github.com/EntropyWorks/color-banner/commit/2e3d4dc23aa1c071bd95c80cc49eafbcd0a2636b))
* add table of contents with gallery link ([9850bb2](https://github.com/EntropyWorks/color-banner/commit/9850bb2c2c0daea8ad1467ca69e483bc9e4ae19b))
* center banner image and move it under the title ([44995eb](https://github.com/EntropyWorks/color-banner/commit/44995eb2789c27f2b5c79e3234498a8047cedbdf))
* complete README and update .gitignore ([90476ab](https://github.com/EntropyWorks/color-banner/commit/90476ab1ff352d7f6781d483c286e8d7e18a30ee))
* credit FIGlet and pyfiglet in README ([af02475](https://github.com/EntropyWorks/color-banner/commit/af024755b0423b21799d5f73de52f3c9529521a5))
* expand CREDITS.md with FIGlet and pyfiglet attribution ([fbe3fe7](https://github.com/EntropyWorks/color-banner/commit/fbe3fe7510afecf58caac48267d9148c28c424b1))
* fix blockquote rendering by adding blank line after &lt;/p&gt; ([8c3864a](https://github.com/EntropyWorks/color-banner/commit/8c3864abbef62a2bda304859d5dab9880df5fa4d))
* fix release-please-config.json path in design spec ([57f22ce](https://github.com/EntropyWorks/color-banner/commit/57f22ceeed57db2e5ec842ec367d71dd4330c0e5))
* mention NOTICE file in Credits section of README ([c5e47b3](https://github.com/EntropyWorks/color-banner/commit/c5e47b30cccacae4ac493ff2aaa0c5ff20d4e99b))
* switch README banner back to assets/banner.png ([307a377](https://github.com/EntropyWorks/color-banner/commit/307a377ec0c298274b1f607b43e05a98505b53f0))
* switch README banner to future_neon ([f753ef0](https://github.com/EntropyWorks/color-banner/commit/f753ef07b1d9281458a8cbc67ac7fdbd37f89656))
* update banner image ([6d9ddd4](https://github.com/EntropyWorks/color-banner/commit/6d9ddd44f36e3ae93544d53f35b3f386bcea53d1))
* update README with font numbering, --all, --save-all, --width, --list-fonts readable ([9a9852a](https://github.com/EntropyWorks/color-banner/commit/9a9852a6e405c2a62b2d5dfbe55aa22ed5c0a965))
