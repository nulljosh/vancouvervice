# Places parked cars, street lights and street trees from /tmp/vv_qa/props.json (computed from site/data/downtown.json)
# as one actor per prop kind holding instanced meshes. Run inside the editor via qa.py.
import json, math
EAS = unreal.EditorActorSubsystem(); sds = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem); Z = -6840
P = json.load(open("/tmp/vv_qa/props.json")); M = lambda p: unreal.load_asset(p)
for a in EAS.get_all_level_actors():
    if a.get_actor_label().startswith("Street_"): EAS.destroy_actor(a)
def ism(label, mesh, items, yaw_off=0.0, zoff=Z, scale=lambda it: 1.0):
    a = EAS.spawn_actor_from_class(unreal.Actor, unreal.Vector(0, 0, Z)); a.set_actor_label(label); a.set_folder_path("Street")
    root = sds.k2_gather_subobject_data_for_instance(a)[0]
    h, fail = sds.add_new_subobject(unreal.AddNewSubobjectParams(parent_handle=root, new_class=unreal.InstancedStaticMeshComponent))
    c = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(unreal.SubobjectDataBlueprintFunctionLibrary.get_data(h))
    c.set_static_mesh(mesh)
    ts = []
    for it in items:
        s = scale(it); ts.append(unreal.Transform(unreal.Vector(it[0] * 100, it[1] * 100, zoff), unreal.Rotator(roll=0, pitch=0, yaw=it[2] + yaw_off), unreal.Vector(s, s, s)))
    c.add_instances(ts, False, True); return len(ts)
base = "/Game/VancouverVice/Props/"
PAINT = {"white": (2.3, 2.3, 2.2), "black": (.12, .12, .13), "silver": (1.4, 1.45, 1.5), "navy": (.2, .35, .95), "red": (1.7, .12, .12), "green": (.25, .65, .35), "beige": (1.9, 1.6, 1.1)}  # multipliers on the grey paint texture
MEL = unreal.MaterialEditingLibrary
def paint(src, name, rgb):  # a copy of the car's paint material in this colour, made once
    path = base + "Paint/" + name
    mi = unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else unreal.EditorAssetLibrary.duplicate_asset(src.get_path_name().split(".")[0], path)
    MEL.set_material_instance_vector_parameter_value(mi, "BaseColorFactor", unreal.LinearColor(*rgb, 1)); unreal.EditorAssetLibrary.save_loaded_asset(mi); return mi
sedan, fer = M(base + "sedan/sedan/StaticMeshes/sedan"), M(base + "ferrari/ferrari/StaticMeshes/ferrari")
n = 0
for i, (k, rgb) in enumerate(PAINT.items()):  # cars take colours in turn, one instanced actor per colour
    for mesh, slot, sel, off, tag in [(sedan, 0, lambda c: not c[3], 0, "Sedans"), (fer, 1, lambda c: c[3], 90, "Cars")]:
        cars = [c for j, c in enumerate(P["car"]) if sel(c) and j % len(PAINT) == i]
        if not cars: continue
        n += ism("Street_%s_%s" % (tag, k), mesh, cars, yaw_off=off)
        a = [x for x in EAS.get_all_level_actors() if x.get_actor_label() == "Street_%s_%s" % (tag, k)][0]
        a.get_component_by_class(unreal.InstancedStaticMeshComponent).set_material(slot, paint(mesh.static_materials[slot].material_interface, "%s_%s" % (tag, k), rgb))
for part in ["pole", "arm", "head"]: n += ism("Street_Lamp_" + part, M(base + "lamp/lamp/StaticMeshes/" + part), P["lamp"])
n += ism("Street_Trees", M(base + "tree/tree/StaticMeshes/tree"), P["tree"], scale=lambda it: it[3])
print("instances", n)
