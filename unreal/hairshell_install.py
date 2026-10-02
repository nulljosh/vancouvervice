# Run in the editor: python3 unreal/qa.py "$(cat unreal/hairshell_install.py)". Imports hair.fbx (unreal/hair_shell.py) onto
# the face skeleton and puts it on the player as HairShell, a SkeletalMeshComponent under Face that follows the
# mannequin through leader pose like Body, Face, Polo and Pants. Strand Hair and HairCards are hidden.
import unreal
unreal.SystemLibrary.execute_console_command(None, "Interchange.FeatureFlags.Import.FBX 0")
face = unreal.load_asset("/Game/Unpacked/Joshua/Joshua/Face/SKM_Joshua_FaceMesh")
D = "/Game/VancouverVice/Joshua/Hair"
t = unreal.AssetImportTask(); t.filename = "/Users/joshua/Documents/Code/vancouvervice/unreal/assets/hair.fbx"
t.destination_path = D; t.destination_name = "SKM_HairShell"; t.automated = True; t.replace_existing = True; t.save = True
ui = unreal.FbxImportUI(); ui.import_mesh = True; ui.import_as_skeletal = True; ui.import_materials = False
ui.import_textures = False; ui.import_animations = False; ui.skeleton = face.skeleton
ui.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH; t.options = ui
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])
mesh = unreal.load_asset(D + "/SKM_HairShell"); print("mesh", mesh)
mel = unreal.MaterialEditingLibrary
if unreal.EditorAssetLibrary.does_asset_exist(D + "/M_HairGinger"):
    mat = unreal.load_asset(D + "/M_HairGinger")
else:
    mat = unreal.AssetToolsHelpers.get_asset_tools().create_asset("M_HairGinger", D, unreal.Material, unreal.MaterialFactoryNew())
    c = mel.create_material_expression(mat, unreal.MaterialExpressionConstant3Vector, -300, 0)
    c.set_editor_property("constant", unreal.LinearColor(0.36, 0.11, 0.03, 1)); mel.connect_material_property(c, "", unreal.MaterialProperty.MP_BASE_COLOR)
    r = mel.create_material_expression(mat, unreal.MaterialExpressionConstant, -300, 200); r.set_editor_property("r", 0.7)
    mel.connect_material_property(r, "", unreal.MaterialProperty.MP_ROUGHNESS)
    mel.recompile_material(mat); unreal.EditorAssetLibrary.save_loaded_asset(mat, False)
bp = unreal.load_asset("/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter")
sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
C = {}
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
    if o: C[o.get_name()] = (o, h)
if "HairShell_GEN_VARIABLE" in C:
    comp = C["HairShell_GEN_VARIABLE"][0]
else:
    h, fail = sds.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=C["Face_GEN_VARIABLE"][1], new_class=unreal.SkeletalMeshComponent, blueprint_context=bp))
    sds.rename_subobject(h, unreal.Text("HairShell"))
    comp = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
comp.set_editor_property("skinned_asset", mesh); comp.set_editor_property("override_materials", [mat])
for n in ("Hair_GEN_VARIABLE", "HairCards_GEN_VARIABLE"):
    if n in C: C[n][0].set_editor_property("visible", False)
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
print("bp", unreal.EditorAssetLibrary.save_loaded_asset(bp, False))
