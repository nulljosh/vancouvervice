# Vancouver Vice loop handoff (2026-10-01, evening)

## What the loop is

A `/loop` that builds out the real Vancouver GTA clone in Unreal, one visual component at a time: body shape, clothes, hair, geometry, and rendering. Each tick: edit code or Blender, screenshot with photo.sh, ship it. Photos go in the session to show progress.

## Where things stand

Avatar is rough and incomplete. Male body from Blender (via unreal/body_male.py: chest, hips, shoulders shaped). Hair shell scalp-grown, face-rigged (via unreal/hair_shell.py). Spawn at Pacific Centre Apple Store (via unreal/scene_setup.py). Open: arms render grey (untextured, needs skin material that actually applies), polo neckline gapes, jeans bag out. City: Google tiles still melt at street level. Mission: not playable. Photos via unreal/photo.sh.

## Next, in order

0. CI first: `gh run list --limit 1`. The city test was red since 2026-09-26 (cops never spawned before the car model loaded); a stand-in cop car landed in 2a4169c, result unconfirmed. If still red, `gh run view --log-failed` and fix before anything else.
1. Grey arms: write a skin material that actually follows the import, fix arms rendering.
2. Polo collar and slim jeans: adjust body shape to fit clothes, finalize silhouette.
3. Import Granville and Georgia detail island: copy the glTF from site/worlds/granville-georgia/hero.glb to Unreal at spawn location so the street is real (buildings, signs, textures).
4. Splash screen until tiles load: show loading card while Cesium 3D Tiles stream in at distance.
5. Mission one per docs/MISSION1.md: lobby and heist dialogue, laptop heist gameplay.
6. Title screen, save/load, settings: ship the vertical slice.

## Restart prompt

```
/loop Vancouver Vice. Read docs/LOOP-HANDOFF.md and docs/METAHUMAN-API.md first. Work the Next list in order, one item per tick, photo with sh unreal/photo.sh after each change and send it. Never run a MetaHuman build mid-session; use the live preview. Keep RAM in check with unreal/guard.sh.
```
