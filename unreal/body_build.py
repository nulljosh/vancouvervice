# Run in the editor: QA_TIMEOUT=900 python3 unreal/qa.py "$(cat unreal/body_build.py)". Rebuilds Joshua's MetaHuman body.
# Joshua, 2026-10-01: "give me a six pack and make me pretty athletically ripped. 6ft. 140lbs!"
# Constraints are MetaHuman body measurements in cm. Set, commit and build in ONE scoped call (splitting them across calls
# produced a no-op build on 2026-09-23, see UNREAL.md), then repoint Body and Face on the player, since every build
# leaves them on /Engine/Transient copies.
import unreal
from metahuman_character_test_utils import ScopedMetaHumanCharacterEditor
HEIGHT, CHEST, WAIST, HIP, MASC = 183.0, 92.0, 74.0, 88.0, -1.5   # 6 ft, 140 lb, lean and cut
mh = unreal.load_asset("/Game/Joshua")
sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
with ScopedMetaHumanCharacterEditor(character=mh):
    cons = sub.get_body_constraints(mh) if hasattr(sub, "get_body_constraints") else mh.get_editor_property("body_constraints")
    want = {"Height": HEIGHT, "Chest": CHEST, "Waist": WAIST, "Hip": HIP, "Masculine/Feminine": MASC}
    out = []
    for c in cons:
        n = str(c.get_editor_property("name")) if hasattr(c, "get_editor_property") else str(c)
        for k, v in want.items():
            if k.lower() in n.lower():
                c.set_editor_property("target_measurement", v); c.set_editor_property("is_active", True)
        out.append(c)
    sub.set_body_constraints(mh, out)
    sub.commit_body_state(mh, mh.get_editor_property("body_state") if hasattr(mh, "get_editor_property") else None) if False else None
    print("can build", sub.can_build_meta_human(mh))
    sub.build_meta_human(mh)
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
# repoint the player at the saved meshes
bp = unreal.load_asset("/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter")
sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
    if o and o.get_name() == "Body_GEN_VARIABLE": o.set_editor_property("skinned_asset", unreal.load_asset("/Game/Unpacked/Joshua/Body/SKM_Joshua_BodyMesh"))
    if o and o.get_name() == "Face_GEN_VARIABLE": o.set_editor_property("skinned_asset", unreal.load_asset("/Game/Unpacked/Joshua/Face/SKM_Joshua_FaceMesh"))
unreal.BlueprintEditorLibrary.compile_blueprint(bp); print("saved", unreal.EditorAssetLibrary.save_loaded_asset(bp, False))
