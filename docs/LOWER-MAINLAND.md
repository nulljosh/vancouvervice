# The Lower Mainland, city by city

Every area is a real-streets map built from OpenStreetMap: `python3 tools/osm.py --area <name>` writes `site/data/<name>.json`, and `city.html?area=<name>` plays it. Add the area to `AREAS` in `tools/osm.py` (centre, then a south-west and north-east corner), to `AREA_NAME` in `site/city.html`, and to the fast travel panel in `site/play.html`.

Real building footprints come from Overture Maps: after the OSM export run `uvx --with duckdb python tools/overture.py --area <name>`. Without them, suburbs (`SUBURB` in `city.html`) fill every residential lot with a house, a gable roof and a yard, and grow firs. Town centres and downtowns keep the extruded towers.

## Order
We take one area to A+ before starting the next: real street names, every landmark, the right kind of houses and trees, the mountains where they really are, signs on the real shops, screenshots checked against photos.

| # | Area | Centre (lat, lon) | Kind | State |
|---|---|---|---|---|
| 1 | Brookswood, Langley | 49.0757, -122.6688 | suburb | live, polishing: real footprints, landmarks by hand |
| 2 | Downtown Vancouver | 49.2833, -123.1187 | downtown | live, polishing |
| 3 | Kitsilano | 49.2690, -123.1575 | suburb | live |
| 4 | Langley City | 49.1044, -122.6604 | town centre | live |
| 5 | Fort Langley | 49.1680, -122.5790 | village | live: real footprints, photo trees, the fort's palisade, heritage false fronts on Glover Road |
| 6 | Walnut Grove | 49.1640, -122.6400 | suburb | live: real footprints, photo trees |
| 7 | Surrey City Centre | 49.1890, -122.8490 | downtown | live: Overture footprints and roads (Overpass was down), photo facades |
| 8 | Cloverdale | 49.1060, -122.7330 | town centre | live: Overture footprints and roads, heritage false fronts on 176 Street |
| 9 | White Rock and South Surrey | 49.0200, -122.8020 | beach town | live: the pier, the White Rock, a sand beach, Overture footprints |
| 10 | Burnaby, Metrotown | 49.2260, -123.0030 | downtown | live: towers on photo facades, SkyTrain guideway, Overture footprints |
| 11 | New Westminster | 49.2010, -122.9120 | town centre | live: the Fraser waterfront, Pier West towers, Overture footprints |
| 12 | Richmond Centre and Steveston | 49.1255, -123.1840 | suburb and village | next: Steveston first |
| 13 | North Vancouver, Lonsdale | 49.3200, -123.0730 | town centre | |
| 14 | West Vancouver, Ambleside | 49.3270, -123.1550 | beach town | |
| 15 | Coquitlam, Port Moody, Port Coquitlam | 49.2840, -122.7930 | suburb | |
| 16 | Delta: Ladner and Tsawwassen | 49.0890, -123.0820 | village | |
| 17 | Maple Ridge and Pitt Meadows | 49.2190, -122.6010 | town centre | |
| 18 | Abbotsford | 49.0500, -122.3040 | town centre | |
| 19 | Mission | 49.1330, -122.3090 | town centre | |
| 20 | Chilliwack | 49.1580, -121.9510 | town centre | |
| 21 | Harrison Hot Springs | 49.2972, -121.7850 | village | live |
| 22 | Victoria (across the water) | 48.4250, -123.3650 | downtown | live |

## Landmarks by hand
A landmark is measured off Esri World Imagery (zoom 20, about 10 cm a pixel): centre, width, depth, roof shape. It goes in `LANDMARKS` or `BUILT` in `city.html`, which clears whatever footprints sit under it. Brookswood has a duplex row on 40 Avenue, the Apostolic Faith Church, the Chevron at 208 Street and Brookswood Secondary.
