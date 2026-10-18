# Vancouver Vice loop handoff (2026-10-17, late evening)

## What the loop is

A `/loop` that works through roadmap.md for Vancouver Vice on the web build (site/city.html and site/real.html), one item per tick: build it, test it headless (node tests/web.mjs, node tests/city.mjs), deploy with npx wrangler deploy, commit, and tick the roadmap. Unreal is shelved, so ticks do not open the editor.

## Where things stand

Unreal is shelved to one dedicated day a week until a 1 TB SSD lands. The limit is RAM on the 16 GB Mac mini, not skill. A boot off the LaCie took 16 minutes and ended in a memory warning with swap nearly full; Joshua closed it. The editor alone is about 6 GB.

Disk is at 34 GB free after old Claude chats and Claude Desktop VM images moved to the LaCie.

CI is green on the latest push (7829e23, the online test and og:image on jaybulb.com). The native shells also point at jaybulb.com now, which fixed the red native-shells check.

Optimization is the focus. optimize.py has the Cesium streaming knobs and an 8 second fps reading, ready for the next editor boot. A tests/bench.mjs baseline was running at the end of the day. Read its output before changing anything.

Open on the web build: optimization on site/city.html and site/real.html, README screenshots, and the promo video.

The SSD is not bought yet. The plan is a 1 TB Samsung T7 Shield, the engine and project moved onto it, and the LaCie sold back to Dad. Price a rented GPU box by the hour first.

Working tree note: several unreal/assets files show as modified and are not part of the loop. Do not stage them.

## Next, in order

0. CI check: `gh run list --limit 1`. If it is red, `gh run view --log-failed` and fix that first.
1. Bench baseline: read the output of the tests/bench.mjs run from the end of the day. If there is none, rerun it once nothing else heavy is running.
2. Web optimization on site/city.html and site/real.html, one change per tick, each measured against the baseline.
3. README screenshots from the web build.
4. Promo video from the web build.
5. SSD: waiting on Joshua's purchase. Do not touch the LaCie or the Unreal engine until the SSD is in.

## Restart prompt

```
/loop Vancouver Vice, web build only. Read docs/LOOP-HANDOFF.md first. Work the Next list in order, one item per tick: build it, test with node tests/web.mjs and node tests/city.mjs, deploy with npx wrangler deploy, commit by exact path, and tick roadmap.md. Do not open Unreal, touch the LaCie, or stage the unreal/assets files already modified in the working tree.
```
