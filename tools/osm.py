"""Export OSM buildings, roads, parks, POIs and coastal water in local metres.

Run: python3 tools/osm.py --area downtown|kits|victoria|langley|harrison|brookswood|fortlangley|walnutgrove|surrey|cloverdale|whiterock|metrotown. +x east, +y south.
Downtown also writes vancouver.json for the existing city page.
"""
import argparse, json, math, urllib.request, urllib.parse, pathlib

WIDTH = {"motorway": 18, "trunk": 16, "primary": 14, "secondary": 12, "tertiary": 10, "residential": 8, "unclassified": 8, "living_street": 6, "service": 5, "pedestrian": 6, "footway": 2.5}

AREAS = {
    "downtown": ((49.2833, -123.1187), (49.2690, -123.1500, 49.2960, -123.0950)),
    "kits": ((49.2690, -123.1575), (49.2620, -123.1750, 49.2760, -123.1400)),
    "victoria": ((48.4250, -123.3650), (48.4150, -123.3800, 48.4350, -123.3500)),
    "langley": ((49.1044, -122.6604), (49.0950, -122.6750, 49.1120, -122.6450)),
    "harrison": ((49.2972, -121.7850), (49.2935, -121.7990, 49.3085, -121.7690)),
    "brookswood": ((49.0757, -122.6688), (49.0680, -122.6840, 49.0840, -122.6420)),  # 200 St and 40 Ave, south Langley
    "fortlangley": ((49.1680, -122.5790), (49.1600, -122.5960, 49.1760, -122.5640)),  # Glover Road at Mavis Avenue, the village and the fort
    "walnutgrove": ((49.1640, -122.6400), (49.1560, -122.6560, 49.1720, -122.6240)),  # 88 Avenue at 208 Street, Walnut Grove
    "surrey": ((49.1890, -122.8490), (49.1810, -122.8630, 49.1970, -122.8350)),  # King George Boulevard at Central City, Surrey City Centre
    "cloverdale": ((49.1060, -122.7330), (49.0980, -122.7470, 49.1140, -122.7190)),  # 176 Street at 57 Avenue, old Cloverdale
    "whiterock": ((49.0200, -122.8020), (49.0120, -122.8160, 49.0280, -122.7880)),  # Marine Drive above the pier, White Rock
    "metrotown": ((49.2260, -123.0030), (49.2180, -123.0170, 49.2340, -122.9890)),  # Kingsborough at Metrotown station, Burnaby
}


def rings(ways):
    """Join a multipolygon's outer ways end to end into closed rings (OSM splits big lakes into many ways)."""
    ways, out = [list(w) for w in ways if len(w) > 1], []
    while ways:
        ring = ways.pop()
        while ring[0] != ring[-1]:
            nxt = next((w for w in ways if w[0] == ring[-1] or w[-1] == ring[-1]), None)
            if nxt is None: break  # ponytail: an open ring (member outside the download) is dropped below
            ways.remove(nxt)
            ring += (nxt if nxt[0] == ring[-1] else nxt[::-1])[1:]
        if ring[0] == ring[-1] and len(ring) >= 4: out.append(ring[:-1])
    return out


def clip(poly, bounds):
    """Sutherland-Hodgman: cut a polygon to the export rectangle, so a 60 km lake becomes the bit on screen."""
    xmin, ymin, xmax, ymax = bounds
    for inside, cut in ((lambda p: p[0] >= xmin, lambda a, b: [xmin, a[1] + (xmin - a[0]) * (b[1] - a[1]) / (b[0] - a[0])]),
                        (lambda p: p[0] <= xmax, lambda a, b: [xmax, a[1] + (xmax - a[0]) * (b[1] - a[1]) / (b[0] - a[0])]),
                        (lambda p: p[1] >= ymin, lambda a, b: [a[0] + (ymin - a[1]) * (b[0] - a[0]) / (b[1] - a[1]), ymin]),
                        (lambda p: p[1] <= ymax, lambda a, b: [a[0] + (ymax - a[1]) * (b[0] - a[0]) / (b[1] - a[1]), ymax])):
        pts, poly = poly, []
        for i, b in enumerate(pts):
            a = pts[i - 1]
            if inside(b):
                if not inside(a): poly.append(cut(a, b))
                poly.append(b)
            elif inside(a): poly.append(cut(a, b))
        if not poly: return []
    return [[round(x, 1), round(y, 1)] for x, y in poly]


def coast_water(lines, bounds):
    """Slice directed OSM coasts into water trapezoids; +y points south.

    OSM water is right of each way, hence positive cross product here.
    Horizontal strips preserve islands without holes in the game's ring format.
    """
    xmin, ymin, xmax, ymax = bounds
    segments = [(a, b) for line in lines for a, b in zip(line, line[1:]) if a != b]
    if not segments:
        return []
    levels = sorted({ymin, ymax, *(p[1] for line in lines for p in line if ymin < p[1] < ymax)})
    # Include rectangle intersections so clamping never bends a shoreline.
    crossings = [a[1] + (x-a[0]) * (b[1]-a[1]) / (b[0]-a[0])
                 for a, b in segments if a[0] != b[0] for x in (xmin, xmax)
                 if min(a[0], b[0]) < x < max(a[0], b[0])]
    levels = sorted({*levels, *(y for y in crossings if ymin < y < ymax)})
    water = []
    def at(seg, y):
        a, b = seg
        return a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
    # ponytail: O(vertices * segments); spatial indexing if regional exports grow.
    for low, high in zip(levels, levels[1:]):
        mid = (low + high) / 2
        cuts = sorted((s for s in segments if min(s[0][1], s[1][1]) < mid < max(s[0][1], s[1][1])), key=lambda s: at(s, mid))
        if not cuts:
            # Outside a closed island's latitude range, choose the nearest shore.
            def distance(s):
                a, b = s
                dx, dy = b[0]-a[0], b[1]-a[1]
                t = max(0, min(1, (((xmin+xmax)/2-a[0])*dx+(mid-a[1])*dy)/(dx*dx+dy*dy)))
                return ((xmin+xmax)/2-a[0]-t*dx)**2+(mid-a[1]-t*dy)**2
            a, b = min(segments, key=distance)
            wet = (b[0]-a[0])*(mid-a[1])-(b[1]-a[1])*((xmin+xmax)/2-a[0]) > 0
        else:
            wet = cuts[0][1][1] > cuts[0][0][1]
        left = None
        for right in [*cuts, None]:
            if wet:
                lx = [max(xmin, min(xmax, at(left, y))) if left else xmin for y in (low, high)]
                rx = [max(xmin, min(xmax, at(right, y))) if right else xmax for y in (low, high)]
                if sum(rx) - sum(lx) > 1e-8:
                    water.append([[lx[0], low], [rx[0], low], [rx[1], high], [lx[1], high]])
            if right:
                wet = right[1][1] < right[0][1]
            left = right
    return water


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--area", choices=AREAS, default="downtown")
    args = parser.parse_args()
    (lat0, lon0), bbox = AREAS[args.area]
    kx = math.cos(math.radians(lat0)) * 111320
    def xz(p): return [round((p["lon"] - lon0) * kx, 1), round(-(p["lat"] - lat0) * 110540, 1)]
    query = f"""[out:json][timeout:120];
(way["building"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
 way["highway"~"^(motorway|trunk|primary|secondary|tertiary|residential|unclassified|living_street|service|pedestrian|footway)$"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
 way["amenity"="parking"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
 way["leisure"~"^(park|garden|pitch)$"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
 way["natural"="coastline"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
 way["natural"="water"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
 relation["natural"="water"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
 node["shop"]["name"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
 node["amenity"~"^(cafe|restaurant|bar|pub|fast_food|bank|pharmacy|cinema|nightclub|ice_cream|library)$"]["name"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
 node["tourism"~"^(hotel|museum|gallery)$"]["name"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
 way["railway"~"^(light_rail|subway)$"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
 node["railway"="station"]["name"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}););
out geom;"""

    MIRRORS = ("https://overpass-api.de/api/interpreter", "https://overpass.kumi.systems/api/interpreter", "https://overpass.private.coffee/api/interpreter")
    for endpoint in MIRRORS:
        req = urllib.request.Request(endpoint, data=urllib.parse.urlencode({"data": query}).encode(), headers={"User-Agent": "vancouvervice-game/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                data = json.load(response)
            if "remark" in data:
                raise RuntimeError(data["remark"])
            break
        except (urllib.error.URLError, TimeoutError, RuntimeError):
            if endpoint == MIRRORS[-1]:
                raise

    out = {"origin": [lat0, lon0], "buildings": [], "roads": [], "parks": [], "water": [], "pois": [], "rail": [], "stations": [], "lots": []}
    northwest = xz({"lat": bbox[2], "lon": bbox[1]})
    southeast = xz({"lat": bbox[0], "lon": bbox[3]})
    coasts = []
    for el in data["elements"]:
        t, g = el.get("tags", {}), el.get("geometry")
        if el["type"] == "node":
            kind = t.get("amenity") or t.get("tourism") or ("grocery" if t.get("shop") in ("supermarket", "convenience", "grocery") else "shop")
            if t.get("railway") == "station": out["stations"].append([*xz(el), t["name"]]); continue
            out["pois"].append([*xz(el), kind, t["name"]]); continue
        if el["type"] == "relation":
            # big lakes are multipolygons: join the outer ways, keep what falls inside the export
            outer = [[xz(p) for p in m["geometry"]] for m in el.get("members", []) if m.get("role") == "outer" and m.get("geometry")]
            for ring in rings(outer):
                if len(c := clip(ring, (*northwest, *southeast))) >= 3: out["water"].append(c)
            continue
        if not g or len(g) < 2: continue
        pts = [xz(p) for p in g]
        if t.get("railway") in ("light_rail", "subway"):
            out["rail"].append({"p": pts, "n": t.get("name", "SkyTrain")})
        elif t.get("natural") == "coastline":
            coasts.append(pts)
        elif "building" in t and len(pts) >= 4:
            h = t.get("height", "").replace("m", "").strip()
            try: h = float(h)
            except ValueError: h = float(t.get("building:levels", 0) or 0) * 3.3 or (18 if t["building"] in ("commercial", "office", "apartments") else 9)
            out["buildings"].append({"p": pts[:-1], "h": round(max(3, min(h, 330)), 1), "n": t.get("name", "")})
        elif t.get("amenity") == "parking":
            if len(pts) >= 4 and pts[0] == pts[-1]: out["lots"].append(pts[:-1])
        elif "highway" in t:
            out["roads"].append({"p": pts, "w": WIDTH.get(t["highway"], 6), "n": t.get("name", ""), "k": t["highway"]})
        elif t.get("leisure") or t.get("natural") == "water":
            if len(pts) >= 4 and pts[0] == pts[-1]:
                out["water" if t.get("natural") == "water" else "parks"].append(pts[:-1])

    out["water"].extend(coast_water(coasts, (*northwest, *southeast)))
    path = pathlib.Path(__file__).resolve().parent.parent / "site/data" / f"{args.area}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(out, separators=(",", ":"))
    path.write_text(encoded)
    if args.area == "downtown":
        path.with_name("vancouver.json").write_text(encoded)
    print(args.area, {key: len(out[key]) for key in ("pois", "buildings", "roads", "parks", "water", "rail", "stations", "lots")}, path.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()
