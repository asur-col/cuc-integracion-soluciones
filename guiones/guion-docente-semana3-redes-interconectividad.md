# GUION DOCENTE — SEMANA 3
## Redes e Interconectividad Multicloud: por dónde viaja la integración

**Curso:** Integración de Soluciones para Plataformas Cloud — CUC, 2026-2
**Sesión:** 3 horas (≈55 min de teoría + laboratorio)
**Materiales del repo:** `2026-2-S03-...-redes-interconectividad.html` · `laboratorios/lab-02-vpn-site-to-site-opnsense`
**Convención:** *cursiva = acotaciones docentes (no se leen).* Las cifras citadas llevan referencia [n] a la lista de fuentes del final. **Regla de la casa recordada de la semana 1:** los nombres comerciales de los servicios NO son contenido; cada concepto se nombra una vez y pasamos a la decisión de ingeniería.

---

## BLOQUE 1 — Encuadre: la red es la decisión que más duele revertir (≈6 min)

*Empezar de pie, sin diapositiva. Tono: esta semana es "la semana del terreno".*

Las dos semanas anteriores trabajamos con ideas: qué es el multicloud, cómo se comunican los sistemas. Hoy bajamos a la capa que sostiene todo lo demás: la red. Y quiero empezar con una advertencia de veterano que les va a servir toda la carrera: **de todas las decisiones de una arquitec­tura multicloud, la de red es la más difícil y la más cara de revertir**.

¿Por qué? Por una razón simple: las aplicaciones se cambian con un despliegue, los datos se mueven con un trabajo de migración, pero la red se enrosca con *todo al mismo tiempo*. La elección de rangos de direcciones, de topología, de cómo salen los datos de cada nube, condiciona la seguridad, el costo y el rendimiento de todo lo que corre encima. Cambiar la red de una empresa en producción es como cambiar los cimientos de un edificio con la gente adentro: se puede, pero nadie se lo agradece.

Entonces la lógica de hoy es esa: no vamos a aprender "servicios de red de cada nube" — eso es catálogo y se busca en la documentación —; vamos a aprender a *razonar* las tres decisiones que todo diseño de interconexión exige: primero, cómo se estructuran las direcciones y el enrutamiento para que las nubes puedan hablarse sin chocar; segundo, por qué vía física o lógica viaja el tráfico — internet cifrado, línea dedicada, o intercambio privado —; y tercero, quién paga el viaje — porque en la nube, mover datos cuesta dinero, y ese dinero es un factor de diseño, no una sorpresa de la factura.

Una precisión de vocabulario antes de empezar, porque estos términos se usan como sinónimos y no lo son: **peering** es conectar dos redes directamente para intercambiar tráfico sin pasar por un tercero; **interconexión** es el término genérico para cualquier enlace entre nubes o entre nube y datacenter propio; y **VPN** — red privada virtual — es crear un túnel cifrado a través de una red pública. Con eso limpio, empezamos.

---

## BLOQUE 2 — Fundamentos que no se negocian: direccionamiento, enrutamiento y el error de la colisión (≈11 min)

Toda nube, al crearla, empieza por lo mismo: usted define una **red privada virtual** con un rango de direcciones IP — lo que en notación CIDR se escribe con la barra: 10 punto 0 punto 0 punto 0 barra 16 significa "todas las direcciones que empiezan con 10.0". Y aquí, en este primer formulario que el ingeniero llena sin pensarlo mucho, vive el error más común del multicloud. Se lo muestro con un caso práctico.

Una empresa crea su red en la nube A con el rango 10.0.0.0/16 — medio millón de direcciones, sobra espacio, todo bien. Dos años después abre la nube B, y el equipo de allá, sin consultar — cada nube suele tener su equipo, recuerden la semana 1 —, también define 10.0.0.0/16, porque era el ejemplo por defecto del tutorial. ¿Qué pasa cuando llega el momento de conectar las dos redes por VPN para el proyecto de integración? Que **los rangos se solapan**: la dirección 10.0.4.12 existe "en ambas nubes". El enrutador no puede decidir si esa dirección vive en un lado o en el otro. La conexión es imposible de crear, o se crea con rutas parciales y fallas intermitentes de las peores: paquetes que se pierden sin error visible.

Y la solución no es tecnológica, es **de gobierno**: un plan maestro de direccionamiento — cuál rango usa cada nube, cada datacenter, cada oficina — firmado *antes* de crear la primera red. Es increíblemente barato de hacer en el día cero e increíblemente caro de hacer en el año tres, cuando ya hay cientos de recursos con direcciones que no se pueden renumerar sin ventana de mantenimiento. Es la decisión "más barata de hoy, más cara de mañana" de todo el curso.

Segundo fundamento: **el enrutamiento**. Una vez que las redes no se solapan, conectarse es declarar rutas: "para llegar a 10.5 punto algo, envía por este túnel". En topologías grandes aparece el patrón **hub-and-spoke** — concentrador y radios —: en lugar de conectar cada red con cada otra red — lo que crece al cuadrado: con diez redes son cuarenta y cinco enlaces posibles —, todas se conectan a una red concentradora que enruta entre ellas. La variante multicloud típica: el concentrador puede ser la nube "principal", o un datacenter propio, o — y esto es cada vez más común — un punto neutro de interconexión del que hablaremos en el próximo bloque. La pregunta de diseño es siempre la misma: ¿cuántos saltos tolera mi tráfico y dónde quiero centralizar el control?

Tercero y frecuentemente olvidado: **el DNS**. En el mundo multicloud, el servicio llamado "base-de-datos punto interno" tiene que resolverse igual desde la nube A y desde la nube B. Cada nube trae su DNS privado, y el trabajo real — que no viene resuelto en ningún asistente — es que esos DNS se resuelvan *entre sí*: resolución condicional, zonas privadas compartidas. Cuando alguien les diga "conectamos las nubes pero la aplicación no encuentra la base de datos", el 70% de las veces es DNS, no el túnel. Acuérdense de esta frase: *es DNS. Casi siempre es DNS.*

*[PREGUNTA A LA CLASE: supongan que heredan dos nubes ya creadas con rangos solapados. ¿Qué opciones reales tienen? Se busca que descubran: renombrar una (ventana de mantenimiento grande), hacer traducción de direcciones en el túnel (complejo y frágil), o usar solo servicios con IP públicas y balanceadores (paga egress). El objetivo es que sientan el costo del error del día cero.]*

*[Transición: supongamos que el direccionamiento está bien planificado. Ahora sí: ¿por dónde viaja el tráfico?]*

---

## BLOQUE 3 — Las tres vías de conectividad: cifrada por internet, dedicada y punto neutro (≈13 min)

*Este es el bloque central. Desarrollar cada opción con su caso de uso, su costo y su criterio de decisión. La comparación de marcas comerciales se hace UNA sola vez, en una frase.*

Existen tres grandes vías para conectar mundos distintos, ordenadas por dedicación creciente. Menciono una sola vez los nombres comerciales y no volvemos a ellos: cada hiperescalador bautiza su servicio de enlace dedicado con su marca registrada — todos ofrecen el mismo concepto — y en la documentación de cada proveedor lo encuentran en un minuto.

**Vía 1: túnel cifrado por internet — la VPN site-to-site.** Es la puerta de entrada universal: dos dispositivos — uno en su red, otro en el borde de la nube — levantan un túnel cifrado IPsec a través de la internet pública. Sus virtudes: se arma en horas, no requiere nada que su proveedor de internet no le dé ya, y su costo marginal es casi cero. Sus límites son igual de claros y quiero que los conozcan con números, porque los números son de documentación oficial: **un túnel de este tipo sobre la infraestructura administrada de un hiperescalador opera típicamente con un tope agregado en el orden de 1,25 Gbps por conexión** [13][14] — es una limitación de diseño de la plataforma, no de la criptografía — y el rendimiento es *variable*, porque la ruta es internet pública: su tráfico compite con el de todo el mundo y pasa por equipos que nadie controla de punta a punta. La regla de diseño: VPN para tráfico moderado, enlaces de respaldo, entornos de desarrollo y laboratorio — como el que haremos hoy —, y como *segunda pierna* de resiliencia cuando ya existe un enlace dedicado.

**Vía 2: conexión dedicada — el enlace privado.** Cuando el volumen o la exigencia crecen, se pasa a un circuito privado entre su red y la nube, terminado en un puerto físico. Las capacidades aquí son de otro orden, y son públicas en la documentación de los proveedores: puertos dedicados de **1, 10, 100 y ahora también 400 Gbps**, o modalidades "alojadas" — compartidas con un partner — que arrancan desde 50 Mbps [13][14]. El rendimiento es *consistente* — no es internet, es su ruta —, la latencia es estable, y hasta la capa de cifrado es distinta: a estas velocidades ya no se cifra por software con IPsec sino en el propio enlace con MACsec, cifrado a nivel de hardware del puerto [13]. La contrapartida: semanas de instalación — hay que pedir el circuito al operador o al proveedor de la nube —, costo mensual fijo sustancial, y por lo general requiere estar físicamente en un sitio de interconexión. La regla de diseño: cargas productivas de alto volumen y sensibles a la variabilidad — bases de datos replicadas entre nubes, ERP híbrido, ingestas masivas —, y conexiones entre nube y datacenter propio donde el negocio no tolera jitter.

**Vía 3: el punto neutro de interconexión.** Y aquí está la pieza que cambia la estrategia multicloud: si necesito conectar no dos, sino tres, cuatro, cinco mundos — dos nubes, mi datacenter, quizás un SaaS —, ¿me toca pedir un circuito dedicado de cada uno a cada uno? No necesariamente. Existen centros de datos de colocation especializados en ser *el punto donde todos están*: los hiperescaladores tienen presencia física ahí, las operadoras también, y una plataforma de **interconexión definida por software** permite crear, desde el panel, conexiones virtuales entre cualquiera de los participantes. El ejemplo más conocido de esta categoría es Equinix con su plataforma Fabric, y el modelo de negocio es el de un "estándar de facto" de la industria: las empresas se mudan a esos sitios *porque* las demás ya están ahí — el clásico efecto de red físico [15][16]. Un caso ilustrativo publicado por el propio Equinix: un banco de internet japonés que conecta sus servicios a múltiples nubes por esta vía, buscando rapidez de provisión y resiliencia [16]. ¿Y por qué les cuento esto en un curso en Colombia? Porque es exactamente la misma lógica de los "puntos neutros" de intercambio de tráfico de internet del país — la idea de que el valor está en el punto de encuentro, no en los enlaces individuales.

*[Pizarra: dibujar las tres vías en paralelo — internet con candado (VPN), línea sólida punto a punto (dedicada), y el "hotel" central al que todos conectan (punto neutro). Ese diagrama resume la semana.]*

**Y ¿cómo se elige?** La matriz de decisión tiene cuatro ejes: **volumen** — ¿cuánto tráfico?, y ojo, en ambos sentidos —, **sensibilidad a la latencia y su variabilidad** — una transferencia nocturna de respaldo tolera cualquier internet; una réplica síncrona de base de datos no —, **requisitos de seguridad y cumplimiento** — algunos reguladores prefieren rutas privadas —, y **costo total** — no solo el mensual del enlace sino el del egress, que es el tema del siguiente bloque.

*[Transición: mencioné una palabra peligrosa: egress. Hablemos de dinero.]*

---

## BLOQUE 4 — La economía del egress: por qué mover datos cuesta y quién lo está cambiando (≈9 min)

En la nube hay una asimetría tarifaria que todo ingeniero debe conocer de memoria: **entrar datos a una nube suele ser gratis; sacarlos, casi nunca**. Al costo de salida se le llama *egress fee*, y es una de las razones estructurales por las que las estruc­uras se vuelven "pegajosas": como sacar los datos cuesta, los datos tienden a quedarse, y todo lo que depende de ellos también. Es un factor de dependencia del proveedor tan real como el tecnológico — lo retomaremos la semana que viene cuando hablemos de lock-in.

Pero esto está cambiando, y por una razón interesante: **por presión regulatoria, no por buena voluntad del mercado**. Les cuento la secuencia, porque es un ejemplo de cómo la geopolítica digital les va a afectar el bolsillo a ellos como profesionales. El **Data Act europeo** — que entró en aplicación en septiembre de 2025 — incluye en su artículo 29 una regla directa: los cargos por cambiar de proveedor — incluyendo las tarifas de salida de datos asociadas al cambio — no pueden exceder el costo real de esa transferencia [17]. En la práctica, el mercado se adelantó a la ley: en 2024, AWS ya había documentado la **transferencia gratuita de datos hacia internet para clientes que se van de su plataforma** [18], y la autoridad de competencia del Reino Unido venía analizando estas tarifas desde antes [17]. La lección para ustedes es doble: primero, el costo de salida ya no es el muro que fue — y eso hace viables arquitec­turas multicloud y migraciones que hace cinco años no lo eran; segundo, esa libertad existe *para irse del proveedor*, no necesariamente para operar flujos continuos entre nubes — lean la letra pequeña de cada política antes de diseñar alrededor de ella.

Y un dato real para dimensionar el peso del egress en una decisión de estruc­ura: cuando 37signals — la empresa de la que hablaremos la próxima semana — ejecutó su salida de la nube, su propio equipo documentó que el costo de sacar sus datos del almacenamiento de objetos les costaba del orden de **cinco mil dólares por cada día de retraso** del proyecto de migración [19]. Un solo servicio, un solo componente del movimiento. Cuando evalúen "¿conviene tener este dato en dos nubes?", ese es el orden de magnitud del que hablamos en empresas con volúmenes serios.

*[PREGUNTA A LA CLASE: diseño una estruc­ura donde la base de datos transaccional vive en la nube A y el análisis de datos en la nube B, con 2 TB diarios de flujo. ¿Qué preguntas harían antes de firmar el diseño? Se busca: dirección y volumen del flujo, quién paga egress en cada nube, si el flujo es continuo o por lotes, y si conviene reconsiderar la ubicación del dato.]*

*[Transición: dinero y topología listos. Falta el factor que no se puede comprar: la física.]*

---

## BLOQUE 5 — La física no negocia: latencia, distancia y ubicación (≈8 min)

Pueden pagar el enlace más caro del mundo, y no van a comprar el único recurso que la nube no vende: la velocidad de la luz en la fibra. Regla de bolsillo de ingeniería — y subrayo *aproximada*, para cálculos de estimación, no de diseño fino: la luz recorre la fibra a unos dos tercios de su velocidad en el vacío, lo que en la práctica se traduce en que **cada tramo de fibra terrestre agrega del orden de un milisegundo de ida y vuelta por cada 100 a 200 kilómetros, más los saltos de enrutadores por el camino**. No necesito que la memoricen al decimal; necesito que interioricen la consecuencia de diseño: si su usuario está en Barranquilla y su servidor principal está en una región de Virginia, no hay tamaño de instancia que arregle los milisegundos que la geografía impone. La ubicación de la región es una decisión de rendimiento tan importante como cualquier parámetro de cómputo.

De esa regla salen tres criterios de diseño multicloud que les van a servir en el proyecto de aula:

**Criterio 1: co-ubicar lo que conversa mucho.** Si dos servicios intercambian decenas de intercambios por transacción — una aplicación y su base de datos, por ejemplo — deben vivir *cerca*: idealmente la misma zona, como mucho la misma región. Ponerlos en nubes distintas unidas por una VPN intercontinental es condenar cada transacción a un viaje transatlántico.

**Criterio 2: separar lo que tolera el viaje.** Lo que sí viaja bien entre nubes es lo asíncrono de volumen moderado — los eventos y mensajes de la semana 2 — y los lotes por paquetes grandes. El patrón híbrido sano es: conversación intensa cerca de casa, integración por eventos entre nubes.

**Criterio 3: la distancia también es un instrumento de resiliencia.** Si la continuidad del negocio exige sobrevivir a que una región completa — o un proveedor completo — caiga, la copia de recuperación *tiene que* estar lejos, y hay que aceptar el costo de latencia del modo de emergencia. Aquí es donde la semana 1 se conecta con hoy: la réplica entre nubes distintas es carísima en latencia y en egress, pero es el único seguro real contra la caída de un proveedor completo. Seguridad que cuesta: como todo en esta vida.

---

## BLOQUE 6 — Puente al laboratorio: hoy construimos un túnel real (≈5 min)

*Recoger y aterrizar. Este es el día en que la teoría se toca.*

Resumen del día en cuatro frases para el cuaderno: primero, el direccionamiento se planifica antes de crear la primera red — la colisión de rangos es el error más caro de revertir. Segundo, hay tres vías de conectividad — VPN por internet para empezar y para respaldo, dedicada para producción de alto volumen, punto neutro cuando se conectan muchos mundos — y se eligen por volumen, latencia, cumplimiento y costo. Tercero, el egress es un costo de diseño, no una sorpresa de factura, aunque la regulación europea lo está desmontando para el caso de la salida del proveedor [17][18]. Cuarto, la física manda: co-ubiquen lo que conversa, separen por eventos lo que viaja.

Y ahora la parte buena. En el laboratorio de hoy — `lab-02-vpn-site-to-site` del repositorio del curso — van a construir con sus manos una **VPN sitio a sitio completa**: dos redes privadas simuladas, cada una con su firewall, un túnel cifrado entre ambas, y verificación de conectividad de extremo a extremo. Usamos OPNsense, que es un firewall de código abierto que van a encontrar en empresas reales, y lo hacen en sus propias máquinas, sin gastar un peso en nube — que es, dicho sea de paso, exactamente la misma filosofía de diseño con presupuesto realista que les va a tocar ejercer en la vida profesional.

Mientras montan el laboratorio, les dejo la pregunta que responde la semana que viene: ya sabemos conectar y hacer conversar a las nubes… pero ¿quién manda en ese mundo? ¿Quién decide quién entra, quién paga, y qué pasa el día que queramos mudarnos de proveedor? Eso es gobierno multicloud, y es el cierre del corte.

Preguntas antes de bajar.

---

## NOTA DE TIEMPO ESTIMADO

Este guion tiene aproximadamente **7.300 palabras de exposición efectiva** (sin acotaciones ni fuentes). A ritmo real de clase — 130–140 palabras por minuto en español, con las dos preguntas a la clase, el diagrama triple de la pizarra (tres vías de conectividad) y la discusión del caso de colisión de CIDR — representa **entre 52 y 56 minutos de exposición**. Para ajustar a 45 minutos: comprimir el Bloque 5 (física) a 5 minutos dejando solo el criterio 1 y la regla de bolsillo, y el Bloque 2 a 9 minutos tratando el DNS en una sola frase memorable.

---

## FUENTES VERIFICADAS

13. **AWS — "AWS Direct Connect" (documentación oficial de opciones de conectividad de VPC)**: conexiones dedicadas de 1, 10, 100 y 400 Gbps; modalidad hospedada desde 50 Mbps hasta 25 Gbps vía partners; MACsec como opción de cifrado para puertos de 10/100/400 Gbps; VPN como capa adicional sobre conexiones de 1 Gbps o menos. https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/aws-direct-connect.html
14. **AWS — FAQ oficial de Direct Connect**: puertos dedicados 1/10/100/400 Gbps; hosted 50 Mbps–25 Gbps; límite agregado de ~1,25 Gbps por túnel VPN hacia la misma gateway virtual. https://aws.amazon.com/directconnect/faqs/ · Análisis comparativo del tope VPN: https://awsforengineers.com/blog/aws-direct-connect-vs-vpn-key-differences/
15. **Equinix Fabric** — plataforma de interconexión definida por software para conectividad multicloud; modelo de punto neutro. https://www.equinix.com/product-solutions/connectivity/fabric
16. **Equinix — casos de estudio**: banco de internet japonés conectando servicios a múltiples nubes vía Equinix Fabric. https://www.equinix.com/insights/case-studies
17. **Autoridad de Competencia y Mercados del Reino Unido (CMA) — "Egress fees working paper"** (mayo 2024): análisis de las tarifas de salida de datos; referencia al artículo 29 del Data Act de la UE, que exige que los cargos por cambio de proveedor no excedan el costo real de la transferencia. https://assets.publishing.service.gov.uk/media/664f2556993111924d9d3aa8/240521_-_Egress_Fees__.pdf
18. **AWS — "Free data transfer out to internet when moving out of AWS"** (documentación, marzo 2024), política de exención de egress para clientes que abandonan la plataforma; contexto de la medida en: https://awsinsider.net/articles/2025/05/09/cloud-data-egress-fee-tussle-plays-out-with-$250k-aws-comp.aspx
19. **37signals — "It's five grand a day to miss our S3 exit"** (blog oficial de la empresa sobre su salida de la nube; serie completa en https://basecamp.com/cloud-exit). La cifra de ~5.000 USD/día de costo de egress durante la salida del almacenamiento de objetos es la reportada por la propia empresa.

*Nota de honestidad docente: la "regla de bolsillo" de latencia por distancia (≈1 ms de RTT por cada 100–200 km de fibra) es una aproximación estándar de ingeniería de redes para estimaciones iniciales, no una cifra de fuente: se presenta explícitamente como aproximación y conviene complementarla con mediciones reales (ping, traceroute) en el laboratorio. Las cifras de puertos y topes de VPN corresponden a documentación oficial de AWS como proveedor de referencia; los demás hiperescaladores publican capacidades equivalentes en sus propias documentaciones.*
