from lib import *
from reg import slide

# 1 · Mapa de la sesión (foto a sangre + ruta de 4 paradas)
b = [
    FOTO('tienda', 0, 0, 1180, 500, 18, 'xMidYMid'),
    SCRIM(0, 0, 1180, 500, .34, 18),
    GRAD_SCRIM(0, 140, 1180, 360, .88, 18),
    T(40, 86, 'De consultas sueltas a agentes seguros', 42, True, '#fff'),
    T(40, 132, 'Ruta de la Semana 15 en cuatro paradas', 24, False, '#F3D9DE'),
]
stops = [
    ('1', 'AGENTES', 'bucle y pasos', VINO),
    ('2', 'CONTROL', 'permission ask', DOSC),
    ('3', 'ATAQUE', 'prompt injection', MAL),
    ('4', 'DEFENSA', 'proyecto Corte 3', OK),
]
x = 40
w_card = 248
gap = 36
for i, (num, t1, t2, col) in enumerate(stops):
    b.append(R(x, 315, w_card, 140, '#fff', col, 4, 16))
    b.append(BADGE(x + 38, 362, num, col, 20, 20))
    b.append(T(x + 74, 368, t1, 24, True, col))
    b.append(T(x + 28, 418, t2, 20, False, INK))
    if i < 3:
        b.append(A(x + w_card + 4, 385, x + w_card + gap - 4, 385, '#fff', 4))
    x += w_card + gap
slide(
    1,
    'Mapa',
    'Ruta de hoy: agentes con control humano y defensa',
    'Cuatro pasos para llevar el asistente de CaribeMart al Proyecto Corte 3.',
    'Basado en: caso del curso CaribeMart · Dibujo propio',
    SVG(*b),
    """Bienvenidos a la semana quince. Hoy cerramos el diseño técnico del asistente operativo de CaribeMart, conectando lo construido en la Unidad tres. A la izquierda ven el caso del curso, CaribeMart, una cadena ficticia del Caribe colombiano con sesenta almacenes, centro de datos principal en Barranquilla y respaldo en Bogotá. Sigan las cuatro tarjetas debajo de la fotografía. En la primera parada veremos qué convierte una llamada suelta a una herramienta en un agente capaz de encadenar varios pasos [cite:1]. En la segunda parada configuraremos la verificación humana mediante permisos de pregunta antes de modificar pedidos [cite:5]. En la tercera parada analizaremos el riesgo de inyección de instrucciones escondido en datos externos [cite:2]. Y en la cuarta parada construiremos la defensa en profundidad, revisaremos el marco legal colombiano [cite:11,12] y repasaremos las reglas del proyecto del tercer corte.""",
    fotos=['tienda'],
)

# 2 · De llamada única a tarea encadenada (antes / después)
b = [
    R(14, 20, 560, 460, GT, '#9a9a9a', 3, 18),
    R(606, 20, 560, 460, VT, VINO, 3, 18),
    T(294, 68, 'SEMANA 13 · LLAMADA ÚNICA', 24, True, INK, 'middle'),
    T(886, 68, 'SEMANA 15 · AGENTE ENCADENADO', 24, True, VINO, 'middle'),
    NODE(130, 175, 'usuario', 'META', '¿Pedido 1001?', INK, '#fff', r=50, isz=64, lsz=20, ssz=18),
    NODE(450, 175, 'funcion', '1 LLAMADA', 'consultar_pedido', INK, '#fff', r=50, isz=64, lsz=20, ssz=18),
    A(186, 175, 394, 175, INK, 4),
    R(50, 345, 488, 100, '#fff', '#9a9a9a', 2, 14),
    T(294, 388, 'Una pregunta, una respuesta', 22, True, INK, 'middle'),
    T(294, 422, 'y el flujo termina de inmediato', 20, False, GRIS, 'middle'),
    NODE(710, 165, 'funcion', '1. ATRASOS', 'pedidos_atrasados', VINO, '#fff', r=46, isz=58, lsz=18, ssz=16),
    NODE(900, 165, 'documento', '2. REGLAS', 'AGENTS.md', DOSC, '#fff', r=46, isz=58, lsz=18, ssz=16),
    NODE(1070, 165, 'candado', '3. PROPONER', 'cancelar_pedido', OK, '#fff', r=46, isz=58, lsz=18, ssz=16),
    A(760, 165, 848, 165, VINO, 4),
    A(950, 165, 1018, 165, DOSC, 4),
    R(640, 345, 492, 100, '#fff', VINO, 2, 14),
    T(886, 388, 'Encadena pasos, pide aprobación', 22, True, VINO, 'middle'),
    T(886, 422, 'y redacta el mensaje al cliente', 20, False, INK, 'middle'),
]
slide(
    2,
    'Contexto',
    'De llamadas sueltas a tareas encadenadas',
    'El modelo deja de responder una consulta aislada para resolver un objetivo operativo.',
    'Basado en: proyecto CaribeMart Corte 3 · Dibujo propio',
    SVG(*b),
    """Comparen detenidamente los dos paneles que tienen en pantalla. A la izquierda recordamos el alcance que logramos construir en la semana trece. Un operador preguntaba por el pedido mil uno, el modelo llamaba una sola vez a consultar pedido y devolvía el estado en texto plano. Ahí terminaba por completo su trabajo sin tomar más iniciativas. Ahora miren el panel derecho en tono vino. En la semana quince damos el salto de una llamada suelta a un agente que encadena varios pasos hacia una meta operativa completa. Primero consulta los pedidos atrasados en la base de datos. Luego cruza esos resultados contra las políticas de negocio escritas en AGENTS punto md. Después propone cuáles cancelar mediante cancelar pedido, pero se detiene ante el candado humano. Finalmente redacta el aviso cordial personalizado para cada comprador afectado en la región Caribe.""",
)

# 3 · Flujo determinista frente a agente (dos carriles horizontales)
b = [
    R(20, 26, 1140, 200, GT, INK, 2.5, 18),
    T(48, 66, 'FLUJO DETERMINISTA (script fijo)', 24, True, INK),
    R(48, 104, 210, 84, '#fff', INK, 2.5, 12),
    T(153, 152, 'Paso 1: leer', 21, True, INK, 'middle'),
    R(348, 104, 230, 84, '#fff', INK, 2.5, 12),
    T(463, 152, 'Paso 2: filtrar', 21, True, INK, 'middle'),
    R(668, 104, 230, 84, '#fff', INK, 2.5, 12),
    T(783, 152, 'Paso 3: guardar', 21, True, INK, 'middle'),
    R(980, 104, 150, 84, '#fff', OK, 2.5, 12),
    T(1055, 152, 'Fin fijo', 21, True, OK, 'middle'),
    A(262, 146, 344, 146, INK, 4),
    A(582, 146, 664, 146, INK, 4),
    A(902, 146, 976, 146, INK, 4),
    R(20, 260, 1140, 215, VT, VINO, 3, 18),
    T(48, 300, 'AGENTE AUTÓNOMO', 24, True, VINO),
    NODE(140, 385, 'usuario', 'META', None, INK, '#fff', r=46, isz=58, lsz=20),
    NODE(410, 385, 'ia', 'RAZONA', None, VINO, '#fff', r=52, isz=66, lsz=20),
    NODE(710, 385, 'funcion', 'ELIGE TOOL', None, DOSC, '#fff', r=52, isz=66, lsz=20),
    NODE(1020, 385, 'bd', 'OBSERVA', None, OK, '#fff', r=46, isz=58, lsz=20),
    A(192, 385, 352, 385, VINO, 4),
    A(468, 385, 652, 385, VINO, 4),
    A(768, 385, 968, 385, DOSC, 4),
    AP([(1020, 334), (1020, 294), (410, 294), (410, 326)], OK, 4, dash='8 6'),
    T(740, 284, 'repite hasta cumplir o pedir ayuda', 19, True, OK, 'middle'),
]
slide(
    3,
    'Arquitectura',
    'Flujo determinista frente a agente autónomo',
    'El flujo fijo ejecuta una receta invariable; el agente decide qué herramienta usar según el contexto.',
    'Basado en: OWASP LLM06:2025 Excessive Agency [cite:1] y OpenCode MCP [cite:6] · Dibujo propio',
    SVG(*b),
    """Fíjense en la diferencia estructural entre los dos carriles horizontales del diagrama. Arriba en gris tienen un flujo determinista clásico escrito por un programador. El software ejecuta exactamente el paso uno para leer, el paso dos para filtrar y el paso tres para guardar, recorriendo siempre el mismo camino predecible sin importar qué datos particulares aparezcan en la base. Abajo ven en cambio un agente autónomo en color vino. Al agente le entregamos una meta abierta en lenguaje natural y un catálogo de herramientas disponibles mediante el protocolo de contexto de modelo, MCP[cite:6]. El modelo razona qué hacer, elige qué herramienta invocar, observa la respuesta real que regresa el servidor y, sigan la flecha punteada verde superior, repite el ciclo hasta completar la meta o pedir ayuda. Esa flexibilidad resulta valiosa para CaribeMart, aunque exige controles estrictos porque no conocemos cada llamada por adelantado[cite:1].""",
)

# 4 · El bucle observar, razonar y actuar (ciclo circular de 4 nodos)
b = [
    C(590, 250, 92, DT, DOSC, 3),
    IC('engranaje', 590, 226, 76, DOSC),
    T(590, 296, 'BUCLE', 24, True, DOSC, 'middle'),
    T(590, 324, 'del agente', 19, False, INK, 'middle'),
]
quads = [
    (250, 120, 'ojo', '1. OBSERVAR', 'meta y datos previos', OK, OKT),
    (930, 120, 'ia', '2. RAZONAR', 'qué paso falta', VINO, VT),
    (930, 380, 'funcion', '3. ACTUAR', 'invocar herramienta MCP', DOSC, DT),
    (250, 380, 'bd', '4. RECIBIR', 'resultado real del servidor', INK, GT),
]
for x, y, ic, t1, t2, col, tint in quads:
    b.append(R(x - 175, y - 62, 350, 124, tint, col, 3, 18))
    b.append(IC(ic, x - 118, y, 56, col))
    b.append(T(x - 74, y - 8, t1, 24, True, col))
    b.append(T(x - 74, y + 26, t2, 19, False, INK))
b.append(A(430, 120, 748, 120, VINO, 5))
b.append(A(930, 186, 930, 312, DOSC, 5))
b.append(A(748, 380, 430, 380, INK, 5))
b.append(A(250, 312, 250, 186, OK, 5))
slide(
    4,
    'Fundamentos',
    'El bucle observar, razonar y actuar',
    'Cada iteración incorpora la respuesta real de la herramienta antes de decidir el siguiente paso.',
    'Basado en: OWASP LLM06:2025 Excessive Agency [cite:1] y MCP [cite:6] · Dibujo propio',
    SVG(*b),
    """Recorramos este ciclo [cite:1] en sentido horario empezando arriba a la izquierda en la caja verde. En el paso uno, observar, el agente recibe la instrucción inicial del operador junto con las reglas vigentes del proyecto y los resultados previos. En el paso dos, razonar, el modelo evalúa qué información real le falta para responder y qué herramienta del servidor MCP puede obtenerla [cite:6]. Sigan ahora la flecha dorada hacia abajo a la derecha. En el paso tres, actuar, propone una llamada estructurada con nombre de herramienta y argumentos en notación de objetos JavaScript, JSON, que el entorno ejecuta si cuenta con permiso. En el paso cuatro, recibir, vuelve la respuesta real desde la base de datos o servicio y queda registrada en la conversación. Luego sube nuevamente a observar con esa nueva evidencia acumulada hasta completar la meta o encontrar una pausa humana.""",
)

# 5 · Cómo el historial guía el siguiente paso (diagrama de secuencia 3 líneas de vida)
b = [
    R(60, 20, 260, 72, GT, INK, 2.5, 14),
    IC('usuario', 110, 56, 42, INK),
    T(150, 64, 'OPERADOR', 22, True, INK),
    R(460, 20, 260, 72, VT, VINO, 2.5, 14),
    IC('ia', 510, 56, 42, VINO),
    T(550, 64, 'HOST · MODELO', 22, True, VINO),
    R(830, 20, 320, 72, DT, DOSC, 2.5, 14),
    IC('servidor', 878, 56, 42, DOSC),
    T(916, 64, 'MCP CARIBEMART', 21, True, DOSC),
    '<line x1="190" y1="92" x2="190" y2="480" stroke="%s" stroke-width="3" stroke-dasharray="8 8"/>' % INK,
    '<line x1="590" y1="92" x2="590" y2="480" stroke="%s" stroke-width="3" stroke-dasharray="8 8"/>' % VINO,
    '<line x1="990" y1="92" x2="990" y2="480" stroke="%s" stroke-width="3" stroke-dasharray="8 8"/>' % DOSC,
]
msgs = [
    (155, 190, 590, '1. Meta: revisar atrasados', VINO, False),
    (225, 590, 990, '2. Llama pedidos_atrasados', VINO, False),
    (295, 990, 590, '3. Devuelve lista en JSON', OK, True),
    (365, 590, 990, '4. Propone cancelar_pedido', DOSC, False),
    (435, 590, 190, '5. Pide aprobar y redacta aviso', VINO, True),
]
for y, x1, x2, lbl, col, dsh in msgs:
    b.append(A(x1, y, x2, y, col, 4, dash='9 6' if dsh else None))
    mx = (x1 + x2) / 2
    w_bg = tw(lbl, 19, True) + 22
    b.append(R(mx - w_bg / 2, y - 34, w_bg, 28, '#fff', None, 0, 6))
    b.append(T(mx, y - 13, lbl, 19, True, col, 'middle'))
slide(
    5,
    'Protocolo',
    'Cómo el historial guía el siguiente paso',
    'El host opencode conserva cada llamada y cada observación para alimentar el siguiente turno.',
    'Basado en: OpenCode MCP docs [cite:6] · Dibujo propio',
    SVG(*b),
    """Este diagrama de secuencia muestra quién dialoga con quién durante una tarea multipaso. A la izquierda tienen al operador humano, en el centro al host opencode junto con el modelo de lenguaje, y a la derecha al servidor MCP caribemart corriendo sobre Node[cite:6]. En el mensaje uno, el operador escribe su meta inicial de revisar pedidos atrasados. En el mensaje dos, el modelo invoca la herramienta de solo lectura pedidos atrasados. En el mensaje tres, señalado con línea punteada verde, el servidor responde con los pedidos filtrados en formato JSON. Con esa observación ya incorporada dentro del historial de contexto, en el mensaje cuatro el modelo razona qué registros superan el umbral permitido y propone llamar cancelar pedido. Finalmente, en el mensaje cinco, la plataforma frena cualquier cambio real para pedir aprobación al operador y prepara el borrador del aviso.""",
)

# 6 · El escenario operativo de CaribeMart (foto lateral bodega + tarjetas de datos)
b = [
    FOTO('bodega', 14, 20, 440, 460, 16, 'xMidYMid'),
    GRAD_SCRIM(14, 320, 440, 160, .85, 16),
    T(40, 412, 'CaribeMart · 60 almacenes', 26, True, '#fff'),
    T(40, 448, 'Barranquilla · respaldo Bogotá', 20, False, '#F3D9DE'),
    R(484, 20, 676, 132, VT, VINO, 3, 16),
    IC('alerta', 536, 86, 54, VINO),
    T(584, 68, 'EL PROBLEMA DIARIO', 22, True, VINO),
    T(584, 102, 'Horas revisando atrasos a mano', 21, False, INK),
    T(584, 132, 'y redactando avisos por cliente', 21, False, INK),
    R(484, 180, 676, 132, DT, DOSC, 3, 16),
    IC('ia', 536, 246, 54, DOSC),
    T(584, 228, 'LA META DEL ASISTENTE', 22, True, DOSC),
    T(584, 262, 'Detectar atrasos, proponer cancelación', 21, False, INK),
    T(584, 292, 'y preparar el texto de respuesta', 21, False, INK),
    R(484, 340, 676, 140, OKT, OK, 3, 16),
    IC('escudo', 536, 410, 54, OK),
    T(584, 390, 'DOS CONDICIONES NO NEGOCIABLES', 22, True, OK),
    T(584, 424, '1. Nada escribe sin permiso humano', 21, False, INK),
    T(584, 456, '2. Ignora órdenes ocultas en datos', 21, False, INK),
]
slide(
    6,
    'CaribeMart',
    'El caso operativo de CaribeMart en el Corte 3',
    'Sesenta tiendas ficticias en el Caribe con dos reglas gerenciales estrictas antes de automatizar.',
    'Basado en: Proyecto de Aula Corte 3',
    SVG(*b),
    """Aterricemos estos conceptos arquitectónicos en el hilo conductor de nuestro curso. CaribeMart opera sesenta almacenes en el país, con centro de datos principal en Barranquilla y respaldo pasivo en Bogotá para garantizar continuidad operativa. Cada mañana el equipo de servicio al cliente perdía horas valiosas revisando manualmente qué envíos estaban atrasados en Cartagena, Santa Marta o Montería, decidiendo cuáles cancelar y redactando correos uno por uno. Como muestra la tarjeta dorada del centro a la derecha, la gerencia aprobó construir un asistente en opencode conectado al servidor MCP de CaribeMart, pero fijó dos condiciones estrictas que no se negocian, visibles abajo en la tarjeta verde. Primera condición: ninguna herramienta que modifique pedidos corre sin autorización humana previa. Segunda condición: el asistente jamás debe obedecer instrucciones escondidas dentro de los datos almacenados. Ambas reglas guiarán toda la semana.""",
    fotos=['bodega'],
)

# 7 · Paso a paso de la cadena en CaribeMart (escalera de 4 peldaños)
steps = [
    (30, 356, '1. CONSULTAR', 'pedidos_atrasados', 'solo lectura con zod', OK, OKT, 'bd'),
    (316, 256, '2. EVALUAR', 'reglas AGENTS.md', 'días límite y tono', DOSC, DT, 'documento'),
    (602, 156, '3. PROPONER', 'cancelar_pedido', 'pide permiso ask', VINO, VT, 'candado'),
    (888, 56, '4. REDACTAR', 'aviso al cliente', 'tono claro y cordial', INK, GT, 'usuario'),
]
b = []
for i, (x, y, t1, t2, t3, col, tint, ic) in enumerate(steps):
    b.append(R(x, y, 262, 124, tint, col, 3, 16))
    b.append(IC(ic, x + 36, y + 34, 40, col))
    b.append(T(x + 66, y + 42, t1, 20, True, col))
    b.append(T(x + 22, y + 78, t2, 17, True, INK, mono=t2.endswith('s') or '_' in t2))
    b.append(T(x + 22, y + 108, t3, 17, False, GRIS))
    if i < 3:
        nx, ny = steps[i + 1][0], steps[i + 1][1]
        b.append(AP([(x + 262, y + 60), (x + 275, y + 60), (x + 275, ny + 60), (nx - 4, ny + 60)], col, 4))
b.append(R(36, 36, 520, 112, '#fff', VINO, 2.5, 14))
b.append(T(60, 74, 'INSTRUCCIÓN AL AGENTE', 19, True, VINO))
b.append(T(60, 108, '«Revisa los pedidos atrasados, propón cuáles', 18, False, INK))
b.append(T(60, 134, 'cancelar y redacta el mensaje para cada cliente»', 18, False, INK))
slide(
    7,
    'Flujo',
    'Cadena completa de herramientas en CaribeMart',
    'El prompt del Proyecto Corte 3 dispara cuatro etapas ordenadas sobre pedidos de prueba.',
    'Basado en: Proyecto de Aula Corte 3 y Zod docs [cite:9] · Dibujo propio',
    SVG(*b),
    """Miren esta escalera ascendente de cuatro peldaños que describe el recorrido completo del proyecto. Arriba a la izquierda ven la instrucción literal que le enviarán a opencode en la prueba del tercer corte: revisar los pedidos atrasados, proponer cuáles cancelar y redactar el mensaje para cada cliente. En el primer peldaño abajo en verde, el agente llama automáticamente a pedidos atrasados, una herramienta de solo lectura con entrada validada usando zod [cite:9]. En el segundo peldaño en dorado, contrasta las fechas y estados de cada registro contra las políticas escritas en AGENTS punto md para determinar cuáles superan el límite de días. En el tercer peldaño en vino, propone invocar cancelar pedido únicamente sobre los casos que aplican, deteniéndose frente al candado humano. Y en el cuarto peldaño redacta el mensaje claro y cordial adaptado a cada comprador afectado.""",
)

# 8 · Cuándo detener el bucle del agente (árbol de decisión)
b = [
    NODE(140, 250, 'engranaje', 'TURNO DEL', 'AGENTE', VINO, VT, r=66, isz=76, lsz=20, ssz=20),
]
branches = [
    (75, 'META CUMPLIDA', 'ya tiene todos los datos', OK, OKT, 'Responde al operador', 'check'),
    (195, 'PIDE APROBACIÓN', 'va a escribir o cancelar', DOSC, DT, 'Pausa esperando al humano', 'candado'),
    (315, 'ERROR CONTROLADO', 'pedido inexistente o inválido', MAL, MALT, 'Informa sin estrellarse', 'alerta'),
    (435, 'LÍMITE DE PASOS', 'evita bucles infinitos', INK, GT, 'Corta y pide intervención', 'reloj'),
]
for y, t1, t2, col, tint, res, ic in branches:
    b.append(AP([(212, 250), (280, 250), (305, y), (350, y)], col, 4))
    b.append(R(354, y - 44, 380, 88, tint, col, 2.5, 14))
    b.append(IC(ic, 396, y, 44, col))
    b.append(T(432, y - 6, t1, 20, True, col))
    b.append(T(432, y + 24, t2, 18, False, INK))
    b.append(A(738, y, 814, y, col, 4))
    b.append(R(818, y - 44, 342, 88, '#fff', col, 2.5, 14))
    b.append(T(989, y + 8, res, 19, True, col, 'middle'))
slide(
    8,
    'Control',
    'Cuatro condiciones para detener el bucle',
    'Un agente seguro nunca gira sin fin: debe saber parar cuando cumple, duda, falla o alcanza un tope.',
    'Basado en: MCP Security Best Practices [cite:7] · Dibujo propio',
    SVG(*b),
    """Un error frecuente cuando alguien diseña su primer agente es dejar el bucle abierto sin criterios explícitos de terminación [cite:7]. Sigan de arriba hacia abajo las cuatro ramas que salen desde el nodo central del turno. La primera rama en verde representa la salida normal y esperada: la meta quedó resuelta con todos los datos necesarios y el modelo entrega su respuesta final al operador. La segunda rama en dorado aparece cuando el agente pretende invocar una herramienta de escritura como cancelar pedido y el host congela el turno esperando confirmación de la persona. La tercera rama en rojo ocurre frente a un error controlado, por ejemplo consultar un identificador inexistente o intentar cancelar un envío entregado, donde el servidor responde texto claro sin estrellarse. Finalmente, la cuarta rama fija un límite máximo de pasos para cortar bucles repetitivos y evitar consumo desbordado de recursos.""",
)

# 9 · Lectura frente a escritura en el bucle (dos zonas con frontera punteada)
b = [
    R(18, 24, 540, 452, OKT, OK, 3, 20),
    R(622, 24, 540, 452, MALT, MAL, 3, 20),
    T(288, 68, 'ZONA DE SOLO LECTURA', 26, True, OK, 'middle'),
    T(892, 68, 'ZONA DE ESCRITURA', 26, True, MAL, 'middle'),
    '<line x1="590" y1="24" x2="590" y2="476" stroke="%s" stroke-width="5" stroke-dasharray="12 10"/>' % VINO,
    C(590, 250, 42, '#fff', VINO, 3.5),
    IC('escudo', 590, 250, 52, VINO),
]
reads = [
    (130, 'consultar_pedido'),
    (230, 'listar_pedidos_por_estado'),
    (330, 'pedidos_atrasados'),
]
for y, nm in reads:
    b.append(R(62, y, 452, 68, '#fff', OK, 2.5, 14))
    b.append(IC('ojo', 102, y + 34, 38, OK))
    b.append(T(136, y + 42, nm, 21, True, OK, mono=True))
b.append(T(288, 444, 'No alteran pedidos.json · seguras en bucle', 19, True, OK, 'middle'))

writes = [
    (150, 'crear_pedido', 'inserta registro nuevo'),
    (280, 'cancelar_pedido', 'cambia estado y motivo'),
]
for y, nm, desc in writes:
    b.append(R(666, y, 452, 92, '#fff', MAL, 2.5, 14))
    b.append(IC('candado', 706, y + 46, 40, MAL))
    b.append(T(740, y + 38, nm, 22, True, MAL, mono=True))
    b.append(T(740, y + 70, desc, 18, False, INK))
b.append(T(892, 444, 'Exigen validación zod + permiso humano', 19, True, MAL, 'middle'))
slide(
    9,
    'Frontera',
    'Separar lectura de escritura en CaribeMart',
    'Las cinco herramientas del proyecto se dividen según su impacto sobre pedidos.json.',
    'Basado en: Proyecto Corte 3, OpenCode [cite:5] y Zod [cite:9] · Dibujo propio',
    SVG(*b),
    """Miren la frontera vertical vino que divide el lienzo exactamente por la mitad con un escudo en el centro. A la izquierda dentro de la zona verde viven las tres herramientas de solo lectura de CaribeMart: consultar pedido y listar pedidos por estado heredadas del laboratorio siete, más la nueva herramienta pedidos atrasados que agregan en el proyecto. Ninguna de estas tres funciones altera el archivo pedidos punto json, de modo que el agente puede invocarlas libremente dentro de su bucle sin riesgo de corromper registros comerciales. A la derecha dentro de la zona roja están ubicadas las dos herramientas que sí modifican estado: crear pedido y cancelar pedido. Toda llamada que pretenda cruzar esa frontera de seguridad hacia la derecha debe superar dos barreras complementarias: validación estricta con zod [cite:9] en el servidor y permiso humano explícito en opencode [cite:5] antes de guardar.""",
)

# 10 · OWASP LLM06: Agencia Excesiva (nodo central + 3 causas raíz)
b = [
    NODE(210, 250, 'alerta', 'OWASP LLM06 [1]', 'Agencia Excesiva', MAL, MALT, r=86, isz=100, lsz=24, ssz=20),
]
causes = [
    (95, 'FUNCIONALIDAD EXCESIVA', 'Expone herramientas de más (ej. borrar todo)', 'funcion'),
    (250, 'PERMISOS EXCESIVOS', 'Credenciales de administrador sin mínimo privilegio', 'llave'),
    (405, 'AUTONOMÍA EXCESIVA', 'Ejecuta acciones críticas sin verificación humana', 'engranaje'),
]
for y, t1, t2, ic in causes:
    b.append(A(302, 250 + (y - 250) * .28, 456, y, MAL, 5))
    b.append(R(462, y - 56, 694, 112, '#fff', MAL, 3, 16))
    b.append(C(522, y, 36, MALT, MAL, 2))
    b.append(IC(ic, 522, y, 44, MAL))
    b.append(T(578, y - 8, t1, 22, True, MAL))
    b.append(T(578, y + 26, t2, 19, False, INK))
slide(
    10,
    'Riesgo',
    'OWASP LLM06:2025 — Agencia Excesiva en agentes',
    'Cuando un modelo mal encaminado ejecuta acciones dañinas por permisos o autonomía sin freno.',
    'Basado en: OWASP LLM06:2025 Excessive Agency [cite:1] · Dibujo propio',
    SVG(*b),
    """Según la guía internacional de seguridad OWASP para aplicaciones basadas en modelos de lenguaje grandes, el sexto riesgo crítico lleva por nombre Agencia Excesiva, identificado como LLM cero seis [cite:1]. Esta vulnerabilidad aparece cuando concedemos al agente demasiado margen de acción frente a salidas inesperadas, interpretaciones ambiguas o entradas manipuladas por terceros. Miren las tres causas raíz documentadas por OWASP en las tarjetas de la derecha. Primera causa, funcionalidad excesiva: conectar herramientas que el asistente realmente no necesita, como funciones capaces de vaciar tablas completas de la tienda. Segunda causa, permisos excesivos: ejecutar el servidor con credenciales de administrador sin aplicar mínimo privilegio sobre los archivos. Tercera causa, autonomía excesiva: permitir que invoque operaciones destructivas o de escritura sin confirmación humana previa. Atacar simultáneamente estas tres raíces es indispensable para operar agentes confiables dentro de CaribeMart.""",
)

# 11 · El efecto dominó de una falla sin freno (cascada)
b = [
    R(24, 34, 290, 120, DT, DOSC, 3, 16),
    IC('alerta', 74, 94, 48, DOSC),
    T(114, 82, 'FALLA INICIAL', 21, True, DOSC),
    T(114, 114, 'dato mal interpretado', 18, False, INK),
    A(320, 94, 410, 94, MAL, 5),
    R(416, 34, 330, 120, MALT, MAL, 3, 16),
    IC('funcion', 466, 94, 48, MAL),
    T(504, 82, 'LLAMADA EN BUCLE', 21, True, MAL),
    T(504, 114, 'cancela diez pedidos', 18, False, INK),
    A(752, 94, 842, 94, MAL, 5),
    R(848, 34, 308, 120, MAL, None, 0, 16),
    C(898, 94, 32, '#fff'),
    IC('dinero', 898, 94, 46, MAL),
    T(938, 82, 'DAÑO REAL', 22, True, '#fff'),
    T(938, 114, 'clientes sin envío', 19, False, '#F9EEF0'),
    R(24, 224, 1132, 240, '#fff', VINO, 3, 18),
    IC('escudo', 104, 344, 76, VINO),
    T(178, 286, 'POR QUÉ NO BASTA CON «CONFIAR EN EL PROMPT»', 24, True, VINO),
    T(178, 332, 'Un modelo probabilístico puede equivocarse incluso sin atacantes.', 21, False, INK),
    T(178, 368, 'Sin validación en código ni permiso ask, un error escala en segundos.', 21, False, INK),
    T(178, 412, 'La seguridad real vive en la arquitectura fuera del modelo.', 21, True, OK),
]
slide(
    11,
    'Impacto',
    'El efecto dominó de automatizar sin frenos',
    'Un fallo aislado de razonamiento puede multiplicarse rápido si la escritura no tiene compuerta.',
    'Basado en: OWASP LLM06:2025 Excessive Agency [cite:1] · Dibujo propio',
    SVG(*b),
    """Fíjense en la cadena superior de izquierda a derecha, porque ilustra un problema serio de confiabilidad. No hace falta siquiera enfrentar a un atacante malicioso para sufrir un incidente operativo grave con un agente autónomo. Basta una fecha mal interpretada, una zona horaria confusa o una equivocación ocasional del modelo sobre los días de retraso para que encadene varias llamadas en segundos y termine cancelando diez pedidos válidos en Barranquilla o Cartagena, dejando clientes reales sin despacho. Lean ahora la tarjeta vino inferior. Confiar únicamente en advertencias amables escritas dentro del prompt del sistema resulta insuficiente porque los modelos de lenguaje son probabilísticos y cometen errores incluso sin malicia. Como subraya la línea verde de cierre, la seguridad real debe vivir en la arquitectura fuera del modelo: en los permisos del host, en server punto js y en la revisión humana [cite:1].""",
)

# 12 · Matriz de autonomía: qué delegar y qué frenar (matriz 2x2 con ejes e iconos -> >= 6 formas)
b = [
    R(156, 24, 476, 200, OKT, OK, 3, 14),
    R(654, 24, 476, 200, DT, DOSC, 3, 14),
    R(156, 244, 476, 200, DT, DOSC, 3, 14),
    R(654, 244, 476, 200, MALT, MAL, 3, 14),
    A(122, 444, 122, 24, INK, 4),
    A(156, 462, 1130, 462, INK, 4),
    IC('ojo', 202, 70, 38, OK),
    T(394, 70, 'BAJO IMPACTO · REVERSIBLE', 20, True, OK, 'middle'),
    T(394, 118, 'consultar_pedido', 22, True, INK, 'middle', mono=True),
    T(394, 158, 'pedidos_atrasados', 22, True, INK, 'middle', mono=True),
    T(394, 200, 'Permiso: allow (automático)', 19, True, OK, 'middle'),
    IC('documento', 700, 70, 38, DOSC),
    T(892, 70, 'ALTO IMPACTO · REVERSIBLE', 20, True, DOSC, 'middle'),
    T(892, 122, 'redactar borrador de mensaje', 21, True, INK, 'middle'),
    T(892, 162, 'crear_pedido de prueba', 21, True, INK, 'middle'),
    T(892, 200, 'Revisión humana recomendada', 19, True, DOSC, 'middle'),
    IC('alerta', 202, 290, 38, DOSC),
    T(394, 290, 'BAJO IMPACTO · IRREVERSIBLE', 20, True, DOSC, 'middle'),
    T(394, 342, 'enviar correo automático al cliente', 21, True, INK, 'middle'),
    T(394, 382, 'marcar nota interna permanente', 21, True, INK, 'middle'),
    T(394, 420, 'Permiso: ask o flujo aprobado', 19, True, DOSC, 'middle'),
    IC('candado', 700, 290, 38, MAL),
    T(892, 290, 'ALTO IMPACTO · IRREVERSIBLE', 20, True, MAL, 'middle'),
    T(892, 340, 'cancelar_pedido', 24, True, MAL, 'middle', mono=True),
    T(892, 380, 'borrar base o emitir reembolso', 21, True, INK, 'middle'),
    T(892, 420, 'Permiso: ask obligatorio o deny', 19, True, MAL, 'middle'),
    T(64, 120, 'BAJO', 20, True, GRIS, 'middle'),
    T(64, 148, 'RIESGO', 18, True, GRIS, 'middle'),
    T(64, 340, 'ALTO', 20, True, MAL, 'middle'),
    T(64, 368, 'RIESGO', 18, True, MAL, 'middle'),
    T(394, 490, 'OPERACIÓN REVERSIBLE', 18, True, GRIS, 'middle'),
    T(892, 490, 'OPERACIÓN IRREVERSIBLE', 18, True, MAL, 'middle'),
]
slide(
    12,
    'Criterio',
    'Matriz de autonomía: qué delegar y qué frenar',
    'El nivel de control depende del impacto sobre el negocio y de si la acción puede deshacerse.',
    'Basado en: NIST AI RMF [cite:10] y OWASP LLM06 [cite:1] · Dibujo propio',
    SVG(*b),
    """Esta matriz dos por dos les entrega un criterio de ingeniería claro aplicable a cualquier plataforma cloud del mercado [cite:1,10]. En el eje horizontal distinguimos entre operaciones fáciles de revertir y operaciones irreversibles sobre el negocio. En el eje vertical evaluamos si el impacto operativo y financiero es bajo o alto. Arriba a la izquierda en verde habitan las consultas de solo lectura como consultar pedido y pedidos atrasados: no alteran datos y corren en modo automático sin fricción. En los cuadrantes dorados quedan tareas como preparar borradores de respuesta, crear pedidos de prueba o enviar comunicaciones externas automáticas que conviene supervisar. Abajo a la derecha en rojo aparece cancelar pedido: implica alto impacto comercial y no se deshace fácilmente frente al comprador, por lo que exige confirmación humana obligatoria mediante ask. Las operaciones destructivas masivas simplemente se prohíben con deny.""",
)

# 13 · Errores típicos al diseñar agentes (3 filas mal vs bien)
rows = [
    (40, 'DAR PERMISO TOTAL', 'todas las herramientas en allow', 'dejar solo lectura en allow'),
    (190, 'SIN TOPE DE CAMBIOS', 'puede cancelar cien en una orden', 'limitar alcance y exigir ask'),
    (340, 'IGNORAR EL ERROR', 'lanza excepción y tumba el servidor', 'devolver mensaje claro controlado'),
]
b = []
for y, t1, t2, fix in rows:
    b.append(R(26, y, 500, 118, MALT, MAL, 3, 16))
    b.append(CH(76, y + 59, 26, False))
    b.append(T(120, y + 50, t1, 22, True, MAL))
    b.append(T(120, y + 86, t2, 19, False, INK))
    b.append(A(536, y + 59, 636, y + 59, VINO, 5))
    b.append(R(646, y, 508, 118, OKT, OK, 3, 16))
    b.append(CH(696, y + 59, 26, True))
    b.append(T(740, y + 66, fix, 22, True, OK))
slide(
    13,
    'Error común',
    'Tres fallos clásicos al pasar de función a agente',
    'Corregir estas prácticas antes de probar evita pérdidas de datos y bloqueos en el proyecto.',
    'Basado en: Proyecto Corte 3 y MCP Security [cite:7] · Dibujo propio',
    SVG(*b),
    """Revisen estos tres tropiezos clásicos que aparecen con mucha frecuencia al pasar de herramientas sueltas a un agente completo en clase. En la primera fila arriba, habilitar permiso automático total por pereza de aprobar en consola permite que el modelo escriba sin supervisión alguna; la corrección verde a la derecha consiste en dejar únicamente las consultas de lectura en modo automático. En la fila central, permitir que una sola llamada altere decenas o cientos de registros multiplica inmediatamente el radio de daño ante cualquier fallo; la práctica segura limita el alcance a un registro por turno y exige verificación humana. En la fila inferior, dejar que un dato inválido o un pedido ya entregado lance una excepción no capturada tumba el servidor MCP que corre sobre entrada y salida estándar; siempre atrapen errores y devuelvan mensajes claros al modelo [cite:7].""",
)

# 14 · Síntesis de la Parte 1 (ruta horizontal con 4 hitos)
b = [
    '<line x1="70" y1="250" x2="1110" y2="250" stroke="%s" stroke-width="10" stroke-linecap="round" stroke-dasharray="2 18"/>' % DOR
]
pts = [
    (160, 'engranaje', 'Bucle dinámico', 'observar, razonar, actuar', VINO, VT, 'up'),
    (445, 'funcion', 'Encadenar pasos', 'atrasos hacia cancelación', DOSC, DT, 'down'),
    (730, 'alerta', 'OWASP LLM06 [1]', 'acotar permisos y alcance', MAL, MALT, 'up'),
    (1015, 'escudo', 'Lectura vs escritura', 'frenar antes de modificar', OK, OKT, 'down'),
]
for i, (x, ic, t1, t2, col, tint, d) in enumerate(pts, 1):
    b.append(C(x, 250, 56, tint, col, 3))
    b.append(IC(ic, x, 250, 72, col))
    b.append(BADGE(x + 42, 206, i, col, 20, 20))
    yy = 110 if d == 'up' else 388
    b.append(T(x, yy, t1, 24, True, col, 'middle'))
    b.append(T(x, yy + 32, t2, 18, False, INK, 'middle'))
slide(
    14,
    'Síntesis',
    'La Parte 1 en cuatro ideas maestras',
    'Ya sabemos cómo razona un agente y por qué debemos acotar su autonomía desde el inicio.',
    'Basado en: OWASP LLM06:2025 [cite:1] · Dibujo propio',
    SVG(*b),
    """Cerramos esta primera parte resumiendo cuatro ideas maestras fundamentales que sostienen todo el diseño de la semana quince. Primero, un agente no sigue un guion estático: opera dentro de un bucle dinámico de observar, razonar, actuar y recibir que aprovecha el historial acumulado de cada conversación. Segundo, en CaribeMart esa cadena conecta la consulta de pedidos atrasados con las reglas de AGENTS punto md, propone cancelar pedido y prepara avisos cordiales por ciudad. Tercero, entregar herramientas sobrantes, credenciales demasiado amplias o autonomía sin freno produce Agencia Excesiva, documentada como OWASP LLM cero seis [cite:1]. Cuarto, trazar una frontera nítida entre lectura segura y escritura controlada nos indica exactamente dónde instalar las compuertas. En la segunda parte aplicaremos el marco cuatro D de fluidez con inteligencia artificial [cite:8] y configuraremos el permiso ask paso a paso dentro del archivo opencode punto json [cite:5].""",
)
