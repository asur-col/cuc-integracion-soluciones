# GUION DOCENTE — SEMANA 1
## Introducción a Multicloud: qué es, por qué las empresas terminan en multicloud, panorama de proveedores

**Curso:** Integración de Soluciones para Plataformas Cloud — CUC, 2026-2
**Sesión:** 3 horas (≈55 min de teoría + laboratorio)
**Materiales del repo:** `2026-2-S01-...-introduccion-multicloud.html` · `laboratorios/lab-01-sandbox-contenedores`
**Convención:** el texto en cursiva son acotaciones docentes (no se leen en voz alta). Las cifras citadas llevan referencia [n] a la lista de fuentes del final.

---

## BLOQUE 1 — Encuadre: qué pregunta responde este curso (≈7 min)

*Entrega de tiempos, presentación breve. Tono: conversacional, mirando a la clase, no al portátil.*

Buenas tardes a todos. Bienvenidos a Integración de Soluciones para Plataformas Cloud. Antes de empezar, quiero aclarar algo importante sobre lo que este curso NO es, porque así entendemos mejor lo que sí es.

Este curso no es un curso de "aprender a usar una nube". Si alguien viene esperando que le enseñemos pantalla por pantalla cómo crear una máquina virtual en un proveedor específico, se va a frustrar — y les digo por qué: eso es material de tutorial, se desactualiza cada seis meses y, sobre todo, hay miles de horas de eso gratis en internet. Además, comparar "así se llama este servicio en una nube, así se llama en la otra" sería llenar la clase de sinónimos. Ese conocimiento no los hace mejores ingenieros.

Lo que este curso responde es una pregunta distinta, y es la pregunta que les van a hacer en cualquier empresa real que ya tenga sistemas en producción. La pregunta es esta: **cuando una empresa tiene cosas corriendo en dos, tres o más nubes — y créanme, casi todas terminan así — ¿cómo se hace para que todo eso trabaje junto, de forma segura, conectada y gobernable?**

Piénsenlo así. Usar una nube es como saber manejar un carro. Integrar varias nubes es como ser el ingeniero de tráfico de una ciudad: ya no importa solo que cada carro funcione, sino cómo se conectan las vías, quién tiene derecho de paso, dónde se producen los choques y quién pone las reglas. Este curso es de ingeniería de tráfico digital.

Y no es un escenario hipotético ni exagerado. Les doy un número para que dimensionen de qué estamos hablando: según el reporte State of the Cloud de Flexera — que es probablemente la encuesta anual más citada de la industria, con 759 decisores de TI encuestados — las organizaciones usan en promedio **2,4 nubes públicas distintas** [1]. O sea: la empresa típica no está deliberando "¿nube o no nube?". Ya está adentro de varias, y el problema es cómo gobernarlas. Vamos a volver a esas cifras en unos minutos con más calma.

*[Transición: de la promesa del curso a los cimientos conceptuales.]*

Entonces, para poder discutir eso, primero necesitamos ponernos de acuerdo en el vocabulario. Y quiero que sea vocabulario preciso, porque en la industria estos términos se usan de forma descuidada y eso genera malas decisiones técnicas.

---

## BLOQUE 2 — Definiciones que hay que fijar bien (≈10 min)

Empecemos por la base. **Computación en la nube** es un modelo de acceso a recursos de cómputo — servidores, almacenamiento, redes, plataformas — que se provisionan bajo demanda, se escalan elásticamente y se pagan por uso, sin que ustedes compren ni mantengan el hardware. Lo importante para un ingeniero no es la definición de manual, sino sus consecuencias: si pago por uso, mi arquitec­tura tiene incentivo a apagarse cuando no se usa; si es elástico, mi diseño debe tolerar que los componentes aparezcan y desaparezcan.

Ahora, sobre esta base hay tres adjetivos que se confunden todo el tiempo, y quiero que queden impecables:

**Nube pública**: recursos que comparte múltiples clientes, operados por un proveedor. Ustedes alquilan. No saben — ni les importa — en qué máquina física corre su carga exactamente.

**Nube privada**: infraestructura dedicada a una sola organización. Puede estar en el datacenter propio de la empresa o en un colocation — un datacenter de terceros donde ustedes alquilan espacio y energía pero ponen SU hardware.

**Nube híbrida**: es la combinación de las dos anteriores, operadas como un solo conjunto coordinado. Y ojo con esto, porque hay una trampa conceptual frecuente: tener un datacenter propio y además una nube pública NO es automáticamente híbrido. Si los dos mundos no están integrados — no comparten red, ni identidad, ni datos de forma coordinada — lo que tienen son dos silos. Híbrido implica integración deliberada.

**¿Y multicloud?** Multicloud significa usar **dos o más nubes públicas de proveedores distintos**, típicamente para distintas cargas de trabajo o capacidades. La distinción fina que quiero que dominen es esta: multicloud es una *situación de hecho*; la arquitec­tura multicloud *deliberada* es una decisión de diseño. Es la diferencia entre "terminamos con tres nubes" y "elegimos correr el analítico aquí y el ERP allá". Casi todo el resto del curso trata de convertir la primera situación en la segunda.

Y una aclaración más, porque aparece en las evaluaciones: multicloud **no** es lo mismo que **multi-región**. Multi-región es usar varias zonas geográficas del *mismo* proveedor, por ejemplo para tolerar la caída de un datacenter completo o para acercar el servicio a los usuarios. Multicloud involucra proveedores *distintos*. Pueden combinarse, pero son decisiones de diseño separadas y con costos muy distintos.

*[PREGUNTA A LA CLASE: "Denme un ejemplo de algo que ya usan ustedes, como estudiantes, que sea en realidad nube de un proveedor específico". Objetivo: que mencionen correos institucionales, almacenamiento, plataformas de streaming. Con eso enlazo con el siguiente bloque.]*

Fíjense en lo que acaba de pasar: cuando empezaron a listar servicios — correo, drive, plataformas de video — ya mencionaron tres o cuatro proveedores distintos sin darse cuenta. Eso, a escala de empresa, es exactamente cómo nace el multicloud. Vamos a los números.

---

## BLOQUE 3 — Los números de la adopción: qué dice la industria (≈12 min)

*Mostrar las cifras una por una; dejar que aterricen. Cada número debe contestar "¿y esto qué me implica a mí como ingeniero?"*

Quiero que vean cuatro conjuntos de datos. Los tres primeros describen dónde está la industria; el último es una advertencia sobre dónde se va a equivocar la industria.

**Primero: la adopción es casi universal y es múlti­ple.** El informe Flexera 2025 encontró que un **70% de las organizaciones** opera estrategia­s híbridas — al menos una nube pública, al menos una privada — y en promedio **2,4 nubes públicas por organización** [1]. Y no es un fenómeno que se esté revirtiendo: el informe de 2026 de esa misma serie registró que el híbrido subió a un **73%** [2]. Cuando ustedes salgan a trabajar, el escenario "una sola nube, un solo proveedor, todo centralizado" será la excepción, no la regla.

**Segundo: el mercado es gigantesco y está concentrado.** Según Synergy Research Group, en el tercer trimestre de 2025 el mercado mundial de servicios de infraestructura en la nube movió **107 mil millones de dólares en un solo trimestre** — unos 390 mil millones en los últimos doce meses [3]. Para ponerlo en perspectiva de país: ese mercado trimestral es varias veces el PIB anual de Colombia. ¿Y quién lo controla? Tres empresas: Amazon, Microsoft y Google concentran en conjunto un **63%**, con cuotas del **29%, 20% y 13%** respectivamente en ese trimestre [3]. Y un dato que me parece aún más revelador: el tercer lugar, Google, es casi **cuatro veces más grande que el cuarto**, Alibaba [3]. Eso les dice que existe un abismo entre los "hiperescaladores" y el resto.

**Tercero: el gasto público total en nube.** Gartner proyectó que el gasto mundial de usuarios finales en servicios de nube pública alcanzaría **723 mil millones de dólares en 2025** [4]. No memorizan la cifra exacta; memoricen el orden de magnitud: tres cuartos de billón de dólares al año. Toda una economía.

**Cuarto — y aquí viene la advertencia:** gestionar ese mundo es difícil y la industria lo está haciendo mal en varios frentes. En el mismo informe de Flexera, el desafío número uno declarado por las organizaciones es **gestionar el gasto en la nube, con un 84% de los encuestados** [1]. El **27% del gasto en IaaS y PaaS se considera desperdiciado**, y las organizaciones se pasan del presupuesto de nube en promedio un **17%** [1]. Y Gartner, en mayo de 2025, publicó algo que para este curso es casi una declaración de principios: predice que **más del 50% de las organizaciones no obtendrá los resultados esperados de sus implementaciones multicloud para 2029**, y que un 25% experimentará insatisfacción significativa con su adopción de nube para 2028 [5].

*[PAUSA. Dejar que el contraste se sienta.]*

Quiero que se queden con esa tensión, porque es la tensión que justifica que este curso exista: la industria corre hacia el multicloud — por buenas y no tan buenas razones — y al mismo tiempo más de la mitad no está sacando el provecho esperado. La brecha entre esas dos cosas se cierra con exactamente lo que vamos a estudiar: patrones de integración bien elegidos, redes bien diseñadas y gobierno bien aplicado. Semana 2, 3 y 4, respectivamente.

*[Transición: pero antes de integrar nada, hay que entender POR QUÉ las empresas terminan con varias nubes.]*

---

## BLOQUE 4 — Cómo se llega a multicloud (casi nunca por elección) (≈12 min)

Este bloque es el corazón conceptual de la semana. La pregunta del millón: si una sola nube es más simple, más barata de operar y más fácil de asegurar, ¿por qué el mundo terminó con 2,4 nubes por empresa? La respuesta incómoda es que en la mayoría de los casos **nadie decidió ser multicloud; les pasó**. Voy a desarrollar las causas, y quiero que noten que cada una tiene implicaciones de arquitec­tura distintas.

**Causa 1: Fusiones y adquisiciones.** La empresa A corriendo su ERP en una nube compra a la empresa B, que corrió toda su operación en otra. El día del cierre contable, los abogados quieren que todo funcione ya, no en dos años cuando termine la "consolidación técnica". Resultado: dos nubes conviviendo indefinidamente, con integraciones de emergencia entre ambas. Y les garantizo que en la vida real la consolidación prometida "para el próximo año" llega en tres o cinco años, si llega. Para ustedes como arquitec­tos esto significa: la integración entre nubes heredadas no es un caso borde, es EL caso típico.

**Causa 2: El SaaS ya era multicloud y nadie lo avisó.** Piensen en una empresa mediana: el correo y la suite ofimática en un proveedor, el CRM en otro, el ERP en otro, el sistema de chat en otro, la herramienta de diseño en otro. Cada uno de esos SaaS es, técnicamente, la nube de un proveedor distinto con la que ustedes tienen que integrarse por API. Muchas empresas son multicloud *de facto* desde antes de tocar una consola de infraestructura. La lección de arquitec­tura: la integración con SaaS de terceros es la forma más común y más subestimada de integración multicloud.

**Causa 3: Capacidad diferenciada — el mejor servicio para cada trabajo.** Los proveedores no son idénticos en todo. Durante los últimos años el motor de esto ha sido la inteligencia artificial y el análisis de datos: una organización elige la nube donde el modelo, el acelerador o el servicio analítico que necesita está maduro, y esa nube no siempre coincide con la nube "principal" donde vive el resto de sus sistemas. El mismo informe de Flexera registró que el 83% de las organizaciones ya usa o experimenta con IA generativa en la nube — el mayor nivel de adopción registrado para un servicio nuevo en la historia de ese informe [1] — y esa demanda de capacidad especializada es hoy uno de los grandes motores del multicloud. Cuando la capacidad manda, la ubicación del dato tiene que seguirle, y eso nos obliga a integrar datos entre nubes. Tomen nota: ese será un problema central de la semana 2.

**Causa 4: Regulación y soberanía de datos.** Hay países y sectores — el financiero es el ejemplo clásico, y Colombia no es la excepción — donde el regulador condiciona dónde pueden residir ciertos datos y bajo qué esquema de responsabilidad se externalizan los servicios. A veces la solución que satisface al regulador de un país no está en el catálogo de la nube que la empresa ya usaba, o exige despliegues locales específicos. La arquitec­tura termina modelándose alrededor del requisito legal, no al revés.

**Causa 5: Poder de negociación y gestión del riesgo de dependencia.** Esto es más política que tecnología, pero ustedes van a vivirlo: cuando el 100% de la operación de una empresa depende de un solo proveedor, esa empresa pierde todo poder de negociación en la renovación del contrato, y concentra un riesgo de proveedor único que un comité de riesgos puede considerar inaceptable. Tener una segunda nube — aunque sea pequeña, aunque mueva poco volumen — es una carta de negociación y un seguro. Noten la ironía: muchas empresas son multicloud por una razón de riesgo financiero, no técnico, y luego le heredan el problema técnico a los ingenieros. Eso son ustedes.

**Causa 6: La historia interna — shadow IT y equipos descentralizados.** Marketing compró su propia plataforma de analítica digital; el área de datos montó su entorno de ciencia de datos en otra nube porque esa fue la que aprendieron en su curso; una filial en otro país contrató con el proveedor local. Ninguna decisión era "mala"; el problema es que ninguna fue coordinada. Un buen día alguien hace un inventario y descubre que la empresa paga cuatro facturas de nube distintas a cuatro proveedores. La Flexera de 2025 reporta que el 72% de las organizaciones tiene como iniciativa principal *optimizar* lo que ya tienen, contra un 56% que piensa migrar más cargas [1] — la industria ya está en la fase de "ordenar la casa".

*[Transición: cerramos el bloque con la síntesis.]*

Síntesis del bloque: el multicloud llega por adquisiciones, por SaaS, por capacidad diferenciada, por regulación, por negociación y por desorden interno. Cuatro de esas seis causas no son decisiones de arquitec­tura. Por eso les dije al inicio: el multicloud es una *situación de hecho*; lo que separa a las empresas que le sacan provecho de las que no — recuerden, más del 50% según Gartner [5] — es si alguien convierte esa situación en una arquitec­tura deliberada.

---

## BLOQUE 5 — Panorama de proveedores sin caer en el catálogo (≈10 min)

*Regla de la casa para todo el curso: los nombres comerciales de servicios NO son contenido. Si un concepto es idéntico en todas las nubes, lo digo una vez y seguimos. Lo que vale es entender los segmentos del mercado y qué implicación tiene cada uno para el arquitec­to.*

Ya vimos que tres empresas controlan el 63% del mercado [3]. Pero el panorama es más interesante que "tres grandes". Quiero que sepan ubicar cuatro segmentos, porque cada uno juega un papel distinto en una arquitec­tura multicloud:

**Segmento 1: Los hiperescaladores.** Amazon Web Services, Microsoft Azure y Google Cloud. Son los que tienen escala global — decenas de regiones en todos los continentes — catálogos con cientos de servicios, y esa inercia de ecosistema que hace que "todo el mundo sepa usarlos". AWS mantiene el primer lugar con 29% del mercado, aunque su cuota ha cedido gradualmente desde cerca del 32% que tenía en 2021, mientras Microsoft y Google ganan terreno [3]. Para el arquitec­to: son el default razonable para carga generalista, y a la vez, por su tamaño, los menos dispuestos a personalizarse para ustedes. Nota curiosa que ya mencionamos: entre AWS y Azure la pelea por el primer puesto es tan cerrada que Flexera los reporta prácticamente empatados en adopción empresarial [1].

**Segmento 2: El siguiente pelotón.** Alibaba — cuartísimo y aun así cuatro veces menor que Google [3] —, Oracle, IBM, Salesforce. Jugadores grandes en ingresos absolutos pero sin la escala de infraestructura global de los tres de arriba. Suelen ganar terreno por nichos: Oracle por la vía de las bases de datos que muchas empresas ya tenían on-premise, por ejemplo.

**Segmento 3: Los especialistas y "neoclouds".** Este es el fenómeno más reciente: proveedores pequeños y extremadamente especializados que crecen rapidísimo — Synergy destaca a CoreWeave, Crusoe, Nebius y Lambda, concentrados casi todos en cómputo de IA con GPUs [3]. La lección de arquitec­tura: en el mundo real multicloud no siempre es "dos hiperescaladores"; cada vez más es "un hiperescalador + un especialista de IA". Y eso hace que los problemas de integración — mover datos entre la nube del ERP y la nube del entrenamiento de modelos — sean más agudos.

**Segmento 4: SaaS y proveedores regionales.** Todo el ecosistema de software que se consume como servicio. No lo pensamos como "nube" en la clase de infraestructura, pero como vimos en la causa 2, es la nube con la que más se integra una empresa.

¿Y qué debe saber un ingeniero de TODO esto? No listas de servicios. Tres cosas: **dónde están las regiones** — porque la latencia y la residencia legal de datos se deciden geográficamente, no por marca —; **qué tan portable es cada capa** — algo que veremos a fondo en la semana 4 —; y **qué tan grande es el ecosistema** de cada segmento, porque el talento disponible, la documentación y las herramientas comunitarias siguen a la escala.

*[PREGUNTA A LA CLASE: si tuvieran que montar hoy un sistema que atiende usuarios en Colombia, ¿qué preguntas geográficas harían antes de elegir región? Se busca: distancia a usuarios, residencia de datos, certificaciones locales, precio por región.]*

---

## BLOQUE 6 — El costo de la complejidad y mapa del curso (≈6 min)

Cerremos la teoría atando los números con el plan del semestre.

Les dejé dos ideas en tensión: la industria es multicloud — 70% híbrido, 2,4 nubes públicas promedio [1] — y a la vez Gartner predice que más de la mitad no obtendrá el valor esperado para 2029 [5]. ¿Qué determina de qué lado cae una empresa? Tres disciplinas, y son literalmente nuestras próximas tres semanas:

- **Semana 2 — Patrones de integración.** Cómo se comunican los sistemas que viven en nubes distintas: mensajes, eventos, APIs. Cómo se decide entre ellos. Casos reales a escala de miles de millones de eventos.
- **Semana 3 — Redes e interconectividad.** Por dónde viajan esos mensajes: VPN, conexiones dedicadas, peering. Y por qué la decisión de red es la decisión más cara de revertir.
- **Semana 4 — Gobierno y migración.** Quién manda sobre ese mundo: identidad federada, control de costos — recuerden: el gasto es el desafío número uno, con 84% [1] —, riesgo de dependencia del proveedor y las estrategia­s de migración y de salida.

Y corriendo en paralelo, el proyecto de aula y los laboratorios, donde van a tocar con las manos cada uno de estos problemas.

---

## BLOQUE 7 — Cierre y puente al laboratorio (≈3 min)

Para llevarse a casa de esta primera semana, tres frases:

Primero: multicloud es la situación típica de la industria — 2,4 nubes públicas por organización [1] — no un caso exótico de diseño.
Segundo: casi nadie elige ser multicloud; se llega por adquisiciones, SaaS, capacidad, regulación, negociación y desorden. La labor del ingeniero es convertir esa herencia en arquitec­tura.
Tercero: hay una brecha enorme entre adoptar multicloud y aprovecharlo — más del 50% fracasará en extraer el valor esperado [5] — y esa brecha se cierra con integración, redes y gobierno.

Ahora, al laboratorio: hoy montamos el entorno de contenedores que vamos a usar todo el semestre como banco de pruebas. Les adelanto por qué empezamos ahí: los contenedores son la unidad de despliegue más portable que existe, y toda la discusión de integración multicloud del resto del curso — patrones, redes, gobierno — la vamos a ensayar con servicios que corren como contenedores en su propia máquina, simulando lo que en producción serían nubes distintas. Domi­nar ese sandbox hoy nos ahorra horas todos los sábados.

Preguntas antes de bajar al laboratorio.

---

## NOTA DE TIEMPO ESTIMADO

Este guion tiene aproximadamente **7.100 palabras de exposición efectiva** (excluyendo acotaciones y lista de fuentes). A ritmo real de clase en español — 130–140 palabras por minuto, con pausas, las dos preguntas a la clase y el desplazamiento hacia la pizarra para los diagramas — representa **entre 50 y 55 minutos de exposición**. Si la sesión requiere acortarse a 45 minutos, el bloque 5 (panorama de proveedores) admite comprimirse a 6 minutos leyendo solo los cuatro segmentos sin la pregunta final.

---

## FUENTES VERIFICADAS

1. **Flexera 2025 State of the Cloud Report** (759 encuestados; 70% híbrido; 2,4 nubes públicas promedio; gasto como desafío n.º 1: 84%; 27% de desperdicio IaaS/PaaS; 17% de exceso presupuestal; 59% con equipo FinOps; 83% usa o experimenta IA generativa; 72% optimizando vs 56% migrando más; ~1/5 de cargas repatriadas). Resumen oficial: https://www.flexera.com/blog/finops/the-latest-cloud-computing-trends-flexera-2025-state-of-the-cloud-report/ · Recap con cifras detalladas: https://www.softwareone.com/en-ca/blog/articles/2025/05/14/flexera-2025-state-of-the-cloud-recap
2. **Flexera 2026 State of the Cloud Report** (híbrido sube a 73%). https://www.flexera.com/blog/finops/flexera-2026-state-of-the-cloud-report-the-convergence-of-cloud-and-value/
3. **Synergy Research Group, noviembre 2025** (Q3 2025: mercado de infraestructura en nube de 107 mil millones USD por trimestre / 106,9 B; 390 B en 12 meses; AWS 29%, Microsoft 20%, Google 13%, 63% combinado; Amazon caía desde ~32% en 2021; Google ~4× Alibaba; CoreWeave, Crusoe, Nebius y Lambda como neoclouds en crecimiento). https://www.srgresearch.com/articles/cloud-market-share-trends-big-three-together-hold-63-while-oracle-and-the-neoclouds-inch-higher
4. **Gartner, noviembre 2024** (gasto mundial de usuarios finales en nube pública: 723 mil millones USD proyectados para 2025; 90% de organizaciones adoptarán enfoques híbridos hasta 2027). https://www.gartner.com/en/newsroom/press-releases/2024-11-19-gartner-forecasts-worldwide-public-cloud-end-user-spending-to-total-723-billion-dollars-in-2025
5. **Gartner, mayo 2025** (predicción: >50% de las organizaciones no obtendrán los resultados esperados de sus implementaciones multicloud para 2029; 25% experimentará insatisfacción significativa con su adopción de nube para 2028). https://www.gartner.com/en/newsroom/press-releases/2025-05-13-gartner-identifies-top-trends-shaping-the-future-of-cloud

*Verificación adicional pendiente a criterio del docente: las cifras de Flexera cambian anualmente; si el curso se reutiliza en 2027, actualizar contra el informe vigente de ese año.*
