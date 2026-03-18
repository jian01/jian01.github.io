---
layout: paper
title: "Aligned but Stereotypical? The Hidden Influence of System Prompts on Social Bias in LVLM-Based Text-to-Image Models"
year: 2025
date_published: "2024-12-04"
authors: "NaHyeon Park, Namin An, Kunhee Kim, Soyeon Yoon, Jiahao Huo, Hyunjung Shim"
published: "arXiv, 2025"
tags:
  - "sesgo-social"
  - "text-to-image"
  - "system-prompts"
  - "modelos-multimodales"
  - "evaluación"
pdf: "/llm_bias/pdfs/2025_park_aligned-stereotypical.pdf"
method_type: "Evaluación / análisis"
datasets:
  - "FairFace"
status:
  - "Irrelevante"
  - "Leido"
image: "imgs/2025_park_aligned-stereotypical.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---

## Qué hace

Estudia cómo los **system prompts** (instrucciones base del sistema) de modelos de visión-lenguaje grandes (LVLMs) usados para generación de imágenes influyen en los sesgos sociales de género y raza en las imágenes generadas, incluso cuando el modelo parece "alineado" con principios de equidad.


---

## Metodología

Los modelos de text-to-image modernos (como DALL-E 3) usan LVLMs como intermediario: el LVLM reformula el prompt del usuario antes de pasarlo al generador de imágenes. Los system prompts del LVLM pueden modificar cómo se interpretan los prompts de usuario.

**El experimento:**
1. Se prueban prompts de usuario que podrían generar imágenes sesgadas (ej. "un médico", "un enfermero", "un CEO", "un asistente de limpieza").
2. Se evalúan estos prompts con diferentes system prompts: el default, system prompts "alineados" (que instruyen al modelo a ser equitativo), y system prompts "neutrales".
3. Se generan imágenes y se mide el sesgo en las imágenes resultantes usando clasificadores de género y etnia sobre los personajes generados.

**Análisis de representaciones internas:**
Se estudian los embeddings del LVLM para ver si los system prompts de alineamiento cambian cómo el modelo representa conceptos con carga de género/raza. Se analiza la similitud coseno entre embeddings de profesiones y atributos demográficos.

Las partes del modelo estudiadas son las representaciones en las capas de atención cruzada (cross-attention) entre texto e imagen.

---

## Datasets utilizados

- **FairFace**: dataset de imágenes con etiquetas de género, etnia y edad para evaluar distribución.
- **Custom profession prompts**: 30 profesiones con distintos estereotipos de género y raza.
- Evaluado con DALL-E 3 (usa GPT-4V como LVLM) y otros modelos text-to-image.

---

## Ejemplo ilustrativo

Prompt del usuario: "Genera la imagen de un cirujano."

Con system prompt default de DALL-E 3: genera un hombre blanco de mediana edad en el 80% de los casos.

Con system prompt "equitativo" que dice "Asegúrate de representar diversidad en género y etnia": genera imágenes más diversas... pero sigue mostrando sesgos sutiles: las mujeres cirujanas generadas son más jóvenes, con menor autoridad visual (sin bisturí, sin bata de cirujano).

Conclusión: el sistema parece equitativo en distribución de género pero mantiene sesgos en el tipo de representación.

---

## Resultados principales

- Los system prompts de "alineamiento" reducen el sesgo demográfico obvio (~30% mejora en distribución de género) pero no eliminan los sesgos cualitativos (cómo se representa visualmente cada grupo).
- Los embeddings del LVLM con system prompts equitativos siguen mostrando alta correlación entre profesiones de alto estatus y marcadores masculinos.
- Los system prompts influyen principalmente en la distribución superficial de géneros/razas pero no en los atributos asociados.

---

## Ventajas respecto a trabajos anteriores

- Primer estudio que analiza el rol de los system prompts en el sesgo de modelos text-to-image.
- Distingue entre sesgos demográficos obvios y sesgos cualitativos sutiles.
- Relevante para el diseño de system prompts en sistemas de IA generativa comercial.

---

## Trabajos previos relacionados

El artículo organiza los trabajos previos en dos ejes: avances en la generación texto-a-imagen (T2I) con énfasis en codificadores de texto, y medición y mitigación del sesgo social en modelos T2I.

- **Nadeem et al. (2021) — StereoSet: Measuring stereotypical bias in pretrained language models**: benchmark de referencia para estereotipos en LLMs cuya lógica de evaluación se extiende al dominio visual en este trabajo; ver [2021_nadeem_stereoset.md](2021_nadeem_stereoset.html).
- **Parrish et al. (2021) — BBQ: A hand-built bias benchmark for question answering**: referente en benchmarks de sesgo en QA, cuya estructura de niveles de complejidad lingüística inspira el diseño jerárquico del benchmark T2I propuesto; ver [2021_parrish_bbq.md](2021_parrish_bbq.html).
- **Gallegos et al. (2024) — Self-debiasing large language models**: método de debiasing mediante prompts de sistema, concepto central en la estrategia de mitigación basada en prompting automático del presente artículo; ver [2024_gallegos_self-debiasing.md](2024_gallegos_self-debiasing.html).
- **Smith et al. (2022) — HolisticBias: A dataset for bias in NLP**: fuente de términos descriptores demográficos con cobertura amplia que inspira la selección de atributos en el benchmark multilingüe propuesto; ver [2022_smith_holistic-descriptor.md](2022_smith_holistic-descriptor.html).
- **Acerbi et al. (2023) — Large language models show human-like content biases in transmission chain experiments**: evidencia de que los LLMs amplifican sesgos culturales, relevante para entender por qué los nuevos LVLM-encoders heredan sesgos del preentrenamiento; ver [2023_acerbi_human-like-biases.md](2023_acerbi_human-like-biases.html).
- **Vig et al. (2020) — Investigating gender bias in language models using causal mediation analysis**: análisis causal del sesgo de género en LLMs, metodología referenciada para fundamentar el estudio de sesgo en los encoders de texto de los modelos T2I; ver [2020_vig_gender-bias-causal.md](2020_vig_gender-bias-causal.html).
- **Venkit et al. (2023) — Nationality bias in text generation**: estudio de sesgo de nacionalidad en generación de texto, motivando la inclusión de atributos de etnia y nacionalidad en el benchmark multilingüe de este trabajo; ver [2023_venkit_nationality-bias.md](2023_venkit_nationality-bias.html).

## Tags

`sesgo-social` `text-to-image` `system-prompts` `modelos-multimodales` `evaluación`
