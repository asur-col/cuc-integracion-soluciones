from lib import *
from reg import slide

# 15 · MCP: USB-C para la IA  (foto + conector)
b = [FOTO('usbc', 0, 20, 580, 326, 16), T(290, 400, 'USB-C: un solo conector', 32, True, INK, 'middle'),
     T(290, 440, 'para todos los dispositivos', 26, False, GRIS, 'middle')]
b.append(NODE(880, 70, 'ia', 'APLICACIÓN IA', None, VINO, VT, r=44, isz=58, lsz=22))
b.append(A(880, 140, 880, 192, VINO, 4))
b.append(R(700, 200, 360, 120, VINO, None, 0, 18)); b.append(PLUG(780, 262, 70, '#fff', VINO))
b.append(T(830, 252, 'PROTOCOLO MCP', 26, True, '#fff')); b.append(T(830, 286, 'mismo formato', 22, False, '#F3D9DE'))
b.append(A(880, 330, 880, 372, VINO, 4)); b.append(A(880, 330, 800, 372, VINO, 4)) if False else None
b.append(IC('servidor', 790, 420, 66, INK)); b.append(T(790, 478, 'sistemas', 22, True, INK, 'middle'))
b.append(IC('bd', 970, 420, 66, DOSC)); b.append(T(970, 478, 'datos', 22, True, DOSC, 'middle'))
b.append(A(850, 330, 800, 378, VINO, 4)); b.append(A(910, 330, 960, 378, VINO, 4))
slide(15, SVG(*b), fotos=['usbc'])

# 16 · Host, cliente y servidor  (zonas)
b = [R(20, 30, 700, 440, VT, VINO, 3, 20, dash='10 7'), T(50, 74, 'MCP HOST · LA APLICACIÓN IA', 26, True, VINO)]
b.append(NODE(140, 250, 'ia', 'HOST', 'la aplicación', VINO, '#fff', r=72, isz=92, lsz=26, ssz=20))
b.append(R(330, 160, 340, 230, '#fff', VINO, 3, 16)); b.append(PLUG(420, 270, 70, VINO, '#fff'))
b.append(T(480, 242, 'MCP CLIENT', 26, True, VINO)); b.append(T(480, 276, 'mantiene', 22, False, INK)); b.append(T(480, 304, 'una conexión', 22, False, INK))
b.append(A(216, 275, 328, 275, VINO, 5))
b.append(R(850, 30, 310, 440, GT, INK, 3, 20))
b.append(NODE(1005, 200, 'servidor', 'MCP SERVER', 'provee contexto', INK, '#fff', r=72, isz=92, lsz=26, ssz=20))
b.append(T(1005, 380, ['herramientas,', 'recursos y prompts'], 22, False, INK, 'middle'))
b.append(A(672, 275, 848, 275, DOSC, 5, both=True)); b.append(T(760, 246, 'pregunta', 20, True, DOSC, 'middle')); b.append(T(760, 312, 'contexto', 20, True, DOSC, 'middle'))
slide(16, SVG(*b))

# 17 · Tres primitivas  (árbol con quién controla)
b = [NODE(150, 250, 'servidor', 'SERVIDOR MCP', 'provee tres tipos', INK, GT, r=84, isz=108, lsz=28, ssz=20)]
prims = [(70, 'funcion', 'HERRAMIENTAS', 'ejecutables', 'las controla el modelo', VINO, VT), (250, 'documento', 'RECURSOS', 'solo lectura', 'los controla la aplicación', DOSC, DT), (430, 'codigo', 'PROMPTS', 'plantillas guiadas', 'los controla el usuario', OK, OKT)]
for y, ic, t1, t2, t3, col, tint in prims:
    b.append(AP([(250, 250), (330, 250), (360, y), (420, y)], col, 4) if y != 250 else A(250, 250, 420, 250, col, 4))
    wch = max(tw(t1, 30, True) + 120, 330)
    b.append(R(430, y - 56, wch, 112, tint, col, 2.5, 16)); b.append(IC(ic, 476, y, 56, col))
    b.append(T(520, y - 4, t1, 30, True, col)); b.append(T(520, y + 28, t2, 22, False, INK))
    b.append(T(430 + wch + 26, y + 8, t3, 24, True, col))
slide(17, SVG(*b))

# 18 · Herramientas MCP: actúa el modelo  (flujo con compuerta humana)
b = []
b.append(NODE(130, 190, 'ia', 'EL MODELO', 'descubre y elige', VINO, VT, r=70, isz=92, lsz=26, ssz=20))
b.append(R(540, 70, 100, 350, DT, DOSC, 3, 14)); b.append(C(590, 160, 46, '#fff', DOSC, 3)); b.append(IC('usuario', 590, 160, 62, DOSC))
b.append(T(590, 258, 'APROBACIÓN', 22, True, DOSC, 'middle')) if False else None
b.append(T(590, 470, 'APROBACIÓN', 26, True, DOSC, 'middle')); b.append(T(590, 440, 'control humano', 20, False, GRIS, 'middle'))
b.append(IC('candado', 590, 300, 60, DOSC))
b.append(A(210, 190, 536, 190, VINO, 5)); b.append(T(375, 168, 'invoca', 24, True, VINO, 'middle'))
b.append(NODE(1050, 190, 'engranaje', 'LA HERRAMIENTA', 'ejecuta una acción', INK, GT, r=70, isz=92, lsz=26, ssz=20))
b.append(A(644, 190, 976, 190, OK, 5)); b.append(T(810, 168, 'si aprueba', 24, True, OK, 'middle'))
slide(18, SVG(*b))

# 19 · Recursos MCP  (lista de URI → aplicación → modelo)
b = []
uris = [(70, 'pedidos://esquema', 'application/json'), (200, 'archivo://docs/politica.txt', 'text/plain')]
for y, u, m in uris:
    s, w, h = CHIP(30, y, u, size=26, fill='#fff', stroke=DOSC, h=84, padx=18, mono=True, icon='documento', isz=44)
    b.append(s); b.append(T(30 + 22, y + h + 28, m, 20, False, GRIS))
b.append(A(600, 170, 690, 190, DOSC, 5) if False else '')
b.append(AP([(640, 112), (700, 112), (730, 190), (770, 190)], DOSC, 5)); b.append(AP([(640, 242), (700, 242), (730, 200), (770, 200)], DOSC, 5))
b.append(NODE(860, 190, 'laptop', 'LA APLICACIÓN DECIDE', None, INK, GT, r=70, isz=92, lsz=26))
b.append(T(860, 330, 'qué contexto pasa al modelo', 22, False, GRIS, 'middle'))
b.append(A(940, 190, 1050, 190, VINO, 5)); b.append(IC('ia', 1105, 190, 76, VINO))
b.append(R(60, 380, 1060, 90, OKT, OK, 3, 16)); b.append(IC('ojo', 130, 425, 56, OK)); b.append(T(190, 436, 'Leer no cambia la base', 36, True, OK))
slide(19, SVG(*b))

# 20 · Prompts MCP  (comando del usuario → plantilla → herramientas)
b = [NODE(110, 120, 'usuario', 'USUARIO', 'elige la plantilla', DOSC, DT, r=58, isz=76, lsz=22, ssz=19)]
b.append(R(260, 70, 880, 90, '#1E1E1E', None, 0, 45)); b.append(T(310, 128, '/pedidos-resumen estado=pendiente', 34, False, '#fff', mono=True))
b.append(T(1110, 120, '▌', 34, False, DOR, 'end') if False else '')
b.append(A(190, 118, 256, 114, DOSC, 4))
b.append(T(700, 192, 'comando del usuario', 22, False, GRIS, 'middle'))
b.append(A(700, 205, 700, 250, DOSC, 5))
b.append(R(260, 260, 880, 110, '#fff', DOSC, 3, 16)); b.append(IC('documento', 330, 315, 66, DOSC))
b.append(T(390, 305, 'PLANTILLA', 28, True, DOSC)); b.append(T(390, 345, 'instrucción lista para usar', 24, False, INK))
for i, x in enumerate((760, 850, 940)):
    b.append(C(x + 30, 315, 34, VT, VINO, 2.5)); b.append(IC('funcion', x + 30, 315, 44, VINO))
b.append(P('M820,315 H846 M910,315 H936', stroke=VINO, sw=3))
b.append(T(700, 440, 'guía varias herramientas juntas', 28, True, VINO, 'middle'))
slide(20, SVG(*b))

# 21 · Ciclo MCP en tres intercambios  (diagrama de secuencia)
b = [R(100, 20, 300, 100, VT, VINO, 3, 16), IC('laptop', 160, 70, 60, VINO), T(200, 78, 'CLIENTE', 28, True, VINO),
     R(780, 20, 300, 100, GT, INK, 3, 16), IC('servidor', 840, 70, 60, INK), T(880, 78, 'SERVIDOR', 28, True, INK)]
b.append('<line x1="250" y1="120" x2="250" y2="480" stroke="%s" stroke-width="3" stroke-dasharray="8 8"/>' % VINO)
b.append('<line x1="930" y1="120" x2="930" y2="480" stroke="%s" stroke-width="3" stroke-dasharray="8 8"/>' % INK)
msgs = [(190, '1 · DESCUBRIR', 'qué sabe hacer'), (275, '2 · LISTAR', 'tools/list'), (360, '3 · LLAMAR', 'tools/call')]
for y, t1, t2 in msgs:
    b.append(A(252, y, 926, y, VINO, 5)); b.append(T(590, y - 30, t1, 26, True, VINO, 'middle')); b.append(T(590, y - 8, t2, 20, False, GRIS, 'middle', mono=t2.startswith('tools')))
b.append(A(926, 440, 252, 440, OK, 5, dash='10 7')); b.append(T(590, 424, 'RESULTADO', 26, True, OK, 'middle')); b.append(T(590, 470, 'dato verificable', 20, False, GRIS, 'middle'))
slide(21, SVG(*b))

# 22 · stdio: tubería local  (zona + tubería)
b = [R(20, 20, 1140, 330, GT, '#9a9a9a', 2.5, 20, dash='10 7'), T(50, 62, 'TU MÁQUINA', 22, True, GRIS)]
b.append(NODE(190, 190, 'codigo', 'OPENCODE', 'cliente MCP', VINO, '#fff', r=76, isz=98, lsz=28, ssz=22))
b.append(NODE(990, 190, 'servidor', 'SERVIDOR NODE', 'server.js local', INK, '#fff', r=76, isz=98, lsz=28, ssz=22))
b.append(R(290, 150, 600, 70, '#fff', DOSC, 4, 35)); b.append(R(290, 150, 600, 70, DT, None, 0, 35, op=.9))
b.append(A(320, 172, 860, 172, VINO, 4)); b.append(A(860, 200, 320, 200, DOSC, 4))
b.append(T(590, 250, 'STDIN y STDOUT', 28, True, DOSC, 'middle')); b.append(T(590, 286, 'tubería local', 22, False, GRIS, 'middle'))
b.append(IC('internet', 450, 425, 70, '#9a9a9a')); b.append(C(450, 425, 46, 'none', MAL, 5)); b.append('<line x1="418" y1="457" x2="482" y2="393" stroke="%s" stroke-width="5"/>' % MAL)
b.append(T(530, 435, 'Sin servidor web ni puerto abierto', 30, True, INK))
slide(22, SVG(*b))

# 23 · HTTP: servidores remotos  (clientes → internet → foto servidor)
b = []
for y in (80, 220, 360):
    b.append(IC('laptop', 100, y + 30, 70, INK))
    b.append(A(150, y + 30, 330, 250, INK, 3))
b.append(T(110, 452, ['CLIENTES VARIOS', 'muchas conexiones'], 22, True, INK, 'middle'))
b.append(C(420, 250, 90, DT, DOSC, 3)); b.append(IC('internet', 420, 235, 100, DOSC))
b.append(R(350, 300, 140, 40, DOSC, None, 0, 20)); b.append(IC('candado', 372, 320, 28, '#fff')); b.append(T(430, 327, 'HTTP', 20, True, '#fff', 'middle'))
b.append(T(420, 380, 'INTERNET', 24, True, DOSC, 'middle')); b.append(T(420, 408, 'HTTP cifrado', 20, False, GRIS, 'middle'))
b.append(A(520, 250, 650, 250, DOSC, 5))
b.append(FOTO('datacenter', 660, 20, 510, 340, 16)); b.append(GRAD_SCRIM(660, 250, 510, 110, .8, 16))
b.append(T(690, 340, 'SERVIDOR REMOTO', 30, True, '#fff'))
b.append(IC('llave', 690, 420, 56, DOSC)); b.append(T(740, 432, 'OAuth y claves', 30, True, DOSC))
slide(23, SVG(*b), fotos=['datacenter'])

# 24 · MCP frente a API REST  (comparación)
b = [R(10, 20, 560, 460, GT, '#9a9a9a', 2.5, 20), R(610, 20, 560, 460, VT, VINO, 3, 20)]
b.append(T(290, 74, 'API REST CLÁSICA', 30, True, INK, 'middle')); b.append(T(890, 74, 'MCP PARA IA', 30, True, VINO, 'middle'))
for i, t in enumerate(('GET /pedidos', 'POST /pedidos')):
    b.append(chip(70, 120 + i * 90, t, size=28, fill='#fff', stroke=INK, mono=True, h=68, padx=24, icon='api', isz=40))
for i, t in enumerate(('tools/list', 'tools/call')):
    b.append(chip(670, 120 + i * 90, t, size=28, fill='#fff', stroke=VINO, mono=True, h=68, padx=24, icon='funcion', isz=40))
b.append(IC('laptop', 150, 380, 70, INK)); b.append(T(210, 392, 'La aplicación decide', 28, True, INK))
b.append(IC('ia', 700, 380, 70, VINO)); b.append(T(760, 392, 'El modelo elige', 28, True, VINO))
b.append(C(590, 250, 28, '#fff', DOSC, 3)); b.append(T(590, 260, 'vs', 24, True, DOSC, 'middle'))
slide(24, SVG(*b))

# 25 · Mini-reto: clasificar  (emparejar)
b = [PAUSE(70, 70, 44), T(140, 62, 'PAUSA Y CLASIFICA', 30, True, DOSC), T(140, 96, '¿Qué primitiva usarías en cada caso?', 24, False, INK)]
tasks = [('A', 'leer esquema', 190), ('B', 'crear pedido', 300), ('C', 'resumen guiado', 410)]
for l, t, y in tasks:
    b.append(C(60, y, 28, DOSC)); b.append(T(60, y + 10, l, 28, True, '#fff', 'middle'))
    b.append(chip(100, y - 32, t, size=26, fill=DT, stroke=DOSC, h=64, padx=20))
bk = [('funcion', 'HERRAMIENTA', VINO, VT, 190), ('documento', 'RECURSO', DOSC, DT, 300), ('codigo', 'PROMPT', OK, OKT, 410)]
for ic, t, col, tint, y in bk:
    b.append(R(780, y - 40, 390, 80, tint, col, 3, 14)); b.append(IC(ic, 830, y, 52, col)); b.append(T(880, y + 10, t, 28, True, col))
for _, _, y in tasks:
    for _, _, _, _, y2 in bk:
        b.append('<line x1="400" y1="%g" x2="770" y2="%g" stroke="#cfcfcf" stroke-width="2.5"/>' % (y, y2))
b.append(C(585, 300, 40, '#fff', DOSC, 4)); b.append(T(585, 316, '?', 44, True, DOSC, 'middle'))
slide(25, SVG(*b))

# 26 · Context7 y el ecosistema  (foto + bus)
b = [FOTO('centralita', 0, 20, 520, 460, 16, 'xMidYMid'), GRAD_SCRIM(0, 330, 520, 150, .85, 16), T(260, 440, 'Escribir una vez, usar en muchos', 26, True, '#fff', 'middle')]
b.append('<line x1="640" y1="70" x2="640" y2="430" stroke="%s" stroke-width="6" stroke-linecap="round"/>' % DOSC)
items = [(70, 'documento', 'CONTEXT7', 'documentación viva', VINO, VT), (250, 'carpeta', 'ARCHIVOS', 'acceso a archivos', INK, GT), (430, 'alerta', 'SENTRY', 'errores y monitoreo · remoto', OK, OKT)]
for y, ic, t1, t2, col, tint in items:
    ic = {'carpeta': 'documento'}.get(ic, ic)
    b.append(A(640, y, 700, y, DOSC, 5)); b.append(C(760, y, 52, tint, col, 2.5)); b.append(IC(ic, 760, y, 66, col))
    b.append(T(840, y - 2, t1, 30, True, col)); b.append(T(840, y + 30, t2, 22, False, GRIS))
b.append(PLUG(640, 38, 52, DOSC, '#fff')) if False else None
slide(26, SVG(*b), fotos=['centralita'])

# 27 · JSON RPC: el sobre del mensaje  (dos paneles de código)
b = [chip(40, 14, 'PETICIÓN', size=24, fill=VT, stroke=VINO, h=48, padx=22), chip(760, 14, 'RESPUESTA', size=24, fill=OKT, stroke=OK, h=48, padx=22)]
c1, w1, h1 = CODE(40, 90, [[('{', 'w')], [('  "jsonrpc"', 'k'), (': ', 'w'), ('"2.0"', 's'), (',', 'w')], [('  "method"', 'k'), (': ', 'w'), ('"tools/call"', 's'), (',', 'w')],
                           [('  "params"', 'k'), (': { ... },', 'w')], [('  "id"', 'k'), (': ', 'w'), ('7', 'n')], [('}', 'w')]], size=24, padx=24, pady=22)
c2, w2, h2 = CODE(760, 90, [[('{', 'w')], [('  "jsonrpc"', 'k'), (': ', 'w'), ('"2.0"', 's'), (',', 'w')], [('  "result"', 'k'), (': { ... },', 'w')],
                           [('  "id"', 'k'), (': ', 'w'), ('7', 'n')], [('}', 'w')]], size=24, padx=24, pady=22)
b += [c1, c2]
b.append(A(40 + w1 + 6, 90 + h1 - 62, 754, 90 + h2 - 62, DOSC, 5)); b.append(T((40 + w1 + 760) / 2, 90 + h1 - 84, 'mismo id', 26, True, DOSC, 'middle'))
b.append(T(590, 420, 'Un sobre uniforme para cada mensaje', 30, True, VINO, 'middle'))
slide(27, SVG(*b))

# 28 · Síntesis de la parte 2  (escalera)
b = []
steps = [('servidor', 'Host, cliente|y servidor', VINO), ('funcion', 'Tres|primitivas', DOSC), ('api', 'JSON RPC|siempre', INK), ('internet', 'stdio local|o HTTP', OK)]
for i, (ic, t, col) in enumerate(steps):
    x = 30 + i * 288; h = 150 + i * 90; y = 490 - h
    b.append(R(x, y, 268, h, col, None, 0, 14))
    b.append(C(x + 134, y + 20, 48, '#fff', col, 4)); b.append(IC(ic, x + 134, y + 20, 62, col))
    b.append(T(x + 134, y + 104, t.split('|'), 26, True, '#fff', 'middle'))
    b.append(BADGE(x + 30, y + 50, i + 1, '#fff', 0, 0) if False else '')
slide(28, SVG(*b))
