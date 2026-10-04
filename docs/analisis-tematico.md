# Análisis temático y técnico — Integración de Soluciones para Plataformas Cloud (2026-2)

**Fase 1 — Análisis.** Documento para aprobación del Ing. Rodolfo Cañas Cervantes antes de producir.
**Fecha del corte de análisis:** domingo 4 de octubre de 2026.
**Insumos revisados:** `index.html` (calendario oficial), las 6 presentaciones HTML publicadas, sus PDF y videos, `guiones/` (S01–S04), `proyectos/`, `STANDARDS.md`, `TEMARIO-…md` y `CLAUDE.md`.
**Método:** cada diapositiva se renderizó a 1280×720 con Chromium (Playwright). Se contaron diapositivas y visuales con un script, se detectaron SVG recortados (`getBBox` > `viewBox`) y textos encima del pie, y se midió la duración de los videos con `ffprobe`. Las capturas no se versionan; se regeneran con `herramientas/` en la Fase 2.

> Los títulos de las semanas del calendario de `index.html` son oficiales y **no cambian**. Las mejoras propuestas van **dentro** de cada semana.

---

## 1. Dónde estamos en el calendario

| Hoy | Semana del calendario | Qué sigue |
|---|---|---|
| Dom 4-oct-2026 | **Termina la semana 9** (28 sep–4 oct, *Orquestación de contenedores con Kubernetes*). La clase fue ayer (sábado 3-oct). | **Receso** 5–11 oct → **Semana 10** (clase sáb 17-oct) → **Semana 11** Repaso U2 / Rúbrica U2 (sáb 24-oct) → Semana 12 (sáb 31-oct). |

**Hallazgo crítico de calendario:** la semana 9 ya se dictó y **no tiene presentación publicada**. Las semanas 5 y 6 tampoco tienen material publicado.

### Divergencia entre `index.html` y `TEMARIO-…md`
El `index.html` (oficial) tiene **17 semanas**: S05 = *Resiliencia y continuidad de negocio multicloud*, S06 = *Repaso U1*, S07 = *Microservicios*. El `TEMARIO` todavía tiene la versión vieja (S05 = repaso, S06 = microservicios, S07 = contenedores con ECR). **Se sigue `index.html`** y el TEMARIO se marca como desactualizado en la Fase 2 (sin reescribirlo sin tu visto bueno).

## 2. Inventario de lo publicado

| Sem. | Título oficial | Diapositivas (portadas/contenido) | Con gráfico* | Partes "X de 4" | Video | Narración por diapositiva | Guion docente |
|---|---|---|---|---|---|---|---|
| 1 | Introducción a multicloud | 17 (1/16) | 13/16 (81 %) | No | 1 × 18:00 | No | Sí (~50–55 min) |
| 2 | Patrones de integración | 16 (1/15) | 14/15 (93 %) | No | 1 × 17:56 | No | Sí (~52–57 min) |
| 3 | Redes e interconectividad multicloud | 19 (1/18) | 16/18 (89 %) | No | 1 × 17:47 | No | Sí (~52–56 min) |
| 4 | Gobierno multicloud y migración | 21 (1/20) | 11/20 (55 %) | No | 1 × 12:59 | No | Sí (~56–62 min) |
| 5 | Resiliencia y continuidad multicloud | — | — | — | — | — | No |
| 6 | Repaso Unidad 1 | — | — | — | — | — | No |
| 7 | Arquitecturas de microservicios | 56 (4/52) | 52/52 (100 %) | **Sí** | **4 × 15:01–15:55 (61:33)** | No (no está en el repo) | No |
| 8 | Contenedores y registro de imágenes | 55 (1/54) | 54/54 (100 %) | No | No ("próximamente") | No | No |
| 9 | Kubernetes | — | — | — | — | — | No |
| 10–17 | (resto) | — | — | — | — | — | No |

\* "Con gráfico" = la diapositiva de contenido tiene `<svg>`, `<img>`, `<canvas>` o tabla además del logo. En S01–S03 muchas tablas cuentan como visual pero son texto tabulado; los gráficos reales (diagramas) son menos.

**Respecto al estándar nuevo (4 partes × ~14 diapositivas × ~15 min ≈ 56–60 diapositivas y 60 min):**
- Solo **S07** está en el estándar de estructura y duración.
- **S08** tiene la densidad (55 diapositivas, todas con visual) pero le faltan las divisorias "Parte X de 4", los videos y la narración.
- **S01–S04** tienen entre el 28 y el 37 % de las diapositivas y entre el 22 y el 30 % de la duración del estándar.

## 3. Calidad visual y técnica (hallazgos verificados en las capturas)

### Transversales
1. **Tres plantillas distintas conviven en el curso:** S01–S03 usan un template "Segoe UI" sin logo visible y sin pie de fuentes. S04 y S08 usan otro, con logo SVG embebido. S07 usa un tercero, con kicker y pie de atribución. Esto rompe la identidad del curso.
2. **El logo CUC se carga desde Wikipedia** (`es.wikipedia.org/wiki/Special:FilePath/Logo_cuc.png`) en S01–S03, S07 e `index.html`. Contradice `STANDARDS.md §8` ("autónomo, abre sin conexión"). Sin red, el logo desaparece (lo oculta `onerror`). En S01–S03 también se cargan por hotlink los logos de AWS, Azure, Google Cloud y Oracle desde Wikimedia.
3. **Media diapositiva vacía:** en S01–S04 y en buena parte de S07, el contenido ocupa la mitad superior y la inferior queda en blanco a 1280×720. Los diagramas son pequeños y la letra de las cajas (11–13 px) no se lee en el video a 1080p.
4. **No hay narración versionada.** Los videos existentes se generaron fuera del repo (AAC a 24 kHz, compatible con voz neural tipo Edge TTS), y no hay guion JSON ni script para regenerarlos. Si cambia una diapositiva, hoy no se puede rehacer su video.
5. **Contador doble de página:** el widget de navegación (`‹ 1/56 ›`) se superpone al número estático del pie en S04, S07 y S08.

### Por semana
| Sem. | Defectos concretos |
|---|---|
| S01 | Logos de proveedores rotos sin red; 3 diapositivas de solo texto (5 "¿Por qué importa?", 10 "Anti-patrones", 17 "Conclusiones"); no hay atribución de fuentes por diapositiva. |
| S02 | Desalineada con su guion: el guion (fuente de verdad) desarrolla los 65 patrones EIP, DoorDash, CDC/streaming y strangler fig (Netflix), pero el deck se centra en SNS/SQS y Database@X. 2 diapositivas atadas a AWS ("fan-out SNS → SQS", "los 3 patrones en AWS"). |
| S03 | Desalineada con su guion: el guion trae el direccionamiento/colisión de CIDR, la economía del egress y la física de la latencia, que no aparecen en el deck. La diapositiva 4 "El mismo concepto, cuatro nombres: VCN · VPC · VNet" **viola la regla 3 de `CLAUDE.md`** (comparar nombres de servicios como eje). SVG recortados en las diapositivas 6 y 15. |
| S04 | **Logos de AWS/Azure/Google Cloud en la portada** (viola `STANDARDS.md §6`). 9 de 20 diapositivas sin gráfico. Texto encima del pie en la diapositiva 16 ("¿Qué R le toca a cada app?"). SVG recortados en las 9 y 15. Diapositiva entera dedicada a "IAM Identity Center (antes AWS SSO)", atada a un proveedor. Video de 13 min. |
| S07 | Referente de calidad de estructura, pero con **10 SVG recortados**, contenido cortado visiblemente en las diapositivas 10, 16, 20, 32, 33, 38, 44, 51, 53 y 55 (p. ej. la 16 corta "Servicio de datos" y "Servicio Catálogo"). Cajas con texto que se sale del rectángulo (diapositivas 4 y 5). |
| S08 | 11 MB por fotos embebidas (Pexels/Pixabay, bien atribuidas). Muchas diapositivas son "tarjetas con ícono genérico naranja" en lugar de diagramas reales. **Las capturas de terminal mencionan Play with Docker, que fue descontinuado** (commit 99e5017). No tiene partes, video ni PDF enlazado en `index.html`. |

## 4. Validación contra referentes externos

Referentes usados (ver detalle y URL en `fuentes-recursos.md §1`):
- **Currículo:** ACM/IEEE-CS/AAAI **CS2023**, áreas SF (Systems Fundamentals), NC (Networking & Communication), PDC (Parallel & Distributed Computing), SEC (Security), SE (Software Engineering) y SEP (Society, Ethics & Professionalism).
- **Industria (neutros respecto al proveedor, como se pidió):** AWS Academy **Cloud Architecting** (15 módulos), Microsoft **AZ-305**, Google **Professional Cloud Architect**, CNCF **KCNA**, Oracle **OCI Multicloud Architect Professional** (ancla de U1), Google Skills path 13 *Hybrid and Multi-Cloud Architect* y FinOps Foundation (FinOps Framework + **FOCUS 1.2**).
- **Normas:** NIST SP 800-145 (definición de nube), **ISO/IEC 22123-1:2023** (vocabulario, reemplaza a ISO/IEC 17788), **ISO/IEC 19941:2017** (interoperabilidad y portabilidad, el estándar más directamente ligado al nombre del curso), ISO/IEC 27017/27018, NIST SP 800-207 (Zero Trust), **NIST SP 800-190** (contenedores), **NIST SP 800-204/204A/B/C** (microservicios, service mesh, DevSecOps), OpenTelemetry, SLSA, SPDX/CycloneDX, CloudEvents, OpenAPI/AsyncAPI.
- **Colombia:** Ley 1581 de 2012 y Decreto 1377 de 2013 (datos personales; transferencia internacional vigilada por la SIC), MinTIC – Guía de seguridad en la nube (Modelo de Seguridad y Privacidad, G12) y Acuerdo Marco de Nube Pública de Colombia Compra Eficiente.

### 4.1 Alineación global
| Referente | Cobertura actual del curso | Brecha principal |
|---|---|---|
| CS2023 SF/PDC | Buena en distribución (S02, S07), virtualización y contenedores (S08) | Falta disponibilidad/confiabilidad cuantitativa (SLA compuesto, RPO/RTO): es S05, que no está producida |
| CS2023 NC | S03 se queda en nombres de gateways | Falta direccionamiento, enrutamiento, BGP, DNS híbrido y topologías hub-and-spoke/tránsito (el guion S03 sí las trae) |
| CS2023 SEC / NIST 800-207 | Identidad federada (S01, S04), borde (S07) | Zero Trust, segmentación, secretos y cadena de suministro (S15, no producida) |
| CS2023 SE | Microservicios y contenedores | CI/CD, GitOps, IaC, pruebas en el pipeline (S10, S12) |
| CS2023 SEP / Ley 1581 | GDPR y "LatAm" de forma genérica en S03 | Ley 1581, transferencia internacional (SIC) y nube en el Estado (MinTIC) con caso colombiano |
| AWS Academy Cloud Architecting | Cubre los módulos de redes, conexión de redes, acceso, desacoplamiento y microservicios | **Módulo 14 "Planning for a Disaster" = S05** (pendiente) y la parte **serverless** del módulo 13, ausente en todo el curso |
| AZ-305 | Identidad y gobierno (S04), infraestructura (S03) | **Continuidad de negocio (15–20 % del examen) = S05**; datos/almacenamiento casi ausente |
| Google PCA | Híbrido/multicloud en redes (S03) | Migración planificada (S04 la tiene) y operación/SRE (S14) |
| CNCF KCNA | Contenedores (S08) | **Fundamentos de Kubernetes (el dominio de mayor peso) = S09, ya dictada sin deck**; entrega de aplicaciones cloud native (S10) y observabilidad (S14) |
| ISO/IEC 19941 | Lock-in y portabilidad en S04 | No se usa el modelo de facetas de interoperabilidad/portabilidad, que es el marco formal del "integrar soluciones" |

### 4.2 Repeticiones detectadas
| Tema | Dónde se repite | Propuesta |
|---|---|---|
| Federación SAML/OIDC | S01 (4 diapositivas: 11–14) **y** S04 (7 diapositivas: 3–9) | S01: solo el **problema** de identidad (una diapositiva y un puente). S04: el **mecanismo** completo (SAML, OIDC, broker, SCIM). |
| Oracle Database@X | S01 (casos), S02 (3 diapositivas), S03 (red ODB) | Un solo caso ancla desarrollado en S02 y referenciado en S01 y S03 con una diapositiva cada uno |
| Interconexión privada entre nubes | S01 (TIM Brasil) y S03 | Se queda en S03; en S01 el caso TIM se usa como motivación |
| Puente contenedores → Kubernetes | S08 (diapositivas 49–52) y S09 | Correcto como puente si S08 no adelanta contenido de S09 |

### 4.3 Brechas y mejoras por semana (dentro del título oficial)
Cada semana se organiza en 4 partes de ~15 min. Entre paréntesis, lo que **ya existe** y se reusa.

| Sem. | Parte 1 | Parte 2 | Parte 3 | Parte 4 | Caso colombiano propuesto | Gráficos de red/flujo clave |
|---|---|---|---|---|---|---|
| **1 Introducción a multicloud** | Modelos NIST 800-145 / ISO 22123: servicio y despliegue; responsabilidad compartida | Multicloud vs. híbrido vs. intercloud; drivers y peajes (existente) | Casos reales y anti-patrones (existente) + marco Well-Architected común a los tres proveedores (seis pilares como concepto) | El problema de identidad (corto) + mapa del curso + diagnóstico | Bancolombia → AWS (aparece en el deck S01 **sin fuente**; hay que verificarla o retirarla) | Topología multicloud vs. híbrida; mapa de responsabilidad compartida |
| **2 Patrones de integración** | Acoplamiento y los patrones EIP (guion) | API síncrona: REST/gRPC, contratos OpenAPI, fallos en cascada (existente) | Mensajería y eventos: cola, pub/sub, CloudEvents, AsyncAPI, idempotencia y outbox | Datos entre nubes: batch, streaming y CDC; strangler fig; caso Database@X (único lugar) | Integración de pagos inmediatos *Bre-B* (Banco de la República) — **verificar fuente** | Diagramas de secuencia, fan-out, CDC |
| **3 Redes e interconectividad** | Direccionamiento: CIDR sin colisión entre nubes y on-premises (guion) | Red privada virtual y sus puertas (genérico, **sin tabla de nombres por proveedor**); hub-and-spoke y tránsito | VPN IPsec/BGP, enlace dedicado, interconexión entre nubes; el viaje de un paquete | Egress, latencia (guion), DNS híbrido; soberanía: Ley 1581 + SIC + GDPR | Latencia Barranquilla ↔ regiones cloud; transferencia internacional de datos según la SIC | **Topologías de red completas (la parte más gráfica del curso)** |
| **4 Gobierno multicloud y migración** | Gobierno = decidir quién decide: landing zone, políticas como código, etiquetado | IAM federado completo: SAML, OIDC, broker, SCIM (existente, ampliado) | Lock-in y portabilidad con el modelo ISO/IEC 19941; egress | 7 Rs + repatriación (existente) + cierre de corte | Acuerdo Marco de Nube Pública (Colombia Compra Eficiente) como mecanismo de gobierno en el Estado | Flujo de login federado; árbol de decisión de las 7 Rs |
| **5 Resiliencia y continuidad** | Vocabulario: SLA/SLO, RPO/RTO, ISO 22301 | Matemática de la disponibilidad compuesta (serie/paralelo) | Estrategias de DR: backup/restore, piloto, warm standby, activo-activo entre proveedores; replicación síncrona/asíncrona, CAP | Caídas reales documentadas y caos controlado | Caída global de CrowdStrike (19-jul-2024) y su impacto en aerolíneas y aeropuertos de la región — **verificar fuente primaria** | Topologías activo-pasivo y activo-activo multirregión |
| **6 Repaso U1** | *Propuesta:* deck corto de integración (CaribeMart de punta a punta) + guía de la rúbrica U1 | — | — | — | CaribeMart (proyecto de aula) | Arquitectura integrada de CaribeMart |
| **7 Microservicios** | (existente) | (existente) | (existente) + serverless/FaaS como alternativa de despliegue (una diapositiva) | (existente) + OWASP API Security Top 10 en el borde | (existente) | Corregir los 10 SVG recortados |
| **8 Contenedores** | (existente) Por qué existen | (existente) Imagen y Dockerfile | (existente) Registros + NIST 800-190 | (existente) Redes y volúmenes, compose, puente | Rehacer capturas sin Play with Docker | Reemplazar tarjetas de íconos por diagramas reales (capas, flujo push/pull) |
| **9 Kubernetes** | Del contenedor al clúster: plano de control y nodos | Pod, ReplicaSet, Deployment; rolling update y rollback | Service, Ingress, DNS interno, ConfigMap y Secret | Probes, HPA, namespaces; gestionado vs. propio | Despliegue de CaribeMart en un clúster | **Topología de clúster, red de pods y services** |
| **10 CI/CD** | DevOps y métricas DORA | Etapas del pipeline: build → test → scan → push | GitHub Actions: workflows, runners, secretos, ambientes | Despliegue a Kubernetes: push vs. GitOps (principios OpenGitOps); estrategias blue/green y canary | CaribeMart con el pipeline completo | Flujo del pipeline; blue/green |
| **11 Repaso U2** | *Propuesta:* deck corto + guía de la rúbrica U2 | — | — | — | CaribeMart contenedorizada | — |
| **12 IaC** | Declarativo vs. imperativo; deriva | Terraform/OpenTofu: proveedores, plan/apply, estado remoto | Módulos y un mismo código contra varios proveedores | Políticas como código (OPA), IaC en el pipeline | Infraestructura reproducible para CaribeMart | Grafo de dependencias; flujo plan/apply |
| **13 Service mesh** | Por qué una malla: lo que el gateway no resuelve | Sidecar vs. ambient; mTLS (NIST 800-204A) | Multiclúster y multicloud: descubrimiento y mirroring | Políticas, tráfico (canary) y costos de la malla | CaribeMart en dos clústeres | **Topología de malla multiclúster** |
| **14 Observabilidad** | Logs, métricas y trazas; OpenTelemetry | Prometheus y Grafana; SLI/SLO/presupuesto de error | Trazas distribuidas entre nubes | AIOps: anomalías vs. umbrales y sus límites | Monitoreo de CaribeMart | Flujo del colector OTel; traza distribuida |
| **15 Seguridad y FinOps** | Cadena de suministro: SLSA, SBOM (SPDX/CycloneDX), firma | Escaneo y políticas de admisión; CSPM | IA en seguridad, con límites honestos | FinOps Framework y FOCUS 1.2; etiquetado y showback | Ley 1581 y responsabilidad del encargado; costos en COP | Flujo de la cadena de suministro; ciclo FinOps |
| **16–17 Repaso + sustentación** | Guía de sustentación y rúbrica U3 | — | — | — | CaribeMart multicloud | — |

**Temas que faltan en todo el curso y se proponen DENTRO de semanas existentes:** serverless/FaaS (S07, P3), seguridad de APIs OWASP (S07, P4), resolución DNS híbrida (S03, P4), modelo ISO/IEC 19941 (S04, P3) y SLA compuesto (S05, P2). Ningún título cambia.

## 5. Alcance: solo material académico
Por instrucción del docente (4-oct-2026), los **laboratorios quedan fuera del alcance** de este análisis y de la Fase 2. Se trabaja solo el material académico: presentaciones HTML, narración, PDF y videos. Las presentaciones no dependen de ninguna plataforma de labs. Cuando una semana necesite un ejemplo práctico, se muestra como demostración conceptual dentro del deck (diagramas, capturas propias y comandos ilustrativos), sin enlazar ni diseñar laboratorios.

## 6. Presentaciones viejas (.pptx)
No se compartió ningún `.pptx` en esta sesión. Cuando las compartas (por ejemplo en `insumos/pptx/`, carpeta no publicada), se extraen con `python-pptx`: texto, notas y la estructura de los diagramas. Cada idea se mapea a una semana en una tabla `docs/mapa-pptx.md` y cada diagrama se **redibuja como SVG propio**. Nunca se pegan imágenes con derechos.

## 7. Conflictos con documentos del repo que hay que resolver en la Fase 2
1. `STANDARDS.md v1.1` exige **17–20 diapositivas**, y el estándar nuevo es de ~56–60 en 4 partes. Se propone un **STANDARDS v2.0** que adopte el formato de S07.
2. `STANDARDS.md §8`: "autónomo/sin conexión" frente al logo y los íconos por hotlink.
3. `CLAUDE.md` dice "solo la semana 4 fue actualizada con video narrado", lo cual quedó desactualizado (S07 tiene 4 videos).
4. `index.html` dice "5 de 16 publicadas", pero hay 6 tarjetas y el calendario tiene 17 semanas.
