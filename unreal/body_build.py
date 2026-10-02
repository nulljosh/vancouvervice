# Run in the editor: QA_TIMEOUT=900 python3 unreal/qa.py "$(cat unreal/body_build.py)". Rebuilds Joshua's MetaHuman body.
# Joshua, 2026-10-01: "give me a six pack and make me pretty athletically ripped. 6ft. 140lbs!"
# Constraints are MetaHuman body measurements in cm. Set, commit and build in ONE scoped call (splitting them across calls
# produced a no-op build on 2026-09-23, see UNREAL.md), then repoint Body and Face on the player, since every build
# leaves them on /Engine/Transient copies.
# Empty build params assert OutFaceMesh && OutBodyMesh and crash the editor (2026-10-01): the build needs an output
# path and pipeline settings, and commit_body_state before it. Run on its own, nothing else open, 12 GB peak.
import unreal
from metahuman_character_test_utils import ScopedMetaHumanCharacterEditor
# exact constraint names; substring matching once set Shoulder Height to 183 and Neck to Waist to 74 (max 53) and the
# solver returned a mush (2026-10-01). Anything not listed is switched off so it can't fight these.
WANT = {"Height": 183.0, "Chest": 96.0, "Waist": 76.0, "Hip": 90.0, "Across Shoulder": 48.0,
        "Masculine/Feminine": 2.0, "Muscularity": 1.8, "Fat": -1.6}   # 6 ft, 140 lb, lean. Masculine/Feminine: +2 is masculine, checked in a live preview 2026-10-01 (every earlier build used -2 and came out female)
mh = unreal.load_asset("/Game/Joshua")
sub = unreal.get_editor_subsystem(unreal.MetaHumanCharacterEditorSubsystem)
with ScopedMetaHumanCharacterEditor(character=mh):
    cons = sub.get_body_constraints(mh)
    out = []
    for c in cons:
        n = str(c.get_editor_property("name"))
        if n in WANT:
            c.set_editor_property("target_measurement", WANT[n]); c.set_editor_property("is_active", True)
        else:
            c.set_editor_property("is_active", False)
        out.append(c)
    sub.set_body_constraints(mh, out)
    sub.commit_body_state(mh)
    print("can build", sub.can_build_meta_human(mh))
    params = unreal.MetaHumanCharacterEditorBuildParameters()
    params.pipeline_type = unreal.MetaHumanDefaultPipelineType.OPTIMIZED
    params.pipeline_quality = unreal.MetaHumanQualityLevel.MEDIUM
    params.absolute_build_path = "/Game/Unpacked/Joshua"
    params.common_folder_path = "/Game/Unpacked/Joshua/Common"
    sub.build_meta_human(mh, params)
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
# repoint the player at the saved meshes
bp = unreal.load_asset("/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter")
sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    o = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
    if o and o.get_name() == "Body_GEN_VARIABLE": o.set_editor_property("skinned_asset", unreal.load_asset("/Game/Unpacked/Joshua/Joshua/Body/SKM_Joshua_BodyMesh"))
    if o and o.get_name() == "Face_GEN_VARIABLE": o.set_editor_property("skinned_asset", unreal.load_asset("/Game/Unpacked/Joshua/Joshua/Face/SKM_Joshua_FaceMesh"))
unreal.BlueprintEditorLibrary.compile_blueprint(bp); print("saved", unreal.EditorAssetLibrary.save_loaded_asset(bp, False))
