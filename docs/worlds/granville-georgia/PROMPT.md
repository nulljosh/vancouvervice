# Granville and Georgia

The brief for the first detail island, in the shape of the fable51-worlds prompts.

Build the block around Granville Street and West Georgia Street in downtown Vancouver as a walkable, recognizable place inside the existing OpenStreetMap city (`site/city.html`). Real footprints stay. What changes is the skin: storey-true façades in the material of each building, a glazed ground floor, and every real tenant from the survey as a sign on the frontage it actually sits on.

Cover, at minimum: Pacific Centre with the Apple Store, Hudson's Bay, the Vancouver Block and its clock, the TD Tower, the Scotia Tower, the Rosewood Hotel Georgia and its residences tower, the Metropolitan Hotel, The Hudson.

Rules. Three.js only in the browser. Textures drawn at start-up, no binary assets. One spec (`site/data/hero/granville-georgia.json`) feeds the browser build and the headless Blender export for Unreal (`tools/hero_blender.py`). Every height carries a source and a confidence. Playwright shoots fixed viewpoints (`tests/hero.mjs`) into `qa/`; the builder never grades its own shot.

## Census

Tenants come from the OpenStreetMap place survey in `site/data/vancouver.json`, snapped to the nearest frontage within 12 m. Heights and materials per building are in the spec, each with its source. Three OSM heights were wrong by an order of magnitude (Hotel Georgia, its residences, The Hudson stored storeys as metres) and are overridden there.

## What shipped

Ten buildings, 84 frontages, 69 tenant signs. Unreal import is next: `unreal/assets/hero-granville-georgia.glb`.
