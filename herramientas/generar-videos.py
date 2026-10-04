#!/usr/bin/env python3
"""Genera los 4 videos MP4 (uno por parte) de una semana: captura + voz sintética + ffmpeg.

Uso (en tu computador, con internet):
    python herramientas/generar-videos.py S01
    python herramientas/generar-videos.py S01 S02 S03          # varias semanas
    python herramientas/generar-videos.py S07 --partes 2,3       # solo algunas partes
    python herramientas/generar-videos.py S01 --voz es-CO-SalomeNeural --velocidad +5%

Opciones:
    --voz         voz de edge-tts (por defecto es-CO-GonzaloNeural, la de los videos actuales del curso)
    --velocidad   ajuste de velocidad de la voz, p. ej. -5% o +5% (por defecto +0%)
    --partes      lista de partes a generar (por defecto 1,2,3,4)
    --sin-voz     modo prueba: silencio con la duración estimada (no usa internet)

Requisitos: Python 3.9+, ffmpeg en el PATH y
    pip install -r herramientas/requirements.txt
    python -m playwright install chromium

Salida: videos/<archivo>-parte1.mp4 … -parte4.mp4 (1920x1080, H.264 + AAC).
El audio de cada diapositiva se guarda en herramientas/.cache-tts/ (se reutiliza si el texto no cambia).
"""
import argparse, asyncio, hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CACHE = RAIZ / "herramientas" / ".cache-tts"
PPM = 135
PAUSA = 0.8      # silencio al final de cada diapositiva (s)
MIN_SIN_NARR = 3.0  # duración de una diapositiva sin narración (s)


def sh(cmd):
    r = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        raise SystemExit(f"Falló: {' '.join(cmd[:6])} …")
    return r.stdout


def duracion(audio):
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(audio)]).strip())


def resolver(clave):
    p = Path(clave)
    if p.suffix == ".html" and p.exists():
        return p.resolve()
    meta = json.loads((RAIZ / "semanas" / clave / "semana.json").read_text(encoding="utf-8"))
    return RAIZ / f"{meta['archivo']}.html"


async def tts(texto, voz, velocidad, destino, sin_voz):
    if sin_voz:
        seg = max(1.0, len(texto.split()) / PPM * 60)
        sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", f"{seg:.2f}", "-q:a", "9", str(destino)])
        return
    import edge_tts
    clave = hashlib.sha1(f"{voz}|{velocidad}|{texto}".encode()).hexdigest()
    CACHE.mkdir(parents=True, exist_ok=True)
    c = CACHE / f"{clave}.mp3"
    if not c.exists() or c.stat().st_size == 0:
        for intento in range(4):
            try:
                await edge_tts.Communicate(texto, voz, rate=velocidad).save(str(c))
                break
            except Exception as e:  # red inestable: reintento con espera
                print(f"   reintento TTS ({e.__class__.__name__})")
                await asyncio.sleep(2 ** intento)
        else:
            raise SystemExit("No se pudo generar la voz (revisa la conexión a internet).")
    shutil.copy(c, destino)


async def capturar(html, carpeta):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        import os
        exe = os.environ.get("CHROMIUM_PATH")  # opcional: usar un Chromium ya instalado
        b = await p.chromium.launch(executable_path=exe) if exe else await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1920, "height": 1080})
        await pg.goto(html.as_uri() + "?captura=1")
        await pg.wait_for_selector('body[data-listo="1"]', timeout=30000)
        narr = await pg.evaluate("window.CURSO.narracion")
        for i in range(len(narr)):
            await pg.evaluate(f"window.CURSO.irA({i})")
            await pg.wait_for_timeout(60)
            await pg.screenshot(path=str(carpeta / f"{i+1:03d}.png"))
        await b.close()
    return narr


async def semana(clave, a):
    html = resolver(clave)
    if not html.exists():
        raise SystemExit(f"No existe {html}. Construye primero: python3 herramientas/construir.py {clave}")
    base = html.stem
    print(f"== {base}")
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        narr = await capturar(html, tmp)
        partes = sorted({int(x) for x in a.partes.split(",")})
        (RAIZ / "videos").mkdir(exist_ok=True)
        for k in partes:
            items = [x for x in narr if x["parte"] == k]
            if not items:
                continue
            lista = tmp / f"lista{k}.txt"
            clips = []
            for x in items:
                n = x["n"]
                png = tmp / f"{n:03d}.png"
                clip = tmp / f"clip{n:03d}.mp4"
                texto = (x.get("texto") or "").strip()
                if texto:
                    mp3 = tmp / f"{n:03d}.mp3"
                    await tts(texto, a.voz, a.velocidad, mp3, a.sin_voz)
                    seg = duracion(mp3) + PAUSA
                    entrada_audio = ["-i", str(mp3)]
                    filtro = ["-af", f"apad=pad_dur={PAUSA}"]
                else:
                    seg = MIN_SIN_NARR
                    entrada_audio = ["-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono"]
                    filtro = []
                sh(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30", "-i", str(png), *entrada_audio,
                    *filtro, "-t", f"{seg:.3f}", "-c:v", "libx264", "-tune", "stillimage", "-preset", "medium", "-crf", "22",
                    "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "96k", "-ar", "24000", "-ac", "1", str(clip)])
                clips.append(clip)
                print(f"   parte {k} · diapositiva {n} · {seg:.1f} s")
            lista.write_text("".join(f"file '{c.as_posix()}'\n" for c in clips))
            salida = RAIZ / "videos" / f"{base}-parte{k}.mp4"
            sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lista), "-c", "copy",
                "-movflags", "+faststart", str(salida)])
            print(f"   ✓ {salida.relative_to(RAIZ)} ({duracion(salida)/60:.1f} min)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("semanas", nargs="+")
    ap.add_argument("--voz", default="es-CO-GonzaloNeural")
    ap.add_argument("--velocidad", default="+0%")
    ap.add_argument("--partes", default="1,2,3,4")
    ap.add_argument("--sin-voz", action="store_true")
    a = ap.parse_args()
    if not shutil.which("ffmpeg"):
        raise SystemExit("Falta ffmpeg en el PATH (https://ffmpeg.org/download.html).")
    for s in a.semanas:
        asyncio.run(semana(s, a))


if __name__ == "__main__":
    main()
