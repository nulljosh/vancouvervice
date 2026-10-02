"""Make Joshua's body read as a lean man, in Blender, deterministically.
Headless: /Applications/Blender.app/Contents/MacOS/Blender -b --python unreal/body_male.py
Reads unreal/assets/joshua_body_v3.fbx (the MetaHuman export, which keeps the female base shape whatever the
sliders say, see docs/METAHUMAN-API.md), writes unreal/assets/joshua_body_v4.fbx plus body_male_front.png and
body_male_side.png. Every LOD gets the same treatment so the Unreal import stays consistent. UVs and weights are
untouched, so the baked MetaHuman skin textures still fit.
Coordinates are body-local cm, -Y is the front (same as polo.py).
"""
import bpy, math, os
from mathutils import Vector

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "unreal/assets/joshua_body_v3.fbx")
DST = os.path.join(REPO, "unreal/assets/joshua_body_v4.fbx")
FRONT = -1.0
CHEST_Z = (110.0, 140.0)     # the band the bust lives in
CHEST_PULL = 0.65            # how far the bust gets pulled back toward the sternum line (1 = flat, craters)
HIP_Z, HIP_SCALE = (72.0, 106.0), 0.90
WAIST_Z, WAIST_SCALE = (96.0, 118.0), 0.95
SHOULDER_Z, SHOULDER_SCALE = (128.0, 144.0), 1.07

def window(z, lo, hi, feather=6.0):
    """1 inside the band, easing to 0 over `feather` cm outside it."""
    if z < lo - feather or z > hi + feather: return 0.0
    if lo <= z <= hi: return 1.0
    d = (lo - z) if z < lo else (z - hi)
    return 0.5 + 0.5 * math.cos(math.pi * d / feather)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=SRC)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
meshes = [o for o in bpy.data.objects if o.type == "MESH"]

for me in meshes:
    vs = me.data.vertices
    # sternum line: per 2 cm row in the chest band, the front-most y within 2.5 cm of the centre line
    rows = {}
    for v in vs:
        z = v.co.z
        if CHEST_Z[0] - 6 <= z <= CHEST_Z[1] + 6 and abs(v.co.x) < 2.5 and v.co.y * FRONT > 0:
            k = int(z // 2); rows[k] = max(rows.get(k, -1e9), v.co.y * FRONT)
    def sternum(z):
        k = int(z // 2)
        near = [rows[j] for j in (k - 1, k, k + 1) if j in rows]
        return max(near) if near else None
    for v in vs:
        x, y, z = v.co
        w = window(z, *CHEST_Z)
        if w and y * FRONT > 0 and 3.0 < abs(x) < 17.0:
            s = sternum(z)
            if s is not None and y * FRONT > s + 1.0:
                side = 1.0 if abs(x) < 12 else max(0.0, (17 - abs(x)) / 5)
                v.co.y = FRONT * (s + (y * FRONT - s) * (1 - CHEST_PULL * w * side))
        w = window(z, *HIP_Z)
        if w: v.co.x = x * (1 - (1 - HIP_SCALE) * w); x = v.co.x
        w = window(z, *WAIST_Z)
        if w: v.co.x = x * (1 - (1 - WAIST_SCALE) * w); x = v.co.x
        w = window(z, *SHOULDER_Z)
        if w and abs(x) > 8: v.co.x = x * (1 + (SHOULDER_SCALE - 1) * w)
    me.data.update()
print("reshaped", [m.name for m in meshes])

bpy.ops.object.select_all(action="DESELECT")
for m in meshes: m.select_set(True)
arm.select_set(True); bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.fbx(filepath=DST, use_selection=True, object_types={"ARMATURE", "MESH", "EMPTY"},
                         add_leaf_bones=False, use_armature_deform_only=True, bake_anim=False)
print("exported", DST)

# verification renders, skin-toned
scene = bpy.context.scene
for cand in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
    if cand in [i.identifier for i in scene.render.bl_rna.properties["engine"].enum_items]:
        scene.render.engine = cand; break
scene.render.resolution_x, scene.render.resolution_y = 700, 1100
scene.world = scene.world or bpy.data.worlds.new("W"); scene.world.use_nodes = True
next(n for n in scene.world.node_tree.nodes if n.type == "BACKGROUND").inputs["Color"].default_value = (0.72, 0.75, 0.8, 1)
mat = bpy.data.materials.new("Skin"); mat.use_nodes = True
next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED").inputs["Base Color"].default_value = (0.85, 0.68, 0.58, 1)
lod0 = next(m for m in meshes if m.name.endswith("_LOD0"))
for m in meshes: m.hide_render = m is not lod0
lod0.data.materials.clear(); lod0.data.materials.append(mat)
sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN")); sun.data.energy = 3
bpy.context.collection.objects.link(sun); sun.rotation_euler = (math.radians(55), 0, math.radians(35))
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam")); bpy.context.collection.objects.link(cam); scene.camera = cam
target = Vector((0, 0, 1.0))
for name, loc in (("body_male_front.png", Vector((0, FRONT * 3.2, 1.0))), ("body_male_side.png", Vector((3.2, 0, 1.0)))):
    cam.location = loc; cam.rotation_euler = (target - loc).to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.join(REPO, "unreal/assets", name); bpy.ops.render.render(write_still=True)
print("rendered")
