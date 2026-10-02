# Run in the editor: python3 unreal/qa.py "$(cat unreal/body_fix.py)".
# 1. The hidden leader mannequin was SKM_Quinn_Simple (Epic's female mannequin), so Body, Polo and Pants took her hip
#    and chest proportions through leader pose. Swap it to SKM_Manny_Simple.
# 2. Hair as the groom's own card mesh (a static mesh) on the Face head bone: strands never rendered in Play
#    without a binding, and the bindings crash on the scanned face. Cards are cheaper on RAM too.
import unreal
bp = unreal.load_asset("/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter")
sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
G = "/MetaHumanCharacter/Optional/Grooms/GroomAssets/Hair/Hair_S_Messy/"
def comps():
    out = {}
    for h in sds.k2_gather_subobject_data_for_blueprint(bp):
        o = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
        if o: out[o.get_name()] = (o, h)
    return out
C = comps()
C["CharacterMesh0"][0].set_editor_property("skinned_asset", unreal.load_asset("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple"))
if "HairCards_GEN_VARIABLE" in C:
    cards = C["HairCards_GEN_VARIABLE"][0]
else:
    h, fail = sds.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=C["Face_GEN_VARIABLE"][1], new_class=unreal.StaticMeshComponent, blueprint_context=bp))
    sds.rename_subobject(h, unreal.Text("HairCards"))
    cards = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
cards.set_editor_property("static_mesh", unreal.load_asset(G + "Hair_S_Messy_CardsMesh_Group0_LOD0"))
cards.set_editor_property("override_materials", [unreal.load_asset("/Game/VancouverVice/Joshua/Hair/MI_Ginger_MI_Hair_Cards")])
cards.set_editor_property("cast_shadow", True)
if "Hair_GEN_VARIABLE" in C:  # strands off; keep the component so the construction script still compiles
    C["Hair_GEN_VARIABLE"][0].set_editor_property("visible", False)
unreal.BlueprintEditorLibrary.compile_blueprint(bp)
print("saved", unreal.EditorAssetLibrary.save_loaded_asset(bp, False), "leader", C["CharacterMesh0"][0].get_editor_property("skinned_asset").get_name(), "cards", cards.get_editor_property("static_mesh").get_name())
