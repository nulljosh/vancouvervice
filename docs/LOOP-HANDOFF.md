# Vancouver Vice loop handoff (2026-11-02, night)

## What the loop is
Joshua's call on 2026-11-02: the real game moves to Unreal. The three.js web game is the prototype (the idea and the kernel: missions, heist, guns, free roam, real map data). Unreal is where it becomes a real game. Each pass: one playable thing in Unreal, proven by a qa.py PASS read from game state, then a short screen recording for Joshua.

## Where things stand
- **Packaged Mac build runs.** `/Volumes/LaCie/Unreal/Builds/2026-11-02/Mac/VancouverVice.app` (1.6 GB) holds the whole Lower Mainland: 18 towns and the corridor between them, 572 chunks, drawn to 2.5 km, at 60 fps. Launch with `open -n <app> --args -windowed -ResX=1600 -ResY=900 -nosound`. The first launch asks for removable-volume access. The editor's PIE runs at 8 fps no matter what is hidden, so judge speed in the packaged build, not in the editor.
- **Working in Unreal:** walk and drive tests pass (`python3 unreal/qa.py`, `python3 unreal/qa.py drive`). Our own downtown replaces the Google tiles. Joshua's model is rigged from his photo and moves on his own clips. Street props and traffic are in: parked and moving cars drive nose first (`unreal/car_facing.py`), street lights and trees sit on the real curbs.
- **Minimap HUD** (BP_VVHud via `unreal/hud.dsl` and `unreal/hud_setup.py`; BP_Missions BeginPlay calls ClientSetHUD).
- **Wanted level and cop chase** (`unreal/cops_setup.py`, `unreal/cop.dsl`, Stars/Calm/Trail/TrailT/Busted vars in `unreal/missions_graph.dsl`). Jacking the car is one star. BP_CopCar follows the Trail breadcrumbs. Ten seconds over 150 m loses them and completes mission two. Caught while slow means BUSTED, then back to the store.
- **Build fixes that are permanent:** CesiumForUnreal is disabled in the uproject, and the BP_Missions Cesium nodes are gone. The five Cesium actor files are in `/Volumes/LaCie/Unreal/cesium_actors_backup`. The engine's UBT was patched so the Xcode finalize step returns early under `UBT_SKIP_XCODE_FINALIZE=1` (original at `/Volumes/LaCie/Unreal/AppleToolChain.cs.orig`). `package.sh` runs the Xcode Stage step itself.
- **Camera:** BP_Missions BeginPlay clamps pitch to -40..25.
- **In flight, written but not yet in the editor:** health, punch and WASTED. `unreal/missions_graph.dsl` (Health regen 2/s; F or left click punches with `JoshuaHero_mRight_Jab_from_Guard` and ApplyRadialDamage 90 cm ahead; Health 0 is WASTED for 5 s with falling_down and input off, then respawn at St. Paul's, with a Posed flag that puts the AnimBP back). `unreal/traffic.dsl` (a car within 2.8 m of Joshua on foot hurts 400/s and launches him). `unreal/hud.dsl` (health bar over the minimap, WASTED text). Steps: add_variable on BP_Missions for Health, Wasted and PunchT (float) and Posed (bool); write the three graphs; fix node names with find_node_types; compile; trace ground at the hospital; BP_Pedestrian EventAnyDamage knocks them down; QA clip; package. The hero glb already carries Jab, falling_down, Stand_Up1 and Shot_and_Fall_Backward. /Game/Characters mounts from `/Volumes/LaCie/UE_5.8/Templates/TemplateResources/High/Characters/Content`, so nothing is missing from the project folder.
- **Web game** is still live at vancouvervice.jaybulb.com. The web tree has uncommitted work from another session (site/play.html and scratch tests under tests/_*.mjs). It is not this loop's. Leave it alone, and commit only exact paths.
- **Drive the editor** with `unreal/qa.py` (file bridge) and `unreal/mcp.py` (raw HTTP on port 18000). The Unreal MCP tools do not load into a session that started before the editor was up. Read UNREAL.md for every gotcha.
- **Storage:** the LaCie is a spinning disk at 125 MB/s, so a cold editor boot takes 15 to 25 minutes. Joshua is buying a fast NVMe drive. The handoff named a Samsung T7 Shield 2 TB and the roadmap names an OWC Envoy Ultra, so check which one he bought. When it is plugged in, copy UE_5.8 (49 GB) and the project onto it, and point `unreal/open.sh` at the new paths.

## Rules for this Mac (16 GB)
One heavy thing at a time. No Playwright or WebKit runs while the editor is up. No MetaHuman builds (they crash the editor). Run `sh unreal/doctor.sh lean` after boot, and restart the editor past about a 15 GB footprint.

## Next, in order
1. Health, punch and WASTED (in flight, above).
2. Guns, more stars over time and more cops, from `docs/GAP-MATRIX.md`.
3. Traffic and people in every town. Once they fill the map, move them from Blueprint ticks to C++ or Mass (Joshua said yes, for later).
4. Free-roam gaps: traffic and people are downtown only, Tab fast travel still uses dead Cesium (`fasttravel.dsl`), and town-to-town driving is untested.
5. Joshua's new look (single cuff, grey dad runners, white socks). Higgsfield render 620d4af1 is approved. The 3D build (image_to_3d with rig, about 38 credits) waits on a credit top-up past the 450 floor. Then unscale in Blender, run `unreal/import_hero.py`, and consolidate onto his clips.
6. Street life: people on the sidewalks, wheels not tinted by the paint, the white wireframe mission dome replaced by a proper marker, and traffic stopping for the player.
7. Mac .app release polish: splash and loading screen while the city streams in. Then the rest of the open list in `roadmap.md`.

## Restart prompt
```
/loop Port Vancouver Vice to Unreal: read docs/LOOP-HANDOFF.md and UNREAL.md first, then work the Next list one playable thing at a time, QA every pass with qa.py and a clip, until the game is A+.
```
