# Benchmark

Graphics numbers for every visual change, so a better-looking city never quietly costs the frame rate. Run `node tests/gfxbench.mjs` with the site served on :8766. Headless Chrome on the Mac mini M4 at 1280 by 720, vsync off, so frame rates read high; compare rows, not absolutes. Each spot shows frames per second, the slowest 5 percent of frames in ms, draw calls and triangles in thousands.

| Date | Build | Ready s | Street fps / p95 / calls / ktris | Park | Skyline | Heap MB |
|---|---|---|---|---|---|---|
| 2026-11-02 06:42 | 802978d (before) | 0.8 | 52 / 21.3 / 1 / 0 | 65 / 16.3 / 1 / 0 | 41 / 26.2 / 1 / 0 | 193 |
| 2026-11-02 06:42 | landmarks, real models, photo facades, street furniture | 1.1 | 24 / 46.5 / 1 / 0 | 30 / 39.1 / 1 / 0 | 18 / 58.9 / 1 / 0 | 226 |
| 2026-11-02 06:44 | 802978d (before) | 0.9 | 50 / 22.5 / 2377 / 6040 | 63 / 16.5 / 1603 / 4185 | 42 / 26 / 3242 / 7187 | 253 |
| 2026-11-02 06:45 | no transmission glass | 1.0 | 45 / 25.4 / 2459 / 13928 | 56 / 33.8 / 1609 / 10725 | 36 / 30 / 3771 / 17342 | 262 |
| 2026-11-02 06:45 | lighter far crowns, 60 near trees | 1.0 | 45 / 24.5 / 2321 / 10120 | 61 / 33.1 / 1445 / 7399 | 36 / 30.7 / 3832 / 15490 | 272 |
