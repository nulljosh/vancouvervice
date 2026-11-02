"""Sidewalk walking loops for Unreal from site/data/<area>.json: each street near the centre gets loops on both
sidewalks (out on one side, back on the other). Writes /tmp/vv_qa/people.json for unreal/people.py.
Run: python3 tools/ue_people.py [area] [x y radius]"""
import json, math, random, sys
area = sys.argv[1] if len(sys.argv) > 1 else "downtown"
SX, SY, RAD = (float(v) for v in sys.argv[2:5]) if len(sys.argv) > 4 else (-4.875, 29.36, 350)
random.seed(11); d = json.load(open(f"site/data/{area}.json")); walks = []
def offset(pts, o):
    out = []
    for i, (x, y) in enumerate(pts):
        a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]; L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
        out.append((x - (b[1] - a[1]) / L * o, y + (b[0] - a[0]) / L * o))
    return out
for r in d["roads"]:
    if r["k"] not in ("primary", "secondary", "tertiary", "residential", "trunk", "unclassified"): continue
    p = [q for q in r["p"] if math.hypot(q[0] - SX, q[1] - SY) < RAD]
    L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(p, p[1:]))
    if len(p) < 2 or L < 40: continue
    side = r.get("w", 10) / 2 + random.uniform(1.6, 2.8)
    for o in (side, -side):
        loop = offset(p, o) + offset(p[::-1], o)
        for _ in range(max(1, int(L // 30))): walks.append({"pts": loop, "start": random.randrange(len(loop)), "speed": random.uniform(120, 165)})
random.shuffle(walks); walks = walks[:140]
print(len(walks), "people"); json.dump(walks, open("/tmp/vv_qa/people.json", "w"))
