import path from "node:path";
import { pathToFileURL } from "node:url";

const { importRuntimeModule } = await import(
  pathToFileURL("C:/Users/GHC/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.11809/skills/presentations/container_tools/runtime_helpers.mjs").href,
);
const { FileBlob, PresentationFile } = await importRuntimeModule("@oai/artifact-tool");
const inputs = process.argv.slice(2);
if (!inputs.length) throw new Error("Pass one or more PPTX paths");

for (const input of inputs) {
  const absolute = path.resolve(input);
  try {
    const presentation = await PresentationFile.importPptx(await FileBlob.load(absolute));
    const snapshot = await presentation.inspect({ kind: "slide", maxChars: 100000 });
    const records = snapshot.ndjson.split(/\r?\n/).filter(Boolean).map(line => JSON.parse(line));
    console.log(`\n=== ${absolute} ===`);
    for (const rec of records) console.log(`${rec.slide}. ${rec.title ?? ""}`);
  } catch (error) {
    console.error(`\n=== ERROR ${absolute} ===\n${error?.message ?? error}`);
  }
}
