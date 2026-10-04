# CLAUDE.md — Guía para asistentes de IA en este repositorio

## Qué es este repositorio

Material del curso **Integración de Soluciones para Plataformas Cloud** (Ingeniería de Sistemas, CUC, Colombia, 2026-2): presentaciones HTML/PDF por semana, videoclases narradas, laboratorios y — desde este commit — guiones docentes.

Contexto de la sesión: clase semanal presencial de 3 horas (sábados, ~20 estudiantes): hasta 1 hora de teoría en vivo + laboratorio práctico. Registro docente, español de Colombia, nivel pregrado.

## Carpeta `guiones/` — la fuente de verdad del contenido

Contiene el **guion docente completo** (el texto real que el profesor dicta en clase, no bullets de diapositiva) para las semanas 1–4, diseñado para sostener **45–60 minutos de exposición por semana**:

- `guion-docente-semana1-introduccion-multicloud.md` (~50–55 min)
- `guion-docente-semana2-patrones-integracion.md` (~52–57 min)
- `guion-docente-semana3-redes-interconectividad.md` (~52–56 min)
- `guion-docente-semana4-gobierno-migracion.md` (~56–62 min)

Cada archivo está organizado **por bloques temáticos** (no por slide), con transiciones, ejemplos desarrollados, dos preguntas a la clase, nota de tiempo estimado y lista de fuentes verificadas al final.

## Reglas para trabajar con los guiones

1. **Los guiones son la fuente de verdad de contenido y densidad.** Si actualizas las presentaciones HTML o las narraciones de video, alinea el contenido con el bloque correspondiente del guion — no al revés. Los HTML actuales son soporte visual; los guiones llevan la densidad para la clase en vivo.
2. **No inventes ni redondees cifras.** Toda cifra cuantitativa (porcentajes, dólares, nombres de empresas) ya tiene fuente verificada numerada en cada guion. Si agregas una cifra nueva, busca su fuente y agrégala a la lista. Si actualizas un dato (p. ej. nuevo informe anual de Flexera), actualiza también la fuente.
3. **Regla de contenido del curso: NO comparar nombres de servicios entre proveedores como eje.** Si un concepto existe igual en cualquier nube, una frase basta. El foco es enseñar a decidir y razonar, no a memorizar sinónimos entre proveedores.
4. **Al generar narraciones de video (guiones JSON)**, puedes comprimir el guion docente, pero no agregar afirmaciones cuantitativas que no estén en él con su fuente.
5. **Referencias cruzadas existentes:** los laboratorios ya están publicados en `laboratorios/` (lab-01 sandbox de contenedores — semana 3, lab-02 VPN site-to-site con OPNsense, lab-03 contenedores con Docker Hub — semana 8, Actividad 1 U2, 10%). Los 3 labs comparten la misma identidad visual (Fraunces + IBM Plex, tokens `:root` vino/dorado con soporte de modo oscuro) — cualquier lab nuevo debe reusar ese mismo `<style>`, no el del template de presentaciones.
6. **Lab de la semana 4 (taller de las 7 Rs) retirado del repo (2026-09-26, instrucción directa de Rodolfo):** el antiguo `lab-03-taller-7rs-gobierno-multicloud.html` se eliminó y la numeración se corrió — el lab de contenedores pasó de `lab-04` a `lab-03`. El guion `guiones/guion-docente-semana4-gobierno-migracion.md` todavía menciona `lab-03-taller-7rs-gobierno-multicloud` por nombre — esa referencia quedó obsoleta y hay que revisarla con Rodolfo antes de volver a dictar la semana 4 (el archivo sigue disponible en el historial de git si se necesita restaurar).
7. **Ritmo de exposición asumido:** 130–140 palabras por minuto en español. Si propones recortes, indica qué bloque se comprime y cuánto tiempo se ahorra (cada guion ya incluye instrucciones de recorte a 45–50 min).

## Producción de presentaciones — estándar v2 (desde 4-oct-2026)

**Alcance acordado con Rodolfo:** las 17 semanas del calendario de `index.html` (títulos oficiales, **no se cambian**). Semanas **1–9 activas** en `index.html`; **10–17 se crean pero quedan desactivadas** (tarjeta `pending`, sin enlace) hasta que Rodolfo las publique. **Solo se entregan diapositivas con su narración**; los videos los genera Rodolfo en su computador. **Los laboratorios están fuera de alcance** (no diseñarlos ni enlazarlos).

- **Estándar:** 1 semana = 1 HTML = **4 partes de ~15 min** (divisoria «Parte X de 4» donde va cada corte de video), ~14 diapositivas de contenido por parte (~56), ≥ 90 % con gráfico SVG propio (preferir topologías de red), estilo CUC vino `#A6192E` / dorado `#D4AF37`, caso colombiano real con fuente, 2 mini-retos, pregunta abierta, CaribeMart como hilo conductor, puente a la semana siguiente. Concepto genérico de industria; los proveedores solo como ejemplo. `STANDARDS.md` v1.1 (17–20 diapositivas) está **superado** por `herramientas/GUIA-AUTOR.md`.
- **Fuentes del HTML:** `semanas/SXX/semana.json` + `parte1..4.html`. El HTML de la raíz (`2026-2-SXX-…html`) es **generado**: no se edita a mano.
- **Herramientas** (`herramientas/`, ver su `README.md`): `construir.py` (arma el HTML autónomo con logo, Roboto, íconos y narración embebidos), `auditar.mjs` (conteos, duración por parte, desbordes, SVG recortados, texto < 13 px, etiquetas encimadas, hojas de contacto), `generar-pdf.mjs`, `generar-videos.py` (4 MP4 por semana, voz `es-CO-GonzaloNeural`, a correr **en local**; la sesión cloud no alcanza el servicio de voz).
- **Cómo regenerar:** `python3 herramientas/construir.py S03` → `node herramientas/auditar.mjs <archivo>.html --capturas /tmp/cap-S03` (mirar `hoja-*.png`) → `node herramientas/generar-pdf.mjs <archivo>.html` → (local) `python herramientas/generar-videos.py S03`.
- **Convenciones:** narración 125–150 palabras por diapositiva (135 ppm ⇒ ~15 min por parte); cada cifra con `[cite:N]` ↔ lista de fuentes de la semana; íconos propios `#i-…` y flechas comunes `#fl-…` (no definir `<marker>`/`id` propios); logo CUC embebido (no hotlink); sin tablas de equivalencias de nombres entre proveedores; no inventar cifras ni casos (verificar con búsqueda web o no usar); tecla **N** muestra la narración en clase.
- **Documentos de la Fase 1:** `docs/analisis-tematico.md` (diagnóstico por semana, brechas y mejoras dentro de cada título), `docs/fuentes-recursos.md` (referentes, licencias de íconos/imágenes/voces, cómo citar), `docs/plan-oleadas.md`, **`docs/plan-continuar-local.md`** (plan vigente y brief por semana).

### Estado por semana (4-oct-2026)
| Semanas | Estado |
|---|---|
| S01–S04 | Publicadas en formato **viejo** (16–21 diapositivas, 1 video); por reconstruir al estándar v2 desde sus guiones |
| S05, S06 | **No existen**; por crear (activas) |
| S07 | Publicada con 4 partes y 4 videos; pendiente corregir 10 SVG recortados, narración versionada y 2 diapositivas nuevas |
| S08 | Publicada (55 diapositivas, sin partes/video/PDF enlazado); pendiente partir en 4 y rehacer capturas sin Play with Docker |
| S09 | **No existe** (ya se dictó); por crear (activa) |
| S10–S16/17 | **No existen**; por crear y dejar **desactivadas** |
| Herramientas | Oleada 0 hecha y probada (plantilla, constructor, auditor, PDF, script de videos) |

### Pendientes
Producir S01→S17 en orden (ver `docs/plan-continuar-local.md`); actualizar `index.html` (contador y tarjetas 1–9 activas, 10–17 desactivadas); `STANDARDS.md` v2.0; marcar `TEMARIO-…md` desactualizado frente a `index.html`; confirmar con Rodolfo que la voz por defecto coincide con la de los videos actuales; verificar o retirar la cifra «Bancolombia → AWS» del deck S01; quitar logos de proveedores de la portada de S04 y la tabla de nombres de S03.

## Pendiente conocido (anterior)

Las presentaciones HTML de las semanas 1–3 aún no reflejan la densidad de los guiones (solo la semana 4 fue actualizada con íconos reales y video narrado). La tarea pendiente natural es expandir la narración de cada semana usando su guion como base.
