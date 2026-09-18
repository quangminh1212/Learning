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
  const presentation = await PresentationFile.importPptx(await FileBlob.load(absolute));
  const snapshot = await presentation.inspect({ kind: "slide,textbox,table,chart", maxChars: 500000 });
  const records = snapshot.ndjson.split(/\r?\n/).filter(Boolean).map(line => JSON.parse(line));
  const bySlide = new Map();
  for (const rec of records) {
    const slideNo = rec.slide;
    if (!slideNo) continue;
    if (!bySlide.has(slideNo)) bySlide.set(slideNo, []);
    if (rec.kind === "slide") bySlide.get(slideNo).push({type: "TITLE", text: rec.title ?? ""});
    else if (rec.kind === "textbox" && rec.text) bySlide.get(slideNo).push({type: "TEXT", text: rec.text});
    else if (rec.kind === "table") bySlide.get(slideNo).push({type: "TABLE", text: rec.preview ?? ""});
    else if (rec.kind === "chart") bySlide.get(slideNo).push({type: "CHART", text: rec.title ?? rec.chartType ?? ""});
  }
  console.log(`\n=== ${absolute} (${bySlide.size} slides) ===`);
  for (const [slideNo, items] of bySlide.entries()) {
    console.log(`\n[SLIDE ${slideNo}]`);
    for (const item of items) console.log(`${item.type}: ${item.text.replaceAll("\n", " | ")}`);
  }
}
