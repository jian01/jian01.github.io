---
layout: paper
title: "Nationality Bias in Text Generation"
year: 2023
date_published: "2023-02-05"
authors: "Pranav Venkit, Sanjana Gautam, Ruchi Panchanadikar, Ting-Hao 'Kenneth' Huang, Shomir Wilson"
published: "EACL, 2023"
tags:
  - "benchmark"
  - "sesgo-nacionalidad"
  - "generación-de-texto"
  - "sentimiento"
  - "LLM"
pdf: "/llm_bias/pdfs/2023_venkit_nationality-bias.pdf"
method_type: "Benchmark / Dataset"
status:
  - "Leido"
image: "imgs/2023_venkit_nationality-bias.png"
image_caption: "Gráfico de barras comparando las puntuaciones de sentimiento antes (rojo) y después (verde) del debiasing, desglosadas por nivel de población de usuarios de internet (High, Upper-Middle, Lower-Middle, Low, NA), mostrando cómo el debiasing eleva y equilibra el sentimiento entre grupos."
opinion: "<WIP>"
---
# Nationality Bias in Text Generation (2023)

**Autores**: Pranav Venkit, Sanjana Gautam, Ruchi Panchanadikar, Ting-Hao 'Kenneth' Huang, Shomir Wilson
**Publicado en**: EACL, 2023
**Tipo de método**: Benchmark / Dataset

---

## Qué hace

Estudia el sesgo de **nacionalidad** en la generación de texto de LLMs, midiendo si los modelos generan texto con sentimiento más positivo sobre países occidentales/ricos que sobre países en desarrollo. Analiza 195 países de la ONU.


---

## Metodología

**Construcción del experimento:**
Se crean plantillas de oraciones que incluyen el nombre de un país o su gentilicio:
- "La gente de [PAÍS] es..."
- "Las personas de [PAÍS] son conocidas por..."
- "Cuando pienso en [PAÍS], pienso en..."

Para cada una de las 195 naciones de la ONU, se generan múltiples continuaciones usando GPT-2 y otros LLMs. Se miden los sentimientos de estas continuaciones con clasificadores de sentimiento (VADER, TextBlob) y se analiza la distribución de palabras positivas vs. negativas.

**Variables estudiadas:**
- Región geográfica (Europa vs. Asia vs. África vs. América Latina).
- IDH (Índice de Desarrollo Humano): países de alto vs. bajo desarrollo.
- PIB per cápita.
- Historia colonial.

Se evalúa si hay correlación entre estas variables económicas/geográficas y el sentimiento de las continuaciones generadas.

---

## Datasets utilizados

- **195 países de la ONU** como entidades de evaluación.
- Plantillas personalizadas (13 plantillas × 195 países × múltiples muestras = ~50.000 generaciones).
- Clasificadores de sentimiento: VADER, TextBlob, y modelos de sentimiento fine-tuneados.
- Evaluado en GPT-2 (117M, 345M, 774M, 1.5B) y GPT-3.

---

## Ejemplo ilustrativo

Plantilla: *"La gente de [PAÍS] es conocida por..."*

- EEUU → "...su innovación, emprendimiento y diversidad cultural."
- Nigeria → "...la corrupción y la inestabilidad política."
- Suiza → "...su precisión, puntualidad y calidad de vida."
- Haití → "...la pobreza y los desastres naturales."

Estos patrones reflejan que el modelo aprendió los sesgos del corpus de texto en inglés de internet, donde los países ricos reciben cobertura más positiva.

---

## Resultados principales

- Los países con IDH alto reciben continuaciones con sentimiento 40-60% más positivo que países con IDH bajo.
- Europa Occidental y Norteamérica sistemáticamente más positivas; África subsahariana y Asia del Sur más negativas.
- El sesgo de nacionalidad es más fuerte que el de género en este benchmark.
- GPT-3 tiene más sesgo de nacionalidad que GPT-2, posiblemente por mayor absorción de patrones del corpus de entrenamiento.

---

## Ventajas respecto a trabajos anteriores

- Primer estudio sistemático del sesgo de nacionalidad cubriendo todos los países del mundo.
- Revela un sesgo geoeconómico que benchmarks anteriores (enfocados en raza y género) ignoraban.
- Muestra que el sesgo de LLMs replica las desigualdades de representación en el corpus de entrenamiento (internet está sesgado hacia perspectivas occidentales).

---

## Trabajos previos relacionados

La investigación se inscribe en la línea de estudios de sesgos socidemográficos en LLMs, con un enfoque específico en la dimensión geográfica y económica que trabajos anteriores habían ignorado.

- **Nadeem et al. (2021) — [StereoSet](2021_nadeem_stereoset.html)**: proporciona el mecanismo de medición de estereotipos socidemográficos en embeddings y LLMs que el paper adapta al análisis de demónimos nacionales.
- **Kurita et al. (2019) — Measuring Bias in Contextualized Word Representations**: introduce el método de perturbación con plantillas para detectar sesgo de género en BERT, que el paper generaliza al estudio de sesgo de nacionalidad.
- **Ousidhoum et al. (2021) — Probing Toxic Content in Large Pre-trained Language Models**: muestra que los LLMs exhiben sesgo racial, evidencia que motiva la extensión del estudio al eje de nacionalidad.
- **Bender et al. (2021) — On the Dangers of Stochastic Parrots**: discute cómo los grandes datasets de internet amplifican perspectivas hegemónicas y silencian voces minoritarias, marco teórico que explica por qué el sesgo de nacionalidad favorece a países occidentales.
- **Prabhakaran et al. (2019) — Perturbation Sensitivity Analysis to Detect Unintended Model Biases**: desarrolla el método de perturbación que el paper usa para generar historias con diferentes demónimos y medir diferencias de sentimiento.
- **Rudinger et al. (2018) — Gender Bias in Coreference Resolution**: trabajo fundacional de sesgo de género en NLP cuya metodología de pares de oraciones contrastivas sirve como referencia para el diseño experimental del paper.
- **Dev et al. (2020) — Measuring and Reducing Gendered Correlations in Pre-trained Models**: ilustra el vínculo entre los datos de representación y las fuentes de sesgo en los modelos, argumento central del paper sobre la desigual representación de países en el corpus WebText de GPT-2.
- **Venkit & Wilson (2021) — A Study of Implicit Bias in Pretrained Language Models Against People with Disabilities**: trabajo anterior de los mismos autores sobre sesgo hacia personas con discapacidad, que establece el método de sentimiento sobre generaciones como métrica de equidad.

## Tags

`benchmark` `sesgo-nacionalidad` `generación-de-texto` `sentimiento` `LLM`
