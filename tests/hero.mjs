// Run: node tests/hero.mjs. Boots the real city, checks the Granville and Georgia island built, shoots the QA viewpoint.
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { readFile, mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const types = { html: 'text/html', js: 'text/javascript', json: 'application/json', png: 'image/png', glb: 'model/gltf-binary' };
const server = createServer(async (req, res) => {
  try { const path = new URL(req.url, 'http://localhost').pathname; const data = await readFile(fileURLToPath(new URL(`../site${path}`, import.meta.url)));
    res.writeHead(200, { 'content-type': types[path.split('.').pop()] || 'application/octet-stream' }); res.end(data); } catch { res.writeHead(404); res.end(); }
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
let browser;
try {
  browser = await chromium.launch({ headless: true, args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const errors = []; page.on('pageerror', e => errors.push(e.message)); page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await page.routeWebSocket('**/ws', () => {});
  await page.goto(`http://127.0.0.1:${server.address().port}/city.html`);
  await page.waitForFunction(() => !!window.S && window.HERO, null, { timeout: 120000 });
  const hero = await page.evaluate(() => HERO[0]);
  assert.equal(hero.name, 'Granville and Georgia');
  assert.equal(hero.buildings, 10, 'all ten spec buildings resolved to footprints');
  assert(hero.fronts >= 20, `storefront frontages built (${hero.fronts})`);
  assert.deepEqual(errors, [], 'island builds without errors');
  // QA viewpoint: stand on Granville, look at the Vancouver Block clock
  await page.evaluate(() => { const v = HERO[0].viewpoint; S.p.set(v.x, v.z); S.a = Math.atan2(v.look[1] - v.z, v.look[0] - v.x); });
  await page.waitForLoadState('networkidle', { timeout: 90000 }); await page.waitForTimeout(1500);
  const dir = new URL('../docs/worlds/granville-georgia/qa/', import.meta.url); await mkdir(dir, { recursive: true });
  await page.screenshot({ path: fileURLToPath(new URL("viewpoint.png", dir)), timeout: 180000 });
  await page.evaluate(() => { S.p.set(-4, 8); S.a = Math.atan2(16 - 8, 8 - -4); }); await page.waitForTimeout(800);
  await page.screenshot({ path: fileURLToPath(new URL("apple-store.png", dir)), timeout: 180000 });
  console.log(`ok: ${hero.buildings} buildings, ${hero.fronts} frontages, shots in docs/worlds/granville-georgia/qa/`);
} finally { await browser?.close(); server.close(); }
