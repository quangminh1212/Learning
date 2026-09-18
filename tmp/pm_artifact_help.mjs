import { pathToFileURL } from "node:url";
const { importRuntimeModule } = await import(
  pathToFileURL("C:/Users/GHC/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.11809/skills/presentations/container_tools/runtime_helpers.mjs").href,
);
const { Presentation } = await importRuntimeModule("@oai/artifact-tool");
const presentation = Presentation.create({ slideSize: { width: 1280, height: 720 } });
const queries = process.argv.slice(2);
for (const query of queries) {
  const result = presentation.help("*", { search: query, include: ["index", "examples", "notes"], maxChars: 30000 });
  console.log(`=== ${query} ===`);
  console.log(result.ndjson);
}
