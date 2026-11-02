# Vancouver Vice loop handoff (2026-11-02, afternoon)

## What the loop is
Joshua's v1 (free roam anywhere in the Lower Mainland, on foot or by car, plus a playable Mac app) ships as 2.0.0, because the tags already passed 1.x. His v2 is the list at the top of roadmap.md and ships as 3.0.0. Each pass: change, QA in WebKit (the Mac app's engine) with screenshots or video, test, commit by exact path, deploy, send Joshua the shots.

Higgsfield is approved for graphics; keep the balance at 450 credits or more (about 455 now).

## Where things stand
The Mac app (apps/apple, a WKWebView shell) loads the live site, so every deploy reaches it. A built copy sits in ~/Applications/VancouverVice.app.

Story mode: mission 1 plays end to end. The store on Georgia is rebuilt from the Higgsfield concept (limestone, living walls, oak tables, polished floor, glass doors). The two staff are real Higgsfield-rigged people (models/characters/staff_m.glb, staff_f.glb) wearing Joshua's clips. You carry four Macs, the male staffer plants himself in the doorway and you knock him down to get out, then two stars and a car chase. Dying on the getaway restarts the heist. Joshua has a snatch animation (Male_Run_Forward_Pick_Up_Left merged into hero.glb). Six guns: you start with the pistol and find the rest as glowing pickups (PICKUPS in play.html); Q and 1 to 7 switch among owned guns; each gun has its own synthesized report (GUNSND).

Real streets: Brookswood covers 32 to 48 Avenue and 196 to 208 Street (6,584 buildings). Vancouver covers Stanley Park to Commercial Drive (17,659 buildings). Every shop ground floor wears one of nine Higgsfield storefronts (materials/shop-*.jpg) picked from its OSM business type, rotating where none is listed. tools/osm.py now keeps shop types (SHOP_KIND) but the Vancouver rebuild with them timed out on Overpass; rerun `python3 tools/osm.py --area downtown`, then overture.py with `--rows <scratchpad>/ov-downtown-full.json`, then copy downtown.json to vancouver.json.

The corridor (big-road map) runs from Tsawwassen to Chilliwack and Harrison; the eastern roads and rivers come from Overture because Overpass was down. There is no open ocean west of the old map edge yet.

Gotchas: never run WebKit or screenshot jobs while tests/web.mjs runs (swiftshader starves and checks fail); copsCome is a known flake; Overpass needs a User-Agent header or it answers 406.

## Next, in order
1. Full test run passing, then commit everything, push, deploy, wait for green CI, tag v2.0.0, send Joshua the Mac zip again.
2. Work down the v2 list in roadmap.md, one item per pass, with a video for each.

## Restart prompt
```
/loop until v1. Then export it, I wanna try playing the game. It should allow us to drive or walk anywhere in the lower mainlands, free roam. When done, build out roadmap to v2, then loop to it, QA every pass, until the game is A+. Read docs/LOOP-HANDOFF.md first.
```
