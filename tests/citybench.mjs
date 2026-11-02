// node tests/citybench.mjs [area] [shotdir]: frame rate, slowest 5% of frames, draw calls and triangles at fixed spots on a real-streets map,
// with a screenshot of each spot when shotdir is given. Site served on :8766. Headless Chrome, so compare rows, not absolutes.
import { chromium } from 'playwright';
const [area = 'brookswood', dir] = process.argv.slice(2);
const SPOTS = { brookswood: [ // [name, spawn x,z, camera x,y,z, look x,y,z]
  ['village', -20, 10, -60, 4, -20, -110, 4, -120], ['40ave', 1300, 112, 1260, 4, 108, 1340, 3, 125], ['duplex', 1326, 105, 1322, 3, 108, 1326, 4.5, 142],
  ['church', 1300, 30, 1302, 2.5, 28, 1277, 4, 56], ['chevron', 1550, 100, 1556, 2.4, 106, 1525, 3.5, 80], ['school', 1724, 612, 1715, 4, 606, 1760, 6, 640],
  ['backfield', 1690, 600, 1700, 9, 600, 1687, 2, 559], ['baker', 0, 0, -40, 30, -40, 960, 60, 500], ['air', 600, 300, 300, 260, 700, 900, 0, 0]] }[area];
const b = await chromium.launch({ channel: 'chrome' }); const rows = [];
for (const [name, sx, sz, ...c] of SPOTS) {
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } }); const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.addInitScript(() => { try { localStorage.setItem('vv-job-backfield', '0'); } catch {} });
  const t0 = Date.now(); await p.goto(`http://localhost:8766/city.html?area=${area}&at=${sx},${sz}`); await p.waitForFunction(() => window.GL && !document.getElementById('load'), null, { timeout: 90000 }); const ready = (Date.now() - t0) / 1000;
  await p.evaluate(c => { window.GS_CAMHOOK = cam => { cam.position.set(c[0], c[1], c[2]); cam.lookAt(c[3], c[4], c[5]); }; }, c); await p.waitForTimeout(2500);
  const r = await p.evaluate(() => new Promise(res => { const ts = []; let last = performance.now(); const f = now => { ts.push(now - last); last = now; if (ts.length < 90) requestAnimationFrame(f); else {
    GL.R.info.autoReset = false; GL.R.info.reset(); GL.R.render(GL.scene, GL.cam); GL.R.info.autoReset = true; const s = ts.slice(5).sort((a, b) => a - b), info = GL.R.info.render; res({ fps: Math.round(1000 / (s.reduce((a, b) => a + b, 0) / s.length)), p95: +s[Math.floor(s.length * .95)].toFixed(1), calls: info.calls, ktris: Math.round(info.triangles / 1000), heap: Math.round((performance.memory?.usedJSHeapSize || 0) / 1e6) }); } }; requestAnimationFrame(f); }));
  if (dir) await p.screenshot({ path: `${dir}/${name}.jpg`, quality: 85 });
  rows.push({ name, ready, ...r, errs: errs.length }); console.log(name, JSON.stringify({ ready, ...r }), errs.slice(0, 2).join(' | ')); await p.close();
}
await b.close();
console.log('| ' + rows.map(r => `${r.name} ${r.fps} / ${r.p95} / ${r.calls} / ${r.ktris}`).join(' | ') + ' |');
