"""Export the drive from Brookswood to downtown Vancouver: Highway 1 and the big roads around it, the Fraser and the inlet.

Run: python3 tools/corridor.py [--hw cached-highways.json] [--water cached-water.json] [--buildings]
--buildings adds Overture footprints within 350 m of a motorway, trunk or primary road (cached raw rows in --rows).
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


RELEASE = "2026-10-21.0"
ROWS = "overture-corridor.json"  # raw Overture rows are cached here (about 120 MB); keep it out of the repo
REACH = 350 * SCALE  # 350 real metres, in game metres


def dense(pts, step):
    """Samples along a polyline every `step` game metres."""
    res = []
    for (ax, az), (bx, bz) in zip(pts, pts[1:]):
        n = max(1, int(math.hypot(bx - ax, bz - az) / step))
        res += [(ax + (bx - ax) * i / n, az + (bz - az) * i / n) for i in range(n)]
    return res + [tuple(pts[-1])]


def grid(pts, cell):
    g = {}
    for x, z in pts: g.setdefault((math.floor(x / cell), math.floor(z / cell)), []).append((x, z))
    return g


def near(g, cell, x, z, r):
    """True when a road sample lies within r of (x, z), looking only at the cells around it."""
    k, cx, cz = math.ceil(r / cell), math.floor(x / cell), math.floor(z / cell)
    return any(math.hypot(x - px, z - pz) <= r for i in range(cx - k, cx + k + 1) for j in range(cz - k, cz + k + 1) for px, pz in g.get((i, j), ()))


def touches(ring, x, z, r):
    """True when (x, z) is inside the footprint or within r of its outline."""
    hit = False
    for (ax, az), (bx, bz) in zip(ring, ring[1:] + ring[:1]):
        if (az > z) != (bz > z) and x < (bx - ax) * (z - az) / (bz - az) + ax: hit = not hit
        dx, dz = bx - ax, bz - az
        t = max(0, min(1, ((x - ax) * dx + (z - az) * dz) / (dx * dx + dz * dz or 1)))
        if math.hypot(ax + t * dx - x, az + t * dz - z) <= r: return True
    return hit


def overture_rows(path):
    """Raw Overture building rows in the corridor bbox. Cached so a rerun skips the S3 query."""
    cache = pathlib.Path(path)
    if cache.exists(): return json.loads(cache.read_text())
    import duckdb
    s, w, n, e = BBOX
    db = duckdb.connect()
    db.execute("INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs; SET s3_region='us-west-2';")
    rows = db.execute(f"""
        SELECT ST_AsGeoJSON(geometry), height, num_floors, class
        FROM read_parquet('s3://overturemaps-us-west-2/release/{RELEASE}/theme=buildings/type=building/*', hive_partitioning=1)
        WHERE bbox.xmin > {w} AND bbox.xmax < {e} AND bbox.ymin > {s} AND bbox.ymax < {n}""").fetchall()
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(rows))
    return rows


def buildings(roads, xz, rows):
    """Footprints near the big roads, drawn at 0.7 about their centroid, clear of the road centre lines."""
    lat0, lon0 = ORIGIN
    kx = math.cos(math.radians(lat0)) * 111320
    lines = [r["p"] for r in roads if r["k"] in KEEP]
    near_grid = grid([p for l in lines for p in dense(l, 10)], REACH)
    road_grid = grid([p for r in roads for p in dense(r["p"], 1)], 4)
    kept = []
    for geo, height, floors, _ in rows:
        g = json.loads(geo)
        ring = (g["coordinates"][0] if g["type"] == "Polygon" else max((p[0] for p in g["coordinates"]), key=len))[:-1]
        if len(ring) < 3: continue
        clon, clat = sum(lon for lon, _ in ring) / len(ring), sum(lat for _, lat in ring) / len(ring)
        real = [((lon - clon) * kx, (lat - clat) * 110540) for lon, lat in ring]
        area = abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(real, real[1:] + real[:1]))) / 2
        if area < 40: continue
        cx, cz = xz({"lat": clat, "lon": clon})
        if not near(near_grid, REACH, cx, cz, REACH): continue
        p = [[round(cx + x * 0.7, 1), round(cz - z * 0.7, 1)] for x, z in real]
        xs, zs = [a for a, _ in p], [b for _, b in p]
        cells = [(i, j) for i in range(math.floor((min(xs) - 4) / 4), math.floor((max(xs) + 4) / 4) + 1) for j in range(math.floor((min(zs) - 4) / 4), math.floor((max(zs) + 4) / 4) + 1)]
        if any(touches(p, x, z, 4) for c in cells for x, z in road_grid.get(c, ())): continue
        h = min(max(height or (floors and floors * 3.2) or 6, 3), 120)
        kept.append((area, {"p": p, "h": round(h, 1)}))
    kept.sort(key=lambda b: -b[0])
    return [b for _, b in kept[:25000]]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--hw"); ap.add_argument("--water")
    ap.add_argument("--buildings", action="store_true", help="add Overture building footprints near the big roads")
    ap.add_argument("--rows", help="cache file for the raw Overture rows (default: next to --hw, else the scratchpad)")
    a = ap.parse_args()
    rows_cache = a.rows or (str(pathlib.Path(a.hw).with_name("overture-corridor.json")) if a.hw else ROWS)
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
    if a.buildings: out["buildings"] = buildings(out["roads"], xz, overture_rows(rows_cache))
    path = pathlib.Path(__file__).resolve().parent.parent / "site/data/corridor.json"
    path.write_text(json.dumps(out, separators=(",", ":")))
    print("corridor", {k: len(out[k]) for k in ("roads", "water", "buildings")}, path.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
