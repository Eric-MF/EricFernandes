// Uso: node cdp.mjs <url> <largura> <altura> <pastaSaida> <y1,y2,...>
import { spawn } from "node:child_process";
import { writeFileSync, mkdirSync } from "node:fs";
const [url, largura, altura, saida, posicoes] = process.argv.slice(2);
const chrome = spawn(process.env.HOME + "/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell",
  ["--no-sandbox", "--hide-scrollbars", "--remote-debugging-port=9333", "about:blank"], { stdio: "ignore" });
const espera = ms => new Promise(r => setTimeout(r, ms));
let alvo;
for (let i = 0; i < 40 && !alvo; i++) { await espera(250); try { alvo = (await (await fetch("http://127.0.0.1:9333/json/list")).json()).find(t => t.type === "page"); } catch {} }
const ws = new WebSocket(alvo.webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);
let id = 0; const pendentes = new Map();
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pendentes.has(m.id)) { pendentes.get(m.id)(m.result); pendentes.delete(m.id); } };
const cmd = (method, params = {}) => new Promise(r => { const n = ++id; pendentes.set(n, r); ws.send(JSON.stringify({ id: n, method, params })); });
const avaliar = async expr => (await cmd("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true })).result?.value;
const movel = Number(largura) < 700;
await cmd("Emulation.setDeviceMetricsOverride", { width: +largura, height: +altura, deviceScaleFactor: 1, mobile: movel });
await cmd("Page.enable");
await cmd("Page.navigate", { url });
await espera(1500);
await avaliar(`localStorage.setItem("consentimento-cookies", JSON.stringify({estatisticas:false,mapa:false,versao:1,data:"teste"})); location.reload(); 1`);
await espera(2000);
mkdirSync(saida, { recursive: true });
console.log("altura da página:", await avaliar("document.documentElement.scrollHeight"));
let n = 0;
for (const y of posicoes.split(",").map(Number)) {
  await avaliar(`document.documentElement.style.scrollBehavior="auto"; scrollTo(0, ${y}); 1`);
  await espera(1400);
  const foto = await cmd("Page.captureScreenshot", { format: "png" });
  writeFileSync(`${saida}/${String(n++).padStart(2, "0")}-${y}.png`, Buffer.from(foto.data, "base64"));
}
ws.close(); chrome.kill();
