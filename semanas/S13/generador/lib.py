# Biblioteca de dibujo SVG para la S13 (lienzo 1180 x 500). Todo el texto >= 14 px.
import html, math, re
from PIL import ImageFont

INK = '#2A2A2A'; GRIS = '#5E5E5E'; VINO = '#A6192E'; VOSC = '#7E1223'; DOR = '#D4AF37'; DOSC = '#9C7B16'
VT = '#F9EEF0'; DT = '#FBF6E7'; GT = '#F4F4F4'; OK = '#2E7D4F'; OKT = '#E8F3EC'; MAL = '#B3261E'; MALT = '#FBEAE8'
W, H = 1180, 500

_F = {}
def _font(size, bold, mono):
    k = (round(size), bold, mono)
    if k not in _F:
        p = '/usr/share/fonts/truetype/liberation/Liberation%s-%s.ttf' % ('Mono' if mono else 'Sans', 'Bold' if bold else 'Regular')
        _F[k] = ImageFont.truetype(p, round(size))
    return _F[k]

def tw(s, size=18, bold=False, mono=False):
    if mono:
        return len(s) * size * 0.6154
    return _font(size, bold, False).getlength(s) * 0.97

def esc(s):
    return html.escape(s, quote=False)

def T(x, y, s, size=18, bold=False, fill=INK, anchor='start', mono=False, italic=False, lh=1.25, op=None):
    """Texto (una cadena o lista de líneas). y = línea base de la primera línea."""
    lines = s if isinstance(s, list) else [s]
    a = ' text-anchor="%s"' % anchor if anchor != 'start' else ''
    st = ' font-weight="700"' if bold else ''
    st += ' font-style="italic"' if italic else ''
    st += ' style="font-family:\'Roboto Mono\',Consolas,monospace"' if mono else ''
    st += ' opacity="%s"' % op if op else ''
    out = []
    for i, l in enumerate(lines):
        out.append('<text x="%g" y="%g"%s font-size="%g"%s fill="%s">%s</text>' % (x, y + i * size * lh, a, size, st, fill, esc(l)))
    return '\n'.join(out)

def R(x, y, w, h, fill='none', stroke=None, sw=2, rx=12, dash=None, op=None):
    s = '<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s"' % (x, y, w, h, rx, fill)
    if stroke: s += ' stroke="%s" stroke-width="%g"' % (stroke, sw)
    if dash: s += ' stroke-dasharray="%s"' % dash
    if op: s += ' opacity="%s"' % op
    return s + '/>'

def C(cx, cy, r, fill='none', stroke=None, sw=2, dash=None):
    s = '<circle cx="%g" cy="%g" r="%g" fill="%s"' % (cx, cy, r, fill)
    if stroke: s += ' stroke="%s" stroke-width="%g"' % (stroke, sw)
    if dash: s += ' stroke-dasharray="%s"' % dash
    return s + '/>'

def I(name, x, y, s, color=VINO):
    return '<use href="#i-%s" x="%g" y="%g" width="%g" height="%g" color="%s"/>' % (name, x, y, s, s, color)

def IC(name, cx, cy, s, color=VINO):
    return I(name, cx - s / 2, cy - s / 2, s, color)

def P(d, fill='none', stroke=INK, sw=3, dash=None, cap='round'):
    s = '<path d="%s" fill="%s" stroke="%s" stroke-width="%g" stroke-linecap="%s" stroke-linejoin="round"' % (d, fill, stroke, sw, cap)
    if dash: s += ' stroke-dasharray="%s"' % dash
    return s + '/>'

def head(x, y, ang, color, sw):
    L = 7 + sw * 2.2; Wd = 4 + sw * 1.3
    bx = x - L * math.cos(ang); by = y - L * math.sin(ang)
    px = -math.sin(ang) * Wd; py = math.cos(ang) * Wd
    return '<polygon points="%g,%g %g,%g %g,%g" fill="%s"/>' % (x, y, bx + px, by + py, bx - px, by - py, color)

def A(x1, y1, x2, y2, color=VINO, sw=4, dash=None, both=False):
    ang = math.atan2(y2 - y1, x2 - x1)
    L = 7 + sw * 2.2
    ex = x2 - (L - 2) * math.cos(ang); ey = y2 - (L - 2) * math.sin(ang)
    sx, sy = x1, y1
    if both:
        sx = x1 + (L - 2) * math.cos(ang); sy = y1 + (L - 2) * math.sin(ang)
    s = '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g" stroke-linecap="round"%s/>' % (
        sx, sy, ex, ey, color, sw, ' stroke-dasharray="%s"' % dash if dash else '')
    s += head(x2, y2, ang, color, sw)
    if both: s += head(x1, y1, ang + math.pi, color, sw)
    return s

def AP(pts, color=VINO, sw=4, dash=None):
    """Flecha con codos: lista de puntos."""
    d = 'M' + ' L'.join('%g,%g' % p for p in pts[:-1])
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ang = math.atan2(y1 - y0, x1 - x0); L = 7 + sw * 2.2
    ex = x1 - (L - 2) * math.cos(ang); ey = y1 - (L - 2) * math.sin(ang)
    d += ' L%g,%g' % (ex, ey)
    return P(d, stroke=color, sw=sw, dash=dash) + head(x1, y1, ang, color, sw)

def CH(cx, cy, r, ok=True):
    col = OK if ok else MAL
    s = C(cx, cy, r, col)
    if ok:
        s += P('M%g,%g L%g,%g L%g,%g' % (cx - .42 * r, cy + .02 * r, cx - .1 * r, cy + .36 * r, cx + .48 * r, cy - .3 * r), stroke='#fff', sw=max(3, r * .2))
    else:
        s += P('M%g,%g L%g,%g M%g,%g L%g,%g' % (cx - .36 * r, cy - .36 * r, cx + .36 * r, cy + .36 * r, cx + .36 * r, cy - .36 * r, cx - .36 * r, cy + .36 * r), stroke='#fff', sw=max(3, r * .2))
    return s

def BADGE(cx, cy, n, color=VINO, r=20, size=20):
    return C(cx, cy, r, color) + T(cx, cy + size * .36, str(n), size, True, '#fff', 'middle')

def NODE(cx, cy, icon, label, sub=None, color=VINO, tint=VT, r=60, isz=80, lsz=22, ssz=17, lab=None):
    s = C(cx, cy, r, tint, color, 2.5) + IC(icon, cx, cy, isz, color)
    ly = cy + r + lsz + 6
    s += T(cx, ly, label, lsz, True, lab or color, 'middle')
    if sub:
        s += T(cx, ly + ssz + 8, sub, ssz, False, GRIS, 'middle')
    return s

def CHIP(x, y, s, size=20, fill=VT, stroke=VINO, color=None, bold=True, anchor='start', padx=16, h=None, icon=None, isz=None, sw=2, mono=False, rx=None):
    """Píldora dimensionada al texto; (x,y) = esquina sup-izq (o centro-x si anchor=middle). Devuelve (svg, ancho, alto)."""
    h = h or size + 22
    isz = isz or h - 14
    w = tw(s, size, bold, mono) + 2 * padx + ((isz + 8) if icon else 0)
    x0 = x - w / 2 if anchor == 'middle' else x
    out = R(x0, y, w, h, fill, stroke, sw, rx if rx is not None else h / 2 if h < 56 else 12)
    tx = x0 + padx
    if icon:
        out += IC(icon, x0 + padx + isz / 2 - 2, y + h / 2, isz, stroke if stroke else VINO)
        tx += isz + 8
    out += T(tx, y + h / 2 + size * .35, s, size, bold, color or (stroke or INK), mono=mono)
    return out, w, h

def chip(x, y, s, **k):
    return CHIP(x, y, s, **k)[0]

_clip = [0]
def _cl(x, y, w, h):
    x2 = min(x + w, 1172); y2 = min(y + h, 492)
    x = max(x, 8); y = max(y, 8)
    return x, y, x2 - x, y2 - y

def FOTO(key, x, y, w, h, rx=14, pos='xMidYMid', zoom=None):
    x, y, w, h = _cl(x, y, w, h)
    _clip[0] += 1
    n = 'clp%d' % _clip[0]
    return ('<clipPath id="%s"><rect x="%g" y="%g" width="%g" height="%g" rx="%g"/></clipPath>'
            '<image href="@@FOTO:%s@@" x="%g" y="%g" width="%g" height="%g" preserveAspectRatio="%s slice" clip-path="url(#%s)"/>'
            % (n, x, y, w, h, rx, key, x, y, w, h, pos, n))

def SCRIM(x, y, w, h, op=.6, rx=0, color='#1d1d1d'):
    x, y, w, h = _cl(x, y, w, h)
    return R(x, y, w, h, color, None, 0, rx, op=op)

def GRAD_SCRIM(x, y, w, h, op=.78, rx=0):
    x, y, w, h = _cl(x, y, w, h)
    _clip[0] += 1
    n = 'gr%d' % _clip[0]
    return ('<linearGradient id="%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d1d1d" stop-opacity="0"/><stop offset="1" stop-color="#1d1d1d" stop-opacity="%s"/></linearGradient>'
            '<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="url(#%s)"/>' % (n, op, x, y, w, h, rx, n))

# ---------- código ----------
KW = {'k': '#E8C56A', 's': '#9BD1A8', 'n': '#8EC3E6', 'c': '#9A9A9A', 'r': '#F2A0A0', 'w': '#F2F2F2', 'v': '#F0B2BE'}
def CODE(x, y, lines, size=20, padx=22, pady=18, w=None, lh=1.45, title=None, fill='#1E1E1E'):
    """lines: lista de líneas; cada línea es lista de (texto, clave_color) o str. Devuelve (svg, w, h)."""
    cw = size * 0.6154
    ls = []
    for l in lines:
        ls.append([(l, 'w')] if isinstance(l, str) else l)
    mx = max(sum(len(t) for t, _ in l) for l in ls)
    tbar = 30 if title else 0
    w = w or mx * cw + 2 * padx + 8
    h = len(ls) * size * lh + 2 * pady + tbar
    out = R(x, y, w, h, fill, None, 0, 12)
    if title:
        out += R(x, y, w, tbar, '#2d2d2d', None, 0, 12) + R(x, y + 14, w, tbar - 14, '#2d2d2d', None, 0, 0)
        out += C(x + 18, y + 15, 5, '#E5645A') + C(x + 36, y + 15, 5, '#E8C56A') + C(x + 54, y + 15, 5, '#6DBE7D')
        out += T(x + w / 2, y + 20, title, 14, False, '#bdbdbd', 'middle')
    for i, l in enumerate(ls):
        cx = x + padx
        by = y + tbar + pady + size * 0.95 + i * size * lh
        for t, k in l:
            out += '<text x="%g" y="%g" style="font-family:\'Roboto Mono\',Consolas,monospace;white-space:pre" font-size="%g" fill="%s" xml:space="preserve">%s</text>' % (cx, by, size, KW.get(k, k), esc(t).replace(' ', ' '))
            cx += len(t) * cw
    return out, w, h

def CALL(x1, y1, x2, y2, n, color=VINO):
    """Llamada numerada: círculo en (x2,y2) y línea desde (x1,y1)."""
    return '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="2.5" stroke-dasharray="5 4"/>' % (x1, y1, x2, y2, color) + BADGE(x2, y2, n, color, 17, 18)

# ---------- glifos propios ----------
def PLUG(cx, cy, s=80, color=VINO, fill='#fff'):
    k = s / 80
    return ('<g transform="translate(%g,%g) scale(%g)" fill="none" stroke="%s" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M-14,-40 V-16 M14,-40 V-16" /><path d="M-26,-16 H26 V8 a26,26 0 0 1 -52,0 Z" fill="%s"/><path d="M0,28 V48 H30"/></g>' % (cx, cy, k, color, fill))

def PAUSE(cx, cy, r=46, color=DOSC):
    return C(cx, cy, r, DT, color, 4) + R(cx - 17, cy - 20, 12, 40, color, None, 0, 3) + R(cx + 5, cy - 20, 12, 40, color, None, 0, 3)

def TOGGLE(x, y, on=True, w=84, h=44):
    col = OK if on else '#9a9a9a'
    kx = x + w - h / 2 if on else x + h / 2
    return R(x, y, w, h, col, None, 0, h / 2) + C(kx, y + h / 2, h / 2 - 5, '#fff')

def BUBBLE(x, y, w, h, fill='#fff', stroke=INK, tail='left', sw=2.5, rx=18):
    out = R(x, y, w, h, fill, stroke, sw, rx)
    if tail == 'left':
        out += '<polygon points="%g,%g %g,%g %g,%g" fill="%s" stroke="%s" stroke-width="%g" stroke-linejoin="round"/>' % (x + 22, y + h - 1, x + 12, y + h + 20, x + 46, y + h - 1, fill, stroke, sw)
        out += '<rect x="%g" y="%g" width="26" height="%g" fill="%s"/>' % (x + 22 + sw / 2, y + h - sw - 1, sw + 2, fill)
    elif tail == 'right':
        out += '<polygon points="%g,%g %g,%g %g,%g" fill="%s" stroke="%s" stroke-width="%g" stroke-linejoin="round"/>' % (x + w - 22, y + h - 1, x + w - 12, y + h + 20, x + w - 46, y + h - 1, fill, stroke, sw)
        out += '<rect x="%g" y="%g" width="26" height="%g" fill="%s"/>' % (x + w - 48 + sw / 2, y + h - sw - 1, sw + 2, fill)
    return out

def SVG(*parts, vb=(0, 0, W, H)):
    return '<svg viewBox="%d %d %d %d">\n%s\n</svg>' % (vb[0], vb[1], vb[2], vb[3], '\n'.join(p for p in parts if p))

# ---------- fotos: créditos ----------
import json, os
FOTOS = json.load(open(os.path.join(os.path.dirname(__file__), 'assets', 'fotos.json')))
def credito(key):
    f = FOTOS[key]
    return 'Foto: %s, Wikimedia Commons (%s)' % (f['autor'].replace('from ', ', ').split(',')[0].strip(), f['licencia'])

# ---------- glosario de siglas ----------
GLOS = [
    ('MCP', 'Model Context Protocol'), ('JSON RPC', 'JSON Remote Procedure Call'), ('JSON', 'JavaScript Object Notation'),
    ('API', 'interfaz de programación de aplicaciones'), ('REST', 'Representational State Transfer'),
    ('HTTP', 'Hypertext Transfer Protocol'), ('SDK', 'kit de desarrollo de software'),
    ('stdio', 'entrada y salida estándar'), ('stdin', 'entrada estándar'), ('stdout', 'salida estándar'),
    ('URI', 'identificador uniforme de recursos'), ('MIME', 'tipo de contenido'), ('IA', 'inteligencia artificial'),
    ('OAuth', 'autorización delegada'), ('OWASP', 'Open Worldwide Application Security Project'),
    ('SIC', 'Superintendencia de Industria y Comercio'), ('RAG', 'generación aumentada por recuperación'),
    ('npm', 'gestor de paquetes de Node'), ('CIDR', ''),
]
def siglas(textos):
    t = ' '.join(textos)
    out = []
    seen = set()
    for k, v in GLOS:
        if not v: continue
        if re.search(r'(?<![\w])%s(?![\w])' % re.escape(k), t):
            if k == 'JSON' and 'JSON RPC' in seen: pass
            out.append('%s = %s' % (k, v)); seen.add(k)
    # JSON RPC ya explica JSON
    if 'JSON RPC' in seen and 'JSON' in seen:
        out = [o for o in out if not o.startswith('JSON = ')]
    return ' · '.join(out)

def linectr(y, size, i, pady=24, title=True, lh=1.45):
    """y del centro vertical de la línea i de un CODE colocado en y."""
    return y + (30 if title else 0) + pady + size * 0.95 + i * size * lh - size * 0.32
