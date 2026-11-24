#!/bin/sh
# Sourced by the unreal/*.sh scripts. One place that says where the engine and project live.
# The drive holds UE_5.8/ and Unreal/VancouverVice/. Set it once per machine:
#   export VV_DRIVE=/Volumes/<NVMe name>     (or write the path into unreal/.drive, gitignored)
[ -z "${VV_DRIVE:-}" ] && [ -f "$(dirname "$0")/.drive" ] && VV_DRIVE=$(cat "$(dirname "$0")/.drive")
if [ -z "${VV_DRIVE:-}" ] || [ ! -d "$VV_DRIVE/UE_5.8" ]; then
  echo "Unreal drive not found. Set VV_DRIVE (or unreal/.drive) to the drive holding UE_5.8/ and Unreal/. Got: '${VV_DRIVE:-unset}'" >&2
  exit 1
fi
UE="$VV_DRIVE/UE_5.8"
UE_APP="$UE/Engine/Binaries/Mac/UnrealEditor.app"
VV="$VV_DRIVE/Unreal"
VV_PROJECT="$VV/VancouverVice/VancouverVice.uproject"
export VV_DRIVE UE UE_APP VV VV_PROJECT
