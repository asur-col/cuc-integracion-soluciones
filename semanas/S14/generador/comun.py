import os, sys, re, html

REPO = '/opt/asur/projects/academy/learning/cuc/2026-2/integracion-soluciones/repositorio/cuc-integracion-soluciones'
HERR = os.path.join(REPO, 'herramientas')
if HERR not in sys.path:
    sys.path.insert(0, HERR)

from lib_svg import *  # noqa: F401,F403

# Colores adicionales suaves manteniendo paleta institucional
AZUL = '#1E5A8A'
AZULT = '#EAF2F8'
MOR = '#6B3FA0'
MORT = '#F3EEF9'

GLOS_S14 = [
    ('LLM', 'modelo grande de lenguaje'),
    ('RAG', 'generación aumentada por recuperación'),
    ('MCP', 'Model Context Protocol'),
    ('BM25', 'búsqueda léxica por relevancia'),
    ('RL', 'aprendizaje por refuerzo'),
    ('API', 'interfaz de programación de aplicaciones'),
    ('JSON RPC', 'JSON Remote Procedure Call'),
    ('JSON', 'JavaScript Object Notation'),
    ('stdio', 'entrada y salida estándar'),
    ('HTTP', 'Hypertext Transfer Protocol'),
    ('PII', 'datos personales identificables'),
    ('SIC', 'Superintendencia de Industria y Comercio'),
    ('OWASP', 'Open Worldwide Application Security Project'),
    ('IA', 'inteligencia artificial'),
    ('AWS', 'Amazon Web Services'),
    ('PDF', 'Portable Document Format'),
    ('SKU', 'código único de producto'),
    ('CLI', 'interfaz de línea de comandos'),
    ('SDK', 'kit de desarrollo de software'),
    ('FAQ', 'preguntas frecuentes'),
    ('SQL', 'lenguaje de consulta estructurado'),
]

def siglas_s14(textos, extra=()):
    t = ' '.join(x for x in textos if x)
    out = []
    seen = set()
    for k, v in GLOS_S14:
        if re.search(r'(?<![\w])%s(?![\w])' % re.escape(k), t):
            if k == 'JSON' and 'JSON RPC' in seen:
                continue
            out.append(f'{k} = {v}')
            seen.add(k)
    for item in extra:
        if item not in out:
            out.append(item)
    res = ' · '.join(out)
    # Limitar a 112 caracteres manteniendo entradas completas
    while len(res) > 112 and ' · ' in res:
        res = res.rsplit(' · ', 1)[0]
    return res

def CODE16(x, y, lines, size=19, padx=22, pady=18, w=None, lh=1.42, title=None, fill='#1E1E1E'):
    """Igual que CODE de lib_svg pero barra de titulo >= 16 px."""
    cw = size * 0.6154
    ls = [[(l, 'w')] if isinstance(l, str) else l for l in lines]
    mx = max(sum(len(t) for t, _ in l) for l in ls)
    tbar = 36 if title else 0
    w = w or mx * cw + 2 * padx + 12
    h = len(ls) * size * lh + 2 * pady + tbar
    out = R(x, y, w, h, fill, None, 0, 12)
    if title:
        out += R(x, y, w, tbar, '#2d2d2d', None, 0, 10)
        out += R(x, y + tbar - 10, w, 10, '#2d2d2d', None, 0, 0)
        out += C(x + 18, y + 18, 5.5, '#E5645A') + C(x + 36, y + 18, 5.5, '#E8C56A') + C(x + 54, y + 18, 5.5, '#6DBE7D')
        out += T(x + w / 2 + 20, y + 24, title, 16, False, '#d0d0d0', 'middle')
    for i, l in enumerate(ls):
        cx = x + padx
        by = y + tbar + pady + size * 0.95 + i * size * lh
        for t, k in l:
            out += '<text x="%g" y="%g" style="font-family:\'Roboto Mono\',Consolas,monospace;white-space:pre" font-size="%g" fill="%s" xml:space="preserve">%s</text>' % (
                cx, by, size, KW.get(k, k), esc(t).replace(' ', '\u00a0'))
            cx += len(t) * cw
    return out, w, h

def linectr16(y, size, i, pady=18, title=True, lh=1.42):
    return y + (36 if title else 0) + pady + size * 0.95 + i * size * lh - size * 0.32

def CARD(x, y, w, h, title, lines, color=VINO, tint=VT, tsz=22, lsz=18, icon=None, rx=16, sw=2.5):
    """Tarjeta segura con titulo y lineas centradas a la izquierda dentro de su rect."""
    out = R(x, y, w, h, tint, color, sw, rx)
    tx = x + 22
    if icon:
        out += IC(icon, x + 42, y + 36, 36, color)
        tx = x + 70
    out += T(tx, y + 43, title, tsz, True, color)
    ly = y + 78
    for ln in lines:
        out += T(x + 22, ly, ln, lsz, False, INK)
        ly += lsz * 1.38
    return out

SLIDES = {}

def add_slide(n, parte, kicker, titulo, sub, fuente, svg, narr, fotos=(), sig_extra=()):
    assert n not in SLIDES, f'Diapositiva duplicada {n}'
    SLIDES[n] = {
        'n': n, 'parte': parte, 'kicker': kicker, 'titulo': titulo, 'sub': sub,
        'fuente': fuente, 'svg': svg, 'narr': narr.strip(),
        'fotos': list(fotos), 'sig_extra': list(sig_extra),
    }
