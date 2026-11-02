# Vancouver Vice loop handoff (2026-11-01, late night)

## What the loop is
One self-paced loop with two stages. First, Vancouver Vice (Joshua's model and the city) until A+: each pass screenshots or films the game, fixes the worst thing, tests, commits and deploys. Then the fleet GitHub issues, easiest real fixes first, skipping joshuatree (another session owns it).

## Where things stand
A new game opens mid-heist inside the store on Georgia: grab six Mac minis, the staff in blue shirts chase you out, one star, jack a car. The whole story is in `site/js/data.js` and `docs/STORY.md`: twenty jobs in three acts, tied together by Dmitri's forty grand. Colin, a fictional McDonald's manager, launders Dmitri's cash through the night deposit, leaves Club Velvet with your girl, and turns out to own Dad's hard drive. Between jobs the city is free roam with yellow job markers (Joshua at the Steam Clock, Ben at Dad's garage, Alexandre in Victoria, all three at the garage). Scene jobs (`kind: "meet"`) play a card when you reach the place.

Walk-in rooms (ROOMS in play.html, furniture footprints in BLOCKS): Granville Pawn, the store on Georgia, Dad's garage, the McDonald's on Granville, Club Velvet. Furniture is solid and movement slides along walls. Getting in a car walks you to the driver's door first; a jacked driver lands on the sidewalk. Staff and Colin wear uniforms on the crowd bodies through a shader shell (`wear()`); standing people hold the walk clip on a feet-together frame because the crowd's idle clip is a bind pose.

Key art from Higgsfield (gpt_image_2_5, 0.25 credits each, on the brand: night, rain, near-black, one red accent) is in `docs/img/render-*.jpg`. Joshua's face reference is media 3758a544. A QA film script lives in the session scratchpad (film.mjs); playwright's ffmpeg is installed.

Colin stays fictional: no disability angle and no likeness from real photos (Joshua asked; declined under the satire rule in CLAUDE.md).

## Next, in order
1. Ship check: the commit for story, car animations, solid furniture and the dark club runs after `node tests/web.mjs` passes.
2. Film a fresh QA video and fix what looks worst: the Harbour Centre and Gastown street shots clipped into buildings, the store staff can get stuck behind tables when chasing.
3. Story jobs that are still generic (taxi and deliver stand-ins for Kits Beach, the Ferry, the Score): give each its own place and beat like the heist and the club.
4. Dad and Mom models once Joshua sends photos (ask before any Higgsfield spend).
5. Fleet issues: Nimble 37 (13 accessibility audit findings), Talli 91 needs a human translator, then Noema and Nimble long range.

## Restart prompt
```
/loop until Vancouver Vice (Joshua's model and the city) is A+, then until all fleet GitHub issues are resolved by code fix and closed (skip joshuatree, the other session owns it). Make every decision; Joshua is only needed for 2FA codes. Ask before any Higgsfield spend.
```
