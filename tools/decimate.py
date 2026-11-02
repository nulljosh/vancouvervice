# blender -b --factory-startup --python decimate.py -- in.glb out.glb target_tris
import bpy, sys
a = sys.argv[sys.argv.index('--') + 1:]
src, dst, target = a[0], a[1], int(a[2])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
for o in [o for o in bpy.context.scene.objects if o.type == 'MESH']:
    tris = sum(len(p.vertices) - 2 for p in o.data.polygons)
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    # weld the per-triangle UV islands' duplicate positions first, or collapse has nothing to merge
    bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.mesh.remove_doubles(threshold=1e-5); bpy.ops.object.mode_set(mode='OBJECT')
    m = o.modifiers.new('dec', 'DECIMATE'); m.decimate_type = 'COLLAPSE'; m.ratio = min(1, target / max(tris, 1)); m.use_collapse_triangulate = True
    bpy.ops.object.modifier_apply(modifier='dec')
    for p in o.data.polygons: p.use_smooth = True
    print('tris', tris, '->', sum(len(p.vertices) - 2 for p in o.data.polygons))
bpy.ops.export_scene.gltf(filepath=dst, export_format='GLB', export_image_format='JPEG', export_jpeg_quality=85)
