import bpy, sys
src, out = sys.argv[-2], sys.argv[-1]
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=src)
for o in list(bpy.data.objects):
    if o.type == "MESH" and o.parent is None: bpy.data.objects.remove(o)
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE"); k = arm.scale[0]
meshes = [o for o in bpy.data.objects if o.type == "MESH"]
arm.data.pose_position = "REST"; bpy.context.view_layer.update(); dg = bpy.context.evaluated_depsgraph_get()
rest = {o.name: [o.matrix_world @ v.co for v in o.evaluated_get(dg).to_mesh().vertices] for o in meshes}  # world-space rest shape
for o in meshes: o.parent = None
bpy.ops.object.select_all(action="DESELECT"); arm.select_set(True); bpy.context.view_layer.objects.active = arm
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
for a in bpy.data.actions:
    for fc in (a.fcurves if hasattr(a, "fcurves") else [c for l in a.layers for s in l.strips for b in s.channelbags for c in b.fcurves]):
        if fc.data_path == "scale" or fc.data_path.endswith(".scale"):  # object or root bone keyed at 0.01 (cm rig) would shrink everything twice
            for kp in fc.keyframe_points:
                if abs(kp.co[1] - k) < k * .05: kp.co[1] = 1.0; kp.handle_left[1] = 1.0; kp.handle_right[1] = 1.0
        if fc.data_path == "location" or fc.data_path.endswith(".location"):
            for kp in fc.keyframe_points: kp.co[1] *= k; kp.handle_left[1] *= k; kp.handle_right[1] *= k
for o in meshes:
    o.matrix_world.identity()
    for v, p in zip(o.data.vertices, rest[o.name]): v.co = p
    o.parent = arm; o.matrix_parent_inverse.identity()
    for m in o.modifiers:
        if m.type == "ARMATURE": m.object = arm
arm.data.pose_position = "POSE"
for pb in arm.pose.bones:
    if abs(pb.scale[0] - k) < k * .05: pb.scale = (1, 1, 1)
print("SCALE", k, "MESHZ", [round(max(v.co.z for v in o.data.vertices), 3) for o in meshes], "BONEZ", round(max(b.head_local.z for b in arm.data.bones), 3))
bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", export_animations=True, export_animation_mode="ACTIONS", export_image_format="AUTO")
