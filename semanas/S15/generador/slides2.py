from lib import *
from reg import slide

# 15 · Por qué el humano sigue en el circuito (foto centralita + compuerta humana)
b = [
    FOTO('centralita', 14, 20, 440, 460, 16, 'xMidYMid'),
    GRAD_SCRIM(14, 320, 440, 160, .85, 16),
    T(40, 412, 'Human-in-the-loop (HITL)', 24, True, '#fff'),
    T(40, 446, 'la persona mantiene el mando', 19, False, '#F3D9DE'),
    NODE(590, 180, 'ia', 'AGENTE', 'propone acción', VINO, VT, r=58, isz=72, lsz=20, ssz=17),
    R(726, 60, 140, 260, DT, DOSC, 3, 16),
    IC('usuario', 796, 130, 62, DOSC),
    IC('candado', 796, 224, 54, DOSC),
    T(796, 294, 'APROBAR', 20, True, DOSC, 'middle'),
    NODE(1050, 180, 'bd', 'PEDIDOS.JSON', 'se modifica solo', OK, OKT, r=58, isz=72, lsz=20, ssz=17),
    A(652, 180, 722, 180, VINO, 5),
    A(870, 180, 988, 180, OK, 5),
    R(490, 355, 670, 125, '#fff', VINO, 2.5, 16),
    T(520, 396, 'La IA acelera el análisis y la redacción.', 21, True, VINO),
    T(520, 434, 'El operador humano autoriza los cambios reales.', 21, False, INK),
]
slide(
    15,
    'Verificación humana',
    'Human-in-the-loop: delegar análisis, no autoridad',
    'El principio HITL coloca una pausa obligatoria antes de que una herramienta modifique datos.',
    'Basado en: OWASP LLM06 [cite:1] y MCP Security [cite:7]',
    SVG(*b),
    """Arrancamos la segunda parte observando a la izquierda la fotografía histórica de una centralita telefónica manual. En aquella época ninguna llamada quedaba enlazada entre dos ciudades hasta que la operadora conectaba físicamente el cable en el tablero después de verificar el destino. En ingeniería de agentes modernos rescatamos exactamente ese principio bajo el nombre human-in-the-loop, abreviado HITL [cite:1,7]. Sigan el flujo horizontal a la derecha. Nuestro agente de inteligencia artificial lee decenas de pedidos atrasados, compara fechas y redacta propuestas en cuestión de segundos, pero justo antes de tocar el archivo pedidos punto json se encuentra con la compuerta dorada del operador humano y el candado. Ahí la ejecución se congela esperando autorización expresa. De este modo aprovechamos la enorme velocidad analítica del modelo, pero conservamos siempre la autoridad operativa, financiera y legal en manos de las personas responsables de CaribeMart.""",
    fotos=['centralita'],
)

# 16 · El marco 4D de fluidez con IA (4 columnas en abanico)
cols = [
    ('1. DELEGACIÓN', 'qué hace la IA', 'y qué conserva', 'el humano', VINO, VT, 'llave'),
    ('2. DESCRIPCIÓN', 'metas claras y', 'reglas escritas', 'en AGENTS.md', DOSC, DT, 'documento'),
    ('3. DISCERNIMIENTO', 'revisar si la', 'propuesta tiene', 'sentido real', OK, OKT, 'ojo'),
    ('4. DILIGENCIA', 'asumir autoría,', 'probar defensas', 'y dejar bitácora', INK, GT, 'escudo'),
]
b = [
    R(30, 24, 1120, 72, VINO, None, 0, 14),
    T(590, 68, 'MARCO 4D DE FLUIDEZ CON INTELIGENCIA ARTIFICIAL [8]', 24, True, '#fff', 'middle'),
]
x = 30
w_c = 258
gap = 29
for t1, l1, l2, l3, col, tint, ic in cols:
    b.append(R(x, 124, w_c, 350, tint, col, 3, 18))
    b.append(C(x + w_c / 2, 206, 44, '#fff', col, 2.5))
    b.append(IC(ic, x + w_c / 2, 206, 54, col))
    b.append(T(x + w_c / 2, 290, t1, 21, True, col, 'middle'))
    b.append(T(x + w_c / 2, 344, [l1, l2, l3], 20, False, INK, 'middle', lh=1.35))
    x += w_c + gap
slide(
    16,
    'Marco 4D',
    'Las cuatro D para trabajar con agentes de IA',
    'Delegación, Descripción, Discernimiento y Diligencia guían el uso responsable en CaribeMart.',
    'Basado en: Anthropic Academy, AI Fluency Framework (4D) [cite:8] · Dibujo propio',
    SVG(*b),
    """Para ordenar con rigor la colaboración cotidiana entre el operador humano y el asistente inteligente aplicamos el marco cuatro D de fluidez con inteligencia artificial [cite:8]. Sigan las cuatro columnas de izquierda a derecha debajo del encabezado vino. La primera D es Delegación: decidir con criterio técnico qué subtareas encargamos al modelo, como consultar atrasos o redactar borradores, y cuáles reservamos al humano, como confirmar cambios definitivos. La segunda D es Descripción: expresar con total precisión tanto la meta de la sesión como las reglas permanentes escritas en AGENTS punto md. La tercera D es Discernimiento: examinar críticamente la propuesta del agente para detectar errores de fecha, motivos pobres o textos sospechosos. La cuarta D es Diligencia: asumir autoría responsable sobre el resultado final, probar las defensas antes y después y documentar cada decisión en bitácora antes de entregar.""",
)

# 17 · D1 y D2: Delegación y Descripción (dos bloques horizontales con detalle)
b = [
    R(24, 30, 1132, 200, VT, VINO, 3, 18),
    C(110, 130, 56, '#fff', VINO, 3),
    IC('llave', 110, 130, 68, VINO),
    T(196, 84, 'D1 · DELEGACIÓN: repartir bien el trabajo', 26, True, VINO),
    T(196, 126, '• Agente lee pedidos_atrasados, cruza fechas y redacta mensajes.', 20, False, INK),
    T(196, 162, '• Humano decide si un pedido realmente debe cancelarse.', 20, False, INK),
    T(196, 198, '• Nunca delegar decisiones irreversibles sin verificación.', 20, True, VINO),
    R(24, 260, 1132, 210, DT, DOSC, 3, 18),
    C(110, 365, 56, '#fff', DOSC, 3),
    IC('documento', 110, 365, 68, DOSC),
    T(196, 314, 'D2 · DESCRIPCIÓN: dar contexto y límites precisos', 26, True, DOSC),
    T(196, 356, '• Prompt concreto: revisar atrasos, proponer cancelación y redactar aviso.', 20, False, INK),
    T(196, 392, '• Reglas permanentes en AGENTS.md: días límite y tono cordial.', 20, False, INK),
    T(196, 428, '• Sin buena descripción el agente inventa criterios propios.', 20, True, DOSC),
]
slide(
    17,
    'Marco 4D',
    'Delegación y Descripción aplicadas a CaribeMart',
    'Antes de ejecutar nada, definimos quién tiene autoridad y bajo qué reglas debe operar el agente.',
    'Basado en: Anthropic AI Fluency (4D) [cite:8] y Proyecto Corte 3 · Dibujo propio',
    SVG(*b),
    """Profundicemos ahora en las dos primeras competencias del marco [cite:8] aplicándolas directamente sobre el proyecto de aula de CaribeMart. En el bloque superior vino, Delegación significa trazar una línea limpia entre asistir en el análisis y decidir sobre el negocio. Delegamos al modelo invocar pedidos atrasados, cruzar fechas de despacho y preparar los borradores de mensaje por ciudad del Caribe, porque ahí multiplica nuestra productividad operativa diaria. Pero jamás le delegamos cancelar compras reales de clientes sin revisión humana previa. En el bloque inferior dorado, Descripción consiste en darle al asistente instrucciones inequívocas tanto en el prompt de la sesión como en el archivo permanente AGENTS punto md. Allí fijamos con exactitud cuántos días definen un atraso, qué tono cordial mantenemos con cada comprador y la regla estricta de que ningún texto almacenado puede reemplazar las políticas oficiales de la tienda.""",
)

# 18 · D3 y D4: Discernimiento y Diligencia (dos paneles lado a lado)
b = [
    R(20, 26, 554, 448, OKT, OK, 3, 18),
    R(606, 26, 554, 448, GT, INK, 3, 18),
    C(297, 108, 48, '#fff', OK, 3),
    IC('ojo', 297, 108, 60, OK),
    T(297, 190, 'D3 · DISCERNIMIENTO', 26, True, OK, 'middle'),
    T(297, 224, 'Evaluar con ojo crítico antes de aprobar', 19, False, GRIS, 'middle'),
    R(54, 256, 486, 188, '#fff', OK, 2, 14),
    T(80, 296, '1. ¿El pedido lleva más de N días?', 19, False, INK),
    T(80, 336, '2. ¿Sigue pendiente o ya fue entregado?', 19, False, INK),
    T(80, 376, '3. ¿El motivo coincide con el caso real?', 19, False, INK),
    T(80, 416, '4. ¿Hay notas sospechosas manipulándolo?', 19, True, MAL),
    C(883, 108, 48, '#fff', INK, 3),
    IC('escudo', 883, 108, 60, INK),
    T(883, 190, 'D4 · DILIGENCIA', 26, True, INK, 'middle'),
    T(883, 224, 'Responder por el resultado ante el cliente', 19, False, GRIS, 'middle'),
    R(640, 256, 486, 188, '#fff', INK, 2, 14),
    T(666, 296, '1. Probar defensas antes y después.', 19, False, INK),
    T(666, 336, '2. Llevar bitácora de aprobado y rechazado.', 19, False, INK),
    T(666, 376, '3. Verificar cumplimiento de Ley 1581 [11].', 19, False, INK),
    T(666, 416, '4. Explicar las decisiones en el PDF.', 19, True, VINO),
]
slide(
    18,
    'Marco 4D',
    'Discernimiento y Diligencia frente al asistente',
    'Aprobar a ciegas anula la supervisión humana; debemos auditar y asumir responsabilidad.',
    'Basado en: Anthropic AI Fluency (4D) [cite:8], Ley 1581/2012 [cite:11] y Proyecto Corte 3 · Dibujo propio',
    SVG(*b),
    """Ahora revisen las dos competencias que entran en acción cuando el agente ya presenta su propuesta concreta en pantalla. A la izquierda en verde tienen el Discernimiento [cite:8]. Si un operador presiona aprobar por inercia sin leer los argumentos, la supervisión humana se vuelve un teatro inútil y pierde todo su valor de control. Discernir exige comprobar cuatro preguntas puntuales: confirmar cuántos días lleva realmente el pedido, revisar que siga pendiente y no haya sido entregado, validar que el motivo tenga sentido real y vigilar si aparece alguna nota sospechosa intentando desviar la respuesta. A la derecha en gris está la Diligencia: responder profesionalmente por las consecuencias ante el cliente. En el Proyecto Corte tres esto implica probar sus defensas, llevar bitácora fiel de lo aprobado y rechazado, cumplir la Ley mil quinientos ochenta y uno [cite:11] y redactar explicaciones con palabras propias.""",
)

# 19 · Los tres niveles de permiso en opencode (semáforo con TOGGLE)
rows = [
    (86, True, OK, '"allow"', 'Ejecuta sin preguntar', 'Ideal para herramientas de solo lectura como pedidos_atrasados', 'ojo'),
    (250, True, DOSC, '"ask"', 'Pausa y pide confirmación', 'Obligatorio para caribemart_cancelar_pedido antes de escribir', 'usuario'),
    (414, False, MAL, '"deny"', 'Bloquea por completo', 'Impide usar comandos destructivos aunque el agente los pida', 'candado'),
]
b = []
for y, on, col, lvl, title, desc, ic in rows:
    tint = OKT if col == OK else (DT if col == DOSC else MALT)
    b.append(R(24, y - 62, 1132, 128, tint, col, 3, 18))
    if col == DOSC:
        b.append(R(54, y - 24, 102, 52, DOSC, None, 0, 26) + C(54 + 102 - 26, y + 2, 21, '#fff'))
    else:
        b.append(TOGGLE(54, y - 24, on, 102, 52))
    b.append(IC(ic, 210, y + 2, 56, col))
    b.append(T(264, y - 4, lvl, 30, True, col, mono=True))
    b.append(T(430, y - 4, title, 26, True, INK))
    b.append(T(264, y + 36, desc, 20, False, INK))
    if col == OK:
        b.append(CH(1096, y + 2, 30, True))
    elif col == MAL:
        b.append(CH(1096, y + 2, 30, False))
    else:
        b.append(C(1096, y + 2, 30, DOSC))
        b.append(T(1096, y + 12, '?', 30, True, '#fff', 'middle'))
slide(
    19,
    'Permisos',
    'Tres efectos de permiso en opencode: allow, ask y deny',
    'OpenCode permite ajustar herramienta por herramienta si corre sola, pide permiso o se bloquea.',
    'Basado en: OpenCode Permissions docs [cite:5] · Dibujo propio',
    SVG(*b),
    """Pasemos ahora del marco conceptual a la configuración práctica directamente dentro de opencode. La documentación oficial de opencode define tres efectos de permiso [cite:5] para gobernar qué puede ejecutar un agente sobre cada herramienta conectada, representados aquí mediante estos tres interruptores horizontales. Arriba en verde está allow, que deja correr la función en automático sin interrumpir el trabajo del operador; resulta muy ágil y seguro para consultas de solo lectura como pedidos atrasados. En el centro en dorado aparece ask, que detiene la llamada justo antes de enviarla al servidor y pregunta al humano si autoriza continuar; este efecto es obligatorio para caribemart cancelar pedido. Abajo en rojo está deny, que bloquea la herramienta por completo aunque el modelo insista en invocarla dentro de su razonamiento. Combinar estos tres niveles por herramienta equilibra eficiencia operativa y protección efectiva de datos.""",
)

# 20 · Configuración exacta en opencode.json (CODE líneas simples sin solapes + CALL)
cd, w, h = CODE(
    26,
    74,
    [
        [('{', 'w')],
        [('  "$schema": "https://opencode.ai/config.json",', 's')],
        [('  "mcp": { "servers": { "caribemart": { ... } } },', 'w')],
        [('  "permission": {', 'k')],
        [('    "caribemart_cancelar_pedido": "ask"', 'k')],
        [('  }', 'k')],
        [('}', 'w')],
    ],
    size=21,
    padx=24,
    pady=24,
    w=810,
    title=None,
)
b = [
    chip(26, 20, 'opencode.json · raíz de mcp-caribemart', size=18, fill=INK, stroke=None, color='#fff', h=40, padx=18, mono=True),
    cd,
]
X = 26 + w + 12
b.append(CALL(X - 10, linectr(74, 21, 2, 24, title=False), X + 38, 175, 1, DOSC))
b.append(T(X + 68, 170, 'Servidor MCP', 22, True, DOSC))
b.append(T(X + 68, 198, 'nombre: caribemart', 18, False, INK))
b.append(CALL(X - 10, linectr(74, 21, 4, 24, title=False), X + 38, 290, 2, VINO))
b.append(T(X + 68, 284, 'Freno humano', 22, True, VINO))
b.append(T(X + 68, 312, 'prefijo + herramienta', 18, False, INK))
b.append(R(26, 368, 1128, 110, DT, DOSC, 3, 16))
b.append(IC('alerta', 84, 423, 52, DOSC))
b.append(T(136, 408, 'Usa exactamente la clave "permission" indicada en la guía del Proyecto Corte 3.', 21, True, INK))
b.append(T(136, 444, 'En opencode 2 del curso funciona junto a "mcp"; no cambies los nombres.', 19, False, GRIS))
slide(
    20,
    'Configuración',
    'Cómo configurar permission ask en opencode.json',
    'Se agrega la sección "permission" junto a "mcp" apuntando al nombre exacto de la herramienta.',
    'Basado en: Proyecto Corte 3 y OpenCode docs [cite:5,6] · Dibujo propio',
    SVG(*b),
    """Aquí tienen la configuración exacta que deben guardar dentro del archivo opencode punto json, ubicado en la raíz de su carpeta de trabajo mcp caribemart. Fíjense en las dos llamadas numeradas a la derecha de la ventana de código oscura. En la llamada número uno conservan intacto el bloque mcp con servers y el nombre caribemart que ya venían usando desde el laboratorio siete. Justo debajo, en la llamada número dos, añaden la clave permission con la entrada caribemart guion bajo cancelar guion bajo pedido igual al valor ask. Presten especial atención al recuadro dorado inferior: aunque las versiones más recientes de la documentación oficial muestran reglas en listas bajo otra clave, en el entorno opencode dos instalado para el curso funciona exactamente esta sintaxis con permission [cite:5] junto a mcp [cite:6]. Mantengan exactamente estos mismos nombres para cumplir toda la rúbrica.""",
)

# 21 · Por qué el prefijo del servidor importa (ensamblaje)
b = [
    R(40, 48, 340, 146, VT, VINO, 3, 16),
    T(210, 96, 'NOMBRE EN opencode.json', 19, True, VINO, 'middle'),
    T(210, 144, 'caribemart', 32, True, INK, 'middle', mono=True),
    T(420, 134, '+', 42, True, DOSC, 'middle'),
    R(460, 48, 120, 146, DT, DOSC, 3, 16),
    T(520, 96, 'SEPARADOR', 18, True, DOSC, 'middle'),
    T(520, 148, '_', 38, True, INK, 'middle', mono=True),
    T(620, 134, '+', 42, True, DOSC, 'middle'),
    R(660, 48, 480, 146, OKT, OK, 3, 16),
    T(900, 96, 'NOMBRE EN server.js', 19, True, OK, 'middle'),
    T(900, 144, 'cancelar_pedido', 30, True, INK, 'middle', mono=True),
    A(590, 206, 590, 266, VINO, 5),
    R(140, 274, 900, 86, '#1E1E1E', None, 0, 14),
    T(590, 326, 'caribemart_cancelar_pedido', 30, True, '#E8C56A', 'middle', mono=True),
    R(40, 390, 520, 92, MALT, MAL, 2.5, 14),
    CH(88, 436, 22, False),
    T(128, 428, 'Error común: poner solo "cancelar_pedido"', 19, True, MAL),
    T(128, 458, 'No coincide y se ejecuta sin pedir permiso', 18, False, INK),
    R(620, 390, 520, 92, OKT, OK, 2.5, 14),
    CH(668, 436, 22, True),
    T(708, 428, 'Verificación rápida en opencode', 19, True, OK),
    T(708, 458, 'El prefijo visible en el chat debe ser idéntico', 18, False, INK),
]
slide(
    21,
    'Detalle técnico',
    'Por qué importa el prefijo caribemart_ en el permiso',
    'OpenCode registra las herramientas combinando el nombre del servidor y el de la función.',
    'Basado en: OpenCode MCP docs [cite:6] y Proyecto Corte 3 · Dibujo propio',
    SVG(*b),
    """Este detalle técnico en apariencia pequeño evita uno de los errores más comunes cuando los estudiantes preparan su entrega final. Observen en las tres cajas superiores cómo construye internamente opencode el identificador único de cualquier herramienta expuesta por un servidor MCP [cite:6]. Toma primero la clave del servidor registrada bajo servers en opencode punto json, que en nuestro proyecto debe llamarse caribemart. Añade un guion bajo como separador obligatorio y lo une sin espacios con el nombre declarado dentro de server punto js, que es cancelar guion bajo pedido. El identificador compuesto resultante aparece en la barra oscura central: caribemart guion bajo cancelar guion bajo pedido. Miren las dos tarjetas de abajo. Si escriben solamente cancelar pedido sin prefijo, la regla no coincide y la herramienta corre sin preguntar. Verifiquen siempre el nombre completo en consola.""",
)

# 22 · Cómo se ve la pausa en la terminal (modal/terminal + opciones)
b = [
    R(40, 24, 680, 452, '#1E1E1E', INK, 3, 18),
    R(40, 24, 680, 44, '#2d2d2d', None, 0, 10),
    T(70, 53, 'opencode · esperando confirmación humana', 18, True, '#E8C56A'),
    T(70, 114, 'Propuesta de herramienta:', 19, False, '#bdbdbd'),
    T(70, 148, 'caribemart_cancelar_pedido', 22, True, '#8EC3E6', mono=True),
    T(70, 196, 'Argumentos:', 19, False, '#bdbdbd'),
    T(70, 228, '{ "id": 1002,', 20, False, '#9BD1A8', mono=True),
    T(70, 258, '  "motivo": "ATRASO: > 5 días" }', 20, False, '#9BD1A8', mono=True),
    R(70, 326, 260, 58, OK, None, 0, 12),
    T(200, 362, '1. Aprobar (Allow)', 21, True, '#fff', 'middle'),
    R(360, 326, 260, 58, MAL, None, 0, 12),
    T(490, 362, '2. Rechazar (Deny)', 21, True, '#fff', 'middle'),
    T(70, 442, 'El proceso queda en pausa hasta tu respuesta.', 18, False, '#E8C56A'),
    R(754, 24, 386, 210, VT, VINO, 3, 16),
    IC('ojo', 812, 82, 48, VINO),
    T(854, 90, 'QUÉ REVISAR AQUÍ', 22, True, VINO),
    T(784, 136, '• Que el id corresponda a un', 19, False, INK),
    T(784, 166, '  pedido realmente atrasado.', 19, False, INK),
    T(784, 202, '• Que el motivo sea válido.', 19, False, INK),
    R(754, 266, 386, 210, DT, DOSC, 3, 16),
    IC('documento', 812, 324, 48, DOSC),
    T(854, 332, 'PARA TU PDF', 22, True, DOSC),
    T(784, 378, '• Toma captura de esta pausa', 19, False, INK),
    T(784, 408, '  antes de aprobar o rechazar.', 19, False, INK),
    T(784, 444, '• Prueba ambos caminos.', 19, True, DOSC),
]
slide(
    22,
    'Ejecución',
    'Cómo se ve la pausa humana en opencode',
    'Antes de ejecutar cancelar_pedido, la interfaz muestra los argumentos y espera tu decisión.',
    'Basado en: OpenCode Permissions docs [cite:5] y Proyecto Corte 3 · Dibujo propio',
    SVG(*b),
    """Cuando la regla de permisos queda bien escrita y lanzan la tarea de varios pasos, opencode detiene el flujo mostrando una pantalla de confirmación humana [cite:5] muy similar a la de la izquierda. Fíjense en los tres datos críticos que deben inspeccionar antes de tomar una decisión. Primero aparece el nombre exacto de la herramienta propuesta: caribemart guion bajo cancelar guion bajo pedido. Debajo ven los argumentos concretos en formato JSON, en este ejemplo el identificador mil dos y el texto del motivo indicando más de cinco días de atraso. Justo abajo figuran los botones para aprobar o rechazar la ejecución. Mientras ustedes no respondan, el servidor Node no recibe ninguna llamada y el archivo permanece intacto. A la derecha recordamos dos acciones clave para el entregable: auditar si el pedido aplica y capturar esta pausa antes y después de decidir.""",
)

# 23 · Aprobar vs rechazar paso a paso (bifurcación)
b = [
    NODE(130, 250, 'usuario', 'DECISIÓN', 'del operador', DOSC, DT, r=66, isz=76, lsz=22, ssz=19),
    AP([(202, 250), (310, 250), (350, 120), (420, 120)], OK, 5),
    T(270, 170, 'APRUEBA', 20, True, OK, 'middle'),
    R(426, 46, 340, 148, OKT, OK, 3, 16),
    IC('servidor', 476, 120, 48, OK),
    T(518, 98, 'server.js ejecuta', 22, True, OK),
    T(518, 134, 'Valida estado con zod', 19, False, INK),
    T(518, 166, 'Actualiza pedidos.json', 19, False, INK),
    A(772, 120, 860, 120, OK, 5),
    R(866, 46, 290, 148, '#fff', OK, 3, 16),
    CH(914, 120, 24, True),
    T(952, 108, 'Cancelado', 22, True, OK),
    T(952, 142, 'Redacta aviso real', 18, False, INK),
    AP([(202, 250), (310, 250), (350, 380), (420, 380)], MAL, 5),
    T(270, 344, 'RECHAZA', 20, True, MAL, 'middle'),
    R(426, 306, 340, 148, MALT, MAL, 3, 16),
    IC('candado', 476, 380, 48, MAL),
    T(518, 358, 'opencode bloquea', 22, True, MAL),
    T(518, 394, 'No llama a server.js', 19, False, INK),
    T(518, 426, 'pedidos.json intacto', 19, True, MAL),
    A(772, 380, 860, 380, MAL, 5),
    R(866, 306, 290, 148, '#fff', MAL, 3, 16),
    CH(914, 380, 24, False),
    T(952, 368, 'Sin cambios', 22, True, MAL),
    T(952, 402, 'Agente sigue o replantea', 18, False, INK),
]
slide(
    23,
    'Flujo',
    'Qué ocurre al aprobar o rechazar una llamada',
    'Ambas respuestas del humano devuelven control limpio al flujo sin romper el bucle del agente.',
    'Basado en: OpenCode Permissions docs [cite:5] y Zod [cite:9] · Dibujo propio',
    SVG(*b),
    """Analicen en este diagrama de bifurcación cómo responde exactamente la arquitectura según la decisión tomada por el operador humano. Si siguen la rama superior en verde cuando ustedes aprueban la llamada propuesta en consola, opencode deja pasar la solicitud hacia el servidor Node server punto js. Allí el manejador ejecuta las validaciones de esquema con zod [cite:9] y las reglas de estado [cite:5], actualiza el registro correspondiente dentro de pedidos punto json y devuelve confirmación al modelo para que redacte el aviso definitivo dirigido al cliente. Ahora sigan la rama inferior en rojo cuando ustedes rechazan la propuesta, por ejemplo porque saben que el despacho hacia Montería sale mañana temprano. En ese escenario opencode bloquea el envío y ni siquiera invoca a server punto js. El archivo queda intacto, el agente recibe la negativa limpia y reformula su respuesta sin colgarse.""",
)

# 24 · Bitácora de decisiones humanas (tabla gráfica SVG de auditoría)
b = [
    R(24, 24, 1132, 62, VINO, None, 0, 14),
    T(56, 62, 'PEDIDO', 20, True, '#fff'),
    T(200, 62, 'PROPUESTA DEL AGENTE', 20, True, '#fff'),
    T(560, 62, 'DECISIÓN', 20, True, '#fff'),
    T(750, 62, 'RAZÓN DOCUMENTADA POR EL OPERADOR', 20, True, '#fff'),
]
rows_b = [
    (102, '1002 · Ana', 'Cancelar (Cartagena, 10 días)', 'APROBADO', 'Cumple > 5 días pendiente; sin guía', OK, OKT),
    (208, '1004 · María', 'Cancelar (Montería, 7 días)', 'RECHAZADO', 'Despacho sale mañana; avisar demora', MAL, MALT),
    (314, '1007 · Vale', 'Cancelar (Santa Marta, 11 días)', 'APROBADO', 'Sin inventario; autoriza supervisor', OK, OKT),
]
for y, ped, prop, dec, raz, col, tint in rows_b:
    b.append(R(24, y, 1132, 88, tint, col, 2.5, 14))
    b.append(T(56, y + 50, ped, 19, True, INK))
    b.append(T(200, y + 50, prop, 19, False, INK))
    b.append(R(548, y + 20, 168, 48, col, None, 0, 10))
    b.append(T(632, y + 51, dec, 18, True, '#fff', 'middle'))
    b.append(T(750, y + 50, raz, 19, False, INK))
b.append(R(24, 420, 1132, 60, DT, DOSC, 2.5, 14))
b.append(IC('registro', 64, 450, 38, DOSC))
b.append(T(102, 458, 'Criterio 3 de la rúbrica: la bitácora prueba que ejerciste criterio humano y no aprobaste todo a ciegas.', 20, True, INK))
slide(
    24,
    'Trazabilidad',
    'Bitácora de decisiones: qué aprobaste y qué rechazaste',
    'Registrar el motivo de cada aprobación y rechazo convierte la pausa en evidencia auditable.',
    'Basado en: Proyecto Corte 3 y NIST AI RMF [cite:10] · Dibujo propio',
    SVG(*b),
    """Fíjense en esta tabla de auditoría operativa pensada para acompañar la evidencia de su entrega. La guía del Proyecto Corte tres exige explícitamente construir una bitácora con las propuestas que aprobaron y con las propuestas que rechazaron durante la ejecución multipaso, explicando la razón de cada decisión. Miren las tres filas de ejemplo ambientadas en tiendas del Caribe colombiano. El pedido mil dos de Ana en Cartagena llevaba diez días pendiente sin despacho asignado, de modo que el operador aprueba su cancelación. En cambio, en la fila central en rojo, aunque el agente sugirió cancelar el pedido mil cuatro en Montería, el humano rechaza esa cancelación porque conoce que el camión sale mañana y prefiere enviar aviso de demora. En la tercera fila aprueba el mil siete por falta de inventario. Documentar el porqué respalda la trazabilidad de riesgo [cite:10] y demuestra discernimiento humano.""",
)

# 25 · Caso práctico: la meta completa en CaribeMart (secuencia)
b = [
    R(40, 22, 1100, 66, GT, INK, 2, 14),
    T(590, 62, 'FLUJO COMPLETO: DE LA CONSULTA AL MENSAJE AL CLIENTE', 22, True, INK, 'middle'),
]
cards = [
    (40, 116, '1', 'pedidos_atrasados(5)', 'Devuelve 1002, 1004 y 1007', 'en estado pendiente', OK, OKT),
    (322, 116, '2', 'Lectura de AGENTS.md', 'Aplica umbral 5 días', 'y regla anti-inyección', DOSC, DT),
    (604, 116, '3', 'Pausa permission ask', 'Propone 1002 y 1007;', 'humano aprueba 1002', VINO, VT),
    (886, 116, '4', 'Mensajes al cliente', '1002: aviso cancelado', '1004: aviso en camino', INK, GT),
]
for x, y, num, t1, t2, t3, col, tint in cards:
    b.append(R(x, y, 254, 240, tint, col, 3, 18))
    b.append(BADGE(x + 127, y + 42, num, col, 22, 22))
    b.append(T(x + 127, y + 106, t1, 18, True, col, 'middle', mono='_' in t1 or '.' in t1))
    b.append(T(x + 127, y + 158, t2, 18, False, INK, 'middle'))
    b.append(T(x + 127, y + 190, t3, 18, False, INK, 'middle'))
for i in range(3):
    x1 = cards[i][0] + 254
    x2 = cards[i + 1][0]
    b.append(A(x1 + 2, 236, x2 - 2, 236, VINO, 4))
b.append(R(40, 384, 1100, 92, '#fff', VINO, 2.5, 16))
b.append(IC('check', 92, 430, 48, OK))
b.append(T(136, 422, 'Resultado observable: herramienta de lectura automática, escritura pausada,', 20, True, INK))
b.append(T(136, 454, 'al menos un rechazo documentado y borradores adaptados a cada comprador.', 20, False, GRIS))
slide(
    25,
    'CaribeMart',
    'Recorrido completo de la tarea multi-paso en CaribeMart',
    'El operador lanza un único pedido en opencode y supervisa el punto exacto de riesgo.',
    'Basado en: Proyecto de Aula Corte 3 · Dibujo propio',
    SVG(*b),
    """Así luce la tarea multipaso completa cuando la ejecutan de principio a fin sobre el servidor MCP de CaribeMart. Sigan las cuatro tarjetas numeradas de izquierda a derecha para ver cómo encajan todas las piezas del corte. En la tarjeta uno en verde, el modelo invoca automáticamente pedidos atrasados con cinco días y recupera los registros mil dos, mil cuatro y mil siete en estado pendiente. En la tarjeta dos en dorado, consulta las políticas de negocio definidas en AGENTS punto md para interpretar cuáles ameritan cancelación y con qué tono dirigirse al comprador. En la tarjeta tres en vino aparece la compuerta humana de permission ask [cite:5]: el asistente propone cancelar, el humano aprueba mil dos y rechaza mil cuatro. En la tarjeta cuatro redacta avisos diferenciados: confirmación de cancelación para Ana y notificación cordial de envío próximo para María.""",
)

# 26 · Mini-reto 1: pausa y decide el permiso
b = [
    R(20, 20, 1140, 460, DT, DOSC, 4, 22, dash='14 9'),
    PAUSE(150, 160, 74),
    T(150, 286, ['PAUSA', 'Y DECIDE'], 26, True, DOSC, 'middle'),
    T(290, 96, 'Mini-reto 1: asigna permisos en CaribeMart', 32, True, VINO),
    T(290, 138, '¿Qué valor pondrías en opencode.json (allow, ask o deny)?', 22, False, INK),
]
tools_r = [
    (184, 'A. caribemart_pedidos_atrasados', 'consulta lista pendiente sin cambiar nada'),
    (272, 'B. caribemart_cancelar_pedido', 'modifica el estado de un pedido real'),
    (360, 'C. borrar_todos_los_pedidos', 'herramienta hipotética destructiva masiva'),
]
for y, nm, desc in tools_r:
    b.append(R(290, y, 830, 74, '#fff', DOSC, 2.5, 14))
    b.append(T(316, y + 34, nm, 21, True, VINO, mono=True))
    b.append(T(316, y + 62, desc, 18, False, GRIS))
slide(
    26,
    'Mini-reto',
    'Pausa el video: ¿allow, ask o deny para cada herramienta?',
    'Clasifica estas tres operaciones según su impacto y reversibilidad antes de ver la respuesta.',
    'Basado en: OpenCode Permissions docs [cite:5] · Dibujo propio',
    SVG(*b),
    """Llegamos al primer mini reto de esta clase para poner a prueba su criterio de seguridad antes de avanzar. Pausen el video durante treinta segundos y decidan qué efecto de permiso asignarían dentro de opencode punto json a cada una de las tres herramientas mostradas a la derecha. La opción A es caribemart guion bajo pedidos guion bajo atrasados, una función de solo lectura que consulta el archivo JSON y devuelve pedidos pendientes sin modificar ningún registro. La opción B es caribemart guion bajo cancelar guion bajo pedido, que escribe un cambio definitivo de estado y guarda el motivo en el pedido seleccionado. La opción C es una herramienta hipotética llamada borrar todos los pedidos, capaz de eliminar de golpe toda la base comercial. Evalúen impacto sobre el negocio y reversibilidad para clasificar cada una entre allow, ask y deny [cite:5].""",
)

# 27 · Resolución del Mini-reto 1 (3 filas con respuesta)
sols = [
    (44, 'A. caribemart_pedidos_atrasados', '"allow"', 'Solo lectura sin efectos secundarios; agiliza el bucle.', OK, OKT, True),
    (194, 'B. caribemart_cancelar_pedido', '"ask"', 'Escribe estado irreversible; exige confirmación y bitácora.', DOSC, DT, True),
    (344, 'C. borrar_todos_los_pedidos', '"deny"', 'Impacto catastrófico innecesario; mejor ni exponerla en MCP.', MAL, MALT, False),
]
b = []
for y, nm, perm, why, col, tint, okflag in sols:
    b.append(R(24, y, 1132, 118, tint, col, 3, 18))
    b.append(CH(78, y + 59, 28, okflag))
    b.append(T(130, y + 48, nm, 22, True, INK, mono=True))
    b.append(T(130, y + 86, why, 20, False, INK))
    b.append(R(940, y + 26, 184, 66, col, None, 0, 12))
    b.append(T(1032, y + 68, perm, 26, True, '#fff', 'middle', mono=True))
slide(
    27,
    'Solución',
    'Resolución del Mini-reto 1: principio de mínimo privilegio',
    'Lectura en automático, escritura sensible con pausa humana y borrado masivo prohibido.',
    'Basado en: OpenCode Permissions [cite:5] y OWASP LLM06 [cite:1] · Dibujo propio',
    SVG(*b),
    """Comparen ahora su respuesta con la solución recomendada en pantalla bajo el principio de mínimo privilegio. Para la herramienta A, caribemart pedidos atrasados, el permiso adecuado es allow en verde [cite:5], porque únicamente consulta datos sin alterar el archivo comercial y pedir confirmación manual en cada lectura terminaría fatigando al operador hasta hacerlo aprobar todo por pura costumbre. Para la herramienta B, caribemart cancelar pedido, el valor obligatorio dentro del proyecto del curso es ask en dorado, pues modifica un pedido comercial real y requiere discernimiento humano más registro en bitácora. Para la herramienta C, borrar todos los pedidos, la regla inmediata es deny en rojo, y bajo las recomendaciones de OWASP LLM cero seis [cite:1] ni siquiera debería existir programada dentro del servidor MCP. Concedan únicamente el mínimo privilegio necesario para cumplir la operación de forma segura.""",
)

# 28 · Síntesis de la Parte 2 (4 pilares verticales)
b = [
    R(30, 32, 1120, 48, DOR, None, 0, 10),
    T(590, 64, 'CONTROL HUMANO EN AGENTES DE CARIBEMART', 22, True, '#fff', 'middle'),
]
cols_s2 = [
    ('usuario', 'HITL|ACTIVO', VINO),
    ('ojo', 'MARCO 4D|COMPLETO', DOSC),
    ('candado', 'PERMISSION|ASK', OK),
    ('registro', 'BITÁCORA|AUDITABLE', INK),
]
for i, (ic, t, col) in enumerate(cols_s2):
    cx = 170 + i * 280
    b.append(R(cx - 72, 80, 144, 286, col, None, 0, 8))
    b.append(R(cx - 92, 366, 184, 26, col, None, 0, 6))
    b.append(C(cx, 156, 50, '#fff', col, 0))
    b.append(IC(ic, cx, 156, 66, col))
    for j in range(3):
        b.append('<line x1="%g" y1="224" x2="%g" y2="354" stroke="#fff" stroke-opacity=".35" stroke-width="4"/>' % (cx - 34 + j * 34, cx - 34 + j * 34))
    b.append(T(cx, 434, t.split('|'), 24, True, col, 'middle'))
slide(
    28,
    'Síntesis',
    'La Parte 2 en cuatro ideas maestras',
    'El control humano se diseña en opencode y se respalda con criterio y bitácora.',
    'Basado en: Anthropic 4D [cite:8] y OpenCode docs [cite:5] · Dibujo propio',
    SVG(*b),
    """Cerramos la segunda parte fijando cuatro pilares fundamentales sobre la verificación humana en agentes modernos. Primero, el principio human-in-the-loop conserva la autoridad final sobre cualquier operación de escritura sensible en manos de la persona operadora mientras delega el análisis veloz al modelo. Segundo, el marco cuatro D ordena nuestra práctica profesional en cuatro competencias claras [cite:8]: delegar con frontera definida, describir reglas precisas en AGENTS punto md, discernir críticamente las propuestas y actuar con diligencia documentada. Tercero, dentro de opencode punto json configuramos exactamente caribemart guion bajo cancelar guion bajo pedido en modo ask [cite:5] junto al bloque mcp. Cuarto, cada aprobación o rechazo se registra en una bitácora con su justificación operativa. Pero qué ocurre si un atacante esconde órdenes maliciosas dentro de los mismos datos que lee el agente? Ese vector lo estudiaremos en la tercera parte.""",
)
