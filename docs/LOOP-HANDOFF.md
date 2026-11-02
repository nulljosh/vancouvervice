# Vancouver Vice loop handoff (2026-11-02, early morning)

## What the loop is
Take every real-streets city to A+, one at a time: Brookswood first, then Vancouver, then the rest of the Lower Mainland in the order in `docs/LOWER-MAINLAND.md`. Sharp, no low-poly look: photo textures, photo tree cut-outs, real footprints, landmarks measured off aerial photos. Each pass: change, QA with screenshots (`node tests/citybench.mjs <area> <shotdir>` shoots and benchmarks), test (`node tests/city.mjs`, `python3 tests/osm.py`, and `node tests/web.mjs` when play.html changes), commit, deploy, send Joshua the shots. Joshua also wants the game to reach its first major version.

Higgsfield is approved; keep the balance at 450 credits or more for his dad's business this week (about 540 left).

## Where things stand
Brookswood (`city.html?area=brookswood`): every building from Overture footprints (`tools/overture.py`, roads too with `--roads` when Overpass is down), houses with photo siding, shingles, garages, doors and driveways, photo firs, cedars and maples as camera-facing cards, photo lawn and asphalt, parking lots, the Brookswood Village strip mall with real shop signs, Mt Baker and Golden Ears bands. Hand-built: a duplex row on 40 Ave (two garages per building), Apostolic Faith Church on 207 St, the Chevron at 208 St, Brookswood Secondary with tennis courts, and the Back Field job (bush party, lose campus security). Do not label the duplex as Joshua's home or put his address in the repo.

Joshua's character in play.html: idle, second idle, walk, run, jab, jump, fall, get-up, shoot-while-walking and a death fall on WASTED.

## Next, in order
1. Brookswood polish: church facade (plain siding reads blocky), shop interiors, more people on the street, traffic on 200 St.
2. Vancouver on the same kit: Overture footprints for downtown, photo trees, landmarks checked against `docs/img`.
3. Fort Langley, then down the list in `docs/LOWER-MAINLAND.md`.
4. Toward 2.0: one menu that reaches every area, a save that carries between play.html and the real streets.

## Restart prompt
```
/loop until A+ perfect cities, no polygons, sharp: Brookswood first, then Vancouver, then the rest of the Lower Mainland per docs/LOWER-MAINLAND.md, toward the first major version. Read docs/LOOP-HANDOFF.md first. QA with screenshots as we go and send Joshua the shots. Higgsfield approved, keep 450 credits.
```
