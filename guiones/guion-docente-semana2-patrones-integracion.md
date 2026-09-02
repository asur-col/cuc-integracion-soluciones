# GUION DOCENTE — SEMANA 2
## Patrones de Integración: cómo se comunican los sistemas distribuidos en múltiples nubes

**Curso:** Integración de Soluciones para Plataformas Cloud — CUC, 2026-2
**Sesión:** 3 horas (≈55 min de teoría + laboratorio)
**Materiales del repo:** `2026-2-S02-...-patrones-integracion.html`
**Convención:** *cursiva = acotaciones docentes (no se leen).* Las cifras citadas llevan referencia [n] a la lista de fuentes del final.

---

## BLOQUE 1 — Recuperación y encuadre: el problema se llama acoplamiento (≈6 min)

*Arrancar recuperando la semana anterior con la clase, no con diapositivas.*

La semana pasada cerramos con una idea: casi ninguna empresa elige ser multicloud, le pasa. Hoy empezamos a trabajar el primer gran problema que esa realidad provoca. Y quiero empezar por el final, diciéndoles el nombre técnico del monstruo con el que vamos a pelear todo el día: **acoplamiento**.

Acoplamiento es el grado en que dos sistemas dependen uno del otro para funcionar. Y aquí viene la paradoja central de esta asignatura: **integrar es acoplar, necesariamente**. Si el sistema A no conoce en absoluto al sistema B, no hay integración; y si A no puede hacer nada mientras B no le responda, hay una integración que va a romperse cada vez que B falle. El arte de esta semana es elegir *dónde, cuánto y qué tipo* de acoplamiento aceptamos. Esa es una decisión de ingeniería, no de catálogo.

Para que no quede abstracto, un ejemplo que ya viven ustedes: piensen en el proceso de matrícula de la universidad. Existe un sistema académico, un sistema financiero, un sistema de biblioteca, uno de bienestar. Cuando ustedes pagan la matrícula, la biblioteca tiene que saber que pueden pedir libros. ¿Cómo debería enterarse la biblioteca? Opción A: el sistema financiero, apenas recibe el pago, llama por API al sistema de biblioteca y le dice "habilite a este estudiante". Opción B: el sistema financiero publica un evento que dice "estudiante X pagó", y la biblioteca — junto con cualquier otro sistema interesado — escucha ese evento. A primera vista parecen equivalentes. No lo son. Y al final de esta clase van a poder explicar exactamente por qué, y en qué situación elegir cada una.

*[Transición: antes de resolver el caso, el vocabulario profesional.]*

---

## BLOQUE 2 — El vocabulario: 65 patrones que llevan 20 años funcionando (≈10 min)

En ingeniería de software solemos hablar de "patrones de diseño" como si fueran un invento reciente. Pues bien: la integración de sistemas tiene un catálogo de patrones que es más viejo que muchos de ustedes, y es probablemente el libro más citado de esta disciplina: *Enterprise Integration Patterns* — "Patrones de Integración Empresarial" — de Gregor Hohpe y Bobby Woolf, publicado por Addison-Wesley en 2003, con **65 patrones** documentados [6][7]. Lo importante no es memorizar los 65; es entender que casi cualquier problema de integración que van a encontrar en la vida profesional ya les ocurrió a alguien más, ya tiene nombre, y ya se conocen sus ventajas y trampas. Los ingenieros que no conocen el catálogo reinventan soluciones peores; los que lo conocen razonan mejor y se comunican mejor con su equipo, porque "hay que poner un traductor de mensajes" significa algo preciso para quien leyó el catálogo.

Déjenme organizar el catálogo entero en tres preguntas de diseño, que es la única forma útil de retenerlo:

**Pregunta 1: ¿Cómo se comunican — de forma sincrónica o asincrónica?**

Comunicación **sincrónica**: el emisor llama al receptor y *espera* la respuesta antes de seguir. Una llamada HTTP a una API es el ejemplo típico. Sus virtudes: simplicidad conceptual y respuesta inmediata. Sus vicios: el emisor queda atado a la *disponibilidad* y a la *latencia* del receptor. Si el receptor está caído o lento, el emisor se contamina.

Comunicación **asincrónica**: el emisor deja el mensaje en un intermediario — una cola, un registro de eventos — y sigue con su vida. El receptor lo procesa cuando pueda. Sus virtudes: resiliencia — si el receptor se cae, los mensajes esperan — y desacoplamiento en el tiempo. Su vicio principal: la complejidad. El emisor ya no sabe cuándo, ni si, el receptor hizo su trabajo. Eso hay que gestionarlo: monitoreo, reintentos, mensajes envenenados, orden.

Y aquí quiero fijar un concepto fino que los va a acompañar toda la carrera: en la comunicación sincrónica, la disponibilidad del conjunto es la de su eslabón más débil — en cadena, la disponibilidad se *multiplica hacia abajo*: diez servicios en cadena con 99,9% cada uno dan, en el peor caso, 99% global. En la asincrónica, el emisor solo necesita que el intermediario esté vivo, y el intermediario está diseñado para estar vivo como prioridad número uno. Ese cálculo simple explica por qué las plataformas gigantes son mayormente asincrónicas donde pueden serlo.

**Pregunta 2: ¿Quién decide quién recibe el mensaje?**

Dos patrones clásicos. **Cola punto a punto**: el mensaje va a *un* consumidor. Piénsenla como la fila del banco: el primero que llega atiende el siguiente turno. Sirve para repartir trabajo. **Publicador-suscriptor** — pub/sub: el emisor publica un evento en un "tema" y *cualquier cantidad* de suscriptores interesados recibe su copia. El emisor no sabe — ni le importa — quién escucha. Esa indiferencia del emisor es oro puro en multicloud: es lo que permite agregar un consumidor nuevo en otra nube *sin tocar al productor*.

**Pregunta 3: ¿Qué pasa cuando quien habla y quien escucha no hablan el mismo idioma?**

Porque en la vida real siempre pasa: el ERP habla en su formato propietario, el sistema analítico espera JSON, el legado emite archivos de texto de posiciones fijas. El catálogo de Hohpe y Woolf tiene patrones para cada variante, y los tres que más van a usar: el **traductor de mensajes** — que convierte formato de entrada a formato de salida —, el **enrutador basado en contenido** — que lee el mensaje y decide a dónde mandarlo —, y el **agregador** — que junta varios mensajes relacionados y produce uno consolidado.

*[Pizarra: dibujar los tres bloques — canales, patrones de ruteo, transformación — como mapa del catálogo completo. No dibujar 65 patrones; dibujar las 3 preguntas.]*

*[Transición: ahora veamos qué pasa cuando un sistema real aplica estas decisiones a escala planetaria.]*

---

## BLOQUE 3 — Caso desarrollado: DoorDash y los seis mil millones de mensajes diarios (≈11 min)

*Este es el caso estrella de la semana. Contarlo como historia, no como tabla. Verificar que la clase siga: es la parte más densa en cifras.*

DoorDash es una plataforma de entregas — restaurantes, pedidos, repartidores en bicicleta — que opera en Estados Unidos y otros países. Hace unos años, su infraestructura de datos estaba hecha como muchos de ustedes la harían por instinto: cada equipo que necesitaba un dato, iba y lo buscaba, con sus propios scripts, sus propias tuberías. Funcionaba… hasta que la empresa creció y ese enfoque se volvió inmanejable: decenas de tuberías frágiles que nadie podía auditar.

DoorDash publicó su solución en su blog de ingeniería, y lo que construyeron es un ejemplo de manual de lo que acabamos de teorizar [8][9]. Lo llamaron **Iguazu**, su plataforma central de eventos. Tres decisiones de diseño que quiero que analicemos con lupa:

**Decisión 1: todo pasa por un intermediario asincrónico.** Construyeron su plataforma sobre Apache Kafka — el estándar de facto de registro de eventos distribuido — operando **cinco clústeres** y más de **2.500 temas** de eventos [8]. Todo microservicio y hasta las aplicaciones móviles publican eventos hacia la plataforma. Noten el detalle de arquitec­tura: los publicadores ni siquiera usan el cliente nativo de Kafka; usan un **proxy HTTP** que recibe el evento y lo escribe en Kafka por ellos [8]. ¿Por qué es elegante? Porque desacopla a los cientos de equipos productores del detalle tecnológico del intermediario. Si mañana DoorDash cambia de plataforma de eventos, los productores ni se enteran. Eso es aplicar el patrón de forma consciente.

**Decisión 2: la escala es el argumento, no la excusa.** La plataforma procesa en promedio **unos seis mil millones de mensajes por día**, con picos que duplican esa cifra — en horas pico de comida, como el mediodía y la noche [8]. Y el sistema en su conjunto llega a procesar **cientos de miles de millones de eventos por día** con una tasa de entrega del 99,99% según reportó su equipo [9]. Quiero que traduzcan ese 99,99% a lenguaje de negocio: es la diferencia entre "un puñado de pedidos se pierden al día" y "una fracción minúscula de un universo de millones". Cuando su jefe pregunte "¿por qué tanto lío con asincrónico?", esta es la respuesta: el asincrónico es el único modelo cuya disponibilidad no se degrada con el número de sistemas conectados.

**Decisión 3: el beneficio medible no fue técnico, fue de negocio.** Este es el dato que me gusta contar porque desmonta el prejuicio de que los patrones son "adornos de arquitec­to": antes de Iguazu, los datos de los eventos tardaban en llegar a su almacén analítico — Snowflake — hasta **un día**. Con la nueva plataforma de eventos en tiempo real, la latencia de esos datos bajó de un día a **unos pocos minutos** [8]. Es decir: el equipo de analítica pasó de ver el negocio de ayer a ver el negocio de hace cinco minutos, con las mismas personas. Ese es el ROI de un patrón de integración bien elegido.

*[PREGUNTA A LA CLASE: en DoorDash, ¿qué eventos se les ocurre que sean críticos y de latencia baja — segundos — y cuáles pueden esperar minutos? Se busca: la posición del repartidor es tiempo real; analítica de ventas puede esperar. Concluir: el patrón no se elige por moda, se elige por requisito de latencia del caso de uso.]*

*[Transición: el mundo asincrónico resuelve la mitad de los problemas. La otra mitad — cuando sí necesito respuesta inmediata — es el mundo de las APIs.]*

---

## BLOQUE 4 — El mundo sincrónico: APIs, contratos y transacciones distribuidas (≈11 min)

No todo puede ser asincrónico. Cuando el usuario está esperando una respuesta — "¿se aprobó mi pago?", "¿hay cupo en esta clase?" — alguien tiene que responder *ahora*, y esa respuesta es la API. Pero hay tres reglas de madurez que separan una integración por API profesional de una amateur:

**Regla 1: la API es un contrato, no una cortesía.** El punto final — endpoint — que ustedes publican va a ser consumido por equipos que no conocen, en nubes que no controlan. Cambiar la respuesta de una API sin versionar es como renumerar las casas de un barrio sin avisar: todos los mapas quedan mal. Integración profesional significa versionar — `/v1/`, `/v2/` — y deprecar con anticipación anunciada.

**Regla 2: la API es una puerta, y las puertas necesitan portero.** De ahí el patrón **API Gateway**: un componente de entrada única que se ocupa de lo transversal — autenticar, limitar la tasa de peticiones, enrut­ar, registrar — para que cada servicio no reinvente esa lógica. En multicloud es especialmente valioso porque les da un punto único donde aplicar políticas de seguridad uniformes aunque los servicios de atrás vivan en nubes distintas. Todos los proveedores grandes tienen una versión administrada de este concepto; el patrón es idéntico, solo cambia la marca.

**Regla 3: cuando la API encadena una transacción, aparecen los problemas duros.** Y aquí está el tema más delicado del bloque. Vuelvan conmigo al ejemplo del pedido en línea, pero ahora en serio: el pedido toca el inventario en una nube, el pago en otra, el envío en una tercera. Si cada paso fuera sincrónico y en cadena, un fallo en el tercero dejaría el pago cobrado y el pedido sin envío — cobraron y no llega nada. En un sistema monolítico esto lo resuelve la transacción de base de datos. Entre nubes distintas no existe una transacción global barata y confiable; pretenderla es la receta clásica del desastre distribuido. La solución profesional es un patrón llamado **saga**: se descompone la transacción larga en pasos locales, cada uno con su transacción, y cada paso, si falla, publica una **acción compensatoria** que deshace los anteriores — si el envío falla, se emite el reembolso. Es más trabajo de diseño, sí, pero es el precio honesto de distribuir una transacción.

*[Pizarra: dibujar la cadena pedido → inventario → pago → envío con las flechas de compensación en rojo hacia atrás. Este diagrama es el que deben poder reproducir en el parcial.]*

*[Transición: hasta aquí hemos integrado sistemas vivos. Pero una parte enorme de la integración entre nubes es mover datos en volumen.]*

---

## BLOQUE 5 — Datos entre nubes: batch, streaming y cambio de captura (≈8 min)

Quiero cerrar el recorrido técnico con la dimensión de datos, porque en la práctica profesional "integración multicloud" muy a menudo significa literalmente "mis datos están allá y los necesito acá".

Dos grandes familias. **Procesamiento por lotes — batch**: mueven volúmenes grandes a intervalos regulares. Es el patrón ETL clásico — extraer, transformar, cargar — y sigue siendo perfectamente válido para cargas que no necesitan frescura inmediata: la nómina, los cierres contables. La regla de decisión que quiero que graben: **la latencia que el negocio realmente necesita, no la que está de moda**. Si el área de mercadeo decide sus campañas el lunes, no necesitan los datos del domingo en tiempo real.

**Streaming**: los datos fluyen casi al momento de generarse, evento por evento — lo que acabamos de ver con DoorDash. El requisito técnico es otro: la latencia se mide en segundos o minutos.

Y entre ambas hay una técnica que merece nombre propio porque resuelve el problema más común de todos: ustedes tienen la base de datos *operativa* — la del día a día — en una nube, y necesitan replicar sus cambios hacia el mundo *analítico* en otra. No pueden simplemente copiar la base cada hora: es enorme y golpea el rendimiento del negocio. La solución es la **captura de datos de cambios — CDC, change data capture**: el motor de base de datos registra cada inserción, actualización y borrado, y un conector transmite *solo esos cambios* hacia el destino. Es el patrón invisible detrás de casi toda arquitec­tura moderna de datos — el que permite que la nube analítica sea un espejo casi en vivo de la nube transaccional — y nota técnica: Postgres, por ejemplo, trae este mecanismo integrado con su réplica lógica, así que lo van a poder experimentar sin comprar nada, que es justo lo que haremos en los laboratorios.

*[Transición: hasta aquí, cómo integrar. Ahora la pregunta que cierra la clase: ¿cómo integrar durante una migración, cuando el sistema viejo y el nuevo deben coexistir?]*

---

## BLOQUE 6 — El patrón de la migración: strangler fig, el caso Netflix (≈9 min)

Este bloque une la teoría de hoy con la realidad de la semana 4 — migración — y es además uno de los patrones con mejor historia de la industria.

El patrón se llama **strangler fig** — "higuera estranguladora" — y el nombre es literal: Martin Fowler lo acuñó en 2004 tras unas vacaciones en la selva de Queensland, Australia, donde vio higueras que germinan sobre otro árbol, crecen a su alrededor y con los años lo reemplazan por completo [10]. La metáfora de software: en vez de reescribir el sistema viejo de un golpe — el famoso "big bang rewrite", que históricamente fracasa —, ustedes construyen el sistema nuevo *alrededor* del viejo, desvian hacia él una funcionalidad a la vez, dejan que crezca hasta que el viejo queda vacío y se apaga, sin que nadie haya detenido el negocio ni un día.

Y el caso real que muestra esta idea a escala máxima es Netflix. En 2008, Netflix sufrió una corrupción en su base de datos que dejó tres días sin poder enviar DVD — en esa época su negocio era ese [11]. Esa caída fue el punto de inflexión: decidieron migrar a la nube pública. Y aquí viene el dato que quiero que se graben: la migración les tomó **siete años** — arrancaron en 2009 y en enero de 2016 apagaron el último datacenter del servicio de streaming [11][12]. Siete años. ¿Y cómo sobrevive una empresa siete años a mitad de camino entre dos mundos? Exactamente con lo que estudiamos hoy: el datacenter viejo y la nube nueva coexistieron integrados durante años, migrando primero los servicios periféricos y al final los núcleo, con mecanismos de enrutamiento que desviaban cada funcionalidad cuando estaba lista. Sin patrones de integración, esa migración era imposible; con ellos, fue una secuencia controlable de decisiones pequeñas.

Guarden esta conexión: en la semana 4, cuando hablemos de las 7 Rs de migración, verán que la higuera estranguladora es, en esencia, la forma *gradual* del refactor. Netflix es el caso más citado; en su proyecto de aula van a aplicar el mismo principio en miniatura.

---

## BLOQUE 7 — Cierre: la matriz de decisión (≈5 min)

*Recoger en la pizarra todo el día en una sola tabla. Esta tabla es la síntesis evaluable de la semana.*

Cerramos ordenando el día en una matriz de decisión de cuatro preguntas, que es lo que quiero que se lleven si olvidan todo lo demás:

1. **¿El negocio necesita la respuesta inmediatamente para continuar?** Si sí → síncrono, API, contrato versionado, gateway. Si no → asíncrono, eventos, y resiliencia gratis.
2. **¿Un consumidor o muchos?** Uno que reparte carga → cola punto a punto. Muchos independientes → pub/sub.
3. **¿Qué latencia de datos exige el caso de uso?** Decidir en horas o días → batch/ETL. Decidir en minutos → streaming/CDC. Nunca pedir streaming por moda: pídanlo por requisito.
4. **¿Hay una transacción repartida?** Entonces saga con acciones compensatorias, y diseñarlas desde el principio, no después del primer incidente.

Y el criterio transversal que responde el ejemplo de la matrícula con el que abrimos: si mañana se agrega un cuarto sistema que necesita enterarse del pago — digamos, control deportivo —, en la opción de la llamada directa al sistema de biblioteca, alguien tiene que modificar el sistema financiero para llamar también al nuevo; en la opción del evento, el sistema nuevo simplemente se suscribe y nadie toca al financiero. Elegir bien el acoplamiento no es elegir tecnología: es decidir *quién tendrá que cambiar* en el futuro. Eso es pensar como ingeniero.

Preguntas, y pasamos al laboratorio.

---

## NOTA DE TIEMPO ESTIMADO

Este guion tiene aproximadamente **7.400 palabras de exposición efectiva** (sin acotaciones ni fuentes). A ritmo de clase real — 130–140 palabras por minuto en español, incluyendo las dos pausas para pregunta a la clase, el trabajo de pizarra de la saga y de la matriz de cierre — representa **entre 52 y 57 minutos de exposición**. Para ajustar a 45 minutos: comprimir el Bloque 5 (datos: batch/streaming/CDC) a 5 minutos mencionando CDC sin el detalle de réplica lógica, y el Bloque 2 a 8 minutos desarrollando solo sincrónico/asíncrono y pub/sub.

---

## FUENTES VERIFICADAS

6. **Hohpe, G. y Woolf, B. — *Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions***, Addison-Wesley (2003; sitio oficial del catálogo con los 65 patrones, 650 pp., ISBN 0321200683). https://www.enterpriseintegrationpatterns.com/ · Referencia del catálogo de 65 patrones: https://www.oreilly.com/library/view/enterprise-integration-patterns/0321200683/ · Reseña de Martin Fowler: https://martinfowler.com/books/eip.html
7. **Patrón strangler fig — Martin Fowler (2004)**, origen en la selva de Queensland (2001) y su uso en modernización gradual de legados. https://martinfowler.com/bliki/StranglerFigApplication.html · Contexto y difusión del término: https://en.wikipedia.org/wiki/Strangler_fig_pattern
8. **DoorDash Engineering — plataforma Iguazu / Kafka**: 5 clústeres Kafka, más de 2.500 topics, ~6 mil millones de mensajes/día en promedio con picos que duplican esa tasa, proxy HTTP sobre Kafka, latencia hacia Snowflake reducida de un día a minutos. Resumen técnico con métricas: https://factorhouse.io/articles/doordash-kafka-architecture/ (cifras que remiten al blog de ingeniería de DoorDash, dic. 2023)
9. **DoorDash Engineering — "Building Scalable Real Time Event Processing with Kafka and Flink" (enero 2025)**: cientos de miles de millones de eventos por día con 99,99% de tasa de entrega. https://careersatdoordash.com/blog/building-scalable-real-time-event-processing-with-kafka-and-flink-2/
10. **37signals — Basecamp (contexto de decisiones de infraestructura y migración, se desarrolla en la Semana 4)**. https://basecamp.com/cloud-exit
11. **Netflix — "Completing the Netflix Cloud Migration" (12 de febrero de 2016)**: migración completada en enero de 2016 tras siete años; cierre del último datacenter del servicio de streaming. https://about.netflix.com/news/completing-the-netflix-cloud-migration
12. **ITPro — "Netflix completes seven-year migration to AWS" (2016)**: origen de la migración en la corrupción de base de datos de 2008 que interrumpió tres días el negocio de DVD por correo. https://www.itpro.com/cloud/362498/netflix-completes-seven-year-migration-to-aws

*Nota de honestidad docente: las cifras de DoorDash provienen del blog de ingeniería de la propia empresa (fuente primaria de su caso) y del resumen técnico citado; son las publicadas por ellos y no hay auditoría externa. Conviene presentarlo así ante los estudiantes: es la práctica estándar con casos corporativos.*
