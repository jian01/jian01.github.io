---
layout: paper
title: "Machine Unlearning"
year: 2021
date_published: "2019-12-09"
authors: "Lucas Bourtoule, Varun Chandrasekaran, Christopher A. Choquette-Choo, Hengrui Jia, Adelin Travers, Baiwu Zhang, David Lie, Nicolas Papernot"
published: "IEEE Symposium on Security and Privacy (S&P), 2021"
tags:
  - "machine-unlearning"
  - "SISA"
  - "exact-unlearning"
  - "privacidad"
  - "reentrenamiento"
pdf: "/llm_bias/pdfs/2021_bourtoule_sisa.pdf"
method_type: "Reentrenamiento exacto"
status:
  - "Pendiente"
image: "imgs/2021_bourtoule_sisa.png"
image_caption: "El framework SISA divide los datos en shards (particiones independientes) y slices (subsecuencias), permitiendo reentrenar solo el shard afectado ante una solicitud de borrado."
opinion: "<WIP>"
---## Qué hace

Introduce **SISA training** (*Sharded, Isolated, Sliced, Aggregated*), el primer framework sistemático para que modelos de machine learning "olviden" datos de entrenamiento de forma eficiente. El problema central es el siguiente: si un usuario solicita que sus datos sean eliminados de un modelo ya entrenado (como requiere el GDPR), la única forma garantizada de hacerlo es reentrenar el modelo desde cero sin esos datos, lo que es prohibitivamente caro.

SISA resuelve esto reorganizando el proceso de entrenamiento de antemano, de modo que cuando llegue una solicitud de borrado, solo sea necesario reentrenar una pequeña fracción del modelo en lugar del modelo completo. No modifica la arquitectura del modelo sino la **estrategia de entrenamiento y partición de los datos**.


---

## Metodología

SISA se basa en tres transformaciones del proceso de entrenamiento:

1. **Sharding (particionamiento)**: Los datos de entrenamiento se dividen en *k* particiones (*shards*) disjuntas. Se entrena un modelo separado (*constituyente*) en cada shard. La predicción final es el agregado de los *k* modelos (por ejemplo, promediando logits). Cuando se pide borrar un dato, solo el modelo del shard que contenía ese dato necesita reentrenarse.

2. **Slicing (segmentación temporal)**: Dentro de cada shard, los datos se dividen en *m* segmentos (*slices*) que se añaden progresivamente durante el entrenamiento. Se guardan checkpoints del modelo al final de cada slice. Al borrar un dato, se restaura el checkpoint justo antes del slice que lo contenía y se continúa entrenando solo desde ahí.

3. **Aggregation (agregación)**: Los modelos constituyentes se combinan para la predicción final. El método de agregación (mayoría de votos, promedio de probabilidades, etc.) se elige según la tarea.

La combinación de sharding y slicing hace que el número de épocas que hay que reejecutar al borrar un dato sea proporcional a *1/(k·m)* en lugar de 1.

---

## Datasets utilizados

- **Purchase-100**: Dataset de comportamiento de compras con 197,324 muestras y 100 clases.
- **SVHN** (Street View House Numbers): Clasificación de dígitos en imágenes.
- **ImageNet**: Clasificación de imágenes a gran escala (1.2M imágenes, 1000 clases).

---

## Ejemplo ilustrativo

Supongamos que se entrena un modelo de clasificación con 1 millón de ejemplos de usuarios. El usuario #47,823 solicita que sus 10 ejemplos sean borrados. Sin SISA, hay que reentrenar el modelo completo con 999,990 ejemplos (~72 horas de GPU).

Con SISA (k=100 shards, m=10 slices): los 10 ejemplos del usuario caen todos en el shard #38. Solo hay que reentrenar el modelo del shard #38 a partir del checkpoint del slice donde aparecía el primer dato del usuario. En práctica, esto tarda ~15 minutos en lugar de 72 horas.

---

## Resultados principales

- En Purchase-100, SISA acelera el desaprendizaje **4.63×** respecto al reentrenamiento completo sin pérdida de precisión.
- En SVHN, la aceleración es de **2.45×**.
- En ImageNet con transfer learning, la aceleración es de **1.36×** con una caída de precisión marginal (<0.5%).
- Si se conoce de antemano la distribución de solicitudes de borrado, la aceleración puede ser significativamente mayor al ordenar los datos estratégicamente.

---

## Ventajas respecto a trabajos anteriores

- Es el primer método de **exact unlearning** para redes neuronales profundas que no requiere reentrenamiento completo.
- A diferencia de los métodos de unlearning aproximado, las garantías son exactas: el modelo reentrenado es estadísticamente indistinguible de uno que nunca vio los datos borrados.
- El framework es agnóstico a la arquitectura y puede aplicarse a cualquier algoritmo de entrenamiento basado en gradientes.
- Convierte el unlearning en un problema de ingeniería de datos (cómo organizar el entrenamiento) en lugar de un problema post-hoc.

---

## Trabajos previos relacionados

El paper revisa el campo emergente del machine unlearning y su conexión con la privacidad diferencial.

- **Cao & Yang (2015) — [Towards Making Systems Forget with Machine Unlearning](2015_cao_machine-unlearning.html)**: trabajo fundacional que introduce el concepto formal de machine unlearning para clasificadores basados en suma de componentes; SISA generaliza esta idea a redes neuronales.
- **Ginart et al. (2019) — [Making AI Forget You: Data Deletion in Machine Learning](2019_ginart_data-deletion.html)**: extiende el unlearning exacto a k-means y datos continuos; SISA adopta su formalización de la condición de indistinguibilidad estadística.
- **Dwork et al. (2006) — Differential Privacy**: la privacidad diferencial es el marco teórico de fondo que motiva las garantías formales de SISA.
- **Carlini et al. (2019) — The Secret Sharer**: demuestra que los modelos memorizan datos de entrenamiento, motivando la necesidad de unlearning.

## Tags

`machine-unlearning` `SISA` `exact-unlearning` `privacidad` `reentrenamiento` `particionamiento`
