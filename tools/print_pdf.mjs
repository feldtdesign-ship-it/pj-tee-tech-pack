// Print an HTML file to PDF through Chrome's DevTools connection.
// Chrome's own --print-to-pdf flag hangs on this Mac (Chrome 153), so build.py uses this instead.
// No installs: Node 22+ has fetch and WebSocket built in.
// Usage: node tools/print_pdf.mjs <chrome> <in.html> <out.pdf>
import { spawn } from "node:child_process";
import { mkdtempSync, readFileSync, writeFileSync, existsSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const [chrome, inFile, outFile] = process.argv.slice(2);
const prof = mkdtempSync(join(tmpdir(), "pjpdf-"));
const ch = spawn(chrome, ["--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  "--remote-debugging-port=0", `--user-data-dir=${prof}`, "about:blank"], { stdio: "ignore" });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const fail = m => { console.error(m); cleanup(); process.exit(1); };
function cleanup() { try { ch.kill("SIGKILL"); } catch {} try { rmSync(prof, { recursive: true, force: true }); } catch {} }
const timer = setTimeout(() => fail("timed out after 150 s"), 150000);

let port;
for (let i = 0; i < 100 && !port; i++) {
  const f = join(prof, "DevToolsActivePort");
  if (existsSync(f)) port = readFileSync(f, "utf8").split("\n")[0].trim();
  else await sleep(100);
}
if (!port) fail("Chrome did not open its DevTools port");

const pages = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
const ws = new WebSocket(pages.find(p => p.type === "page").webSocketDebuggerUrl);
await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
let id = 0; const wait = new Map(), events = [];
ws.onmessage = m => { const d = JSON.parse(m.data); if (d.id && wait.has(d.id)) { wait.get(d.id)(d); wait.delete(d.id); } else if (d.method) events.push(d.method); };
const send = (method, params = {}) => new Promise(r => { const i = ++id; wait.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });

await send("Page.enable");
await send("Page.navigate", { url: pathToFileURL(resolve(inFile)).href });
for (let i = 0; i < 600 && !events.includes("Page.loadEventFired"); i++) await sleep(100);
await send("Runtime.evaluate", { expression: "document.fonts.ready.then(()=>true)", awaitPromise: true });
const res = await send("Page.printToPDF", { printBackground: true, preferCSSPageSize: true, marginTop: 0, marginBottom: 0, marginLeft: 0, marginRight: 0 });
if (!res.result || !res.result.data) fail("printToPDF failed: " + JSON.stringify(res.error || res).slice(0, 300));
writeFileSync(outFile, Buffer.from(res.result.data, "base64"));
clearTimeout(timer); ws.close(); cleanup();
console.log("ok", outFile);
