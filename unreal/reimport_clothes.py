# Run in the editor: python3 unreal/qa.py "$(cat unreal/reimport_clothes.py)". Reimports polo.fbx and pants.fbx over the
# existing skeletal meshes with the legacy FBX importer (Interchange rejects the Blender bind poses), onto the body skeleton.
import unreal
unreal.SystemLibrary.execute_console_command(None, "Interchange.FeatureFlags.Import.FBX 0")
skel = unreal.load_asset("/Game/VancouverVice/Joshua/Polo/SKM_Polo").skeleton
A = "/Users/joshua/Documents/Code/vancouvervice/unreal/assets/"
tasks = []
for fbx, dest, name in (("polo.fbx", "/Game/VancouverVice/Joshua/Polo", "SKM_Polo"), ("pants.fbx", "/Game/VancouverVice/Joshua/Pants", "SKM_Pants")):
    t = unreal.AssetImportTask(); t.filename = A + fbx; t.destination_path = dest; t.destination_name = name
    t.automated = True; t.replace_existing = True; t.save = True
    ui = unreal.FbxImportUI(); ui.import_mesh = True; ui.import_as_skeletal = True; ui.import_materials = False
    ui.import_textures = False; ui.import_animations = False; ui.skeleton = skel
    ui.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
    t.options = ui; tasks.append(t)
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
print("imported", [str(x) for t in tasks for x in t.imported_object_paths])
