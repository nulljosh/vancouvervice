#!/bin/sh
# Packages the vertical slice as a Development Mac .app via RunUAT BuildCookRun.
# Run with the editor CLOSED (see roadmap.md milestone: "Build in the editor without Play; QA
# on the packaged app at each milestone"). Cook/build/pak/archive all want the RAM the editor
# is holding, and BuildCookRun launches its own headless cook anyway.
#
#   sh unreal/package.sh
#
# Output: /Volumes/LaCie/Unreal/Builds/<YYYY-MM-DD>/, with the .app inside Mac/.
# Log: /Volumes/LaCie/Unreal/Builds/<YYYY-MM-DD>/package.log (also unreal/package.log, a symlink
# to the latest run, so `tail -f unreal/package.log` works from a fresh session).

set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
ENGINE=/Volumes/LaCie/UE_5.8
RUNUAT="$ENGINE/Engine/Build/BatchFiles/RunUAT.sh"
PROJECT=/Volumes/LaCie/Unreal/VancouverVice/VancouverVice.uproject
DATE=$(date +%Y-%m-%d)
ARCHDIR="/Volumes/LaCie/Unreal/Builds/$DATE"
LOG="$ARCHDIR/package.log"

# --- guards, same idea as doctor.sh's thresholds ---

if pgrep -x UnrealEditor >/dev/null; then
  echo "refusing to package: UnrealEditor is running. Close it first (the cook needs the RAM, and" >&2
  echo "a live editor holding the project can also corrupt the cook)." >&2
  exit 1
fi

free_pct() { memory_pressure 2>/dev/null | awk '/free percentage/ {gsub("%","",$5); print $5}'; }
swap_pct() { sysctl -n vm.swapusage | awk '{gsub("M","",$3); gsub("M","",$6); if ($3>0) printf "%d", $6*100/$3; else print 0}'; }
F=$(free_pct); S=$(swap_pct)
# ponytail: fixed thresholds, same call as doctor.sh's heal(); tune if the Mac gets more RAM.
# A cook is heavier and longer than an editor relaunch, so ask for more headroom (25% vs 15%).
if [ "${F:-0}" -lt 25 ] || [ "${S:-100}" -gt 80 ]; then
  echo "refusing to package: only ${F:-0}% RAM free, swap ${S:-0}% used. Close other apps first." >&2
  exit 1
fi

if [ ! -x "$RUNUAT" ]; then
  echo "RunUAT not found at $RUNUAT (checked the installed 5.8.2 engine on LaCie)" >&2
  exit 1
fi

if [ ! -f "$PROJECT" ]; then
  echo "project not found at $PROJECT" >&2
  exit 1
fi


mkdir -p "$ARCHDIR"
echo "packaging to $ARCHDIR"
echo "log: $LOG"

# BuildCookRun flags: Development client config for QA (roadmap wants Development, not Shipping,
# for this milestone), Mac platform, build+cook+stage+pak+archive so the archive directory ends
# up with a runnable, self-contained .app. -nop4 skips Perforce (this isn't a P4 depot). -utf8output
# keeps the log readable. -unattended avoids any interactive prompt blocking an unattended run.
# Redirect (not `| tee`) so $? below is RunUAT's real exit status, not sh(1)'s pipefail-less
# pipeline status; tail the log from another terminal to watch it live.
# Speed (Joshua 2026-11-02: "it's a game not rocket science"): -cookincremental re-cooks only changed packages (the old
# -iterate recooked all 2226 every time, 6 min), -ForceUncompressed skips 2 min of pak compression, and there is no
# archive copy: play the app straight from Binaries/Mac. Old note: -iterate re-cooks only changed packages (the shader and cook caches stay in Saved/ and DerivedDataCache/);
# FAST=1 also skips the C++ build and reuses the last binaries when nothing native changed. The first build of a
# machine is slow (shaders from scratch, off the LaCie); after that a rebuild takes minutes.
BUILD="-build"; [ "${FAST:-0}" = 1 ] && BUILD="-skipbuild"
# xcodebuild fails when UBT spawns it on this Mac (no message) but works from a shell, so the engine's UBT is patched to
# skip it under UBT_SKIP_XCODE_FINALIZE=1 (backup: /Volumes/LaCie/Unreal/AppleToolChain.cs.orig) and we run it below.
export UBT_SKIP_XCODE_FINALIZE=1
set +e
"$RUNUAT" BuildCookRun \
  -project="$PROJECT" \
  -platform=Mac \
  -clientconfig=Development \
  $BUILD -cook -cookincremental -stage -pak -ForceUncompressed \
  -nop4 -utf8output -unattended \
  > "$LOG" 2>&1
STATUS=$?
set -e

ln -sf "$LOG" "$HERE/package.log"

if [ "$STATUS" -ne 0 ]; then
  echo "package FAILED (status $STATUS), see $LOG (or unreal/package.log)" >&2
  tail -40 "$LOG" >&2
  exit "$STATUS"
fi

# Finalize. QUICK=1 (content-only change, the app already exists): copy the staged files straight into the app's
# Contents/UE and re-sign ad hoc, a few seconds instead of the Xcode Stage pass (about 2 min). Otherwise run Xcode,
# which also compiles Build/Mac/Resources/Assets.xcassets (the app icon).
APP=/Volumes/LaCie/Unreal/VancouverVice/Binaries/Mac/VancouverVice.app
STAGED=/Volumes/LaCie/Unreal/VancouverVice/Saved/StagedBuilds/Mac
if [ "${QUICK:-0}" = 1 ] && [ -d "$APP/Contents/UE" ]; then
  rsync -a --delete "$STAGED/Engine" "$STAGED/VancouverVice" "$APP/Contents/UE/" && cp "$STAGED/NOTICES.txt" "$STAGED/UECommandLine.txt" "$APP/Contents/UE/" \
    && codesign --force --deep -s - "$APP" >> "$LOG" 2>&1 || { echo "quick finalize FAILED, see $LOG" >&2; exit 1; }
  echo "packaged (quick): $APP"; exit 0
fi
(cd "$ENGINE/Engine/Source" && UBT_NO_POST_DEPLOY=true xcodebuild build \
  -workspace /Volumes/LaCie/Unreal/VancouverVice/Intermediate/ProjectFiles/VancouverVice_Mac_VancouverVice.xcworkspace \
  -scheme VancouverVice -configuration Development -destination generic/platform=macOS \
  CODE_SIGN_ALLOW_ENTITLEMENTS_MODIFICATION=YES -allowProvisioningUpdates UE_XCODE_BUILD_MODE=Stage \
  -hideShellScriptEnvironment >> "$LOG" 2>&1) || { echo "xcode finalize FAILED, see $LOG" >&2; exit 1; }
if [ -n "$APP" ]; then
  echo "packaged: $APP"
else
  echo "BuildCookRun reported success but no .app was found under $ARCHDIR, check $LOG" >&2
  exit 1
fi
