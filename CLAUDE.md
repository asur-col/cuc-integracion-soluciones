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
5. **Referencias cruzadas existentes:** los laboratorios ya están publicados en `laboratorios/` (lab-01 sandbox de contenedores, lab-02 VPN site-to-site con OPNsense, lab-03 taller de 7 Rs). Los guiones ya referencian esos nombres exactos en sus puentes al laboratorio.
6. **Ritmo de exposición asumido:** 130–140 palabras por minuto en español. Si propones recortes, indica qué bloque se comprime y cuánto tiempo se ahorra (cada guion ya incluye instrucciones de recorte a 45–50 min).

## Pendiente conocido

Las presentaciones HTML de las semanas 1–3 aún no reflejan la densidad de los guiones (solo la semana 4 fue actualizada con íconos reales y video narrado). La tarea pendiente natural es expandir la narración de cada semana usando su guion como base.
