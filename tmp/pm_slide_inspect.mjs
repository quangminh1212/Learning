import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";

const { importRuntimeModule } = await import(
  pathToFileURL("C:/Users/GHC/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.11809/skills/presentations/container_tools/runtime_helpers.mjs").href,
);
const { FileBlob, PresentationFile } = await importRuntimeModule("@oai/artifact-tool");

const inputPaths = process.argv.slice(2);
if (!inputPaths.length) throw new Error("Pass one or more PPTX paths");

for (const inputPath of inputPaths) {
  const absolute = path.resolve(inputPath);
  const presentation = await PresentationFile.importPptx(await FileBlob.load(absolute));
  const snapshot = await presentation.inspect({
    kind: "deck,slide,textbox,shape,image,table,chart,notes,layout",
    maxChars: 200000,
  });
  console.log(`=== ${absolute} ===`);
  console.log(snapshot.ndjson);
  console.log(`=== SLIDE_COUNT ${presentation.slides.count ?? presentation.slides.items?.length ?? "unknown"} ===`);
  const montage = await presentation.export({ format: "webp", montage: true, scale: 1 });
  const montagePath = path.join(path.dirname(absolute), `${path.basename(absolute, path.extname(absolute))}.inspect-montage.webp`);
  await fs.writeFile(montagePath, new Uint8Array(await montage.arrayBuffer()));
  console.log(`=== MONTAGE ${montagePath} ===`);
}
