"""Build a detail island as a glTF for Unreal, headless, from the same spec city.html uses.
Run: blender -b -P tools/hero_blender.py -- granville-georgia [out.glb]
Footprints come from site/data/<area>.json, façade styles and heights from site/data/hero/<name>.json.
Storefront band, upper façade and roof get their own materials; tenant names become extruded text on the frontage.
Axes: game +x east, +z south. Blender is z-up, so game z becomes -y; the glTF exporter flips to y-up itself.
"""
import bpy, bmesh, json, math, sys, os
from pathlib import Path

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else ["granville-georgia"]
name, out = args[0], (args[1] if len(args) > 1 else f"unreal/assets/hero-{args[0]}.glb")
root = Path(__file__).resolve().parents[1]
spec = json.loads((root / "site/data/hero" / f"{name}.json").read_text())
D = json.loads((root / "site/data" / f"{spec['area']}.json").read_text())

bpy.ops.wm.read_factory_settings(use_empty=True)
def hexrgb(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)) + (1,)
def mat(n, color, rough=.5, metal=0.0, emit=None):
    m = bpy.data.materials.new(n); m.use_nodes = True
    bsdf = next(x for x in m.node_tree.nodes if x.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = color; bsdf.inputs["Roughness"].default_value = rough; bsdf.inputs["Metallic"].default_value = metal
    if emit: bsdf.inputs["Emission Color"].default_value = emit; bsdf.inputs["Emission Strength"].default_value = 1.5
    return m
mats = {k: mat(f"facade_{k}", hexrgb(s["base"]), .45, .2) for k, s in spec["styles"].items()}
mats["storefront"] = mat("storefront", (.16, .2, .24, 1), .2, .3); mats["roof"] = mat("roof", (.3, .31, .33, 1), .9)
mats["sign"] = mat("sign", (.75, .2, .17, 1), .4); mats["signtext"] = mat("signtext", (1, 1, 1, 1), .3, 0, (1, 1, 1, 1))
band = spec["band"]; pois = D.get("pois", [])

def add_mesh(nm, bm, m):
    me = bpy.data.meshes.new(nm); bm.to_mesh(me); bm.free(); ob = bpy.data.objects.new(nm, me); ob.data.materials.append(m); bpy.context.collection.objects.link(ob); return ob

def prism(nm, pts, y0, y1, m):
    bm = bmesh.new(); lo = [bm.verts.new((x, -z, y0)) for x, z in pts]; hi = [bm.verts.new((x, -z, y1)) for x, z in pts]
    n = len(pts)
    for i in range(n): bm.faces.new((lo[i], lo[(i + 1) % n], hi[(i + 1) % n], hi[i]))
    if y0 > 0: bm.faces.new(hi)
    bm.normal_update(); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); return add_mesh(nm, bm, m)

def signs(pts, bname):
    n = len(pts)
    for i in range(n):
        (ax, az), (bx, bz) = pts[i], pts[(i + 1) % n]; L = math.hypot(bx - ax, bz - az)
        if L < 6: continue
        ux, uz = (bx - ax) / L, (bz - az) / L; nx, nz = -uz, ux  # outward for CCW-in-game (area > 0)
        for x, z, kind, label in pois:
            t = ((x - ax) * ux + (z - az) * uz) / L
            if not .03 < t < .97: continue
            px, pz = ax + (bx - ax) * t, az + (bz - az) * t
            if math.hypot(x - px, z - pz) > 12: continue
            w = max(4, min(L * .6, len(label) * .55))
            bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1); bmesh.ops.scale(bm, vec=(w, .15, 1.0), verts=bm.verts)
            board = add_mesh(f"sign_{label}", bm, mats["sign"]); board.location = (px + nx * .12, -(pz + nz * .12), band - .55); board.rotation_euler = (0, 0, math.atan2(-uz, ux))
            cu = bpy.data.curves.new(f"txt_{label}", "FONT"); cu.body = label; cu.size = .6; cu.extrude = .02; cu.align_x = "CENTER"; cu.align_y = "CENTER"
            tx = bpy.data.objects.new(f"txt_{label}", cu); tx.data.materials.append(mats["signtext"]); bpy.context.collection.objects.link(tx)
            tx.location = (px + nx * .22, -(pz + nz * .22), band - .55); tx.rotation_euler = (math.pi / 2, 0, math.atan2(-uz, ux))

count = 0
for b in spec["buildings"]:
    src = D["buildings"][b["id"]]; p = src["p"]
    area = sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))
    pts = p if area > 0 else list(reversed(p))
    prism(f"{b['name']}_ground", pts, 0, band, mats["storefront"]); prism(f"{b['name']}_upper", pts, band, b["h"], mats[b["style"]])
    signs(pts, b["name"]); count += 1
    if b.get("clock"):
        cx = sum(q[0] for q in p) / len(p); cz = sum(q[1] for q in p) / len(p)
        bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1); bmesh.ops.scale(bm, vec=(7, 7, 12), verts=bm.verts); t = add_mesh("clock_tower", bm, mats["stone"]); t.location = (cx, -cz, b["h"] + 6)
        bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=2.2, radius2=1.2, depth=4); l = add_mesh("clock_lantern", bm, mats["roof"]); l.location = (cx, -cz, b["h"] + 14)
# roofs share the upper prism cap already; stamp the roof material on top faces
for ob in bpy.data.objects:
    if ob.name.endswith("_upper"):
        ob.data.materials.append(mats["roof"])
        for f in ob.data.polygons:
            if f.normal.z > .9: f.material_index = 1
bpy.ops.object.select_all(action="SELECT")
for ob in list(bpy.data.objects):
    if ob.type == "FONT": bpy.context.view_layer.objects.active = ob; bpy.ops.object.convert(target="MESH")
outp = root / out; outp.parent.mkdir(parents=True, exist_ok=True)
bpy.ops.export_scene.gltf(filepath=str(outp), export_format="GLB", export_apply=True, export_yup=True)
print(f"hero: {count} buildings, {len([o for o in bpy.data.objects if o.name.startswith('txt_')])} tenant signs -> {outp} ({outp.stat().st_size // 1024} KB)")
