# Herramientas de producción del curso

| Script | Qué hace |
|---|---|
| `construir.py` | Arma el HTML autónomo de una semana desde `semanas/SXX/` (plantilla v2) |
| `auditar.mjs` | Cuenta diapositivas, gráficos y duración por parte; detecta desbordes, SVG recortados, texto pequeño y etiquetas encimadas; genera capturas y hojas de contacto |
| `generar-pdf.mjs` | PDF de 16:9, una diapositiva por página |
| `generar-videos.py` | **Los 4 MP4 de una semana con un solo comando**: captura de cada diapositiva + voz sintética + ffmpeg |
| `GUIA-AUTOR.md` | Formato de las fuentes y reglas de diseño, contenido y narración |

## Generar los videos en tu computador (Windows, macOS o Linux)

Los videos no se pueden generar en la sesión cloud de Claude porque el servicio de voz está bloqueado por la red. En tu computador:

1. **Instala una sola vez:**
   - Python 3.9 o superior (https://www.python.org) y ffmpeg (Windows: `winget install Gyan.FFmpeg`; macOS: `brew install ffmpeg`).
   - Desde la carpeta del repositorio:
     ```bash
     pip install -r herramientas/requirements.txt
     python -m playwright install chromium
     ```
2. **Genera los 4 videos de una semana:**
   ```bash
   python herramientas/generar-videos.py S01
   ```
   Salen en `videos/2026-2-S01-integracion-soluciones-introduccion-multicloud-parte1.mp4` … `-parte4.mp4`, a 1920×1080.
3. Otras opciones:
   ```bash
   python herramientas/generar-videos.py S01 S02 S03           # varias semanas seguidas
   python herramientas/generar-videos.py S05 --partes 2         # rehacer solo la parte 2
   python herramientas/generar-videos.py S01 --velocidad -5%    # voz un poco más lenta
   ```
   Por defecto la voz es **`es-CO-GonzaloNeural`**, la misma voz masculina colombiana de los videos actuales del curso. El audio de cada diapositiva se guarda en `herramientas/.cache-tts/`, así que si solo cambias una diapositiva, la siguiente corrida solo regenera esa voz.
4. Sube los MP4 (`git add videos/…-parte*.mp4`) y en `index.html` cambia el texto "video: próximamente" de esa semana por los 4 enlaces (`Ver video Parte 1 →` …), con el mismo formato que la semana 7.

## Reconstruir HTML y PDF después de editar una semana

```bash
python3 herramientas/construir.py S03
node herramientas/auditar.mjs 2026-2-S03-integracion-soluciones-redes-interconectividad.html --capturas /tmp/cap-S03
node herramientas/generar-pdf.mjs 2026-2-S03-integracion-soluciones-redes-interconectividad.html
```
`auditar.mjs` y `generar-pdf.mjs` necesitan Playwright para Node: `npm i -g playwright && npx playwright install chromium` (o `npm i playwright` dentro del repo).

## Modo docente en clase
Abre el HTML de la semana: las flechas ← → navegan y la tecla **N** muestra la narración de la diapositiva actual (sirve como guion en vivo). `#12` en la URL salta a la diapositiva 12.
