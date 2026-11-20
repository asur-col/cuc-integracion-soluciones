#!/usr/bin/env python3
import os, sys, re, json, html

GEN_DIR = os.path.dirname(os.path.abspath(__file__))
S14_DIR = os.path.dirname(GEN_DIR)
sys.path.insert(0, GEN_DIR)

from comun import SLIDES, credito, siglas_s14
from meta import SEMANA_META
import p1, p2, p3, p4  # noqa: F401

assert len(SLIDES) == 56, f"Esperaba 56 slides, hay {len(SLIDES)}"

PROHIBIDOS = ['→', '/', '&', '±', '~', '*', '_', '`', '#', '<', '>', '(', ')', 'http://', 'https://', 'sumativa', 'Killercoda', 'Play with Docker']

def texto_visible_svg(svg):
    return [html.unescape(re.sub(r'<[^>]+>', '', x)) for x in re.findall(r'<text[^>]*>(.*?)</text>', svg, re.S)]

def limpiar_texto_palabras(t):
    return re.sub(r'\[cite:\d+\]', '', t).split()

avisos = []
partes = {1: [], 2: [], 3: [], 4: []}

for n in range(1, 57):
    s = SLIDES[n]
    k = s['parte']
    fu = s['fuente']
    # Chequear longitudes de metadatos
    if len(s['titulo']) > 65:
        avisos.append(f"S{n} titulo largo ({len(s['titulo'])}): {s['titulo']}")
    if len(s['sub']) > 105:
        avisos.append(f"S{n} sub largo ({len(s['sub'])}): {s['sub']}")
    if len(fu) > 135:
        avisos.append(f"S{n} fuente larga ({len(fu)}): {fu}")
    if '[cite:' in s['svg']:
        avisos.append(f"S{n} contiene [cite:N] dentro del SVG (rompe parser HTML5)")

    # Chequear siglas
    tv = texto_visible_svg(s['svg'])
    sg = siglas_s14([s['titulo'], s['sub']] + tv, extra=s['sig_extra'])

    # Chequear narracion
    narr = s['narr']
    for bad in PROHIBIDOS:
        if bad.lower() in narr.lower():
            avisos.append(f"S{n} simbolo/termino prohibido en narracion: {bad!r}")
    w = len(limpiar_texto_palabras(narr))
    if not (135 <= w <= 145):
        avisos.append(f"S{n} narracion {w} palabras (objetivo 135-145)")

    sec = (
        f'<section data-kicker="{html.escape(s["kicker"])}" '
        f'data-titulo="{html.escape(s["titulo"])}" '
        f'data-sub="{html.escape(s["sub"])}" '
        f'data-fuente="{html.escape(fu)}" '
        f'data-siglas="{html.escape(sg)}">\n'
        f'{s["svg"]}\n'
        f'<aside class="narracion">{html.escape(narr, quote=False)}</aside>\n'
        f'</section>'
    )
    partes[k].append((n, w, sec))

for k in range(1, 5):
    assert len(partes[k]) == 14, f"Parte {k} tiene {len(partes[k])} slides"
    out_p = os.path.join(S14_DIR, f'parte{k}.html')
    with open(out_p, 'w', encoding='utf-8') as f:
        f.write('\n'.join(x[2] for x in partes[k]) + '\n')
    pw = sum(x[1] for x in partes[k])
    dw = len(SEMANA_META['partes'][k - 1]['narracion'].split())
    tot_w = pw + dw
    mins = (tot_w / 135.0 * 60 + 15 * 0.8) / 60.0
    print(f"Parte {k}: 14 slides, {pw}+{dw}={tot_w} palabras (~{mins:.2f} min)")

for f in SEMANA_META['fuentes']:
    if len(f['corta']) > 82:
        avisos.append(f"Fuente {f['n']} corta > 82 ({len(f['corta'])}): {f['corta']}")

out_j = os.path.join(S14_DIR, 'semana.json')
with open(out_j, 'w', encoding='utf-8') as f:
    json.dump(SEMANA_META, f, ensure_ascii=False, indent=2)

if avisos:
    print("\nAVISOS:")
    for a in avisos:
        print(" -", a)
    sys.exit(2)
else:
    print("\nGENERACION LIMPIA SIN AVISOS")
