// Run: node tests/roam.mjs. Free roam: walk off a town's map onto the corridor, and arrive in a town from it.
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const types = { html: 'text/html', js: 'text/javascript', json: 'application/json', png: 'image/png', jpg: 'image/jpeg', glb: 'model/gltf-binary' };
const server = createServer(async (req, res) => {
  try {
    const path = new URL(req.url, 'http://localhost').pathname;
    const data = await readFile(fileURLToPath(new URL(`../site${path}`, import.meta.url)));
    res.writeHead(200, { 'content-type': types[path.split('.').pop()] || 'application/octet-stream' });
    res.end(data);
  } catch { res.writeHead(404); res.end(); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const base = `http://127.0.0.1:${server.address().port}/city.html`;
let browser;
try {
  browser = await chromium.launch({ headless: true, args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 640, height: 360 } });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.routeWebSocket('**/ws', () => {});
  const boot = async area => { await page.goto(`${base}?area=${area}`); await page.waitForFunction(() => !!window.S, null, { timeout: 180000 }); };
  const handoff = () => page.evaluate(() => { portal(); return JSON.parse(localStorage.getItem('vv-handoff') || 'null'); });

  // On foot in Chilliwack, past the east edge of the map: hands off to the corridor, still on foot.
  await boot('chilliwack');
  const out = await page.evaluate(() => { S.driving = false; S.p.set(EDGE[1] + 40, (EDGE[2] + EDGE[3]) / 2); S.arrive.set(-1e6, -1e6); return true; });
  assert(out);
  const h1 = await handoff();
  assert.equal(h1?.to, 'corridor', 'walking off Chilliwack hands off to the corridor');
  assert.equal(h1.drive, false, 'the handoff keeps you on foot');
  assert.deepEqual(errors, [], 'Chilliwack boots and hands off without errors');

  // The page carries on to the corridor by itself and you arrive on foot. Then stand in Abbotsford: hands off into the town.
  await page.waitForURL(/area=corridor/, { timeout: 30000 });
  await page.waitForFunction(() => !!window.S, null, { timeout: 180000 });
  assert.equal(await page.evaluate(() => S.driving), false, 'arrive on the corridor on foot');
  const h2 = await page.evaluate(() => { const [x, z] = LL(TOWNS.abbotsford); S.p.set(x, z); S.arrive.set(-1e6, -1e6); portal(); return JSON.parse(localStorage.getItem('vv-handoff') || 'null'); });
  assert.equal(h2?.to, 'abbotsford', 'the corridor hands off into Abbotsford');
  assert.deepEqual(errors, [], 'no errors on the corridor');
  console.log('PASS free roam: town edge to corridor on foot, corridor into a town');
} finally {
  await browser?.close();
  await new Promise(resolve => server.close(resolve));
}
