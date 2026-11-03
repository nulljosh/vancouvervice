#!/bin/sh
# Applies unreal/*.dsl and menu assets to the project with no editor window (UnrealEditor-Cmd, null renderer).
# VV_FIND="term,term" sh unreal/headless.sh only looks up node names. Then build: FAST=1 sh unreal/package.sh
E=/Volumes/LaCie/UE_5.8/Engine/Binaries/Mac/UnrealEditor-Cmd
P=/Volumes/LaCie/Unreal/VancouverVice/VancouverVice.uproject
LOG=/Volumes/LaCie/Unreal/scratch/headless.log
"$E" "$P" -run=pythonscript -script="$(cd "$(dirname "$0")" && pwd)/headless.py" -unattended -nullrhi -nosplash -nosound -stdout >"$LOG" 2>&1
echo "exit $?"
cat /Volumes/LaCie/Unreal/scratch/headless.out; grep -E "Traceback|Error:" "$LOG" | grep -v LogInit | head -20
