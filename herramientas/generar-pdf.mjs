#!/usr/bin/env node
// Genera el PDF (una diapositiva por página, 1280x720) de una o varias presentaciones.
// Uso: node herramientas/generar-pdf.mjs 2026-2-S01-....html [otro.html ...]
import { createRequire } from 'module';
import path from 'path';
const require = createRequire(import.meta.url);
let pw;
for (const c of ['playwright', '/opt/node22/lib/node_modules/playwright']) { try { pw = require(c); break; } catch (e) {} }
if (!pw) { console.error('Falta playwright: npm i -g playwright && npx playwright install chromium'); process.exit(1); }

const browser = await pw.chromium.launch();
for (const f of process.argv.slice(2)) {
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.route(/^https?:\/\//, r => r.abort());
  await page.goto('file://' + path.resolve(f) + '?captura=1');
  await page.waitForSelector('body[data-listo="1"]', { timeout: 20000 });
  await page.emulateMedia({ media: 'print' });
  const out = f.replace(/\.html$/, '.pdf');
  await page.pdf({ path: out, width: '1280px', height: '720px', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  console.log('PDF →', out);
  await page.close();
}
await browser.close();
