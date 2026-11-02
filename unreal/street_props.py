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
sed = [c for c in P["car"] if not c[3]]; fer = [c for c in P["car"] if c[3]]
n = ism("Street_Sedans", M(base + "sedan/sedan/StaticMeshes/sedan"), sed)
n += ism("Street_Cars", M(base + "ferrari/ferrari/StaticMeshes/ferrari"), fer, yaw_off=90)
for part in ["pole", "arm", "head"]: n += ism("Street_Lamp_" + part, M(base + "lamp/lamp/StaticMeshes/" + part), P["lamp"])
n += ism("Street_Trees", M(base + "tree/tree/StaticMeshes/tree"), P["tree"], scale=lambda it: it[3])
print("instances", n)
