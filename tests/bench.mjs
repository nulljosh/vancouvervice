// Run: node tests/bench.mjs. Headless numbers for the README: boot time, frames per 10 s, island build, with and without the detail island.
import { createServer } from 'node:http'; import { readFile } from 'node:fs/promises'; import { fileURLToPath } from 'node:url'; import { chromium } from 'playwright';
const types = { html: 'text/html', js: 'text/javascript', json: 'application/json' };
const server = createServer(async (req, res) => { try { const p = new URL(req.url, 'http://x').pathname; res.writeHead(200, { 'content-type': types[p.split('.').pop()] || 'application/octet-stream' }); res.end(await readFile(fileURLToPath(new URL(`../site${p}`, import.meta.url)))); } catch { res.writeHead(404); res.end(); } });
await new Promise(r => server.listen(0, '127.0.0.1', r));
const browser = await chromium.launch({ headless: true, args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
const rows = [];
for (const hero of ['0', '1']) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } }); await page.routeWebSocket('**/ws', () => {});
  const t0 = Date.now(); await page.goto(`http://127.0.0.1:${server.address().port}/city.html?hero=${hero}`); await page.waitForFunction(() => !!window.S, null, { timeout: 120000 }); const boot = Date.now() - t0;
  const t1 = Date.now(); if (hero === '1') await page.waitForFunction(() => !!window.HERO, null, { timeout: 180000 }); const build = hero === '1' ? Date.now() - t1 : 0;
  const info = hero === '1' ? await page.evaluate(() => HERO[0]) : null;
  await page.evaluate(() => { window.__f = 0; const o = requestAnimationFrame; window.requestAnimationFrame = f => o(t => { window.__f++; f(t); }); });
  await page.waitForTimeout(10000); const frames = await page.evaluate(() => window.__f);
  rows.push({ scene: hero === '1' ? 'downtown + Granville and Georgia island' : 'downtown (OSM extrusions only)', boot_ms: boot, island_build_ms: build, frames_per_10s: frames, buildings: info?.buildings ?? '', frontages: info?.fronts ?? '' });
  await page.close();
}
await browser.close(); server.close(); console.table(rows);
