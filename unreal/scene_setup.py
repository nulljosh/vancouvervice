# Run in the editor: python3 unreal/qa.py "$(cat unreal/scene_setup.py)". Idempotent. Puts the level in its mission-one state:
# PlayerStart on the Georgia sidewalk outside the Pacific Centre Apple Store, a hidden catch pad under it (tile holes
# swallow the pawn), the PhotoCam facing the spawn, and Cesium memory caps. Lvl_ThirdPerson is World Partition, so every
# actor lives in its own external package: save_current_level() alone does not save them (they reverted on 2026-10-01).
import unreal, math
w = unreal.UnrealEditorSubsystem().get_editor_world()
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
SPAWN, YAW = unreal.Vector(-487.5, 2936.1, -6740.0), 134.7
touched = []
for a in eas.get_all_level_actors():
    if a.get_actor_label() in ("SpawnCatchPad", "PhotoCam", "FacePreview", "MHPreview") or "MetaHumanDefaultEditorPipelineActor" in a.get_name(): eas.destroy_actor(a)
ps = unreal.GameplayStatics.get_all_actors_of_class(w, unreal.PlayerStart)[0]
ps.set_actor_location_and_rotation(SPAWN, unreal.Rotator(roll=0, pitch=0, yaw=YAW), False, False); touched.append(ps)
pad = eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(SPAWN.x, SPAWN.y, -6852.0), unreal.Rotator(0, 0, 0))
pad.set_actor_label("SpawnCatchPad"); pad.static_mesh_component.set_static_mesh(unreal.load_asset("/Engine/BasicShapes/Cube.Cube"))
pad.set_actor_scale3d(unreal.Vector(40, 40, 0.2)); pad.set_actor_hidden_in_game(True); touched.append(pad)
f = unreal.Vector(math.cos(math.radians(YAW)), math.sin(math.radians(YAW)), 0)
feet = unreal.Vector(SPAWN.x, SPAWN.y, -6838.0)
loc, eye = feet + f * 420 + unreal.Vector(0, 0, 150), feet + unreal.Vector(0, 0, 105)
cam = eas.spawn_actor_from_class(unreal.CameraActor, loc, unreal.MathLibrary.find_look_at_rotation(loc, eye))
cam.set_actor_label("PhotoCam")
cc = cam.get_components_by_class(unreal.CameraComponent)[0]
cc.set_editor_property("field_of_view", 40.0); cc.set_editor_property("constrain_aspect_ratio", False); touched.append(cam)
t = unreal.GameplayStatics.get_actor_of_class(w, unreal.Cesium3DTileset)
t.set_editor_property("maximum_cached_bytes", 256 * 1024 * 1024); t.set_editor_property("maximum_simultaneous_tile_loads", 12)
t.set_editor_property("enforce_culled_screen_space_error", True); t.set_editor_property("culled_screen_space_error", 64.0); touched.append(t)
pk = [a.get_outermost() for a in touched]
print("saved actors", unreal.EditorLoadingAndSavingUtils.save_packages(pk, False), [p.get_name()[-40:] for p in pk])
print("level", unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level(), "dirty", unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True))
bp = unreal.load_asset("/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter")
unreal.BlueprintEditorLibrary.compile_blueprint(bp); print("bp", unreal.EditorAssetLibrary.save_loaded_asset(bp, False))
