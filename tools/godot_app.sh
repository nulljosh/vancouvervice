#!/bin/sh
# Builds godot/export/Vancouver Vice.app from the installed Godot editor (no export templates needed):
# the editor binary auto-runs a .pck named after itself, so the app is Godot.app renamed, re-iconed, plus the game pack.
set -e; cd "$(dirname "$0")/../godot"
G=${GODOT:-$HOME/Applications/Godot.app}; A="export/Vancouver Vice.app"
rm -rf "$A"; mkdir -p export data; cp ../site/data/downtown.json data/; cp -R "$G" "$A"
"$G/Contents/MacOS/Godot" --headless --path . --export-pack macOS "$A/Contents/Resources/Godot.pck" >/dev/null 2>&1
P="$A/Contents/Info.plist"
for k in CFBundleName CFBundleDisplayName; do plutil -replace $k -string "Vancouver Vice" "$P"; done
plutil -replace CFBundleIdentifier -string com.jaybulb.vancouvervice "$P"
plutil -replace CFBundleIconFile -string vv.icns "$P"; cp icon.icns "$A/Contents/Resources/vv.icns"
codesign --force --deep -s - "$A" 2>/dev/null || true
ls -la "$A/Contents/Resources/Godot.pck" && echo "built: godot/$A"
