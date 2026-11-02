# Vancouver Vice brand

One city at night in the rain, one hot red. Loud display type, quiet body text.

## Type
- **Display: Anton**, uppercase, slanted 7 degrees (`--vv-slant`), tight line height. Wordmark, section titles, character names. Self-hosted at `site/fonts/anton.woff2`, SIL Open Font License (`brand/Anton-OFL.txt`).
- **Text: the system font** (SF on Apple). Everything you read in sentences, every button, every HUD line.
- Never set body copy in the display face. Never put type in the icon.

## Colour
| Token | Hex | Use |
|---|---|---|
| `--vv-night` | #0c0d10 | page and menu background |
| `--vv-asphalt` | #15171c | cards, panels |
| `--vv-curb` | #25272d | rules, borders |
| `--vv-fog` | #a3a6ad | secondary text |
| `--vv-paper` | #f3f1ec | primary text |
| `--vv-red` | #e0362c | the one action colour: CTAs, VICE in the wordmark, wanted stars |
| `--vv-gastown` | #e8b21a | Joshua |
| `--vv-kits` | #5b8cff | Ben |
| `--vv-victoria` | #c9ccd3 | Alexandre |
| `--vv-seawall` | #2e9e8f | water, maps |

## Wordmark
`VANCOUVER` in paper over `VICE` in red, both in the display face, stacked, slanted. On photos, a 48 percent black scrim behind it, never a gradient.

## Layout
8 point grid (`--vv-1` to `--vv-12`), radii 8 / 16 / 24, controls 48 high and pill shaped. Full-bleed art, then content in a 1200 wide column.

## Files
`site/css/brand.css` holds every token; the landing, the title screen and the pause menu load it. The game HUD stays on the system font for legibility.
