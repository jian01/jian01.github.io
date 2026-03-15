---
layout: paper
title: "Sustainable Modular Debiasing of Language Models"
year: 2021
authors: "Anne Lauscher, Tobias Lüken, Goran Glavaš"
published: "Findings of EMNLP, 2021"
tags:
  - "debiasing"
  - "adapters"
  - "modular"
  - "BERT"
  - "sesgo-de-género"
pdf: "/llm_bias/pdfs/2021_lauscher_modular-debiasing.pdf"
method_type: "Adapters / PEFT"
datasets:
  - "WinoBias"
  - "StereoSet"
  - "CrowS-Pairs"
  - "WNC (Wikipedia Neutrality Corpus)"
  - "GLUE benchmark"
measures_general_quality: "Sí"
status:
  - "Pendiente"
image: "imgs/2021_lauscher_modular-debiasing.png"
image_caption: "Un adaptador de debiasing (pequeños módulos de cuello de botella) se inserta en cada capa de BERT. Solo se entrenan los parámetros del adaptador; los pesos de BERT se congelan."
opinion: "<WIP>"
---
# Sustainable Modular Debiasing of Language Models (2021)

**Autores**: Anne Lauscher, Tobias Lüken, Goran Glavaš
**Publicado en**: Findings of EMNLP, 2021
**Tipo de método**: Adapters / PEFT

---

## Qué hace

Propone un framework de **debiasing modular y sostenible** para modelos de lenguaje basado en **adaptadores** (*adapters*). La idea central es que en lugar de modificar los pesos del modelo base, se entrena un pequeño módulo adaptador independiente (*debiasing adapter*) que puede enchufarse y desenchufarse del modelo sin alterar sus parámetros originales. Esto hace el debiasing "sostenible": un mismo adaptador puede reutilizarse en múltiples modelos o tareas, y puede actualizarse cuando cambian las nociones sociales de sesgo sin reentrenar el modelo completo.

El paper es también uno de los primeros en estudiar si el debiasing de un tipo de sesgo (género) transfiere a otros (raza, religión) y si los adaptadores preservan mejor las capacidades downstream que el fine-tuning completo.


---

## Metodología

Los adaptadores son módulos de cuello de botella (*bottleneck adapter*) insertados dentro de cada capa del transformer. Cada adaptador tiene dos capas lineales: una de proyección hacia abajo (de dimensión d a d/r, donde r es el factor de reducción) y una de proyección hacia arriba (de d/r a d), con una conexión residual. Los parámetros del adaptador son típicamente <1% de los parámetros del modelo base.

**Proceso de entrenamiento del adaptador de debiasing**:
1. Se congela BERT completamente.
2. Se insertan los adaptadores en todas las capas transformer.
3. Se entrena solo los adaptadores con el objetivo de debiasing: contrastive debiasing loss sobre pares de oraciones género-swapped, igual al objetivo de CDA (Counterfactual Data Augmentation).
4. El adaptador entrenado puede entonces "enchufarse" en cualquier instancia de BERT para debiasearla, o "desenchufarse" para recuperar el modelo original.

El paper también propone **adapter stacking** para debiasing multi-dimensión: se apilan adaptadores de género, raza y religión, cada uno entrenado independientemente, para mitigar múltiples sesgos simultáneamente.

---

## Datasets utilizados

- **WinoBias**: Para evaluar sesgo de género en co-referencia.
- **StereoSet**: Para evaluar sesgo estereotipado en múltiples dimensiones.
- **CrowS-Pairs**: Para evaluación de sesgo social.
- **WNC (Wikipedia Neutrality Corpus)**: Pares de oraciones biased/debiased para entrenamiento del adaptador.
- **GLUE benchmark**: Para medir la preservación de capacidades downstream.

---

## Ejemplo ilustrativo

Se tiene BERT-base y se quiere debiasear para género sin modificar el modelo base (porque está siendo usado en producción para múltiples tareas). Se entrena un adaptador de debiasing de género con 50K pares de oraciones contrastivas (10 minutos de entrenamiento). En producción, para aplicaciones sensibles al género se activa el adaptador; para otras tareas se desactiva. Si en el futuro las métricas de sesgo evolucionan, solo se actualiza el adaptador, no el modelo base.

Sin adaptador: BERT asigna mayor probabilidad a *"The nurse is she"* que *"The nurse is he"* con diferencia grande. Con adaptador activo: la diferencia de probabilidad se reduce significativamente, y el accuracy en GLUE solo cae 0.3 puntos.

---

## Resultados principales

- El adaptador de debiasing reduce el sesgo de género en WinoBias en un 20-30% relativo.
- La degradación en tareas downstream (GLUE) es **menor que la del fine-tuning completo** para debiasing, confirmando el beneficio de la modularidad.
- El adapter stacking para debiasing multi-dimensión funciona sin interferencia entre adaptadores de diferentes tipos de sesgo.
- Los adaptadores de género muestran transferencia parcial a sesgo de raza y religión, aunque menor que el debiasing directo en esas dimensiones.

---

## Ventajas respecto a trabajos anteriores

- A diferencia del fine-tuning completo para debiasing (Gira et al., MABEL), los adaptadores **no modifican el modelo base**, haciendo el debiasing reversible y modular.
- La modularidad permite desplegar el mismo adaptador sobre múltiples versiones del modelo o combinarlo con otros adaptadores (tarea específica + debiasing).
- "Sostenible" en el sentido de que cuando las nociones sociales de sesgo evolucionan, solo se actualiza el adaptador: el costo de actualización es proporcional al tamaño del adaptador (<1% de BERT), no del modelo.
- Precursor directo de los métodos de debiasing basados en LoRA y PEFT que dominan el campo en 2023-2025.

---

## Trabajos previos relacionados

- **Houlsby et al. (2019) — Parameter-Efficient Transfer Learning with Adapters**: introduce los adaptadores para transfer learning eficiente; Lauscher et al. aplican esta arquitectura al debiasing.
- **Ravfogel et al. (2020) — INLP**: baseline de debiasing por proyección lineal iterativa con el que se comparan los adaptadores.
- **Meade et al. (2021) — [An Empirical Survey of Debiasing Techniques](2021_meade_debiasing-survey.html)**: evaluación comparativa de métodos; los adaptadores de Lauscher et al. son uno de los métodos evaluados.
- **Xie et al. (2023) — [Parameter-Efficient Debiasing](2023_xie_parameter-efficient-debiasing.html)**: extiende directamente el trabajo de Lauscher et al. usando LoRA en lugar de adaptadores clásicos.
- **Yang et al. (2023) — [Bias Neurons Elimination](2023_yang_bias-neurons.html)**: identifica las neuronas de sesgo en BERT usando una metodología complementaria a la de los adaptadores.

## Tags

`debiasing` `adapters` `modular` `BERT` `sesgo-de-género` `parameter-efficient` `sostenible`
