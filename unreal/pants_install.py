# Run in the editor: python3 unreal/qa.py "$(cat unreal/pants_install.py)". Dark grey jeans on the player, following the body.
import unreal
bp=unreal.load_asset("/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter")
sds=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
COMPS={}
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
    if o: COMPS[o.get_name()]=o
at=unreal.AssetToolsHelpers.get_asset_tools(); mel=unreal.MaterialEditingLibrary
P="/Game/VancouverVice/Joshua/Pants/"
if unreal.EditorAssetLibrary.does_asset_exist(P+"M_JeansIndigo"):
    mat=unreal.load_asset(P+"M_JeansIndigo")
else:
    mat=at.create_asset("M_JeansIndigo", P[:-1], unreal.Material, unreal.MaterialFactoryNew())
    c=mel.create_material_expression(mat, unreal.MaterialExpressionConstant3Vector, -300, 0)
    c.set_editor_property("constant", unreal.LinearColor(0.02,0.03,0.07,1))
    mel.connect_material_property(c, "", unreal.MaterialProperty.MP_BASE_COLOR)
    r=mel.create_material_expression(mat, unreal.MaterialExpressionConstant, -300, 200); r.set_editor_property("r", 0.75)
    mel.connect_material_property(r, "", unreal.MaterialProperty.MP_ROUGHNESS)
    mel.recompile_material(mat); unreal.EditorAssetLibrary.save_loaded_asset(mat, False)
if "Pants_GEN_VARIABLE" in COMPS:
    comp=COMPS["Pants_GEN_VARIABLE"]
else:
    hs=sds.k2_gather_subobject_data_for_blueprint(bp)
    mesh_h=[h for h in hs if unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h)).get_name()=="CharacterMesh0"][0]
    h,fail=sds.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=mesh_h, new_class=unreal.SkeletalMeshComponent, blueprint_context=bp))
    print("add:", fail)
    sds.rename_subobject(h, unreal.Text("Pants"))
    comp=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
comp.set_editor_property("skinned_asset", unreal.load_asset(P+"SKM_Pants"))
comp.set_editor_property("override_materials", [mat])
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
print(unreal.EditorAssetLibrary.save_loaded_asset(bp, False), comp.get_name(), comp.get_attach_parent().get_name() if comp.get_attach_parent() else None)
