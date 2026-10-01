# Run in the editor: python3 unreal/qa.py "$(cat unreal/hair_install.py)". Curly ginger hair on the player, bound to the Face mesh.
# Uses the MetaHuman plugin's Hair_L_AfroCurly groom and its binding; a GroomComponent under Face follows the head bone on its own.
import unreal
bp=unreal.load_asset("/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter")
sds=unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
GROOM="/MetaHumanCharacter/Optional/Grooms/GroomAssets/Hair/Hair_L_AfroCurly/Hair_L_AfroCurly"
BIND="/MetaHumanCharacter/Optional/Grooms/Bindings/Hair/Hair_L_AfroCurly_Binding"
def comps():
    out={}
    for h in sds.k2_gather_subobject_data_for_blueprint(bp):
        o=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
        if o: out[o.get_name()]=(o,h)
    return out
C=comps()
if "Hair_GEN_VARIABLE" in C:
    comp=C["Hair_GEN_VARIABLE"][0]
else:
    face_h=C["Face_GEN_VARIABLE"][1]
    h,fail=sds.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=face_h, new_class=unreal.GroomComponent, blueprint_context=bp))
    print("add:", fail)
    sds.rename_subobject(h, unreal.Text("Hair"))
    comp=unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
comp.set_editor_property("groom_asset", unreal.load_asset(GROOM))
# ponytail: no binding. Hair_L_AfroCurly_Binding targets the stock MetaHuman face; on the scanned face it asserts in
# HairStrands DeformedRootResource and segfaults the editor (2026-10-01). Attach to the head socket instead.
comp.set_editor_property("binding_asset", None)
comp.set_editor_property("attach_socket_name", "head")
# ginger: the groom material exposes HairMelanin/HairRedness style params on MetaHuman grooms; set what exists
mats=comp.get_materials()
print("hair materials", [m.get_name() if m else None for m in mats])
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
print(unreal.EditorAssetLibrary.save_loaded_asset(bp, False), comp.get_name(), comp.get_attach_parent().get_name() if comp.get_attach_parent() else None)
