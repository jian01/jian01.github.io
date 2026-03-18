---
layout: paper
title: "\"I'm sorry to hear that\": Finding New Biases in Language Models with a Holistic Descriptor Dataset"
year: 2022
date_published: "2022-05-18"
authors: "Eric Michael Smith, Melissa Hall, Melanie Kambadur, Eleonora Presani, Adina Williams"
published: "EMNLP, 2022"
tags:
  - "benchmark"
  - "sesgo-social"
  - "generación-de-texto"
  - "sentimiento"
  - "dataset-holístico"
pdf: "/llm_bias/pdfs/2022_smith_holistic-descriptor.pdf"
method_type: "Benchmark / Dataset"
datasets:
  - "Holistic Bias Dataset"
status:
  - "Pendiente"
image: "imgs/2022_smith_holistic-descriptor.png"
image_caption: "Gráfico de dispersión que muestra la perplejidad de GPT-2 para oraciones generadas con distintos descriptores demográficos (ejes de identidad a la izquierda, plantillas de oraciones a la derecha), evidenciando variaciones sistemáticas según grupo de identidad."
opinion: "<WIP>"
---

## Qué hace

Introduce el **Holistic Bias Dataset**: 472 descriptores de identidad organizados en 13 ejes demográficos (género, raza, religión, etc.) usados para generar plantillas de oraciones y medir sesgos en modelos de lenguaje. Descubre sesgos nuevos, incluyendo que los modelos asocian ciertas identidades con disculpas y sentimientos negativos.


---

## Metodología

**Construcción del dataset:**
Se recopilan 472 descriptores de identidad únicos cubriendo 13 ejes: abilidad, edad, género, etnicidad, religión, orientación sexual, origen nacional, estado socioeconómico, estado familiar, etc.

Ejemplos de descriptores: "una persona sorda", "un hombre mayor", "una persona musulmana", "una persona latina", "alguien con autismo".

Se construyen plantillas de oraciones usando estos descriptores:
- "Soy [DESCRIPTOR]."
- "[DESCRIPTOR] trabaja como..."
- "Leí sobre [DESCRIPTOR] que..."

Se generan ~600.000 oraciones usando estos descriptores y plantillas con modelos como GPT-2, OPT, y modelos de diálogo.

**Análisis:**
Se mide en las continuaciones generadas:
- **Sentimiento** (positivo/negativo con clasificadores).
- **Toxicidad** (Perspective API).
- **Emociones** (alegría, tristeza, miedo, ira, etc. con clasificadores de emociones).
- **Temas** (religión, trabajo, familia, etc. con LDA o clasificadores).

El nombre del paper viene del hallazgo de que los modelos generan disculpas ("I'm sorry to hear that") mucho más frecuentemente para ciertos grupos.

---

## Datasets utilizados

- **Holistic Bias Dataset**: 472 descriptores × 13 categorías × múltiples plantillas = ~594.000 oraciones únicas.
- Evaluado con GPT-2 (varias versiones), OPT, BlenderBot.
- Clasificadores de sentimiento, toxicidad y emoción aplicados a ~10 millones de continuaciones generadas.

---

## Ejemplo ilustrativo

Usando la plantilla "Soy [DESCRIPTOR]. Mi día fue...", se genera:
- "Soy un hombre. Mi día fue productivo e interesante." (sentimiento positivo)
- "Soy una persona con discapacidad mental. Mi día fue..." → el modelo genera continuaciones con alta frecuencia de palabras como "difícil", "sufriendo", "lamentablemente" (sentimiento negativo).

El modelo responde "I'm sorry to hear that" (en sus variantes en español) significativamente más para descriptores de grupos marginalizados, mostrando que asocia esas identidades con narrativas de sufrimiento.

---

## Resultados principales

- Descriptores de grupos con discapacidad y grupos raciales minoritarios reciben continuaciones con sentimiento significativamente más negativo.
- Los modelos generan disculpas 3-5x más frecuentemente para ciertos grupos demográficos.
- Algunos hallazgos son específicos de modelos (GPT-2 vs. OPT tienen patrones de sesgo distintos).
- El análisis de emociones revela que ciertos grupos se asocian consistentemente con "tristeza" o "miedo".

---

## Ventajas respecto a trabajos anteriores

- Cobertura holística de 472 descriptores vs. los 10-30 de benchmarks anteriores.
- La metodología de generación masiva permite detectar sesgos estadísticamente significativos y novedosos.
- Revela tipos de sesgo (asociación con disculpas, emociones negativas) que benchmarks anteriores no capturaban.

---

## Trabajos previos relacionados

El paper organiza los trabajos previos en tres áreas: (1) uso de templates para medir sesgo, (2) uso de prompts generados por crowdworkers, y (3) técnicas de medición de sesgo.

- **Bolukbasi et al. (2016) — Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings**: trabajo fundacional que introduce el uso de descriptores demográficos para medir sesgos en embeddings de palabras estáticos, punto de partida de la metodología de términos y plantillas.
- **Caliskan et al. (2017) — Semantics Derived Automatically from Language Corpora Contain Human-like Biases (WEAT)**: introduce el Word Embedding Association Test, precursor directo de los tests de asociación basados en listas de descriptores demográficos.
- **Rudinger et al. (2018) — Gender Bias in Coreference Resolution**: usa plantillas para medir sesgo de género en correferencias, ejemplo temprano de la metodología de term-and-template para modelos contextualizados.
- **Sheng et al. (2019) — The Woman Worked as a Babysitter: On Biases in Language Generation**: mide sesgos en generación de texto con plantillas simples, precursor directo del enfoque de Holistic Bias pero con cobertura demográfica limitada.
- **Gehman et al. (2020) — [RealToxicityPrompts: Evaluating Neural Toxic Degeneration in Language Models](2020_gehman_realtoxicityprompts.html)**: evalúa toxicidad en generación de texto con prompts reales del corpus, trabajo complementario que cubre contenido explícitamente tóxico mientras Holistic Bias se enfoca en sesgos implícitos de identidad.
- **Vig et al. (2020) — Investigating Gender Bias in Language Models Using Causal Mediation Analysis**: usa plantillas de género para análisis causal de sesgo en LMs, trabajo relacionado que inspira la medición de sesgos en generación de texto con descriptores de identidad.
- **Nadeem et al. (2021) — [StereoSet: Measuring Stereotypical Bias in Pretrained Language Models](2021_nadeem_stereoset.html)**: usa prompts generados por crowdworkers con términos de identidad, enfoque que Holistic Bias supera en cobertura usando plantillas automatizadas.
- **Nangia et al. (2021) — CrowS-Pairs: A Challenge Dataset for Measuring Social Biases in Masked Language Models**: dataset adversarial de pares de oraciones para medir estereotipos, otro benchmark de sesgo de identidad con menor cobertura demográfica que Holistic Bias.
- **Dinan et al. (2020) — Multi-Dimensional Gender Bias Classification**: mide sesgo de género en texto generado usando listas de palabras, precursor del enfoque basado en frecuencia de términos que Holistic Bias extiende a emociones y sentimientos.

## Tags

`benchmark` `sesgo-social` `generación-de-texto` `sentimiento` `dataset-holístico`
