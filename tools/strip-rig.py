# Blender -b --factory-startup --python tools/strip-rig.py -- in.glb out.glb: plain mesh in bind pose, no armature, no clips, for the Higgsfield rigger
import bpy, sys
i, o = sys.argv[sys.argv.index('--') + 1:]
bpy.ops.wm.read_factory_settings(use_empty=True); bpy.ops.import_scene.gltf(filepath=i)
for ob in list(bpy.data.objects):
    if ob.type == 'MESH':
        for m in list(ob.modifiers): ob.modifiers.remove(m)
        mw = ob.matrix_world.copy(); ob.parent = None; ob.matrix_world = mw
for ob in [o for o in bpy.data.objects if o.type != 'MESH' or o.name.startswith('Icosphere')]: bpy.data.objects.remove(ob)
for a in list(bpy.data.actions): bpy.data.actions.remove(a)
bpy.ops.export_scene.gltf(filepath=o, export_animations=False, export_skins=False)
print('stripped', [ (ob.name, tuple(round(x,2) for x in ob.dimensions)) for ob in bpy.data.objects])
