---
layout: paper
title: "Debiasing the Fine-Grained Classification Task in LLMs with Bias-Aware PEFT"
year: 2025
authors: "Daiying Zhao, Xinyu Yang, Hang Chen"
published: "ACL, 2025"
tags:
  - "debiasing"
  - "PEFT"
  - "LoRA"
  - "clasificación-fina"
  - "fairness"
pdf: "/llm_bias/pdfs/2025_zhao_debiasing-peft.pdf"
method_type: "Adapters / PEFT"
datasets:
  - "CUB-200"
  - "Stanford Cars"
  - "Food-101"
measures_general_quality: "Sí"
status:
  - "Pendiente"
image: "imgs/2025_zhao_debiasing-peft.png"
image_caption: "Gráfico de barras que compara los logits finales del modelo para categorías emocionales de grano fino (a) y grueso (b), distinguiendo entre muestras que contienen (azul/naranja claro) y no contienen (azul oscuro/rojo) el atributo emocional, ilustrando el sesgo en la tarea de clasificación."
---
# Debiasing the Fine-Grained Classification Task in LLMs with Bias-Aware PEFT (2025)

**Autores**: Daiying Zhao, Xinyu Yang, Hang Chen
**Publicado en**: ACL, 2025
**Tipo de método**: Adapters / PEFT

---

## Qué hace

Propone Bias-Aware PEFT, un método de fine-tuning eficiente en parámetros que incorpora explícitamente la conciencia del sesgo durante el fine-tuning en tareas de clasificación fina, reduciendo el sesgo que emerge al especializar LLMs en categorías muy similares.


---

## Metodología

**El problema específico:** Las tareas de clasificación fina (fine-grained classification) — como identificar razas de perro, modelos de auto, o especies de plantas — tienen categorías muy similares entre sí. Los LLMs pueden desarrollar sesgos cuando se especializan en estas tareas: por ejemplo, al clasificar razas de perros, el modelo podría ser más preciso para razas más representadas en el corpus de entrenamiento (ej. razas occidentales) que para razas menos representadas.

**Bias-Aware PEFT:**
Se adapta LoRA con un término adicional de regularización que penaliza el sesgo en la distribución de predicciones. El método tiene dos componentes:

1. **Bias-aware LoRA matrices**: Las matrices de bajo rango de LoRA se inicializan usando la estructura de las clases menos representadas en los datos. Esto sesga la inicialización hacia ser más sensible a estas clases desde el inicio.

2. **Regularización de equidad**: Durante el fine-tuning, se añade un término de loss que penaliza si la distribución de predicciones es significativamente diferente entre grupos de clases "privilegiadas" (bien representadas) y "no privilegiadas" (subrepresentadas). Los gradientes de este término fluyen hacia las matrices LoRA, no hacia los pesos base.

Las capas modificadas son las matrices Q, K, V, O de atención mediante LoRA, con la regularización adicional de equidad.

---

## Datasets utilizados

- **CUB-200**: 200 especies de pájaros (clasificación fina). Se inyectan artificialmente sesgos seleccionando subconjuntos desequilibrados de las clases.
- **Stanford Cars**: 196 modelos de autos.
- **Food-101**: 101 categorías de comida.
- Evaluados en Llama-2 y CLIP fine-tuneados.

---

## Ejemplo ilustrativo

Se fine-tunea un LLM para clasificar 196 modelos de autos. El dataset de entrenamiento tiene 500 imágenes/textos de modelos americanos y europeos populares, pero sólo 10-20 de modelos asiáticos (Kia, Hyundai, BYD). Sin Bias-Aware PEFT, el modelo aprende a clasificar bien los modelos populares pero falla en los asiáticos subrepresentados. Con Bias-Aware PEFT, la regularización de equidad fuerza al modelo a distribuir su "atención" más equitativamente entre los grupos, mejorando la clasificación de los modelos subrepresentados.

---

## Resultados principales

- Mejora la accuracy de las clases subrepresentadas en 5-15% sin degradar las clases bien representadas.
- La métrica de equidad (diferencia de accuracy entre grupos privilegiados/no privilegiados) se reduce de ~20% a ~8%.
- Overhead computacional mínimo respecto a LoRA estándar.
- Funciona mejor cuando el desequilibrio de representación es severo (>10:1 ratio).

---

## Ventajas respecto a trabajos anteriores

- Aborda un tipo de sesgo (en clasificación fina) que benchmarks generales de sesgo no capturan.
- Integra la conciencia del sesgo directamente en la inicialización y el objetivo de PEFT.
- Más eficiente que métodos de re-balanceo de datos tradicionales.

---

## Trabajos previos relacionados

El artículo organiza los trabajos previos en tres categorías para el sesgo de etiqueta: métodos de reentrenamiento (basados en datos y en algoritmos), métodos PEFT, y enfoques post-hoc. También revisa trabajo sobre el rol de las capas intermedias en LLMs.

- **Gira et al. (2022) — Debiasing pre-trained language models via efficient fine-tuning**: propone un método PEFT para debiasing que es el antecedente más directo de este trabajo, al que la propuesta de capas intermedias ofrece una alternativa más eficiente; ver [2022_gira_debiasing-efficient-finetuning.md](2022_gira_debiasing-efficient-finetuning.html).
- **He et al. (2022) — MABEL: Attenuating gender bias using textual entailment data**: método de reentrenamiento con datos contrafácticos para debiasing, representativo del paradigma de reentrenamiento data-based al que el artículo compara su enfoque; ver [2022_he_mabel.md](2022_he_mabel.html).
- **Thakur et al. (2023) — Gender makeover**: data augmentation mediante cambio de género para debiasing, referente del enfoque data-based de reentrenamiento evaluado en comparativa; ver [2023_thakur_gender-makeover.md](2023_thakur_gender-makeover.html).
- **Hassan & Alikhani (2023) — DCALM**: método algorithm-based que modifica arquitectura o restricciones de entrenamiento para debiasing de tipo clasificación fina; ver [2023_hassan_dcalm.md](2023_hassan_dcalm.html).
- **Zhao et al. (2021) — Calibrate before use**: método de calibración post-hoc de predicciones del modelo para reducir sesgos de etiqueta, referente del paradigma post-hoc evaluado en el artículo; ver [2021_zhao_calibrate-before-use.md](2021_zhao_calibrate-before-use.html).
- **Yang et al. (2023) — Bias neurons in transformers**: poda de neuronas de sesgo, representante del paradigma de intervención en neuronas con el que el enfoque de capas intermedias contrasta; ver [2023_yang_bias-neurons.md](2023_yang_bias-neurons.html).
- **Meade et al. (2021) — An empirical survey of debiasing techniques**: encuesta de referencia que motiva la búsqueda de métodos PEFT más eficientes y generalizables para debiasing de clasificación fina; ver [2021_meade_debiasing-survey.md](2021_meade_debiasing-survey.html).

## Tags

`debiasing` `PEFT` `LoRA` `clasificación-fina` `fairness`
