# Vancouver Vice loop handoff (2026-11-02, early morning)

## What the loop is
Get to a QA video of Joshua stealing a car in Brookswood and driving the real freeways to downtown Vancouver, a drive of about 10 to 20 minutes. Then keep taking every real-streets city to A+ (Brookswood, Vancouver, then the rest of the Lower Mainland in the order in `docs/LOWER-MAINLAND.md`): sharp, no low-poly look, photo textures and photo tree cut-outs. Each pass: change, QA with screenshots or video, test (`node tests/city.mjs`, `python3 tests/osm.py`, and `node tests/web.mjs` when play.html changes), commit, deploy, send Joshua the shots.

Higgsfield is approved; keep the balance at 450 credits or more (about 540 left).

## Where things stand
The drive is three maps joined by handoffs. Brookswood and downtown are life size. The corridor between them (`city.html?area=corridor`, built by `tools/corridor.py`) is Highway 1, the big roads, the Fraser and Burrard Inlet at half scale, so the real 50 km route takes about 14 minutes. Driving off one map saves latitude, longitude, heading, speed, wallet, stars and the car in localStorage and opens the next map at the same spot.

In the car: E beside any car in traffic pulls the driver out (one star). Sedans drive whole streets, one-way carriageways keep their direction and lane, and cars that fall far behind come back near you. `AUTO()` routes the real road graph (fastest time) and drives it like a person; `tests/drive.mjs` films the whole trip with it.

Brookswood also has people on the sidewalks, a stucco church, and Joshua's own idle, jog and sprint clips. Do not label the duplex as Joshua's home or put his address in the repo.

## Next, in order
1. Watch the drive video and fix what looks wrong: car orientation, lane position, interchanges, speed on 200 St.
2. The corridor needs life: overpasses at the right height, the Port Mann Bridge, buildings along the highway, signs (exit signs with real names).
3. Vancouver on the Brookswood kit: Overture footprints for downtown, photo trees, landmarks checked against `docs/img`.
4. Fort Langley, then down the list in `docs/LOWER-MAINLAND.md`.
5. Toward 2.0: one menu that reaches every area, and the save that now crosses maps carried into play.html too.

## Restart prompt
```
/loop until we can QA a video of stealing a car in Brookswood and driving the freeways to Vancouver (10 to 20 minute drive), then keep taking every city to A+, no polygons, sharp. Read docs/LOOP-HANDOFF.md first. QA with screenshots and video as we go and send Joshua the shots. Higgsfield approved, keep 450 credits.
```
