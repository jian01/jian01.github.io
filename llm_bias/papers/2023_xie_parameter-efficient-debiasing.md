---
layout: paper
title: "An Empirical Analysis of Parameter-Efficient Methods for Debiasing Pre-Trained Language Models"
year: 2023
authors: "Zhongbin Xie, Thomas Lukasiewicz"
published: "ACL, 2023"
tags:
  - "debiasing"
  - "LoRA"
  - "PEFT"
  - "adapters"
  - "fine-tuning-eficiente"
pdf: "/llm_bias/pdfs/2023_xie_parameter-efficient-debiasing.pdf"
method_type: "Adapters / PEFT"
datasets:
  - "StereoSet"
  - "CrowS-Pairs"
  - "SEAT"
  - "WinoBias"
  - "GLUE"
measures_general_quality: "Sí"
status:
  - "Pendiente"
image: "imgs/2023_xie_parameter-efficient-debiasing.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---
# An Empirical Analysis of Parameter-Efficient Methods for Debiasing Pre-Trained Language Models (2023)

**Autores**: Zhongbin Xie, Thomas Lukasiewicz
**Publicado en**: ACL, 2023
**Tipo de método**: Adapters / PEFT

---

## Qué hace

Compara sistemáticamente múltiples métodos de fine-tuning eficiente en parámetros (PEFT) aplicados al debiasing: LoRA, adapters, prefix tuning, y prompt tuning. Identifica qué método logra el mejor balance entre reducción de sesgo y preservación de rendimiento.


---

## Metodología

Los métodos PEFT reducen el número de parámetros entrenables manteniendo los pesos del modelo base congelados. Este paper los compara como herramientas de debiasing:

**Métodos evaluados:**

1. **LoRA (Low-Rank Adaptation):** Añade matrices de bajo rango adicionales a las capas de atención (Q, K, V, O). En lugar de actualizar W, entrena ΔW = A×B donde A y B son matrices de rango pequeño. Modifica efectivamente las capas de atención sin cambiar los pesos originales.

2. **Adapters:** Módulos bottleneck insertados entre capas del transformer. Sólo los parámetros del adapter se entrenan. (Ver Gira et al. 2022).

3. **Prefix tuning:** Añade vectores "prefix" entrenables al principio de las secuencias de clave y valor en cada capa de atención. El resto del modelo no cambia.

4. **Prompt tuning:** Añade tokens virtuales entrenables al inicio del input. La capa de embeddings no se modifica; sólo los embeddings de los tokens virtuales.

Todos se entrenan sobre datos de CDA (Counterfactual Data Augmentation) con el mismo objetivo.

---

## Datasets utilizados

- **StereoSet**: benchmark principal de sesgo.
- **CrowS-Pairs**: pares sesgados/no sesgados.
- **SEAT**: asociaciones en embeddings.
- **WinoBias**: correferencias de género.
- **GLUE**: degradación de rendimiento en downstream tasks.
- Modelos evaluados: BERT-base, RoBERTa-base, BERT-large.

---

## Ejemplo ilustrativo

Para el mismo objetivo de debiasing (hacer que BERT trate equitativamente a hombres y mujeres en oraciones de profesiones), los cuatro métodos modifican partes distintas del modelo:
- LoRA: modifica matrices Q/K/V en todas las capas de atención.
- Adapters: añade módulos entre capas.
- Prefix tuning: añade vectores al principio de cada secuencia en el espacio de atención.
- Prompt tuning: añade tokens al input original.

El resultado: LoRA logra mejor balance que los demás; prompt tuning preserva mejor el rendimiento pero reduce menos el sesgo.

---

## Resultados principales

- **LoRA** es el mejor PEFT para debiasing: mayor reducción de sesgo con menor degradación de rendimiento.
- Adapters quedan en segundo lugar, seguidos de prefix tuning.
- Prompt tuning es el más conservador: mínima degradación pero también menor reducción de sesgo.
- Todos los PEFT superan al fine-tuning completo en preservación de rendimiento, con reducción de sesgo comparable.

---

## Ventajas respecto a trabajos anteriores

- Primera comparación sistemática de múltiples PEFT métodos para debiasing.
- Revela que la elección del método PEFT importa: no todos son igualmente efectivos.
- La conclusión de que LoRA es el mejor método para debiasing es prácticamente relevante dado el uso generalizado de LoRA.

---

## Trabajos previos relacionados

El paper se sitúa en dos líneas: (1) métodos de debiasing para PLMs, y (2) métodos de fine-tuning eficiente en parámetros. Para el debiasing, cita principalmente trabajos basados en fine-tuning con CDA y métodos post-hoc. Para los métodos PEFT, cita los trabajos originales que los propusieron.

- **Meade et al. (2022) — An empirical survey of the effectiveness of debiasing techniques**: estudio empírico del que este paper adopta el protocolo de evaluación y los benchmarks de referencia; [2021_meade_debiasing-survey.md](2021_meade_debiasing-survey.html)
- **Nadeem et al. (2021) — StereoSet**: benchmark de sesgo estereotípico usado como métrica principal de evaluación; [2021_nadeem_stereoset.md](2021_nadeem_stereoset.html)
- **Gira et al. (2022) — Debiasing pre-trained language models via efficient fine-tuning**: trabajo previo más directo que aplica adapters para debiasing, al que este paper extiende y compara sistemáticamente; [2022_gira_debiasing-efficient-finetuning.md](2022_gira_debiasing-efficient-finetuning.html)
- **He et al. (2022) — MABEL**: trabajo que aplica contrastive learning con métodos PEFT para debiasing de género; [2022_he_mabel.md](2022_he_mabel.html)
- **Lauscher et al. (2021) — Sustainable modular debiasing of language models**: aplica adapters para debiasing de forma modular, siendo una referencia directa del enfoque de este paper.
- **Li & Liang (2021) — Prefix-Tuning**: artículo original que propone prefix tuning, uno de los tres métodos PEFT evaluados en este estudio.
- **Lester et al. (2021) — The power of scale for parameter-efficient prompt tuning**: artículo original de prompt tuning, otro de los métodos evaluados.
- **Houlsby et al. (2019) — Parameter-efficient transfer learning for NLP**: artículo original de adapter tuning, tercer método evaluado.
- **Liang et al. (2020) — Towards debiasing sentence representations (SentenceDebias)**: método post-hoc de referencia con el que se compara empíricamente en los experimentos.
- **Schick et al. (2021) — Self-diagnosis and self-debiasing**: segundo método post-hoc de referencia en las comparaciones empíricas.

## Tags

`debiasing` `LoRA` `PEFT` `adapters` `fine-tuning-eficiente`
