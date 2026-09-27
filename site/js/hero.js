// Detail island: real façades and storefronts for one block, built from data/hero/*.json over the OSM footprints.
// 1 unit = 1 metre, +x east, +z south (same as city.html). Textures are drawn at start-up, no binary assets.
import * as THREE from "three";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";

// upper façade tile: 4 bays wide, 4 storeys tall, so repeat = 1 / (4 * bay) by 1 / (4 * storey)
function facadeTex(s, storey) {
  const c = document.createElement("canvas"); c.width = c.height = 1024; const x = c.getContext("2d");
  x.fillStyle = s.base; x.fillRect(0, 0, 1024, 1024);
  const bw = 256, sh = 256;
  for (let r = 0; r < 4; r++) for (let q = 0; q < 4; q++) {
    const gx = q * bw, gy = r * sh, pad = s.columns ? 40 : 18, top = 30, bot = 26;
    const gr = x.createLinearGradient(gx, gy + top, gx, gy + sh - bot); gr.addColorStop(0, "#9fb6c8"); gr.addColorStop(.35, s.glass); gr.addColorStop(1, "#0b1014");
    x.fillStyle = gr; x.fillRect(gx + pad, gy + top, bw - pad * 2, sh - top - bot);
    x.fillStyle = "rgba(255,255,255,.08)"; x.fillRect(gx + pad + 6, gy + top + 6, (bw - pad * 2) * .3, sh - top - bot - 12);
    x.strokeStyle = s.frame; x.lineWidth = 8; x.strokeRect(gx + pad, gy + top, bw - pad * 2, sh - top - bot);
    x.beginPath(); x.moveTo(gx + bw / 2, gy + top); x.lineTo(gx + bw / 2, gy + sh - bot); x.stroke();
    if (s.columns) { x.fillStyle = "rgba(0,0,0,.12)"; x.fillRect(gx, gy, 14, sh); x.fillStyle = "rgba(255,255,255,.25)"; x.fillRect(gx + 14, gy, 10, sh); }
    x.fillStyle = "rgba(0,0,0,.15)"; x.fillRect(gx, gy + sh - 8, bw, 8);
  }
  for (let i = 0; i < 3000; i++) { x.fillStyle = `rgba(0,0,0,${Math.random() * .05})`; x.fillRect(Math.random() * 1024, Math.random() * 1024, 3, 3); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 16; t.colorSpace = THREE.SRGBColorSpace;
  t.repeat.set(1 / (4 * s.bay), 1 / (4 * storey)); return t;
}

// ground floor along one edge: glazing every 4 m, a door per tenant, tenant names on the sign band
function frontTex(L, tenants, s) {
  const W = Math.max(256, Math.min(1024, Math.round(L * 16))), H = 128, c = document.createElement("canvas"); c.width = W; c.height = H; const x = c.getContext("2d");
  const px = W / L, bandY = 0, bandH = H * .3;
  x.fillStyle = "#23262a"; x.fillRect(0, 0, W, H);
  x.fillStyle = s.frame; x.fillRect(0, bandY, W, bandH);
  for (let m = 0; m < L; m += 4) { const gx = m * px + 6 * px / 4, gw = Math.min(4, L - m) * px - 12 * px / 4;
    const gr = x.createLinearGradient(0, bandH, 0, H); gr.addColorStop(0, "#b8c9d6"); gr.addColorStop(.5, "#3c4c5a"); gr.addColorStop(1, "#1a2229");
    x.fillStyle = gr; x.fillRect(gx, bandH + 8, gw, H - bandH - 8); x.fillStyle = "rgba(255,244,214,.22)"; x.fillRect(gx + gw * .1, bandH + 30, gw * .3, H - bandH - 40); }
  x.textBaseline = "middle"; x.textAlign = "center";
  for (const t of tenants) {
    const cx = t.t * W, w = Math.min(W * .5, Math.max(6 * px, t.name.length * 1.0 * px)), sign = t.color;
    x.fillStyle = sign; x.fillRect(cx - w / 2, bandY + 4, w, bandH - 8);
    x.fillStyle = "#fff"; x.font = `bold ${Math.round(bandH * .55)}px Helvetica, Arial`; x.fillText(t.name, cx, bandY + bandH / 2, w - 20);
    x.fillStyle = "#2b2f33"; x.fillRect(cx - 1.1 * px, bandH + 8, 2.2 * px, H - bandH - 8); x.fillStyle = "#c9d6e0"; x.fillRect(cx - .9 * px, bandH + 14, 1.8 * px, H - bandH - 16); x.fillStyle = "#8a8f94"; x.fillRect(cx + .55 * px, H * .6, .12 * px, .5 * px);
  }
  const t = new THREE.CanvasTexture(c); t.anisotropy = 16; t.colorSpace = THREE.SRGBColorSpace; return t;
}

const SIGN = ["#c0392b", "#1f5e3b", "#2a5fb8", "#111111", "#e0a526", "#6b2d8b", "#d35400"];
const wall = (ax, az, bx, bz, y0, y1, u0, u1, v0, v1) => {
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute([ax, y0, az, bx, y0, bz, bx, y1, bz, ax, y1, az], 3));
  g.setAttribute("uv", new THREE.Float32BufferAttribute([u0, v0, u1, v0, u1, v1, u0, v1], 2)); g.setIndex([0, 1, 2, 0, 2, 3]); g.computeVertexNormals(); return g;
};

export function buildHero(D, spec) {
  const group = new THREE.Group(), skip = new Set(), storey = spec.storey, band = spec.band, upper = {}, tex = {};
  const cap = (p, y) => { const s = new THREE.ShapeGeometry(new THREE.Shape(p.map(([x, z]) => new THREE.Vector2(x, -z)))); s.rotateX(-Math.PI / 2); s.translate(0, y, 0); return s; };
  const roofs = [], fronts = [];
  const pois = (D.pois || []).map(([x, z, kind, name], i) => ({ x, z, kind, name, color: SIGN[i % SIGN.length] }));
  for (const b of spec.buildings) {
    const src = D.buildings[b.id]; if (!src) continue; skip.add(b.id);
    const p = src.p, s = spec.styles[b.style]; if (!(b.style in tex)) { tex[b.style] = facadeTex(s, storey); upper[b.style] = []; }
    // footprint winding: make faces point out
    let area = 0; for (let i = 0; i < p.length; i++) { const [x1, z1] = p[i], [x2, z2] = p[(i + 1) % p.length]; area += x1 * z2 - x2 * z1; }
    const pts = area > 0 ? p : [...p].reverse();
    for (let i = 0; i < pts.length; i++) {
      const [ax, az] = pts[i], [bx, bz] = pts[(i + 1) % pts.length], L = Math.hypot(bx - ax, bz - az); if (L < .5) continue;
      upper[b.style].push(wall(ax, az, bx, bz, band, b.h, 0, L, band, b.h));
      // tenants whose POI sits within 12 m of this edge, projected onto it
      const ten = []; for (const q of pois) { const t = ((q.x - ax) * (bx - ax) + (q.z - az) * (bz - az)) / (L * L); if (t < .03 || t > .97) continue;
        const px = ax + (bx - ax) * t, pz = az + (bz - az) * t; if (Math.hypot(q.x - px, q.z - pz) < 12 && !ten.some(o => Math.abs(o.t - t) * L < 6)) ten.push({ t, name: q.name, color: q.color }); }
      if (L < 6 && !ten.length) { upper[b.style].push(wall(ax, az, bx, bz, 0, band, 0, L, 0, band)); continue; }
      const m = new THREE.Mesh(wall(ax, az, bx, bz, 0, band, 0, 1, 0, 1), new THREE.MeshStandardMaterial({ map: frontTex(L, ten, s), roughness: .3, metalness: .2 }));
      m.castShadow = m.receiveShadow = true; fronts.push(m);
    }
    roofs.push(cap(p, b.h));
    if (b.clock) { // Vancouver Block clock tower: square shaft, four faces, a lantern
      const cx = p.reduce((a, q) => a + q[0], 0) / p.length, cz = p.reduce((a, q) => a + q[1], 0) / p.length;
      const shaft = new THREE.Mesh(new THREE.BoxGeometry(7, 12, 7), new THREE.MeshStandardMaterial({ color: 0xf1ece2, roughness: .6 })); shaft.position.set(cx, b.h + 6, cz); shaft.castShadow = true; group.add(shaft);
      const c = document.createElement("canvas"); c.width = c.height = 256; const x = c.getContext("2d"); x.fillStyle = "#f8f5ee"; x.fillRect(0, 0, 256, 256); x.fillStyle = "#1a1a1a"; x.beginPath(); x.arc(128, 128, 110, 0, 7); x.fill(); x.fillStyle = "#f8f5ee"; x.beginPath(); x.arc(128, 128, 100, 0, 7); x.fill();
      x.strokeStyle = "#1a1a1a"; x.lineWidth = 8; x.beginPath(); x.moveTo(128, 128); x.lineTo(128, 50); x.moveTo(128, 128); x.lineTo(190, 150); x.stroke(); for (let i = 0; i < 12; i++) { x.beginPath(); x.arc(128 + Math.cos(i / 12 * 6.283) * 88, 128 + Math.sin(i / 12 * 6.283) * 88, 5, 0, 7); x.fill(); }
      const ct = new THREE.CanvasTexture(c); ct.colorSpace = THREE.SRGBColorSpace; const fm = new THREE.MeshStandardMaterial({ map: ct, roughness: .5 });
      for (const [dx, dz, ry] of [[0, -3.55, 0], [0, 3.55, Math.PI], [3.55, 0, Math.PI / 2], [-3.55, 0, -Math.PI / 2]]) { const f = new THREE.Mesh(new THREE.PlaneGeometry(5.5, 5.5), fm); f.position.set(cx + dx, b.h + 7, cz + dz); f.rotation.y = ry; group.add(f); }
      const lantern = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 2.2, 4, 8), new THREE.MeshStandardMaterial({ color: 0x3d5a3a, metalness: .3, roughness: .5 })); lantern.position.set(cx, b.h + 14, cz); group.add(lantern);
    }
  }
  for (const k in upper) { if (!upper[k].length) continue; const m = new THREE.Mesh(mergeGeometries(upper[k]), new THREE.MeshStandardMaterial({ map: tex[k], roughness: .4, metalness: .3 })); m.castShadow = m.receiveShadow = true; group.add(m); }
  if (roofs.length) { const m = new THREE.Mesh(mergeGeometries(roofs), new THREE.MeshStandardMaterial({ color: 0x4f5154, roughness: .9 })); m.receiveShadow = true; group.add(m); }
  fronts.forEach(f => group.add(f));
  return { group, skip, fronts: fronts.length, buildings: skip.size };
}
