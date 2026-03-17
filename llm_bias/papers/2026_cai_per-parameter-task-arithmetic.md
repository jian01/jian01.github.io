---
layout: paper
title: "Per-parameter Task Arithmetic for Unlearning in Large Language Models"
year: 2026
date_published: "2026-01-29"
authors: "Chengyi Cai, Zesheng Ye, Jiangchao Yao, Jianzhong Qi, Bo Han, Xiaolu Zhang, Feng Liu, Jun Zhou"
published: "arXiv, 2026"
tags:
  - "machine-unlearning"
  - "task-arithmetic"
  - "edición-de-modelos"
  - "LLM"
  - "per-parámetro"
pdf: "/llm_bias/pdfs/2026_cai_per-parameter-task-arithmetic.pdf"
method_type: "Enmascarado / edición de pesos"
status:
  - "Pendiente"
image: "imgs/2026_cai_per-parameter-task-arithmetic.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---## Qué hace

Propone un método de unlearning basado en **aritmética de task vectors** con escala por parámetro, donde se calcula un "vector de olvido" y se resta del modelo original con pesos adaptativos por parámetro, logrando mayor precisión que la resta uniforme.


---

## Metodología

**Task Arithmetic:** Es una técnica que permite "editar" modelos combinando vectores de pesos. Un "task vector" es la diferencia entre los pesos de un modelo fine-tuneado en una tarea y los pesos del modelo base. Sumar/restar task vectors permite añadir o quitar habilidades.

**Unlearning con Task Arithmetic (base):**
1. Fine-tunear el modelo sobre el forget set para crear un "forget model".
2. Computar el forget task vector = pesos del forget model - pesos del modelo original.
3. Restar el forget task vector del modelo original: modelo unlearned = pesos originales - α × forget vector.

El hiperparámetro α controla cuánto se olvida. El problema con este enfoque simple es que α es uniforme para todos los parámetros, lo que es subóptimo: algunos parámetros están fuertemente asociados al forget set mientras que otros apenas lo están.

**Per-Parameter Task Arithmetic (la contribución):**
Se calcula un α diferente por parámetro basado en qué tan relevante es ese parámetro para el forget set. La relevancia se estima con gradientes: parámetros con grandes gradientes sobre el forget set reciben un α mayor (se restan más fuertemente). Parámetros con gradientes pequeños reciben α cercano a 0 (casi no se modifican).

Esto permite un olvido más quirúrgico que afecta principalmente los parámetros más relacionados con el conocimiento a olvidar.

---

## Datasets utilizados

- **TOFU**: autores ficticios.
- **WMDP**: conocimiento peligroso.
- Evaluación general: MMLU, TruthfulQA.

---

## Ejemplo ilustrativo

Task arithmetic uniforme es como restar un ingrediente de una receta en la misma proporción en todos los pasos: si quieres "desaprender" el uso de sal, reducís sal en todos los pasos por igual, pero algunos pasos (ej. hornear el bizcocho) usan muy poca sal y no necesitan cambio. Per-parameter task arithmetic identifica exactamente qué pasos usan más sal y los reduce más agresivamente, mientras deja casi sin cambio los pasos donde la sal era irrelevante.

---

## Resultados principales

- Mejor balance forget/retain que task arithmetic uniforme en TOFU y WMDP.
- Menor degradación en MMLU (~1-2% vs ~3-5% para task arithmetic estándar).
- Más eficiente que fine-tuning: no requiere gradientes durante la inferencia, sólo una resta de vectores.
- El costo adicional de calcular α por parámetro es mínimo (requiere un forward-backward pass único sobre el forget set).

---

## Ventajas respecto a trabajos anteriores

- Mejora la precisión del unlearning por task arithmetic sin aumentar significativamente el costo.
- La asignación diferencial de α es una mejora natural y bien motivada.
- Más eficiente en inference que métodos de fine-tuning: la modificación se aplica una sola vez a los pesos.

---

## Trabajos previos relacionados

El paper se apoya en dos líneas de trabajo: métodos de unlearning basados en entrenamiento y métodos de model merging/task arithmetic, proponiendo una mejora al segundo paradigma para unlearning.

- **Maini et al. (2024) — TOFU: A Task of Fictitious Unlearning**: [TOFU](2024_maini_tofu.html) es el benchmark principal de evaluación usado en los experimentos, además de ser fuente del método GD (Gradient Difference) que es una de las líneas base de comparación.
- **Cao & Yang (2015) — Towards Making Systems Forget with Machine Unlearning**: [Cao & Yang (2015)](2015_cao_machine-unlearning.html) es la referencia fundacional del machine unlearning como campo, citada para contextualizar la motivación del trabajo.
- **Yao et al. (2023) — Large Language Model Unlearning (GA)**: [Yao et al. (2023)](2023_yao_large-llm-unlearning.html) introduce Gradient Ascent (GA) como método pionero de unlearning en LLMs minimizando la log-likelihood de los ejemplos a olvidar; es una de las líneas base directas del paper.
- **Zhang et al. (2024) — Negative Preference Optimization (NPO)**: [NPO](2024_zhang_negative-preference-optimization.html) construye la función de pérdida de unlearning separando el componente no preferido de DPO; es otro baseline de comparación central.
- **Fan et al. (2024) — Simplicity NPO (SimNPO)**: [SimNPO](2024_fan_simplicity-npo.html) elimina la dependencia del modelo de referencia en NPO; es una de las líneas base training-based evaluadas.
- **Jin et al. (2024) — RWKU: Benchmarking Real-World Knowledge Unlearning**: [RWKU](2024_jin_rwku.html) proporciona un marco de evaluación complementario para unlearning en escenarios reales.
- **Ilharco et al. (2022) — Editing Models with Task Arithmetic**: introduce el concepto de task vector como diferencia de pesos entre un modelo fine-tuneado y el original, siendo la base técnica directa sobre la que PerTA construye su mejora.
- **Liu et al. (2024) — Rethinking Machine Unlearning for LLMs**: [Rethinking Unlearning](2024_liu_rethinking-unlearning.html) analiza limitaciones de los métodos actuales de unlearning, proveyendo contexto evaluativo relevante.
- **Dorna et al. (2025) — OpenUnlearning**: [OpenUnlearning](2025_dorna_openunlearning.html) ofrece un marco unificado de comparación de métodos de unlearning que da soporte al benchmarking empleado.
- **AdaMerging (Yu et al., 2023)**: extiende task arithmetic aprendiendo coeficientes capa por capa para multi-task learning, trabajo directamente relacionado con el enfoque de pesos adaptativos de PerTA aunque en un contexto diferente (fusión en vez de olvido).

## Tags

`machine-unlearning` `task-arithmetic` `edición-de-modelos` `LLM` `per-parámetro`
