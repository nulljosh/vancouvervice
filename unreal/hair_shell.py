"""Short curly strawberry-blond hair as a skinned shell grown off Joshua's scalp.
Headless: /Applications/Blender.app/Contents/MacOS/Blender -b --python unreal/hair_shell.py
Reads unreal/assets/joshua_face_v2.fbx, writes unreal/assets/hair.fbx plus hair_front.png and hair_side.png.
Why a shell: the MetaHuman groom bindings crash HairStrands on the scanned face, an unbound groom never renders in Play,
and the groom's card mesh needs groom-only textures to show. A shell skinned to the face skeleton follows the head
through leader pose like the clothes do, and costs almost nothing.
"""
import bpy, bmesh, math, os
from mathutils import Vector, noise

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACE_FBX = os.path.join(REPO, "unreal/assets/joshua_face_v2.fbx")
HAIR_FBX = os.path.join(REPO, "unreal/assets/hair.fbx")
FRONT_SIGN = -1.0           # -Y is the face side, same as polo.py
FRONT_DROP = 0.060          # m below the crown the hairline sits at the forehead
BACK_DROP = 0.165           # m below the crown it reaches at the nape
LIFT = 0.012                # m the shell sits off the scalp
CURL = 0.018                # m of curl noise on top of that
CURL_SCALE = 55.0           # noise frequency per metre; higher is tighter curls
COLOR = (0.62, 0.26, 0.09, 1.0)   # strawberry blond from the scan video

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=FACE_FBX)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
face = bpy.data.objects["SKM_Joshua_FaceMesh_LOD0"]
for o in list(bpy.data.objects):
    if o.type == "MESH" and o is not face:
        bpy.data.objects.remove(o)

mw = face.matrix_world
# the FBX export reorders material slots (names no longer match faces), so skin = the biggest face group
from collections import Counter
skin = {Counter(p.material_index for p in face.data.polygons).most_common(1)[0][0]}
ws = [mw @ v.co for v in face.data.vertices]
zmax = max(w.z for w in ws)
ys = [w.y for w in ws]
ymin, ymax = min(ys), max(ys)

def scalp(w):
    back = (w.y - ymin) / (ymax - ymin) if FRONT_SIGN < 0 else (ymax - w.y) / (ymax - ymin)   # 0 at the face, 1 at the nape
    drop = FRONT_DROP + (BACK_DROP - FRONT_DROP) * max(0.0, min(1.0, (back - 0.25) / 0.6))
    return w.z > zmax - drop

hair = face.copy(); hair.data = face.data.copy(); hair.name = "Hair"
bpy.context.collection.objects.link(hair)
bm = bmesh.new(); bm.from_mesh(hair.data)
bm.verts.ensure_lookup_table()
kill = [f for f in bm.faces if f.material_index not in skin or not all(scalp(mw @ v.co) for v in f.verts)]
bmesh.ops.delete(bm, geom=kill, context="FACES")
bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=2, use_grid_fill=True)
bm.normal_update()
inv = mw.inverted()
scale = (inv.to_3x3() @ Vector((0, 0, 1))).length          # world metres to mesh units
for v in bm.verts:
    w = mw @ v.co
    n = noise.noise(w * CURL_SCALE)                          # -1..1
    v.co = v.co + v.normal * (LIFT + CURL * (0.5 + 0.5 * n)) * scale
bm.to_mesh(hair.data); bm.free()
mat = bpy.data.materials.new("M_HairGinger"); mat.use_nodes = True
bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
bsdf.inputs["Base Color"].default_value = COLOR; bsdf.inputs["Roughness"].default_value = 0.75
hair.data.materials.clear(); hair.data.materials.append(mat)
print("hair verts", len(hair.data.vertices))

bpy.ops.object.select_all(action="DESELECT")
hair.select_set(True); arm.select_set(True); bpy.context.view_layer.objects.active = arm
bpy.ops.export_scene.fbx(filepath=HAIR_FBX, use_selection=True, object_types={"ARMATURE", "MESH"},
                         add_leaf_bones=False, use_armature_deform_only=True, bake_anim=False)
print("exported", HAIR_FBX)

# verification renders: face + hair
scene = bpy.context.scene
for cand in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
    if cand in [i.identifier for i in scene.render.bl_rna.properties["engine"].enum_items]:
        scene.render.engine = cand; break
scene.render.resolution_x = scene.render.resolution_y = 800
scene.world = scene.world or bpy.data.worlds.new("W"); scene.world.use_nodes = True
next(n for n in scene.world.node_tree.nodes if n.type == "BACKGROUND").inputs["Color"].default_value = (0.72, 0.75, 0.8, 1)
sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN")); sun.data.energy = 3
bpy.context.collection.objects.link(sun); sun.rotation_euler = (math.radians(50), 0, math.radians(30))
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam")); bpy.context.collection.objects.link(cam); scene.camera = cam
centre = sum((mw @ v.co for v in face.data.vertices), Vector()) / len(face.data.vertices)
for name, off in (("hair_front.png", Vector((0, FRONT_SIGN * 0.6, 0.02))), ("hair_side.png", Vector((0.6, 0, 0.02)))):
    cam.location = centre + off
    cam.rotation_euler = (centre - cam.location).to_track_quat("-Z", "Y").to_euler()
    scene.render.filepath = os.path.join(REPO, "unreal/assets", name)
    bpy.ops.render.render(write_still=True)
print("rendered")
