---
layout: paper
title: "Understanding Dataset Difficulty with V-Usable Information"
year: 2022
authors: "Kawin Ethayarajh, Yejin Choi, Swabha Swayamdipta"
published: "ICML, 2022"
tags:
  - "benchmark"
  - "dificultad-dataset"
  - "teoría-de-información"
  - "correlaciones-espurias"
  - "evaluación"
pdf: "/llm_bias/pdfs/2022_ethayarajh_v-usable-information.pdf"
method_type: "Benchmark / Dataset"
datasets:
  - "MNLI"
  - "SNLI"
  - "QQP"
  - "QNLI"
status:
  - "Pendiente"
image: "imgs/2022_ethayarajh_v-usable-information.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
---
# Understanding Dataset Difficulty with V-Usable Information (2022)

**Autores**: Kawin Ethayarajh, Yejin Choi, Swabha Swayamdipta
**Publicado en**: ICML, 2022
**Tipo de método**: Benchmark / Dataset

---

## Qué hace

Introduce la **V-Usable Information** (V-info), una medida de teoría de la información para cuantificar la "dificultad" de un dataset para una familia de modelos específica. Revela que muchos benchmarks de NLP tienen muy baja dificultad real porque los modelos explotan correlaciones espurias.


---

## Metodología

**La intuición:** La dificultad de un dataset no es absoluta — depende de qué familia de modelos lo esté resolviendo. Un dataset puede ser "difícil" para modelos de bag-of-words pero "fácil" para transformers (porque los transformers pueden aprender patrones que los modelos simples no pueden).

**V-Usable Information:**
V-info(X→Y) mide cuánta información sobre la variable objetivo Y (etiqueta) puede extraer un modelo de la familia V a partir de las features X (texto de entrada). Formalmente es la diferencia entre la incertidumbre sobre Y sin ver X y la incertidumbre sobre Y dado X, según el mejor modelo de la familia V.

Si V-info es alta: el modelo puede extraer mucha información útil → el dataset es fácil para esa familia.
Si V-info es baja: el modelo no puede extraer información útil → el dataset es difícil.

**Aplicación:** Se computa V-info para datasets de NLP populares (MNLI, SNLI, QQP, etc.) con diferentes familias de modelos. Se usa para identificar si los modelos están resolviendo tareas por las razones correctas o por correlaciones espurias.

También se define **pointwise V-info** para ejemplos individuales: permite identificar qué ejemplos son "fáciles" o "difíciles" para un modelo específico.

---

## Datasets utilizados

- **MNLI** (inferencia textual): 433.000 pares de hipótesis-premisa.
- **SNLI** (inferencia textual): 570.000 pares.
- **QQP** (preguntas duplicadas): 400.000 pares.
- **QNLI** (QA como inferencia).
- Evaluado con familias de modelos que van desde bag-of-words hasta BERT.

---

## Ejemplo ilustrativo

En MNLI, muchas etiquetas de "contradicción" pueden predecirse sólo porque la hipótesis contiene palabras de negación como "no", "nunca", "jamás" — sin leer la premisa. Un modelo bag-of-words que sólo mira estas palabras puede predecir "contradicción" correctamente el 70% del tiempo. V-info mide exactamente esto: la fracción del rendimiento que viene de estas correlaciones espurias vs. del razonamiento lingüístico real. MNLI tiene alta V-info para modelos simples → es "fácil" por razones erróneas.

---

## Resultados principales

- SNLI y MNLI tienen alta V-info incluso para modelos muy simples, sugiriendo que muchas muestras son resolubles por correlaciones superficiales.
- Los benchmarks más difíciles (ANLI, WinoGrande) tienen V-info más baja para modelos simples.
- Pointwise V-info permite filtrar ejemplos "fáciles" para crear subsets de evaluación más rigurosos.
- Los modelos que se desempeñan bien en V-info alta no necesariamente razonan correctamente: pueden explotar artefactos del dataset.

---

## Ventajas respecto a trabajos anteriores

- Formaliza con teoría de la información el concepto intuitivo de "dificultad de dataset".
- Permite comparar dificultad entre datasets de forma principled.
- Identifica correlaciones espurias automáticamente sin necesidad de análisis manual.

---

## Trabajos previos relacionados

- **Gururangan et al. (2018) — Annotation Artifacts in Natural Language Inference Data**: identifica que muchos ejemplos de NLI son resolubles por artefactos estadísticos sin leer la premisa, motivación empírica directa para medir formalmente la "dificultad" de datasets con V-info.
- **Poliak et al. (2018) — Hypothesis Only Baselines in Natural Language Inference**: demuestra que modelos que sólo ven la hipótesis logran alta accuracy en SNLI/MNLI, evidencia concreta de correlaciones espurias que V-info cuantifica formalmente.
- **McCoy et al. (2019) — Right for the Wrong Reasons: Diagnosing Syntactic Heuristics in Natural Language Inference (HANS)**: propone un benchmark para detectar si los modelos usan heurísticas superficiales, trabajo que inspira la noción de dataset difícil para modelos simples.
- **Devlin et al. (2019) — BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding**: modelo cuyo alto rendimiento en benchmarks con correlaciones espurias es uno de los fenómenos que V-info ayuda a explicar.
- **Nie et al. (2020) — Adversarial NLI: A New Benchmark for Natural Language Understanding**: crea un dataset de NLI construido adversarialmente para ser difícil para modelos actuales, ejemplo de benchmark con V-info más baja que los datasets estándar.
- **Sakaguchi et al. (2020) — WinoGrande: An Adversarial Winograd Schema Challenge at Scale**: dataset construido para eliminar sesgos estadísticos, ejemplo de cómo aumentar la dificultad (bajar V-info) de forma deliberada.
- **Belinkov et al. (2019) — Don't Take the Easy Way Out: Ensemble Based Methods for Avoiding Known Dataset Biases**: propone métodos para que los modelos ignoren artefactos del dataset, trabajo complementario al diagnóstico que V-info proporciona.
- **Blodgett et al. (2020) — Language (Technology) is Power: A Critical Survey of "Bias" in NLP**: señala la importancia de medir correctamente el sesgo en NLP, contexto en el que V-info ofrece una formalización rigurosa.
- **Swayamditta et al. (2020) — Rethinking Dataset Cartography: Agreement-Based Debiasing**: propone cartografía de datasets para clasificar ejemplos según su dificultad, trabajo conceptualmente relacionado con la noción de pointwise V-info.

## Tags

`benchmark` `dificultad-dataset` `teoría-de-información` `correlaciones-espurias` `evaluación`
