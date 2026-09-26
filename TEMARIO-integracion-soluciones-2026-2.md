# Temario definitivo — Integración de Soluciones para Plataformas Cloud (2026-2)

**Docente:** Rodolfo Cañas Cervantes — Universidad de la Costa (CUC), Ingeniería de Sistemas.
**Grupo:** PRESENCIAL-24801, sábado 10:00–13:00, nivel 8, 20 estudiantes.
**Enfoque:** multicloud real — de concepto (Unidad 1) a construcción práctica sobre AWS (Unidad 2) a integración con infraestructura propia + IA (Unidad 3). No un sandbox AWS aislado.

**Uso de este documento:** referencia única para construir cualquier presentación semanal de este curso. No repetir el temario completo en cada brief — apuntar aquí.

**Reorganización 2026-08-15 (v2):** versión anterior mezclaba concepto de multicloud y contenedores/CI/CD dentro de Unidad 1, dejando Unidad 3 sin identidad propia. Rediseño de Rodolfo: cada unidad ahora tiene un ancla temática clara —
- **U1 = concepto** (Oracle Multicloud Architect)
- **U2 = construcción práctica** (AWS Lab Project: microservicios + CI/CD)
- **U3 = frontera** (IA aplicada a multicloud + integración con infraestructura ASUR)

**Auditoría 2026-08-21 (sin cambios aplicados al temario):** se investigó con Perplexity un rediseño mayor (mover U1 a labs simulados online, reemplazar el lab AWS de U2 por un pipeline GitHub-centric, cambiar Amazon Q Developer por GitHub Copilot Student en semana 11). **Rechazado en su totalidad para este semestre** — ver `AUDITORIA-propuesta-perplexity-para-claude.md` para el detalle. Motivo principal: violaría el principio "≥90% práctico real en la nube" (Killercoda/namespaces simulados no son interconectividad multicloud) y cambiaría la espina dorsal de U2 a mitad de semestre, con el lab AWS ya en marcha (fases 1-2 adelantadas en semana 2) y el curso Academy [182349] activo hasta 30-nov. Sobre semana 11: Rodolfo confirma que el curso ya tiene acceso a Amazon Q Developer desde antes del cierre de registros (15-may-2026), así que no hace falta cambiarlo. El temario queda igual que en la versión v2 (2026-08-15). La propuesta completa de Perplexity/equipo técnico queda archivada como insumo para el rediseño de **2027-1**, no para este semestre.

---

## Estructura de evaluación (igual a las demás asignaturas presenciales de Rodolfo)

- 3 unidades → 3 cortes de evaluación (sin examen parcial escrito: cada corte cierra con una rúbrica de proyecto), cada uno vale **30%** de la nota final.
- Cada corte (30%) = **10%** actividades de clase (**2**, 5% cada una, **ambas prácticas reales en el Learner Lab de AWS** — ninguna es un ejercicio de solo papel/diagrama) + **20%** proyecto de aula/rúbrica práctica.
- **10%** restante = Prueba de Competencia Genérica institucional (fuera del alcance del portal).
- Principio transversal: contenido **≥90% práctico**.

## Unidad 1 — El concepto de multicloud (semanas 1-5)

Ancla: **Oracle "Become an OCI Multicloud Architect Professional"** (`learn.oracle.com`/Coursera, gratis y público — confirmado por Rodolfo como la base real del deck 2025-2 de la asignatura). Es la referencia conceptual oficial de "multicloud interconectado": no solo usar varias nubes por separado, sino conexión privada real entre proveedores. No hay cuenta Oracle Cloud gestionada para estudiantes — se usa como marco teórico, la práctica de esta unidad ya es 100% AWS.

| Módulo Oracle | Contenido | Semana |
|---|---|---|
| 1. Estrategias multicloud + IAM en OCI | Introducción a multicloud, casos de uso, IAM, identity domains, federación | Semana 1 |
| 3. Oracle Database@Azure / Database@Google Cloud | Un mismo servicio ancla desplegado en varias nubes — caso real de integración | Semana 2 |
| 2. Redes OCI e interconectividad | VCN, gateways, peering, Site-to-Site VPN, FastConnect, OCI-Azure/Google Interconnect | Semana 3 |
| 4. Preparación para certificación | Repaso | No aplica (no es objetivo de certificación) |

## Unidad 2 — Construcción práctica sobre AWS (semanas 6-10)

Ancla: **AWS Academy Lab Project - Microservices and CI/CD Pipeline Builder [182349]**, creado 2026-08-06, 3 ago–30 nov 2026. **Verificado vía Canvas API (2026-08-15)**, curso ya aprovisionado. A diferencia de Arquitectura en la Nube/Seguridad en Redes (cursos "Cloud Architecting"/"Cloud Security", con 15-17 módulos independientes, cada uno con su propio lab), este es un **Lab Project**: estructura mucho más chica y **no divisible por tema**.

Contenido real del curso (5 módulos de Canvas, no confundir con "módulo" temático):
1. Bienvenida e información general.
2. **Un único bloque de contenido**, con exactamente 2 items:
   - `Instrucciones de laboratorio: Creación de microservicios y una canalización de CI/CD con AWS` — **un solo lab consolidado**, todo en un solo ejercicio guiado, no labs separados por servicio.
   - `Evaluación de conocimientos: Creación de microservicios y una canalización de CI/CD con AWS` — quiz de 50 pts.
3. Insignias/certificados de finalización.
4. Encuesta de comentarios.
5. Recursos de AWS T&C.

**Identificadores exactos del lab (verificado vía Canvas API, 2026-08-15)**:
- Module item id `17989932`, `content_id` 4009756, tipo `ExternalTool`.
- Se abre vía LTI en Vocareum: `assignment=2029442` (`labs.vocareum.com/lti/launch.php?assignment=2029442`).
- **Es un solo lab, un solo `assignment` de Vocareum** — no tiene sub-labs separables ni IDs distintos por fase. Las Actividades del plan semanal **apuntan al mismo lab en distintos momentos de avance**, no a labs AWS distintos.
- El quiz asociado (`Evaluación de conocimientos`, assignment_id 2208638, 50 pts) es el único ítem calificable nativo de Canvas para este módulo — queda como **formativo, sin nota**, igual que los quizzes por módulo de Arquitectura en la Nube/Seguridad en Redes.

**Contenido real del lab (verificado 2026-08-15 vía el README oficial del lab + fuentes públicas — outline de AWS Academy en Scribd/GitHub/Medium, no vía IA)**: el estudiante parte de una aplicación monolítica real ("coffee suppliers") corriendo en un EC2 con MySQL/RDS, y la descompone en 2 microservicios (`customer` y `employee`). Stack real usado: **AWS Cloud9** (IDE), **CodeCommit** (2 repos: `microservices` y `deployment`), Docker (build manual en Cloud9), **Amazon ECR**, **ECS Fargate** (clúster serverless), **Application Load Balancer** con 4 target groups y enrutamiento por path, **CodeDeploy** (despliegue Blue/Green sobre ECS) y **CodePipeline** (dispara el despliegue cuando se actualiza la imagen en ECR). **Corrección importante: el lab NO usa CodeBuild** — el build de las imágenes Docker es manual en Cloud9, no automatizado por un CodeBuild; el pipeline solo orquesta CodeCommit → CodeDeploy. Referencias corregidas en el temario de abajo (semana 8).

9 fases reales del lab (para dimensionar el esfuerzo real, no exhaustivo):
1. Diseño y estimación de costos (diagrama de arquitectura + AWS Pricing Calculator — este es el requisito real "R2" de costos, hecho **al inicio** del lab como planeación, no al final).
2. Análisis de la aplicación monolítica existente.
3. Entorno de desarrollo: Cloud9 + repositorio Git en CodeCommit.
4. Configuración de los 2 microservicios + pruebas de contenedores Docker (la fase más larga y con más edición de código real).
5. Registro en ECR + clúster ECS + task definitions + archivos de despliegue (CodeDeploy AppSpec).
6. Load Balancer y enrutamiento por path (`/admin/*` → employee).
7. Servicios ECS (customer y employee).
8. Pipeline CI/CD: CodeDeploy + CodePipeline, con despliegue Blue/Green real.
9. Actualizaciones iterativas: restringir acceso por IP, actualizar UI, verificar que el pipeline se dispara solo al actualizar la imagen en ECR, escalar el servicio.

## Unidad 3 — IA + integración con infraestructura propia (semanas 11-16)

Ancla doble, a propósito (Rodolfo quiere que esta unidad tenga identidad propia, no solo ser "el cierre logístico"):
- **IA aplicada a multicloud**: cómo la inteligencia artificial ya está entrando en la operación de infraestructura multi-proveedor — asistentes de código para IaC/pipelines (Amazon Q Developer), observabilidad predictiva (AIOps), detección de amenazas asistida por IA.
- **Complemento propio ASUR**: el pipeline construido en Unidad 2 se extiende para desplegar también en infraestructura real administrada por Rodolfo (`.11`), cerrando la idea de "multicloud real, no simulado" — mismo patrón de interconexión privada que Oracle Interconnect/FastConnect (Unidad 1, semana 3), ahora aplicado en la práctica.

Propuesta concreta del segundo destino: un "sandbox de microservicios" en `.11` (mismo patrón que Portal Mona — contenedores aislados, publicados solo en loopback, expuestos vía el túnel de Cloudflare existente), con un endpoint de salud simple. **Pendiente construir** — no bloqueante para las semanas 1-11, se necesita antes de semana 12.

## Plan semana a semana

| Semana | Fechas 2026 | Unidad | Tema | Actividad/Evaluación |
|---|---|---|---|---|
| 1 | 3–9 ago | U1 | **Introducción a multicloud**: qué es una arquitectura multicloud, multicloud vs. nube híbrida, casos de uso reales, conclusiones clave (Oracle Módulo 1: estrategias multicloud + IAM). Cierra con encuadre breve del curso (evaluación, calendario, expectativas) | Actividad diagnóstica (no cuenta nota) — identificar ejemplos de multicloud vs. híbrido en casos reales |
| 2 | 10–16 ago | U1 | Patrones de integración: API, mensajería, eventos — anclado a Oracle Módulo 3 (Database@Azure/Database@Google Cloud como caso real de un servicio ancla multi-nube) | **5% · Actividad 1 (U1):** práctica en AWS — cada estudiante crea en su Learner Lab una cola (SQS) y un tópico de eventos (SNS/EventBridge) y conecta 2 servicios simples entre sí, replicando en AWS los 3 patrones vistos (API/mensajería/eventos) |
| 3 | 17–23 ago | U1 | Redes e interconectividad multicloud: VPN, FastConnect/Interconnect (Oracle Módulo 2) + **soberanía de datos y cumplimiento regional**: dónde vive físicamente el dato, regiones, GDPR y marcos análogos en LatAm | **5% · Actividad 2 (U1):** práctica en AWS — configurar un Site-to-Site VPN o VPC Peering en el Learner Lab, replicando en AWS el patrón de interconexión privada de Oracle |
| 4 | 24–30 ago | U1 | Gobierno multicloud: IAM federado, vendor lock-in y **estrategias de migración entre proveedores (los 6/7 Rs: rehost, replatform, refactor, repurchase, retain, retire, relocate)** — el complemento lógico de la discusión de lock-in | |
| 5 | 31 ago–6 sep | U1 | Repaso Unidad 1 | **Rúbrica U1** — 20% proyecto (por definir) |
| 6 | 7–13 sep | U2 | Arquitecturas de microservicios: descomposición de monolitos, comunicación síncrona/asíncrona, API Gateway | |
| 7 | 14–20 sep | U2 | Contenedores y registro de imágenes: Docker, Amazon ECR — **arranque del lab AWS** | **5% · Actividad 1 (U2):** checkpoint del lab AWS Vocareum #2029442 (imagen en ECR corriendo) |
| 8 | 21–27 sep | U2 | Contenedores y registro de imágenes: Docker, build de imágenes, capas y Dockerfile, registros (concepto genérico — Docker Hub/Amazon ECR/Azure ACR/Google Artifact Registry) — **laboratorio build → push → run** | **10% · Actividad 1 (U2):** [Laboratorio 3 — Contenedores con Docker Hub](laboratorios/lab-03-contenedores-docker-hub.html) |
| 9 | 28 sep–4 oct | U2 | Cierre de Unidad 2: orquestación con Kubernetes (pods, deployments, services — conceptos, sin atarse a un proveedor) + pipeline CI/CD genérico con GitHub Actions (build → test → push → deploy), cerrando el ciclo `build → push → run` de la semana 8 con despliegue automatizado de CaribeMart contenedorizada | — (evaluación de U2 ya cubierta en semana 8, 10%) |
| **Receso** | 5–11 oct | — | Sin clase | |
| 10 | 12–18 oct | U2 | Repaso Unidad 2 | **Rúbrica U2 — 20% proyecto:** CaribeMart contenedorizada con pipeline CI/CD funcionando de punta a punta (build → push a registro → despliegue automatizado) |
| 11 | 19–25 oct | U3 | Infraestructura como código multicloud: Terraform/OpenTofu — un mismo código de infraestructura desplegado contra distintos proveedores (demo contra floci, emulador AWS en `.3`), estado remoto y por qué IaC es la base de cualquier pipeline multicloud serio | |
| 12 | 26 oct–1 nov | U3 | Service mesh e interconexión entre clústeres multicloud: mTLS cruzado y mirroring de servicios (Istio/Linkerd genérico; Google Anthos Service Mesh como caso real documentado), aplicación práctica del patrón de interconexión de la semana 3 | **5% · Actividad 1 (U3):** práctica en sandbox — mTLS entre 2 servicios en clústeres distintos — **1 nov: último día retiro de asignatura** |
| 13 | 2–8 nov | U3 | Observabilidad multicloud: logs, métricas y trazas (OpenTelemetry, Prometheus/Grafana) + tendencia AIOps — detección de anomalías y alertas predictivas frente al monitoreo tradicional de umbrales fijos | **5% · Actividad 2 (U3):** instrumentar CaribeMart con métricas/trazas básicas y documentar 1 anomalía detectada |
| 14 | 9–15 nov | U3 | Seguridad multicloud y FinOps: cadena de suministro de software (escaneo de imágenes, SBOM), IA aplicada a seguridad con discusión honesta de límites (fatiga de alertas, sesgos, ataques adversariales — *human-augmented*, no autónomos) y gestión de costos multicloud (FinOps) | |
| 15–16 | 16–29 nov | U3 | Repaso + entrega/sustentación del proyecto final | **Rúbrica U3 — 20% proyecto:** CaribeMart desplegada multicloud con pipeline, observabilidad y seguridad aplicada, documentado como cierre del tercer corte. **Fin de clases: 30 nov** |
| — | 30 nov–13 dic | — | Sin clase | Cierre académico administrativo: corrección notas (1-4 dic) · cierre 9-10 dic · grados 11 dic |

**Nota de numeración de actividades U2 (actualizada 2026-09-26):** la Actividad 1 de U2 (semana 8, 10%) ya no depende de AWS Vocareum — se movió a un laboratorio propio en Play with Docker + Docker Hub (build → push → run), sin costo ni cupos de AWS Academy de por medio. La semana 9 cierra la unidad con Kubernetes + CI/CD, sin actividad calificada adicional (el 10% de U2 ya se cubrió en semana 8). **Pendiente de decisión de Rodolfo:** si el lab AWS de la semana 7 (checkpoint, fila de arriba) se alcanzó a calificar de verdad o quedó sin ejecutar — hay evidencia en memoria de que el lab AWS solo se usó como calentamiento informal en semana 2, nunca confirmado como checkpoint formal.

**Temario de U2 (semana 9) y U3 completo (semanas 11-16) rediseñado y aprobado por Rodolfo el 2026-09-26**, generico y sin AWS Academy — reemplaza el diseño anclado a AWS Lab Project de la sección "Validación externa" más abajo (que queda como registro histórico de la decisión de agosto, ya superada). Fuentes de validación del nuevo temario: `memorias/INVESTIGACION-fuentes-B2-temario-generico.md` (Oracle OCI, Google Skills path 13, Coursera "Foundation to Multi-Cloud").

## Proyectos de aula (20% de cada unidad) — por definir

La idea general de cada proyecto ya está anclada al contenido de su unidad, pero el enunciado/rúbrica exacta **todavía no está definida** — Rodolfo los diseña más cerca de cada corte, mismo criterio que Arquitectura en la Nube (la rúbrica se libera solo la semana del corte, no antes):

- **U1 (Rúbrica U1):** anclado al concepto de multicloud — evaluación de una arquitectura multi-proveedor propuesta por el estudiante (gobierno, interconexión, selección de proveedores).
- **U2 (Rúbrica U2, actualizado 2026-09-26):** CaribeMart contenedorizada (Docker) con pipeline CI/CD genérico (build → push a registro → despliegue), continuando el hilo conductor de la aplicación de ejemplo iniciado en U1.
- **U3 (Rúbrica U3, cierre del curso, actualizado 2026-09-26):** CaribeMart desplegada multicloud (varios proveedores/ASUR vía IaC de la semana 11) con al menos un componente aplicado de las semanas de U3 — observabilidad, seguridad o service mesh — enunciado exacto por definir más cerca del corte.

## Quiz de conocimiento AWS — formativo, sin nota

`Evaluación de conocimientos: Creación de microservicios y una canalización de CI/CD con AWS` (50 pts en Canvas) queda como **práctica formativa, sin nota**, igual que los quizzes por módulo de Arquitectura en la Nube y Seguridad en Redes. **Actualizado 2026-09-26:** con el rediseño genérico de U2 (ya no ancla a AWS Lab Project), la nota real de U2 viene del laboratorio de contenedores (semana 8, 10%) y de la Rúbrica U2 (20%, CaribeMart con pipeline) — este quiz de AWS sigue disponible como práctica formativa opcional para quien quiera profundizar en la implementación AWS específica, no como requisito.

## Validación externa del temario (Perplexity Deep Research, 2026-08-15) — ⚠️ SUPERADA 2026-09-26

> Esta sección documenta la decisión de agosto de anclar U2/U3 a AWS Academy/Lab Project. Esa decisión **se revirtió el 2026-09-26** (AWS Academy no resultó viable para el curso) — el temario vigente de U2 (semana 9) y U3 (semanas 11-16) es genérico, sin AWS, validado con Oracle/Google Skills/Coursera en `memorias/INVESTIGACION-fuentes-B2-temario-generico.md`. Queda como registro histórico de por qué se había diseñado así, no como el diseño actual.

Se contrastó este temario contra currículos reales de multicloud vigentes 2024-2026 (learning path de Oracle "OCI Multicloud Architect Professional", outline oficial del AWS Academy Lab Project, certificaciones de FinOps Foundation, documentación de Istio/Linkerd, guías de AIOps y XDR). Veredicto: los dos anclajes elegidos (Oracle para concepto, AWS Lab Project para práctica) son correctos y siguen vigentes — la certificación Oracle incluso se extendió en 2026 a los tres hyperscalers (Database@AWS además de Azure y Google Cloud), lo que refuerza el caso de "un mismo servicio en varias nubes" de la semana 2.

**Cambios aceptados y ya aplicados arriba:**
1. **FinOps** (gestión de costos multicloud, estándar FOCUS) — agregado en semana 9. Se ubicó en U2, no en U1 como sugería la investigación. Nota de precisión (verificada 2026-08-15 contra el README real del lab): el requisito de costos del propio Lab Project (R2, estimación con AWS Pricing Calculator) en realidad se hace **al inicio** del lab, como planeación — no al final. La sesión de semana 9 no es ese mismo entregable, sino una revisión pedagógica propia: comparar esa estimación inicial contra el costo real observado ya con la infraestructura desplegada, que es un ejercicio de FinOps más rico y solo posible al final.
2. **Estrategias de migración (6/7 Rs)** — agregado en semana 4, junto a vendor lock-in, que es el problema que esas estrategias resuelven.
3. **Soberanía de datos y cumplimiento regional** — agregado en semana 3, junto a redes/interconectividad (dónde vive físicamente el dato es la continuación natural de cómo se conectan las regiones).
4. **Service mesh multicloud** (Istio multi-primary / Linkerd multicluster) — agregado en semana 12. Era el gap más relevante: es el mecanismo técnico concreto que hace posible la integración AWS↔ASUR que esa sesión ya exigía, y conecta a nivel de aplicación lo que la semana 3 enseña a nivel de red.
5. **Herramientas nombradas concretamente en toda U3** — Amazon Q Developer, CloudWatch anomaly detection / DevOps Guru / X-Ray Insights, CrowdStrike Falcon XDR / Microsoft Sentinel Copilot / SentinelOne Singularity.

**Cambio rechazado, con justificación:** la investigación proponía *fusionar* las semanas 13 (observabilidad) y 14 (seguridad) en una sola sesión de "IA en operaciones" para liberar espacio. Se rechaza: eso reduciría la Unidad 3 a 2 sesiones de IA y le quitaría justamente la identidad temática que la unidad debe tener (el "toque de nuevas tecnologías con IA" es el criterio de diseño explícito de esta unidad, no un relleno). El espacio que la investigación buscaba liberar se obtuvo de otra forma — moviendo FinOps a U2 y agregando migración/soberanía como complementos de sesiones de U1 que ya existían, sin sacrificar ninguna sesión de IA.

**Sobre el orden pedagógico:** la investigación confirmó que el orden actual (concepto → práctica → IA) es defendible y recomendó mantenerlo. Invertirlo haría que el estudiante construya un pipeline mono-proveedor sin haber discutido todavía por qué eso es insuficiente en multicloud, debilitando la justificación del proyecto integrador final. La sugerencia complementaria fue aplicar principios de *flipped classroom* dentro de cada sesión (lecturas/videos antes de clase, resolución de problemas en clase), no reordenar unidades.

## Gaps / pendientes

- Construir cada semana de U2 (9) y U3 (11-16) según el estándar REQ-046 (deck 50-60 slides, ≥90% imagen real, guion+audio+4 videos, laboratorio gratuito) — ninguna todavía está construida, solo el temario está aprobado.
- El "sandbox de microservicios en `.11`" y el resto de infraestructura AWS-específica de los gaps de agosto ya no aplican al rediseño genérico — revisar si algo de esa infraestructura sigue siendo útil para las nuevas semanas (p. ej. floci para IaC en semana 11).
- Diseñar el enunciado exacto de los 3 proyectos de aula (20% c/u) — se libera semana del corte correspondiente.

## Referencias

- AWS Academy Lab Project - Microservices and CI/CD Pipeline Builder [182349] — usado como ancla de U2/U3 hasta 2026-09-25, ya no vigente.
- Oracle "OCI Multicloud Architect Professional 2025" (mylearn.oracle.com #144474) — referencia conceptual de multicloud, Unidad 1 completa.
- Google Skills path 13 "Hybrid and Multi-Cloud Architect" (skills.google/paths/13) — Kubernetes/Anthos, referencia de semanas 9 y 12.
- Coursera "Foundation to Multi-Cloud" (coursera.org/learn/foundation-to-multi-cloud) — secuencia contenedores→Kubernetes→Terraform, referencia de semanas 8-9-11.
- Calendario académico oficial: Acuerdo CD-645 CUC 2026.
- Contexto completo: `/opt/asur/MEMORY/project_integracion_soluciones_syllabus.md` (solo accesible desde `.3`).
