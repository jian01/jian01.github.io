---
layout: paper
title: "Language Models Get a Gender Makeover: Mitigating Gender Bias with Few-Shot Data Interventions"
year: 2023
date_published: "2023-06-07"
authors: "Himanshu Thakur, Atishay Jain, Praneetha Vaddamanu, Percy Liang, Louis-Philippe Morency"
published: "ACL, 2023"
tags:
  - "debiasing"
  - "few-shot"
  - "in-context-learning"
  - "sesgo-de-género"
  - "sin-entrenamiento"
pdf: "/llm_bias/pdfs/2023_thakur_gender-makeover.pdf"
method_type: "Fine-tuning / data augmentation"
datasets:
  - "WinoBias"
  - "StereoSet"
  - "BBQ"
measures_general_quality: "No"
status:
  - "Leido"
image: "imgs/2023_thakur_gender-makeover.png"
image_caption: "Gráfico de barras mostrando la frecuencia de palabras asociadas al género en el dataset analizado: términos masculinos como \"he\", \"his\" y \"him\" dominan ampliamente frente a términos femeninos, ilustrando el desequilibrio de representación de género."
opinion: "<WIP>"
---

## Qué hace

Propone reducir el sesgo de género en LLMs usando sólo unas pocas docenas de ejemplos contrafactuales como demostraciones de few-shot learning. No requiere fine-tuning: funciona sólo modificando el contexto del prompt.


---

## Metodología

La observación clave es que el in-context learning (few-shot) puede cambiar sustancialmente el comportamiento de un LLM. Si se le muestran ejemplos donde el género es tratado equitativamente, el modelo tenderá a seguir ese patrón.

**Construcción de los ejemplos few-shot:**
Se crean pares de ejemplos de "datos intervenidos" — historias cortas o situaciones donde:
1. Los roles de género están explícitamente invertidos respecto a los estereotipos.
2. Las mujeres ocupan roles de alta autoridad y los hombres roles de cuidado, y viceversa.
3. Los pronombres son usados de forma balanceada y no estereotipada.

Por ejemplo:
- Ejemplo intervención: "La cirujana jefa presentó su investigación. Su colega enfermero preparó los materiales."
- Ejemplo normal (estereotipado): "El cirujano jefe presentó su investigación. Su colega enfermera preparó los materiales."

Estos ejemplos se incluyen como demostraciones al inicio del prompt. El modelo, al ver estos patrones en el contexto, genera respuestas más equilibradas.

**Selección de ejemplos:**
Se prueba que la selección importa: ejemplos de alta calidad (claramente contrafactuales y variados) funcionan mejor que ejemplos aleatorios. Se propone un algoritmo de selección basado en diversidad.

---

## Datasets utilizados

- **WinoBias**: evaluación principal de sesgo de género en correferencias.
- **StereoSet**: completación de oraciones.
- **BBQ**: preguntas de opción múltiple.
- Datasets de generación de texto libre con plantillas de género.

---

## Ejemplo ilustrativo

Sin intervención, ante el prompt "El médico le dijo a la enfermera que ella debería...", el modelo resuelve "ella" como referente a la enfermera (asumiendo que la enfermera es mujer). Con las demostraciones few-shot de historias con géneros invertidos, el modelo aprende que el pronombre "ella" puede referirse al médico, y resuelve la ambigüedad de forma más equitativa.

---

## Resultados principales

- Con 32 ejemplos few-shot, WinoBias score mejora del 60% (equidad) al 75-80% en GPT-3 y GPT-4.
- Comparado con fine-tuning sobre miles de ejemplos, los resultados son competitivos con sólo 32-64 ejemplos.
- La calidad de los ejemplos importa: ejemplos seleccionados con diversidad superan ejemplos aleatorios en un 10%.
- El método funciona mejor con modelos más grandes (mayor capacidad de in-context learning).

---

## Ventajas respecto a trabajos anteriores

- Extremadamente eficiente: sólo 32-64 ejemplos vs. miles para fine-tuning.
- Sin costo de entrenamiento: aplicable en producción sin necesidad de actualizar pesos.
- El análisis de qué hace que los ejemplos sean efectivos es una contribución científica independiente.

---

## Trabajos previos relacionados

El paper sitúa su contribución dentro de dos líneas de investigación: el análisis del sesgo de género en LLMs preentrenados y los métodos de debiasing, con énfasis particular en aquellos basados en datos.

- **Nadeem et al. (2021) — [StereoSet](2021_nadeem_stereoset.html)**: benchmark de evaluación de estereotipos socidemográficos que el paper usa como métrica principal de evaluación del debiasing logrado.
- **He et al. (2022) — [MABEL](2022_he_mabel.html)**: método de debiasing que combina augmentación de datos por intercambio de género con aprendizaje contrastivo; la estrategia de augmentación es directamente comparable con las intervenciones de datos propuestas en este paper, aunque MABEL requiere entrenamiento de modelos auxiliares.
- **Bolukbasi et al. (2016) — Man is to Computer Programmer as Woman is to Homemaker?**: trabajo clásico de debiasing en word embeddings que establece la técnica de "equalización" en el espacio de embeddings, antecedente histórico de los métodos de debiasing de datos.
- **Maudslay et al. (2019) — It's All in the Name: Mitigating Gender Bias with Name-Based Counterfactual Data Substitution**: propone la sustitución de nombres de género como método de CDA, técnica que el paper toma como referencia directa para su método de intervención.
- **Kirk et al. (2021) — Bias Out-of-the-Box: An Empirical Analysis of Intersectional Occupational Biases in Popular Generative Language Models**: documenta el sesgo de género en GPT-2, motivando las evaluaciones del paper.
- **Parrish et al. (2021) — [BBQ: A Hand-Built Bias Benchmark for Question Answering](2021_parrish_bbq.html)**: benchmark de preguntas de opción múltiple con ambigüedad de sesgo que el paper usa como uno de sus datasets de evaluación.
- **Zhang et al. (2018) — Mitigating Unwanted Biases with Adversarial Learning**: método algorítmico de debiasing mediante pérdida adversarial, referencia representativa del enfoque algorítmico que el paper contrasta con su propuesta basada en datos.
- **Meade et al. (2021) — [An Empirical Survey of the Effectiveness of Debiasing Techniques](2021_meade_debiasing-survey.html)**: encuesta empírica de técnicas de debiasing que proporciona el contexto comparativo para evaluar la efectividad relativa del método del paper.

## Tags

`debiasing` `few-shot` `in-context-learning` `sesgo-de-género` `sin-entrenamiento`
