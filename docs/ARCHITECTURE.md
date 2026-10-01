# How Vancouver Vice works

Three versions of one game, sharing the same rules and map data.

## The pieces
| Part | Where | What it does |
|---|---|---|
| Main game | `site/play.html` | Simplified Vancouver and Victoria with all the gameplay: missions, cops, heroes, weapons, weather, saves. three.js, runs anywhere. |
| Real streets | `site/city.html` | Downtown, Kits, Victoria and Langley built from OpenStreetMap. Real buildings, signs, shops you walk into, traffic, cops, SkyTrain, online play. |
| Real Vancouver beta | `site/real.html` | Google photorealistic 3D tiles streamed through Cesium. |
| Unreal version | `unreal/`, `UNREAL.md` | The high-end build, set up through Unreal's MCP. In progress. |
| Online world | `worker.js` | One Cloudflare Durable Object relays player positions. |
| Map exporter | `tools/osm.py` | Pulls buildings, roads, parks, water, shops, SkyTrain lines and stations from OpenStreetMap. |
| Apps | `apps/` | Native shells: Windows C#, Linux C, Mac and iOS SwiftUI, Android Java. Each opens the live game. |
| Models | `site/models/` | Hero and 12 people (Rocketbox, MIT), converted with Blender. |
| Key art | `tools/key_art.py` | Generates six-panel Unreal cover grid: Harbour Centre at sunset, cop chase, seagull, Gastown clock, SkyTrain, drawn in code and rasterized. |
| Key art render | `tools/key_art.mjs` | Browser render of the key art panels for README and landing preview. |
| RAM watchdog | `unreal/guard.sh` | Monitors editor memory, restarts if footprint exceeds safe limits or free RAM drops below 15 percent. |
| Hair install | `unreal/hair_install.py` | Applies Hair_S_Messy groom to the Mesh head socket with strawberry blonde settings (hairMelanin 0.22, hairRedness 1.0). |
| Pants carve | `unreal/pants.py` | Carves pants from the body mesh in Blender: height band waist 100 to ankle -5, offset 3 cm. |
| Pants import | `unreal/pants_install.py` | Imports carved pants with Interchange FBX onto the polo skeleton. |
| Mission dialogue | `unreal/employees.dsl` | DSL draft for mission one characters and dialogue with Apple Store employees. |
| Mission one | `unreal/mission1.dsl` | Mission one script: rob Apple Store, two chasing employees, gun tutorial. |

## How the city is built
`tools/osm.py` turns OpenStreetMap into local metres around a centre point. `city.html` extrudes every building footprint to its real height, lays roads as ribbons, and indexes footprints in a 25 metre grid so collision is one point-in-polygon test. Places from OpenStreetMap map to the building they sit in, which is how walking into a building knows it's a 7-Eleven.

## How the game stays smooth
Buildings are merged into a handful of meshes. Traffic, lamps and trees are instanced. People are only animated near you. Post effects are desktop only.

## Shipping
`npx wrangler deploy` publishes `site/` and the online worker. Tagging `v*` makes GitHub Actions build every app and attach it to a release. Apps are signed when signing secrets exist, unsigned otherwise.
