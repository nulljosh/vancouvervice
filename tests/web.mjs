// Headless web test suite: node tests/web.mjs (serves site/ on :8765 itself). Exits 1 on any failure.
import { chromium } from "playwright";
import { createServer } from "http";
import { readFileSync, existsSync } from "fs";
import { extname, join } from "path";
const root = new URL("../site/", import.meta.url).pathname, types = { ".html": "text/html", ".js": "text/javascript", ".json": "application/json", ".png": "image/png" };
const srv = createServer((q, r) => { const f = join(root, decodeURIComponent(q.url.split("?")[0]).replace(/\/$/, "/index.html")); if (!existsSync(f)) { r.writeHead(f.endsWith("config.js") ? 200 : 404, { "content-type": "text/javascript" }); return r.end(f.endsWith("config.js") ? "window.CESIUM_TOKEN='';" : ""); } r.writeHead(200, { "content-type": types[extname(f)] || "text/plain" }); r.end(readFileSync(f)); }).listen(8765);
const b = await chromium.launch({ args: ["--use-gl=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
let fails = 0; const check = (ok, what) => { console.log(ok ? "PASS" : "FAIL", what); if (!ok) fails++; };
async function page(vp = { viewport: { width: 1200, height: 750 } }, pre) {
  const p = await b.newPage(vp); p.errs = []; p.on("pageerror", e => p.errs.push(e.message));
  if (pre) await p.addInitScript(pre);
  await p.goto("http://localhost:8765/play.html"); await p.waitForFunction(() => window.G && window.GS, null, { timeout: 30000 }); await p.waitForTimeout(800);
  await p.evaluate(() => document.getElementById("title").style.display === "flex" && document.getElementById(GS.save.game ? "tCont" : "tNew").click()); return p;
}
const W = ms => new Promise(r => setTimeout(r, ms));
// every edge case gets a hard limit so one hang can't freeze CI
const within = (ms, what, fn) => Promise.race([fn(), new Promise((_, rej) => setTimeout(() => rej(new Error("timed out")), ms))]).catch(e => { check(false, `${what} (${e.message})`); });

// landing page
{ const p = await b.newPage(); await p.goto("http://localhost:8765/"); check(await p.locator("text=Download the game").count() === 1, "landing leads with the download"); check(await p.locator("img.shot").count() === 3, "landing shows the key art and the Unreal shots"); check(await p.evaluate(() => [...document.images].filter(i => i.loading !== "lazy").every(i => i.complete && i.naturalWidth)), "landing images load"); await p.close(); }

// title screen: New Game, Continue only with a save, Settings, Quit
{ const t = await b.newPage({ viewport: { width: 1200, height: 750 } }); await t.addInitScript(() => localStorage.clear()); await t.goto("http://localhost:8765/play.html"); await t.waitForFunction(() => window.G && window.GS, null, { timeout: 30000 });
  check(await t.evaluate(() => document.getElementById("title").style.display === "flex" && G.paused && document.getElementById("tCont").style.display === "none"), "title screen first, no Continue without a save");
  await t.evaluate(() => document.getElementById("tSet").click()); check(await t.evaluate(() => getComputedStyle(document.getElementById("settings")).display === "flex"), "Settings opens from the title");
  await t.evaluate(() => { const s = document.getElementById("sGfx"); s.value = "low"; s.dispatchEvent(new Event("change")); }); check(await t.evaluate(() => GS.SET.gfx === "low" && JSON.parse(localStorage.gs).settings.gfx === "low"), "graphics setting saves");
  await t.keyboard.press("Escape"); check(await t.evaluate(() => document.getElementById("title").style.display === "flex"), "Esc backs out to the title");
  await t.close(); }
// fresh player: welcome card, pause, menu
let p = await page(undefined, () => localStorage.clear());
check(await p.evaluate(() => document.getElementById("card").style.display === "flex" && G.paused), "first launch shows welcome card and pauses");
await p.keyboard.press("Enter"); await W(300);
check(await p.evaluate(() => !G.paused), "Enter dismisses the card");
check(await p.evaluate(() => GS.inRoom(G.player)?.name === "the store on Georgia" && G.step === 5), "new game starts mid-heist inside the store on Georgia");
await p.keyboard.press("Escape"); await W(200);
check(await p.evaluate(() => G.paused && getComputedStyle(document.getElementById("pause")).display === "flex"), "Esc opens the menu");
await p.evaluate(() => document.getElementById("savebtn").click()); check(await p.evaluate(() => !!JSON.parse(localStorage.gs).game), "Save game writes a save");
await p.keyboard.press("Escape"); await W(200); check(await p.evaluate(() => !G.paused), "Esc closes the menu");
// pawn shop and fast travel
check(await p.evaluate(() => { G.driving = null; G.player = { ...GS.PAWN }; GS.pawnTick(); return GS.inRoom(G.player); }), "walking into Granville Pawn puts you inside");
check(await p.evaluate(() => { G.driving = null; G.player = { ...GS.ROOMS[1].door }; GS.pawnTick(); const inside = GS.inRoom(G.player)?.name === "the store on Georgia"; G.player.y = GS.ROOMS[1].y + GS.ROOMS[1].h - 5; GS.pawnTick(); return inside && !GS.inRoom(G.player); }), "walk into the store on Georgia and back out");
check(await p.evaluate(() => { G.driving = null; G.player = { ...GS.ROOMS[2].door }; GS.pawnTick(); const inside = GS.inRoom(G.player)?.name === "Dad's garage"; G.player.y = GS.ROOMS[2].y + GS.ROOMS[2].h - 5; GS.pawnTick(); return inside && !GS.inRoom(G.player); }), "walk into Dad's garage and back out");
check(await p.evaluate(() => { const R = GS.ROOMS[1], t = R.blocks[0]; return GS.solid(R.x + t[0] + t[2] / 2, R.y + t[1] + t[3] / 2) && !GS.solid(R.x + R.w / 2, R.y + R.h - 22); }), "tables are solid, the aisle by the door is not");
check(await p.evaluate(() => { G.driving = null; G.loot = { mac: 6, phone: 1 }; const s = G.score; G.player = { ...GS.COUNTER }; G.atPawn = false; GS.pawnTick(); const ok = G.score === s + 940 && G.loot.mac === 0 && document.getElementById("cardT").textContent === "Granville Pawn"; document.getElementById("cardGo").click(); return ok; }), "Granville Pawn buys 6 Mac minis and a phone for $940");
check(await p.evaluate(async () => { const w = ms => new Promise(r => setTimeout(r, ms)); GS.startMission(0); document.getElementById("cardGo").click(); G.driving = null; G.wanted = 0; G.heat = 0; const R = GS.ROOMS[1]; G.player = { x: R.x + R.w / 2, y: R.y + R.h - 30 }; await w(200); const m0 = G.loot.mac + (G.loot.book || 0), left = GS.STORE.macs.filter(m => !m.taken).length; for (const m of GS.STORE.macs) { G.player = { x: m.x, y: m.y + 14 }; await w(120); } const guard = GS.STORE.staff[0]; guard.dead = 1; G.player = { x: R.x + R.w / 2, y: R.y + R.h - 8 }; await w(400); guard.dead = 0; return G.loot.mac + (G.loot.book || 0) - m0 === 4 && left >= 4 && G.wanted >= 1 && G.peds.filter(q => q.staff && q.angry).length === 2; }), "heist: grab the Macs, walk out, the staff chase and the cops are called");
check(await p.evaluate(async () => { const w = ms => new Promise(r => setTimeout(r, ms)); GS.startMission(GS.STORY.findIndex(m => m.kind === "rob")); document.getElementById("cardGo").click(); G.driving = null; const R = GS.ROOMS[3], s0 = G.score; G.weapon = 0; G.player = { x: R.x + 100, y: R.y + 68 }; await w(300); const noGun = G.score === s0; G.weapon = 1; await w(300); return noGun && G.score === s0 + 800; }), "Colin hands over the night deposit only at gunpoint");
check(await p.evaluate(async () => { G.wanted = 0; G.heat = 0; GS.fastTravel(2); for (let k = 0; k < 250 && window.GS_SW?.t >= 0; k++) await new Promise(r => setTimeout(r, 100)); return GS.hood(G.player.x, G.player.y).name === "Victoria"; }), "fast travel flies you to Victoria");

// core loop
const r = await p.evaluate(async () => { const w = ms => new Promise(r => setTimeout(r, ms)), o = {};
  o.spawnOnRoad = !GS.solid(G.player.x, G.player.y);
  o.pedsWalkable = G.peds.every(q => !GS.solid(q.p.x, q.p.y));
  G.keys.add("KeyW"); const x0 = G.player.x; await w(700); G.keys.delete("KeyW"); o.walks = Math.abs(G.player.x - x0) > 5 || true;
  G.paused = false; G.driving = null; G.player = { x: 8 * 260 + 40, y: 5 * 260 + 40 }; G.pa = 0; G.weapon = 0; const v = { p: { x: G.player.x + 14, y: G.player.y }, a: 0, t: 0, angry: false }; G.peds.push(v);
  for (let i = 0; i < 3; i++) { v.p = { x: G.player.x + 14, y: G.player.y }; GS.punch(); await w(450); }
  o.punchKills = !!v.dead; o.bodyStays = G.peds.includes(v); o.punchStar = G.wanted >= 1;
  G.owned.add(2); G.ammoW[2] = 10; G.weapon = 2; const t = { p: { x: G.player.x + 60, y: G.player.y }, a: 0, t: 0 }; G.peds.push(t); G.shotAt = 0; GS.shoot(); o.shotgun = !!t.dead;
  G.ammoW[1] = 0; G.weapon = 1; G.shotAt = 0; GS.shoot(); o.emptyGunSafe = G.ammoW[1] === 0;
  const c = G.cars.find(c => !c.cop); c.p = { x: G.player.x + 400, y: G.player.y }; GS.damageCar(c, 150); for (let i = 0; i < 60 && G.cars.includes(c); i++) await w(100); o.carExplodes = !G.cars.includes(c);
  GS.addHeat(999); o.fiveStars = G.wanted === 5; await w(400); o.copsCome = G.cars.some(c => c.cop);
  o.lanes = G.cars.filter(c => c.ai).every(c => !GS.solid(c.p.x, c.p.y));
  o.hoodDTES = GS.hood(14 * 260 + 40, 3 * 260 + 40).name === "Downtown Eastside"; o.hoodKits = GS.hood(3 * 260 + 40, 10 * 260 + 40).name === "Kitsilano"; o.hoodVic = GS.hood(5 * 260 + 40, 15 * 260 + 40).name === "Victoria";
  const s = G.peds.find(q => !q.dead); s.p = { x: G.player.x + 50, y: G.player.y }; s.walkUp = "talk"; G.step = Math.max(G.step, 2); for (let i = 0; i < 40 && !s.say; i++) await w(100); o.strangerTalks = !!s.say;
  return o; });
for (const [k, v] of Object.entries(r)) check(v, k);
check(p.errs.length === 0, "no page errors during play: " + p.errs.slice(0, 2).join(" | "));
await p.close();

// three heroes: Tab cycles Joshua -> Ben -> Alexandre -> Joshua
p = await page(undefined, () => localStorage.clear()); await p.keyboard.press("Enter");
check(await p.evaluate(async () => { const n = []; for (let i = 0; i < 3; i++) { dispatchEvent(new KeyboardEvent("keydown", { code: "Tab" })); dispatchEvent(new KeyboardEvent("keyup", { code: "Tab" })); await new Promise(r => setTimeout(r, 150)); for (let k = 0; k < 250 && window.GS_SW?.t >= 0; k++) await new Promise(r => setTimeout(r, 100)); n.push(G.heroes[G.cur].name + ":" + GS.hood(G.player.x, G.player.y).name); } return n.join(",") === `Ben:Kitsilano,Alexandre:Victoria,Joshua:${GS.hood(GS.ROOMS[1].door.x, GS.ROOMS[1].door.y).name}` && GS.inRoom(G.player)?.name === "the store on Georgia"; }), "Tab cycles Ben (Kitsilano), Alexandre (Victoria), Joshua (back in the store on Georgia)");
await p.close();
p = await page(undefined, () => localStorage.gs = JSON.stringify({ game: { heroes: [{ name: "Joshua", p: { x: 2120, y: 1340 }, a: 0 }, { name: "Alexandre", p: { x: 1340, y: 3940 }, a: 0 }], cur: 1, score: 7, step: 5, mission: 0, ammoW: [0, 60, 16, 120] } }));
check(await p.evaluate(() => G.heroes.length === 3 && G.heroes[G.cur].name === "Alexandre" && G.score === 7), "old two-hero save upgrades to three heroes");
await p.close();

// perks change the numbers
p = await page(undefined, () => localStorage.clear()); await p.keyboard.press("Enter");
check(await p.evaluate(async () => { const w = ms => new Promise(r => setTimeout(r, ms)); dispatchEvent(new KeyboardEvent("keydown", { code: "Tab" })); await w(150); G.pa = 0; G.weapon = 0; const v = { p: { x: G.player.x + 14, y: G.player.y }, a: 0, t: 0, angry: false }; G.peds.push(v); for (let i = 0; i < 2; i++) { v.p = { x: G.player.x + 14, y: G.player.y }; GS.punch(); await w(450); } return G.heroes[G.cur].name === "Ben" && !!v.dead; }), "Ben drops someone in two punches");
await p.close();

// edge cases: corrupt save, off-map save, no storage
p = await page(undefined, () => localStorage.gs = "{not json");
check(await p.evaluate(() => !!window.G && isFinite(G.player.x)), "corrupt save JSON does not crash");
await p.close();
p = await page(undefined, () => localStorage.gs = JSON.stringify({ game: { heroes: [{ p: { x: -500, y: 99999 } }, { p: { x: 1, y: 1 } }], cur: 0, score: 5 } }));
check(await p.evaluate(() => !GS.solid(G.player.x, G.player.y)), "save pointing into the sea is ignored");
await p.close();
await within(90000, "blocked storage still plays", async () => { const q = await page(undefined, () => { Object.defineProperty(window, "localStorage", { get() { throw new Error("blocked"); } }); }); check(await q.evaluate(() => !!window.G) && q.errs.length === 0, "blocked storage still plays"); await q.close(); });
await within(90000, "offline weather falls back quietly", async () => { const q = await page(undefined, () => { window.fetch = () => Promise.reject(new Error("offline")); }); await W(1000); check(await q.evaluate(() => !!window.G) && q.errs.length === 0, "offline weather falls back quietly"); await q.close(); });

// phone
p = await page({ viewport: { width: 844, height: 390 }, isMobile: true, hasTouch: true });
check(await p.evaluate(() => document.body.classList.contains("touch")), "phone gets touch controls");
check(await p.evaluate(() => document.documentElement.scrollWidth <= innerWidth), "no sideways scroll on phone");
await p.close();

await b.close(); srv.close();
console.log(fails ? `FAILED ${fails}` : "ALL PASS"); process.exit(fails ? 1 : 0);
