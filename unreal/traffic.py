# Spawns BP_TrafficCar actors along /tmp/vv_qa/traffic.json (tools/ue_traffic.py), painted from the parked-car colours.
import json, random
EAS = unreal.EditorActorSubsystem(); Z = -6840; random.seed(5)
for a in EAS.get_all_level_actors():
    if a.get_actor_label().startswith("Traffic_"): EAS.destroy_actor(a)
cls = unreal.load_asset("/Game/VancouverVice/BP_TrafficCar").generated_class()
paints = [unreal.load_asset(p.split(".")[0]) for p in unreal.EditorAssetLibrary.list_assets("/Game/VancouverVice/Props/Paint", False, False) if "Sedans_" in p]
for i, r in enumerate(json.load(open("/tmp/vv_qa/traffic.json"))):
    pts = [unreal.Vector(x * 100, y * 100, Z) for x, y in r["pts"]]; s = r["start"]
    a = EAS.spawn_actor_from_class(cls, pts[s]); a.set_actor_label("Traffic_%02d" % i); a.set_folder_path("Traffic")
    a.set_editor_property("Points", pts); a.set_editor_property("Index", (s + 1) % len(pts)); a.set_editor_property("Speed", r["speed"])
    a.get_component_by_class(unreal.StaticMeshComponent).set_material(0, random.choice(paints))
print("traffic", i + 1)
