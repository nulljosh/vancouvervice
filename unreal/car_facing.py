"""The sedan glb's nose points down -X, so BP_TrafficCar (and BP_CopCar, its copy) drove rear first. Turn the mesh
component 180 degrees in both Blueprints so the nose leads. Run once: python3 unreal/qa.py "$(cat unreal/car_facing.py)"."""
import unreal

EAL = unreal.EditorAssetLibrary; SDS = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
for path in ("/Game/VancouverVice/BP_TrafficCar", "/Game/VancouverVice/Cops/BP_CopCar"):
    bp = EAL.load_asset(path)
    for h in SDS.k2_gather_subobject_data_for_blueprint(bp):
        o = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(SDS.k2_find_subobject_data_from_handle(h))
        if isinstance(o, unreal.StaticMeshComponent) and o.get_editor_property("static_mesh") and "sedan" in o.get_editor_property("static_mesh").get_path_name():
            o.set_editor_property("relative_rotation", unreal.Rotator(roll=0, pitch=0, yaw=180))
            print("turned", path, o.get_name())
    unreal.BlueprintEditorLibrary.compile_blueprint(bp); EAL.save_loaded_asset(bp)
