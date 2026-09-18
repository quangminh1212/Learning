import path from "node:path";
import { pathToFileURL } from "node:url";
const { importRuntimeModule } = await import(pathToFileURL("C:/Users/GHC/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.11809/skills/presentations/container_tools/runtime_helpers.mjs").href);
const { FileBlob, PresentationFile } = await importRuntimeModule("@oai/artifact-tool");
const presentation = await PresentationFile.importPptx(await FileBlob.load(path.resolve(process.argv[2])));
for (const id of process.argv.slice(3)) {
  const obj = presentation.resolve(id);
  console.log(`\n${id} type=${obj.type} geometry=${obj.geometry}`);
  console.log("position", obj.position);
  if (obj.text) {
    console.log("text keys", Object.getOwnPropertyNames(obj.text), "text=", obj.text.toString?.());
    console.log("text style", obj.text.style);
    console.log("text style keys", Object.getOwnPropertyNames(obj.text.style ?? {}));
  }
  console.log("fill", obj.fill, "line", obj.line, "style", obj.style);
  const proto = obj.toProto?.();
  if (proto) console.log("proto", JSON.stringify(proto, null, 2).slice(0, 10000));
}
