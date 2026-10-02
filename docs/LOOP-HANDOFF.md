# Vancouver Vice loop handoff (2026-10-01, evening)

## What the loop is

A `/loop` that builds out the real Vancouver GTA clone in Unreal, one visual component at a time: body shape, clothes, hair, geometry, and rendering. Each tick: edit code or Blender, screenshot with photo.sh, ship it. Photos go in the session to show progress.

## Where things stand

Male body via unreal/body_male.py (Blender-shaped chest, hips, shoulders). Hair via unreal/hair_shell.py (curly strawberry-blond shell, scalp-grown, face-rigged). Spawn and camera via unreal/scene_setup.py (Joshua at Pacific Centre Apple Store). Photos via unreal/photo.sh. Arms still render grey (needs skin material that actually applies). Polo neckline gapes. Google tiles melt at street level. Next is one-command pipeline: unreal/avatar.sh assembles all of it.

## Next, in order

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
