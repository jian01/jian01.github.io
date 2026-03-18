---
layout: paper
title: "Task-Specific Skill Localization in Fine-tuned Language Models"
year: 2023
date_published: "2023-02-13"
authors: "Abhishek Panigrahi, Nikunj Saunshi, Haoyu Zhao, Sanjeev Arora"
published: "arXiv, 2023"
tags:
  - "interpretabilidad"
  - "localización-habilidades"
  - "fine-tuning"
  - "sparse-masks"
  - "BERT"
pdf: "/llm_bias/pdfs/2023_panigrahi_skill-localization.pdf"
status:
  - "Leido"
image: "imgs/2023_panigrahi_skill-localization.png"
image_caption: "Imagen asociada al paper sobre localización de habilidades específicas en modelos de lenguaje fine-tuneados."
opinion: "<WIP>"
---

## Qué hace

Estudia qué partes de un LLM fine-tuneado son responsables de las habilidades específicas de la tarea vs. las capacidades generales pre-entrenadas. Descubre que los cambios de fine-tuning son esparsos y localizados, y aprende "sparse masks" que identifican el subconjunto mínimo de parámetros responsables de cada habilidad.


---

## Metodología

**La pregunta central:** Cuando fine-tuneamos BERT en análisis de sentimiento, ¿se actualiza el modelo entero o sólo ciertas partes? ¿Las partes actualizadas son las que "saben" sentimientos o son cambios distribuidos?

**Sparse Mask Learning:**
Se aprende una máscara binaria M sobre los parámetros del modelo fine-tuneado tal que:
1. El modelo con sólo los parámetros M activados (y el resto reseteado al valor pre-entrenado) mantiene el rendimiento en la tarea fine-tuneada.
2. La máscara M es lo más esparsa posible (mínimo número de parámetros activados).

Esto se logra con una regularización L0 sobre M durante el aprendizaje de la máscara. La máscara se aprende capa por capa.

**Lo que revela:**
- Las habilidades de las tareas downstream están localizadas en un subconjunto pequeño de parámetros.
- Este subconjunto es diferente para cada tarea.
- Los parámetros fuera de la máscara son esencialmente iguales al modelo pre-entrenado.

---

## Datasets utilizados

- **GLUE**: tareas de NLP (SST-2, MNLI, QQP, QNLI, RTE, STS-B).
- **SuperGLUE**: BoolQ, MultiRC.
- Evaluado en BERT-base, RoBERTa-base, T5-base.

---

## Ejemplo ilustrativo

Se fine-tunea BERT en análisis de sentimiento (SST-2). El modelo tiene 110M parámetros. La sparse mask revela que sólo el 5% de los parámetros (5.5M) cambiaron significativamente respecto al modelo pre-entrenado y son responsables del rendimiento en SST-2. El 95% restante podría resetearse a sus valores pre-entrenados sin pérdida de accuracy.

Esto tiene implicaciones prácticas: si alguien quiere modificar sólo la habilidad de sentimiento sin afectar otras capacidades, sólo necesita tocar ese 5% de parámetros.

---

## Resultados principales

- Las habilidades de fine-tuning son esparsas: 5-20% de los parámetros son suficientes para mantener el rendimiento en la tarea.
- Las máscaras son específicas por tarea: superposición entre máscaras de diferentes tareas es sólo del 20-30%.
- Los parámetros más importantes están concentrados en las últimas capas del transformer y en las cabezas de atención.
- El análisis revela que el fine-tuning no "reescribe" el conocimiento pre-entrenado sino que añade una capa adicional de especialización.

---

## Ventajas respecto a trabajos anteriores

- Las sparse masks son más interpretables que los gradientes de atribución: identifican explícitamente qué parámetros son esenciales.
- Demuestra la modularidad del conocimiento en LLMs fine-tuneados.
- Tiene implicaciones directas para edición de modelos, unlearning, y transferencia de conocimiento.

---

## Trabajos previos relacionados

El paper organiza los trabajos relacionados en tres categorías: conocimiento/habilidades en LLMs, fine-tuning eficiente en parámetros (PEFT), y la hipótesis de billetes de lotería. Esta estructura refleja las tres líneas de investigación que convergen en la localización de habilidades.

- **Wang et al. (2022) — [Skill Neurons in Language Models](2022_wang_skill-neurons.html)**: descubren neuronas "skill" altamente predictivas de tareas downstream en soft prompt-tuning, trabajo directamente relacionado con la localización de habilidades que este paper extiende al contexto del fine-tuning supervisado.
- **Meng et al. (2022) — Locating and Editing Factual Associations in GPT (ROME)**: demuestra que el conocimiento factual se localiza en las capas FFN de los modelos, motivando la hipótesis de que las habilidades de fine-tuning también están localizadas.
- **Dai et al. (2022) — Knowledge Neurons in Pretrained Transformers**: identifica neuronas cuya activación correlaciona con hechos específicos en BERT, antecedente directo de la idea de localización de conocimiento/habilidades.
- **Frankle & Carbin (2018) — The Lottery Ticket Hypothesis**: el paper contrasta explícitamente su método con LTH, argumentando que las sparse masks de grafting son más interpretables que los "billetes de lotería" clásicos.
- **Ben-Zaken et al. (2022) — BitFit: Simple Parameter-efficient Fine-tuning**: actualiza solo los sesgos durante el fine-tuning con rendimiento comparable; representa el estado del arte en PEFT contra el que se compara el método de grafting.
- **Houlsby et al. (2019) — Parameter-Efficient Transfer Learning (Adapters)**: método PEFT fundacional que entrena pequeños módulos adicionales entre capas, contexto para entender la localización de habilidades como guía para PEFT.
- **Yang et al. (2022) — [Task-Specific Compression via Pruning](2022_yang_task-specific-compression.html)**: trabajo relacionado sobre identificación de subnetworks específicos por tarea, que aborda el problema de localización desde la perspectiva de la compresión.
- **Li et al. (2022) — The Lazy Neuron Phenomenon**: muestra que las activaciones feed-forward son esparsas en modelos grandes, evidencia que apoya la hipótesis de localización de habilidades del paper.

## Tags

`interpretabilidad` `localización-habilidades` `fine-tuning` `sparse-masks` `BERT`
