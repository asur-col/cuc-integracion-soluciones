# ESTÁNDAR DE PRESENTACIONES — Integración de Soluciones para Plataformas Cloud

**Curso:** Integración de Soluciones para Plataformas Cloud · CUC · 2026-2
**Docente:** Ing. Rodolfo J. Cañas C.
**Propósito:** este documento es el estándar obligatorio para producir o actualizar cualquier presentación del curso. Toda presentación nueva o rediseñada debe cumplirlo en su totalidad.

---

## 1. Filosofía: presentación, no documento

Una presentación se **mira y se escucha**; no se lee. La regla de oro:

> **Poco texto, muchas imágenes.** El slide apoya al docente; no lo reemplaza.

- Máximo 2 bloques cortos de texto por slide (una frase o cita, no párrafos).
- Ningún slide de contenido puede ser "solo texto": siempre debe existir un elemento visual dominante (diagrama, topología, gráfico, comparativa visual o imagen).
- Si una idea cabe en un diagrama, se dibuja: no se describe con texto.

## 2. Contenido: investigado, nunca inventado

- Todo concepto, definición o cifra debe provenir de **fuentes confiables**: documentación oficial de proveedores (AWS Docs, Microsoft Learn, Google Cloud Docs), estándares (NIST, IEEE, IETF), reportes de industria (Flexera, Gartner, Bain, MarketsandMarkets) y "learnings" oficiales.
- **Neutralidad de proveedor:** no amarrar el curso a un solo proveedor (p. ej. solo AWS). Tomar conceptos y fuentes de todo el ecosistema: AWS, Azure, Google Cloud, IBM, Red Hat, Cloudflare, NIST, Fortinet, etc. En los diagramas usar etiquetas genéricas ("Nube A", "Proveedor B") salvo que el caso exija una marca.
- Toda cifra lleva su cita `[cite:N]` y corresponde a una entrada de la slide de fuentes.

## 3. Visuales: qué usar y cuándo

| El contenido amerita… | Usar |
|---|---|
| Arquitectura o conectividad | Diagrama de red con íconos (routers, switches, firewalls, nubes, servidores, usuarios) |
| Multicloud / híbrido | Diagrama cloud con varias nubes y enlaces |
| Procesos o flujos | Diagrama de flujo con íconos y flechas etiquetadas |
| Comparativas | Tabla o comparativa visual de dos carriles (antes/después) |
| Tendencias de mercado | Gráfico de barras o cifras grandes con fuente |
| Concepto abstracto | Imagen real de referencia (ver §4) |
| Casos de uso | Topologías reales o casos ilustrativos dibujados (con nombres genéricos) |

## 4. Imágenes: uso, propiedad y atribución

- Preferir imágenes de **uso libre u oficiales**. Si la mejor imagen no es libre, igual puede usarse **reconociendo al propietario**.
- Toda imagen o diagrama lleva **pie de página con atribución**: fuente y URL donde se consigue. Esto enriquece la presentación y la hace más presentable y verificable.
- Los diagramas de elaboración propia se marcan como tales y se acompañan del "Basado en: <fuente oficial> — <URL>".
- Formato del pie (clase `.src` en la plantilla): `Fuente: NIST SP 800-207 — nist.gov/publications/zero-trust-architecture · Diagrama: elaboración propia`.

## 5. Marca: solo la universidad

- **Único logo permitido:** el de la Universidad de la Costa (CUC), en portada (grande) y esquina superior derecha de cada slide (pequeño).
- **Sin logos ni nombres de proveedores de nube en la página 1** (ni AWS, ni Azure, ni Google Cloud, ni ningún otro). La portada lleva únicamente: logo CUC, etiqueta de semana/unidad, título, subtítulo, curso, docente y período.
- Paleta institucional: vino `#A6192E`, dorado `#D4AF37`, tintes `#f9eef0` / `#fbf6e7`.
- Tipografía y plantilla: la base HTML aprobada del curso (1280×720, navegación por teclado, barra de progreso, pie con docente · curso · período y numeración `NN / NN`).

## 6. Estructura obligatoria de cada semana

1. **Portada** — solo logo CUC (ver §5).
2. **Mapa de la sesión** — 4 actos que resumen el recorrido.
3. **Contenido visual** — un visual dominante por slide, texto mínimo, citas `[cite:N]`.
4. **Caso de uso o topología real** — al menos uno por semana.
5. **Pregunta a la clase** — una pregunta abierta para discusión.
6. **Fuentes citadas** — lista numerada con nombre de fuente y URL; coincide con las citas del deck.

## 7. Repositorio y nomenclatura

- Repo: `asur-col/cuc-integracion-soluciones` (GitHub, rama `main`, servido por GitHub Pages).
- Archivos: `2026-2-SXX-integracion-soluciones-<tema-en-minusculas-con-giones>.html` (mismo nombre para el `.pdf` si existe).
- Cada HTML es **autónomo** (CSS, JS y logo CUC embebidos): debe abrirse sin conexión.
- Los cambios se suben en un solo commit por lote con mensaje descriptivo (p. ej. `Rediseño visual S01–S05 + estándar de presentaciones`).

## 8. Checklist antes de publicar

- [ ] Portada sin logos ni nombres de proveedores; solo CUC.
- [ ] Ningún slide de contenido es solo texto.
- [ ] Cada cifra tiene su `[cite:N]` y aparece en "Fuentes citadas".
- [ ] Toda imagen/diagrama tiene pie con fuente + URL o marca "elaboración propia".
- [ ] Fuentes variadas (≥3 proveedores/instituciones distintas por semana).
- [ ] El archivo abre sin conexión y navega con flechas del teclado.
- [ ] Nombre de archivo conforme a §7 y commit con mensaje descriptivo.

---
*Versión 1.0 — Septiembre 2026. Cualquier modificación a este estándar se discute y versiona en este mismo repositorio.*
