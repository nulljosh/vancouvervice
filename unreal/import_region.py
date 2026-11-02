"""Import one Lower Mainland town (built by tools/ue_region.sh) and place it on the world, same as downtown:
z -6840, complex-as-simple double-sided collision, actors in the City/<Area> outliner folder.
Run: QA_TIMEOUT=1500 python3 unreal/qa.py "AREA='surrey'; $(cat unreal/import_region.py)"
One town per call keeps the editor's memory flat on the 16 GB Mac."""
import unreal

Z = -6840
SRC = "/Volumes/LaCie/Unreal/dl/region/%s.glb" % AREA
DST = "/Game/City/" + AREA.title()
EAS = unreal.EditorActorSubsystem()

t = unreal.AssetImportTask()
t.filename, t.destination_path, t.automated, t.save, t.replace_existing = SRC, DST, True, True, True
unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([t])

for a in EAS.get_all_level_actors():  # re-runs replace, never double
    if a.get_folder_path() == "City/" + AREA.title(): EAS.destroy_actor(a)
n = 0
for p in unreal.EditorAssetLibrary.list_assets(DST, True, False):
    if "/StaticMeshes/" not in p: continue
    m = unreal.load_asset(p.split(".")[0]); bs = m.get_editor_property("body_setup")
    bs.set_editor_property("collision_trace_flag", unreal.CollisionTraceFlag.CTF_USE_COMPLEX_AS_SIMPLE)
    bs.set_editor_property("double_sided_geometry", True)
    unreal.EditorAssetLibrary.save_loaded_asset(m, False)
    a = EAS.spawn_actor_from_object(m, unreal.Vector(0, 0, Z)); a.set_actor_label(m.get_name()); a.set_folder_path("City/" + AREA.title()); n += 1
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
print("REGION", AREA, "placed", n)
