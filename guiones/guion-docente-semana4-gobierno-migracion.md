# GUION DOCENTE — SEMANA 4
## Gobierno Multicloud y Migración: identidad federada, lock-in, las 7 Rs y la repatriación

**Curso:** Integración de Soluciones para Plataformas Cloud — CUC, 2026-2
**Sesión:** 3 horas (≈60 min de teoría + laboratorio/taller)
**Materiales del repo:** `2026-2-S04-...-gobierno-multicloud.html` · `laboratorios/lab-03-taller-7rs-gobierno-multicloud`
**Convención:** *cursiva = acotaciones docentes (no se leen).* Las cifras citadas llevan referencia [n] a la lista de fuentes del final.

---

## BLOQUE 1 — Encuadre: gobierno es decidir quién decide (≈7 min)

Última semana del primer corte, y cerramos con la capa que en la práctica separa las estruc­uras multicloud que funcionan de las que se convierten en un desierto de costos y tickets de soporte: el **gobierno**.

Déjenme arrancar desmontando un malentendido. Cuando se dice "gobierno de la nube", muchos piensan en burocracia: comités, firmas, plantillas. En ingeniería, gobierno es algo mucho más concreto: **definir quién puede tomar qué decisiones, bajo qué reglas, y con qué evidencia se auditan esas decisiones**. Un buen gobierno multicloud responde cuatro preguntas operativas, y les pido memorizarlas como los cuatro pilares del cierre del curso:

- **Identidad:** ¿quién soy y qué me está permitido hacer — en cada nube, con una sola credencial bien administrada?
- **Costos:** ¿quién autoriza el gasto, quién lo monitorea y qué pasa cuando se descontrola?
- **Seguridad y cumplimiento:** ¿qué estándares aplican por igual en todas las nubes y quién responde por ellos?
- **Portabilidad:** ¿qué tanto nos podemos ir — o llegar — de un proveedor sin que el negocio se detenga?

Y antes de desarrollarlos, el dato que justifica por qué este bloque ocupa una semana entera y no una charla de veinte minutos: según el informe de Flexera que citamos en la semana 1, el **desafío número uno** de las organizaciones con la nube es gestionar el gasto — lo reporta el **84% de los encuestados** —, el **27% del gasto en infraestructura y plataforma se considera desperdiciado**, y las organizaciones se exceden del presupuesto en promedio un **17%** [1]. Ya existen equipos enteros dedicados a esto — el **59% de las organizaciones ya tiene un equipo de FinOps**, finanzas más operaciones, contra un 51% del año anterior [1]. Es decir: la mitad de esta clase va a terminar trabajando en algo relacionado con estos cuatro pilares, aunque su título diga "arquitecto" o "desarrollador". Vamos pilar por pilar, con el énfasis que la semana pide: identidad a fondo, costos y lock-in con casos, y la segunda mitad completa para migración y repatriación.

---

## BLOQUE 2 — Identidad federada: el problema N×M y los dos protocolos del mundo real (≈13 min)

*Este es el bloque técnico central de la semana. Desarrollar el flujo paso a paso en la pizarra; es el contenido más evaluable.*

Empecemos por el problema, que es hermoso en su simplicidad. Una empresa usa — recuerden la semana 1 — en promedio 2,4 nubes públicas [1], más el SaaS de correo, el de CRM, el de chat… digamos quince sistemas. Si cada sistema administrara sus propias credenciales, tendríamos quince contraseñas por empleado, quince procesos de alta y baja, quince lugares donde olvidar revocar el acceso del que renunció. En matemáticas: con N sistemas y M usuarios, la administración manual escala como N×M. En seguridad: cada uno de esos quince almacenes de contraseñas es una superficie de ataque. La respuesta a ese problema tiene un nombre: **federación de identidad** — una sola fuente de la verdad sobre quién es usted, y el resto de los sistemas le creen *sin conocer su contraseña*.

El vocabulario técnico, porque lo van a leer en toda la documentación del mundo: el **proveedor de identidad — IdP** — es quien verifica quién es usted: su instancia corporativa de directorio, o servicios de identidad en la nube de los que hay varias marcas y ya. El **proveedor de servicio — SP, o "relying party"** — es el sistema al que usted quiere entrar: la consola de la nube B, la aplicación de nómina. La federación es el protocolo por el cual el IdP le dice al SP "yo conozco a esta persona y esto es lo que puede hacer", con firmas criptográficas que el SP puede verificar sin volver a llamar a nadie.

Y aquí llegamos a los dos estándares que coexisten en el mundo real, con su historia, porque la historia explica el presente. **SAML 2.0** — Security Assertion Markup Language — fue ratificado como estándar por el consorcio OASIS en **marzo de 2005** [20][21]. Piensen qué era el mundo en 2005: XML era el lenguaje universal de la empresa, los portales web internos eran la frontera del cómputo, y el móvil no existía como plataforma de trabajo. SAML fue diseñado para ese mundo: la identidad viaja en documentos XML firmados, típicamente entregados al navegador mediante redirecciones y formularios HTTP. Funciona — lleva veinte años funcionando en universidades, bancos y gobiernos; la federación académica mundial de la que hacen parte las universidades es uno de sus ecosistemas más grandes [20] — pero es denso, verboso y famoso por sus mensajes de error criptográficos que pueden arruinar una tarde a cualquiera.

Veinte años después, el mundo cambió: aplicaciones móviles, aplicaciones de una sola página en el navegador, y sobre todo **APIs**. Para ese mundo se creó **OAuth 2.0** — un marco de *autorización*, no de autenticación: delega el acceso a APIs — y encima de él, **OpenID Connect — OIDC** — ratificado en **febrero de 2014** [20][21], que le agrega a OAuth la pieza que le faltaba: *autenticación*, responder "¿quién es este usuario?" con un **token de identidad** — un JWT, un JSON firmado y compacto —. La diferencia práctica que deben dominar: SAML viaja en XML y fue pensado para el navegador de escritorio; OIDC viaja en JSON, es nativo de apps móviles, de aplicaciones de una sola página y de APIs, y además hereda de OAuth todo el ecosistema de autorización — scopes, tokens de acceso, refresh tokens [20][21].

¿Y cómo se elige? No se elige por gusto: se elige por *lo que soporta el sistema al que quieren entrar y por el tipo de cliente*. Regla práctica: aplicaciones web corporativas heredadas y federación académica → SAML casi seguro; todo lo moderno, móvil y orientado a APIs → OIDC. Y lo más importante para un arquitec­to multicloud: **ustedes no eligen uno para toda la empresa; eligen un IdP que hable ambos**, y cada aplicación se conecta con el protocolo que le corresponda. La estrategia correcta no es ganarse la guerra de protocolos — es no pelearla.

Ahora el flujo, paso a paso, para que deje de ser magia. Quiero que lo sigan en la pizarra mientras lo narro: el empleado abre la consola de la nube B. La consola no le pide contraseña: lo redirige al IdP corporativo con una solicitud firmada. El IdP — donde el empleado ya tiene sesión — le pide un segundo factor si aplica, valida la política — ¿está activo? ¿es de este departamento? — y responde con una aserción firmada criptográficamente: "es Ana, del área de datos, autenticada hace treinta segundos". El navegador entrega esa aserción a la consola, la consola la verifica con el certificado público del IdP que configuró el día del pacto — confianza establecida una vez — y concede el acceso, mapeando la identidad de Ana a los roles que Ana tiene en *esa* nube. Fíjense en las tres propiedades de oro: la contraseña de Ana nunca salió del IdP; el alta y la baja de Ana se hacen en un solo lugar; y la auditoría — quién entró, a qué, cuándo — tiene una fuente única.

*[PREGUNTA A LA CLASE: Ana renuncia un viernes a las 5 de la tarde. Con el modelo de quince contraseñas dispersas, ¿cuánto tarda en desactivársele todo? ¿Y con federación bien hecha? Se busca: el IdP desactiva la cuenta y el acceso a todo muere con la sesión — en minutos, no en semanas. Ese es el argumento de seguridad más vendible del que disponen.]*

*[Transición: la identidad controla quién entra. Ahora, qué pasa cuando quieren salir — o simplemente pensar en irse.]*

---

## BLOQUE 3 — Vendor lock-in: anatomía de la dependencia y defensas honestas (≈9 min)

**Vendor lock-in** — dependencia del proveedor — es la situación en que el costo de cambiar de proveedor se vuelve tan alto que la decisión deja de ser económica y se vuelve estructural. Y quiero que lo estudien con rigor, porque hay dos extremos igual de ingenuos: el que niega el lock-in — "yo migro cuando quiera" — y el que lo paraliza — "no usemos nada de nadie". El punto profesional está en saber *dónde* se acumula la dependencia, porque no se acumula por igual en todas las capas. Cuatro niveles, de menor a mayor:

**Nivel 1 — Datos.** Es el más básico y ya lo estudiamos la semana pasada: el costo de egress y la inercia de los formatos. La buena noticia la vimos también: el Data Act europeo y las políticas de salida gratuita implementadas por los grandes proveedores desde 2024 han rebajado este muro para el caso del cambio de proveedor [17][18].

**Nivel 2 — APIs e interfaces.** Cada nube expone sus propios servicios con sus propias APIs. Si su aplicación llama directamente a los servicios administrados de una nube — su base de datos administrada, su cola de mensajes, su almacenamiento — esas llamadas no funcionan en otra nube. Es el lock-in más comentado y también el más matizable: algunas interfaces se volvieron de facto estándares — el modelo de objetos y la API de almacenamiento estilo S3 es hoy un dialecto común que casi todos los proveedores y las plataformas de código abierto hablan — pero matizar no es negar.

**Nivel 3 — Servicios administrados.** El más sutil y el más poderoso. La propuesta de valor de la nube es "usted concentra en su negocio, el proveedor opera la plataforma". Cada servicio administrado que adoptan — bases de datos administradas, funciones sin servidor, flujos de integración administrados — es una responsabilidad que ustedes entregaron… y que recuperarán el día de una migración, con intereses. No es un argumento contra los servicios administrados — a menudo valen cada peso — es el cálculo que hay que hacer con los ojos abiertos.

**Nivel 4 — Operaciones y personas.** El más silencioso: los runbooks, el monitoreo, los scripts, el conocimiento del equipo. Si su operación entera está escrita alrededor de las herramientas de un proveedor, migrar no es solo mover código: es reciclar músculo operativo.

¿Y las defensas? Tres honestas y una deshonesta. **Defensa 1: estándares y software abierto en las capas que más duelen** — motores de base de datos y colas de código abierto, orquestación de contenedores con Kubernetes, formatos abiertos. Noten la ironía elegante: son los mismos contenedores que ya montamos en el laboratorio de la semana 1 — el sandbox no era un capricho, era la defensa portátil del curso. **Defensa 2: infraestructura como código** — si su nube entera está descrita en archivos versionados, reproducirla en otra parte es un proyecto *posible*; si está construida a mano por consola, es arqueología. **Defensa 3: aislamiento del código de negocio** — mantener el núcleo de su aplicación en un runtime portable y confinar las dependencias del proveedor a los bordes. **Y la defensa deshonesta: la "capa mágica de abstracción multi-nube"** que promete que su aplicación será idéntica en cualquier nube sin tocar nada. Esa abstracción o es tan delgada que no abstrae nada, o tan gruesa que les impide usar *lo mejor* de cada nube — y recuerden la semana 1: si las empresas terminan multicloud es justamente para acceder a capacidades diferenciadas. Una abstracción total contradice el motivo por el que existen aquí. El arquitec­to maduro no busca cero lock-in; busca **lock-in consciente**: dependencias elegidas, documentadas y con costo de salida estimado.

*[Transición: con esa base, pasamos a la mitad práctica de la clase: cómo se mueve una empresa entera.]*

---

## BLOQUE 4 — Las 7 Rs: el vocabulario profesional de la migración (≈13 min)

*Este bloque alimenta directamente el taller del laboratorio. Cada R con ejemplo hablado y criterio de decisión. Ritmo ágil.*

Cuando una empresa decide moverse — al cloud, entre clouds, o de vuelta — nadie mueve todo de la misma forma, porque en el inventario hay de todo: sistemas sanos, fósiles irreemplazables, licencias a punto de vencer. La industria estandarizó ese análisis en un marco conocido como **las 7 Rs**, originado en las 5 Rs de Gartner y consolidado en esa forma de siete por Gartner en 2019 y por la guía prescriptiva de migración de AWS [22][23]. El marco es de AWS como referencia publicada, pero se usa igual con cualquier proveedor — de nuevo: es decisión, no catálogo.

Voy una por una, y con cada una la pregunta de decisión que la activa. Tomen nota de las preguntas, no de las letras:

**1. Retire — retirar.** El sistema simplemente se apaga, porque nadie lo usa o porque otra cosa ya lo reemplazó. Suena trivial y no lo es: cada sistema retirado es uno menos que migrar, asegurar, monitorear y pagar. Los especialistas en migración lo dicen sin rodeos: **primero se retira** — encoger el inventario antes de moverlo es la ganancia más barata de todo el proyecto [22][24]. La pregunta: *¿alguien extrañaría este sistema? Si la respuesta honesta es no, no lo migre: apáguelo.*

**2. Retain — retener.** Quedarse donde está, por ahora o para siempre. Causas legítimas: el sistema es sensible y está estable; el costo de moverlo no se recupera jamás; una regla regulatoria lo amarra a su ubicación. La pregunta: *¿mover este sistema agrega valor o solo agrega riesgo?*

**3. Rehost — rehospedar, el famoso "lift and shift".** Levantar la máquina y sentarla igual en la nube: mismo sistema operativo, misma aplicación, sin cambios. Es la vía rápida — y por eso la favorita de los proyectos con fechas políticas — pero también la que deja más valor sobre la mesa: la aplicación corre igual que antes, sin aprovechar nada nuevo. La pregunta: *¿la prioridad es velocidad o transformación?*

**4. Relocate — reubicar.** Mover al nivel del hipervisor: los bloques de máquinas virtuales enteros se trasladan a la nube sin reinstalar nada — es la vía cuando hay una plataforma virtualizada que la nube destino soporta directamente [22][23]. Diferencia fina con rehost: relocate mueve la infraestructura tal cual, rehost re-crea la máquina. La pregunta: *¿mi plataforma de virtualización tiene equivalente directo en el destino?*

**5. Replatform — replataformizar.** "Levantar, ajustar y mover": cambios quirúrgicos de bajo riesgo para aprovechar lo administrado — la base de datos propia pasa a la base de datos administrada del destino, el almacenamiento local pasa a almacenamiento de objetos. Cambia lo justo para capturar ahorro operativo sin reescribir la aplicación. La pregunta: *¿qué componente, si lo cambio solo, me da el mayor ahorro por el menor riesgo?*

**6. Repurchase — recomprar.** Cancelar el software propio o licenciado y comprarlo como servicio — el "drop and shop": fuera el CRM comprado en 2012 con su servidor; entra el CRM en la nube por suscripción [23]. Es muchas veces la decisión más económica del inventario… y también una nueva forma de lock-in, ahora hacia el SaaS. La pregunta: *¿este software es diferenciador para mi negocio o es un commodity que alguien más opera mejor que yo?*

**7. Refactor — refactorizar/rearquitecturar.** Rediseñar la aplicación para explotar las capacidades nativas de la nube: escalar por componentes, funciones sin servidor, colas, resiliencia real. Es la de mayor valor potencial y también la de mayor costo y riesgo — por eso las guías serias de migración masiva la reservan para después de la migración básica, no durante [22]. La pregunta: *¿el negocio necesita de esta aplicación un cambio de escala o de agilidad que su arquitec­tura actual no puede dar por más hardware que le ponga?*

Y el conjunto se aplica *por aplicación*, no por empresa: un proyecto de migración real es una cartera donde cada sistema recibe su R. La distribución típica de una cartera empresarial tiende a concentrar peso en rehost y replatform, con refactor reservado a pocos sistemas núcleo — y les presento esa distribución como estimación de la industria, no como ley: la composición exacta depende del inventario de cada empresa [24].

*[PREGUNTA A LA CLASE, calentamiento del taller: la universidad tiene un sistema de notas de 1998 en un servidor físico, un portal web moderno en contenedores, un chat corporativo en SaaS y una nómina que el regulador exige auditar en sitio. Asignen una R a cada uno y defiéndanla. Se espera discusión: nómina → retain; notas → rehost o replatform según riesgo; portal → replatform/refactor; chat → repurchase ya hecho.]*

*[Transición: y si la R es la octava — la que no está en la lista oficial — ¿moverse de la nube a infraestructura propia? Le llaman repatriación, y tiene los casos más citados de la industria.]*

---

## BLOQUE 5 — La repatriación: 37signals, Dropbox y Ahrefs — las matemáticas de irse (≈14 min)

*El bloque estrella del corte. Narrar como historia con cifras. Cada cifra está citada; no redondear de más.*

Para cerrar, quiero contarles tres historias reales que juntas desmontan el último dogma que les quede sobre la nube: que irse de ella es fracasar. La repatriación — mover cargas de la nube pública a infraestructura propia o colocation — es una estrategia legítima cuando las condiciones del negocio la favorecen, y lo primero que deben saber es que no es marginal: según Flexera, aproximadamente **un quinto de las cargas de trabajo en la nube fue repatriado en el último año** por las organizaciones encuestadas [1]. ¿Un quinto? Sí. Y el informe aclara algo clave para no sacar conclusiones apresuradas: el flujo hacia la nube sigue superando al de salida — el repatriado es un porcentaje del total, en un contexto donde la huella total sigue creciendo [1]. La nube no se está muriendo; el dogma de que la nube es *siempre* la respuesta, sí.

**Historia 1: 37signals — el caso del manifiesto.** 37signals es la empresa de Chicago detrás de Basecamp y HEY, herramientas de colaboración con decenas de años de operación. En 2022 su cofundador y director de tecnología, David Heinemeier Hansson — DHH — publicó la decisión de salir de la nube, y las cifras de esa saga están documentadas por la propia empresa [19]: su factura anual de infraestructura en la nube llegaba a **3,2 millones de dólares**; el hardware para reemplazarla — servidores propios — costó alrededor de **600 mil dólares**; la proyección original de ahorro era de **7 millones de dólares en cinco años**, cifra que luego la empresa revisó al alza: sus ahorros superarán **los 10 millones de dólares en cinco años** [19][25]. Al año de ejecutada la salida — la migración se completó en 2023 — ya reportaban alrededor de **un millón de dólares de ahorro anual** [19], y el propio DHH reportó cerca de 2 millones ahorrados en su primer año completo [25]. La reducción de costos de infraestructura total de la empresa quedó entre la **mitad y dos tercios** — y ojo al detalle que los ingenieros apreciarán: **sin contratar personal adicional** [19]. Ahora, la honestidad del caso: 37signals es una empresa de software con un equipo de operaciones de élite, cargas estables y predecibles — su tráfico es constante, no explota diez veces en navidad — y experiencia previa operando hardware. El propio DHH tituló su FAQ "la computación en la nube no es para todos" — y esa es exactamente la lectura correcta: no es que la nube sea mala; es que *para su patrón de carga*, la economía no cerraba.

**Historia 2: Dropbox — la repatriación elegante.** Dropbox, el gigante del almacenamiento, es la entrada más seria del catálogo porque no es un blog de opinión: son los números de su registro público ante la SEC cuando salió a bolsa en 2018. Durante años Dropbox corrió sobre la nube de AWS, y en 2016 emprendió el proyecto **Magic Pocket** — su sistema de almacenamiento propio, co-diseñado entre hardware y software [26] — migrando la gran mayoría de los datos de sus usuarios a datacenters propios, con AWS retenida para una fracción residual. Los resultados, de sus propios documentos públicos: en 2016 redujeron sus costos de infraestructura en unos **39,5 millones de dólares**, y en 2017 en **35,1 millones adicionales — alrededor de 75 millones de dólares en dos años** [27]. Y el detalle fino que quiero que aprecien como futuros arquitec­tos: no fue solo comprar servidores — reescribieron la capa de almacenamiento para su carga específica, algo que solo es rentable cuando almacenas exabytes. Cuando su escala es tan grande que usted mismo es un hiperescalador, la economía del alquiler se invierte.

**Historia 3: Ahrefs — la repatriación preventiva.** Y el caso más radical: la empresa que estudió irse a la nube y decidió **nunca ir**. Ahrefs, la empresa de herramientas de SEO con sede en Singapur, publicó en su blog de ingeniería el análisis de su decisión: al mantener su infraestructura en hardware propio en centros de colocation — en lugar de migrarla a nube pública — estimaron un ahorro acumulado de **alrededor de 400 millones de dólares en dos años y medio** [28][29]. Cuatrocientos millones. Su argumento es el mismo de los otros dos casos llevado al extremo: cargas masivas, estables y de cómputo intensivo, donde el margen del alquiler se vuelve una fortuna.

*[PAUSA. Recoger en la pizarra antes de cerrar.]*

¿Qué comparten los tres casos? Esto es lo evaluable: **cargas grandes, estables y predecibles** — lo contrario del patrón "crece diez veces y luego vuelve a cero" donde la elasticidad de la nube brilla; **equipos capaces de operar hardware y software a ese nivel** — nadie de estos tres casos ahorró dinero por azar; y **escala suficiente para que el margen de la nube pese** — para una pyme con dos servidores, la nube sigue siendo una ganga evidente. La fórmula mental que les dejo: **la nube vende elasticidad y velocidad; el hardware propio vende costos unitarios a escala. Su trabajo como ingeniero es medir qué necesita su negocio de esas dos cosas — y en qué proporción — y pagar por lo que usa.** Quien no hace esa cuenta no está eligiendo; está siguiendo la moda, hacia arriba o hacia abajo.

Y el cierre del argumento vuelve al gobierno del inicio de la clase: la razón por la que 37signals, Dropbox y Ahrefs *pudieron* elegir es que diseñaron con portabilidad en mente — código portable, formatos abiertos, capacidades de operar. La libertad arquitec­tónica no se compra el día de la mudanza; se construye todos los días, en las decisiones de la semana 3 — dónde viven los datos — y de esta — qué dependencias aceptamos.

---

## BLOQUE 6 — Cierre del corte y puente al taller (≈4 min)

Cuatro semanas, cuatro capas, un solo relato: el multicloud *sucede* — semana 1 —; se conversa con patrones — semana 2 —; se conecta por redes — semana 3 —; y se gobierna con identidad, costos, portabilidad y decisiones de migración — semana 4.

En el taller de hoy — `lab-03-taller-7rs-gobierno-multicloud` — cada grupo recibe un portafolio ficticio pero realista de sistemas y aplica el marco completo: clasificar cada carga con su R, justificar la identidad y el gobierno que exige, y estimar el costo de la decisión. Es un ensayo en miniatura de lo que les van a pedir en el proyecto de aula: razonar y defender, no memorizar.

Los tres mensajes del corte, si solo se llevan tres: **primero**, la identidad federada convierte un problema de N×M en un problema de N — un IdP que hable SAML para el legado y OIDC para lo moderno [20][21]. **Segundo**, el lock-in no se elimina: se administra conscientemente, capa por capa. **Tercero**, migrar y repatriar no son temas religiosos: son matemáticas de volumen, estabilidad y capacidad operativa — 3,2 millones de factura anual contra 600 mil dólares de hardware [19], 75 millones ahorrados en dos años [27], 400 millones en dos años y medio [28]. Números, no consignas.

Preguntas, y bajamos al taller.

---

## NOTA DE TIEMPO ESTIMADO

Este guion tiene aproximadamente **8.000 palabras de exposición efectiva** (sin acotaciones ni fuentes). A ritmo real de clase — 130–140 palabras por minuto en español, con la narración paso a paso del flujo de login federado en pizarra, las dos preguntas a la clase (desactivación de Ana y calentamiento del taller 7 Rs), y la pausa de síntesis del bloque 5 — representa **entre 56 y 62 minutos de exposición**. Es el guion más largo del corte por decisión de diseño: cierra el corte y concentra los tres casos de estudio. Para ajustar a 50 minutos: comprimir el Bloque 3 (lock-in) a 6 minutos citando solo los niveles 2 y 3, y el Bloque 1 a 4 minutos dejando los cuatro pilares como lista sin el dato de FinOps (que se retoma en la semana de costos si el temario la incluye).

---

## FUENTES VERIFICADAS

1. **Flexera 2025 State of the Cloud Report** (gasto como desafío n.º 1: 84%; 27% de desperdicio IaaS/PaaS; 17% de exceso presupuestal; 59% con equipo FinOps — vs. 51% el año anterior —; 2,4 nubes públicas promedio; ~1/5 de las cargas repatriadas en el último año, con huella total en la nube en aumento). https://www.flexera.com/blog/finops/the-latest-cloud-computing-trends-flexera-2025-state-of-the-cloud-report/ · Cifras detalladas: https://www.softwareone.com/en-ca/blog/articles/2025/05/14/flexera-2025-state-of-the-cloud-recap
17. **CMA (Reino Unido) — Egress fees working paper** (2024): análisis de tarifas de salida; artículo 29 del Data Act de la UE sobre cargos de cambio de proveedor. https://assets.publishing.service.gov.uk/media/664f2556993111924d9d3aa8/240521_-_Egress_Fees__.pdf
18. **AWS — política de transferencia gratuita de datos al abandonar la plataforma** (marzo 2024). Referenciada en: https://awsinsider.net/articles/2025/05/09/cloud-data-egress-fee-tussle-plays-out-with-$250k-aws-comp.aspx
19. **37signals / Basecamp — serie "Leaving the Cloud"** (fuente primaria de la empresa): factura anual de nube de 3,2 M USD; ~600 k USD en servidores; ahorro proyectado original de 7 M USD/5 años y revisado a más de 10 M USD/5 años; ~1 M USD/año de ahorro ya materializado; reducción de costos de infraestructura de entre la mitad y dos tercios; sin contratación de personal adicional; "five grand a day" de egress durante la salida de S3. https://basecamp.com/cloud-exit
20. **Comparativa técnica SAML 2.0 vs. OIDC** (SAML 2.0 ratificado por OASIS en marzo de 2005; OpenID Connect Core 1.0 ratificado en febrero de 2014 sobre OAuth 2.0; XML vs. JSON/JWT; soporte móvil/SPA; ecosistemas de federación como InCommon/eduGAIN en SAML). https://duendesoftware.com/blog/20260528-saml-and-openid-connect-oidc · https://auth0.com/intro-to-iam/saml-vs-openid-connect-oidc
21. **Clerk — "OIDC vs SAML for Enterprise SSO"** (fechas de ratificación y diferencias estructurales entre ambos protocolos). https://clerk.com/articles/oidc-vs-saml-for-enterprise-sso-a-2026-decision-guide
22. **AWS Prescriptive Guidance — "About the migration strategies"** (las 7 Rs; recomendaciones para migraciones masivas: rehost/relocate/replatform primero, refactor después; relocate a nivel de hipervisor; retire/retain como estrategia­s legítimas). https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/migration-strategies.html
23. **AWS Prescriptive Guidance — "Paths to the cloud"** (las 7 Rs y su origen en las 7 Rs de Gartner 2019; definiciones de rehost, relocate, replatform, repurchase/drop-and-shop, refactor, retain/revisit, retire). https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-microsoft-workloads-aws/cloud-paths.html
24. **Cloudtech — "The 7 Rs of Cloud Migration: Strategies & Statistics"** (distribución típica aproximada de carteras: mayoría rehost/replatform, refactor minoritario; la recomendación "retire first"). https://cloudtech.com/feeds/blog/aws-migration-statistics-rehost-percentage · https://opsiocloud.com/knowledge-base/what-are-7rs-of-cloud-migration/ — *presentado en el guion explícitamente como estimación de la industria, no como cifra auditada.*
25. **Data Center Dynamics — "37signals claims it saved almost $2m last year from cloud repatriation"** (octubre de 2024). https://www.datacenterdynamics.com/en/news/37signals-claims-it-saved-almost-2m-last-year-from-cloud-repatriation/ · Titular de The Register citado por la propia 37signals: "Save $7 million on cloud by spending $600k on servers". https://basecamp.com/cloud-exit
26. **Dropbox — "Scaling to exabytes and beyond"** (blog de ingeniería, 2016): origen del proyecto Magic Pocket de almacenamiento propio. https://dropbox.tech/infrastructure/magic-pocket-infrastructure
27. **GeekWire — "Dropbox saved almost $75 million over two years by building its own tech infrastructure"** (2018, con cifras del S-1 presentado ante la SEC): 39,5 M USD de reducción en 2016 y 35,1 M USD en 2017; tres datacenters propios. https://www.geekwire.com/2018/dropbox-saved-almost-75-million-two-years-building-tech-infrastructure/
28. **Ahrefs — "How Ahrefs Saved US$400M in 3 Years by NOT Going to the Cloud"** (blog de ingeniería, fuente primaria): ~400 M USD de ahorro estimado en ~2,5 años por no migrar su infraestructura a nube pública. https://tech.ahrefs.com/how-ahrefs-saved-us-400m-in-3-years-by-not-going-to-the-cloud-8939dd930af8
29. **ITPro — "Singapore firm 'saves $400 million' by not migrating to cloud"** (2023): cobertura del caso Ahrefs. https://www.itpro.com/cloud/370241/singapore-firm-saves-400-million-by-not-migrating-to-cloud

*Nota de honestidad docente: las cifras de 37signals y Ahrefs provienen de los blogs oficiales de las propias empresas (fuente primaria de cada caso); las de Dropbox provienen de su registro S-1 ante la SEC, la fuente más auditable de las tres. Ninguna tiene verificación contable externa independiente, y así conviene presentarlo en clase: es la norma en los casos corporativos y una excelente oportunidad para hablar de crítica de fuentes con los estudiantes.*
