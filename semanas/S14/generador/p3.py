from comun import *

# 29 · El problema de la memoria externa creciente (foto bodega + documentos)
b = [
    FOTO('bodega', 0, 14, 460, 472, 16, 'xMidYMid'),
    GRAD_SCRIM(0, 310, 460, 176, .85, 16),
    T(24, 418, 'CARIBEMART · 60 ALMACENES', 18, True, DOR),
    T(24, 452, ['Barranquilla, Bogotá y', 'cientos de documentos'], 23, True, '#fff'),
    CARD(500, 30, 650, 195, 'LO QUE EL MODELO NO SABE DE FÁBRICA',
         ['• Políticas de devoluciones y garantías de CaribeMart', '• Horarios y reglas por bodega en Barranquilla y Bogotá', '• Circulares internas actualizadas esta semana'], VINO, VT, 21, 18, 'alerta'),
    CARD(500, 255, 650, 215, 'POR QUÉ NO CABE TODO EN AGENTS.md',
         ['• Cientos de páginas saturan la ventana de contexto', '• Aumenta latencia, costo y caídas de atención', '• Necesitamos recuperar solo el fragmento útil'], DOSC, DT, 21, 18, 'documento'),
]
add_slide(29, 3, 'Motivación', 'Cuando el conocimiento del negocio supera a AGENTS.md',
          'Los manuales extensos y cambiantes no caben completos en el prompt de cada sesión.',
          'Basado en: Lewis et al. RAG [cite:10] y Anthropic [cite:7] · ' + credito('bodega'),
          SVG(*b),
          'En la parte tres resolvemos el problema arquitectónico que quedó abierto al cierre del bloque anterior. Miren la bodega real de CaribeMart a la izquierda. Una cadena minorista con sesenta almacenes entre Barranquilla y Bogotá acumula manuales extensos de devoluciones, tablas de garantía por electrodoméstico, instructivos de despacho entre sedes y circulares internas que cambian cada mes. Como resumen las tarjetas de la derecha, el modelo preentrenado exclusivamente con textos públicos de internet no conoce esos documentos privados de la empresa, y pegarlos enteros dentro de AGENTS.md saturaría la ventana de contexto, elevaría el costo operativo y reduciría la atención [cite:7]. ¿Cómo logramos entonces que el asistente responda exactamente según la política vigente de CaribeMart sin cargar doscientas páginas en cada llamada? La respuesta práctica es la generación aumentada por recuperación, conocida como RAG simple [cite:10].',
          fotos=['bodega'])

# 30 · Qué es RAG (Generación Aumentada por Recuperación) (fórmula visual)
b = [
    NODE(120, 130, 'pregunta', 'PREGUNTA', 'duda de política', INK, GT, r=52, isz=64, lsz=19, ssz=17),
    NODE(120, 355, 'bd', 'DOCUMENTOS', 'base externa propia', OK, OKT, r=52, isz=64, lsz=19, ssz=17),
    A(178, 355, 315, 355, OK, 4),
    R(325, 290, 250, 130, OKT, OK, 2.5, 16),
    T(450, 344, 'RECUPERADOR', 21, True, OK, 'middle'),
    T(450, 376, 'trae solo top 3 chunks', 18, False, INK, 'middle'),
    A(178, 130, 655, 175, INK, 4),
    A(582, 355, 655, 265, OK, 4),
    NODE(735, 220, 'ia', 'MODELO (LLM)', 'lee pregunta + evidencia', VINO, VT, r=66, isz=80, lsz=21, ssz=17),
    A(808, 220, 895, 220, VINO, 5),
    BUBBLE(905, 120, 250, 175, '#fff', VINO, 'left'),
    T(1030, 180, 'RESPUESTA', 22, True, VINO, 'middle'),
    T(1030, 214, ['fundamentada', 'y con cita exacta'], 19, False, INK, 'middle'),
    T(1030, 260, 'sin reentrenar pesos', 17, True, OK, 'middle'),
    R(325, 40, 260, 88, DT, DOSC, 2, 14),
    T(455, 76, 'Memoria paramétrica (pesos)', 17, True, DOSC, 'middle'),
    T(455, 104, '+ Memoria externa (docs)', 17, True, VINO, 'middle'),
]
add_slide(30, 3, 'Concepto', 'Qué es RAG: recuperar evidencia antes de responder',
          'Combina la capacidad lingüística del modelo con una memoria documental externa actualizable.',
          'Fuente: Lewis et al., Retrieval-Augmented Generation [cite:10] · Dibujo propio',
          SVG(*b),
          'El artículo seminal de Lewis y coautores en dos mil veinte definió RAG como la combinación inteligente de dos tipos de memoria [cite:10]. Por un lado está la memoria paramétrica, es decir el conocimiento lingüístico y general guardado en los pesos del modelo durante su preentrenamiento. Por otro lado está la memoria no paramétrica, una colección externa de documentos reales que nuestro equipo puede editar y actualizar cada día sin reentrenar jamás el modelo. Sigan el flujo del diagrama. Abajo a la izquierda viven los manuales de CaribeMart. Cuando llega una duda operativa arriba a la izquierda, un recuperador busca únicamente los tres fragmentos más relacionados con esa pregunta y los entrega junto con la consulta al modelo en el centro. Así el modelo redacta la respuesta de la derecha apoyándose en evidencia real, citando el documento exacto en lugar de adivinar.')

# 31 · Dos fases de RAG: indexación (offline) y consulta (online) (dos carriles)
b = [
    R(25, 28, 1130, 206, DT, DOSC, 3, 18),
    R(25, 262, 1130, 208, OKT, OK, 3, 18),
    T(55, 68, 'FASE 1 · INDEXACIÓN (offline, cuando cambian documentos)', 21, True, DOSC),
    T(55, 302, 'FASE 2 · CONSULTA (online, en cada pregunta del usuario)', 21, True, OK),
]
f1 = [(65, 'Docs CaribeMart', 'PDF y Markdown'), (335, 'Limpiar texto', 'quitar ruido'), (605, 'Chunking', 'cortar con solape'), (875, 'Guardar índice', 'léxico o vectorial')]
for i, (x, t1, t2) in enumerate(f1):
    b.append(R(x, 100, 220, 104, '#fff', DOSC, 2.5, 14))
    b.append(T(x + 110, 144, t1, 20, True, DOSC, 'middle'))
    b.append(T(x + 110, 176, t2, 17, False, INK, 'middle'))
    if i < 3:
        b.append(A(x + 224, 152, x + 266, 152, DOSC, 4))
f2 = [(65, 'Pregunta', 'duda operativa'), (335, 'Buscar top k', 'traer 3 chunks'), (605, 'Armar prompt', 'pregunta + citas'), (875, 'Responder', 'con fuente real')]
for i, (x, t1, t2) in enumerate(f2):
    b.append(R(x, 336, 220, 104, '#fff', OK, 2.5, 14))
    b.append(T(x + 110, 380, t1, 20, True, OK, 'middle'))
    b.append(T(x + 110, 412, t2, 17, False, INK, 'middle'))
    if i < 3:
        b.append(A(x + 224, 388, x + 266, 388, OK, 4))
add_slide(31, 3, 'Fases', 'Las dos fases de RAG: indexar offline y consultar online',
          'Separar la preparación de documentos de la consulta mantiene las respuestas rápidas.',
          'Basado en: Lewis et al. [cite:10] y Anthropic [cite:11] · Dibujo propio',
          SVG(*b),
          'Todo sistema RAG, desde un script educativo de cien líneas hasta un buscador corporativo en la nube, se divide en estas dos pistas horizontales bien diferenciadas. Arriba en dorado tienen la fase uno, indexación fuera de línea. Esta pista solo corre cuando ustedes cargan o actualizan manuales de CaribeMart: se leen los archivos, se limpia el texto de ruido, se dividen en fragmentos llamados chunks y se guardan en un índice rápido [cite:11]. Abajo en verde tienen la fase dos, consulta en línea, que ocurre cada vez que un operador hace una pregunta. Aquí no volvemos a leer toda la biblioteca desde cero: el buscador consulta el índice en milisegundos, recupera los tres fragmentos más relevantes, los inserta en el prompt y el modelo genera una respuesta verificable con fuente [cite:10]. Separar estas dos fases mantiene muy bajos los tiempos de espera y los costos.')

# 32 · Paso 1: ingesta y limpieza de documentos (izquierda docs -> normalizador -> salida limpia)
b = [
    R(30, 50, 280, 110, '#fff', INK, 2, 14),
    T(170, 96, 'politica-envios.md', 19, True, INK, 'middle', mono=True),
    T(170, 128, 'texto limpio y títulos', 17, False, GRIS, 'middle'),
    R(30, 195, 280, 110, '#fff', VINO, 2, 14),
    T(170, 241, 'garantias-2026.pdf', 19, True, VINO, 'middle', mono=True),
    T(170, 273, 'tablas y encabezados', 17, False, GRIS, 'middle'),
    R(30, 340, 280, 110, '#fff', DOSC, 2, 14),
    T(170, 386, 'bodega-baq.html', 19, True, DOSC, 'middle', mono=True),
    T(170, 418, 'etiquetas y menú HTML', 17, False, GRIS, 'middle'),
    A(316, 105, 425, 220, INK, 4),
    A(316, 250, 425, 250, VINO, 4),
    A(316, 395, 425, 280, DOSC, 4),
    NODE(515, 250, 'engranaje', 'LIMPIEZA', 'quita menús y ruido', VINO, VT, r=68, isz=80, lsz=21, ssz=17),
    A(590, 250, 695, 250, OK, 5),
    R(705, 55, 445, 390, OKT, OK, 3, 18),
    T(927, 98, 'TEXTO NORMALIZADO + METADATOS', 20, True, OK, 'middle'),
    R(735, 130, 385, 125, '#fff', OK, 2, 12),
    T(755, 165, 'fuente: "garantias-2026.pdf"', 17, True, VINO, mono=True),
    T(755, 196, 'seccion: "Devoluciones Caribe"', 17, False, INK, mono=True),
    T(755, 227, 'vigencia: "2026-11"', 17, False, GRIS, mono=True),
    R(735, 278, 385, 136, '#fff', INK, 2, 12),
    T(755, 314, 'Por qué importan los metadatos:', 18, True, INK),
    T(755, 346, 'Permiten citar el documento exacto', 17, False, INK),
    T(755, 376, 'y filtrar versiones vencidas.', 17, False, INK),
]
add_slide(32, 3, 'Ingesta', 'Paso 1: limpiar documentos y conservar metadatos',
          'Basura entra, basura se recupera; limpiar encabezados repetidos y guardar el origen es clave.',
          'Basado en: Anthropic, Contextual Retrieval [cite:11] · Dibujo propio',
          SVG(*b),
          'El primer paso de la indexación rara vez recibe suficiente cuidado en proyectos reales, y justamente ahí se decide gran parte de la calidad de un sistema RAG. A la izquierda ven los documentos originales de CaribeMart en formatos variados: guías escritas en Markdown, archivos PDF de garantías y páginas internas de intranet con menús y pies repetidos. En el centro todo el texto pasa por una limpieza cuidadosa que elimina barras de navegación, pies de página repetitivos y etiquetas HTML que solo introducen ruido al índice. A la derecha vemos qué sale hacia la base documental: texto normalizado acompañado de metadatos esenciales como el nombre del archivo, la sección exacta y la fecha de vigencia [cite:11]. Sin esos metadatos estructurados, luego el agente no podrá citar de dónde extrajo cada regla ni distinguir una circular vigente de otra vencida del año anterior.')

# 33 · Paso 2: fragmentación o chunking (documento dividido + comparativa tamaño)
b = [
    R(30, 30, 1120, 215, GT, INK, 2, 18),
    T(60, 68, 'DOCUMENTO LARGO DIVIDIDO EN FRAGMENTOS (CHUNKS) CON SOLAPE', 20, True, INK),
    R(60, 96, 340, 116, VT, VINO, 2.5, 12),
    T(230, 140, 'Chunk 1', 21, True, VINO, 'middle'),
    T(230, 174, 'Sección 1 y parte de 2', 17, False, INK, 'middle'),
    R(360, 96, 360, 116, DT, DOSC, 2.5, 12, op='0.9'),
    T(540, 140, 'Chunk 2 (con solape)', 21, True, DOSC, 'middle'),
    T(540, 174, 'Cierra 2 y abre 3 sin cortar', 17, False, INK, 'middle'),
    R(680, 96, 390, 116, OKT, OK, 2.5, 12),
    T(875, 140, 'Chunk 3', 21, True, OK, 'middle'),
    T(875, 174, 'Cierra sección 3 completa', 17, False, INK, 'middle'),
    CARD(30, 272, 352, 196, 'MUY PEQUEÑO (ej. 50 tokens)',
         ['• Corta la oración o la condición', '• Pierde de qué producto habla', '• Recupera frases sueltas sin sentido'], MAL, MALT, 19, 17, 'x'),
    CARD(414, 272, 352, 196, 'EQUILIBRADO (con solape)',
         ['• Respeta párrafos y títulos', '• Solape moderado entre fragmentos', '• Mantiene contexto de cada regla'], OK, OKT, 19, 17, 'check'),
    CARD(798, 272, 352, 196, 'MUY GRANDE (ej. 3.000 tokens)',
         ['• Mezcla 5 temas en un bloque', '• Diluye la búsqueda por relevancia', '• Vuelve a meter ruido en ventana'], DOSC, DT, 19, 17, 'alerta'),
]
add_slide(33, 3, 'Chunking', 'Paso 2: fragmentar documentos sin cortar las ideas',
          'El tamaño del fragmento y el solape deciden si el buscador entrega contexto útil o ruido.',
          'Basado en: Anthropic, Contextual Retrieval [cite:11] · Dibujo propio',
          SVG(*b),
          '¿Por qué no guardamos cada manual completo como una sola pieza gigante dentro del índice? Porque si recuperamos tres manuales enteros de cuarenta páginas cada uno, volvemos a inundar la ventana de contexto del modelo y reaparece el ruido. Por eso arriba ven el proceso de fragmentación o chunking: dividimos el texto limpio en trozos manejables procurando respetar encabezados y párrafos completos, y dejamos un pequeño solape u overlap entre un fragmento y el siguiente para que ninguna condición o excepción quede partida por la mitad [cite:11]. Abajo tienen las tres zonas claras de diseño. Si el fragmento es diminuto, la frase queda huérfana y pierde su sujeto. Si es enorme, mezcla cinco temas distintos y mete mucho relleno. Un tamaño moderado con solape suave entre fragmentos contiguos y su título adjunto funciona muy bien ahora.')

# 34 · Paso 3: índice léxico (BM25) vs vectorial (embeddings) e híbrido (con dato Anthropic)
b = [
    CARD(30, 30, 540, 210, 'BÚSQUEDA LÉXICA (BM25 / PALABRAS)',
         ['• Busca coincidencia exacta de términos', '• Imbatible para códigos SKU, IDs, "Ley 1581"', '• Falla si usas sinónimos ("demora" vs "atraso")'], AZUL, AZULT, 20, 18, 'codigo'),
    CARD(610, 30, 540, 210, 'BÚSQUEDA VECTORIAL (EMBEDDINGS)',
         ['• Compara cercanía de significado semántico', '• Encuentra "demora en envío" para "pedido atrasado"', '• Puede fallar con códigos exactos o siglas raras'], VINO, VT, 20, 18, 'ia'),
    A(300, 246, 480, 296, AZUL, 4),
    A(880, 246, 700, 296, VINO, 4),
    R(80, 304, 1020, 166, OKT, OK, 3, 18),
    IC('check', 148, 386, 62, OK),
    T(205, 352, 'ENFOQUE HÍBRIDO RECOMENDADO (LÉXICO + VECTORIAL + CONTEXTO)', 21, True, OK),
    T(205, 392, 'Anthropic midió en RAG contextual: embeddings + BM25 reducen fallos en 49 %', 19, True, INK),
    T(205, 426, 'y al añadir reordenamiento (reranking) la reducción llega al 67 %.', 19, False, INK),
]
add_slide(34, 3, 'Indexación', 'Paso 3: índice léxico, vectorial y búsqueda híbrida',
          'Las palabras exactas y el significado semántico se complementan al recuperar fragmentos.',
          'Fuente: Anthropic, Contextual Retrieval [cite:11] · Dibujo propio',
          SVG(*b),
          'Una vez tenemos los fragmentos listos, ¿cómo decide el buscador cuáles responden mejor a una consulta? Existen dos familias que ven en las tarjetas superiores. A la izquierda, la búsqueda léxica clásica con algoritmos como BM25 localiza coincidencias exactas de palabras y su relevancia estadística; es imbatible cuando alguien busca un código SKU, una referencia de producto o la Ley mil quinientos ochenta y uno, pero falla con sinónimos. A la derecha, la búsqueda vectorial usa embeddings para comparar significado cercano: conecta demora en entrega con pedido atrasado aunque no compartan palabras. Como muestra la banda verde inferior, combinar ambas estrategias es superior: Anthropic comprobó en su estudio de recuperación contextual que unir embeddings con BM25 reduce los fallos de recuperación en cuarenta y nueve por ciento, y hasta sesenta y siete por ciento al añadir reordenamiento [cite:11].')

# 35 · Qué es un embedding explicado de forma visual (plano 2D de cercanía)
b = [
    R(30, 30, 680, 440, '#fff', INK, 2, 18),
    T(370, 72, 'Mapa simplificado de significados (vectores en 2D)', 21, True, INK, 'middle'),
    A(90, 415, 670, 415, INK, 2.5),
    A(90, 415, 90, 96, INK, 2.5),
    R(140, 118, 290, 152, VT, VINO, 2, 18, dash='6 5'),
    T(285, 146, 'Cerca en significado', 17, True, VINO, 'middle'),
    C(200, 185, 9, VINO), T(216, 191, '"pedido atrasado"', 17, True, INK),
    C(215, 224, 9, VINO), T(232, 230, '"demora de entrega"', 17, False, INK),
    C(190, 254, 9, OK), T(208, 260, 'Pregunta: "¿si tarda 4 días?"', 17, True, OK),
    R(420, 285, 260, 114, AZULT, AZUL, 2, 18, dash='6 5'),
    T(550, 314, 'Otro tema aparte', 17, True, AZUL, 'middle'),
    C(455, 348, 9, AZUL), T(472, 354, '"horario Barranquilla"', 17, False, INK),
    C(465, 378, 9, AZUL), T(482, 384, '"dirección almacén"', 17, False, INK),
    CARD(740, 36, 410, 200, 'QUÉ ES UN EMBEDDING',
         ['Un modelo convierte un texto en', 'una lista de números (vector).', 'Ideas parecidas quedan cerca.'], VINO, VT, 20, 18, 'grafica'),
    CARD(740, 262, 410, 204, 'POR QUÉ SIRVE EN RAG',
         ['La pregunta también se vuelve vector.', 'Medimos distancia y traemos los', 'fragmentos más cercanos.'], OK, OKT, 20, 18, 'check'),
]
add_slide(35, 3, 'Vectores', 'Qué es un embedding sin matemática pesada',
          'Representar textos como coordenadas permite buscar por intención y no solo por palabras iguales.',
          'Basado en: Lewis et al. [cite:10] y Anthropic [cite:11] · Dibujo propio',
          SVG(*b),
          'Muchas veces el término embedding suena innecesariamente intimidante, pero su intuición visual es tan sencilla como este plano de dos dimensiones a la izquierda. Un modelo especializado en embeddings convierte cada fragmento de texto en un arreglo numérico ordenado, es decir una coordenada dentro de un mapa geométrico de significados [cite:10,11]. Textos que expresan ideas afines quedan agrupados en la misma región del espacio: fíjense arriba en vino cómo pedido atrasado y demora de entrega caen muy cerca entre sí, mientras horario de Barranquilla y dirección de almacén caen en otro vecindario azul aparte. Cuando un operador pregunta qué aplica si un envío tarda cuatro días, transformamos su pregunta en otro punto verde y medimos cuáles fragmentos están a menor distancia. Así encontramos la norma correcta aunque el usuario no escriba exactamente las mismas palabras del manual.')

# 36 · Flujo completo de consulta en CaribeMart (5 nodos con BADGE) - texto >= 17px
b = [
    R(30, 30, 1120, 440, GT, '#DDD', 2, 22),
]
pasos_q = [
    (137, 160, '1', 'usuario', 'OPERADOR', ['¿Cómo compensar', 'un atraso?'], INK, '#fff'),
    (363, 160, '2', 'documento', 'BUSCADOR', ['consulta el', 'índice RAG'], AZUL, AZULT),
    (589, 160, '3', 'bd', 'TOP 3 CHUNKS', ['trae texto y', 'sección exacta'], OK, OKT),
    (815, 160, '4', 'ia', 'MODELO (LLM)', ['redacta con', 'evidencia'], VINO, VT),
    (1041, 160, '5', 'check', 'RESPUESTA', ['cita manual', 'oficial'], OK, OKT),
]
for i, (cx, cy, num, ic, tit, sub, col, tint) in enumerate(pasos_q):
    b.append(R(cx - 92, cy - 82, 184, 198, tint, col, 2.5, 16))
    b.append(IC(ic, cx, cy - 14, 52, col))
    b.append(BADGE(cx - 66, cy - 58, num, col, 17, 17))
    b.append(T(cx, cy + 44, tit, 18, True, col, 'middle'))
    b.append(T(cx, cy + 74, sub, 17, False, INK, 'middle'))
    if i < 4:
        nx = pasos_q[i + 1][0]
        b.append(A(cx + 94, cy + 12, nx - 94, cy + 12, col, 4))
b.append(R(56, 304, 1068, 144, '#fff', VINO, 2.5, 16))
b.append(T(82, 342, 'QUÉ VIAJA AL MODELO EN EL PASO 4 (PROMPT AUMENTADO):', 19, True, VINO))
b.append(T(82, 378, 'Instrucción: "Responde solo usando estos fragmentos; si no consta el dato, dilo y cita la fuente."', 18, True, INK))
b.append(T(82, 416, 'Fragmento: [politica-envios.md §3.2] "Atraso > 3 días: envío gratis..."', 17, False, GRIS, mono=True))
add_slide(36, 3, 'Flujo', 'Flujo completo de una consulta RAG en CaribeMart',
          'De la pregunta del operador a una respuesta trazable con sección y documento.',
          'Basado en: Lewis et al. [cite:10] · Dibujo propio',
          SVG(*b),
          'Sigamos ahora el recorrido completo en vivo cuando un asesor u operador de CaribeMart tiene una duda concreta de política interna. En el paso uno pregunta cómo compensar un pedido atrasado. En el paso dos el buscador consulta el índice de documentos ya preparado previamente en la fase fuera de línea. En el paso tres recupera únicamente los tres fragmentos mejor puntuados conservando siempre su etiqueta de documento y sección exacta [cite:10]. En el paso cuatro, miren la caja blanca inferior, construimos un prompt aumentado con reglas muy estrictas: instruimos al modelo para que responda solo usando esos fragmentos recuperados, cite el origen exacto y reconozca explícitamente si algún dato no aparece en las fuentes. Así en el paso cinco sale una respuesta trazable y auditable, sin inventar descuentos ni prometer beneficios fuera de la política vigente.')

# 37 · Respuesta fundamentada vs alucinación (antes / después con burbujas)
b = [
    R(25, 30, 550, 440, MALT, MAL, 3, 20),
    R(605, 30, 550, 440, OKT, OK, 3, 20),
    T(300, 74, 'SIN RAG: ALUCINA CON SEGURIDAD', 22, True, MAL, 'middle'),
    T(880, 74, 'CON RAG SIMPLE: RESPUESTA CON CITA', 22, True, OK, 'middle'),
    CHIP(300, 104, 'Pregunta: "¿Cuántos días tengo para devolver?"', 17, '#fff', INK, anchor='middle', h=44, padx=16)[0],
    CHIP(880, 104, 'Misma pregunta con top-3 fragmentos', 17, '#fff', INK, anchor='middle', h=44, padx=16)[0],
    BUBBLE(65, 178, 470, 145, '#fff', MAL, 'left'),
    T(300, 232, ['"En CaribeMart tienes 30 días', 'calendario para cualquier producto."'], 20, True, MAL, 'middle'),
    T(300, 282, '(dato inventado de memoria general)', 17, False, GRIS, 'middle'),
    CH(105, 392, 24, False),
    T(145, 400, 'Sin fuente; promete política falsa', 19, True, MAL),
    BUBBLE(645, 178, 470, 145, '#fff', OK, 'left'),
    T(880, 224, ['"Perecederos: 24 horas. Hogar: 15 días', 'con factura [politica-devoluciones §2]."'], 19, True, OK, 'middle'),
    T(880, 282, '(si no aparece en docs: "No consta")', 17, False, GRIS, 'middle'),
    CH(685, 392, 24, True),
    T(725, 400, 'Verificable y auditable por el equipo', 19, True, OK),
]
add_slide(37, 3, 'Fidelidad', 'Respuesta fundamentada frente a alucinación segura',
          'Exigir evidencia recuperada reduce inventos y permite auditar cada respuesta.',
          'Basado en: Lewis et al. RAG [cite:10] · Dibujo propio',
          SVG(*b),
          '¿Cuál es la ganancia práctica más visible para CaribeMart cuando conectan recuperación documental verificada? Comparen con atención las dos burbujas de diálogo del gráfico. Cuando un cliente o un asesor pregunta cuántos días tiene para devolver un artículo y el modelo responde únicamente desde su memoria paramétrica sin RAG, suele inventar un plazo genérico como treinta días calendario que suena muy convincente pero contradice por completo la política de perecederos de la empresa. Con RAG simple a la derecha, el modelo lee el fragmento recuperado de la política oficial de devoluciones y responde con precisión verificable [cite:10]: veinticuatro horas para perecederos y quince días para productos del hogar con factura, dejando la cita visible. Igual de valioso: si la pregunta toca algo que no existe en los manuales, la instrucción del prompt lo obliga a responder que no consta.')

# 38 · RAG simple en un proyecto local (CODE16 compacto dentro de 1180)
lines_rag = [
    [('const chunks = cargarDocs("./docs/");', 'c')],
    [('function buscar(pregunta, k = 3) {', 'k')],
    [('  return chunks', 'w')],
    [('    .map(c => ({', 'w')],
    [('      fuente: c.id, texto: c.txt,', 'w')],
    [('      pt: similitud(pregunta, c)', 'w')],
    [('    }))', 'w')],
    [('    .sort((a, b) => b.pt - a.pt)', 'n')],
    [('    .slice(0, k);', 's')],
    [('}', 'k')],
]
cd, w, h = CODE16(24, 34, lines_rag, size=17, padx=18, pady=16, w=680, title='rag-simple.js — búsqueda mínima local')
b = [cd]
calls = [
    (0, 770, 96, 1, 'Carga .md de docs/', INK),
    (5, 770, 232, 2, 'Puntúa y conserva fuente', DOSC),
    (8, 770, 336, 3, 'Retorna solo top-k', OK),
]
for idx, cx, cy, num, lbl, col in calls:
    ly = linectr16(34, 17, idx, pady=16, title=True)
    b.append(CALL(706, ly, cx, cy, num, col))
    b.append(T(cx + 26, cy + 7, lbl, 19, True, col))
b.append(R(745, 378, 405, 96, VT, VINO, 2.5, 14))
b.append(T(947, 412, 'SIN SOBREINGENIERÍA', 18, True, VINO, 'middle'))
b.append(T(947, 444, 'Empieza con BM25 o similitud local', 17, False, INK, 'middle'))
add_slide(38, 3, 'Implementación', 'Cómo luce un RAG simple sin sobreingeniería',
          'No necesitan un clúster masivo para empezar; basta indexar fragmentos con su fuente y puntaje.',
          'Ejemplo didáctico de elaboración propia sobre CaribeMart',
          SVG(*b),
          'Muchos equipos de ingeniería fracasan al inicio porque antes de comprobar si sus documentos están limpios intentan desplegar tres bases de datos complejas y costosas en la nube. Miren este esquema en apenas diez líneas a la izquierda para entender el corazón de un RAG simple local. En la llamada uno cargamos los documentos ya fragmentados desde la carpeta local de documentación de CaribeMart. En la llamada dos recorremos cada fragmento guardando su identificador de origen y calculando un puntaje de relevancia contra la pregunta, ya sea por coincidencia léxica tipo BM25 o por cercanía de vectores [cite:11]. En la llamada tres ordenamos de mayor a menor puntuación y devolvemos únicamente los tres fragmentos superiores. Esa salida limpia se inyecta al prompt o se expone como herramienta de consulta. Empiecen siempre simple, midan qué recupera y escalen solo cuando el volumen lo exija.')

# 39 · Fallos típicos de un RAG simple (3 pares síntoma -> arreglo)
errs = [
    (54, 'Chunks cortados a la mitad', 'Corta la condición de la excepción', 'Respetar títulos con solape moderado', MAL),
    (194, 'Índice desactualizado', 'Responde con política del año pasado', 'Reindexar en CI o al cambiar docs/ + fecha', DOSC),
    (334, 'Usar RAG para contar datos vivos', 'Pregunta "¿cuántos pedidos hoy?" a PDFs', 'Datos operativos van por MCP SQL/JSON', VINO),
]
b = []
for y, tit, sint, fix, col in errs:
    b.append(R(30, y, 520, 114, MALT, col, 2.5, 16))
    b.append(CH(74, y + 57, 22, False))
    b.append(T(114, y + 46, tit, 21, True, col))
    b.append(T(114, y + 80, sint, 18, False, INK))
    b.append(A(558, y + 57, 635, y + 57, OK, 4))
    b.append(R(645, y, 505, 114, OKT, OK, 2.5, 16))
    b.append(CH(689, y + 57, 22, True))
    b.append(T(729, y + 46, 'Solución práctica', 18, True, OK))
    b.append(T(729, y + 80, fix, 19, True, INK))
add_slide(39, 3, 'Depuración', 'Tres fallos clásicos en RAG simple y cómo corregirlos',
          'Casi todos los errores de RAG nacen en los fragmentos o en pedirle datos transaccionales.',
          'Basado en: Anthropic, Contextual Retrieval [cite:11] · Dibujo propio',
          SVG(*b),
          'Cuando un buscador RAG entrega respuestas pobres o imprecisas, casi nunca es culpa directa del modelo de lenguaje; suele deberse a uno de estos tres fallos concretos de ingeniería. Fila uno: fragmentos partidos por conteo rígido de caracteres que separan una regla general de su excepción operativa; el arreglo consiste en dividir por secciones respetando encabezados y añadiendo un solape moderado [cite:11]. Fila dos: alguien actualizó el manual de garantías en la carpeta de documentos, pero olvidó reconstruir el índice, de modo que el sistema sigue citando la política vencida del año anterior; la solución es reindexar automáticamente al cambiar archivos y conservar fechas de vigencia. Fila tres, el error conceptual más frecuente: usar RAG para contar cuántos pedidos pendientes hay hoy en Barranquilla. RAG consulta manuales estables; los datos transaccionales vivos pertenecen siempre a herramientas MCP.')

# 40 · Comparación honesta: AGENTS.md vs RAG vs herramientas MCP (3 tarjetas visuales ricas)
cols3 = [
    (30, 'AGENTS.md', 'Reglas fijas del proyecto', 'Cambia poco (por sprint)', 'Siempre en ventana', 'Atraso > 3 días, tono,', 'datos != instrucciones', VINO, VT, 'documento'),
    (414, 'RAG SIMPLE', 'Conocimiento documental', 'Cambia por semana o mes', 'Top-k bajo demanda', 'Manual de devoluciones,', 'garantías de 60 tiendas', OK, OKT, 'bd'),
    (798, 'HERRAMIENTAS MCP', 'Datos vivos y acciones', 'Cambia cada segundo', 'Ejecuta cuando hace falta', 'pedidos_atrasados,', 'cancelar_pedido (ask)', AZUL, AZULT, 'funcion'),
]
b = []
for x, tit, qg, cc, cv, e1, e2, col, tint, ic in cols3:
    b.append(R(x, 28, 352, 444, '#fff', col, 3, 20))
    b.append(R(x, 28, 352, 92, tint, None, 0, 18))
    b.append(IC(ic, x + 52, 74, 48, col))
    b.append(T(x + 92, 82, tit, 21, True, col))
    items = [('Qué resuelve', qg), ('Cuándo cambia', cc), ('Cómo entra', cv), ('En CaribeMart', e1 + ' ' + e2)]
    yy = 152
    for idx_it, (k, v) in enumerate(items):
        b.append(R(x + 18, yy - 24, 316, 68 if idx_it < 3 else 82, GT if idx_it % 2 == 0 else '#fff', '#E0E0E0', 1.5, 10))
        b.append(T(x + 32, yy, k, 16, True, col))
        if idx_it < 3:
            b.append(T(x + 32, yy + 26, v, 18, False, INK))
        else:
            b.append(T(x + 32, yy + 24, e1, 17, True, INK))
            b.append(T(x + 32, yy + 48, e2, 17, True, INK))
        yy += 78
add_slide(40, 3, 'Comparativa', 'Comparación honesta: AGENTS.md vs RAG vs MCP',
          'No compiten entre sí; cada mecanismo cubre una frecuencia de cambio y un tipo de dato.',
          'Basado en: AGENTS.md [cite:8], RAG [cite:10] y OpenCode [cite:9,12] · Dibujo propio',
          SVG(*b),
          'Esta comparación honesta es fundamental para diseñar arquitecturas limpias sin forzar una sola herramienta para resolverlo todo. Vean las tres columnas en paralelo. A la izquierda está AGENTS.md: guarda reglas fijas del proyecto que cambian poco por cada ciclo de desarrollo y entran siempre en la ventana de contexto, como la definición exacta de atraso o las reglas obligatorias de seguridad [cite:8,9]. En el centro está RAG simple: almacena manuales, tablas de garantías y políticas extensas que cambian por semana o mes y se recuperan bajo demanda según la pregunta del usuario [cite:10]. A la derecha están las herramientas MCP: consultan datos operativos que cambian segundo a segundo y ejecutan acciones reales como cancelar pedido bajo confirmación humana [cite:12]. Si meten datos vivos en AGENTS.md caducan de inmediato; si dejan reglas de seguridad solo en RAG, podrían omitirse en algún turno.')

# 41 · Árbol de decisión rápido para elegir entre los tres
b = [
    NODE(140, 250, 'pregunta', 'NUEVO DATO', '¿dónde va?', INK, GT, r=58, isz=70, lsz=19, ssz=17),
    A(204, 250, 290, 120, AZUL, 4),
    A(204, 250, 290, 250, VINO, 4),
    A(204, 250, 290, 380, OK, 4),
    R(300, 66, 440, 106, AZULT, AZUL, 2.5, 16),
    T(520, 108, '¿Cambia en tiempo real o modifica estado?', 19, True, AZUL, 'middle'),
    T(520, 140, 'ej. inventario hoy, cancelar pedido 1042', 17, False, INK, 'middle'),
    R(300, 196, 440, 106, VT, VINO, 2.5, 16),
    T(520, 238, '¿Es norma fija que siempre debe aplicar?', 19, True, VINO, 'middle'),
    T(520, 270, 'ej. comando de test, regla datos != orden', 17, False, INK, 'middle'),
    R(300, 326, 440, 106, OKT, OK, 2.5, 16),
    T(520, 368, '¿Es texto amplio de políticas o manuales?', 19, True, OK, 'middle'),
    T(520, 400, 'ej. garantías 2026, guía de 60 almacenes', 17, False, INK, 'middle'),
    A(748, 120, 845, 120, AZUL, 4),
    A(748, 250, 845, 250, VINO, 4),
    A(748, 380, 845, 380, OK, 4),
    CHIP(855, 88, 'Usa herramienta MCP', 21, AZUL, AZUL, color='#fff', h=64, padx=24, icon='funcion', isz=34)[0],
    CHIP(855, 218, 'Ponlo en AGENTS.md', 21, VINO, VINO, color='#fff', h=64, padx=24, icon='documento', isz=34)[0],
    CHIP(855, 348, 'Indexa en RAG simple', 21, OK, OK, color='#fff', h=64, padx=24, icon='bd', isz=34)[0],
]
add_slide(41, 3, 'Decisión', 'Árbol de decisión: dónde ubicar cada conocimiento',
          'Tres preguntas concretas resuelven la mayoría de las dudas de arquitectura.',
          'Síntesis de diseño · Elaboración propia',
          SVG(*b),
          'Cuando estén diseñando su propio asistente en el proyecto de aula del tercer corte, pasen cada pieza de información por este árbol de tres preguntas rápidas. Pregunta uno arriba en azul: ¿el dato cambia minuto a minuto en producción o implica modificar un registro real como cancelar un pedido específico? Entonces pertenece a una herramienta MCP validada estrictamente con zod. Pregunta dos en el centro en vino: ¿es una instrucción obligatoria del proyecto, un comando exacto de prueba o una norma de seguridad que debe regir siempre en cada sesión? Entonces va directamente en AGENTS.md [cite:8]. Pregunta tres abajo en verde: ¿es un manual extenso, una guía por sucursal o una política de devoluciones que solo hace falta cuando alguien consulta ese tema? Entonces se indexa en RAG simple [cite:10]. Tres preguntas claras evitan construir arquitecturas costosas y frágiles.')

# 42 · Síntesis de la parte 3 (triángulo integrador)
b = [
    R(40, 30, 1100, 440, GT, '#DDD', 2, 22),
    NODE(590, 118, 'documento', 'AGENTS.md', 'reglas fijas', VINO, VT, r=48, isz=58, lsz=20, ssz=17),
    NODE(240, 360, 'bd', 'RAG SIMPLE', 'chunking + índice + cita', OK, OKT, r=52, isz=62, lsz=20, ssz=17),
    NODE(940, 360, 'funcion', 'MCP', 'datos vivos y acciones', AZUL, AZULT, r=52, isz=62, lsz=20, ssz=17),
    A(530, 148, 292, 316, VINO, 4, both=True),
    A(650, 148, 888, 316, VINO, 4, both=True),
    A(300, 360, 880, 360, OK, 4, both=True),
    CHIP(590, 236, 'Asistente completo de CaribeMart', 22, '#fff', DOSC, anchor='middle', h=62, padx=26, icon='ia', isz=36)[0],
]
add_slide(42, 3, 'Síntesis', 'Síntesis de la parte tres: RAG simple y su lugar',
          'Fragmentar con solape, indexar con metadatos y combinar con AGENTS.md y MCP.',
          'Síntesis de la parte 3 · Dibujo propio',
          SVG(*b),
          'Cerramos la parte tres observando este triángulo de equilibrio que sostiene al asistente moderno de CaribeMart. En el vértice superior, AGENTS.md conserva vivas, cortas y visibles las normas estables de negocio y seguridad en cada sesión dentro de opencode [cite:8,9]. En el vértice inferior izquierdo, RAG simple limpia los manuales corporativos, fragmenta respetando encabezados con solape, indexa con metadatos claros y recupera únicamente los fragmentos pertinentes citando su origen exacto para frenar las alucinaciones [cite:10,11]. En el vértice inferior derecho, el protocolo MCP conecta las bases operativas en tiempo real y ejecuta cambios delicados bajo control humano. Con estas tres piezas claramente diferenciadas estamos listos para la parte cuatro: armaremos la arquitectura completa en opencode con permiso ask, analizaremos el caso real colombiano de Nequi, revisaremos el marco legal vigente y veremos el laboratorio B.')
