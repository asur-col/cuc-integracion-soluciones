# Metadatos y fuentes verificadas (HTTP 200) para Semana 14

SEMANA_META = {
  "semana": 14,
  "etiqueta_semana": "Semana 14",
  "archivo": "2026-2-S14-integracion-soluciones-capacidades-contexto-rag",
  "titulo": "Capacidades de los modelos: razonamiento, programación asistida, contexto y memoria (AGENTS.md); RAG simple",
  "unidad": "Unidad 3",
  "subtitulo": "Cómo razonan los modelos, cómo dar contexto con AGENTS.md y cómo recuperar conocimiento de CaribeMart con RAG simple",
  "narracion_portada": (
    "Bienvenidos a la semana catorce de Integración de Soluciones para Plataformas Cloud. "
    "En la semana trece conectamos modelos con herramientas reales mediante el protocolo MCP. "
    "Hoy respondemos qué pasa dentro del modelo y cómo darle memoria útil del negocio. "
    "Exploraremos el razonamiento paso a paso, la programación asistida con revisión de cambios, "
    "el archivo AGENTS.md en opencode y la recuperación aumentada de generación simple para CaribeMart."
  ),
  "partes": [
    {
      "titulo": "Razonamiento y programación asistida",
      "resumen": "Cómputo en tiempo de prueba, tokens de pensamiento, inspección de cambios y límites reales en código.",
      "narracion": (
        "Parte uno. Razonamiento y programación asistida. "
        "No todos los problemas se resuelven en un solo golpe de texto. "
        "Veremos cómo los modelos razonadores invierten cómputo extra al inferir mediante tokens de pensamiento, "
        "cuándo conviene pagar esa latencia frente a un modelo estándar y cómo trabaja un asistente de código "
        "sobre repositorios reales inspeccionando parches y resultados en SWE-bench Verified."
      )
    },
    {
      "titulo": "Contexto y memoria con AGENTS.md",
      "resumen": "Ventana de contexto, degradación por ruido y memoria estable del proyecto CaribeMart en opencode.",
      "narracion": (
        "Parte dos. Contexto y memoria del proyecto con AGENTS.md. "
        "Cuando cierran una sesión, el modelo olvida todo lo conversado. "
        "Además, si llenan la ventana de contexto con ruido, el rendimiento cae en el centro. "
        "Aprenderemos a escribir un archivo AGENTS.md conciso para CaribeMart en opencode, "
        "separando reglas de negocio de los datos de clientes antes de resolver el primer mini reto."
      )
    },
    {
      "titulo": "RAG simple: recuperar conocimiento",
      "resumen": "Fragmentación de documentos, índice léxico o vectorial y respuestas fundamentadas sin inventar.",
      "narracion": (
        "Parte tres. Generación aumentada por recuperación simple. "
        "Un archivo AGENTS.md funciona muy bien para reglas breves, pero no soporta cientos de páginas de manuales. "
        "Aquí entra la recuperación aumentada de generación. "
        "Recorreremos las fases de fragmentación, indexación léxica o vectorial y consulta en vivo, "
        "y compararemos con honestidad cuándo usar AGENTS.md, cuándo RAG y cuándo herramientas MCP."
      )
    },
    {
      "titulo": "CaribeMart integrado, marco y práctica",
      "resumen": "Arquitectura completa con opencode y permission ask, caso real Nequi en Colombia, marco legal y práctica del proyecto.",
      "narracion": (
        "Parte cuatro. Arquitectura integrada en CaribeMart, marco colombiano y práctica. "
        "Unimos las piezas en opencode con servidor MCP caribemart, permiso ask para cancelar pedidos, "
        "contexto AGENTS.md y recuperación documental. "
        "Analizaremos el caso colombiano real de Nequi en Amazon Bedrock, la normativa de datos de la SIC, "
        "el segundo mini reto, la pregunta abierta y la vista conceptual del laboratorio B."
      )
    }
  ],
  "narracion_fuentes": (
    "En esta última diapositiva quedan todas las fuentes verificadas que respaldan las cifras, "
    "estándares y casos reales trabajados durante la semana catorce."
  ),
  "fuentes": [
    {
      "n": 1,
      "ref": "OpenAI, «Learning to reason with LLMs» (presentación de OpenAI o1, septiembre de 2024)",
      "url": "https://openai.com/index/learning-to-reason-with-llms/",
      "corta": "OpenAI, «Learning to reason with LLMs» (modelo o1, 2024)"
    },
    {
      "n": 2,
      "ref": "DeepSeek-AI, «DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning» (arXiv:2501.12948)",
      "url": "https://arxiv.org/abs/2501.12948",
      "corta": "DeepSeek-AI, «DeepSeek-R1» (RL), arXiv:2501.12948"
    },
    {
      "n": 3,
      "ref": "OpenAI, «Introducing SWE-bench Verified» (500 tareas validadas por humanos, agosto 2024 / febrero 2025)",
      "url": "https://openai.com/index/introducing-swe-bench-verified/",
      "corta": "OpenAI, «Introducing SWE-bench Verified» (500 tareas)"
    },
    {
      "n": 4,
      "ref": "Anthropic, «Introducing computer use, a new Claude 3.5 Sonnet, and Claude 3.5 Haiku» (octubre de 2024)",
      "url": "https://www.anthropic.com/news/3-5-models-and-computer-use",
      "corta": "Anthropic, «Claude 3.5 Sonnet y SWE-bench Verified»"
    },
    {
      "n": 5,
      "ref": "Princeton NLP, «SWE-bench Leaderboards» (Jimenez et al., 2.294 y 500 instancias, swebench.com)",
      "url": "https://www.swebench.com/",
      "corta": "Princeton NLP, «SWE-bench Leaderboards», swebench.com"
    },
    {
      "n": 6,
      "ref": "Liu et al., «Lost in the Middle: How Language Models Use Long Contexts» (TACL, arXiv:2307.03172)",
      "url": "https://arxiv.org/abs/2307.03172",
      "corta": "Liu et al., «Lost in the Middle», arXiv:2307.03172"
    },
    {
      "n": 7,
      "ref": "Anthropic, «Effective context engineering for AI agents» (engineering / research, 2025)",
      "url": "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents",
      "corta": "Anthropic, «Effective context engineering for AI agents»"
    },
    {
      "n": 8,
      "ref": "AGENTS.md, «A simple, open format for guiding coding agents» (usado en >60 mil proyectos, agents.md)",
      "url": "https://agents.md/",
      "corta": "AGENTS.md, formato abierto (>60 mil repos), agents.md"
    },
    {
      "n": 9,
      "ref": "OpenCode (opencode), «Rules: AGENTS.md e instrucciones en opencode.json» (opencode.ai/v1/docs/rules/)",
      "url": "https://opencode.ai/v1/docs/rules/",
      "corta": "OpenCode, «Rules» (AGENTS.md), opencode.ai/v1/docs/rules"
    },
    {
      "n": 10,
      "ref": "Lewis et al., «Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks» (NeurIPS 2020, arXiv:2005.11401)",
      "url": "https://arxiv.org/abs/2005.11401",
      "corta": "Lewis et al., «Retrieval-Augmented Generation», arXiv:2005.11401"
    },
    {
      "n": 11,
      "ref": "Anthropic, «Contextual Retrieval» (RAG con BM25, embeddings y reranking, septiembre de 2024)",
      "url": "https://www.anthropic.com/engineering/contextual-retrieval",
      "corta": "Anthropic, «Contextual Retrieval» (BM25 y embeddings)"
    },
    {
      "n": 12,
      "ref": "OpenCode (opencode v1), «Permissions: allow, ask y deny por herramienta» (opencode.ai/v1/docs/permissions/)",
      "url": "https://opencode.ai/v1/docs/permissions/",
      "corta": "OpenCode v1, «Permissions» (allow, ask, deny), opencode.ai/v1"
    },
    {
      "n": 13,
      "ref": "AWS Customer Stories, «Approving 70% more loans for underserved customers using AWS with Nequi» (Bedrock, RAG y MCP)",
      "url": "https://aws.amazon.com/solutions/case-studies/nequi-bedrock/",
      "corta": "AWS Case Study, «Nequi» (Bedrock, RAG y MCP), aws.amazon.com"
    },
    {
      "n": 14,
      "ref": "Congreso de la República de Colombia, «Ley Estatutaria 1581 de 2012: Protección de Datos Personales»",
      "url": "https://www.alcaldiabogota.gov.co/sisjur/normas/Norma1.jsp?i=49981",
      "corta": "Congreso de Colombia, Ley Estatutaria 1581 de 2012"
    },
    {
      "n": 15,
      "ref": "Superintendencia de Industria y Comercio (SIC), «Circular Externa 002 del 21 de agosto de 2024: IA y datos personales»",
      "url": "https://sedeelectronica.sic.gov.co/transparencia/normativa/circular-externa-2-de-2024-de-la-superintendencia-de-industria-y-comercio-lineamientos-sobre-el-tratamiento-de-datos",
      "corta": "SIC, Circular Externa 002 de 2024 (IA y datos personales)"
    },
    {
      "n": 16,
      "ref": "OWASP Foundation, «OWASP Top 10 for Large Language Model Applications 2026» (Prompt Injection)",
      "url": "https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/",
      "corta": "OWASP, «Top 10 for LLM Applications 2026», genai.owasp.org"
    }
  ]
}
