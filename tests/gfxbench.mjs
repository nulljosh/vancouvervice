// Graphics benchmark: load time, frame rate and GPU load at fixed camera spots, one row per run in docs/BENCHMARK.md.
// node tests/gfxbench.mjs [page=play.html] [label]   (server on :8766 from site/)
import { chromium } from 'playwright';
import { appendFileSync, existsSync, writeFileSync } from 'node:fs';
import { execSync } from 'node:child_process';
const page = process.argv[2] || 'play.html', label = process.argv[3] || execSync('git rev-parse --short HEAD').toString().trim();
const b = await chromium.launch({ channel: 'chrome', args: ['--disable-gpu-vsync', '--disable-frame-rate-limit'] });
const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
await p.addInitScript(() => localStorage.clear());
const t0 = Date.now();
await p.goto(`http://localhost:8766/${page}`, { waitUntil: 'load' }); await p.waitForFunction(() => window.G && window.GS, null, { timeout: 60000 });
const ready = (Date.now() - t0) / 1000;
await p.click('#tNew'); await p.waitForTimeout(300); await p.click('#cardGo'); await p.waitForTimeout(8000);
// [name, camera (x, y, z) in blocks/units, look]
const spots = [['street', [7.07, 26, 7.6], [7.07, 22, 5.6]], ['park', [2.2, 40, 3.9], [2.6, 30, 3.2]], ['skyline', [6.0, 400, 10.5], [9.0, 60, 4.5]]];
const rows = [];
for (const [name, cp, look] of spots) {
  rows.push(await p.evaluate(async ([cp, look]) => {
    document.getElementById('card').style.display = 'none'; G.paused = false;
    window.GS_CAMHOOK = c => { c.position.set(cp[0] * 260, cp[1], cp[2] * 260); c.lookAt(look[0] * 260, look[1], look[2] * 260); };
    await new Promise(r => setTimeout(r, 1500));
    const ts = []; await new Promise(r => { const f = t => { ts.push(t); if (ts.length < 120) requestAnimationFrame(f); else r(); }; requestAnimationFrame(f); });
    const d = ts.slice(1).map((t, i) => t - ts[i]).sort((a, b) => a - b), avg = d.reduce((a, b) => a + b, 0) / d.length;
    return { fps: Math.round(1000 / avg), p95: +d[Math.floor(d.length * .95)].toFixed(1), ...GS.perf() };
  }, [cp, look]));
}
const heap = await p.evaluate(() => performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1e6) : 0);
await b.close();
const md = 'docs/BENCHMARK.md';
if (!existsSync(md)) writeFileSync(md, `# Benchmark\n\nGraphics numbers for every visual change, so a better-looking city never quietly costs the frame rate. Run \`node tests/gfxbench.mjs\` with the site served on :8766. Headless Chrome on the Mac mini M4 at 1280 by 720, vsync off, so frame rates read high; compare rows, not absolutes. Each spot shows frames per second, the slowest 5 percent of frames in ms, draw calls and triangles in thousands.\n\n| Date | Build | Ready s | Street fps / p95 / calls / ktris | Park | Skyline | Heap MB |\n|---|---|---|---|---|---|---|\n`);
const cellOf = r => `${r.fps} / ${r.p95} / ${r.calls} / ${Math.round(r.tris / 1000)}`;
const line = `| ${new Date().toISOString().slice(0, 16).replace('T', ' ')} | ${label} | ${ready.toFixed(1)} | ${rows.map(cellOf).join(' | ')} | ${heap} |\n`;
appendFileSync(md, line); console.log(line.trim());
