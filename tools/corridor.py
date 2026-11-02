"""Export the drive from Brookswood to downtown Vancouver: Highway 1 and the big roads around it, the Fraser and the inlet.

Run: python3 tools/corridor.py [--hw cached-highways.json] [--water cached-water.json]
The real route is about 50 km. The corridor map is drawn at half scale (SCALE) so the drive takes about 12 minutes,
while Brookswood and downtown stay life size; city.html hands the car between them by latitude and longitude.
"""
import argparse, json, math, pathlib, urllib.request, urllib.parse
from osm import rings, clip, coast_water

SCALE = 0.5
ORIGIN = (49.0757, -122.6688)  # Brookswood's origin, so the two maps share a reference
BBOX = (49.06, -123.16, 49.31, -122.63)
KEEP = {"motorway", "motorway_link", "trunk", "trunk_link", "primary", "primary_link"}
MIRRORS = ("https://overpass-api.de/api/interpreter", "https://overpass.private.coffee/api/interpreter", "https://overpass.kumi.systems/api/interpreter")


def fetch(query):
    for endpoint in MIRRORS:
        try:
            req = urllib.request.Request(endpoint, data=urllib.parse.urlencode({"data": query}).encode(), headers={"User-Agent": "vancouvervice-game/1.0"})
            with urllib.request.urlopen(req, timeout=300) as r:
                return json.load(r)
        except Exception:
            if endpoint == MIRRORS[-1]: raise


def simplify(pts, tol):
    """Douglas-Peucker: a 50 km shoreline at full OSM detail would slice into tens of thousands of water strips."""
    if len(pts) < 3: return pts
    (ax, ay), (bx, by) = pts[0], pts[-1]
    L = math.hypot(bx - ax, by - ay) or 1e-9
    i, d = max(((i, abs((by - ay) * p[0] - (bx - ax) * p[1] + bx * ay - by * ax) / L) for i, p in enumerate(pts[1:-1], 1)), key=lambda q: q[1])
    return simplify(pts[:i + 1], tol)[:-1] + simplify(pts[i:], tol) if d > tol else [pts[0], pts[-1]]


def width(t):
    """Carriageway width in game metres: real lanes at 3.7 m plus shoulders, shrunk a little so split carriageways at half scale don't overlap."""
    k = t["highway"]
    try: lanes = int(t.get("lanes", "").split(";")[0])
    except ValueError: lanes = {"motorway": 3, "trunk": 2, "primary": 2}.get(k, 1)
    oneway = t.get("oneway") in ("yes", "1", "-1") or k in ("motorway", "motorway_link")
    lanes = lanes if oneway else max(2, lanes)
    return round((lanes * 3.7 + (3 if k.startswith("motorway") else 1)) * .8, 1), oneway, lanes


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--hw"); ap.add_argument("--water")
    a = ap.parse_args()
    b = ",".join(map(str, BBOX))
    hw = json.load(open(a.hw)) if a.hw else fetch(f'[out:json][timeout:180];way["highway"~"^(motorway|motorway_link|trunk|trunk_link|primary|primary_link|secondary)$"]({b});out geom;')
    wt = json.load(open(a.water)) if a.water else fetch(f'[out:json][timeout:240];(way["natural"="coastline"]({b});way["natural"="water"]["water"~"river|lake|reservoir"]({b});relation["natural"="water"]["water"~"river|lake"]({b});way["waterway"="riverbank"]({b}););out geom;')
    lat0, lon0 = ORIGIN
    kx = math.cos(math.radians(lat0)) * 111320
    def xz(p): return [round((p["lon"] - lon0) * kx * SCALE, 1), round(-(p["lat"] - lat0) * 110540 * SCALE, 1)]
    nw, se = xz({"lat": BBOX[2], "lon": BBOX[1]}), xz({"lat": BBOX[0], "lon": BBOX[3]})
    out = {"origin": [lat0, lon0], "scale": SCALE, "buildings": [], "roads": [], "parks": [], "water": [], "pois": [], "rail": [], "stations": [], "lots": []}
    for el in hw["elements"]:
        t, g = el.get("tags", {}), el.get("geometry") or []
        k = t.get("highway")
        if len(g) < 2 or not (k in KEEP or (k == "secondary" and t.get("name") == "200 Street")): continue
        w, ow, lanes = width(t)
        pts = [xz(p) for p in g]
        if t.get("oneway") == "-1": pts.reverse()
        r = {"p": pts, "w": w, "n": t.get("name") or t.get("ref", ""), "k": k, "lanes": lanes}
        if ow: r["ow"] = 1
        if t.get("ref"): r["ref"] = t["ref"]
        if t.get("bridge") == "yes" or t.get("layer", "0") not in ("0", ""):
            try: r["layer"] = int(t.get("layer", "1"))
            except ValueError: r["layer"] = 1
        out["roads"].append(r)
    coasts = []
    for el in wt["elements"]:
        if el["type"] == "relation":
            outer = [[xz(p) for p in m["geometry"]] for m in el.get("members", []) if m.get("role") == "outer" and m.get("geometry")]
            for ring in rings(outer):
                if len(c := clip(simplify(ring, 3), (*nw, *se))) >= 3: out["water"].append(c)
            continue
        g = el.get("geometry") or []
        pts = [xz(p) for p in g]
        if el.get("tags", {}).get("natural") == "coastline": coasts.append(simplify(pts, 6))
        elif len(pts) >= 4 and pts[0] == pts[-1] and len(c := clip(simplify(pts[:-1], 3), (*nw, *se))) >= 3: out["water"].append(c)
    out["water"].extend(coast_water(coasts, (*nw, *se)))
    path = pathlib.Path(__file__).resolve().parent.parent / "site/data/corridor.json"
    path.write_text(json.dumps(out, separators=(",", ":")))
    print("corridor", {k: len(out[k]) for k in ("roads", "water")}, path.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
