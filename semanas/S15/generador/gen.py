#!/usr/bin/env python3
# Generador de semanas/S15/parte1..4.html y semanas/S15/semana.json
import html
import json
import os
import re
import sys

REPO = '/opt/asur/projects/academy/learning/cuc/2026-2/integracion-soluciones/repositorio/cuc-integracion-soluciones'
S13_GEN = os.path.join(REPO, 'semanas', 'S13', 'generador')
GEN_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, S13_GEN)
from lib import *  # noqa: E402,F403

sys.path.insert(0, GEN_DIR)
from reg import SL  # noqa: E402

GLOS_S15 = [
    ('MCP', 'Model Context Protocol'),
    ('LLM', 'modelo de lenguaje grande'),
    ('OWASP', 'Open Worldwide Application Security Project'),
    ('MITRE ATLAS', 'Adversarial Threat Landscape for Artificial-Intelligence Systems'),
    ('AI RMF', 'AI Risk Management Framework'),
    ('NIST', 'National Institute of Standards and Technology'),
    ('HITL', 'human-in-the-loop (verificación humana)'),
    ('JSON RPC', 'JSON Remote Procedure Call'),
    ('JSON', 'JavaScript Object Notation'),
    ('API', 'interfaz de programación de aplicaciones'),
    ('SDK', 'kit de desarrollo de software'),
    ('SIC', 'Superintendencia de Industria y Comercio'),
    ('RAG', 'generación aumentada por recuperación'),
    ('IA', 'inteligencia artificial'),
    ('npm', 'gestor de paquetes de Node'),
    ('stdio', 'entrada y salida estándar'),
    ('ESM', 'módulos ECMAScript'),
    ('HTML', 'Lenguaje de Marcado de Hipertexto'),
]


def siglas_s15(textos):
    t = ' '.join(textos)
    out = []
    seen = set()
    for k, v in GLOS_S15:
        if re.search(r'(?<![\w])%s(?![\w])' % re.escape(k), t):
            out.append('%s = %s' % (k, v))
            seen.add(k)
    if 'JSON RPC' in seen and 'JSON' in seen:
        out = [o for o in out if not o.startswith('JSON = ')]
    return ' · '.join(out)


def texto_visible(svg):
    return re.findall(r'<text[^>]*>(.*?)</text>', svg, re.S)


def limpiar_narr(t):
    t = re.sub(r'\[cite:\d+(?:\s*,\s*\d+)*\]', '', t)
    return re.sub(r'\s+', ' ', t).strip()


def construir_meta():
    return {
        'semana': 15,
        'etiqueta_semana': 'Semana 15',
        'archivo': '2026-2-S15-integracion-soluciones-agentes-delegacion-prompt-injection',
        'titulo': 'Agentes, delegación con verificación humana y prompt injection',
        'unidad': 'Unidad 3',
        'subtitulo': 'Encadenar herramientas con control humano (permission ask), resistir prompt injection y preparar el proyecto Corte 3 de CaribeMart',
        'narracion_portada': (
            'Bienvenidos a la semana quince de Integración de Soluciones para Plataformas Cloud. '
            'En las semanas anteriores conectamos modelos con herramientas mediante MCP y les dimos '
            'contexto de negocio con AGENTS punto md. Hoy integramos agentes autónomos con control '
            'humano mediante permission ask, analizamos el riesgo de prompt injection y preparamos '
            'paso a paso el proyecto de aula del tercer corte para CaribeMart.'
        ),
        'partes': [
            {
                'titulo': 'De llamadas sueltas a agentes autónomos',
                'resumen': 'Bucle observar-razonar-actuar, encadenamiento de herramientas en CaribeMart y el riesgo OWASP LLM06 de Agencia Excesiva.',
                'narracion': (
                    'Parte uno. De llamadas sueltas a agentes autónomos. Hasta aquí nuestros modelos '
                    'respondían una sola consulta por turno. Hoy damos el salto a tareas encadenadas '
                    'donde el agente observa, razona y actúa en varios pasos. Veremos cómo funciona ese '
                    'bucle en CaribeMart desde pedidos atrasados hasta proponer cancelaciones y por qué '
                    'OWASP advierte sobre la agencia excesiva cuando faltan límites.'
                ),
            },
            {
                'titulo': 'Delegación con verificación humana',
                'resumen': 'Principio human-in-the-loop, marco 4D de fluidez con IA y configuración de permission ask en opencode.json con bitácora.',
                'narracion': (
                    'Parte dos. Delegación con verificación humana. Un agente útil analiza rápido, '
                    'pero las decisiones sensibles sobre pedidos deben pasar por manos humanas. '
                    'Aplicaremos el principio human-in-the-loop junto al marco cuatro D, configuraremos '
                    'permission ask para cancelar pedido en opencode punto json, practicaremos cómo '
                    'aprobar o rechazar con bitácora y resolveremos el primer mini reto.'
                ),
            },
            {
                'titulo': 'Prompt injection directo e indirecto',
                'resumen': 'OWASP LLM01, técnicas MITRE ATLAS y anatomía del ataque oculto en el campo nota de pedidos.json en CaribeMart.',
                'narracion': (
                    'Parte tres. Prompt injection directo e indirecto. Cuando un modelo mezcla reglas '
                    'del sistema con datos externos en la misma ventana de contexto, un texto malicioso '
                    'puede hacerse pasar por orden legítima. Revisaremos OWASP LLM cero uno, MITRE ATLAS '
                    'y seguiremos la trazabilidad exacta del ataque escondido en el campo nota de '
                    'pedidos punto json dentro de CaribeMart.'
                ),
            },
            {
                'titulo': 'Defensa en profundidad, marco colombiano y Proyecto Corte 3',
                'resumen': 'Las dos defensas en AGENTS.md y server.js con zod, casos reales de la SIC, marco legal y rúbrica del Proyecto Corte 3.',
                'narracion': (
                    'Parte cuatro. Defensa en profundidad, marco colombiano y Proyecto Corte tres. '
                    'Implementaremos las dos defensas obligatorias en AGENTS punto md y en server punto js '
                    'con zod, comprobaremos la prueba antes y después del ataque, analizaremos sanciones '
                    'reales de la SIC en Colombia bajo la Ley mil quinientos ochenta y uno y cerraremos '
                    'repasando fechas y criterios del proyecto.'
                ),
            },
        ],
        'narracion_fuentes': (
            'En esta diapositiva final quedan todas las fuentes oficiales y casos reales consultados '
            'para esta semana. Abran los enlaces verificados si desean profundizar en cada estándar o norma.'
        ),
        'fuentes': [
            {
                'n': 1,
                'ref': 'OWASP GenAI Security Project, «LLM06:2025 Excessive Agency», genai.owasp.org (consultado 13 de noviembre de 2026)',
                'url': 'https://genai.owasp.org/llmrisk/llm062025-excessive-agency/',
                'corta': 'OWASP GenAI, «LLM06:2025 Excessive Agency», genai.owasp.org',
            },
            {
                'n': 2,
                'ref': 'OWASP GenAI Security Project, «LLM01:2025 Prompt Injection», genai.owasp.org (consultado 13 de noviembre de 2026)',
                'url': 'https://genai.owasp.org/llmrisk/llm01-prompt-injection/',
                'corta': 'OWASP GenAI, «LLM01:2025 Prompt Injection», genai.owasp.org',
            },
            {
                'n': 3,
                'ref': 'OWASP Foundation, «OWASP GenAI LLM Top 10 2026» (agosto de 2026)',
                'url': 'https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/',
                'corta': 'OWASP, «GenAI LLM Top 10 2026» (agosto de 2026)',
            },
            {
                'n': 4,
                'ref': 'MITRE ATLAS, «Adversarial Threat Landscape for Artificial-Intelligence Systems» (técnica AML.T0051 LLM Prompt Injection)',
                'url': 'https://atlas.mitre.org/',
                'corta': 'MITRE ATLAS, «AML.T0051 LLM Prompt Injection», atlas.mitre.org',
            },
            {
                'n': 5,
                'ref': 'OpenCode, «Permissions: allow, ask, deny en opencode.json», opencode.ai/docs (consultado 13 de noviembre de 2026)',
                'url': 'https://opencode.ai/docs/permissions/',
                'corta': 'OpenCode, «Permissions», opencode.ai/docs',
            },
            {
                'n': 6,
                'ref': 'OpenCode, «MCP servers: configuración local y remota en opencode.json», opencode.ai/docs (consultado 13 de noviembre de 2026)',
                'url': 'https://opencode.ai/docs/mcp-servers/',
                'corta': 'OpenCode, «MCP servers», opencode.ai/docs',
            },
            {
                'n': 7,
                'ref': 'Model Context Protocol (MCP), «Security Best Practices», modelcontextprotocol.io (consultado 13 de noviembre de 2026)',
                'url': 'https://modelcontextprotocol.io/docs/2025-11-25/tutorials/security/security_best_practices',
                'corta': 'MCP, «Security Best Practices», modelcontextprotocol.io',
            },
            {
                'n': 8,
                'ref': 'Anthropic Academy, «AI Fluency: Framework & Foundations (4D: Delegation, Description, Discernment, Diligence)»',
                'url': 'https://anthropic.skilljar.com/ai-fluency-framework-foundations',
                'corta': 'Anthropic, «AI Fluency: Framework & Foundations (4D)»',
            },
            {
                'n': 9,
                'ref': 'Zod, «TypeScript-first schema validation with static type inference», zod.dev (consultado 13 de noviembre de 2026)',
                'url': 'https://zod.dev/',
                'corta': 'Zod, «Schema validation», zod.dev',
            },
            {
                'n': 10,
                'ref': 'NIST, «AI Risk Management Framework (AI RMF)», nist.gov (consultado 13 de noviembre de 2026)',
                'url': 'https://www.nist.gov/itl/ai-risk-management-framework',
                'corta': 'NIST, «AI Risk Management Framework (AI RMF)», nist.gov',
            },
            {
                'n': 11,
                'ref': 'Congreso de la República de Colombia, «Ley Estatutaria 1581 de 2012: Régimen General de Protección de Datos Personales» (Diario Oficial 48587)',
                'url': 'https://www.alcaldiabogota.gov.co/sisjur/normas/Norma1.jsp?i=49981',
                'corta': 'Congreso de Colombia, Ley Estatutaria 1581 de 2012 (Habeas Data)',
            },
            {
                'n': 12,
                'ref': 'Superintendencia de Industria y Comercio (SIC), «Circular Externa 002 del 21 de agosto de 2024: Lineamientos sobre el Tratamiento de Datos Personales en Sistemas de Inteligencia Artificial»',
                'url': 'https://sedeelectronica.sic.gov.co/transparencia/normativa/circular-externa-2-de-2024-de-la-superintendencia-de-industria-y-comercio-lineamientos-sobre-el-tratamiento-de-datos',
                'corta': 'SIC, Circular Externa 002 del 21 de agosto de 2024 (IA y datos)',
            },
            {
                'n': 13,
                'ref': 'Superintendencia de Industria y Comercio (SIC), «214 millones de multa a Mercado Libre por exigir a sus usuarios reconocimiento facial para acceder a sus cuentas», sedeelectronica.sic.gov.co',
                'url': 'https://sedeelectronica.sic.gov.co/noticias/214-millones-de-multa-mercado-libre-por-exigir-sus-usuarios-reconocimiento-facial-para-acceder-sus-cuentas',
                'corta': 'SIC, «214 millones de multa a Mercado Libre por biometría», sic.gov.co',
            },
            {
                'n': 14,
                'ref': 'Superintendencia de Industria y Comercio (SIC), «Resolución 45710 del 18 de junio de 2026: cierre definitivo a World Foundation y Tools for Humanity», sedeelectronica.sic.gov.co',
                'url': 'https://sedeelectronica.sic.gov.co/comunicado/la-sic-confirma-la-sancion-de-cierre-inmediato-y-definitivo-de-la-operacion-de-tratamiento-de-datos-sensibles-adelantada-por-world',
                'corta': 'SIC, «Resolución 45710 de 2026: cierre a World Foundation», sic.gov.co',
            },
        ],
    }


def render():
    import slides1, slides2, slides3, slides4  # noqa: F401
    for n in range(1, 57):
        assert n in SL, f'Falta diapositiva {n}'

    s15_dir = os.path.join(REPO, 'semanas', 'S15')
    os.makedirs(s15_dir, exist_ok=True)

    meta = construir_meta()
    for f in meta['fuentes']:
        assert len(f['corta']) <= 82, f"Fuente {f['n']} corta > 82: {len(f['corta'])}"

    bad_chars = re.compile(r'[→±~*#/&]|https?://')
    bad_words = re.compile(r'sumativa|killercoda|play with docker', re.I)

    out_of_range = []
    min_fs = 999
    cites_seen = set()

    for k in range(1, 5):
        start = (k - 1) * 14 + 1
        end = k * 14
        sections = []
        parte_words = 0
        for n in range(start, end + 1):
            s = SL[n]
            fu = s['fuente']
            for f in s['fotos']:
                if 'Foto:' not in fu:
                    fu += ' · ' + credito(f)
            tv = [html.unescape(re.sub('<[^>]+>', '', x)) for x in texto_visible(s['body'])]
            sg = siglas_s15([s['titulo'], s['sub']] + tv + s['sig'])

            # Check font sizes inside SVG
            for m_fs in re.finditer(r'font-size="([0-9.]+)"', s['body']):
                fs = float(m_fs.group(1))
                min_fs = min(min_fs, fs)
                if fs < 16:
                    print(f'WARN SVG font-size {fs} < 16 en diapo {n}')

            # Check narration
            narr_clean = limpiar_narr(s['narr'])
            wc = len(narr_clean.split())
            parte_words += wc
            if wc < 135 or wc > 145:
                out_of_range.append((n, wc))
            if bad_chars.search(narr_clean):
                print(f'WARN simbolo raro en narr diapo {n}: {bad_chars.findall(narr_clean)}')
            if bad_words.search(narr_clean) or bad_words.search(s['body']):
                print(f'WARN palabra prohibida en diapo {n}')

            for m_c in re.finditer(r'\[cite:([^\]]+)\]', s['narr'] + ' ' + fu + ' ' + s['body']):
                cites_seen.update(int(x.strip()) for x in m_c.group(1).split(','))

            sec = (
                f'<section data-kicker="{html.escape(s["kicker"])}" '
                f'data-titulo="{html.escape(s["titulo"])}" '
                f'data-sub="{html.escape(s["sub"])}" '
                f'data-fuente="{html.escape(fu)}" '
                f'data-siglas="{html.escape(sg)}">\n'
                f'{s["body"]}\n'
                f'<aside class="narracion">{s["narr"]}</aside>\n'
                f'</section>'
            )
            sections.append(sec)

        with open(os.path.join(s15_dir, f'parte{k}.html'), 'w', encoding='utf-8') as fp:
            fp.write('\n'.join(sections) + '\n')

        extra = len(limpiar_narr(meta['partes'][k - 1]['narracion']).split())
        items = 15
        if k == 1:
            extra += len(limpiar_narr(meta['narracion_portada']).split())
            items += 1
        if k == 4:
            extra += len(limpiar_narr(meta['narracion_fuentes']).split())
            items += 1
        tot_w = parte_words + extra
        mins = (tot_w / 135.0 * 60 + items * 0.8) / 60.0
        print(f'Parte {k}: contenido={parte_words} palabras, total={tot_w} palabras ({mins:.2f} min)')

    with open(os.path.join(s15_dir, 'semana.json'), 'w', encoding='utf-8') as fp:
        json.dump(meta, fp, ensure_ascii=False, indent=2)

    print(f'Min font-size SVG: {min_fs}')
    print(f'Citas usadas: {sorted(cites_seen)}')
    faltan = sorted(set(range(1, 15)) - cites_seen)
    if faltan:
        print(f'WARN fuentes sin citar: {faltan}')
    if out_of_range:
        print(f'Fuera de 135-145 palabras ({len(out_of_range)}): {out_of_range}')
    else:
        print('OK todas las 56 diapositivas entre 135 y 145 palabras')


if __name__ == '__main__':
    render()
