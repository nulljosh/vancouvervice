# Vancouver Vice loop handoff (2026-11-23)

## What the loop is
The real game was meant to be Unreal 5.8. The three.js web game is the prototype and the source of the idea (missions, the heist, guns, free roam, real map data). Each pass closes one gap between the game and GTA V (menus, HUD, missions, driving, cops, combat, free roam, world), fixes the top bug it finds, checks the result, commits, and reports in one line.

## Where things stand
- The Unreal project is gone. It lived only on the LaCie drive, which went back, and it was never in git. The city, the Blueprints, the MetaHuman setup, the imported map and the packaged builds went with it. The UE 5.8 engine install on that drive is gone too.
- Every `/Volumes/LaCie` path in `unreal/*.sh` is dead (`open.sh`, `headless.sh`, `photo.sh`, `demo.sh`, `package.sh`). Do not run them until the new drive is set up and the paths point at it.
- What survives on GitHub: the live web game, the map data for 24 Lower Mainland areas in `site/data`, the models in `unreal/assets` and `site/models`, the Unreal build scripts in `tools/` (`ue_city.py`, `ue_region.sh`, `ue_traffic.py`, `ue_people.py`, `ue_props.py`), and the Blueprint DSL and Python in `unreal/`.
- The README is clean (a002749): the stale screenshots are gone, the Canada Place and downtown shots stay, and the benchmarks moved to `docs/ARCHITECTURE.md`.
- The Mac has about 17 GB free. Unreal needs roughly 60 to 80 GB, and cleanup only frees about 10 GB, so the Unreal work waits for the drive.
- The web game is still live. The web tree has uncommitted work from another session (`site/play.html`, `site/models/vehicles/ferrari.glb` and scratch tests under `tests/_*.mjs`). Leave it alone and commit only exact paths.
- Higgsfield app balance is 0.25 credits, so no new generated assets for now.

## Next, in order
1. Get the NVMe drive (1 TB). Plug it in, check the mount name, and keep the 17 GB headroom in mind for the install.
2. Reinstall UE 5.8 on the new drive.
3. Rebuild the project from the `tools/` and `unreal/` scripts. Point `unreal/open.sh`, `headless.sh`, `photo.sh`, `demo.sh` and `package.sh` at the new paths, and drop the `/Volumes/LaCie` defaults.
4. Set up Git LFS before the first large commit, so the project and its binary assets go in from day one.
5. Meanwhile, the web game: pick the top gap from the list in `roadmap.md` and fix it in `site/play.html` once that uncommitted perf pass is sorted out by its owner.

## Restart prompt
```
/loop Vancouver Vice forever loop: identify gaps between the game and GTA V (menus, HUD, missions, driving, cops, combat, free roam, world) and look for bugs; each pass fix the top one in the Unreal project, build, QA in the packaged app with a screenshot or clip, commit, report in one line.
```
