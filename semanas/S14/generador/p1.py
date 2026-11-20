from comun import *

# 1 · Mapa de la sesión (foto lateral + 4 estaciones)
b = [
    FOTO('programador', 0, 14, 390, 472, 16, 'xMidYMid'),
    GRAD_SCRIM(0, 310, 390, 176, .85, 16),
    T(24, 418, 'HOY EN SEMANA 14', 18, True, DOR),
    T(24, 452, ['Del razonamiento al', 'conocimiento de negocio'], 22, True, '#fff'),
]
est = [
    (76, '1', 'Razonamiento y código', 'Test-time compute, diffs y SWE-bench', VINO, VT, 'ia'),
    (186, '2', 'Contexto y AGENTS.md', 'Ventana de trabajo y memoria estable', DOSC, DT, 'documento'),
    (296, '3', 'RAG simple', 'Chunking, búsqueda y citas con fuente', OK, OKT, 'bd'),
    (406, '4', 'CaribeMart y práctica', 'opencode, Nequi, ley y práctica del proyecto', INK, GT, 'servidor'),
]
b.append('<line x1="470" y1="90" x2="470" y2="420" stroke="%s" stroke-width="5" stroke-dasharray="6 8"/>' % DOR)
for y, num, tit, sub, col, tint, ic in est:
    b.append(R(525, y - 42, 635, 86, tint, col, 2.5, 16))
    b.append(BADGE(470, y, num, col, 24, 22))
    b.append(IC(ic, 570, y, 42, col))
    b.append(T(612, y - 6, tit, 23, True, col))
    b.append(T(612, y + 24, sub, 18, False, INK))
add_slide(1, 1, 'Mapa', 'Ruta de la semana 14 en cuatro bloques',
          'De cómo piensa un modelo a cómo consulta los documentos reales de CaribeMart.',
          'Elaboración propia · ' + credito('programador'),
          SVG(*b),
          'Bienvenidos a la semana catorce de Integración de Soluciones para Plataformas Cloud. A la izquierda tenemos el punto de partida de hoy: pasar de modelos que solo llaman funciones a asistentes capaces de razonar, entender un proyecto y consultar documentos propios. Sigan los cuatro bloques a la derecha. En el bloque uno revisaremos qué ocurre dentro de un modelo razonador y cómo se integra en programación asistida revisando cada parche. En el bloque dos aprenderemos cómo funciona la ventana de contexto y cómo darle memoria estable al proyecto CaribeMart con el archivo AGENTS.md en opencode. En el bloque tres construiremos paso a paso un esquema de generación aumentada por recuperación, conocida como RAG simple. Por último, en el bloque cuatro integraremos todo con permisos seguros, analizaremos el caso colombiano real de Nequi y revisaremos el enfoque del laboratorio B.',
          fotos=['programador'])

# 2 · Dos formas de responder: estándar vs razonador (dos carriles horizontales)
b = [
    R(20, 26, 1140, 200, GT, INK, 2.5, 18),
    R(20, 260, 1140, 214, VT, VINO, 2.5, 18),
    T(50, 68, 'MODELO ESTÁNDAR (respuesta directa)', 22, True, INK),
    T(50, 302, 'MODELO RAZONADOR (piensa antes de responder)', 22, True, VINO),
]
b.append(CHIP(50, 110, 'Prompt complejo', 20, '#fff', INK, h=56, padx=20)[0])
b.append(A(268, 138, 375, 138, INK, 4))
b.append(NODE(440, 138, 'ia', 'LLM', None, INK, '#fff', r=44, isz=56, lsz=18))
b.append(A(492, 138, 635, 138, INK, 4))
b.append(CHIP(645, 110, 'Emite respuesta token a token de inmediato', 20, '#fff', INK, h=56, padx=22)[0])
b.append(CHIP(50, 355, 'Prompt complejo', 20, '#fff', VINO, h=56, padx=20)[0])
b.append(A(268, 383, 350, 383, VINO, 4))
b.append(R(360, 326, 360, 114, DT, DOSC, 2.5, 16))
b.append(IC('engranaje', 404, 383, 44, DOSC))
b.append(T(440, 372, 'Tokens de pensamiento', 21, True, DOSC))
b.append(T(440, 404, 'divide, verifica y corrige', 18, False, INK))
b.append(A(728, 383, 815, 383, VINO, 4))
b.append(CHIP(825, 355, 'Respuesta verificada', 20, OKT, OK, h=56, padx=22)[0])
add_slide(2, 1, 'Fundamentos', 'Dos formas de responder: directa o con razonamiento',
          'Un modelo razonador dedica tokens internos a pensar antes de escribir la salida.',
          'Basado en: OpenAI o1 [cite:1] y DeepSeek-R1 [cite:2] · Dibujo propio',
          SVG(*b),
          'Fíjense en las dos bandas horizontales del diagrama para distinguir dos familias de modelos. Arriba tienen un modelo grande de lenguaje, o LLM, de tipo estándar. Cuando recibe una pregunta difícil, empieza a predecir palabra por palabra la respuesta final de inmediato, sin pausa previa. Si comete un error lógico en la segunda línea, suele seguir de largo construyendo sobre esa equivocación. Abajo ven el enfoque de un modelo razonador, como o1 [cite:1] o DeepSeek-R1 [cite:2]. Antes de entregar texto al usuario, el modelo abre una fase interna de tokens de pensamiento donde descompone el problema en pasos, prueba hipótesis y revisa si alguna condición falla. Eso toma algunos segundos adicionales de cómputo en tiempo de inferencia, pero transforma problemas complejos de varios pasos lógicos en soluciones verificables. No es magia en absoluto, es darse tiempo de cálculo antes de hablar.',
          sig_extra=['LLM = modelo grande de lenguaje'])

# 3 · Cómputo en tiempo de prueba (test-time compute) (curva ascendente)
b = [
    R(30, 30, 680, 440, '#fff', INK, 2, 18),
    A(110, 410, 670, 410, INK, 3),
    A(110, 410, 110, 66, INK, 3),
    T(390, 452, 'Más cómputo en inferencia (test-time compute)', 19, True, INK, 'middle'),
    T(128, 86, 'Precisión en tareas lógicas', 19, True, VINO),
    P('M140,365 Q300,320 420,210 T635,105', stroke=VINO, sw=6),
    C(190, 346, 12, GRIS), C(360, 260, 12, DOSC), C(580, 126, 14, OK),
    T(196, 298, 'Poco pensamiento', 18, True, GRIS, 'middle'),
    T(310, 232, 'Más verificación', 18, True, DOSC, 'middle'),
    T(575, 174, 'Consenso y revisión', 18, True, OK, 'middle'),
    CARD(745, 36, 410, 195, 'ANTES: PREENTRENAMIENTO',
         ['Escalar datos y parámetros', 'antes de publicar el modelo.', 'Costo fijo por pregunta.'], INK, GT, 20, 18, 'servidor'),
    CARD(745, 256, 410, 214, 'AHORA: TEST-TIME COMPUTE',
         ['Escalar el tiempo y tokens', 'que piensa en cada petición.', 'Aprendido por refuerzo.'], VINO, VT, 20, 18, 'ia'),
]
add_slide(3, 1, 'Paradigma', 'Cómputo en tiempo de prueba para resolver problemas',
          'Invertir más cómputo al inferir eleva la precisión sin reentrenar todo el modelo.',
          'Basado en: OpenAI o1 [cite:1] y DeepSeek-R1 [cite:2] · Dibujo propio',
          SVG(*b),
          'Durante años, mejorar un modelo significaba casi exclusivamente entrenarlo con más textos y más tarjetas gráficas antes de lanzarlo al público. Con el paradigma de cómputo en tiempo de prueba, conocido en inglés como test-time compute, aparece una segunda palanca de calidad muy poderosa. Miren la curva vino a la izquierda. Cuando al modelo se le asignan más tokens para razonar justo en el momento de la consulta, su precisión en tareas de lógica, matemáticas y depuración sube de manera sostenida. Como muestran las tarjetas de la derecha, este hábito no se programa a mano regla por regla: tanto OpenAI con o1 [cite:1] como DeepSeek-R1 [cite:2] demostraron que el aprendizaje por refuerzo, o RL, enseña al modelo a pensar de forma productiva. El precio práctico es mayor latencia y consumo de tokens, por eso debemos elegir cuándo activarlo.')

# 4 · Cómo funcionan los tokens de pensamiento (ciclo interno + filtro)
b = [
    NODE(110, 250, 'documento', 'PREGUNTA', 'lógica o código', INK, GT, r=58, isz=70, lsz=20, ssz=17),
    A(174, 250, 245, 250, VINO, 4),
    R(255, 50, 560, 400, DT, DOSC, 3, 20, dash='10 6'),
    T(535, 90, 'CADENA INTERNA (<think>)', 22, True, DOSC, 'middle'),
]
pasos = [
    (128, '1', 'Descompone el problema en subpasos', VINO),
    (208, '2', 'Detecta contradicción o caso borde', MAL),
    (288, '3', 'Retrocede (backtracking) y replantea', DOSC),
    (368, '4', 'Verifica la solución propuesta', OK),
]
for y, num, txt, col in pasos:
    b.append(R(285, y, 500, 58, '#fff', col, 2, 12))
    b.append(BADGE(318, y + 29, num, col, 18, 18))
    b.append(T(350, y + 36, txt, 19, True, INK))
b.append(A(822, 250, 905, 250, OK, 4))
b.append(R(915, 130, 240, 240, OKT, OK, 3, 18))
b.append(IC('check', 1035, 196, 62, OK))
b.append(T(1035, 266, 'RESPUESTA', 22, True, OK, 'middle'))
b.append(T(1035, 302, ['limpia y', 'coherente'], 20, False, INK, 'middle'))
b.append(T(1035, 354, 'cobra todos los tokens', 16, True, GRIS, 'middle'))
add_slide(4, 1, 'Mecanismo', 'Qué ocurre dentro de los tokens de pensamiento',
          'El modelo ensaya, detecta fallos y retrocede antes de redactar la respuesta final.',
          'Basado en: OpenAI o1 [cite:1] y DeepSeek-R1 [cite:2] · Dibujo propio',
          SVG(*b),
          'Detengámonos a mirar qué pasa por dentro cuando un modelo razonador recibe una pregunta compleja desde la izquierda. En el cuadro punteado dorado aparece la cadena de pensamiento interna, delimitada en modelos abiertos como DeepSeek-R1 mediante bloques think [cite:2]. Primero, el modelo parte el problema grande en piezas manejables. Segundo, si una suposición no cuadra con los datos observados, el propio modelo detecta la contradicción en lugar de seguir inventando. Tercero, hace backtracking o retroceso para explorar otra ruta diferente. Cuarto, comprueba el resultado final antes de pasar al bloque verde de la derecha. Un detalle clave de ingeniería y presupuesto en la nube [cite:1]: aunque parte de ese razonamiento quede resumido u oculto en la pantalla del usuario, todos esos tokens de pensamiento consumen cómputo real y cuentan tanto en la facturación como en el tiempo total.')

# 5 · Impacto medido en AIME 2024 (gráfico de barras verificadas)
b = [
    R(30, 30, 740, 440, '#fff', INK, 2, 18),
    T(400, 74, 'Examen matemático AIME 2024 (% resuelto)', 22, True, INK, 'middle'),
    '<line x1="90" y1="390" x2="730" y2="390" stroke="%s" stroke-width="3"/>' % INK,
]
bars = [
    (170, 12, '12 %', 'GPT-4o', 'estándar', GRIS),
    (360, 74, '74 %', 'o1 (1 intento)', 'razonador', VINO),
    (550, 83, '83 %', 'o1 (consenso 64)', 'más cómputo', DOSC),
]
for cx, pct, lbl, mod, sub, col in bars:
    bh = pct * 2.5
    by = 390 - bh
    b.append(R(cx - 55, by, 110, bh, col, None, 0, 10))
    b.append(T(cx, by - 12, lbl, 24, True, col, 'middle'))
    b.append(T(cx, 422, mod, 19, True, INK, 'middle'))
    b.append(T(cx, 448, sub, 16, False, GRIS, 'middle'))
b.append(CARD(800, 40, 350, 200, 'DATO CLAVE VERIFICADO',
              ['GPT-4o: 1,8 de 15 problemas.', 'o1 (pass@1): 11,1 de 15.', 'Salto de +62 puntos.'], VINO, VT, 20, 18, 'grafica'))
b.append(CARD(800, 265, 350, 195, 'Y EN CIENCIA Y CÓDIGO',
              ['En GPQA supera precisión de', 'doctorados humanos.', 'DeepSeek-R1 logra efecto', 'análogo con RL puro.'], OK, OKT, 20, 18, 'check'))
add_slide(5, 1, 'Evidencia', 'Salto medido entre modelo estándar y razonador',
          'En problemas de razonamiento profundo como AIME 2024, pensar antes multiplica el acierto.',
          'Fuente: OpenAI, Learning to reason with LLMs [cite:1] · DeepSeek-R1 [cite:2]',
          SVG(*b),
          'Vean los números reales medidos por OpenAI en el examen olímpico de matemáticas AIME de dos mil veinticuatro [cite:1]. En la barra gris de la izquierda, un modelo estándar muy capaz como GPT-4o apenas resolvió el doce por ciento de los problemas en promedio, es decir menos de dos de quince. Al pasar a o1, representado en la barra vino, con un solo intento subió al setenta y cuatro por ciento. Y en la barra dorada, al dedicar más cómputo en tiempo de prueba comparando sesenta y cuatro muestras por consenso, alcanzó el ochenta y tres por ciento. Además, en pruebas científicas de posgrado superó la media de expertos con doctorado. DeepSeek-R1 confirmó el mismo patrón con aprendizaje por refuerzo puro [cite:2]. No estamos viendo un truco cosmético, sino una capacidad nueva para tareas de alta complejidad lógica.')

# 6 · Cuándo usar razonador vs estándar (dos columnas)
b = [
    R(30, 30, 540, 440, OKT, OK, 3, 20),
    R(610, 30, 540, 440, VT, VINO, 3, 20),
    IC('reloj', 100, 90, 56, OK),
    T(145, 98, 'USA MODELO ESTÁNDAR', 26, True, OK),
    IC('ia', 680, 90, 56, VINO),
    T(725, 98, 'USA MODELO RAZONADOR', 26, True, VINO),
]
izq = [
    ('Clasificar tickets', 'intención o idioma en milisegundos'),
    ('Extraer campos JSON', 'nombre, fecha o número de pedido'),
    ('Redactar respuestas', 'plantillas breves con tono amable'),
    ('Regla práctica', 'baja latencia y menor costo por llamada'),
]
der = [
    ('Depurar fallos ocultos', 'trazar errores en varios archivos'),
    ('Planificar varios pasos', 'decidir orden de herramientas MCP'),
    ('Validar reglas complejas', 'cruzar políticas, fechas y excepciones'),
    ('Regla práctica', 'acepta segundos extra a cambio de rigor'),
]
for i, (t1, t2) in enumerate(izq):
    y = 148 + i * 78
    b.append(R(56, y, 488, 64, '#fff', OK if i == 3 else '#CFE6D6', 2, 12))
    b.append(T(78, y + 27, t1, 20, True, OK if i == 3 else INK))
    b.append(T(78, y + 52, t2, 17, False, GRIS))
for i, (t1, t2) in enumerate(der):
    y = 148 + i * 78
    b.append(R(636, y, 488, 64, '#fff', VINO if i == 3 else '#ECCFD4', 2, 12))
    b.append(T(658, y + 27, t1, 20, True, VINO if i == 3 else INK))
    b.append(T(658, y + 52, t2, 17, False, GRIS))
add_slide(6, 1, 'Criterio', 'Cuándo usar un razonador y cuándo un modelo estándar',
          'No toda tarea necesita pensar diez segundos; el exceso de cómputo también cuesta.',
          'Basado en: OpenAI o1 [cite:1] · Dibujo propio',
          SVG(*b),
          'Una decisión clásica de arquitectura en la nube es no gastar recursos pesados en tareas triviales. En el panel verde de la izquierda tienen las situaciones donde un modelo estándar rápido brilla: clasificar un ticket de soporte, extraer un código de pedido a formato JSON o redactar una respuesta corta con tono amable. Ahí ustedes necesitan milisegundos de latencia y un costo muy bajo por cada millón de tokens procesados. En el panel vino de la derecha aparecen las tareas que sí justifican un modelo razonador [cite:1]: depurar un error que cruza varios módulos, planificar qué herramientas MCP llamar en qué orden o verificar excepciones en reglas de negocio de CaribeMart. Si ponen un razonador lento simplemente a saludar a un cliente, pagan más tiempo y más presupuesto operativo sin ganar nada real en calidad ni en experiencia.')

# 7 · Programación asistida: del autocompletado al agente de repositorio (3 niveles)
niveles = [
    (40, 'NIVEL 1 · LÍNEA', 'Autocompletado', 'Completa la línea actual', 'en el editor', GRIS, GT, 'codigo'),
    (410, 'NIVEL 2 · BLOQUE', 'Chat con código', 'Genera una función aislada', 'tú copias y pegas', DOSC, DT, 'documento'),
    (780, 'NIVEL 3 · REPO', 'Agente de código', 'Lee archivos, edita diffs', 'y corre pruebas reales', VINO, VT, 'git'),
]
b = []
for i, (x, tag, tit, l1, l2, col, tint, ic) in enumerate(niveles):
    b.append(R(x, 54, 350, 380, tint, col, 3, 20))
    b.append(CHIP(x + 175, 78, tag, 17, col, col, color='#fff', anchor='middle', h=40, padx=18)[0])
    b.append(C(x + 175, 190, 50, '#fff', col, 2.5))
    b.append(IC(ic, x + 175, 190, 62, col))
    b.append(T(x + 175, 280, tit, 25, True, col, 'middle'))
    b.append(T(x + 175, 324, l1, 19, False, INK, 'middle'))
    b.append(T(x + 175, 352, l2, 19, False, INK, 'middle'))
    if i < 2:
        b.append(A(x + 356, 244, x + 404, 244, VINO, 4))
b.append(T(590, 474, 'opencode trabaja en el nivel 3: contexto del proyecto + herramientas + revisión humana', 19, True, VINO, 'middle'))
add_slide(7, 1, 'Código', 'Programación asistida: del autocompletado al agente',
          'Pasamos de sugerir la siguiente línea a editar repositorios completos con pruebas.',
          'Basado en: OpenCode [cite:9] y SWE-bench [cite:3,5] · Dibujo propio',
          SVG(*b),
          'La programación asistida por inteligencia artificial ha evolucionado en tres generaciones que conviene distinguir con total claridad. En la tarjeta gris de la izquierda está el nivel uno: el autocompletado clásico que adivina las siguientes palabras de la línea mientras ustedes escriben código en el editor. En el centro aparece el nivel dos: copiar un fragmento en un chat externo, pedir una función suelta y pegarla de vuelta a mano en su archivo. A la derecha está el nivel tres, el agente de repositorio como opencode [cite:9]. Aquí el modelo lee varios archivos del proyecto, busca dependencias entre módulos, propone cambios estructurados mediante diffs sobre el código real y ejecuta comandos de prueba para comprobar si algo se rompió [cite:3]. Por eso en esta unidad nos importa tanto qué contexto exacto le entregamos y cómo controlamos sus permisos en cada sesión.')

# 8 · Anatomía de un parche (diff unificado) (CODE16 + CALL)
lines_diff = [
    [('--- a/server.js', 'c')],
    [('+++ b/server.js', 'c')],
    [('@@ -42,4 +42,6 @@', 'k')],
    [(' const dias = Number(args.dias);', 'w')],
    [('-return pedidos.filter(p => p.estado == "pendiente");', 'r')],
    [('+if (!Number.isInteger(dias) || dias < 1) throw Error("N");', 's')],
    [('+return pedidos.filter(p => p.estado === "pendiente" && p.dias > dias);', 's')],
]
cd, w, h = CODE16(24, 48, lines_diff, size=17, padx=18, pady=18, w=796, title='git diff — server.js (CaribeMart)')
b = [cd]
calls = [
    (0, 875, 92, 1, 'Archivo original y nuevo', INK),
    (2, 875, 174, 2, 'Ubicación exacta de líneas', DOSC),
    (4, 875, 258, 3, 'Línea eliminada (rojo)', MAL),
    (6, 875, 344, 4, 'Línea agregada (verde)', OK),
]
for idx, cx, cy, num, lbl, col in calls:
    ly = linectr16(48, 17, idx, pady=18, title=True)
    b.append(CALL(822, ly, cx, cy, num, col))
    b.append(T(cx + 26, cy + 7, lbl, 19, True, col))
b.append(R(845, 398, 318, 76, DT, DOSC, 2.5, 14))
b.append(T(1004, 428, 'REGLA DE INGENIERÍA', 17, True, DOSC, 'middle'))
b.append(T(1004, 456, 'Lee el diff antes de aceptar', 18, True, INK, 'middle'))
add_slide(8, 1, 'Inspección', 'Anatomía de un diff: revisar antes de aceptar',
          'Los agentes proponen parches unificados que todo desarrollador debe auditar línea por línea.',
          'Ejemplo de elaboración propia sobre CaribeMart',
          SVG(*b),
          'Cuando un asistente de código modifica un archivo en CaribeMart, no reescribe todo el repositorio a ciegas ni debería trabajar sin control del equipo. Lo que entrega es un parche o diff unificado como el que ven a la izquierda. Sigan las llamadas numeradas hacia la derecha. La llamada uno muestra qué archivo se compara antes y después del cambio. La llamada dos indica en qué línea exacta del archivo ocurre la edición. La llamada tres, marcada en rojo con signo menos, muestra lo que se borra: aquí había una consulta que no validaba los días ni filtraba realmente por atraso. La llamada cuatro, en verde con signo más, introduce la validación de entero positivo y el filtro correcto. La tarjeta dorada abajo resume la regla de oro profesional: nunca aprueben un cambio de inteligencia artificial sin leer su diff completo.')

# 9 · El ciclo de programación asistida (4 nodos en círculo)
b = [
    R(40, 30, 1100, 440, GT, '#DDD', 2, 24),
]
nodos = [
    (270, 145, 'ojo', '1. LEER', 'código, reglas y fallo', INK, GT),
    (910, 145, 'codigo', '2. PROPONER DIFF', 'parche mínimo y claro', VINO, VT),
    (910, 360, 'pipeline', '3. PROBAR', 'tests y validación real', DOSC, DT),
    (270, 360, 'usuario', '4. REVISAR', 'humano aprueba o corrige', OK, OKT),
]
for cx, cy, ic, t1, t2, col, tint in nodos:
    b.append(R(cx - 190, cy - 62, 380, 124, '#fff', col, 3, 18))
    b.append(C(cx - 122, cy, 40, tint, col, 2))
    b.append(IC(ic, cx - 122, cy, 50, col))
    b.append(T(cx - 65, cy - 8, t1, 23, True, col))
    b.append(T(cx - 65, cy + 24, t2, 18, False, INK))
b.append(A(466, 145, 714, 145, VINO, 5))
b.append(A(910, 212, 910, 292, DOSC, 5))
b.append(A(714, 360, 466, 360, OK, 5))
b.append(A(270, 292, 270, 212, INK, 4, dash='8 6'))
b.append(CHIP(590, 224, 'Ciclo iterativo hasta pasar pruebas', 20, '#fff', VINO, anchor='middle', h=52, padx=24)[0])
add_slide(9, 1, 'Flujo', 'El ciclo real: leer, proponer diff, probar y revisar',
          'La calidad no sale en el primer intento; sale de ejecutar pruebas sobre cada cambio.',
          'Basado en: SWE-bench [cite:3,5] y OpenCode [cite:9] · Dibujo propio',
          SVG(*b),
          'Un error muy común al empezar con programación asistida es creer que el modelo acierta todo de un solo tiro mágico. En la práctica profesional el trabajo sigue este ciclo de cuatro estaciones continuas. Arriba a la izquierda, en el paso uno, el agente lee los archivos relevantes, las reglas del proyecto y el mensaje de error exacto. Luego sigue la flecha vino hacia el paso dos: propone un diff mínimo y acotado al problema. Después baja al paso tres: se ejecutan las pruebas automáticas o el comando de verificación para comprobar si el arreglo funciona de verdad. Finalmente pasa al paso cuatro abajo a la izquierda, donde ustedes como desarrolladores inspeccionan el resultado, aprueban el cambio o devuelven una corrección [cite:3]. Sin pruebas automáticas ni revisión humana, generar código rápido únicamente acelera la entrada de errores ocultos al repositorio.')

# 10 · SWE-bench Verified: tareas reales (embudo + dos tipos de test)
b = [
    R(30, 30, 560, 440, VT, VINO, 2.5, 18),
    T(310, 74, 'De issues reales a SWE-bench Verified', 21, True, VINO, 'middle'),
    R(80, 110, 460, 72, '#fff', INK, 2, 14),
    T(310, 142, '2.294 issues reales en 12 repos Python', 20, True, INK, 'middle'),
    T(310, 168, 'SWE-bench completo', 17, False, GRIS, 'middle'),
    A(310, 186, 310, 226, VINO, 4),
    R(115, 232, 390, 72, '#fff', DOSC, 2.5, 14),
    T(310, 264, 'Filtro y revisión por ingenieros humanos', 20, True, DOSC, 'middle'),
    T(310, 290, 'elimina tareas ambiguas o imposibles', 17, False, GRIS, 'middle'),
    A(310, 308, 310, 348, OK, 4),
    R(145, 354, 330, 86, OKT, OK, 3, 14),
    T(310, 392, 'SWE-bench Verified: 500 tareas', 22, True, OK, 'middle'),
    T(310, 422, 'solo entrega issue y código', 17, False, INK, 'middle'),
    CARD(625, 36, 525, 198, 'PRUEBA 1: FAIL_TO_PASS',
         ['Tests unitarios del error reportado.', 'Fallaban antes del parche y deben', 'pasar después de aplicarlo.'], VINO, '#fff', 21, 18, 'check'),
    CARD(625, 262, 525, 200, 'PRUEBA 2: PASS_TO_PASS',
         ['Tests de funciones existentes.', 'Garantizan que el cambio no rompió', 'otras partes del repositorio.'], OK, '#fff', 21, 18, 'escudo'),
]
add_slide(10, 1, 'Evaluación', 'SWE-bench Verified: medir en repositorios reales',
          'Resolver funciones sueltas ya no basta; hoy se evalúan parches sobre proyectos completos.',
          'Fuente: OpenAI, SWE-bench Verified [cite:3] y Princeton NLP [cite:5]',
          SVG(*b),
          'Para saber qué tan bueno es un modelo programando no basta pedirle que ordene una lista en diez líneas. Por eso la industria usa SWE-bench, creado por Princeton a partir de dos mil doscientas noventa y cuatro incidencias reales de doce repositorios de Python en GitHub [cite:5]. A la izquierda ven cómo nació SWE-bench Verified: ingenieros humanos auditaron y filtraron quinientas tareas bien especificadas donde el modelo solo recibe la descripción del problema y acceso al código, nunca los tests ocultos [cite:3]. A la derecha están las dos pruebas que debe superar el parche. Primero, las pruebas FAIL TO PASS, que fallaban antes y deben pasar tras el arreglo. Segundo, las pruebas PASS TO PASS, que aseguran que el modelo no dañó funciones vecinas. Esa doble verificación es exactamente la que deben exigir en su código.')

# 11 · Evolución medida en SWE-bench Verified (gráfico de barras comparativo)
b = [
    R(30, 30, 760, 440, '#fff', INK, 2, 18),
    T(410, 74, 'Porcentaje resuelto en SWE-bench', 21, True, INK, 'middle'),
    '<line x1="90" y1="386" x2="750" y2="386" stroke="%s" stroke-width="3"/>' % INK,
]
bars_swe = [
    (175, 16.0, '16,0 %', 'GPT-4o', 'original', GRIS),
    (335, 33.2, '33,2 %', 'GPT-4o', 'Verified', DOSC),
    (500, 33.4, '33,4 %', 'Claude 3.5', 'previo', AZUL),
    (660, 49.0, '49,0 %', 'Claude 3.5', 'Verified', VINO),
]
for cx, val, lbl, m1, m2, col in bars_swe:
    bh = val * 4.4
    by = 386 - bh
    b.append(R(cx - 48, by, 96, bh, col, None, 0, 10))
    b.append(T(cx, by - 12, lbl, 22, True, col, 'middle'))
    b.append(T(cx, 418, m1, 18, True, INK, 'middle'))
    b.append(T(cx, 442, m2, 16, False, GRIS, 'middle'))
b.append(CARD(815, 40, 335, 198, 'PROGRESO REAL',
              ['Claude 3.5 Sonnet subió de', '33,4 % a 49,0 % en', 'SWE-bench Verified.'], VINO, VT, 20, 18, 'grafica'))
b.append(CARD(815, 264, 335, 198, 'PERO ATENCIÓN',
              ['Incluso cerca del 50 %, la', 'mitad de tareas difíciles', 'aún fallan sin revisión.'], MAL, MALT, 20, 18, 'alerta'))
add_slide(11, 1, 'Cifras', 'Lo que logra un buen agente y lo que todavía falla',
          'Los avances en SWE-bench Verified son notables, pero la tasa de error sigue siendo alta.',
          'Fuentes: OpenAI [cite:3] y Anthropic [cite:4] sobre SWE-bench Verified',
          SVG(*b),
          'Miremos los datos verificados de progreso en código real. En las primeras dos barras ven la evaluación publicada por OpenAI cuando lanzó SWE-bench Verified [cite:3]: usando el mismo mejor agente abierto, GPT-4o pasó de dieciséis por ciento en el conjunto original sin filtrar a treinta y tres coma dos por ciento en el subconjunto verificado. En las barras tres y cuatro ven la cifra publicada por Anthropic para la actualización de Claude tres punto cinco Sonnet [cite:4]: subió de treinta y tres coma cuatro por ciento a cuarenta y nueve coma cero por ciento en esas mismas quinientas tareas. Son saltos enormes en pocos meses, pero fíjense en la tarjeta roja de la derecha: incluso rozando el cincuenta por ciento, una de cada dos incidencias reales no queda resuelta a la primera. Por eso la supervisión humana sigue siendo indispensable.')

# 12 · Límites reales de la programación asistida (3 tarjetas de alerta)
fallos = [
    (36, 'ALUCINA RUTAS O API', ['Inventa nombres de paquetes,', 'métodos que no existen o', 'archivos de otra carpeta.'], 'Cómo evitarlo:', 'Darle estructura real', 'y correr pruebas locales.', MAL, MALT, 'alerta'),
    (414, 'ROMPE LO QUE SERVÍA', ['Corrige un caso concreto', 'pero daña una regla previa', 'sin darse cuenta.'], 'Cómo evitarlo:', 'Revisar todo el diff y', 'exigir PASS_TO_PASS.', DOSC, DT, 'x'),
    (792, 'NO SABE TU NEGOCIO', ['Sintaxis perfecta pero lógica', 'incorrecta para CaribeMart,', 'sus plazos o permisos.'], 'Cómo evitarlo:', 'Contexto estable del', 'proyecto con AGENTS.md.', VINO, VT, 'pregunta'),
]
b = []
for x, tit, desc, ctit, c1, c2, col, tint, ic in fallos:
    b.append(R(x, 30, 352, 440, '#fff', col, 3, 20))
    b.append(R(x, 30, 352, 86, tint, None, 0, 18))
    b.append(IC(ic, x + 48, 73, 44, col))
    b.append(T(x + 84, 80, tit, 20, True, col))
    yy = 152
    for ln in desc:
        b.append(T(x + 26, yy, ln, 19, False, INK))
        yy += 30
    b.append(R(x + 22, 290, 308, 152, OKT, OK, 2, 14))
    b.append(T(x + 40, 326, ctit, 18, True, OK))
    b.append(T(x + 40, 362, c1, 19, True, INK))
    b.append(T(x + 40, 392, c2, 19, False, INK))
add_slide(12, 1, 'Límites', 'Tres fallos frecuentes en programación asistida',
          'Sin contexto ni pruebas, un modelo veloz introduce errores sutiles con mucha seguridad.',
          'Basado en: OWASP LLM [cite:16] y SWE-bench [cite:3] · Dibujo propio',
          SVG(*b),
          'En el aula y en producción aparecen tres fallos repetidos cuando confiamos ciegamente en un asistente de código. Primera columna en rojo: el modelo alucina rutas, parámetros o paquetes externos que suenan verosímiles pero no existen en nuestro repositorio. Segunda columna en dorado: arregla el error puntual que le pedimos, pero rompe sin querer otra función que ya servía porque no corrió pruebas de regresión completas [cite:3]. Tercera columna en vino: escribe JavaScript impecable en sintaxis, pero viola las reglas propias de CaribeMart, por ejemplo qué cuenta como pedido atrasado en la cadena o qué campo escrito por un cliente no debe obedecer nunca [cite:16]. En las cajas verdes de abajo está el antídoto práctico para los tres males: mostrar la estructura real del proyecto, revisar el diff completo con pruebas y mantener memoria clara del negocio.')

# 13 · De la capacidad bruta al contexto de CaribeMart (antes / después)
b = [
    R(20, 30, 550, 440, MALT, MAL, 3, 20),
    R(610, 30, 550, 440, OKT, OK, 3, 20),
    T(295, 76, 'MODELO POTENTE SIN CONTEXTO', 23, True, MAL, 'middle'),
    T(885, 76, 'MISMO MODELO + CONTEXTO', 23, True, OK, 'middle'),
    NODE(140, 210, 'ia', 'RAZONADOR', None, MAL, '#fff', r=52, isz=66, lsz=19),
    A(200, 210, 296, 210, MAL, 4, dash='8 6'),
    BUBBLE(304, 130, 240, 145, '#fff', MAL, 'left'),
    T(424, 182, ['¿Atrasado = 1 día', 'o 5 días? Improviso'], 19, True, MAL, 'middle'),
    CH(100, 385, 24, False),
    T(140, 393, 'No conoce las reglas de CaribeMart', 19, True, INK),
    NODE(720, 180, 'documento', 'AGENTS.md', None, OK, '#fff', r=44, isz=54, lsz=18),
    NODE(720, 330, 'ia', 'RAZONADOR', None, OK, '#fff', r=44, isz=54, lsz=18),
    A(720, 246, 720, 280, OK, 4),
    A(772, 300, 872, 230, OK, 4),
    BUBBLE(880, 145, 256, 145, '#fff', OK, 'left'),
    T(1008, 198, ['Atrasado > 3 días.', 'Uso pedidos_atrasados'], 18, True, OK, 'middle'),
    CH(665, 422, 22, True),
    T(702, 430, 'Aplica la norma real y respeta permisos', 18, True, INK),
]
add_slide(13, 1, 'Puente', 'Un modelo brillante sin contexto igual se equivoca',
          'La capacidad de razonar no reemplaza las reglas propias de tu repositorio y tu negocio.',
          'Basado en: AGENTS.md [cite:8] y CaribeMart · Dibujo propio',
          SVG(*b),
          'Esta comparación visual resume por qué la segunda parte de la clase es tan decisiva como la primera. A la izquierda tenemos un modelo razonador de última generación sin ningún contexto de nuestro proyecto. Sabe muchísimo de programación general, pero cuando le preguntan por pedidos atrasados de CaribeMart tiene que adivinar cuántos días definen un atraso, qué herramienta llamar o cómo responderle al cliente. A la derecha usamos exactamente el mismo modelo, pero conectado a un archivo AGENTS.md con las reglas claras y verificadas de CaribeMart [cite:8]. Ahora razona sobre hechos concretos de la operación: consulta pedidos atrasados con el umbral correcto y redacta en el tono esperado. La inteligencia del modelo es el motor; el contexto del proyecto es el mapa y el volante. Sin un buen mapa, un motor más potente solo nos desvía mucho más rápido.')

# 14 · Síntesis de la parte 1 (ruta horizontal)
b = ['<line x1="80" y1="230" x2="1100" y2="230" stroke="%s" stroke-width="10" stroke-linecap="round" stroke-dasharray="2 18"/>' % DOR]
pts = [
    (160, 'engranaje', 'Test-time|compute', 'piensa antes de hablar', VINO, VT, 'up'),
    (445, 'grafica', 'Elegir cuándo|razonar', 'costo vs complejidad', DOSC, DT, 'down'),
    (735, 'codigo', 'Revisar|cada diff', 'y correr pruebas', INK, GT, 'up'),
    (1020, 'documento', 'Falta el|contexto', 'siguiente bloque', OK, OKT, 'down'),
]
for i, (x, ic, t1, t2, col, tint, d) in enumerate(pts, 1):
    b.append(C(x, 230, 56, tint, col, 3))
    b.append(IC(ic, x, 230, 70, col))
    b.append(BADGE(x + 42, 230 - 42, i, col, 19, 20))
    yy = 92 if d == 'up' else 340
    b.append(T(x, yy, t1.split('|'), 25, True, col, 'middle'))
    b.append(T(x, yy + 62, t2, 18, False, GRIS, 'middle'))
add_slide(14, 1, 'Síntesis', 'Síntesis de la parte uno: razonamiento y código',
          'Cuatro ideas clave antes de pasar a la memoria del proyecto.',
          'Síntesis de la parte 1 · Dibujo propio',
          SVG(*b),
          'Cerramos la primera parte de la sesión recorriendo estas cuatro estaciones sobre la línea dorada. Estación uno: los modelos razonadores invierten cómputo en tiempo de prueba generando tokens de pensamiento para verificar pasos lógicos y corregir errores antes de responder [cite:1,2]. Estación dos: ese cómputo extra mejora muchísimo la lógica compleja, como vimos en AIME y en SWE-bench Verified [cite:3,4], pero debemos reservarlo para tareas que justifiquen su latencia y costo frente a un modelo estándar rápido. Estación tres: en programación asistida trabajamos por ciclos rigurosos de lectura, diff unificado, pruebas automáticas y revisión humana obligatoria. Estación cuatro: la capacidad de razonar sola no conoce las reglas de CaribeMart. En la parte dos entraremos a la ventana de contexto, veremos por qué el ruido degrada al modelo y aprenderemos a construir memoria estable con AGENTS.md.')
