"""Swap an area's buildings for Overture Maps footprints (every real building: OSM plus Microsoft and Google footprints).

Run after tools/osm.py: uvx --with duckdb python tools/overture.py --area brookswood
OSM names and heights win where an OSM building overlaps an Overture one. Writes "footprints": "overture" so the
game stops inventing houses for that area.
"""
import argparse, json, pathlib, sys
import duckdb

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from osm import AREAS  # noqa: E402

RELEASE = "2026-10-21.0"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--area", choices=AREAS, required=True)
    ap.add_argument("--rows", help="cache file for the Overture query (reused when present)")
    ap.add_argument("--roads", action="store_true", help="also replace the roads with Overture's (OSM-derived) segments, for when Overpass is down")
    args = ap.parse_args(); area = args.area
    (lat0, lon0), (s, w, n, e) = AREAS[area]
    path = pathlib.Path(__file__).resolve().parent.parent / "site/data" / f"{area}.json"
    data = json.loads(path.read_text())
    kx = __import__("math").cos(__import__("math").radians(lat0)) * 111320
    xz = lambda lon, lat: [round((lon - lon0) * kx, 1), round(-(lat - lat0) * 110540, 1)]

    cache = pathlib.Path(args.rows) if args.rows else None
    if cache and cache.exists():
        rows = json.loads(cache.read_text())
    else:
        db = duckdb.connect()
        db.execute("INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs; SET s3_region='us-west-2';")
        rows = db.execute(f"""
            SELECT ST_AsGeoJSON(geometry), height, num_floors, class
            FROM read_parquet('s3://overturemaps-us-west-2/release/{RELEASE}/theme=buildings/type=building/*', hive_partitioning=1)
            WHERE bbox.xmin > {w} AND bbox.xmax < {e} AND bbox.ymin > {s} AND bbox.ymax < {n}""").fetchall()
        if cache: cache.write_text(json.dumps(rows))

    osm = data["buildings"]
    def centre(p): return sum(x for x, _ in p) / len(p), sum(z for _, z in p) / len(p)
    def inside(p, x, z):
        hit = False
        for (ax, az), (bx, bz) in zip(p, p[1:] + p[:1]):
            if (az > z) != (bz > z) and x < (bx - ax) * (z - az) / (bz - az) + ax: hit = not hit
        return hit
    out = []
    for geo, height, floors, cls in rows:
        g = json.loads(geo)
        ring = (g["coordinates"][0] if g["type"] == "Polygon" else max((p[0] for p in g["coordinates"]), key=len))[:-1]
        if len(ring) < 3: continue
        p = [xz(lon, lat) for lon, lat in ring]
        cx, cz = centre(p)
        twin = next((b for b in osm if len(b["p"]) >= 3 and inside(b["p"], cx, cz)), None)
        h = height or (floors and floors * 3.1) or (twin and twin["h"]) or 9
        out.append({"p": p, "h": round(min(h, 330), 1), "n": (twin or {}).get("n", ""), **({"k": cls} if cls else {})})
    # keep any OSM building Overture missed
    out += [b for b in osm if len(b["p"]) >= 3 and not any(inside(o["p"], *centre(b["p"])) for o in out)]
    data["buildings"], data["footprints"] = out, "overture"
    if args.roads:
        from osm import WIDTH
        db = duckdb.connect(); db.execute("INSTALL spatial; LOAD spatial; INSTALL httpfs; LOAD httpfs; SET s3_region='us-west-2';")
        segs = db.execute(f"""
            SELECT ST_AsGeoJSON(geometry), class, names.primary
            FROM read_parquet('s3://overturemaps-us-west-2/release/{RELEASE}/theme=transportation/type=segment/*', hive_partitioning=1)
            WHERE subtype = 'road' AND bbox.xmax > {w} AND bbox.xmin < {e} AND bbox.ymax > {s} AND bbox.ymin < {n}""").fetchall()
        keep = {"motorway", "trunk", "primary", "secondary", "tertiary", "residential", "unclassified", "living_street", "service", "pedestrian", "footway"}
        data["roads"] = [{"p": [xz(lon, lat) for lon, lat in json.loads(g)["coordinates"]], "w": WIDTH.get(c, 6), "n": nm or "", "k": c} for g, c, nm in segs if c in keep and json.loads(g)["type"] == "LineString"]
        print(len(data["roads"]), "Overture road segments")
    path.write_text(json.dumps(data, separators=(",", ":")))
    print(area, len(rows), "Overture footprints,", len(out), "buildings in all,", path.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
