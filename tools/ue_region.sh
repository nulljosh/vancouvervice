#!/bin/sh
# Builds every Lower Mainland town plus the big-road corridor between them as Unreal city chunks, on one world
# whose origin is downtown. The corridor leaves out each town's box so nothing is built twice.
# Run: sh tools/ue_region.sh [outdir]   (default /Volumes/LaCie/Unreal/dl/region)
set -e; cd "$(dirname "$0")/.."; OUT=${1:-/Volumes/LaCie/Unreal/dl/region}; B=/Applications/Blender.app/Contents/MacOS/Blender; mkdir -p "$OUT"
TOWNS="ambleside lonsdale metrotown newwest portmoody steveston ladner surrey cloverdale whiterock brookswood walnutgrove fortlangley mapleridge abbotsford mission chilliwack harrison"
python3 - $TOWNS downtown > "$OUT/exclude.json" <<'PY'
import json, math, sys
LAT0, LON0 = 49.2833, -123.1187; boxes = []
for a in sys.argv[1:]:
    d = json.load(open(f"site/data/{a}.json")); la, lo = d["origin"]
    ox, oy = (lo - LON0) * math.cos(math.radians(LAT0)) * 111320, -(la - LAT0) * 110540
    xs = [p[0] + ox for b in d["buildings"] for p in b["p"]]; ys = [p[1] + oy for b in d["buildings"] for p in b["p"]]
    boxes.append([min(xs), min(ys), max(xs), max(ys)])
print(json.dumps(boxes))
PY
for T in $TOWNS; do $B -b --factory-startup --python tools/ue_city.py -- $T "$OUT/$T.glb" 800 grass 2>&1 | grep -E "^CHUNKS" | sed "s/^/$T /"; done
$B -b --factory-startup --python tools/ue_city.py -- corridor "$OUT/corridor.glb" 2000 grass "$OUT/exclude.json" 2>&1 | grep -E "^CHUNKS" | sed "s/^/corridor /"
