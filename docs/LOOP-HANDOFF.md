# Vancouver Vice loop handoff (2026-11-02, just past midnight)

## What the loop is
Bring the web game to A+: the whole Vancouver map, every landmark against its Higgsfield render in `docs/img`, real models where shapes fall short ("no polygons"), physics and AI that feel like GTA, Joshua's character and animation. Each pass: change, QA with screenshots or a video, benchmark, test, commit, deploy, send Joshua the shots. Higgsfield is approved; keep an eye on credits (about 617 left) and say what each spend buys.

## Where things stand
Live: the landmark rebuilds, real Higgsfield models (Steam Clock, Douglas firs, street trees on the 60 trees nearest the camera), photo facades and ground in `site/materials`, lamps, hydrants and bus shelters, ten code-review fixes.

Testing then shipping (commit "Joshua moves like a person, physics, smarter traffic and crowds, assets in order"): Joshua's idle and run clips merged onto his body (`models/characters/hero.glb`, 1.6 MB), jog on W and sprint on Shift timed to the measured stride (constants `WALK_V`, `RUN_V`, `JOG`, `SPRINT`), cars knock you down, your car stops on other cars, traffic that brakes, queues, turns at intersections and keeps the right-hand lane, crowds that panic at gunfire and wait at the curb, cops that route down the streets (`copRoute`), and the folder move to `models/characters|vehicles|props`.

Graphics cost is tracked in `docs/BENCHMARK.md` (`node tests/gfxbench.mjs [page] [label]`, server on :8766 from site/). Street view is 45 fps against 50 before the visual pass. Never use transmission glass: it re-renders the whole scene. Assets and how to make new ones: `docs/ASSETS.md` (`tools/decimate.py`, `tools/merge-clips.mjs`).

Rules learned: never edit play.html while a background test-and-commit of it runs; heavy screenshot runs during a test can time it out; `node --check` the module script before every run; a texture swapped to a bigger image needs `dispose()` first.

## Next, in order
1. The grey dome mountains: a North Shore mountain backdrop from Higgsfield on a cylinder.
2. Ben and Alexandre still use the crowd walk sped up; give them idle and run the same way, or reuse a rigged body.
3. BC Place red glow and roof cables, Harbour Centre lit lifts, SeaBus at Waterfront, Brockton totems, Kits Pool.
4. Skyline view costs 15M triangles: cull far shadow casters, lighter far crowns.
5. Fleet issues: Nimble 37 (13 accessibility findings), Talli 91 needs a human translator. Issue 44 became an original poster landing from our renders.

## Restart prompt
```
/loop until A+: Vancouver Vice physics, AI, graphics and every landmark. Read docs/LOOP-HANDOFF.md first. QA with screenshots and video, benchmark in docs/BENCHMARK.md, send Joshua the shots. Higgsfield is approved, watch credits.
```
