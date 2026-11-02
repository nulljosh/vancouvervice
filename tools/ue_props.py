"""Street props for Unreal: parked cars along both curbs, street lights every 34 m, trees every 13 m on smaller streets,
from site/data/<area>.json, within RAD metres of a centre. Writes /tmp/vv_qa/props.json for unreal/street_props.py.
Run: python3 tools/ue_props.py [area] [x y radius]   (metres, +x east, +y south; default the Apple Store spawn)"""
import json, math, random, sys
area = sys.argv[1] if len(sys.argv) > 1 else "downtown"
SX, SY, RAD = (float(v) for v in sys.argv[2:5]) if len(sys.argv) > 4 else (-4.875, 29.36, 650)
random.seed(7); d = json.load(open(f"site/data/{area}.json")); CELL = 40; grid = {}
for b in d["buildings"]:
    xs = [p[0] for p in b["p"]]; ys = [p[1] for p in b["p"]]
    for gx in range(int(min(xs) // CELL), int(max(xs) // CELL) + 1):
        for gy in range(int(min(ys) // CELL), int(max(ys) // CELL) + 1): grid.setdefault((gx, gy), []).append(b["p"])
def inside(pts, x, y):
    c = False
    for (ax, ay), (bx, by) in zip(pts, pts[1:] + pts[:1]):
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax: c = not c
    return c
blocked = lambda x, y: any(inside(p, x, y) for p in grid.get((int(x // CELL), int(y // CELL)), []))
out = {"car": [], "lamp": [], "tree": []}; ok = {"residential", "secondary", "tertiary", "primary", "unclassified", "living_street", "trunk"}
for r in d["roads"]:
    if r["k"] not in ok: continue
    w = r.get("w", 8)
    for (ax, ay), (bx, by) in zip(r["p"], r["p"][1:]):
        L = math.hypot(bx - ax, by - ay)
        if L < 20 or math.hypot((ax + bx) / 2 - SX, (ay + by) / 2 - SY) > RAD: continue
        ux, uy = (bx - ax) / L, (by - ay) / L; nx, ny = -uy, ux; yaw = math.degrees(math.atan2(uy, ux))
        for side in (1, -1):
            at = lambda s, off: (ax + ux * s + nx * side * off, ay + uy * s + ny * side * off)
            for s in [10 + 6.5 * i for i in range(int((L - 20) / 6.5) + 1)]:  # parked cars, 45 percent of bays, kept off corners
                x, y = at(s, w / 2 - 1.3)
                if random.random() < .45 and not blocked(x, y): out["car"].append([x, y, yaw + (0 if side > 0 else 180), random.random() < .3])
            for s in [8 + 34 * i for i in range(int((L - 12) / 34) + 1)]:
                x, y = at(s, w / 2 + 2.4)
                if not blocked(x, y): out["lamp"].append([x, y, yaw + (-90 if side > 0 else 90)])
            if r["k"] in ("residential", "tertiary", "secondary"):
                for s in [5 + 13 * i for i in range(int((L - 10) / 13) + 1)]:
                    x, y = at(s, w / 2 + 4.2)
                    if not blocked(x, y) and random.random() < .8: out["tree"].append([x, y, random.uniform(0, 360), random.uniform(.8, 1.15)])
print({k: len(v) for k, v in out.items()}); json.dump(out, open("/tmp/vv_qa/props.json", "w"))
