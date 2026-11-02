"""Builds a real-streets map (site/data/<area>.json) as sharp, textured city chunks for Unreal, in headless Blender.
Same rules as city.html: storefront band on the ground floor, glass towers over 45 m, concrete or glass mid-rise,
brick or stone low-rise, tar roofs, asphalt roads on concrete sidewalks, grass parks, water.
Run: Blender -b --factory-startup --python tools/ue_city.py -- <area> <out.glb> [chunk_m]
Coordinates: data is metres, +x east, +y south. Blender gets +X east, +Y north, so y flips."""
import bpy, json, math, os, sys
from mathutils.geometry import tessellate_polygon
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
AREA, OUT = argv[0], argv[1]
CHUNK = float(argv[2]) if len(argv) > 2 else 800.0
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
D = json.load(open(os.path.join(ROOT, "data", AREA + ".json")))

bpy.ops.wm.read_factory_settings(use_empty=True)

def image_mat(name, img, rough, metal=0.0, tint=None):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if img:
        t = m.node_tree.nodes.new("ShaderNodeTexImage"); t.image = bpy.data.images.load(os.path.join(ROOT, "materials", img))
        m.node_tree.links.new(t.outputs["Color"], b.inputs["Base Color"])
    elif tint:
        b.inputs["Base Color"].default_value = (*tint, 1)
    return m

# material name -> (image, tile width m, tile height m, roughness, metal)
MATS = {
    "shop": ("shop.jpg", 16, 8, .5, 0), "glass": ("glass.jpg", 14, 14, .12, .55), "concrete": ("concrete.jpg", 14, 14, .85, 0),
    "brick": ("brick.jpg", 13, 13, .9, 0), "stone": ("stone.jpg", 14, 14, .8, 0), "roof": ("asphalt.jpg", 5, 5, 1, 0),
    "road": ("asphalt.jpg", 6, 6, .95, 0), "walk": ("sidewalk.jpg", 3, 3, .9, 0), "grass": ("grass.jpg", 6, 6, 1, 0),
}
for k in ["cafe", "clothes", "restaurant", "convenience", "barber", "pub", "guns", "pharmacy", "pawn"]:
    MATS["shop-" + k] = ("shop-%s.jpg" % k, 14.2, 8, .5, 0)
M = {k: image_mat(k, v[0], v[3], v[4]) for k, v in MATS.items()}
M["water"] = image_mat("water", None, .05, 0, (.02, .07, .09)); MATS["water"] = (None, 50, 50, .05, 0)

chunks = {}  # (cx, cy) -> {mat: [verts, faces, uvs]}
def bucket(x, y, mat):
    c = chunks.setdefault((math.floor(x / CHUNK), math.floor(y / CHUNK)), {})
    return c.setdefault(mat, [[], [], []])

def P(x, y, z): return (x, -y, z)  # data +y south -> Blender +Y north

def walls(pts, z0, z1, mat, cx, cy):
    V, F, U = bucket(cx, cy, mat); tw, th = MATS[mat][1], MATS[mat][2]; run = 0.0
    ring = pts + [pts[0]] if pts[0] != pts[-1] else pts
    for (ax, ay), (bx, by) in zip(ring, ring[1:]):
        L = math.hypot(bx - ax, by - ay)
        if L < .05: continue
        i = len(V); V += [P(ax, ay, z0), P(bx, by, z0), P(bx, by, z1), P(ax, ay, z1)]
        F.append((i, i + 1, i + 2, i + 3))
        U += [(run / tw, z0 / th), ((run + L) / tw, z0 / th), ((run + L) / tw, z1 / th), (run / tw, z1 / th)]; run += L

def flat(pts, z, mat, cx, cy):
    if len(pts) < 3: return
    if pts[0] == pts[-1]: pts = pts[:-1]
    V, F, U = bucket(cx, cy, mat); tw = MATS[mat][1]
    try: tris = tessellate_polygon([[Vector((x, -y, 0)) for x, y in pts]])
    except Exception: return
    i = len(V); V += [P(x, y, z) for x, y in pts]; U += [(x / tw, -y / tw) for x, y in pts]
    F += [(i + c, i + b, i + a) for a, b, c in tris]  # wound to face up

def ribbon(pts, w, z, mat):
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        L = math.hypot(bx - ax, by - ay)
        if L < .05: continue
        nx, ny = -(by - ay) / L * w / 2, (bx - ax) / L * w / 2; ex, ey = (bx - ax) / L * w / 4, (by - ay) / L * w / 4  # overlap the joints
        q = [(ax - ex + nx, ay - ey + ny), (bx + ex + nx, by + ey + ny), (bx + ex - nx, by + ey - ny), (ax - ex - nx, ay - ey - ny)]
        V, F, U = bucket((ax + bx) / 2, (ay + by) / 2, mat); tw = MATS[mat][1]; i = len(V)
        V += [P(x, y, z) for x, y in q]; U += [(x / tw, -y / tw) for x, y in q]; F.append((i + 3, i + 2, i + 1, i))

def inside(pts, x, y):
    c = False
    for (ax, ay), (bx, by) in zip(pts, pts[1:] + pts[:1]):
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax: c = not c
    return c

SHOPKIND = {"guns": "guns", "clothes": "clothes", "barber": "barber", "cafe": "cafe", "restaurant": "restaurant", "fast_food": "restaurant",
            "ice_cream": "cafe", "bar": "pub", "pub": "pub", "nightclub": "pub", "pharmacy": "pharmacy", "grocery": "convenience", "pawn": "pawn"}
CELL = 60; grid = {}
for n, b in enumerate(D["buildings"]):
    if len(b["p"]) < 3: continue
    xs = [p[0] for p in b["p"]]; ys = [p[1] for p in b["p"]]
    for gx in range(math.floor(min(xs) / CELL), math.floor(max(xs) / CELL) + 1):
        for gy in range(math.floor(min(ys) / CELL), math.floor(max(ys) / CELL) + 1): grid.setdefault((gx, gy), []).append(n)
shopOf = {}
for x, y, kind, *_ in D.get("pois", []):
    s = SHOPKIND.get(kind)
    if not s: continue
    for n in grid.get((math.floor(x / CELL), math.floor(y / CELL)), []):
        if n not in shopOf and inside(D["buildings"][n]["p"], x, y): shopOf[n] = s; break

for n, b in enumerate(D["buildings"]):
    p = b["p"]
    if len(p) < 3 or b.get("canopy"): continue
    h = max(3.0, b.get("h") or 8); cx = sum(q[0] for q in p) / len(p); cy = sum(q[1] for q in p) / len(p)
    band = min(8, h); kind = "glass" if h > 45 else ("concrete" if n % 3 else "glass") if h > 16 else ("brick" if n % 3 else "stone")
    sk = shopOf.get(n) or ["", "cafe", "clothes", "restaurant", "", "convenience", "barber", "pub"][n % 8]
    walls(p, 0, band, "shop-" + sk if sk else "shop", cx, cy)
    if h > band: walls(p, band, h, kind, cx, cy)
    flat(p, h, "roof", cx, cy)

for r in D["roads"]:
    if r["k"] in ("footway",): ribbon(r["p"], 3, .06, "walk"); continue
    w = r.get("w", 8); ribbon(r["p"], w + 7, .03, "walk"); ribbon(r["p"], w, .09, "road")
for poly in D.get("parks", []):
    if len(poly) > 2: flat(poly, .02, "grass", *poly[0])
for poly in D.get("water", []):
    if len(poly) > 2: flat(poly, .12, "water", *poly[0])

# a paved base under everything, chunk by chunk
xs = [p[0] for b in D["buildings"] for p in b["p"]]; ys = [p[1] for b in D["buildings"] for p in b["p"]]
for gx in range(math.floor(min(xs) / CHUNK), math.floor(max(xs) / CHUNK) + 1):
    for gy in range(math.floor(min(ys) / CHUNK), math.floor(max(ys) / CHUNK) + 1):
        x0, y0 = gx * CHUNK, gy * CHUNK
        flat([(x0, y0), (x0 + CHUNK, y0), (x0 + CHUNK, y0 + CHUNK), (x0, y0 + CHUNK)], 0, "walk", x0 + 1, y0 + 1)

tris = 0
for (gx, gy), mats in chunks.items():
    me = bpy.data.meshes.new("City_%s_%d_%d" % (AREA, gx, gy)); V, F, U, MI = [], [], [], []; order = list(mats)
    for mi, k in enumerate(order):
        v, f, u = mats[k]; o = len(V); V += v; F += [tuple(i + o for i in face) for face in f]; MI += [mi] * len(f); U += u
    me.from_pydata(V, [], F); me.update()
    for k in order: me.materials.append(M[k])
    for poly, mi in zip(me.polygons, MI): poly.material_index = mi
    uv = me.uv_layers.new(name="UVMap")
    for loop in me.loops: uv.data[loop.index].uv = U[loop.vertex_index]
    for poly in me.polygons: poly.use_smooth = False
    ob = bpy.data.objects.new(me.name, me); bpy.context.collection.objects.link(ob); tris += sum(len(p.vertices) - 2 for p in me.polygons)
print("CHUNKS", len(chunks), "TRIS", tris)
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_image_format="JPEG", export_yup=True)
print("WROTE", OUT, os.path.getsize(OUT))
