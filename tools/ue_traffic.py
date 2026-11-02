"""Traffic routes for Unreal from site/data/<area>.json: each main road near the centre becomes a loop (right lane out,
right lane back). Writes /tmp/vv_qa/traffic.json for unreal/traffic.py. Run: python3 tools/ue_traffic.py [area] [x y radius]"""
import json, math, random, sys
area = sys.argv[1] if len(sys.argv) > 1 else "downtown"
SX, SY, RAD = (float(v) for v in sys.argv[2:5]) if len(sys.argv) > 4 else (-4.875, 29.36, 500)
random.seed(3); d = json.load(open(f"site/data/{area}.json")); routes = []
def offset(pts, o):  # shift a polyline sideways (to the right of travel when o > 0, +y is south)
    out = []
    for i, (x, y) in enumerate(pts):
        a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]; L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
        out.append((x - (b[1] - a[1]) / L * o, y + (b[0] - a[0]) / L * o))
    return out
for r in d["roads"]:
    if r["k"] not in ("primary", "secondary", "trunk", "tertiary"): continue
    p = [q for q in r["p"] if math.hypot(q[0] - SX, q[1] - SY) < RAD]
    L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(p, p[1:]))
    if len(p) < 2 or L < 60: continue
    lane = r.get("w", 12) / 4
    loop = offset(p, -lane) + offset(p[::-1], -lane)
    for _ in range(max(1, int(L // 35))): routes.append({"pts": loop, "start": random.randrange(len(loop)), "speed": random.uniform(1000, 1500)})
random.shuffle(routes); routes = routes[:160]
print(len(routes), "cars"); json.dump(routes, open("/tmp/vv_qa/traffic.json", "w"))
