// node tools/merge-clips.mjs base.glb out.glb clip.glb [clip.glb ...]: copy each clip file's animations onto base's skeleton by bone name (needs @gltf-transform/core and /extensions)
// Clips the base already has are skipped. Translation tracks are scaled by the two skeletons' hip heights, so a shorter body's feet stay on the ground.
import { NodeIO } from '@gltf-transform/core'; import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
const [base, out, ...clips] = process.argv.slice(2), io = new NodeIO().registerExtensions(ALL_EXTENSIONS);
const doc = await io.read(base), root = doc.getRoot(), byName = new Map(root.listNodes().map(n => [n.getName(), n])), buf = root.listBuffers()[0];
const clipName = a => a.getName().split('|')[1] || a.getName(), have = new Set(root.listAnimations().map(clipName)), hipY = r => r.listNodes().find(n => n.getName() === 'Hips')?.getTranslation()[1];
for (const f of clips) { const src = (await io.read(f)).getRoot(), k = process.env.HIPK ? +process.env.HIPK : (hipY(root) && hipY(src)) ? hipY(root) / hipY(src) : 1; // HIPK=1 keeps the clip's own hip height (match clips merged earlier)
  for (const a of src.listAnimations()) { const name = clipName(a); if (have.has(name)) continue; have.add(name); const na = doc.createAnimation(name); let ok = 0;
    for (const ch of a.listChannels()) { const t = byName.get(ch.getTargetNode()?.getName()); if (!t) continue; const s = ch.getSampler(), move = ch.getTargetPath() === 'translation';
      const acc = x => doc.createAccessor().setType(x.getType()).setArray(x.getArray().map(v => move && x === s.getOutput() ? v * k : v)).setBuffer(buf);
      const ns = doc.createAnimationSampler().setInput(acc(s.getInput())).setOutput(acc(s.getOutput())).setInterpolation(s.getInterpolation());
      na.addSampler(ns).addChannel(doc.createAnimationChannel().setTargetNode(t).setTargetPath(ch.getTargetPath()).setSampler(ns)); ok++; }
    console.log(name, 'channels', ok, '/', a.listChannels().length, 'hip scale', k.toFixed(3)); } }
for (const a of root.listAnimations()) if (a.getName().includes('|')) a.setName(clipName(a));
await io.write(out, doc); console.log(root.listAnimations().map(a => a.getName()));
