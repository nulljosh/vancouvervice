#!/bin/sh
# Applies unreal/*.dsl and menu assets to the project with no editor window (UnrealEditor-Cmd, null renderer).
# VV_FIND="term,term" sh unreal/headless.sh only looks up node names. Then build: FAST=1 sh unreal/package.sh
. "$(cd "$(dirname "$0")" && pwd)/drive.sh"
E="$UE/Engine/Binaries/Mac/UnrealEditor-Cmd"
P="$VV_PROJECT"; mkdir -p "$VV/scratch"
LOG="$VV/scratch/headless.log"
"$E" "$P" -run=pythonscript -script="$(cd "$(dirname "$0")" && pwd)/headless.py" -unattended -nullrhi -nosplash -nosound -stdout >"$LOG" 2>&1
echo "exit $?"
cat "$VV/scratch/headless.out"; grep -E "Traceback|Error:" "$LOG" | grep -v LogInit | head -20
