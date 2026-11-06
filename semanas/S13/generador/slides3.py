from lib import *
from reg import slide

# 29 · Mapa: de la teoría al código en 6 pasos  (foto a sangre + ruta)
b = [FOTO('programador', 0, 0, 1180, 500, 18, 'xMidYMid'), SCRIM(0, 0, 1180, 500, .28, 18), GRAD_SCRIM(0, 170, 1180, 330, .88, 18)]
b.append(chip(30, 28, 'De la teoría al código en 6 pasos', size=32, fill=VINO, stroke=None, color='#fff', h=64, padx=26))
steps = ['CREAR', 'HERRAMIENTA', 'VALIDAR', 'INSTALAR', 'REGISTRAR', 'PROBAR']
widths = [tw(s, 22, True) + 28 + 56 for s in steps]
gap = (1120 - sum(widths)) / 5
x = 30
for i, s in enumerate(steps):
    b.append(R(x, 380, widths[i], 76, '#fff', None, 0, 14)); b.append(BADGE(x + 30, 418, i + 1, VINO, 18, 20)); b.append(T(x + 56, 426, s, 22, True, VINO))
    if i < 5: b.append(A(x + widths[i] + 3, 418, x + widths[i] + gap - 3, 418, DOR, 4))
    x += widths[i] + gap
slide(29, SVG(*b), fotos=['programador'])

# 30 · Las piezas del laboratorio  (zona + flujo)
b = [R(300, 40, 860, 400, GT, '#9a9a9a', 2.5, 20, dash='10 7'), T(330, 84, 'TU MÁQUINA', 22, True, GRIS)]
b.append(NODE(130, 220, 'usuario', 'ESTUDIANTE', 'pregunta y revisa', INK, GT, r=66, isz=84, lsz=24, ssz=19))
b.append(NODE(450, 220, 'codigo', 'OPENCODE', 'host MCP local', VINO, '#fff', r=66, isz=84, lsz=24, ssz=19))
b.append(NODE(740, 220, 'servidor', 'SERVER.JS', 'servidor MCP stdio', INK, '#fff', r=66, isz=84, lsz=24, ssz=19))
b.append(NODE(1040, 220, 'bd', 'PEDIDOS.JSON', 'lee los datos', DOSC, '#fff', r=66, isz=84, lsz=24, ssz=19))
b.append(A(200, 220, 380, 220, INK, 5)); b.append(A(522, 220, 668, 220, VINO, 5, both=True)); b.append(A(812, 220, 968, 220, DOSC, 5))
b.append(T(290, 196, 'pregunta', 20, True, INK, 'middle')); b.append(T(595, 196, 'stdio', 20, True, VINO, 'middle')); b.append(T(890, 196, 'lee', 20, True, DOSC, 'middle'))
slide(30, SVG(*b))

# 31 · package.json  (código con anotaciones)
cd, w, h = CODE(30, 40, [[('{', 'w')], [('  "type"', 'k'), (': ', 'w'), ('"module"', 's'), (',', 'w')], [('  "dependencies"', 'k'), (': {', 'w')],
                         [('    "@modelcontextprotocol/sdk"', 'k'), (': ', 'w'), ('"..."', 's'), (',', 'w')], [('    "zod"', 'k'), (': ', 'w'), ('"..."', 's')], [('  }', 'w')], [('}', 'w')]], size=26, padx=26, pady=24, title='package.json')
b = [cd]
X = 30 + w + 8
for i, n, col, t1, t2, ty in ((1, 1, VINO, 'ESM nativo de Node', None, 118), (3, 2, DOSC, 'SDK oficial MCP', None, 232), (4, 3, OK, '¿Por qué zod?', 'declara reglas en código', 340)):
    b.append(CALL(X, linectr(40, 26, i), X + 70, ty - 6, n, col)); b.append(T(X + 102, ty, t1, 26, True, col))
    if t2: b.append(T(X + 102, ty + 32, t2, 22, False, GRIS))
slide(31, SVG(*b))

# 32 · server.js  (código + resultado)
cd, w, h = CODE(30, 30, [[('server.tool', 'k'), ('(', 'w')], [('  "consultar_pedido"', 's'), (',', 'w')], [('  schema', 'n'), (',', 'w')], [('  async ', 'k'), ('({ pedidoId }) => {', 'w')],
                         [('    ', 'w'), ('return { estado, cliente }', 'w')], [('  }', 'w')], [(')', 'w')]], size=26, padx=26, pady=24, title='server.js · esqueleto')
b = [cd]
X = 30 + w + 8
b.append(CALL(X, linectr(30, 26, 1), X + 60, 100, 1)); b.append(T(X + 92, 106, 'nombre', 24, True, VINO))
b.append(CALL(X, linectr(30, 26, 2), X + 60, 168, 2, DOSC)); b.append(T(X + 92, 174, 'esquema', 24, True, DOSC))
b.append(CALL(X, linectr(30, 26, 4), X + 60, 236, 3, OK)); b.append(T(X + 92, 242, 'lógica', 24, True, OK))
b.append(A(w + 20, 395, 780, 395, OK, 4)) if False else None
b.append(R(X, 320, 1150 - X, 150, OKT, OK, 3, 16)); b.append(T(X + 30, 410, 'Pedido 1001:', 34, True, INK)); b.append(T(X + 30, 452, 'estado enviado', 34, True, OK))
slide(32, SVG(*b))

# 33 · Validación con zod antes de ejecutar  (embudo)
b = []
s, w, h = CODE(30, 20, [[('pedidoId', 'k'), (': z.number().int().positive()', 'w')]], size=26, padx=22, pady=18, title=None)
b.append(s)
b.append(T(30 + w + 20, 66, 'esquema zod', 22, True, GRIS))
b.append(NODE(100, 250, 'usuario', 'ENTRADA', None, INK, GT, r=56, isz=72, lsz=22))
b.append(A(166, 250, 450, 250, INK, 5))
b.append(R(450, 150, 120, 200, DT, DOSC, 4, 16)); b.append(IC('escudo', 510, 230, 80, DOSC)); b.append(T(510, 385, 'ZOD', 26, True, DOSC, 'middle'))
b.append(T(510, 140, 'el SDK valida solo', 22, True, DOSC, 'middle'))
b.append(A(574, 220, 760, 220, OK, 5)); b.append(CH(660, 190, 22, True)) if False else None
b.append(NODE(850, 220, 'funcion', 'MANEJADOR', 'antes de llamarlo', OK, OKT, r=66, isz=84, lsz=24, ssz=19))
b.append(A(924, 220, 1040, 220, OK, 5)); b.append(IC('bd', 1100, 220, 80, OK))
b.append(AP([(510, 352), (510, 430), (640, 430)], MAL, 5)); b.append(CH(690, 430, 30, False))
b.append(T(740, 424, 'RECHAZADO', 26, True, MAL)); b.append(T(740, 456, 'texto o negativo: nunca llega a la base', 20, False, INK))
slide(33, SVG(*b))

# 34 · Instalación y arranque stdio  (antes / después)
b = [R(10, 20, 570, 330, MALT, MAL, 3, 20), R(600, 20, 570, 330, OKT, OK, 3, 20)]
b.append(CH(60, 70, 24, False)); b.append(T(100, 82, 'PROHIBIDO', 32, True, MAL)); b.append(CH(650, 70, 24, True)); b.append(T(690, 82, 'PERMITIDO', 32, True, OK))
c1, w1, h1 = CODE(40, 120, [[('console.log', 'r'), ('("listo")', 'w')]], size=28, padx=24, pady=22); b.append(c1)
c2, w2, h2 = CODE(630, 120, [[('console.error', 'k'), ('("listo")', 'w')]], size=28, padx=24, pady=22); b.append(c2)
b.append(T(40, 280, 'rompe el protocolo stdio', 28, True, MAL)); b.append(T(630, 280, 'sale por error, protocolo intacto', 28, True, OK))
b.append(R(300, 385, 580, 90, GT, INK, 2.5, 45)); b.append(IC('contenedor', 360, 430, 56, INK)); b.append(T(410, 422, 'npm install', 30, True, INK, mono=True)); b.append(T(410, 454, 'instala SDK y zod locales', 20, False, GRIS))
slide(34, SVG(*b))

# 35 · Registro en opencode.json  (código + recomendación)
cd, w, h = CODE(30, 20, [[('  "mcp"', 'k'), (': {', 'w')], [('    "servers"', 'k'), (': {', 'w')], [('      "caribemart"', 'k'), (': {', 'w')], [('        "type"', 'k'), (': ', 'w'), ('"local"', 's'), (',', 'w')],
                         [('        "command"', 'k'), (': [', 'w'), ('"node"', 's'), (', ', 'w'), ('"server.js"', 's'), (']', 'w')], [('      }', 'w')], [('    }', 'w')], [('  }', 'w')]], size=24, padx=24, pady=22, title='opencode.json')
b = [cd]
X = 30 + w + 8
for i, n, col, t, ty in ((1, 1, OK, 'recomendada', 70), (2, 2, DOSC, 'nombre único', 160), (4, 3, VINO, 'comando', 250)):
    b.append(CALL(X, linectr(20, 24, i, 22), X + 60, ty - 6, n, col)); b.append(T(X + 92, ty, t, 26, True, col))
b.append(R(30, 395, 1120, 90, DT, DOSC, 2.5, 16)); b.append(IC('documento', 90, 440, 54, DOSC))
b.append(T(140, 432, 'Formato de la semana 12 también funciona', 26, True, INK)); b.append(T(140, 466, 'mcp con enabled', 22, False, GRIS))
slide(35, SVG(*b), titulo='Registro recomendado en opencode.json', sub='mcp punto servers con tipo local y comando node; en opencode 2.0.31 funcionan ambos formatos.')

# 36 · Verificar conexión  (terminal + semáforo)
cd, w, h = CODE(30, 20, [[('$ ', 'k'), ('opencode mcp list', 'w')], [('caribemart  ', 'w'), ('● connected', 's')]], size=28, padx=26, pady=26, title='terminal')
b = [cd]
b.append(T(30, 20 + h + 44, '/mcps: ver estado y errores', 26, True, INK))
b.append(R(640, 20, 520, 170, OKT, OK, 3, 18)); b.append(C(710, 105, 36, OK)); b.append(T(770, 98, 'CONECTADO', 32, True, OK)); b.append(T(770, 136, 'puedes preguntar', 26, False, INK))
b.append(R(640, 220, 520, 170, MALT, MAL, 3, 18)); b.append(C(710, 305, 36, MAL)); b.append(T(770, 298, 'DESCONECTADO', 32, True, MAL)); b.append(T(770, 336, 'revisa ruta y archivo', 26, False, INK))
b.append(IC('codigo', 110, 340, 100, VINO) if False else '')
b.append(A(w + 40, 90, 636, 105, OK, 4)); b.append(A(w + 40, 120, 636, 305, MAL, 4, dash='9 7'))
slide(36, SVG(*b))

# 37 · Flujo completo del pedido 1001  (carriles)
actors = [(130, 'usuario', 'ESTUDIANTE', INK), (440, 'ia', 'MODELO', VINO), (760, 'codigo', 'OPENCODE', DOSC), (1060, 'servidor', 'SERVIDOR MCP', OK)]
b = []
for x, ic, t, col in actors:
    b.append(R(x - 105, 10, 210, 76, '#fff', col, 3, 14)); b.append(IC(ic, x - 72, 48, 40, col)); b.append(T(x - 44, 55, t, 18, True, col))
    b.append('<line x1="%g" y1="86" x2="%g" y2="490" stroke="%s" stroke-width="2.5" stroke-dasharray="7 7"/>' % (x, x, col))
msg = [(150, 130, 440, '1 PREGUNTA', VINO, None), (220, 440, 760, '2 PROPUESTA', VINO, None), (290, 760, 1060, '3 EJECUCIÓN', DOSC, 'consultar_pedido { pedidoId: 1001 }'),
       (370, 1060, 440, '4 OBSERVACIÓN', OK, 'estado enviado'), (450, 440, 130, '5 RESPUESTA', OK, None)]
for y, x1, x2, t, col, sub in msg:
    dash = '10 7' if t[0] in '45' else None
    b.append(A(x1 + (4 if x2 > x1 else -4), y, x2 + (-4 if x2 > x1 else 4), y, col, 5, dash=dash))
    b.append(T((x1 + x2) / 2, y - 14, t, 24, True, col, 'middle'))
    if sub: b.append(R((x1 + x2) / 2 - tw(sub, 18, False, True) / 2 - 6, y + 12, tw(sub, 18, False, True) + 12, 28, '#fff', None, 0, 6)); b.append(T((x1 + x2) / 2, y + 32, sub, 18, False, INK, 'middle', mono=True))
slide(37, SVG(*b))

# 38 · Qué verán en opencode  (ventana de terminal + anotaciones)
cd, w, h = CODE(30, 20, [[('> ', 'k'), ('caribemart_consultar_pedido', 'w')], [('  argumentos: ', 'c'), ('{ "pedidoId": 1001 }', 'w')], [('  resultado: ', 'c'), ('estado enviado', 's')]], size=26, padx=26, pady=28, title='opencode')
b = [cd]
X = 30 + w + 8
b.append(CALL(X, linectr(20, 26, 0, 28), X + 60, 70, 1)); b.append(T(X + 92, 76, 'servidor_herramienta', 26, True, VINO, mono=True))
b.append(CALL(X, linectr(20, 26, 1, 28), X + 60, 170, 2, DOSC)); b.append(T(X + 92, 176, 'argumentos enviados', 26, True, DOSC))
b.append(CALL(X, linectr(20, 26, 2, 28), X + 60, 262, 3, OK)); b.append(T(X + 92, 268, 'resultado recibido', 26, True, OK))
b.append(R(30, 340, 1120, 120, DT, DOSC, 3, 18)); b.append(IC('documento', 110, 400, 70, DOSC))
b.append(T(170, 392, 'Primera evidencia', 34, True, INK)); b.append(T(170, 438, 'de la actividad', 34, True, DOSC))
slide(38, SVG(*b))

# 39 · Agregar listar y crear  (foto + dos herramientas)
b = [FOTO('bodega', 0, 20, 470, 460, 16), GRAD_SCRIM(0, 330, 470, 150, .85, 16), T(235, 450, 'Mismo patrón seguro', 28, True, '#fff', 'middle')]
b.append(C(560, 130, 56, VT, VINO, 2.5)); b.append(IC('registro', 560, 130, 72, VINO))
b.append(T(640, 120, 'LISTAR POR ESTADO', 30, True, VINO)); b.append(T(640, 156, 'lee pedidos.json', 24, False, INK))
b.append(chip(560, 235, 'solo lectura', size=22, fill=OKT, stroke=OK, h=48, padx=18, icon='ojo', isz=30))
b.append(C(560, 370, 56, DT, DOSC, 2.5)); b.append(IC('funcion', 560, 370, 72, DOSC))
b.append(T(640, 360, 'CREAR PEDIDO', 30, True, DOSC)); b.append(T(640, 396, 'escribe con control', 24, False, INK))
b.append(chip(560, 440, 'cliente, total y estado validados', size=22, fill=MALT, stroke=MAL, h=44, padx=18, icon='escudo', isz=28))
slide(39, SVG(*b), fotos=['bodega'])

# 40 · Inspector MCP  (comando + ventana + ciclo)
b = [R(30, 20, 1120, 70, '#1E1E1E', None, 0, 35), T(70, 64, '$ npx @modelcontextprotocol/inspector node server.js', 28, False, '#fff', mono=True)]
b.append(R(30, 130, 440, 350, '#fff', INK, 3, 14)); b.append(R(30, 130, 440, 44, '#E9E9E9', None, 0, 14)); b.append(R(30, 150, 440, 24, '#E9E9E9', None, 0, 0))
for i, c in enumerate(('#E5645A', '#E8C56A', '#6DBE7D')): b.append(C(56 + i * 22, 152, 6, c))
b.append(T(250, 158, 'navegador', 15, False, GRIS, 'middle'))
for i, t in enumerate(('consultar_pedido', 'listar_por_estado', 'crear_pedido')):
    b.append(chip(60, 200 + i * 86, t, size=24, fill=VT, stroke=VINO, h=62, padx=20, mono=True, icon='funcion', isz=34))
cyc = [(700, 260, 'ojo', 'LISTAR', 'ves tus tres herramientas', VINO, 'up'), (1050, 260, 'funcion', 'LLAMAR', 'pruebas argumentos malos', DOSC, 'up'), (880, 425, 'engranaje', 'CORREGIR', 'ajustas antes de opencode', OK, 'right')]
for x, y, ic, t, sub, col, pos in cyc:
    b.append(C(x, y, 52, '#fff', col, 3)); b.append(IC(ic, x, y, 66, col))
    if pos == 'up': b.append(T(x, y - 96, t, 28, True, col, 'middle')); b.append(T(x, y - 68, sub, 18, False, GRIS, 'middle'))
    else: b.append(T(x + 76, y - 4, t, 28, True, col)); b.append(T(x + 76, y + 24, sub, 18, False, GRIS))
b.append(A(756, 260, 992, 260, VINO, 5)); b.append(A(1030, 308, 920, 380, DOSC, 5)); b.append(A(846, 385, 722, 308, OK, 5))
slide(40, SVG(*b))

# 41 · Problemas típicos  (síntoma → arreglo)
rows = [(40, 'RUTA ERRADA', 'server.js no encontrado', 'revisa cwd y comando'), (190, 'PUNTO TXT', 'guardado como .txt', 'muestra las extensiones'), (340, 'FALTA INSTALL', 'SDK no encontrado', 'ejecuta npm install')]
b = []
for y, t1, t2, fix in rows:
    b.append(R(30, y, 480, 120, MALT, MAL, 3, 16)); b.append(CH(80, y + 60, 26, False)); b.append(T(125, y + 54, t1, 30, True, MAL)); b.append(T(125, y + 92, t2, 24, False, INK))
    b.append(A(516, y + 60, 650, y + 60, VINO, 6))
    b.append(R(660, y, 490, 120, OKT, OK, 3, 16)); b.append(CH(710, y + 60, 26, True)); b.append(T(755, y + 72, fix, 28, True, OK))
slide(41, SVG(*b))

# 42 · Síntesis de la parte 3  (lista de verificación)
items = [('ESQUELETO MÍNIMO', 'SDK y zod', 'package'), ('VALIDA ANTES DE ACTUAR', 'rechaza lo inválido', 'escudo'),
         ('REGISTRO RECOMENDADO', 'mcp servers local', 'documento'), ('CONECTADO Y VERIFICADO', 'mcp list primero', 'check')]
b = ['<line x1="90" y1="70" x2="90" y2="430" stroke="%s" stroke-width="6" stroke-linecap="round"/>' % DOR]
for i, (t, sub, ic) in enumerate(items):
    y = 70 + i * 120
    ic = {'package': 'contenedor'}.get(ic, ic)
    b.append(CH(90, y, 38, True)); b.append(IC(ic, 220, y, 70, VINO))
    b.append(T(290, y - 2, t, 34, True, VINO)); b.append(T(290, y + 34, sub, 24, False, GRIS))
slide(42, SVG(*b))
