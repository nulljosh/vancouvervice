# Assets

Everything the web game loads, where it lives and where it came from. Paths are under `site/`. Keep a model under about 300 KB and 12k triangles unless there is only one of it on screen; shrink textures to 1024 px. Graphics cost goes in `docs/BENCHMARK.md` (`node tests/gfxbench.mjs`).

## Models (`models/`)

| Path | What | Triangles | Size | Source |
|---|---|---|---|---|
| `characters/hero.glb` | Joshua's body with idle, walk and run clips (`Idle`, `Casual_Walk`, `Run_02`) | 31k | 1.6 MB | Converted with Blender, clips from the Higgsfield rig, merged by bone name |
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

## Maps (`data/`)

OpenStreetMap extracts for `city.html`: `downtown.json`, `vancouver.json`, `kits.json`, `victoria.json`, `langley.json`, `harrison.json`. The main game's map is the 16 by 18 block grid `vanMap` in `js/data.js`; `docs/LANDMARKS.md` maps every landmark to its cell.

## Art (`img/`, `docs/img/`)

`site/img` holds the landing page art. `docs/img` holds the Higgsfield reference renders: `landmark-*.jpg` for every landmark and `render-*.jpg` for the story.

## Making a new model

1. A clean source image on white (Higgsfield `gpt_image_2_5`, 0.25 credits).
2. Image to 3D, textured (30 credits).
3. Decimate in headless Blender: `/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python tools/decimate.py -- in.glb out.glb 3000`. Weld first, or the per-triangle UV islands block every collapse.
4. `npx @gltf-transform/cli optimize out.glb final.glb --simplify false --compress draco --texture-compress webp --texture-size 1024`.
