// Copies the web game's models into godot/assets without Draco or meshopt compression, which Godot can't read.
// Needs: npm i @gltf-transform/core@4 @gltf-transform/extensions@4 draco3dgltf meshoptimizer
// Run: node tools/godot_assets.mjs
import { NodeIO } from "@gltf-transform/core";
import { ALL_EXTENSIONS } from "@gltf-transform/extensions";
import draco3d from "draco3dgltf";
import { MeshoptDecoder } from "meshoptimizer";
import { fileURLToPath } from "node:url";
import path from "node:path";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const MAP = {
  "site/models/characters/hero.glb": "godot/assets/joshua.glb",
  "site/models/characters/people/male_adult_07.glb": "godot/assets/brian.glb",
  "site/models/vehicles/sedan.glb": "godot/assets/sedan.glb",
};
await MeshoptDecoder.ready;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({ "draco3d.decoder": await draco3d.createDecoderModule(), "meshopt.decoder": MeshoptDecoder });
for (const [src, dst] of Object.entries(MAP)) {
  const doc = await io.read(path.join(root, src));
  const used = doc.getRoot().listExtensionsUsed().map(e => e.extensionName);
  for (const e of doc.getRoot().listExtensionsUsed()) if (/draco|meshopt/i.test(e.extensionName)) e.dispose();
  await io.write(path.join(root, dst), doc);
  console.log(src, "->", dst, "had", used.join(",") || "none");
}
