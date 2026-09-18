import path from "node:path";
import { pathToFileURL } from "node:url";
const { importRuntimeModule } = await import(pathToFileURL("C:/Users/GHC/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.11809/skills/presentations/container_tools/runtime_helpers.mjs").href);
const { FileBlob, PresentationFile } = await importRuntimeModule("@oai/artifact-tool");
const presentation = await PresentationFile.importPptx(await FileBlob.load(path.resolve(process.argv[2])));
for (const slideNo of [2,5,9,11]) {
  const slide = presentation.slides.getItem(slideNo - 1);
  console.log(`\nSLIDE ${slideNo}`);
  for (const [name, obj] of [["slide",slide],["shapes",slide.shapes],["images",slide.images],["tables",slide.tables],["charts",slide.charts]]) {
    const protoNames = [];
    let p = obj;
    while (p && p !== Object.prototype && protoNames.length < 4) {
      protoNames.push(...Object.getOwnPropertyNames(p));
      p = Object.getPrototypeOf(p);
    }
    console.log(name, "keys=", Object.keys(obj), "items=", Array.isArray(obj.items) ? obj.items.length : typeof obj.items, "proto=", [...new Set(protoNames)].filter(x=>x!=='constructor').sort().join(","));
    if (Array.isArray(obj.items) && obj.items[0]) {
      let q=obj.items[0], names=[]; let r=q; while(r && r!==Object.prototype && names.length<4){names.push(...Object.getOwnPropertyNames(r));r=Object.getPrototypeOf(r)}
      console.log(" first", [...new Set(names)].filter(x=>x!=='constructor').sort().join(","));
    }
  }
}
