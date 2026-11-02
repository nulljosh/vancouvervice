// node tests/drive.mjs <outdir> [max seconds]: the whole trip on film. Joshua walks up to a car stopped on 200 Street in Brookswood,
// pulls the driver out, and the autopilot drives the real roads: 200 St north, Highway 1 west, Hastings into downtown Vancouver.
// Records a video of the page (it keeps rolling across the map handoffs), logs the route every 10 s and the trip time at the end.
import { chromium } from 'playwright';
const [out, max = '1500'] = process.argv.slice(2);
const b = await chromium.launch({ channel: 'chrome' });
const ctx = await b.newContext({ viewport: { width: 1280, height: 720 }, recordVideo: { dir: out, size: { width: 1280, height: 720 } } });
const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
const t0 = Date.now(), log = (...a) => console.log(((Date.now() - t0) / 1000).toFixed(0).padStart(5) + 's', ...a);
const ready = () => p.waitForFunction(() => window.S && !document.getElementById('load'), null, { timeout: 120000 });
await p.goto('http://localhost:8766/city.html?area=brookswood&at=-44,160'); await p.evaluate(() => localStorage.removeItem('vv-handoff')); await ready(); await p.waitForFunction(() => traffic.length > 20, null, { timeout: 60000 });
// a car pulls up at the corner: stop one on 200 St just ahead of him
const where = await p.evaluate(() => { let mine = null, bd = 1e9, best = 0; // the car whose street passes closest to him
  for (const c of traffic) for (let d = 0; d < c.l.L; d += 2) { const q = laneAt(c.l, d, c.dir, c.side); const k = Math.hypot(q.x - S.p.x, q.z - S.p.y); if (k < bd) { bd = k; best = d; mine = c; } }
  mine.d = Math.max(0, best - 14 * mine.dir); mine.v = 0; window.MINE = mine; return [mine.l.r.n, Math.round(bd)]; });
log('car stopped on', where); await p.waitForTimeout(2500);
for (let i = 0; i < 60; i++) { const d = await p.evaluate(() => { const g = MINE.g.position; S.a = Math.atan2(g.z - S.p.y, g.x - S.p.x); return Math.hypot(g.x - S.p.x, g.z - S.p.y); });
  if (d < 3.2) break; await p.keyboard.down('KeyW'); await p.waitForTimeout(150); }
await p.keyboard.up('KeyW'); await p.waitForTimeout(400); await p.keyboard.press('KeyE'); await p.waitForTimeout(1500);
log('stolen:', await p.evaluate(() => S.driving && S.carKind.kind), 'stars', await p.evaluate(() => P.stars));
log('route points', await p.evaluate(ts => { window.TS = ts; return AUTO(); }, +process.env.TS || 1));
let last = '';
while ((Date.now() - t0) / 1000 < +max) {
  await p.waitForTimeout(5000);
  const st = await p.evaluate(() => window.S && !document.getElementById('load') ? { area: new URLSearchParams(location.search).get('area'), ll: toLL(S.p.x, S.p.y).map(v => v.toFixed(4)), kmh: Math.round(S.car.v * 3.6), on: document.getElementById('hud').textContent.split('\n')[1], stars: P.stars, i: S.auto?.i, n: S.auto?.path.length, done: !!S.auto?.done, trip: window.TRIP } : null).catch(() => null);
  if (!st) { log('(loading the next map)'); continue; }
  log(JSON.stringify(st));
  if (st.area !== last) { last = st.area; await p.screenshot({ path: `${out}/arrive-${st.area}.jpg`, quality: 85 }); }
  if (st.done && (st.area === 'vancouver' || st.area === 'downtown')) { log('ARRIVED in', st.trip?.toFixed(1), 'minutes'); await p.waitForTimeout(4000); break; }
  if (st.done) { log('autopilot stopped short in', st.area); break; }
}
console.log(errs.length ? 'ERRORS ' + errs.slice(0, 5).join(' | ') : 'no page errors');
await ctx.close(); await b.close();
