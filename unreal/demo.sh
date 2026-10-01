#!/bin/sh
# Mission one on autoplay, recorded. Starts Play, lets the city stream in, runs the walk test (out of the Apple Store)
# then the drive test (jack the car, floor it), screen-records the editor window the whole time, stops Play, writes a GIF.
#   sh unreal/demo.sh [seconds]      default 75
HERE=$(cd "$(dirname "$0")" && pwd); OUT=${OUT:-/tmp/vv_demo}; SECS=${1:-75}; mkdir -p "$OUT"
open -a /Volumes/LaCie/UE_5.8/Engine/Binaries/Mac/UnrealEditor.app
python3 -c "import sys; sys.path.insert(0,'$HERE'); import qa; qa.mcp('EditorToolset.EditorAppToolset','StartPIE',{'options':{'bSimulate':False,'playMode':'PlayMode_InViewPort','warmupSeconds':5}})"
WID=$(swift "$HERE/wid.swift" 2>/dev/null | awk '/Unreal Editor/{print $1}')
[ -n "$WID" ] && screencapture -x -v -V "$SECS" -l "$WID" "$OUT/demo.mov" &
REC=$!
sleep 25   # tiles
echo "walk: $(QA_TIMEOUT=60 python3 "$HERE/qa.py" "QA_RESULT='FAIL walk script crashed'
$(cat "$HERE/qa_walk.py")")"
for i in $(seq 1 15); do sleep 2; r=$(QA_TIMEOUT=20 python3 "$HERE/qa.py" 'print(QA_RESULT)'); case "$r" in RUNNING*) ;; *) break;; esac; done
echo "walk result: $r"
echo "drive: $(QA_TIMEOUT=60 python3 "$HERE/qa.py" "$(cat "$HERE/qa_drive.py")")"
for i in $(seq 1 12); do sleep 2; d=$(QA_TIMEOUT=20 python3 "$HERE/qa.py" 'print(QA_RESULT)'); case "$d" in RUNNING*) ;; *) break;; esac; done
echo "drive result: $d"
wait $REC
python3 -c "import sys; sys.path.insert(0,'$HERE'); import qa; qa.mcp('EditorToolset.EditorAppToolset','StopPIE',{})"
ffmpeg -y -loglevel error -i "$OUT/demo.mov" -vf "fps=10,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse=dither=bayer" "$OUT/demo.gif"
echo "gif: $OUT/demo.gif"
