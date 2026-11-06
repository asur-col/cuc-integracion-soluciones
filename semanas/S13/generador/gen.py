#!/usr/bin/env python3
# Genera semanas/S13/parte1..4.html (diseño visual v2) conservando títulos y narraciones de semanas/S13_orig.
import re, sys, os, json, html
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

RAIZ = os.path.dirname(os.path.abspath(__file__))
SEC = re.compile(r"<section\b([^>]*)>(.*?)</section>", re.S)
ORIG = []
for k in range(1, 5):
    t = open(f'{RAIZ}/semanas/S13_orig/parte{k}.html', encoding='utf-8').read()
    for a, c in SEC.findall(t):
        at = dict(re.findall(r'([\w-]+)\s*=\s*"([^"]*)"', a))
        narr = re.search(r'<aside class="narracion">(.*?)</aside>', c, re.S).group(1)
        ORIG.append(dict(k=k, kicker=at['data-kicker'], titulo=at['data-titulo'], sub=at.get('data-sub', ''), fuente=at['data-fuente'], narr=narr))
assert len(ORIG) == 56

from reg import SL, slide

def fuente_base(f):
    if ' = ' in f:
        i = min([f.find(x) for x in ('Fuente:', 'Basado') if f.find(x) >= 0])
        f = f[i:]
    return f.replace('Diagrama: elaboración propia', 'Dibujo propio')

NARR_FIX = [
    ('Los servidores ya no cuelgan directamente de mcp. Ahora van bajo mcp servers con un nombre único.',
     'Los servidores van bajo mcp servers con un nombre único, que es la forma recomendada.'),
    ('El formato viejo con enabled ya no aplica. Si copian ese ejemplo de Context7 sin actualizar, la conexión fallará.',
     'En opencode dos punto cero punto treinta y uno funcionan ambos formatos: mcp servers y el de la semana doce, con mcp directo y enabled. En este curso usamos mcp servers como forma recomendada. No mezclen los dos formatos en un mismo archivo.'),
    ('El registro usa el formato vigente de opencode versión dos.', 'El registro usa el formato recomendado de opencode versión dos.'),
    ('registro en opencode usa el formato vigente con mcp servers local', 'registro en opencode usa el formato recomendado con mcp servers local'),
]

def texto_visible(svg):
    return re.findall(r'<text[^>]*>(.*?)</text>', svg, re.S)

def render():
    import slides1, slides2, slides3, slides4  # registran en SL
    for n in range(1, 57):
        assert n in SL, f'falta diapositiva {n}'
    for k in range(1, 5):
        out = []
        for n in range(1, 57):
            o = ORIG[n - 1]
            if o['k'] != k: continue
            s = SL[n]
            titulo = s['titulo'] or o['titulo']; sub = s['sub'] if s['sub'] is not None else o['sub']
            fu = s['fuente'] or fuente_base(o['fuente'])
            for f in s['fotos']:
                fu += ' · ' + credito(f)
            tv = [html.unescape(re.sub('<[^>]+>', '', x)) for x in texto_visible(s['body'])]
            sg = siglas([titulo, sub] + tv + list(s['sig']))
            narr = o['narr']
            for a, b in NARR_FIX:
                narr = narr.replace(a, b)
            out.append('<section data-kicker="%s" data-titulo="%s" data-sub="%s" data-fuente="%s" data-siglas="%s">\n%s\n<aside class="narracion">%s</aside>\n</section>' % (
                o['kicker'], titulo, sub, fu, sg, s['body'], narr))
        open(f'{RAIZ}/semanas/S13/parte{k}.html', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    # semana.json: ajuste de la narración de la parte 3 y textos cortos de fuentes
    m = json.load(open(f'{RAIZ}/semanas/S13_orig/semana.json', encoding='utf-8'))
    m['partes'][2]['narracion'] = m['partes'][2]['narracion'].replace('con su formato vigente', 'con su formato recomendado')
    cortas = json.load(open(f'{RAIZ}/fuentes_cortas.json', encoding='utf-8'))
    for f in m['fuentes']:
        f['corta'] = cortas[str(f['n'])]
    json.dump(m, open(f'{RAIZ}/semanas/S13/semana.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('ok', len(SL))

if __name__ == '__main__':
    render()
