# Assets

Everything the web game loads, where it lives and where it came from. Paths are under `site/`. Keep a model under about 300 KB and 12k triangles unless there is only one of it on screen; shrink textures to 1024 px. Graphics cost goes in `docs/BENCHMARK.md` (`node tests/gfxbench.mjs`).

## Models (`models/`)

| Path | What | Triangles | Size | Source |
|---|---|---|---|---|
| `characters/hero.glb` | Joshua's body with idle, second idle, walk, run, jab, jump, fall, get-up, shoot-while-walking and death clips (`Idle`, `Idle_02`, `Casual_Walk`, `Run_02`, `Right_Jab_from_Guard`, `Regular_Jump`, `falling_down`, `Stand_Up1`, `Walk_Forward_While_Shooting_inplace`, `Shot_and_Fall_Backward`, plus `Male_Run_Forward_Pick_Up_Left` for grabbing) | 31k | 1.8 MB | Converted with Blender, clips from the Higgsfield rig, merged by bone name |
| `characters/staff_m.glb`, `characters/staff_f.glb` | The two store staff from the heist render: Higgsfield image, image to 3D with rig and idle, then Joshua's clips merged on by bone name | | 1.1 MB each | Higgsfield (`gpt_image_2_5`, `image_to_3d`) |
| `img/store/*.jpg` | Store interior: living wall and limestone generated as tiles on Higgsfield, floor and oak cut from `docs/img/georgia-store-concept.jpg` | | | Higgsfield |
| `materials/shop-*.jpg` | Nine storefronts (guns, clothes, barber, cafe, restaurant, pawn, pharmacy, convenience, pub), fictional names, no real brands | | | Higgsfield `gpt_image_2_5` |
| `characters/people/*.glb` | The crowd: 6 men, 6 women, each with walk and idle | 7k to 9k | 2.4 MB each | Microsoft Rocketbox, MIT |
| `vehicles/sedan.glb` | The everyday car, tinted per car | 12k | 1.2 MB | Higgsfield image to 3D |
| `props/tree.glb` | Street tree, on the 60 nearest blocks' trees | 12k | 288 KB | Higgsfield image to 3D, decimated in Blender |
| `props/fir.glb` | Stanley Park Douglas fir, every fir in the park | 3k | 164 KB | Higgsfield image to 3D, decimated in Blender |
| `props/clock.glb` | The Gastown Steam Clock | 9k | 272 KB | Higgsfield image to 3D, decimated in Blender |

Soldier, Xbot and the Ferrari load from the three.js examples CDN.

## Materials (`materials/`)

Photo textures, 1024 px JPEG, each one tile of 160 by 160 world units (four floors). They replace the canvas-drawn facades once loaded; the canvases stay as the fallback.

| File | Used on |
|---|---|
| `glass.jpg` | Downtown towers |
| `concrete.jpg` | Offices, Harbour Centre |
| `shop.jpg` | Street-level podiums under the towers |
| `brick.jpg` | Gastown, Yaletown, Water Street |
| `stone.jpg` | Victoria, the Art Gallery, the Legislature |
| `siding.jpg` | Kitsilano houses, tinted per house |
| `asphalt.jpg`, `sidewalk.jpg` | Roads and sidewalks |

`northshore.webp` is the North Shore range behind the city (Higgsfield painting, sky keyed out to alpha).

## Maps (`data/`)

OpenStreetMap extracts for `city.html`: `downtown.json`, `vancouver.json`, `kits.json`, `victoria.json`, `langley.json`, `harrison.json`. The main game's map is the 16 by 18 block grid `vanMap` in `js/data.js`; `docs/LANDMARKS.md` maps every landmark to its cell.

## Art (`img/`, `docs/img/`)

`site/img` holds the landing page art. `docs/img` holds the Higgsfield reference renders: `landmark-*.jpg` for every landmark and `render-*.jpg` for the story.

## Making a new model

1. A clean source image on white (Higgsfield `gpt_image_2_5`, 0.25 credits).
2. Image to 3D, textured (30 credits).
3. Decimate in headless Blender: `/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python tools/decimate.py -- in.glb out.glb 3000`. Weld first, or the per-triangle UV islands block every collapse.
4. `npx @gltf-transform/cli optimize out.glb final.glb --simplify false --compress draco --texture-compress webp --texture-size 1024`.

## Giving a body Joshua's moves

1. Strip the old skeleton: `Blender -b --factory-startup --python tools/strip-rig.py -- in.glb plain.glb`.
2. Upload `plain.glb` and run Higgsfield `3d_rigging` with animation 0 (Idle), 8 credits.
3. `node tools/merge-clips.mjs rigged.glb merged.glb hero-source.glb` copies Casual_Walk and Run_02 by bone name, scaling hip motion to the new body's height.
4. Compress as in step 4 above.
