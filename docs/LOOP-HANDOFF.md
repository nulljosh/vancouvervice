# Vancouver Vice loop handoff (2026-09-26, evening)

## What the loop is

Driving Unreal 5.8 headless to build Vancouver Vice Act Two as a vertical slice: polish the first five minutes (Apple Store heist, car jack, escape) to shipping quality, package the macOS .app, and QA against real hardware before wide release. One subagent per step (Haiku for mechanical tasks, Sonnet for architecture), Opus for hard decisions only. Restart from the task queue if session ends.

## Where things stand

First detail island shipped and live: Granville and Georgia with ten buildings, each sourced from real OSM heights. Façade generator (site/js/hero.js) produces storey-true glazing; every tenant rendered as a sign on its own storefront. Blender export (tools/hero_blender.py) builds headless into single 8.7 MB Unreal asset with 69 tenant signs. QA via Playwright, benchmarks: island builds in 10.9 s, swiftshader renders 5 fps headless; fix was deferring scene.add one extra frame. Deployed via wrangler, both tests pass (tests/city.mjs, tests/hero.mjs). Live at vancouvervice.heyitsmejosh.com/city.html. Editor 8-10 GB (near-player tile loading fixed the 54 GB hog; guard.sh monitors footprint and restarts if unsafe). Player visible in Play with strawberry blonde hair and carved pants on the polo skeleton. Spawn moved to Apple Store Georgia sidewalk. Cesium tileset lean: 256 MB cache, 12 loads, SSE 64. Key art live on README and landing (six panels drawn by key_art.py). Mission one DSL drafted with two chasing employees and gun tutorial. Known gaps: pawn broken in packaged builds (check GameMode default pawn), polo fits badly, city.mjs CI times out on swiftshader, body needs 6 ft slim rebuild.

## Next, in order

0. Body rebuild — 6 ft slim male MetaHuman, commit and build (previous build produced female mesh), verify via CaptureAssetImage
1. Pawn spawn fix — check GameMode default pawn and PlayerStart in Lvl_ThirdPerson, run qa.py shot to get street photo, verify in packaged build
2. Polo refit — weight painting, bone hierarchy, pants and jacket fit polish
3. Apply mission one DSL — two chasing Apple employees, gun tutorial wired into BP_ThirdPersonCharacter
4. Drive-by shooting — playtest car physics, hold Shift aim, mouse click fire, record demo
5. Walls and camera collision — walk through interiors (inside-out camera fix), third-person clip check
6. Map detail SSE 6 and daylight — day/night flashing, shader bump, Gastown perf test
7. Splash preload screen — loading spinner while tiles stream
8. BP_Heat stars and system — three stars, wanted meter, crime heat
9. NPCs and dynamic crowd — NPCs, dialogue, mission feedback
10. Headless QA mode — autoplay.dsl unattended, crash logs, fail fast
11. Package the .app — build macOS binary, sign, notarize, ship

## Restart prompt

```
/loop 1h Vancouver Vice island import and polish. First goal: Unreal import of Granville-Georgia island via MCP (8.7 MB Blender asset with 69 tenant signs), test playability in Lvl_ThirdPerson. Then: Gastown island build, Robson at Burrard, Waterfront. Pawn and camera are next fixes if Unreal import blocked. One Haiku subagent per step, mechanical work only; Sonnet for architecture decisions. Next roadmap milestone: vertical slice packaged and QA'd on real Mac. If blocked or decision point: stop the loop, post findings, wait for guidance.
```
