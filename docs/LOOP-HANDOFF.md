# Vancouver Vice loop handoff (2026-11-02, night)

## What the loop is
Joshua's call: the real game is Unreal 5.8. The three.js web game is the prototype and the source of the idea (missions, the heist, guns, free roam, real map data). Each pass closes one gap between the game and GTA V (menus, HUD, missions, driving, cops, combat, free roam, world), fixes the top bug it finds, builds, checks the packaged Mac app with a screenshot or clip, commits, and reports in one line.

## Where things stand
- The packaged Mac build runs as its own app. QA passed in the packaged build for the title's Enter key, the three save slots and the in-game tutorial help box.
- Fixes going into tonight's build: the punch plays through the AnimBP DefaultSlot, so the player no longer freezes; the objective beam had collision and lifted him on every jump, now off; pause tab labels no longer overlap; Seawall is the game's own display typeface (tools/make_font.py), used in the menus, the wordmark and the app icon; and a lighter render preset cuts lag.
- Edits no longer need the editor window. `sh unreal/headless.sh` changes the game in about 90 seconds (UnrealEditor-Cmd running unreal/headless.py). Font import is the one step that still needs the full editor, done once hidden.
- Joshua's feedback tonight: the game feels laggy, the progress is mediocre, and the art is so-so. Lag comes first in the next builds: check the frame time in the packaged app after each pass.
- Build loop: `sh unreal/headless.sh`, then `FAST=1 sh unreal/package.sh`.
- Rules for this Mac (16 GB): one heavy thing at a time; no MetaHuman builds (they crash the editor); run `sh unreal/doctor.sh lean` after an editor boot, and restart the editor past about a 15 GB footprint.
- Storage: the LaCie is a spinning disk, so cold editor boots are slow. Joshua has bought a fast NVMe drive. When it is plugged in, move UE_5.8 and the project onto it and point `unreal/open.sh` at the new paths.
- The web game is still live. The web tree has uncommitted work from another session (site/play.html and scratch tests under tests/_*.mjs). Leave it alone and commit only exact paths.

## Next, in order
1. Mission one starts inside the store: grab a few Mac minis, fight the employees to get out, then a getaway car and losing the cops.
2. Guns: pick one up and fire it, with muzzle flash, a reload and ammo that runs out.
3. More cops as the wanted stars rise, and tougher ones at the top.
4. Car damage: dents and lost panels that show on the car, not just smoke and fire.

## Restart prompt
```
/loop Vancouver Vice forever loop: identify gaps between the game and GTA V (menus, HUD, missions, driving, cops, combat, free roam, world) and look for bugs; each pass fix the top one in the Unreal project, build, QA in the packaged app with a screenshot or clip, commit, report in one line.
```
