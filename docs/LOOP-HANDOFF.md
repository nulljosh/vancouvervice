# Vancouver Vice loop handoff (2026-11-02, afternoon)

## What the loop is
Joshua's call on 2026-11-02: the real game moves to Unreal. The three.js web game is the prototype (the idea and the kernel: missions, heist, guns, free roam, real map data). Unreal is where it becomes a real game. Each pass: one playable thing in Unreal, proven by a qa.py PASS read from game state, then a short screen recording for Joshua.

## Where things stand
Unreal 5.8.2 lives on the LaCie (`/Volumes/LaCie/UE_5.8`, project `/Volumes/LaCie/Unreal/VancouverVice`, 16 GB). The LaCie is a spinning disk at 125 MB/s, so a cold editor boot takes 15 to 25 minutes. Joshua is buying a Samsung T7 Shield 2 TB; when it is plugged in, copy UE_5.8 (49 GB) and the project onto it and point `unreal/open.sh` at the new paths.

The project already has: Google 3D tiles of downtown through Cesium, the Apple Store spawn on Georgia with a catch pad, BP_Missions (mission one walk, mission two jack a car), the VehicleTemplate sports car, Joshua's MetaHuman (rough), and `unreal/qa.py` walk and drive tests that passed in September. Read UNREAL.md for every gotcha.

The Unreal MCP tools do not load into a session that started before the editor was up. Drive the editor with `unreal/qa.py` (file bridge) and `unreal/mcp.py` (raw HTTP on port 18000).

The web game is still live at vancouvervice.jaybulb.com. Tested and deployed as 4c1ba8b. Uncommitted on top, not yet tested by web.mjs: bake() merges static models per material, a local decimated Ferrari (site/models/vehicles/ferrari.glb, 359k to 44k triangles, needs an ASSETS.md row, CC-BY vicent091036), car paint fix (Body_Color), objective card only touches the DOM on change, dead HVGirl code gone. Profiling found the skinned crowd is the real story-mode hog (hiding peds: 60 to 97 fps). Commit it after web.mjs passes on a day the editor is closed. Tag v2.0.0 once CI on 4c1ba8b is green.

Rules for this Mac (16 GB): one heavy thing at a time. No Playwright or WebKit runs while the editor is up. No MetaHuman builds (they crash the editor). `sh unreal/doctor.sh lean` after boot; restart the editor past about 15 GB footprint.

## Next, in order
1. Editor up: `doctor.sh lean`, then `python3 unreal/qa.py` (walk) and `python3 unreal/qa.py drive`. Fix whatever fails (GameMode default pawn, PlayerStart, catch pad). Record a clip with `screencapture -V`, send it.
2. Port the heist from the web game: the store interior, grab the Macs, the guard in the doorway, two stars and the chase.
3. Guns, cops and stars from the web game's rules.
4. City sharpness: our own Overture/OSM buildings as meshes (tools/hero_blender.py exports FBX) over or instead of the Google tiles. Best done once the SSD makes restarts cheap.
5. Free roam beyond downtown, then the rest of the v2 list in roadmap.md.

## Restart prompt
```
/loop Port Vancouver Vice to Unreal: read docs/LOOP-HANDOFF.md and UNREAL.md first, then work the Next list one playable thing at a time, QA every pass with qa.py and a clip, until the game is A+.
```
