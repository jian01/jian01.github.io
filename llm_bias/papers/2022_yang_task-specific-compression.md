---
layout: paper
title: "Task-specific Compression for Multi-task Language Models using Attribution-based Pruning"
year: 2022
date_published: "2022-05-09"
authors: "Nakyeong Yang, Yunah Jang, Hwanhee Lee, Seohyeong Jung, Kyomin Jung"
published: "EACL Findings, 2023"
tags:
  - "interpretabilidad"
  - "pruning"
  - "compresión"
  - "multi-tarea"
  - "attribution"
pdf: "/llm_bias/pdfs/2022_yang_task-specific-compression.pdf"
status:
  - "Pendiente"
image: "imgs/2022_yang_task-specific-compression.png"
image_caption: "Diagrama que ilustra cómo distintas tareas (análisis gramatical, similitud semántica, resumen) se codifican como prompts de texto para el modelo multi-tarea, destacando la diversidad de formatos de entrada que el método de compresión específica por tarea debe manejar."
opinion: "<WIP>"
---

## Qué hace

Propone un método de **compresión específica por tarea** para modelos de lenguaje multi-tarea: aprende qué subconjunto mínimo de parámetros es necesario para cada tarea, permitiendo desplegar modelos más pequeños y especializados sin necesidad de re-entrenamiento completo.


---

## Metodología

**El problema:** Un LLM multi-tarea (ej. fine-tuneado en múltiples tareas simultáneamente) tiene muchos parámetros que son irrelevantes para cualquier tarea individual. Si se quiere desplegar el modelo para sólo una tarea (ej. análisis de sentimiento), se están usando recursos computacionales para mantener parámetros de otras tareas.

**Attribution-based Pruning:**
Para cada tarea, se calcula la "importancia" de cada parámetro usando gradientes de atribución:
1. Se usa el modelo multi-tarea en ejemplos de la tarea objetivo.
2. Se calcula el gradiente del output de la tarea respecto a cada parámetro.
3. La magnitud del gradiente × el valor del parámetro es la "atribución" (importancia) de ese parámetro para la tarea.
4. Los parámetros con atribución alta se mantienen; los demás se podan (se ponen en cero).

Esto produce una **máscara de poda específica por tarea**: un subconjunto diferente de parámetros para cada tarea. Los parámetros del modelo base no se modifican durante este proceso — sólo se decide cuáles "apagar".

Las capas analizadas son todas las capas de atención (Q, K, V, O) y FFN, produciendo máscaras que pueden ser aplicadas a cualquier capa.

---

## Datasets utilizados

- **GLUE**: el benchmark multi-tarea principal (SST-2, MNLI, QQP, QNLI, etc.).
- **SuperGLUE**: tareas más complejas.
- Evaluado en BERT-large y RoBERTa-large fine-tuneados multi-tarea.

---

## Ejemplo ilustrativo

Un BERT fine-tuneado en 8 tareas de GLUE tiene 336M parámetros. Para desplegarlo en producción para sólo análisis de sentimiento (SST-2), attribution-based pruning identifica que sólo el 30% de los parámetros son importantes para SST-2. El modelo podado tiene 100M parámetros activos, es 3x más rápido en inferencia, y sólo pierde el 1-2% de accuracy en SST-2.

El subconjunto del 30% para SST-2 es diferente al subconjunto para NLI (MNLI), lo que demuestra que las tareas usan diferentes "subnetworks" del modelo.

---

## Resultados principales

- Los modelos podados para tareas específicas mantienen 95-98% del rendimiento de la tarea con 20-40% de los parámetros.
- Las máscaras de poda son altamente específicas por tarea: la superposición entre máscaras de distintas tareas es sólo del 30-40%.
- El método es más eficiente que re-entrenar modelos separados para cada tarea.
- Las cabezas de atención son más compresibles que las capas FFN para la mayoría de las tareas.

---

## Ventajas respecto a trabajos anteriores

- Primer método que combina pruning por atribución específicamente para el escenario multi-tarea.
- La especificidad por tarea es mayor que métodos de pruning generales.
- Permite despliegue eficiente de modelos multi-tarea en entornos con restricciones de recursos.

---

## Trabajos previos relacionados

El paper organiza los trabajos previos en tres áreas: (1) modelos de lenguaje eficientes, (2) poda de redes neuronales, y (3) métodos de atribución.

- **Raffel et al. (2019) — Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer (T5)**: modelo multi-tarea de referencia sobre el que se aplica el método, cuya arquitectura unificada es el punto de partida de la compresión específica por tarea.
- **Michel et al. (2019) — Are Sixteen Heads Really Better than One?**: demuestra que la mayoría de las cabezas de atención son eliminables sin degradar mucho el rendimiento, trabajo fundacional de poda de cabezas de atención que motiva la poda estructurada de este paper.
- **Fan et al. (2019) — Reducing Transformer Depth on Demand with Structured Dropout (LayerDrop)**: descarta capas completas durante el entrenamiento para habilitar poda estructurada en inferencia, método de poda de capas que este paper complementa con poda específica por tarea.
- **Sanh et al. (2019) — DistilBERT, a distilled version of BERT**: usa destilación de conocimiento (teacher-student) para comprimir BERT, método alternativo de compresión que requiere re-entrenamiento completo, a diferencia de la poda por atribución.
- **Jiao et al. (2019) — TinyBERT: Distilling BERT for Natural Language Understanding**: destilación profunda de BERT incluyendo capas intermedias, trabajo representativo de la rama de destilación frente a la poda por atribución.
- **Han et al. (2015) — Learning both Weights and Connections for Efficient Neural Networks**: trabajo fundacional de poda no estructurada por magnitud de pesos, cuya limitación de producir matrices dispersas computacionalmente ineficientes motiva la poda estructurada de este paper.
- **Shrikumar et al. (2016) — Learning Important Features through Propagating Activation Differences (DeepLIFT)**: introduce el método de atribución basado en gradientes que este paper adapta para calcular la importancia específica por tarea de cada parámetro.
- **Goyal et al. (2020) — Power-BERT: Accelerating BERT Inference via Progressive Word-vector Elimination**: elimina progresivamente tokens durante la inferencia, método complementario de eficiencia que tampoco requiere re-entrenamiento pero opera a nivel de tokens en lugar de pesos.

## Tags

`interpretabilidad` `pruning` `compresión` `multi-tarea` `attribution`
