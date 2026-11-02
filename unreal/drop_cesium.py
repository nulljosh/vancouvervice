"""Remove every Cesium actor from the open level and save it. Our own city replaced the Google tiles.
Run: python3 unreal/qa.py "$(cat unreal/drop_cesium.py)", then quit the editor and set CesiumForUnreal
"Enabled": false in VancouverVice.uproject so the plugin stops compiling into every build."""
import unreal

EAS = unreal.EditorActorSubsystem(); gone = []
for a in EAS.get_all_level_actors():
    if a.get_class().get_name().startswith("Cesium"): gone.append(a.get_class().get_name()); EAS.destroy_actor(a)
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
print("CESIUM removed", len(gone), sorted(set(gone)))
