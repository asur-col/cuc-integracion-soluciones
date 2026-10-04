#!/usr/bin/env python3
"""Construye la presentación HTML autónoma de una semana a partir de sus fuentes.

Uso:
    python3 herramientas/construir.py S01          # una semana
    python3 herramientas/construir.py todas        # todas las carpetas semanas/S*

Entrada (semanas/SXX/):
    semana.json    metadatos, partes, narraciones de portada/divisorias y fuentes
    parte1.html … parte4.html   diapositivas de contenido (<section> … </section>)
Salida (raíz del repo):
    <archivo>.html  — HTML autónomo (CSS, JS, fuentes, íconos y logo embebidos)

Ver herramientas/GUIA-AUTOR.md para el formato de las fuentes.
"""
import base64, html, json, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
HERR = RAIZ / "herramientas"
PPM = 135  # palabras por minuto de la voz sintética (CLAUDE.md: 130–140)
PAUSA = 0.8  # segundos de silencio por diapositiva en el video

CURSO = "Integración de Soluciones para Plataformas Cloud"


def b64(p):
    return base64.b64encode(Path(p).read_bytes()).decode()


def fuentes_css():
    f = HERR / "assets" / "fonts"
    out = []
    for peso in (400, 500, 700):
        out.append(f"@font-face{{font-family:'Roboto';font-weight:{peso};font-style:normal;"
                   f"src:url(data:font/woff2;base64,{b64(f / f'roboto-latin-{peso}-normal.woff2')}) format('woff2');}}")
    for peso in (400, 700):
        out.append(f"@font-face{{font-family:'Roboto Mono';font-weight:{peso};font-style:normal;"
                   f"src:url(data:font/woff2;base64,{b64(f / f'roboto-mono-latin-{peso}-normal.woff2')}) format('woff2');}}")
    return "\n".join(out)


ATTR = re.compile(r'([\w-]+)\s*=\s*"([^"]*)"')
SEC = re.compile(r"<section\b([^>]*)>(.*?)</section>", re.S)
NARR = re.compile(r'<aside\s+class="narracion"\s*>(.*?)</aside>', re.S)
CITE = re.compile(r"\[cite:(\d+(?:\s*,\s*\d+)*)\]")


def limpiar_narr(t):
    t = re.sub(r"<[^>]+>", " ", t)
    t = CITE.sub("", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def palabras(t):
    return len(t.split())


def cites_en(t):
    out = set()
    for m in CITE.finditer(t):
        out.update(int(x) for x in m.group(1).split(","))
    return out


def construir(clave):
    d = RAIZ / "semanas" / clave
    meta = json.loads((d / "semana.json").read_text(encoding="utf-8"))
    sem = meta["semana"]
    etiqueta_sem = meta.get("etiqueta_semana", f"Semana {sem}")
    logo = "data:image/png;base64," + b64(HERR / "assets" / "logo-cuc.png")
    iconos = (HERR / "plantilla" / "iconos.svg").read_text(encoding="utf-8")
    css = (HERR / "plantilla" / "estilo.css").read_text(encoding="utf-8")
    js = (HERR / "plantilla" / "motor.js").read_text(encoding="utf-8")

    diapos = []  # (html, narracion_texto, parte)
    avisos = []
    citas_usadas = set()
    partes = meta["partes"]
    assert len(partes) == 4, "Cada semana debe tener exactamente 4 partes"

    # Portada (pertenece al video de la Parte 1)
    portada = f'''<section class="slide portada" data-tipo="portada">
  <div class="t-g"></div><div class="t-v"></div>
  <div class="logo-main" role="img" aria-label="Universidad de la Costa"></div>
  <div class="p-kicker">{html.escape(etiqueta_sem)} · {html.escape(meta["unidad"])}</div>
  <h1>{html.escape(meta["titulo"])}</h1>
  <h3>{html.escape(meta.get("subtitulo", ""))}</h3>
  <div class="bar"></div>
  <div class="autor"><b>Ing. Rodolfo Cañas Cervantes</b><br>Universidad de la Costa (CUC) · Ingeniería de Sistemas<br>{CURSO} · Periodo 2026-2 · Barranquilla, Colombia</div>
  <div class="b-g"></div><div class="b-v"></div>
</section>'''
    diapos.append((portada, limpiar_narr(meta["narracion_portada"]), 1, "portada"))
    citas_usadas |= cites_en(meta["narracion_portada"])

    for k in range(1, 5):
        p = partes[k - 1]
        mapa = "".join(
            f'<div class="{"on" if j == k else ""}"><small>Parte {j}</small>{html.escape(partes[j-1]["titulo"])}</div>'
            for j in range(1, 5))
        div = f'''<section class="slide divisoria" data-tipo="divisoria" data-parte="{k}">
  <div class="d-num">Parte {k} de 4</div><div class="d-big">0{k}</div>
  <h2>{html.escape(p["titulo"])}</h2>
  <div class="d-res">{html.escape(p.get("resumen", ""))}</div>
  <div class="d-mapa">{mapa}</div>
  <div class="d-pie">{html.escape(etiqueta_sem)} · {html.escape(meta["titulo"])}</div>
  <div class="logo-div" role="img" aria-label="CUC"></div>
</section>'''
        diapos.append((div, limpiar_narr(p["narracion"]), k, "divisoria"))
        citas_usadas |= cites_en(p["narracion"])

        fuente = (d / f"parte{k}.html").read_text(encoding="utf-8")
        fuente = re.sub(r"<!--.*?-->", "", fuente, flags=re.S)
        secciones = SEC.findall(fuente)
        if not secciones:
            avisos.append(f"parte{k}.html no tiene <section>")
        for attrs, cuerpo in secciones:
            a = dict(ATTR.findall(attrs))
            mn = NARR.search(cuerpo)
            narr = mn.group(1) if mn else ""
            if not mn:
                avisos.append(f"parte{k}: diapositiva «{a.get('data-titulo','?')}» sin narración")
            cuerpo = NARR.sub("", cuerpo).strip()
            citas_usadas |= cites_en(narr) | cites_en(cuerpo) | cites_en(a.get("data-fuente", ""))
            cuerpo_html = CITE.sub(lambda m: f'<sup class="cite">[{m.group(1)}]</sup>', cuerpo)
            fuente_pie = CITE.sub(lambda m: f'[{m.group(1)}]', a.get("data-fuente", ""))
            sub = a.get("data-sub", "")
            sec = f'''<section class="slide" data-tipo="contenido" data-parte="{k}">
  <div class="s-head">
    <div class="kicker">{a.get("data-kicker", "")}</div>
    <h2>{a.get("data-titulo", "")}</h2>
    <div class="rule"></div>
    {f'<div class="sub">{sub}</div>' if sub else ''}
  </div>
  <div class="logo-corner" role="img" aria-label="CUC"></div>
  <div class="s-body">{cuerpo_html}</div>
  <div class="s-foot"><span class="curso">{CURSO} · {html.escape(etiqueta_sem)} · Parte {k} de 4</span><span class="src">{fuente_pie}</span><span class="pg">@@PG@@</span></div>
</section>'''
            diapos.append((sec, limpiar_narr(narr), k, "contenido"))

    # Fuentes citadas (al final de la Parte 4)
    lis = "".join(
        f'<li value="{f["n"]}">{html.escape(f["ref"])}'
        + (f' — <a href="{html.escape(f["url"])}">{html.escape(f["url"])}</a>' if f.get("url") else "")
        + "</li>" for f in meta["fuentes"])
    fsec = f'''<section class="slide" data-tipo="fuentes" data-parte="4">
  <div class="s-head"><div class="kicker">Referencias</div><h2>Fuentes citadas</h2><div class="rule"></div></div>
  <div class="logo-corner" role="img" aria-label="CUC"></div>
  <div class="s-body"><ol class="fuentes">{lis}</ol></div>
  <div class="s-foot"><span class="curso">{CURSO} · {html.escape(etiqueta_sem)}</span><span class="src">Diagramas: elaboración propia del curso salvo indicación</span><span class="pg">@@PG@@</span></div>
</section>'''
    diapos.append((fsec, limpiar_narr(meta.get("narracion_fuentes", "")), 4, "fuentes"))

    n = len(diapos)
    cuerpo = []
    narr_json = []
    for idx, (h, t, parte, tipo) in enumerate(diapos, 1):
        cuerpo.append(h.replace("@@PG@@", f"{idx} / {n}"))
        narr_json.append({"n": idx, "parte": parte, "tipo": tipo, "texto": t})

    # Validaciones
    nums = {f["n"] for f in meta["fuentes"]}
    faltan = sorted(citas_usadas - nums)
    sobran = sorted(nums - citas_usadas)
    if faltan:
        avisos.append(f"citas sin entrada en fuentes: {faltan}")
    if sobran:
        avisos.append(f"fuentes nunca citadas: {sobran}")

    narr_txt = json.dumps(narr_json, ensure_ascii=False).replace("</", "<\\/")
    slides_txt = "\n".join(cuerpo)
    titulo = f"{meta['titulo']} — {etiqueta_sem} · {CURSO}"
    salida = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(titulo)}</title>
<!-- Generado por herramientas/construir.py desde semanas/{clave}/ — no editar a mano. -->
<style>
{fuentes_css()}
{css}
div.logo-main,div.logo-corner,div.logo-div{{background:url({logo}) center/contain no-repeat;}}
sup.cite{{font-size:.62em;color:var(--dorado-osc);font-weight:700;margin-left:1px;}}
</style>
</head>
<body>
{iconos}
<div id="progreso"></div>
<div id="stage">
{slides_txt}
</div>
<div id="nav"><button id="b-ant" aria-label="Anterior">‹</button><span id="cont"></span><button id="b-sig" aria-label="Siguiente">›</button></div>
<div id="panel-narr"></div>
<script type="application/json" id="narracion">{narr_txt}</script>
<script>
{js}
</script>
</body>
</html>
'''
    out = RAIZ / f"{meta['archivo']}.html"
    out.write_text(salida, encoding="utf-8")

    # Resumen
    print(f"== {clave} → {out.name} ({len(salida)//1024} KB, {n} diapositivas)")
    for k in range(1, 5):
        items = [x for x in narr_json if x["parte"] == k]
        w = sum(palabras(x["texto"]) for x in items)
        seg = w / PPM * 60 + PAUSA * len(items)
        cont = sum(1 for x in items if x["tipo"] == "contenido")
        print(f"   Parte {k}: {cont} de contenido, {len(items)} en video, {w} palabras ≈ {seg/60:.1f} min")
    for a in avisos:
        print("   AVISO:", a)
    return not faltan


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    claves = sorted(p.name for p in (RAIZ / "semanas").glob("S*") if (p / "semana.json").exists()) \
        if sys.argv[1] == "todas" else sys.argv[1:]
    ok = all([construir(c) for c in claves])
    sys.exit(0 if ok else 2)
