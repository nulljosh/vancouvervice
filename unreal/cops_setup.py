"""Cop car for the wanted level: BP_CopCar is BP_TrafficCar in black and white paint with a red and blue light bar.
Its EventGraph (unreal/cop.dsl) follows BP_Missions' Trail, the breadcrumbs of where the player drove, so it stays on
the roads the player used. One cop is placed near spawn, parked until the player is wanted.
Run once: python3 unreal/qa.py "$(cat unreal/cops_setup.py)", then write unreal/cop.dsl into BP_CopCar."""
import unreal

EAL = unreal.EditorAssetLibrary; MEL = unreal.MaterialEditingLibrary; AT = unreal.AssetToolsHelpers.get_asset_tools()
D = "/Game/VancouverVice/Cops"

def light(name, rgb):
    p = D + "/" + name
    if EAL.does_asset_exist(p): return EAL.load_asset(p)
    m = AT.create_asset(name, D, unreal.Material, unreal.MaterialFactoryNew())
    c = MEL.create_material_expression(m, unreal.MaterialExpressionConstant3Vector, -300, 0)
    c.set_editor_property("constant", unreal.LinearColor(rgb[0] * 40, rgb[1] * 40, rgb[2] * 40, 1))
    MEL.connect_material_property(c, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    m.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    MEL.recompile_material(m); EAL.save_loaded_asset(m); return m

red, blue = light("M_LightRed", (1, .02, .02)), light("M_LightBlue", (.02, .1, 1))

if not EAL.does_asset_exist(D + "/BP_CopCar"):
    EAL.duplicate_asset("/Game/VancouverVice/BP_TrafficCar", D + "/BP_CopCar")
bp = EAL.load_asset(D + "/BP_CopCar")
SDS = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
def comps():
    return {unreal.SubobjectDataBlueprintFunctionLibrary.get_object(SDS.k2_find_subobject_data_from_handle(h)).get_name(): h
            for h in SDS.k2_gather_subobject_data_for_blueprint(bp)}
cube = unreal.load_asset("/Engine/BasicShapes/Cube")
for nm, mat, y in (("LightRed", red, -35), ("LightBlue", blue, 35)):
    if nm + "_GEN_VARIABLE" not in comps():
        h, _ = SDS.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=list(comps().values())[1], new_class=unreal.StaticMeshComponent, blueprint_context=bp))
        SDS.rename_subobject(h, nm)
    o = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(SDS.k2_find_subobject_data_from_handle(comps()[nm + "_GEN_VARIABLE"]))
    o.set_editor_property("static_mesh", cube); o.set_material(0, mat)
    o.set_editor_property("relative_location", unreal.Vector(-20, y, 152)); o.set_editor_property("relative_scale3d", unreal.Vector(.25, .6, .12))
    o.set_editor_property("cast_shadow", False); o.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
unreal.BlueprintEditorLibrary.compile_blueprint(bp); EAL.save_loaded_asset(bp)

EAS = unreal.EditorActorSubsystem()
for a in EAS.get_all_level_actors():
    if a.get_actor_label() == "Cop_01": EAS.destroy_actor(a)
cop = EAS.spawn_actor_from_class(bp.generated_class(), unreal.Vector(-6000, 2000, -6840))
cop.set_actor_label("Cop_01"); cop.set_folder_path("Traffic")
cop.get_component_by_class(unreal.StaticMeshComponent).set_material(0, EAL.load_asset("/Game/VancouverVice/Props/Paint/Sedans_black"))
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
print("COPS ready", bp.get_path_name(), cop.get_actor_location())
