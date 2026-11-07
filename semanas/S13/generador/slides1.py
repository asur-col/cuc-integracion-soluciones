from lib import *
from reg import slide

# 1 · El límite: solo texto  (flujo horizontal con enlace roto)
b = []
b.append(NODE(170, 170, 'documento', 'CHAT', 'pregunta escrita', INK, GT, r=72, isz=92, lsz=26, ssz=19))
b.append(NODE(590, 170, 'ia', 'MODELO', 'solo devuelve texto', VINO, VT, r=82, isz=108, lsz=28, ssz=19))
b.append(NODE(1010, 170, 'bd', 'PEDIDOS', None, '#8a8a8a', GT, r=72, isz=92, lsz=26, lab=GRIS))
b.append(A(248, 170, 502, 170, VINO, 5)); b.append(T(375, 150, 'texto', 20, True, VINO, 'middle'))
b.append(A(682, 170, 930, 170, '#9a9a9a', 5, dash='9 8'))
b.append(CH(806, 170, 22, False)); b.append(T(806, 224, 'sin conexión', 20, True, MAL, 'middle'))
b.append(CHIP(590, 380, 'El modelo no conoce el pedido 1001', 30, VT, VINO, anchor='middle', padx=28, h=70)[0])
slide(1, SVG(*b))

# 2 · Tres cosas que el modelo no puede hacer solo  (abanico)
b = []
b.append(NODE(190, 250, 'ia', 'MODELO', None, VINO, VT, r=96, isz=120, lsz=30))
rows = [(80, 'bd', 'NO CONSULTA', 'Pedidos en vivo', VINO, VT), (250, 'reloj', 'NO SABE LA HORA', 'Fecha y estado actual', INK, GT), (420, 'funcion', 'NO ACTÚA', 'Crear o cancelar pedido', DOSC, DT)]
for y, ic, t1, t2, col, tint in rows:
    b.append(A(292, 250 + (y - 250) * .22, 560, y, '#9a9a9a', 4, dash='9 8'))
    b.append(CH(430, 250 + (y - 250) * .6, 18, False))
    b.append(C(620, y, 56, tint, col, 2.5)); b.append(IC(ic, 620, y, 72, col))
    b.append(T(702, y - 2, t1, 30, True, col)); b.append(T(702, y + 32, t2, 24, False, GRIS))
slide(2, SVG(*b))

# 3 · Herramientas: funciones reales fuera del modelo  (foto + cadena vertical)
b = [FOTO('herramientas', 0, 20, 430, 460, 16), SCRIM(0, 400, 430, 80, .62, 0)]
b[1] = GRAD_SCRIM(0, 330, 430, 150, .8, 16)
b.append(T(215, 452, 'Funciones reales', 28, True, '#fff', 'middle'))
steps = [(110, 'ia', 'EL MODELO PROPONE', 'nombre y argumentos', VINO, VT), (250, 'servidor', 'LA APLICACIÓN EJECUTA', 'la función real', INK, GT), (390, 'bd', 'VUELVE EL DATO', 'verificable', DOSC, DT)]
for y, ic, t1, t2, col, tint in steps:
    b.append(C(560, y, 54, tint, col, 2.5)); b.append(IC(ic, 560, y, 70, col))
    b.append(T(640, y - 2, t1, 28, True, col)); b.append(T(640, y + 30, t2, 22, False, GRIS))
b.append(A(560, 168, 560, 192, VINO, 4)); b.append(A(560, 308, 560, 332, INK, 4))
slide(3, SVG(*b), fotos=['herramientas'])

# 4 · Function calling en una frase  (banner + flujo)
b = [R(30, 20, 1120, 150, VINO, None, 0, 18)]
b.append(T(590, 92, 'El modelo propone, la aplicación ejecuta', 42, True, '#fff', 'middle'))
b.append(T(590, 138, 'y le devuelve el resultado verificado', 24, False, '#F3D9DE', 'middle'))
b.append(NODE(190, 300, 'ia', 'MODELO', None, VINO, VT, r=62, isz=82, lsz=24))
b.append(NODE(590, 300, 'servidor', 'APLICACIÓN', None, INK, GT, r=62, isz=82, lsz=24))
b.append(NODE(990, 300, 'bd', 'DATO', None, DOSC, DT, r=62, isz=82, lsz=24))
b.append(A(258, 290, 520, 290, VINO, 5)); b.append(T(389, 268, 'propone', 20, True, VINO, 'middle'))
b.append(A(658, 290, 920, 290, DOSC, 5)); b.append(T(789, 268, 'ejecuta', 20, True, DOSC, 'middle'))
b.append(AP([(990, 232), (990, 215), (190, 215), (190, 226)], OK, 4, dash='9 7')); b.append(T(590, 206, 'resultado', 20, True, OK, 'middle'))
slide(4, SVG(*b))

# 5 · El bucle en 4 pasos  (ciclo)
b = []
nodes = [(130, 100, 'usuario', 'PREGUNTA', '¿Estado del pedido?', INK, GT), (720, 100, 'funcion', 'PROPUESTA', 'consultar_pedido', VINO, VT),
         (720, 400, 'servidor', 'EJECUCIÓN', 'la app ejecuta', INK, GT), (130, 400, 'bd', 'DATO', 'responde real', DOSC, DT)]
for i, (x, y, ic, t1, t2, col, tint) in enumerate(nodes, 1):
    b.append(C(x, y, 62, tint, col, 2.5)); b.append(IC(ic, x, y, 80, col)); b.append(BADGE(x - 46, y - 46, i, col, 20, 22))
    b.append(T(x + 82, y - 2, t1, 28, True, col)); b.append(T(x + 82, y + 30, t2, 22, False, GRIS))
b.append(A(440, 100, 640, 100, VINO, 5)); b.append(A(720, 168, 720, 330, VINO, 5))
b.append(A(640, 400, 440, 400, VINO, 5)); b.append(A(130, 332, 130, 170, VINO, 5))
b.append(IC('engranaje', 430, 250, 96, DOSC)); b.append(T(430, 330, 'se repite', 22, True, DOSC, 'middle'))
slide(5, SVG(*b))

# 6 · Anatomía de una llamada  (código grande con anotaciones)
b = [chip(40, 14, 'PROPUESTA DEL MODELO', size=22, fill=VT, stroke=VINO, icon='ia')]
cd, w, h = CODE(40, 90, [
    [('{', 'w')],
    [('  "nombre"', 'k'), (': ', 'w'), ('"consultar_pedido"', 's'), (',', 'w')],
    [('  "argumentos"', 'k'), (': { ', 'w'), ('"pedidoId"', 'k'), (': ', 'w'), ('1001', 'n'), (' }', 'w')],
    [('}', 'w')]], size=30, padx=26, pady=24)
b.append(cd)
b.append(CALL(720, 135, 790, 135, 1)); b.append(T(822, 128, 'NOMBRE', 28, True, VINO)); b.append(T(822, 158, 'exacto, sin inventar', 20, False, GRIS))
b.append(CALL(720, 190, 790, 235, 2, DOSC)); b.append(T(822, 235, 'ARGUMENTOS', 28, True, DOSC)); b.append(T(822, 265, 'valores según el esquema', 20, False, GRIS))
b.append(A(390, 90 + h + 10, 390, 390, INK, 4))
b.append(CHIP(390, 400, 'La aplicación valida y ejecuta', 26, GT, INK, anchor='middle', padx=24, h=64, icon='servidor')[0])
slide(6, SVG(*b))

# 7 · Esquema: ficha de la herramienta  (capas)
b = []
b.append(R(40, 20, 690, 460, '#fff', INK, 3, 18))
b.append(T(70, 62, 'consultar_pedido', 28, True, VINO, mono=True))
layers = [(90, 'documento', 'DESCRIPCIÓN', 'qué hace y cuándo usarla', VINO, VT), (210, 'engranaje', 'PARÁMETROS', 'pedidoId: entero positivo', DOSC, DT), (330, 'escudo', 'VALIDACIÓN', 'rechaza lo inválido', OK, OKT)]
for y, ic, t1, t2, col, tint in layers:
    b.append(R(66, y, 640, 100, tint, None, 0, 12)); b.append(R(66, y, 10, 100, col, None, 0, 4))
    b.append(IC(ic, 140, y + 50, 64, col)); b.append(T(196, y + 46, t1, 28, True, col)); b.append(T(196, y + 78, t2, 22, False, INK))
b.append(A(730, 250, 880, 250, VINO, 5)); b.append(T(805, 226, 'la lee', 22, True, VINO, 'middle'))
b.append(NODE(990, 220, 'ia', 'MODELO', 'elige con la descripción', VINO, VT, r=80, isz=104, lsz=28, ssz=20))
slide(7, SVG(*b))

# 8 · Quién ejecuta: la aplicación, no el modelo  (frontera)
b = [R(20, 30, 540, 440, VT, None, 0, 18), R(620, 30, 540, 440, GT, None, 0, 18)]
b.append(NODE(290, 200, 'ia', 'EL MODELO DECIDE', 'propone herramienta', VINO, '#fff', r=84, isz=108, lsz=28, ssz=22))
b.append(NODE(890, 130, 'servidor', 'LA APLICACIÓN ACTÚA', 'valida y ejecuta', INK, '#fff', r=62, isz=80, lsz=28, ssz=22))
b.append(IC('bd', 890, 400, 76, DOSC)); b.append(A(890, 320, 890, 356, INK, 4))
b.append('<line x1="590" y1="30" x2="590" y2="470" stroke="%s" stroke-width="5" stroke-dasharray="14 10"/>' % VINO)
b.append(A(390, 150, 820, 120, VINO, 5)); b.append(T(520, 112, 'ordena', 22, True, VINO, 'middle'))
b.append(C(590, 290, 48, '#fff', VINO, 4)); b.append(IC('candado', 590, 290, 58, VINO))
b.append(CHIP(590, 360, 'Frontera de seguridad', 20, VINO, None, color='#fff', anchor='middle', padx=16, h=44)[0])
slide(8, SVG(*b))

# 9 · El resultado vuelve como observación  (flujo con código)
b = []
b.append(NODE(110, 150, 'servidor', 'HERRAMIENTA', None, INK, GT, r=62, isz=80, lsz=22))
cd, w, h = CODE(250, 80, [[('estado', 'k'), (': ', 'w'), ('"enviado"', 's')], [('cliente', 'k'), (': ', 'w'), ('"Luis"', 's')]], size=24, padx=22, pady=20, title='OBSERVACIÓN')
b.append(cd)
b.append(NODE(740, 150, 'ia', 'MODELO', 'lee el dato real', VINO, VT, r=62, isz=80, lsz=22, ssz=19))
b.append(BUBBLE(900, 70, 260, 130, VT, VINO, 'left')); b.append(T(1030, 118, ['Su pedido', 'fue enviado'], 26, True, VINO, 'middle'))
b.append(A(176, 140, 246, 140, INK, 4)); b.append(A(250 + w + 4, 140, 668, 140, DOSC, 4)); b.append(A(808, 140, 896, 134, VINO, 4))
b.append(T(1030, 250, 'RESPUESTA FINAL', 20, True, VINO, 'middle'))
b.append(R(60, 330, 1060, 120, DT, DOSC, 3, 18))
b.append(IC('llave', 150, 390, 64, DOSC)); b.append(T(210, 382, 'REGLA DE ORO', 20, True, DOSC)); b.append(T(210, 424, 'Sin observación no hay respuesta', 34, True, INK))
slide(9, SVG(*b))

# 10 · Antes de MCP: integración a medida  (foto + conexiones a medida)
b = [FOTO('enredo', 0, 20, 470, 460, 16), GRAD_SCRIM(0, 330, 470, 150, .85, 16), T(235, 440, 'Un desarrollo por conexión', 26, True, '#fff', 'middle')]
rows = [(90, 'APP A', 'formato propio', VINO), (250, 'APP B', 'otro formato', DOSC), (410, 'APP C', 'otro más', INK)]
for y, a, f, col in rows:
    b.append(IC('laptop', 560, y, 70, col)); b.append(T(560, y + 62, a, 22, True, col, 'middle'))
    b.append(A(620, y, 930, y, col, 4, dash='12 7' if a != 'APP A' else None)); b.append(T(775, y - 14, f, 22, True, col, 'middle'))
    b.append(IC('funcion', 1010, y, 76, col));
b.append(T(1100, 256, 'cada', 20, False, GRIS, 'middle')) if False else None
slide(10, SVG(*b), fotos=['enredo'])

# 11 · Mini-reto: pausa  (reto)
b = [R(20, 20, 1140, 460, DT, DOSC, 4, 22, dash='14 9')]
b.append(PAUSE(160, 170, 80)); b.append(T(160, 300, ['PAUSA', 'Y RESPONDE'], 28, True, DOSC, 'middle'))
b.append(T(300, 130, '¿Cuál es el estado del pedido 1001?', 44, True, VINO))
b.append(T(300, 195, '¿Qué debe hacer el modelo?', 34, False, INK))
b.append(R(300, 280, 800, 150, '#fff', DOSC, 2.5, 16))
b.append(IC('llave', 370, 355, 70, DOSC)); b.append(T(440, 335, 'PISTA', 22, True, DOSC)); b.append(T(440, 385, 'Llamar consultar_pedido con el número 1001', 28, True, INK))
slide(11, SVG(*b))

# 12 · CaribeMart: tres herramientas mínimas  (foto banda + llaves)
b = [FOTO('tienda', 0, 0, 1180, 210, 16, 'xMidYMid'), GRAD_SCRIM(0, 100, 1180, 110, .75, 16), T(30, 192, 'CaribeMart', 30, True, '#fff')]
xs = [('consultar_pedido', 'bd', VINO, VT), ('listar_por_estado', 'registro', VINO, VT), ('crear_pedido', 'funcion', DOSC, DT)]
x = 40; spans = []
for nm, ic, col, tint in xs:
    s, w, h = CHIP(x, 250, nm, size=26, fill=tint, stroke=col, mono=True, h=78, padx=20, icon=ic, isz=48)
    b.append(s); spans.append((x, x + w)); x += w + 34
(a1, b1), (a2, b2), (a3, b3) = spans
b.append(P('M%g,350 V372 H%g V350' % (a1, b2), stroke=OK, sw=4)); b.append(T((a1 + b2) / 2, 412, 'LEEN: solo consultan', 30, True, OK, 'middle'))
b.append(P('M%g,350 V372 H%g V350' % (a3, 1140), stroke=MAL, sw=4)); b.append(T((a3 + 1140) / 2, 412, 'ESCRIBE: exige confirmación', 28, True, MAL, 'middle'))
b.append(T((a3 + 1140) / 2, 452, 'validación estricta con zod', 22, False, GRIS, 'middle'))
slide(12, SVG(*b), fotos=['tienda'])

# 13 · El error clásico: alucinar el estado  (antes / después)
b = [R(10, 20, 570, 460, MALT, MAL, 3, 20), R(600, 20, 570, 460, OKT, OK, 3, 20)]
b.append(T(295, 72, 'SIN HERRAMIENTA', 30, True, MAL, 'middle')); b.append(T(885, 72, 'CON HERRAMIENTA', 30, True, OK, 'middle'))
b.append(IC('ia', 110, 200, 90, MAL)); b.append(BUBBLE(190, 130, 360, 120, '#fff', MAL, 'left'))
b.append(T(370, 180, ['Su pedido 1001', 'fue entregado'], 28, True, MAL, 'middle'))
b.append(CH(110, 330, 30, False)); b.append(T(160, 342, 'suena seguro, es inventado', 24, True, INK))
b.append(IC('ia', 690, 200, 90, OK)); b.append(A(740, 200, 800, 200, OK, 4)); b.append(IC('bd', 850, 200, 74, OK))
b.append(BUBBLE(690, 290, 400, 90, '#fff', OK, 'left')); b.append(T(890, 345, 'Consultó 1001: enviado', 28, True, OK, 'middle'))
b.append(CH(690, 430, 26, True)); b.append(T(735, 440, 'dato verificado de la base', 24, True, INK))
slide(13, SVG(*b))

# 14 · Síntesis de la parte 1  (ruta)
b = ['<line x1="70" y1="250" x2="1110" y2="250" stroke="%s" stroke-width="10" stroke-linecap="round" stroke-dasharray="2 18"/>' % DOR]
pts = [(160, 'documento', 'El texto no basta', INK, GT, 'up'), (440, 'funcion', 'Propone y ejecuta', VINO, VT, 'down'),
       (720, 'codigo', 'Esquema JSON', DOSC, DT, 'up'), (1000, 'ojo', 'Observación', OK, OKT, 'down')]
for i, (x, ic, t, col, tint, d) in enumerate(pts, 1):
    b.append(C(x, 250, 58, tint, col, 3)); b.append(IC(ic, x, 250, 76, col)); b.append(BADGE(x + 44, 250 - 44, i, col, 20, 22))
    yy = 130 if d == 'up' else 392
    b.append(T(x, yy, t, 30, True, col, 'middle'))
slide(14, SVG(*b))
