---
layout: paper
title: "How does GPT-2 compute greater-than?: Interpreting mathematical abilities in a pre-trained language model"
year: 2023
date_published: "2023-04-30"
authors: "Michael Hanna, Ollie Liu, Alexandre Variengien"
published: "arXiv, 2023"
tags:
  - "interpretabilidad-mecanística"
  - "circuitos"
  - "GPT-2"
  - "razonamiento-numérico"
  - "MLP-layers"
pdf: "/llm_bias/pdfs/2023_hanna_gpt2-greater-than.pdf"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2023_hanna_gpt2-greater-than.png"
image_caption: "Diagrama del circuito identificado en GPT-2 para la tarea greater-than, mostrando el flujo de información entre cabezas de atención (a5.h1, a6.h9, a9.h1, etc.), capas MLP (m8–m11) y los logits de salida, con distinción entre entradas normales y entradas del tipo \"01\"."
opinion: "<WIP>"
---## Qué hace

Reverse-engineer cómo GPT-2 resuelve la tarea "greater-than": dado "La guerra duró de 1942 a 19__", el modelo debe completar con años mayores a 42. Identifica el circuito responsable y explica exactamente cómo cada componente contribuye al cómputo.


---

## Metodología

**La tarea greater-than:** Input: "The [NOUN] lasted from 18YY to 18__." El modelo debe completar con años > YY. Esto requiere una comparación numérica implícita.

**La metodología sigue tres pasos:**

1. **Identificar cabezas importantes con activation patching:** Se hace patching para identificar qué cabezas de atención y capas MLP son importantes para el rendimiento en greater-than. Se identifica que principalmente las cabezas de atención en las capas 3-8 y algunas capas MLP son cruciales.

2. **Análisis de la función de las cabezas:** Para cada cabeza identificada, se analiza qué tokens atiende y qué información transporta. Se usan técnicas como:
   - Visualización de attention patterns.
   - Probing classifiers para saber qué información está codificada en las activaciones.
   - Logit lens: proyectar las activaciones intermedias al vocabulario para ver qué predice el modelo en cada capa.

3. **Construcción del mecanismo completo:** Las cabezas en capas 3-5 atienden al año YY y codifican el valor numérico. Las capas MLP en 5-7 implementan la comparación numérica (usando sus memorias de relaciones numéricas del preentrenamiento). Las cabezas en capas 7-8 copian la información de "años mayores a YY" al token de output.

---

## Datasets utilizados

- **Dataset Greater-Than personalizado**: 1.000 ejemplos de la forma "The [NOUN] lasted from 18YY to 18__" con YY variando de 00 a 99.
- Evaluado en GPT-2 XL (1.5B parámetros).
- Comparado con GPT-2 small para verificar si el mecanismo escala.

---

## Ejemplo ilustrativo

"La guerra duró de 1942 a 19..." → GPT-2 debe completar con 43, 44, ..., 99 con alta probabilidad y con 00, 01, ..., 41 con baja probabilidad.

El análisis revela: las cabezas de atención en la capa 4 leen el "42" y lo encodean como un número en el residual stream. Las capas MLP 5-6 tienen memorias que implementan algo como "si el año es 42, los años 43-99 son mayores". Las cabezas de output en capa 8 consultan estas memorias y proyectan las probabilidades al vocabulario.

---

## Resultados principales

- El circuito de ~15 cabezas + 2-3 capas MLP preserva el 85% del rendimiento greater-than del modelo completo.
- Las capas MLP actúan como "tablas de lookup" numéricas: tienen representaciones específicas de relaciones como ">", "<" entre años.
- El mecanismo es similar en GPT-2 small y XL, sugiriendo que es una solución robusta que emerge consistentemente.

---

## Ventajas respecto a trabajos anteriores

- Primer análisis completo de cómo un LLM computa una operación matemática simple.
- Revela que las capas MLP del transformer funcionan como memorias asociativas (tablas de lookup).
- El mecanismo identificado explica por qué los LLMs tienen capacidades matemáticas limitadas: dependen de memorias del corpus de entrenamiento, no de computación algorítmica.

---

## Trabajos previos relacionados

Este trabajo se ubica en la intersección de la interpretabilidad mecanística y el razonamiento matemático en LLMs. Utiliza herramientas de análisis de circuitos previamente desarrolladas para estudiar cómo emergen capacidades numéricas en modelos preentrenados.

- **Elhage et al. (2021) — A Mathematical Framework for Transformer Circuits**: proporciona el marco formal de circuitos en transformers (residual stream, composición de cabezas) sobre el que se construye todo el análisis del paper.
- **Wang et al. (2022) — [Interpretability in the Wild: IOI Circuit](2022_wang_ioi-circuit.html)**: referencia metodológica directa; el circuito IOI en GPT-2 small es el antecedente más cercano en cuanto a análisis de circuitos completos en modelos preentrenados.
- **Goldowsky-Dill et al. (2023) — [Localizing Model Behavior with Path Patching](2023_goldowskydill_path-patching.html)**: introduce el path patching que se usa directamente en este paper para atribuir causalidad a los componentes del circuito.
- **Geva et al. (2021) — Transformer Feed-Forward Layers are Key-Value Memories**: aporta la interpretación de las capas MLP como memorias clave-valor, que el paper extiende al dominio numérico.
- **Meng et al. (2022) — Locating and Editing Factual Associations in GPT**: demuestra que el conocimiento factual se localiza en las capas FFN, motivando la búsqueda de representaciones numéricas en las MLP del circuito.
- **Vig et al. (2020) — [Investigating Gender Bias with Causal Mediation Analysis](2020_vig_gender-bias-causal.html)**: introduce el análisis de mediación causal para atribuir comportamientos a componentes del transformer, técnica adaptada en este paper.
- **Geiger et al. (2021) — [Causal Abstractions of Neural Networks](2021_geiger_causal-abstractions.html)**: proporciona el marco de intervenciones causales que fundamenta las ablaciones causales del paper.
- **Nanda et al. (2023) — Progress Measures for Grokking via Mechanistic Interpretability**: muestra cómo el análisis de circuitos puede explicar la adquisición de capacidades matemáticas en modelos entrenados desde cero, contexto complementario al estudio de modelos preentrenados.
- **Olah et al. (2020) — Zoom In: An Introduction to Circuits**: trabajo fundacional de la perspectiva de circuitos en redes neuronales que inspira la metodología general del paper.
- **Brown et al. (2020) — Language Models are Few-Shot Learners**: establece que los LLMs adquieren capacidades matemáticas sin entrenamiento explícito, motivando la pregunta central del paper sobre cómo ocurre esto internamente.

## Tags

`interpretabilidad-mecanística` `circuitos` `GPT-2` `razonamiento-numérico` `MLP-layers`
