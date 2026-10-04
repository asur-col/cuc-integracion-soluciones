# Plan para continuar en local (Claude local + tu computador)

**Estado al 4-oct-2026:** la Fase 2 quedó **suspendida a petición del docente** tras la Oleada 0 (herramientas). Se lanzaron 14 subagentes para las semanas 1–6 y 9–17 y se detuvieron antes de escribir contenido: **no existe ninguna diapositiva nueva**. Los decks publicados (S01–S04, S07, S08) siguen como estaban.

**Decisiones del docente ya tomadas**
- Alcance: **las 17 semanas del calendario**, empezando por la semana 1 y avanzando en orden.
- **Activas en `index.html`: semanas 1 a 9.** Las semanas 10 en adelante se crean pero quedan **desactivadas** (tarjeta gris, sin enlace) hasta que el docente las publique.
- **Solo diapositivas con su narración (guion).** Los **videos los genera el docente en su computador** con `herramientas/generar-videos.py` (voz `es-CO-GonzaloNeural`, la de los videos actuales; no se generan videos en sesiones cloud).
- **Laboratorios fuera de alcance.** No se diseñan ni se enlazan; no se tocan `laboratorios/` ni sus tarjetas en `index.html`.
- Los títulos del calendario de `index.html` son oficiales y no cambian.

## 1. Orden de trabajo recomendado
1. **S01 → S06** (Unidad 1, en orden). S01–S04 se reconstruyen desde sus guiones (`guiones/`, fuente de verdad); S05 y S06 son nuevas.
2. **S07 y S08** (ya publicadas): migrarlas al formato `semanas/SXX/` (S07 ya tiene sus 4 partes; S08 hay que partirla en 4) y corregir los defectos listados en `docs/analisis-tematico.md §3`.
3. **S09** (Kubernetes; ya se dictó sin deck).
4. **S10 → S16–17** (nuevas, desactivadas).
5. Cierre: `index.html`, `CLAUDE.md`, `STANDARDS.md` v2.0, PDF de cada semana.

## 2. Cómo se trabaja una semana (receta)
1. Leer `herramientas/GUIA-AUTOR.md` y mirar `herramientas/ejemplo/parte-ejemplo.html`.
2. Copiar el deck viejo (si existe) fuera del repo para consultarlo: la construcción lo sobrescribe.
3. Crear `semanas/SXX/semana.json` y `parte1.html … parte4.html`.
4. `python3 herramientas/construir.py SXX` → sin AVISOS (citas ↔ fuentes cuadradas).
5. `node herramientas/auditar.mjs <archivo>.html --capturas /tmp/cap-SXX` → "✓ sin problemas", 4 partes de 13.5 a 16.5 min, ≥ 90 % de diapositivas con gráfico. **Mirar las hojas de contacto** (`hoja-*.png`).
6. `node herramientas/generar-pdf.mjs <archivo>.html`.
7. Activar la semana en `index.html` (si es 1–9) con enlaces a HTML y PDF. El enlace al video se agrega cuando el docente sube los MP4.
8. Commit por semana (o por bloque de semanas) en la rama de trabajo.

Con varios subagentes en paralelo (modelo Sonnet), **uno por semana**, con el encargo de esta receta; el modelo principal audita cada entrega (conteos, capturas, precisión técnica, fuentes). Los briefs de cada semana están en la §3.

## 3. Brief por semana
Todas: 4 partes × ~14 diapositivas, narración 125–150 palabras por diapositiva, caso colombiano real con fuente (si no se verifica, no se usa), 2 mini-retos, 1 pregunta abierta, CaribeMart como hilo, puente a la semana siguiente, sin tablas de equivalencias de nombres entre proveedores.

| Sem. | Archivo (raíz) | Título oficial | Estado en `index.html` | Insumos y puntos de atención |
|---|---|---|---|---|
| 1 | `2026-2-S01-integracion-soluciones-introduccion-multicloud` | Introducción a multicloud | **Activa** | Guion S01. Verificar o retirar «Bancolombia → AWS, ~1.000 apps, US$130 M» (sin fuente en el deck viejo). NIST 800-145, ISO/IEC 22123-1. Identidad solo como problema (el mecanismo es S04). |
| 2 | `…-S02-integracion-soluciones-patrones-integracion` | Patrones de integración | **Activa** | Guion S02 (EIP, DoorDash, CDC, strangler fig). Database@X como UN caso ancla. Caso colombiano: verificar Bre-B / PSE antes de usar. |
| 3 | `…-S03-integracion-soluciones-redes-interconectividad` | Redes e interconectividad multicloud | **Activa** | Guion S03. **Eliminar la tabla «VCN · VPC · VNet».** Ley 1581, Decreto 1377, SIC (fuentes en `docs/fuentes-recursos.md §1.3`). Más topologías de red. |
| 4 | `…-S04-integracion-soluciones-gobierno-multicloud` | Gobierno multicloud y migración | **Activa** | Guion S04 (ignorar la referencia al taller de las 7 Rs). **Portada sin logos de proveedores.** ISO/IEC 19941. Acuerdo Marco de Nube Pública (verificar). |
| 5 | `…-S05-integracion-soluciones-resiliencia-continuidad` | Resiliencia y continuidad de negocio multicloud | **Activa** | Nueva. Disponibilidad compuesta (cálculo propio con fórmula), RPO/RTO, 4 estrategias de DR, CAP/PACELC, caso CrowdStrike 19-jul-2024 y un postmortem oficial (verificar fecha y causa). |
| 6 | `…-S06-integracion-soluciones-repaso-unidad1` | Repaso Unidad 1 | **Activa** | Nueva. Integra S01–S05 y guía la Rúbrica U1 (`proyectos/proyecto-aula-corte1.html`). No resolver el proyecto: usar un caso análogo. |
| 7 | `…-S07-integracion-soluciones-microservicios` | Arquitecturas de microservicios | **Activa** | Ya publicada: migrar al formato nuevo, **corregir 10 SVG recortados** (diapositivas 10, 16, 20, 32, 33, 38, 44, 51, 53, 55), agregar narración versionada, 1 diapositiva de serverless y 1 de OWASP API Security. |
| 8 | `…-S08-integracion-soluciones-contenedores` | Contenedores y registro de imágenes | **Activa** | Ya publicada: partir en 4 partes, reemplazar las capturas de Play with Docker (descontinuado), cambiar tarjetas con ícono genérico por diagramas reales, NIST SP 800-190. Mantener las fotos con atribución. |
| 9 | `…-S09-integracion-soluciones-kubernetes` | Orquestación de contenedores con Kubernetes | **Activa** (ya se dictó) | Nueva. Verificar todo YAML/comando en kubernetes.io. Caso colombiano o CNCF end-user (decir cuál es). |
| 10 | `…-S10-integracion-soluciones-cicd` | Cierre de Unidad 2: pipeline CI/CD genérico con GitHub Actions | Desactivada | Nueva. DORA, OIDC con la nube, push vs. GitOps (OpenGitOps), blue/green y canary. |
| 11 | `…-S11-integracion-soluciones-repaso-unidad2` | Repaso Unidad 2 | Desactivada | Nueva. El enunciado de la Rúbrica U2 **no está definido**: presentar solo «ejes esperados» y decir que lo libera el docente. |
| 12 | `…-S12-integracion-soluciones-iac` | Infraestructura como código multicloud | Desactivada | Nueva. Terraform/OpenTofu (licencia BSL 2023, verificar), estado remoto, políticas como código. Sin lab ni demo «floci». |
| 13 | `…-S13-integracion-soluciones-service-mesh` | Service mesh e interconexión entre clústeres multicloud | Desactivada | Nueva. Istio (ambient: verificar estado actual), Linkerd, mTLS, SPIFFE, multiclúster; confirmar el nombre vigente del producto de malla de Google. |
| 14 | `…-S14-integracion-soluciones-observabilidad` | Observabilidad multicloud | Desactivada | Nueva. OpenTelemetry, Prometheus/Grafana, SLO, AIOps con límites honestos; cifras solo de CNCF u otra fuente primaria. |
| 15 | `…-S15-integracion-soluciones-seguridad-finops` | Seguridad multicloud y FinOps | Desactivada | Nueva. SLSA, SBOM, Sigstore, IA en seguridad con límites, FOCUS 1.2 (29-may-2025), FinOps Framework; verificar cada cifra y la circular de la Superintendencia Financiera antes de citarla. |
| 16–17 | `…-S16-integracion-soluciones-repaso-sustentacion` | Repaso + entrega/sustentación del proyecto final | Desactivada | Nueva. Un solo deck («Semanas 16–17»). Rúbrica U3 sin definir: solo «ejes esperados». |

## 4. Tareas que me quedaron pendientes en la sesión cloud
- **No** se modificó `index.html`: cuando existan los decks hay que (a) pasar el contador a «X de 17 publicadas», (b) listar las 17 semanas con enlaces a HTML y PDF en las semanas 1–9, (c) dejar las semanas 10–17 como tarjetas `pending` sin enlace, con el título oficial del calendario. Los títulos y el calendario no cambian.
- Verificar con el docente que `es-CO-GonzaloNeural` coincide con la voz de los videos actuales (se infirió por el tono medio de ~94 Hz de la voz de S07 y por el AAC a 24 kHz de `edge-tts`; no se pudo confirmar sin acceso al servicio). Si no coincide, probar `es-CO-SalomeNeural` o las voces es-MX/es-ES y ajustar `--voz`.
- Reescribir `STANDARDS.md` a v2.0 (hoy pide 17–20 diapositivas) y marcar `TEMARIO-…md` como desactualizado frente a `index.html` (S05 = Resiliencia, S06 = Repaso U1, S07 = Microservicios).
- Logo: `herramientas/assets/logo-cuc.png` salió del base64 que ya estaba embebido en el deck de S08 (300×100). Si hay un logo oficial en SVG o de mayor resolución, reemplazarlo ahí (un solo lugar).
- Si Playwright de Node no está disponible, `npm i -g playwright && npx playwright install chromium`.

## 5. Videos (los hace el docente, en su computador)
Instrucciones completas en `herramientas/README.md`. Resumen:
```bash
pip install -r herramientas/requirements.txt && python -m playwright install chromium
python herramientas/generar-videos.py S01          # 4 MP4 en videos/
python herramientas/generar-videos.py S01 S02 S03  # varias semanas
```
Después: `git add videos/` y reemplazar en `index.html` «video: próximamente» por los 4 enlaces (`Ver video Parte 1 →` … `Parte 4 →`, mismo formato que la semana 7). La narración de cada diapositiva vive dentro del HTML (`#narracion`) y se puede leer en clase pulsando **N**.
