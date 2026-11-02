// node tools/merge-clips.mjs base.glb out.glb clip.glb [clip.glb ...]: copy each clip file's animations onto base's skeleton by bone name (needs @gltf-transform/core and /extensions)
import { NodeIO } from '@gltf-transform/core'; import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
const [base, out, ...clips] = process.argv.slice(2), io = new NodeIO().registerExtensions(ALL_EXTENSIONS);
const doc = await io.read(base), root = doc.getRoot(), byName = new Map(root.listNodes().map(n => [n.getName(), n])), buf = root.listBuffers()[0];
for (const f of clips) for (const a of (await io.read(f)).getRoot().listAnimations()) {
  const name = a.getName().split('|')[1] || a.getName(), na = doc.createAnimation(name); let ok = 0;
  for (const ch of a.listChannels()) { const t = byName.get(ch.getTargetNode()?.getName()); if (!t) continue; const s = ch.getSampler();
    const acc = x => doc.createAccessor().setType(x.getType()).setArray(x.getArray().slice()).setBuffer(buf);
    const ns = doc.createAnimationSampler().setInput(acc(s.getInput())).setOutput(acc(s.getOutput())).setInterpolation(s.getInterpolation());
    na.addSampler(ns).addChannel(doc.createAnimationChannel().setTargetNode(t).setTargetPath(ch.getTargetPath()).setSampler(ns)); ok++; }
  console.log(name, 'channels', ok, '/', a.listChannels().length);
}
for (const a of root.listAnimations()) if (a.getName().includes('|')) a.setName(a.getName().split('|')[1]);
await io.write(out, doc); console.log(root.listAnimations().map(a => a.getName()));
