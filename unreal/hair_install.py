# Run in the editor: python3 unreal/qa.py "$(cat unreal/hair_install.py)". Short strawberry-blond curls on the player.
# Groom: the MetaHuman plugin's Hair_S_Messy, no binding (the plugin binding targets the stock face and segfaults
# HairStrands on the scanned face, 2026-10-01). It hangs off the Mesh "head" socket like the glasses do, with the
# same face-space offset, so it follows the head bone in Play.
import unreal
bp=unreal.load_asset("/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter")
sds=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
GROOM="/MetaHumanCharacter/Optional/Grooms/GroomAssets/Hair/Hair_S_Messy/Hair_S_Messy"
MELANIN, REDNESS = 0.22, 1.0   # strawberry blond, from the scan video
def comps():
    out={}
    for h in sds.k2_gather_subobject_data_for_blueprint(bp):
        o=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
        if o: out[o.get_name()]=(o,h)
    return out
C=comps()
if "Hair_GEN_VARIABLE" in C:
    comp,h=C["Hair_GEN_VARIABLE"]
    sds.attach_subobject(C["CharacterMesh0"][1], h)
else:
    h,fail=sds.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=C["CharacterMesh0"][1], new_class=unreal.GroomComponent, blueprint_context=bp))
    print("add:", fail); sds.rename_subobject(h, unreal.Text("Hair"))
    comp=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
comp.set_editor_property("groom_asset", unreal.load_asset(GROOM))
comp.set_editor_property("binding_asset", None)
# same offset the glasses use: inverse of the face head bone ref pose, under the Mesh "head" socket
# measured offset of the Mesh head socket in face-mesh space (same as glasses_install.py, stable across rebuilds)
class R: translation=unreal.Vector(-154.66,-0.85,0.0); rotation=unreal.Rotator(roll=0,pitch=0,yaw=-90).quaternion()
# the head socket itself is set by the construction script (Python can't set a socket on a Blueprint component); see hair.dsl
comp.set_editor_property('relative_location', R.translation); comp.set_editor_property('relative_rotation', R.rotation.rotator())
# ginger material instances, one per slot
P="/Game/VancouverVice/Joshua/Hair/"; at=unreal.AssetToolsHelpers.get_asset_tools(); mel=unreal.MaterialEditingLibrary
over=[]
for i,m in enumerate(comp.get_materials()):
    name=f"MI_Ginger_{m.get_name()}"
    if unreal.EditorAssetLibrary.does_asset_exist(P+name): mi=unreal.load_asset(P+name)
    else:
        mi=at.create_asset(name, P[:-1], unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
        mel.set_material_instance_parent(mi, m)
    mel.set_material_instance_scalar_parameter_value(mi, "hairMelanin", MELANIN)
    mel.set_material_instance_scalar_parameter_value(mi, "hairRedness", REDNESS)
    mel.update_material_instance(mi); unreal.EditorAssetLibrary.save_loaded_asset(mi, False); over.append(mi)
comp.set_editor_property("override_materials", over)
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
print(unreal.EditorAssetLibrary.save_loaded_asset(bp, False), "parent", comp.get_attach_parent().get_name() if comp.get_attach_parent() else None, "rel", R.translation.to_tuple())
