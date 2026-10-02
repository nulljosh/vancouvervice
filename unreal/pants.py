"""Build dark grey jeans that fit Joshua's MetaHuman body and skin to the same armature.
Headless: /Applications/Blender.app/Contents/MacOS/Blender -b --python unreal/pants.py
Reads unreal/assets/joshua_body.fbx, writes unreal/assets/pants.fbx plus front/side
verification renders. Everything below is in the body's own local space (cm), same as the
source FBX bone rest positions -- object world matrices carry the cm to m scale, so mesh
vertex coords and armature bone head_local/tail_local numbers are directly comparable.
"""
import bpy, bmesh, math, os
import numpy as np
from mathutils import Vector, kdtree

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BODY_FBX = os.path.join(REPO, "unreal/assets/joshua_body_v3.fbx")
PANTS_FBX = os.path.join(REPO, "unreal/assets/pants.fbx")
OUT_FRONT = os.path.join(REPO, "unreal/assets/pants_front.png")
OUT_SIDE = os.path.join(REPO, "unreal/assets/pants_side.png")

# ---- tunables (cm, body local space) --------------------------------------------------
HIP_HALF = 21.0              # cm either side of centre; wider than this is a hand
WAIST_Z = 100.0               # hip line in body space (the body sits taller than the rig), tucked under the polo hem
ANKLE_Z = -5.0                # cut at ankle, extends below Z=0
THIGH_RADIUS = 18.5          # max dist from thigh bone axis kept as "leg"
CALF_RADIUS = 14.5           # max dist from calf bone axis kept as "leg"
CLOTH_OFFSET = 3.0           # cm, offset outward along normal for cloth ease/thickness
FRONT_SIGN = -1.0            # -Y is front (checked against renders below)

# ---------------------------------------------------------------------------------------
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=BODY_FBX)

arm = bpy.data.objects["root"]
# cuts follow the rig, so a rebuilt body keeps the fit
_B = arm.data.bones
WAIST_Z = _B["pelvis"].head_local.z + 10.0
ANKLE_Z = _B["foot_l"].head_local.z - 13.0
body = next(o for o in bpy.data.objects if o.type == "MESH" and o.name.endswith("_LOD1"))  # export names vary

# "SKM_Joshua_BodyMesh" is a wrapper empty carrying the cm to m (0.01) scale; "root" (the
# armature) is parented to it. Bake that scale onto the armature itself and drop the
# wrapper, so the exported hierarchy is a clean armature+mesh with no parent empty.
wrapper = bpy.data.objects.get("SKM_Joshua_BodyMesh")
if wrapper:
    bpy.ops.object.select_all(action="DESELECT")
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")

# drop the other LODs and empties, keep the scene clean for render + export
for name in ["SKM_Joshua_BodyMesh_LOD0", "SKM_Joshua_BodyMesh_LOD2", "SKM_Joshua_BodyMesh_LOD3",
             "SKM_Joshua_BodyMesh", "SKM_Joshua_BodyMesh_LodGroup"]:
    o = bpy.data.objects.get(name)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)

bones = arm.data.bones
def bpos(name, which="head"):
    b = bones[name]
    return (b.head_local if which == "head" else b.tail_local).copy()

# leg bones: thigh and calf on each side
thigh_l_head = bpos("thigh_l", "head")
thigh_l_tail = bpos("thigh_l", "tail")
calf_l_head = bpos("calf_l", "head")
calf_l_tail = bpos("calf_l", "tail")

thigh_r_head = bpos("thigh_r", "head")
thigh_r_tail = bpos("thigh_r", "tail")
calf_r_head = bpos("calf_r", "head")
calf_r_tail = bpos("calf_r", "tail")

def segment_test(co, head, tail, radius, z_min, z_max):
    """Test if vertex belongs to a bone segment, within Z range and distance."""
    if co.z < z_min or co.z > z_max:
        return False
    axis = tail - head
    L = axis.length
    if L < 1e-6:
        return False
    t = (co - head).dot(axis) / (L * L)
    if t < -0.25 or t > 1.25:
        return False
    closest = head + axis * max(0.0, min(1.0, t))
    return (co - closest).length <= radius

def keep_test(co):
    """Keep every body vertex in the waist-to-ankle band. ponytail: a height band beats bone-radius tests here,
    the body mesh is wider than the rig's bone radii and a radius cut left garters, not jeans (2026-10-01)."""
    # ponytail: hands hang at hip height in the bind pose, so a plain height band grabbed them as mitts (2026-10-01).
    # Legs never leave the hip width; anything wider is an arm or a hand.
    return ANKLE_Z <= co.z <= WAIST_Z and abs(co.x) <= HIP_HALF
    # thigh: full range
    if segment_test(co, thigh_l_head, thigh_l_tail, THIGH_RADIUS, ANKLE_Z, WAIST_Z):
        return True
    if segment_test(co, thigh_r_head, thigh_r_tail, THIGH_RADIUS, ANKLE_Z, WAIST_Z):
        return True
    # calf: full range
    if segment_test(co, calf_l_head, calf_l_tail, CALF_RADIUS, ANKLE_Z, WAIST_Z):
        return True
    if segment_test(co, calf_r_head, calf_r_tail, CALF_RADIUS, ANKLE_Z, WAIST_Z):
        return True
    return False

# ---- duplicate body to Pants shell, keep only the leg region ----------------------------
bpy.ops.object.select_all(action="DESELECT")
body.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.duplicate()
pants = bpy.context.active_object
pants.name = "Pants"
pants.data.name = "Pants"

bm = bmesh.new()
bm.from_mesh(pants.data)
bm.verts.ensure_lookup_table()
to_delete = [v for v in bm.verts if not keep_test(v.co)]
bmesh.ops.delete(bm, geom=to_delete, context="VERTS")
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
bm.normal_update()

# ---- offset outward along vertex normal for cloth thickness ---------------------------
for v in bm.verts:
    v.co += v.normal * CLOTH_OFFSET

bm.normal_update()
bm.to_mesh(pants.data)
bm.free()
pants.data.update()

# ---- material: dark grey denim -------------------------------------------------------
mat = bpy.data.materials.new("Jeans")
mat.use_nodes = True
bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
bsdf.inputs["Base Color"].default_value = (0.05, 0.055, 0.065, 1.0)
bsdf.inputs["Roughness"].default_value = 0.75
pants.data.materials.clear()
pants.data.materials.append(mat)

# ---- smooth: subdivide once and apply so it reads as fabric, not skin -----------------
subsurf = pants.modifiers.new("Smooth", type="SUBSURF")
subsurf.levels = 1
subsurf.render_levels = 1
bpy.context.view_layer.objects.active = pants
bpy.ops.object.modifier_apply(modifier=subsurf.name)
bpy.ops.object.shade_smooth()

# ---- skin to the SAME armature: bake weights from the REAL posed surface ---------------
# Same strategy as polo: track surface motion via Surface Deform, then solve per-vertex
# bone weights by least squares to reproduce those tracked positions under actual poses.

body_vertex_weights = [{g.group: g.weight for g in v.groups} for v in body.data.vertices]
body_group_names = [vg.name for vg in body.vertex_groups]
for name in body_group_names:
    pants.vertex_groups.new(name=name)

body_kd = kdtree.KDTree(len(body.data.vertices))
for idx, v in enumerate(body.data.vertices):
    body_kd.insert(v.co, idx)
body_kd.balance()

K_NEIGHBORS = 16
candidates = []
for v in pants.data.vertices:
    prior = {}
    wsum = 0.0
    for co, idx, dist in body_kd.find_n(v.co, K_NEIGHBORS):
        w = 1.0 / (dist + 0.1)
        wsum += w
        for gidx, gw in body_vertex_weights[idx].items():
            prior[gidx] = prior.get(gidx, 0.0) + w * gw
    if wsum > 1e-8:
        prior = {g: w / wsum for g, w in prior.items()}
    candidates.append(prior)

pants.parent = body.parent
pants.matrix_parent_inverse = body.matrix_parent_inverse.copy()

def set_pose(bone_rotations):
    """Zero every pose bone, then apply the given {bone_name: (x,y,z) degrees} on top."""
    bpy.ops.object.select_all(action="DESELECT")
    arm.select_set(True)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="POSE")
    for pb in arm.pose.bones:
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = (0.0, 0.0, 0.0)
    for name, deg in bone_rotations.items():
        pb = arm.pose.bones[name]
        pb.rotation_mode = "XYZ"
        pb.rotation_euler = tuple(math.radians(d) for d in deg)
    bpy.context.view_layer.update()
    bpy.ops.object.mode_set(mode="OBJECT")

# sample poses to fit against: rest plus leg/hip rotations
SAMPLE_POSES = [
    ("rest", {}),
    ("l30", {"thigh_l": (30.0, 0.0, 0.0)}),
    ("l60", {"thigh_l": (60.0, 0.0, 0.0)}),
    ("r30", {"thigh_r": (30.0, 0.0, 0.0)}),
    ("r60", {"thigh_r": (60.0, 0.0, 0.0)}),
]

sdmod = pants.modifiers.new("SurfaceBind", type="SURFACE_DEFORM")
sdmod.target = body
set_pose({})
bpy.ops.object.select_all(action="DESELECT")
pants.select_set(True)
bpy.context.view_layer.objects.active = pants
bpy.ops.object.surfacedeform_bind(modifier=sdmod.name)
print("surface deform bound:", sdmod.is_bound)

target_positions = {}
bone_matrices = {}
for pose_name, rot in SAMPLE_POSES:
    set_pose(rot)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    pants_eval = pants.evaluated_get(depsgraph)
    mesh_eval = pants_eval.to_mesh()
    target_positions[pose_name] = [v.co.copy() for v in mesh_eval.vertices]
    pants_eval.to_mesh_clear()

    mats = {}
    for gidx, name in enumerate(body_group_names):
        pb = arm.pose.bones.get(name)
        b = arm.data.bones.get(name)
        if pb is None or b is None:
            continue
        M = np.array(pb.matrix @ b.matrix_local.inverted())
        mats[gidx] = (M[:3, :3], M[:3, 3])
    bone_matrices[pose_name] = mats

set_pose({})
pants.modifiers.remove(sdmod)

# solve each vertex's bone weights
LAMBDA = 0.3
fit_errors = []
for i in range(len(pants.data.vertices)):
    prior = candidates[i]
    cand = sorted(g for g in prior if any(g in bone_matrices[p] for p, _ in SAMPLE_POSES))
    if not cand:
        continue
    v0 = np.array(pants.data.vertices[i].co)
    w0 = np.array([prior[g] for g in cand])
    rows, targets = [], []
    for pose_name, _ in SAMPLE_POSES:
        mats = bone_matrices[pose_name]
        cols = []
        for g in cand:
            R, T = mats.get(g, (np.eye(3), np.zeros(3)))
            cols.append(R @ v0 + T)
        rows.append(np.stack(cols, axis=1))
        targets.append(np.array(target_positions[pose_name][i]))
    A = np.vstack(rows)
    t = np.concatenate(targets)
    K = len(cand)
    AtA = A.T @ A + LAMBDA * np.eye(K)
    Atb = A.T @ t + LAMBDA * w0
    w = np.linalg.solve(AtA, Atb)
    w = np.clip(w, 0.0, None)
    total = w.sum()
    if total <= 1e-8:
        continue
    w = w / total
    fit_errors.append(float(np.abs(A @ w - t).mean()))
    for g, wg in zip(cand, w):
        if wg > 1e-4:
            pants.vertex_groups[body_group_names[g]].add([i], float(wg), "REPLACE")

print("weight-fit mean residual (cm):", sum(fit_errors) / max(1, len(fit_errors)))

armmod = pants.modifiers.new("root", type="ARMATURE")
armmod.object = arm
armmod.use_vertex_groups = True
armmod.use_deform_preserve_volume = False

print("pants verts:", len(pants.data.vertices), "vgroups:", len(pants.vertex_groups))

# ---- render setup ------------------------------------------------------------------
skin_mat = bpy.data.materials.new("SkinPreview")
skin_mat.use_nodes = True
skin_bsdf = next(n for n in skin_mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
skin_bsdf.inputs["Base Color"].default_value = (0.75, 0.57, 0.48, 1.0)
skin_bsdf.inputs["Roughness"].default_value = 0.6
body.data.materials.clear()
body.data.materials.append(skin_mat)

scene = bpy.context.scene
engine_items = [i.identifier for i in scene.render.bl_rna.properties["engine"].enum_items]
for cand in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
    if cand in engine_items:
        scene.render.engine = cand
        break
scene.render.resolution_x = 900
scene.render.resolution_y = 1200
scene.render.film_transparent = False
if hasattr(scene, "world") and scene.world is None:
    scene.world = bpy.data.worlds.new("World")
scene.world.use_nodes = True
bg = next(n for n in scene.world.node_tree.nodes if n.type == "BACKGROUND")
bg.inputs["Color"].default_value = (0.72, 0.75, 0.8, 1.0)
bg.inputs["Strength"].default_value = 1.1

sun_data = bpy.data.lights.new("Sun", type="SUN")
sun_data.energy = 3.0
sun = bpy.data.objects.new("Sun", sun_data)
bpy.context.collection.objects.link(sun)
sun.rotation_euler = (math.radians(55), 0, math.radians(35))

fill_data = bpy.data.lights.new("Fill", type="SUN")
fill_data.energy = 1.2
fill = bpy.data.objects.new("Fill", fill_data)
bpy.context.collection.objects.link(fill)
fill.rotation_euler = (math.radians(60), 0, math.radians(-140))

cam_data = bpy.data.cameras.new("Cam")
cam_data.lens = 50
cam = bpy.data.objects.new("Cam", cam_data)
bpy.context.collection.objects.link(cam)
scene.camera = cam

target = Vector((0, 0, 1.05))

def point_camera(loc):
    cam.location = loc
    direction = target - loc
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

def render(path):
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("rendered", path)

point_camera(Vector((0, FRONT_SIGN * 1.7, 1.05)))
render(OUT_FRONT)

point_camera(Vector((1.7, 0, 1.05)))
render(OUT_SIDE)

set_pose({})

# ---- export skeletal mesh (armature + pants, deform bones only, no leaf bones) --------
bpy.ops.object.mode_set(mode="OBJECT")
bpy.ops.object.select_all(action="DESELECT")
arm.select_set(True)
pants.select_set(True)
bpy.context.view_layer.objects.active = pants

bpy.ops.export_scene.fbx(
    filepath=PANTS_FBX,
    use_selection=True,
    object_types={"ARMATURE", "MESH"},
    add_leaf_bones=False,
    use_armature_deform_only=True,
    bake_anim=False,
    mesh_smooth_type="FACE",
    use_mesh_modifiers=True,
)
print("exported", PANTS_FBX)
