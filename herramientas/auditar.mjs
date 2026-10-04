#!/usr/bin/env node
// Auditoría de una presentación construida con la plantilla v2.
// Uso: node herramientas/auditar.mjs <archivo.html> [--capturas <dir>] [--json <salida.json>]
// Requiere Playwright (npm i -g playwright  ó  NODE_PATH apuntando a una instalación).
import { createRequire } from 'module';
import path from 'path';
import fs from 'fs';
const require = createRequire(import.meta.url);
let pw;
for (const c of ['playwright', '/opt/node22/lib/node_modules/playwright']) { try { pw = require(c); break; } catch (e) {} }
if (!pw) { console.error('Falta playwright: npm i -g playwright && npx playwright install chromium'); process.exit(1); }

const args = process.argv.slice(2);
const archivo = args[0];
const capDir = args.includes('--capturas') ? args[args.indexOf('--capturas') + 1] : null;
const jsonOut = args.includes('--json') ? args[args.indexOf('--json') + 1] : null;
const PPM = 135, PAUSA = 0.8, MIN_FONT = 13;

const browser = await pw.chromium.launch({ args: ['--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
await page.route(/^https?:\/\//, r => r.abort());
await page.goto('file://' + path.resolve(archivo) + '?captura=1');
await page.waitForSelector('body[data-listo="1"]', { timeout: 20000 });
await page.evaluate(() => { document.getElementById('stage').style.transform = 'none'; });

const res = await page.evaluate(({ MIN_FONT }) => {
  const S = [...document.querySelectorAll('.slide')];
  const NARR = window.CURSO.narracion;
  const out = [];
  S.forEach((s, i) => {
    window.CURSO.irA(i);
    const tipo = s.dataset.tipo, parte = +(s.dataset.parte || 1);
    const r = { n: i + 1, tipo, parte, titulo: (s.querySelector('h2,h1')?.textContent || '').trim(), problemas: [] };
    const body = s.querySelector('.s-body');
    if (tipo === 'contenido' && body) {
      const svgs = [...body.querySelectorAll('svg')].filter(v => !v.closest('symbol'));
      const formas = svgs.reduce((a, v) => a + v.querySelectorAll('rect,line,path,circle,ellipse,polygon,polyline,use').length, 0);
      r.grafico = formas >= 6 || body.querySelector('img') !== null;
      r.tabla = !!body.querySelector('table'); r.terminal = !!body.querySelector('.terminal');
      const br = body.getBoundingClientRect();
      // desborde de cualquier elemento fuera del área útil
      let peor = 0, quien = '';
      body.querySelectorAll('*').forEach(e => {
        if (e.closest('svg') && e.tagName.toLowerCase() !== 'svg') return;
        const q = e.getBoundingClientRect(); if (!q.width || !q.height) return;
        const ov = Math.max(q.bottom - br.bottom, q.right - br.right, br.left - q.left, br.top - q.top);
        if (ov > peor) { peor = ov; quien = e.tagName + (e.className && typeof e.className === 'string' ? '.' + e.className : ''); }
      });
      if (peor > 2) r.problemas.push(`desborde ${Math.round(peor)}px (${quien})`);
      // texto HTML recortado dentro de su caja
      body.querySelectorAll('.nota,.reto,.terminal,td,.cifra-cap').forEach(e => {
        if (e.scrollHeight > e.clientHeight + 3 || e.scrollWidth > e.clientWidth + 3) r.problemas.push(`texto recortado en ${e.className || e.tagName}`);
      });
      svgs.forEach(v => {
        if (v.dataset.autoajuste) r.problemas.push(`SVG auto-ajustado (viewBox original ${v.dataset.autoajuste})`);
        const vb = v.viewBox.baseVal; const q = v.getBoundingClientRect();
        if (!vb || !vb.width) return;
        const k = Math.min(q.width / vb.width, q.height / vb.height);
        const textos = [...v.querySelectorAll('text')];
        let chicas = 0, minf = 99;
        textos.forEach(t => { const f = parseFloat(getComputedStyle(t).fontSize) * k; if (f < MIN_FONT) { chicas++; minf = Math.min(minf, f); } });
        if (chicas) r.problemas.push(`${chicas} textos SVG < ${MIN_FONT}px (mín ${minf.toFixed(1)}px)`);
        // etiquetas encimadas
        const cajas = textos.map(t => t.getBoundingClientRect()).filter(b => b.width > 0);
        let enc = 0;
        for (let a = 0; a < cajas.length; a++) for (let b = a + 1; b < cajas.length; b++) {
          const A = cajas[a], B = cajas[b];
          const ix = Math.min(A.right, B.right) - Math.max(A.left, B.left), iy = Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top);
          if (ix > 2 && iy > 2 && ix * iy > 0.25 * Math.min(A.width * A.height, B.width * B.height)) enc++;
        }
        if (enc) r.problemas.push(`${enc} pares de etiquetas SVG encimadas`);
        // texto que se sale de la pantalla del SVG
        textos.forEach(t => { const b = t.getBoundingClientRect(); if (b.right > q.right + 2 || b.left < q.left - 2) r.problemas.push('texto SVG fuera del lienzo: ' + t.textContent.slice(0, 30)); });
      });
      // texto HTML pequeño
      body.querySelectorAll('div,p,li,td,th,span').forEach(e => {
        if (e.closest('svg')) return;
        const own = [...e.childNodes].some(c => c.nodeType === 3 && c.textContent.trim().length > 2);
        if (own && parseFloat(getComputedStyle(e).fontSize) < MIN_FONT) r.problemas.push('texto HTML < ' + MIN_FONT + 'px: ' + e.textContent.trim().slice(0, 30));
      });
    }
    const t = (NARR[i] && NARR[i].texto) || '';
    r.palabras = t ? t.split(/\s+/).length : 0;
    out.push(r);
  });
  return out;
}, { MIN_FONT });

if (capDir) {
  fs.mkdirSync(capDir, { recursive: true });
  for (let i = 0; i < res.length; i++) {
    await page.evaluate(i => window.CURSO.irA(i), i);
    await page.screenshot({ path: path.join(capDir, String(i + 1).padStart(2, '0') + '.png') });
  }
  // Hojas de contacto: 6 diapositivas por imagen (hoja-01.png, …) para revisión visual rápida
  const hoja = await browser.newPage({ viewport: { width: 1290, height: 1100 } });
  for (let h = 0; h * 6 < res.length; h++) {
    const celdas = res.slice(h * 6, h * 6 + 6).map(r => `<figure><img src="data:image/png;base64,${fs.readFileSync(path.resolve(capDir, String(r.n).padStart(2, '0') + '.png')).toString('base64')}"><figcaption>${r.n} · P${r.parte} · ${r.tipo}${r.problemas.length ? ' ⚠' : ''}</figcaption></figure>`).join('');
    await hoja.setContent(`<style>body{margin:0;background:#333;display:grid;grid-template-columns:640px 640px;gap:6px;padding:2px;font:14px sans-serif;color:#fff}figure{margin:0}img{width:640px;height:360px;display:block}figcaption{padding:2px 4px}</style>${celdas}`);
    await hoja.waitForTimeout(150);
    await hoja.screenshot({ path: path.join(capDir, 'hoja-' + String(h + 1).padStart(2, '0') + '.png'), fullPage: true });
  }
}
await browser.close();

// Resumen
const cont = res.filter(r => r.tipo === 'contenido');
const div = res.filter(r => r.tipo === 'divisoria');
console.log(`\n# ${path.basename(archivo)}`);
console.log(`Diapositivas: ${res.length} · divisorias: ${div.length} · contenido: ${cont.length} · con gráfico: ${cont.filter(r => r.grafico).length} (${Math.round(100 * cont.filter(r => r.grafico).length / Math.max(1, cont.length))} %)`);
for (let p = 1; p <= 4; p++) {
  const it = res.filter(r => r.parte === p);
  const w = it.reduce((a, r) => a + r.palabras, 0);
  const min = (w / PPM * 60 + PAUSA * it.length) / 60;
  const c = it.filter(r => r.tipo === 'contenido');
  const flag = (min < 13.5 || min > 16.5) ? '  ⚠ fuera de 13.5–16.5 min' : '';
  console.log(`  Parte ${p}: ${c.length} de contenido (${c.filter(r => r.grafico).length} con gráfico) · ${w} palabras ≈ ${min.toFixed(1)} min${flag}`);
}
const sinNarr = res.filter(r => r.palabras === 0 && r.tipo !== 'fuentes');
if (sinNarr.length) console.log('  ⚠ sin narración: ' + sinNarr.map(r => r.n).join(', '));
const sinGraf = cont.filter(r => !r.grafico);
if (sinGraf.length) console.log('  · sin gráfico: ' + sinGraf.map(r => `${r.n}${r.tabla ? '(tabla)' : r.terminal ? '(terminal)' : ''}`).join(', '));
const prob = res.filter(r => r.problemas.length);
console.log(prob.length ? `  ⚠ ${prob.length} diapositivas con problemas:` : '  ✓ sin problemas de maquetación');
prob.forEach(r => console.log(`    ${r.n} «${r.titulo.slice(0, 55)}»: ${[...new Set(r.problemas)].slice(0, 4).join(' | ')}`));
if (jsonOut) fs.writeFileSync(jsonOut, JSON.stringify(res, null, 1));
process.exit(prob.length ? 3 : 0);
