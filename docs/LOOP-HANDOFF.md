# Vancouver Vice loop handoff (2026-11-01, near midnight)

## What the loop is
Build the whole Vancouver map out to A+ while QAing free roam: walk and drive every neighbourhood, screenshot it, fix the worst thing, test, commit, deploy, send Joshua the screenshots. Every landmark has a Higgsfield reference render; QA each one in game against its render until it holds up. "0 polygons" from Joshua means nothing should look blocky or faceted: smooth, sharp, real models where shapes fall short. Fleet GitHub issues come after (skip joshuatree).

## Where things stand
Shipped tonight: the heist opening, free roam with job markers, the full twenty-job story (Dmitri, Colin, Dad's hard drive), car entry and exit animations, solid furniture, the dark Club Velvet, city pass 1 (Kits houses, Victoria masonry, Stanley Park firs on grass, no centre lines or crosswalks in residential streets).

Testing then shipping (commit "Real cars, bridges, the seawall, the SkyTrain and Waterfront Station"): the Higgsfield sedan model (`site/models/sedan.glb`, 1.2 MB, tinted per car; the procedural extruded sedan is the fallback), Lions Gate towers and cables, Burrard pylons and truss, the Stanley Park seawall, the Expo Line guideway on Main Street with a station and two trains, Waterfront Station, `docs/LANDMARKS.md`.

Written, not applied yet: `lm2.py` in the session scratchpad rebuilds the weak landmarks (Canada Place sails plus a cruise ship, a real Steam Clock with steam, the Art Gallery portico and dome, Rogers Arena glass drum with the red ring, Granville Island tin sheds and silos, the BC Legislature with its dome and lit outline). Apply it after the current test run lands, then QA with the landmark shot script (`lm.mjs` in the scratchpad: one camera per landmark, copy it into tests/ to run it so playwright resolves). If the scratchpad is gone, rebuild those landmarks from `docs/LANDMARKS.md` and the renders.

Landmark map and status: `docs/LANDMARKS.md`. Reference renders: `docs/img/landmark-*.jpg` (13) and story art `docs/img/render-*.jpg`.

Higgsfield, from Joshua tonight: renders are fine to make (0.25 credits each, gpt_image_2_5, on the brand: night, rain, near-black, one red #e0362c accent). He said use Higgsfield "a little" for 3D models: image_to_3d is 30 credits textured; one was spent on the sedan. Ask before more 3D models. Shrink every GLB's textures with the PIL script approach (1024 JPEG) before shipping. Joshua's face reference is media 3758a544.

Rules learned: never edit play.html while a background test-and-commit of it is running; syntax check the module script with `node --check` before every run; a module-level const used in the block loop must be declared before line ~650 (puffMat is not); camera shots inside buildings are framing errors, not game bugs.

## Next, in order
1. Land the current test run, apply `lm2.py`, QA every landmark again, send shots, ship.
2. Remaining landmark gaps from LANDMARKS.md: BC Place red glow and roof cables, Harbour Centre lifts lit, SeaBus at Waterfront, Brockton Point totems, Kits Pool.
3. Downtown streets still look the same everywhere: vary the podium towers, add street furniture (bus shelters, lamp posts, hydro poles in Kits), and the street trees are lollipops (icosahedron crowns), make them round and leafy.
4. More 3D models only with Joshua's yes (a SkyTrain car, a bus).
5. Fleet issues: Nimble 37 (13 accessibility audit findings), Talli 91 needs a human translator.

## Restart prompt
```
/loop qa free roam until entire Vancouver map built out a+quality etcetera. Every landmark against its Higgsfield render in docs/img until it holds up; read docs/LOOP-HANDOFF.md first. Send screenshots as you go. Ask before any Higgsfield 3D model.
```
