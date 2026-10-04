# Plan de producción por oleadas — Fase 2

> **Actualización 4-oct-2026:** el docente aprobó producir las **17 semanas empezando por la 1**, con las semanas **1–9 activas** y **10–17 creadas pero desactivadas**; entrega **solo diapositivas + narración** (los videos los genera él en local) y sin laboratorios. La Oleada 0 está hecha y la producción quedó **suspendida**; el plan operativo vigente está en `docs/plan-continuar-local.md`. Las oleadas de abajo se conservan como referencia del orden original (el orden vigente es S01→S17).

Ordenado por **urgencia del calendario**. Hoy es el 4-oct-2026; la próxima clase es la S10, el sábado 17-oct.

## Estándar de producción propuesto (STANDARDS v2.0, basado en S07)
- **1 semana = 1 HTML = 4 partes de ~15 min.** Cada parte abre con una diapositiva divisoria "Parte X de 4", que marca el corte de video, y trae unas 13–14 diapositivas de contenido, 56–60 en total.
- Al menos el **90 % de las diapositivas de contenido con gráfico real**: diagrama, topología o flujo, no tarjetas con íconos. Prioridad a los diagramas de red.
- Plantilla única: la de S07, corregida. Lienzo de 1280×720, vino `#A6192E` y dorado `#D4AF37`, logo CUC **embebido**, pie con fuente `.src` y un solo contador de página. El contenido ocupa el alto útil y las cajas usan letra de al menos 15 px.
- **Narración por diapositiva** dentro del mismo HTML (`<script type="application/json" id="narracion">`, con un objeto por diapositiva: texto y `parte`). Son unas 140–150 palabras por diapositiva a 135 ppm, lo que da unos 60 s por diapositiva y ~15 min por parte. Cada parte cierra con su cifra de duración estimada.
- Cada parte incluye 1 caso colombiano en la semana, 1 mini-reto, 1 pregunta a la clase, fuentes `[cite:N]` y cierre de síntesis con puente a la semana siguiente. **Los laboratorios quedan fuera del alcance** (instrucción del 4-oct): solo material académico.
- Concepto genérico de industria primero; la marca del proveedor solo aparece como ejemplo. No se comparan nombres de servicios.

## Oleada 0 — Infraestructura (modelo principal, ~1 sesión)
1. `herramientas/plantilla-semana.html`: plantilla v2, con un ajuste automático del `viewBox` de los SVG que evita los recortes.
2. `herramientas/auditar.mjs`: cuenta diapositivas, gráficos y partes; detecta desbordes y SVG recortados; estima la duración desde la narración; genera la hoja de contactos de capturas.
3. `herramientas/generar-pdf.mjs`: PDF de 16:9, una diapositiva por página (Playwright).
4. `herramientas/generar-videos.py` + `README`: **un solo comando produce los 4 MP4 de una semana** con este flujo: captura → TTS (`edge-tts`, voz es-CO, o Azure) → ffmpeg, a 1080p y AAC.
5. `STANDARDS.md` pasa a la v2.0.

## Oleada 1 — Urgente: U2 en curso (subagentes Sonnet en paralelo)
| Semana | Motivo | Estado en `index.html` |
|---|---|---|
| **S09 Kubernetes** | Ya se dictó sin deck; material de estudio para la Rúbrica U2 | Desactivada hasta que la publiques |
| **S10 CI/CD** | Clase del 17-oct | Desactivada |
| **S11 Repaso U2** | Clase del 24-oct (deck corto si lo apruebas) | Desactivada |
| **S08 Contenedores** | Mejora: partir en 4, rehacer las capturas sin Play with Docker, añadir narración, PDF y videos | Publicada (se actualiza) |

## Oleada 2 — U3 (paralelo, clases del 31-oct al 21-nov)
S12 IaC · S13 Service mesh · S14 Observabilidad · S15 Seguridad y FinOps · S16–17 guía de sustentación. Todas quedan **creadas y desactivadas**.

## Oleada 3 — Correcciones de lo publicado en U2
S07: corregir los 10 SVG recortados, añadir la narración versionada, una diapositiva de serverless y otra de OWASP API, y regenerar el PDF. Los videos solo se rehacen si cambia el contenido.

## Oleada 4 — U1 (ya dictada: material para estudio y para 2027-1)
S01–S04 se reconstruyen al estándar **a partir de sus guiones docentes** (fuente de verdad). Se eliminan las repeticiones (SAML/OIDC, Database@X) y la tabla de nombres por proveedor de S03. Se crean S05 Resiliencia y S06 Repaso U1.

## Oleada 5 — Cierre
Auditoría final de las 17 semanas, `CLAUDE.md` actualizado (estándar, convenciones, cómo regenerar PDF y videos, estado por semana, pendientes) y corrección de la divergencia entre el TEMARIO e `index.html`.

## Control de calidad por entrega de subagente (lo hace el modelo principal)
- [ ] 4 divisorias y 52–56 diapositivas de contenido; al menos el 90 % con gráfico.
- [ ] `auditar.mjs` sin desbordes ni SVG recortados; hoja de contactos revisada a ojo.
- [ ] Duración estimada por parte de 14 a 16 min.
- [ ] Precisión técnica: cada cifra con `[cite:N]` y fuente verificable; sin afirmaciones inventadas.
- [ ] Caso colombiano con fuente; portada solo con el logo CUC.
- [ ] Un commit por oleada en `claude/blissful-lovelace-uxk3q8`.

## Decisiones que necesito antes de arrancar
1. **Semanas de repaso (S06, S11, S16–17):** ¿deck corto de integración + guía de rúbrica, o sin deck?
2. **Prioridad de U1 (S01–S06):** ¿la reconstruimos ahora (oleada 4) o la dejamos para 2027-1?
3. **Voz:** ¿`edge-tts` es-CO (como los videos actuales) o Azure AI Speech con tu clave?
4. **.pptx viejas:** si las tienes, súbelas a `insumos/pptx/` antes de la oleada 1 para mapearlas.
