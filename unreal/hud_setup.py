"""HUD and minimap, no UMG: a top-down orthographic SceneCapture on the walker paints RT_Minimap (north up, so it
never spins), and BP_VVHud (a plain HUD Blueprint, graph in unreal/hud.dsl) draws it bottom-left with a player dot.
Run once: python3 unreal/qa.py "$(cat unreal/hud_setup.py)", then write unreal/hud.dsl into BP_VVHud's EventGraph."""
import unreal

AT = unreal.AssetToolsHelpers.get_asset_tools(); EAL = unreal.EditorAssetLibrary; D = "/Game/VancouverVice/HUD"

rt = EAL.load_asset(D + "/RT_Minimap") if EAL.does_asset_exist(D + "/RT_Minimap") else \
    AT.create_asset("RT_Minimap", D, unreal.TextureRenderTarget2D, unreal.TextureRenderTargetFactoryNew())
rt.set_editor_property("size_x", 512); rt.set_editor_property("size_y", 512)
EAL.save_loaded_asset(rt)

if not EAL.does_asset_exist(D + "/BP_VVHud"):
    f = unreal.BlueprintFactory(); f.set_editor_property("parent_class", unreal.HUD)
    AT.create_asset("BP_VVHud", D, unreal.Blueprint, f)
hud = EAL.load_asset(D + "/BP_VVHud"); EAL.save_loaded_asset(hud)

# The game mode's HUD class does not stick at runtime; BP_Missions BeginPlay calls ClientSetHUD(BP_VVHud) instead.

ch = EAL.load_asset("/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter")
SDS = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
handles = SDS.k2_gather_subobject_data_for_blueprint(ch)
names = [unreal.SubobjectDataBlueprintFunctionLibrary.get_variable_name(SDS.k2_find_subobject_data_from_handle(h)) for h in handles]
if "MinimapCapture" not in [str(n) for n in names]:
    p = unreal.AddNewSubobjectParams(parent_handle=handles[0], new_class=unreal.SceneCaptureComponent2D, blueprint_context=ch)
    h, err = SDS.add_new_subobject(p)
    SDS.rename_subobject(h, "MinimapCapture")
unreal.BlueprintEditorLibrary.compile_blueprint(ch)
cap = None
# Component templates live on the generated class; set them through the subobject data.
for h in SDS.k2_gather_subobject_data_for_blueprint(ch):
    o = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(SDS.k2_find_subobject_data_from_handle(h))
    if isinstance(o, unreal.SceneCaptureComponent2D): cap = o
cap.set_editor_property("projection_type", unreal.CameraProjectionMode.ORTHOGRAPHIC)
cap.set_editor_property("ortho_width", 30000.0)  # 300 m across
cap.set_editor_property("texture_target", rt)
cap.set_editor_property("relative_location", unreal.Vector(0, 0, 20000))
cap.set_editor_property("absolute_rotation", True)
cap.set_editor_property("relative_rotation", unreal.Rotator(roll=0, pitch=-90, yaw=0))
cap.set_editor_property("capture_every_frame", True)
cap.set_editor_property("capture_source", unreal.SceneCaptureSource.SCS_FINAL_COLOR_LDR)
unreal.BlueprintEditorLibrary.compile_blueprint(ch); EAL.save_loaded_asset(ch)
print("HUD setup", rt.get_path_name(), hud.get_path_name(), cap.get_name())
