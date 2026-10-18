# Runs inside the editor (qa.py bridge). Sets the Cesium streaming knobs for a smooth walk, then averages fps over 8 s of Play.
# Usage: python3 qa.py "$(cat optimize.py)"  (start Play first). Tune SSE up (blurrier, faster) until fps is 30+.
# Result: QA_RESULT = "fps 28.4 | sse=16 ..." or "FAIL <why>".
import unreal
SSE = globals().get("SSE", 16)  # 8 sharp, 16 balanced, 32 fast
world = unreal.UnrealEditorSubsystem().get_game_world()
tiles = unreal.GameplayStatics.get_actor_of_class(world, unreal.Cesium3DTileset)
QA_RESULT = "RUNNING"
if not tiles:
    QA_RESULT = "FAIL no Cesium3DTileset in the level"
else:
    knobs = {  # ponytail: names are the C++ UPROPERTYs in snake_case; any that this plugin version lacks are skipped and reported
        "maximum_screen_space_error": float(SSE),
        "maximum_cached_bytes": 512 * 1024 * 1024,
        "maximum_simultaneous_tile_loads": 12,
        "preload_ancestors": True,
        "preload_siblings": False,
        "loading_descendant_limit": 10,
        "enable_fog_culling": True,
        "enforce_culled_screen_space_error": True,
        "culled_screen_space_error": 64.0,
    }
    skipped = []
    for k, v in knobs.items():
        try: tiles.set_editor_property(k, v)
        except Exception: skipped.append(k)
    S = {"t": 0.0, "n": 0}
    def _tick(dt):
        S["t"] += dt; S["n"] += 1
        if S["t"] >= 8.0:
            unreal.unregister_slate_post_tick_callback(S["h"])
            global QA_RESULT
            QA_RESULT = "fps %.1f | sse=%s | skipped: %s" % (S["n"] / S["t"], SSE, ",".join(skipped) or "none")
    S["h"] = unreal.register_slate_post_tick_callback(_tick)
