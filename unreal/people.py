# Spawns BP_Pedestrian actors on /tmp/vv_qa/people.json (tools/ue_people.py), each a random crowd model playing its walk.
import json, random
EAS = unreal.EditorActorSubsystem(); Z = -6840; random.seed(9)
for a in EAS.get_all_level_actors():
    if a.get_actor_label().startswith("Person_"): EAS.destroy_actor(a)
cls = unreal.load_asset("/Game/VancouverVice/BP_Pedestrian").generated_class(); ar = unreal.AssetRegistryHelpers.get_asset_registry()
A = {str(x.asset_name): str(x.package_name) for x in ar.get_assets_by_path("/Game/VancouverVice/People", True)}
kinds = [(unreal.load_asset(A[n]), unreal.load_asset(A[n + "walk"])) for n in A if n + "walk" in A]
for i, r in enumerate(json.load(open("/tmp/vv_qa/people.json"))):
    pts = [unreal.Vector(x * 100, y * 100, Z) for x, y in r["pts"]]; s = r["start"]; mesh, walk = random.choice(kinds)
    a = EAS.spawn_actor_from_class(cls, pts[s]); a.set_actor_label("Person_%03d" % i); a.set_folder_path("People")
    a.set_editor_property("Points", pts); a.set_editor_property("Index", (s + 1) % len(pts)); a.set_editor_property("Speed", r["speed"])
    b = a.get_component_by_class(unreal.SkeletalMeshComponent); b.set_skeletal_mesh_asset(mesh)
    b.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
    b.set_editor_property("animation_data", unreal.SingleAnimationPlayData(anim_to_play=walk, saved_looping=True, saved_playing=True, saved_play_rate=r["speed"] / 140))
print("people", i + 1, "kinds", len(kinds))
