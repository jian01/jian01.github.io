---
layout: paper
title: "MABEL: Attenuating Gender Bias using Textual Entailment Data"
year: 2022
date_published: "2022-10-26"
authors: "Jacqueline He, Mengzhou Xia, Christiane Fellbaum, Danqi Chen"
published: "EMNLP, 2022"
tags:
  - "debiasing"
  - "NLI"
  - "contrastive-learning"
  - "sesgo-de-género"
  - "BERT"
pdf: "/llm_bias/pdfs/2022_he_mabel.pdf"
method_type: "Fine-tuning / data augmentation"
datasets:
  - "SNLI + MultiNLI"
  - "StereoSet"
  - "SEAT"
  - "CrowS-Pairs"
  - "WinoBias"
  - "GLUE"
measures_general_quality: "Sí"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2022_he_mabel.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---## Qué hace

Propone MABEL (**M**itigating **A**ssociations via **B**alanced **E**ntailment **L**earning), un método de debiasing de género que usa datos de inferencia textual (NLI) para crear un objetivo de aprendizaje contrastivo que alinea las representaciones de oraciones equivalentes excepto por el género.


---

## Metodología

**La idea central:** Dos oraciones que sólo difieren en el género del sujeto deberían tener representaciones similares en el espacio de embeddings del modelo. Ej: "La médica examinó al paciente" y "El médico examinó al paciente" deberían ser representadas de forma muy similar.

**Construcción de los datos de entailment:**
Se usan pares de oraciones de SNLI/MultiNLI donde una oración implica a la otra. Se aplica CDA para crear versiones de género intercambiado. Así se obtienen pares:
- (oración_original_femenina, oración_original_masculina) → deberían tener representaciones similares
- (oración_contrafactual_femenina, oración_contrafactual_masculina) → también deberían ser similares
- (oración_femenina, oración_masculina_no_entailment) → deberían ser diferentes

**El objetivo de entrenamiento:**
Se entrena el encoder (BERT/RoBERTa) con un objetivo de aprendizaje contrastivo:
1. **Contrastive loss**: las representaciones de pares de género intercambiado de la misma oración deben ser cercanas en el espacio vectorial.
2. **Entailment-preserving loss**: la estructura de entailment entre oraciones debe preservarse (si A implica B, sus representaciones deberían reflejar esto).

Las capas que se modifican son las **capas de self-attention y FFN de BERT/RoBERTa** durante el fine-tuning contrastivo.

---

## Datasets utilizados

- **SNLI + MultiNLI**: ~900.000 pares de entailment usados para crear los datos de debiasing.
- **StereoSet, SEAT, CrowS-Pairs**: evaluación de sesgo.
- **WinoBias**: evaluación de sesgo de género en correferencias.
- **GLUE**: evaluación de downstream performance.

---

## Ejemplo ilustrativo

Par de entailment: "La ingeniera diseñó el puente" → implica → "Alguien diseñó algo."

Versión de género intercambiado: "El ingeniero diseñó el puente" → implica → "Alguien diseñó algo."

MABEL entrena al modelo para que:
1. Las representaciones de "La ingeniera diseñó el puente" y "El ingeniero diseñó el puente" sean similares.
2. Ambas representaciones sean distintas de oraciones sobre temas diferentes.
3. La relación de entailment con "Alguien diseñó algo" se preserve en ambos casos.

---

## Resultados principales

- MABEL logra el mejor trade-off sesgo/rendimiento entre los métodos evaluados al momento de su publicación.
- En SEAT, reduce la magnitud del sesgo de 0.64 a 0.21 (0 es ideal).
- En WinoBias, mejora la equidad de resolución de correferencias en un 15%.
- Degradación en GLUE: <1%, mejor que CDA y SentenceDebias.

---

## Ventajas respecto a trabajos anteriores

- Usa NLI como datos de entrenamiento debiasing: aprovecha millones de pares disponibles gratuitamente.
- El objetivo contrastivo basado en entailment es más principled que la augmentación simple de datos.
- Mejor balance entre reducción de sesgo y preservación de capacidades que métodos anteriores.

---

## Trabajos previos relacionados

El paper divide los trabajos previos de debiasing de representaciones en dos categorías: métodos específicos por tarea (task-specific) y métodos agnósticos de tarea (task-agnostic), siendo MABEL de la segunda categoría.

- **Ravfogel et al. (2020) — Null It Out: Guarding Protected Attributes by Iterative Nullspace Projection (INLP)**: método de proyección que elimina iterativamente información de atributos protegidos del espacio de embeddings, representante principal de los enfoques basados en proyección geométrica que MABEL mejora.
- **Liang et al. (2020) — Towards Debiasing Sentence Representations (SentDebias)**: computa el subespacio de género y lo proyecta fuera de las representaciones, método task-agnostic que es una de las principales comparaciones de MABEL.
- **Kaneko & Bollegala (2021) — Debiasing Pre-trained Contextualised Embeddings (Context-Debias)**: elimina el subespacio de género de representaciones contextualizadas usando pares de género intercambiado, otra comparación directa de MABEL con resultados similares en SEAT pero peores en WinoBias.
- **Webster et al. (2020) — Measuring and Reducing Gendered Correlations in Pre-trained Models (CDA + Dropout)**: usa counterfactual data augmentation (CDA) y mayor dropout para reducir asociaciones de género, método que MABEL supera en el trade-off sesgo/rendimiento.
- **Cheng et al. (2021) — FairFil: Contrastive Neural Debiasing Method for Pretrained Text Encoders (FairFil)**: método contrastivo task-agnostic más directamente comparable a MABEL por usar también aprendizaje contrastivo, pero sin aprovechar datos de NLI.
- **Gao et al. (2021) — SimCSE: Simple Contrastive Learning of Sentence Embeddings**: introduce el aprendizaje contrastivo de oraciones que MABEL adapta para el debiasing, siendo la base del componente de pérdida contrastiva del método.
- **May et al. (2019) — On Measuring Social Biases in Sentence Encoders (SEAT)**: introduce la métrica SEAT (Sentence Encoder Association Test) que es el principal benchmark intrínseco de evaluación usado en el paper.
- **Zhao et al. (2018) — Gender Bias in Coreference Resolution: Evaluation and Debiasing Methods (WinoBias)**: introduce el dataset WinoBias para evaluar sesgo de género en resolución de correferencias, una de las evaluaciones extrínsecas clave del paper.
- **Goldfarb-Tarrant et al. (2021) — Intrinsic Bias Metrics Do Not Correlate with Application Bias**: demuestra que las métricas intrínsecas (SEAT) no correlacionan con el rendimiento en tareas reales, motivación para que MABEL evalúe tanto métricas intrínsecas como extrínsecas.

## Tags

`debiasing` `NLI` `contrastive-learning` `sesgo-de-género` `BERT`
