# Runs inside the editor during Play (python3 qa.py wasted). Stands Joshua in a traffic car's path until it kills him
# (the BP variables are not instance-editable, and this tests the real path): WASTED must start, the HUD shows it for
# 5 s, then Joshua wakes up at St. Paul's with full health.
import unreal
if "WST" in globals() and WST.get("h"):
    unreal.unregister_slate_post_tick_callback(WST["h"])
world = unreal.UnrealEditorSubsystem().get_game_world()
walker = unreal.GameplayStatics.get_player_controller(world, 0).get_controlled_pawn()
M = unreal.GameplayStatics.get_actor_of_class(world, unreal.load_asset("/Game/VancouverVice/BP_Missions").generated_class())
car = unreal.GameplayStatics.get_actor_of_class(world, unreal.load_asset("/Game/VancouverVice/BP_TrafficCar").generated_class())
WST = {"t": 0.0, "stage": "hit"}
QA_RESULT = "RUNNING"

def _finish(msg):
    global QA_RESULT
    unreal.unregister_slate_post_tick_callback(WST["h"]); WST["h"] = None
    QA_RESULT = msg

def _step(dt):
    if not unreal.UnrealEditorSubsystem().get_game_world():
        return _finish("FAIL play stopped mid-test")
    WST["t"] += dt
    h = M.get_editor_property("Health")
    if WST["stage"] == "hit":  # stand Joshua in the car's path
        walker.set_actor_location(car.get_actor_location() + car.get_actor_forward_vector() * 150 + unreal.Vector(0, 0, 100), False, True)
        if M.get_editor_property("Wasted") > 0: WST["hit"] = round(h); WST["stage"] = "wasted"; WST["t"] = 0.0
        elif WST["t"] > 8: return _finish(f"FAIL the car never killed him, health {h:.0f}")
    elif WST["stage"] == "wasted":
        if WST["t"] > 7.0:
            loc = walker.get_actor_location()
            d = ((loc.x + 22200) ** 2 + (loc.y + 78500) ** 2) ** 0.5
            ok = d < 500 and h > 95
            return _finish(("PASS" if ok else "FAIL") + f" car hit health {WST['hit']}, respawn {d:.0f} cm from St. Paul's, health {h:.0f}")

WST["h"] = unreal.register_slate_post_tick_callback(_step)
