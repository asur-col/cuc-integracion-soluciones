# Guía de autor — presentaciones semanales (plantilla v2)

Esta guía es **obligatoria** para quien produzca o modifique una semana del curso *Integración de Soluciones para Plataformas Cloud* (CUC 2026-2), sea una persona o un agente de IA. Complementa `STANDARDS.md` y `CLAUDE.md`.

## 1. Qué se entrega por semana

Carpeta `semanas/SXX/` con:

| Archivo | Contenido |
|---|---|
| `semana.json` | Metadatos, títulos de las 4 partes, narraciones de portada, divisorias y fuentes, y la lista numerada de fuentes |
| `parte1.html` … `parte4.html` | Las diapositivas de contenido de cada parte, una `<section>` por diapositiva |

El constructor genera en la raíz el HTML autónomo `<archivo>.html`, con portada, divisorias "Parte X de 4", cabeceras, logo, pie, numeración, fuentes citadas, tipografía, íconos y narración embebidos:

```bash
python3 herramientas/construir.py SXX                    # construye
node herramientas/auditar.mjs <archivo>.html --capturas /tmp/capturas-SXX   # audita y captura
node herramientas/generar-pdf.mjs <archivo>.html          # PDF
```

**Nunca se edita a mano el HTML generado.** Se editan las fuentes y se reconstruye.

## 2. Estructura y cantidades (estándar)

- **4 partes de ~15 minutos**; cada parte es un video independiente.
- **14 diapositivas de contenido por parte** (13 a 15 aceptable), 56 en total.
- **Duración por parte: 14 a 16 min** a 135 palabras por minuto. En la práctica, **125–150 palabras de narración por diapositiva de contenido** y unas 1.850–2.050 palabras por parte. El auditor calcula y avisa.
- **Al menos 13 de 14 diapositivas por parte con gráfico real** (diagrama, topología, flujo, gráfico de datos), dibujado en SVG propio. Una tabla o una terminal no cuentan como gráfico: úsalas con moderación (máximo 1 por parte).
- Por semana, como mínimo: **1 caso colombiano real con fuente**, **2 mini-retos** pausables ("Pausa el video…"), **1 pregunta abierta a la clase**, y una diapositiva de **síntesis al final de cada parte**. La Parte 1 incluye un **mapa de la sesión**. La Parte 4 cierra con la síntesis de la semana y el **puente a la semana siguiente**.
- **Los laboratorios están fuera del alcance** (instrucción del docente, 4-oct-2026): no se diseñan, no se enlazan y no se promete ninguno. Cuando haga falta lo práctico, se muestra como demostración conceptual dentro del deck (comandos ilustrativos o capturas dibujadas).
- El hilo conductor del curso es **CaribeMart**, el caso del proyecto de aula (`proyectos/proyecto-aula-corte1.html`): cadena colombiana de retail con 60 almacenes, datacenter principal en Barranquilla y respaldo pasivo en Bogotá, e-commerce con picos en el Día sin IVA. Es ficticio y se presenta como "caso del curso"; no reemplaza el caso colombiano real con fuente.

## 3. `semana.json`

```json
{
  "semana": 3,
  "etiqueta_semana": "Semana 3",
  "archivo": "2026-2-S03-integracion-soluciones-redes-interconectividad",
  "titulo": "Redes e interconectividad multicloud",
  "unidad": "Unidad 1",
  "subtitulo": "Direccionamiento, túneles, enlaces dedicados y soberanía del dato",
  "narracion_portada": "Bienvenidos a la semana tres… (40–70 palabras)",
  "partes": [
    {"titulo": "Direccionamiento sin colisiones", "resumen": "Una o dos frases que se muestran en la divisoria.", "narracion": "Parte uno… (50–80 palabras: qué veremos y por qué importa)"},
    {"titulo": "…", "resumen": "…", "narracion": "…"},
    {"titulo": "…", "resumen": "…", "narracion": "…"},
    {"titulo": "…", "resumen": "…", "narracion": "…"}
  ],
  "narracion_fuentes": "Todas las fuentes citadas quedan en esta última diapositiva… (15–30 palabras)",
  "fuentes": [
    {"n": 1, "ref": "NIST SP 800-145, The NIST Definition of Cloud Computing (2011)", "url": "https://csrc.nist.gov/pubs/sp/800/145/final"}
  ]
}
```
- El **título oficial** sale del calendario de `index.html` y **no se cambia**.
- Las fuentes se numeran desde 1. El constructor avisa si citas un número que no existe o si una fuente nunca se cita: ambas cosas deben quedar en cero.

## 4. Formato de una diapositiva (`parteN.html`)

```html
<section data-kicker="Topología" data-titulo="Título corto y afirmativo (máx. ~70 caracteres)"
         data-sub="Subtítulo opcional de una línea (máx. ~120 caracteres)"
         data-fuente="Basado en: NIST SP 800-207 [cite:4] · Diagrama: elaboración propia">
  <svg viewBox="0 0 1180 500"> … </svg>
  <aside class="narracion">Texto que dice la voz sintética… [cite:4]</aside>
</section>
```

Mira `herramientas/ejemplo/parte-ejemplo.html`, que trae 4 patrones listos:
- **A. Diagrama a pantalla completa:** `<svg viewBox="0 0 1180 500">` directo en la sección. Es el patrón preferido para topologías de red.
- **B. Diagrama + notas:** `<div class="fila"><div class="c-60 lienzo"><svg viewBox="0 0 720 500">…</svg></div><div class="c-40 col">… .nota …</div></div>`.
- **C. Cifras grandes:** `.cifra` + `.cifra-cap`, siempre con `[cite:N]`. Combínalo con un gráfico de barras SVG para que cuente como gráfico.
- **D. Mini-reto:** `.reto` + `.nota.dorada` + ilustración SVG.

Otras clases disponibles: `.nota`, `.nota.dorada`, `table.tabla`, `.terminal` (con `<span class="p">$</span>`, `.c` para comentario, `.ok`), `ul.lista`, `.pie-lienzo`, `code`, y columnas `.c-50`, `.c-70`/`.c-30`.

## 5. Reglas de diseño gráfico

- **Área útil: 1180 × 500 px.** Dibuja dentro del `viewBox` con márgenes de 10 px. Si algo se sale, el motor amplía el `viewBox` (no recorta), pero eso encoge todo y el auditor lo marca como problema: corrígelo.
- **Tamaños mínimos dentro de SVG:** etiquetas 15–16, títulos de zona 18–20 en negrita, notas secundarias 14 como mínimo. El auditor rechaza texto renderizado por debajo de 13 px.
- **Paleta:** vino `#A6192E` (principal), vino oscuro `#7E1223`, dorado `#D4AF37` (relleno/acento) y dorado oscuro `#9C7B16` (texto y trazos dorados, por contraste), texto `#2A2A2A`, gris `#5E5E5E`, tintes `#F9EEF0` (vino) / `#FBF6E7` (dorado) / `#F4F4F4` (gris), verde `#2E7D4F` (correcto) y rojo `#B3261E` (error). No uses otros colores salvo para datos de una gráfica que lo requiera.
- **Flechas:** usa los marcadores comunes `marker-end="url(#fl-vino)"`, `#fl-dorado`, `#fl-gris`, `#fl-negro` y `#fl-verde`. **No definas `<marker>` ni `id` propios**: los ids se repiten entre diapositivas y se rompen. Si de verdad necesitas un `id` (por ejemplo un gradiente), ponle el prefijo `sXXpNdM-`.
- **Íconos (biblioteca propia):** `<use href="#i-NOMBRE" x y width height color="#A6192E"/>`. Disponibles: `router`, `switch`, `firewall`, `servidor`, `bd`, `nube`, `usuario`, `equipo`, `laptop`, `movil`, `internet`, `balanceador`, `contenedor`, `cluster`, `pod`, `cola`, `evento`, `api`, `gateway`, `candado`, `llave`, `escudo`, `edificio`, `datacenter`, `engranaje`, `documento`, `codigo`, `git`, `pipeline`, `alerta`, `reloj`, `dinero`, `grafica`, `ojo`, `ia`, `funcion`, `registro`, `region`, `sensor`, `check`, `x`, `pregunta` y `colombia`. Tamaño típico entre 48 y 72. Pon siempre una etiqueta de texto debajo del ícono.
- **Gráficos de red (los favoritos del docente):** zonas con borde punteado o tintado (sede, región, VPC/VNet genérica, clúster), nodos con íconos y etiquetas, enlaces etiquetados (protocolo, ancho de banda, cifrado), direcciones IP/CIDR de ejemplo (RFC 1918) y leyenda cuando hay más de dos tipos de enlace.
- **Variedad:** no repitas el mismo esquema (por ejemplo "tres cajas con flechas") en diapositivas seguidas. Alterna topología, secuencia temporal (diagrama de secuencia), flujo, línea de tiempo, gráfico de barras, matriz 2×2, antes/después y árbol de decisión.
- **Prohibido:** tarjetas decorativas con un ícono y texto como "relleno", imágenes externas o por hotlink, logos de proveedores en la portada, fotos con derechos y figuras copiadas de libros (se redibujan y se cita "Basado en").
- **Texto en pantalla:** mínimo. Como máximo dos bloques cortos de texto HTML por diapositiva. La explicación va en la narración.

## 6. Reglas de contenido

1. **Concepto genérico de industria primero**; los proveedores (AWS, Azure, Google Cloud, OCI y otros) aparecen como **ejemplos**. **No hagas tablas de equivalencias de nombres de servicios entre proveedores** (regla 3 de `CLAUDE.md`). Si un concepto existe igual en todas las nubes, una frase basta.
2. **No inventes ni redondees cifras.** Toda cifra, fecha, empresa o caso lleva `[cite:N]` en la narración y, si aparece en pantalla, también en la diapositiva. La fuente debe ser verificable y, en lo posible, primaria (documentación oficial, norma, regulador, informe del autor original, comunicado de la empresa). **Verifica cada fuente con búsqueda web antes de usarla.** Si no puedes verificar un dato, no lo uses.
3. Para S01–S04, el **guion docente** en `guiones/` es la fuente de verdad del contenido y de sus cifras (que ya traen fuente). Comprímelo o expándelo, pero no lo contradigas. Si una cifra del deck viejo no tiene fuente, verifícala o retírala.
4. **Caso colombiano real** con fuente (empresa, entidad pública, regulación, incidente, infraestructura). Nada de casos inventados presentados como reales.
5. **Registro:** español de Colombia, docente, pregrado de 8.º semestre. Se tutea a la clase en plural ("ustedes", "fíjense", "piensen").

## 7. Reglas de narración (voz sintética es-CO)

- Es lo que **dice** el docente, no lo que se lee en pantalla. Explica el diagrama recorriéndolo ("a la izquierda…", "sigan la flecha vino…") y cierra cada diapositiva con la idea clave o la transición a la siguiente.
- Usa frases de 15 a 25 palabras. Nada de viñetas, markdown, emojis, URL ni símbolos que la voz no lea bien (→, /, &, ±, ~, paréntesis largos). Escribe "por ciento" o usa "%" pegado al número. Las siglas van tal como se pronuncian en español (API, VPN, BGP); la primera vez dilas completas ("red privada virtual, VPN").
- `[cite:N]` se puede poner en la narración: el constructor lo quita del audio y lo usa para validar.
- Las narraciones de las divisorias presentan la parte. La de la portada da la bienvenida y presenta el tema de la semana.

## 8. Control de calidad antes de entregar (obligatorio)

1. `python3 herramientas/construir.py SXX` → **sin AVISO**.
2. `node herramientas/auditar.mjs <archivo>.html --capturas /tmp/capturas-SXX` → **"✓ sin problemas de maquetación"**, 4 partes entre 13.5 y 16.5 min, y al menos 90 % de las diapositivas de contenido con gráfico.
3. **Mira las capturas**, todas, con la herramienta de lectura de imágenes. Busca textos que se salen de sus cajas o rectángulos, flechas que no tocan su nodo, etiquetas encimadas con líneas, zonas vacías desproporcionadas y diagramas ilegibles. El auditor no detecta todo: el ojo manda.
4. Revisa que el `<title>`, la portada y los títulos de las partes sean coherentes con el título oficial.
5. No modifiques `index.html`, otras semanas ni los archivos de `herramientas/`. Si encuentras un fallo en la plantilla, repórtalo en tu entrega.
