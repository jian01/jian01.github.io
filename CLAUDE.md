# CLAUDE.md — Instrucciones para Claude Code

Este archivo es leído automáticamente por Claude Code al inicio de cada sesión.

---

## Proyecto: resumen-papers

Jekyll 4.3 static site. Root: `/mnt/d/Escritorio/resumen papers/`

## Estructura de directorios

```
/mnt/d/Escritorio/resumen papers/
├── _config.yml              # kramdown GFM, math_engine: mathjax, theme: minima
├── _layouts/
│   ├── default.html         # carga MathJax 3 (inlineMath: $$ y \( \))
│   └── paper.html           # layout de cada paper (extiende default)
├── assets/css/style.scss
├── index.md                 # página raíz del sitio
└── llm_bias/
    ├── index.md             # índice de la literature review
    ├── topics/              # páginas de tópicos (tablas de papers)
    │   ├── unlearning.md
    │   ├── bias.md
    │   ├── alignment.md
    │   └── interpretability.md
    ├── papers/              # ~95 páginas de paper individuales (*.md)
    │   └── imgs/            # imágenes de papers (nombre: STEM.png)
    ├── pdfs/                # PDFs originales (nombre: STEM.pdf)
    ├── data/                # datos auxiliares (NO servidos por Jekyll)
    │   ├── papers.json      # lista de todos los papers con metadata
    │   ├── citations.json   # referencias de cada paper (Semantic Scholar)
    │   └── not_found.txt    # papers no encontrados en S2
    ├── fetch_citations.py   # script para poblar citations.json via S2 API
    └── *.py                 # scripts auxiliares de mantenimiento
```

## Convención de nombres de archivos

`YEAR_FIRSTAUTHOR_KEYWORD.md` — e.g. `2024_zhang_negative-preference-optimization.md`
Mismo stem para PDF (`pdfs/STEM.pdf`) e imagen (`papers/imgs/STEM.png`).

## Front matter de papers (papers/*.md)

```yaml
layout: paper
title: "..."
year: 2024
date_published: "YYYY-MM-DD"   # fecha arXiv v1
authors: "Apellido, Nombre, ..."
published: "Venue, Year"
tags:
  - "tag1"
method_type: "Tipo de método"
status:
  - "Leido"        # o Pendiente, Relevante, Irrelevante
pdf: "/llm_bias/pdfs/STEM.pdf"
image: "imgs/STEM.png"
image_caption: "..."
opinion: "Texto personal"
```

## Estructura del body de cada paper

```
## Qué hace
## Metodología
## Datasets utilizados
## Ejemplo ilustrativo   (opcional)
## Resultados principales
## Ventajas respecto a trabajos anteriores
## Trabajos previos relacionados
## Trabajos donde se usan   (solo para benchmarks/datasets)
## Tags
```

Todo en español.

## Archivos de tópico (topics/*.md)

Tabla con columnas: `Estado | Año | Título | Tipo de método | Resumen | Citas*`
- Estado: spans con clases `dot dot-relevante`, `dot-leido`, `dot-pendiente`, `dot-irrelevante`
- Link: `[Ver](../papers/STEM.html)`
- Al final: `## Estadísticas` con tabla de conteos por tipo de método y frecuencia de datasets
- Cuando se cambia el status de un paper hay que actualizarlo tanto en el .md del paper como en la fila de la tabla del tópico

## Convenciones de matemáticas

- Display math: `$$...$$` en línea propia → siempre funciona
- Inline math: `$$...$$` inline (NO `$...$`) → protegido por kramdown con `math_engine: mathjax`
- `_config.yml` tiene `math_engine: mathjax` → kramdown convierte `$$...$$` inline a `\(...\)`
- MathJax 3 en default.html con `inlineMath: [['$','$'], ['\\(','\\)']]`
- NUNCA usar `$...$` con subscripts en el body (kramdown los mangled); usar siempre `$$...$$`
- En front matter (opinion field), igual usar `$$\\delta_l$$` (el `\\` en YAML = `\` en el string)

## Tipos de método en bias.md (Métodos de Mitigación)

- `Alineamiento / RLHF` — métodos con reward model + PPO/RLHF (Bai, BeaverTails)
- `Fine-tuning` — fine-tuning estándar sobre datos debiaseados (FairFil, Gira)
- `Data augmentation` — generación/augmentación de datos de entrenamiento (MABEL, Thakur, Han)
- `Adapters / PEFT` — módulos adaptadores o PEFT (Lauscher, Xie, Zhao)
- `Edición de pesos / neuronas` — localización y edición de parámetros específicos (Yang, BiasEdit, KnowBias)
- `Tiempo de inferencia` — intervención en tiempo de inferencia sin modificar pesos (Gallegos, FairSteer, BiasFilter)
- `Evaluación / análisis` — papers de análisis puro sin método de mitigación activo
- `Otro` — métodos que no encajan en las categorías anteriores (D-CALM, Causal-Debias, Shrestha)

---

## Tarea: Agregar "## Trabajos previos relacionados"

1. Leer el PDF real (o HTML de ar5iv) del paper
2. Encontrar la sección "Related Work" (o referencias en la introducción si no hay sección dedicada)
3. Extraer los trabajos citados más importantes
4. Por cada uno, escribir un bullet: **Autor et al. (Año) — Título**: breve explicación de la relación
5. Si el paper organiza los trabajos en categorías, incluir un párrafo corto describiendo ese marco antes de los bullets
6. Si el paper citado está en el repo, agregar link relativo: `[Título](STEM.html)` (desde papers/) o `[Título](../papers/STEM.html)` (desde topics/)
7. Insertar la sección justo antes de `## Tags`

### Formato ejemplo

```markdown
## Trabajos previos relacionados

El paper organiza los trabajos previos en dos ejes: métodos de edición directa vs. externa.

- **[ROME — Meng et al. (2022)](2022_meng_rome.html)**: método de referencia de Locate-and-Edit que este trabajo extiende.
- **GPT-3 — Brown et al. (2020)**: modelo base sobre el que se evalúan los métodos.
```

- Bullets concisos (1-2 frases cada uno)
- Foco en los ~5-10 trabajos más importantes, no todas las citas
- Siempre leer el PDF real — no inventar trabajos relacionados

---

## Tarea: Agregar "## Trabajos donde se usan" (solo benchmarks/datasets)

Tabla con los papers del repo que usan ese dataset y cómo lo usan:

```markdown
## Trabajos donde se usan

| Paper | Cómo se usa |
|-------|-------------|
| [Título](STEM.html) | Breve descripción de cómo se usa el dataset |
```

---

## Datos auxiliares (llm_bias/data/)

### internal_citations.json ⚠️ REGENERAR CUANDO CAMBIE "Trabajos previos relacionados"

Mapa `paper_id → {title, cites, cited_by, cites_count, cited_by_count}`.
- `cites`: lista de ids de papers del repo que este paper cita en su sección de related work
- `cited_by`: lista de ids de papers del repo que citan a este paper
- **Regenerar siempre que se edite la sección "## Trabajos previos relacionados" de cualquier paper:**
  ```bash
  python3 llm_bias/build_internal_citations.py
  ```
  (desde la raíz del proyecto, tarda <1s)
