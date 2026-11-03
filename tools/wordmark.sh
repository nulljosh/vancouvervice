#!/bin/sh
# Renders the Vancouver Vice wordmark in Seawall: T_Logo (1024x512, transparent, for the title screen) and the app icon
# (1024, wordmark on night with rounded corners). Run: sh tools/wordmark.sh  (needs ImageMagick)
set -eu
R=$(cd "$(dirname "$0")/.." && pwd); F="$R/brand/Seawall.ttf"; T=${TMPDIR:-/tmp}/vvwm; mkdir -p "$T"
PAPER="#e4e0d6"; RED="#e0362c"; NIGHT="#15171c"
word() { magick -background none -fill "$2" -font "$F" -pointsize "$3" label:"$1" -trim +repage "$T/$4.png"; }
stack() {  # $1 out, $2 width: VANCOUVER over VICE, both the same width
  word VANCOUVER "$PAPER" 300 a; word VICE "$RED" 600 b
  magick "$T/a.png" -resize "$2"x "$T/a2.png"; magick "$T/b.png" -resize "$2"x "$T/b2.png"
  magick -background none "$T/a2.png" \( -size 1x$(( $2 / 30 )) xc:none \) "$T/b2.png" -gravity west -append "$1"
}
stack "$T/logo.png" 900
magick "$T/logo.png" -resize 1000x490 -background none -gravity southwest -extent 1024x512 "$R/brand/logo.png"
stack "$T/icon.png" 760
magick -size 1024x1024 xc:none -fill "$NIGHT" -draw "roundrectangle 0,0,1023,1023,200,200" "$T/icon.png" -gravity center -composite "$R/brand/app-icon.png"
echo wrote brand/logo.png brand/app-icon.png
