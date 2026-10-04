# Fuentes y recursos con licencia — Integración de Soluciones para Plataformas Cloud (2026-2)

Este documento tiene dos partes. La **§1** reúne los referentes de contenido que validan el temario. Las **§2 a §5** cubren los recursos gráficos (íconos, imágenes, tipografías, voz), con lo que se puede reutilizar y cómo citarlo.
Regla del curso (`STANDARDS.md §5`): toda imagen o diagrama lleva pie con fuente y URL, o la marca "Diagrama: elaboración propia — basado en <fuente>".

> Estado: las licencias se resumen tal como las publica cada titular a octubre de 2026. Antes de usar un recurso en la Fase 2 se abre la URL de términos y, si cambió algo, se actualiza esta tabla. No es asesoría legal.

---

## 1. Referentes de contenido (validación del temario)

### 1.1 Currículo y certificaciones
| # | Referente | URL | Uso en el curso |
|---|---|---|---|
| R1 | ACM/IEEE-CS/AAAI, *Computer Science Curricula 2023* (CS2023) | https://csed.acm.org/wp-content/uploads/2025/11/CS2023-Report.htm · https://dl.acm.org/doi/pdf/10.1145/3664191 | Áreas SF, NC, PDC, SEC, SE, SEP |
| R2 | AWS Academy *Cloud Architecting* — esquema de 15 módulos | https://media.uem.edu.in/uploads/sites/3/2021/03/ACA-Course-Outline-EN-2019-05-29.pdf (esquema público) | Contraste de cobertura (DR, desacoplamiento, microservicios/serverless) |
| R3 | Microsoft, *Study guide AZ-305* (skills measured) | https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-305 | Pesos: identidad/gobierno/monitoreo 25–30 %, datos 20–25 %, continuidad 15–20 %, infraestructura 30–35 % |
| R4 | Google Cloud, *Professional Cloud Architect exam guide* | https://cloud.google.com/learn/certification/guides/professional-cloud-architect | Híbrido/multicloud, migración, operación |
| R5 | CNCF / Linux Foundation, *KCNA* | https://www.cncf.io/training/certification/kcna/ · https://training.linuxfoundation.org/certification/kubernetes-cloud-native-associate/ | Dominios Kubernetes, orquestación, entrega y arquitectura cloud native (los pesos varían entre versiones; se toman de la página oficial al producir S09) |
| R6 | Oracle, *OCI Multicloud Architect Professional* | https://mylearn.oracle.com (curso #144474) | Ancla conceptual de U1 (ya en uso) |
| R7 | Google Skills, path 13 *Hybrid and Multi-Cloud Architect* | https://skills.google/paths/13 | Kubernetes y multiclúster (S09, S13) |
| R8 | FinOps Foundation, *FinOps Framework* y *FOCUS 1.2* (ratificado el 29-may-2025) | https://www.finops.org/insights/focus-1-2-available/ · https://focus.finops.org/wp-content/uploads/2025/05/FOCUS-spec-v1_2.pdf | S15 |

### 1.2 Normas y estándares
| # | Norma | URL | Semana |
|---|---|---|---|
| N1 | NIST SP 800-145, *The NIST Definition of Cloud Computing* | https://csrc.nist.gov/pubs/sp/800/145/final | S01 |
| N2 | ISO/IEC 22123-1:2023, vocabulario de cloud computing (reemplaza ISO/IEC 17788:2014) | https://www.iso.org/standard/82758.html | S01 |
| N3 | ISO/IEC 19941:2017, *Interoperability and portability* (modelo de facetas) | https://committee.iso.org/standard/66639.html | S02, S04 |
| N4 | ISO/IEC 27017 (controles de seguridad en la nube) e ISO/IEC 27018 (datos personales en la nube) | https://www.iso.org/standard/43757.html · https://www.iso.org/standard/76559.html | S04, S15 |
| N5 | ISO 22301 (continuidad de negocio) | https://www.iso.org/standard/75106.html | S05 |
| N6 | NIST SP 800-207, *Zero Trust Architecture* | https://csrc.nist.gov/pubs/sp/800/207/final | S03, S07, S15 |
| N7 | NIST SP 800-190, *Application Container Security Guide* (2017) | https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-190.pdf | S08, S15 |
| N8 | NIST SP 800-204 / 204A / 204B / 204C (microservicios, service mesh, ABAC, DevSecOps) | https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204.pdf · https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204A.pdf · https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-204c.pdf | S07, S10, S13 |
| N9 | OpenTelemetry (especificación CNCF) | https://opentelemetry.io/docs/specs/otel/ | S14 |
| N10 | SLSA (niveles de la cadena de suministro) · SPDX (ISO/IEC 5962:2021) · CycloneDX (ECMA-424) | https://slsa.dev · https://spdx.dev · https://cyclonedx.org | S15 |
| N11 | CloudEvents (CNCF) · OpenAPI · AsyncAPI | https://cloudevents.io · https://spec.openapis.org · https://www.asyncapi.com | S02 |
| N12 | OpenGitOps (principios GitOps, CNCF) | https://opengitops.dev | S10 |
| N13 | RFC 4301 (IPsec) · RFC 4271 (BGP-4) · RFC 1918 (direccionamiento privado) | https://www.rfc-editor.org | S03 |
| N14 | OWASP API Security Top 10 (2023) | https://owasp.org/API-Security/ | S07 |

### 1.3 Marco colombiano
| # | Fuente | URL | Semana |
|---|---|---|---|
| C1 | Ley 1581 de 2012 (protección de datos personales) | http://www.secretariasenado.gov.co/senado/basedoc/ley_1581_2012.html | S03, S15 |
| C2 | Decreto 1377 de 2013 | https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=53646 | S03 |
| C3 | SIC, estudio sobre transferencia internacional de datos personales | https://www.sic.gov.co/sites/default/files/files/Proteccion_Datos/consulta_avanzada/TRANSFERENCIA-INTERNACIONAL-DE-DATOS-PERSONALES-09-03-2017.pdf | S03 |
| C4 | MinTIC, *Seguridad en la Nube — Guía No. 12* (MSPI) | https://gobiernodigital.mintic.gov.co/692/articles-5482_G12_Seguridad_Nube.pdf | S04, S15 |
| C5 | MinTIC, *Guía Técnica de Computación en la Nube* | https://www.mintic.gov.co/portal/715/articles-58727_recurso_2.pdf | S01, S04 |
| C6 | MinTIC: Acuerdo Marco de Nube Pública (noticia oficial) | https://mintic.gov.co/portal/inicio/Sala-de-prensa/Noticias/126027:El-MinTIC-capacita-a-los-funcionarios-de-las-entidades-publicas-para-que-se-suban-a-la-nube | S04 |

### 1.4 Libros base ya citados en el curso
Gregor Hohpe y Bobby Woolf, *Enterprise Integration Patterns* (S02); Sam Newman, *Building Microservices* (2.ª ed.) y *Monolith to Microservices*; Chris Richardson, *Microservices Patterns*; Eric Evans, *Domain-Driven Design* (S07); Google, *Site Reliability Engineering* (sre.google/books, de lectura libre en línea) para SLO y presupuestos de error (S05, S14). Se citan por nombre y capítulo; nunca se copian sus figuras: se redibujan.

---

## 2. Íconos y símbolos para diagramas

| Recurso | Licencia / términos | ¿Se puede reutilizar? | Condiciones clave | URL | Cómo citar (pie `.src`) |
|---|---|---|---|---|---|
| **Íconos propios del curso (SVG dibujados a mano en el HTML)** | Propiedad del curso | Sí, sin restricción | Recomendado como opción por defecto: neutro respecto al proveedor | — | `Diagrama: elaboración propia — basado en <fuente>` |
| **Cisco Network Topology Icons** | Uso autorizado por Cisco sin permiso adicional | Sí | **Sin modificar** (no recolorear ni editar); no implicar respaldo de Cisco | https://www.cisco.com/c/en/us/about/brand-center/network-topology-icons.html · https://www.cisco.com/c/en/us/about/brand-center/copyright-use.html | `Íconos: Cisco Network Topology Icons` |
| **Kubernetes Icons Set** (kubernetes/community) | Apache-2.0 **o** CC-BY-4.0, a elección | Sí, incluso modificados | Atribución (CC-BY); el logo de Kubernetes es marca de la Linux Foundation | https://github.com/kubernetes/community/tree/main/icons | `Íconos: Kubernetes Icons Set (CC BY 4.0)` |
| **AWS Architecture Icons** | Términos de AWS para diagramas de arquitectura | Sí, para representar servicios AWS | Sin alterar colores ni forma; no usarlos como logo propio | https://aws.amazon.com/architecture/icons/ | `Íconos: AWS Architecture Icons` |
| **Azure Architecture Icons** | Términos de Microsoft: diagramas, material de formación y documentación | Sí | No recortar, rotar ni distorsionar; nombre completo cerca del ícono | https://learn.microsoft.com/en-us/azure/architecture/icons/ | `Íconos: Microsoft Azure Architecture Icons` |
| **Google Cloud Icons** | Uso para diagramas de arquitectura propios | Sí | Seguir las guías de marca de Google | https://cloud.google.com/icons | `Íconos: Google Cloud Icons` |
| **Tabler Icons** | MIT | Sí, incluso modificados | Mantener el aviso de licencia en el código fuente | https://tabler.io/icons | `Íconos: Tabler Icons (MIT)` |
| **Lucide** | ISC | Sí | Igual que MIT | https://lucide.dev | `Íconos: Lucide (ISC)` |
| **CNCF artwork** (logos de proyectos CNCF) | Según cada proyecto; las marcas son de la LF | Solo para referirse al proyecto | Uso nominativo, sin alterar | https://github.com/cncf/artwork | `Logo: CNCF artwork` |
| **Simple Icons** (logos de marcas) | CC0 para el SVG, **pero las marcas siguen siendo de sus titulares** | Solo uso nominativo | Prohibidos en la portada (`STANDARDS §6`) | https://simpleicons.org | `Logo: <marca> vía Simple Icons` |

**Recomendación para la Fase 2:** usar íconos propios (SVG genéricos de router, firewall, nube, contenedor, clúster) y Kubernetes Icons Set (que se puede recolorear a vino/dorado) como base. Los íconos de AWS, Azure y GCP se reservan para cuando el caso exija la marca. **Embeber siempre** los SVG; nada de hotlinks.

## 3. Fotografías e imágenes

| Recurso | Licencia | ¿Atribución obligatoria? | Restricciones | URL |
|---|---|---|---|---|
| **Pexels** (usado en S08) | Pexels License | No, pero el curso **siempre atribuye** | No vender sin modificar; no implicar respaldo de personas identificables | https://www.pexels.com/license/ |
| **Pixabay** (usado en S08) | Pixabay Content License | No (el curso atribuye) | Igual que Pexels; no usar marcas o personas de forma engañosa | https://pixabay.com/service/license-summary/ |
| **Unsplash** | Unsplash License | No (el curso atribuye) | No compilar para un servicio competidor | https://unsplash.com/license |
| **Wikimedia Commons** | Varía por archivo (CC BY, CC BY-SA, dominio público) | **Sí**, según el archivo | CC BY-SA obliga a compartir igual las obras derivadas: evitar recortar o editar | https://commons.wikimedia.org |
| **Logo CUC** | Marca institucional de la Universidad de la Costa | Uso institucional del docente | **Embeberlo en base64 desde un archivo oficial**, no por hotlink a Wikipedia | Oficina de comunicaciones CUC |
| **Capturas de terminal propias** | Propiedad del curso | — | Sin datos personales, IP públicas reales ni tokens | — |

Formato de pie para fotos: `Foto: <autor> — <plataforma> (<licencia>, uso libre)` (ya en uso en S08).

## 4. Tipografías
| Fuente | Licencia | Uso |
|---|---|---|
| Fraunces, IBM Plex Sans, IBM Plex Mono (labs e `index.html`) | SIL Open Font License 1.1 | Libre, incluso embebida. Para que funcione sin conexión se embebe un subconjunto WOFF2 o se cae a la fuente del sistema |
| Segoe UI / Arial (decks actuales) | Fuentes del sistema | No se distribuyen; solo se referencian |

## 5. Voz sintética, narración y notas
| Opción | Términos | Calidad (es-CO) | Funciona en esta sesión cloud | Comentario |
|---|---|---|---|---|
| **Microsoft Edge TTS** (`edge-tts`, voces `es-CO-SalomeNeural` / `es-CO-GonzaloNeural`) | Servicio de lectura en voz alta de Edge, sin licencia comercial explícita; zona gris para redistribución | Alta | **No** (endpoint bloqueado por el proxy, 403) | Probablemente la voz de los videos actuales (AAC a 24 kHz). Aceptable para material educativo sin fines de lucro; para máxima tranquilidad, usar Azure AI Speech |
| **Azure AI Speech** (mismas voces neurales) | Licencia comercial; capa gratuita F0 con cuota mensual de caracteres (cifra a verificar en el portal) | Alta | No (requiere clave e internet) | Opción formal recomendada si se quiere licencia clara |
| **Piper** (offline, ONNX) | Software MIT; **cada voz tiene su propia licencia** (ver el `MODEL_CARD`) | Media | No (modelos en Hugging Face, bloqueado) | Respaldo offline |
| **espeak-ng** | GPL-3.0 | Baja (robótica) | Instalable | Solo para pruebas de sincronía |

**Conclusión:** los MP4 no se pueden generar en esta sesión por la red. La Fase 2 deja `herramientas/generar-videos` para correr en tu computador con `edge-tts` (o Azure si configuras una clave).

**Notas/narración:** el texto de narración es **obra propia del curso**. Se versiona en el repo junto a cada deck, con cada cifra citada `[cite:N]` contra la lista de fuentes de esa semana (regla 2 de `CLAUDE.md`).

---

## 6. Recursos actuales del repo que hay que corregir por licencia o autonomía
| Dónde | Problema | Acción en la Fase 2 |
|---|---|---|
| S01–S03, S07, `index.html` | Logo CUC por hotlink a Wikipedia | Embeber en base64 |
| S01–S03 | Logos AWS/Azure/GCP/Oracle por hotlink a Wikimedia (marcas) | Retirar o reemplazar por etiquetas genéricas, salvo en los casos que exigen la marca, y entonces embebidos |
| S04 portada | Logos de proveedores en la portada | Retirar (`STANDARDS §6`) |
| S04 | AWS Architecture Icons embebidos (uso permitido) | Mantener donde el caso sea AWS; añadir el pie `Íconos: AWS Architecture Icons` |
| S01–S04 | Sin pie de fuente ni de atribución por diapositiva | Agregar la clase `.src` en cada diapositiva |
