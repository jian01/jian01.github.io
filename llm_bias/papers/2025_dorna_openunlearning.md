---
layout: paper
title: "OpenUnlearning: Accelerating LLM Unlearning via Unified Benchmarking of Methods and Metrics"
year: 2025
authors: "Vineeth Dorna, Anmol Reddy Mekala, Wenlong Zhao, Andrew McCallum, Zachary Chase Lipton, J. Zico Kolter, Pratyush Maini"
published: "arXiv, 2025"
tags:
  - "machine-unlearning"
  - "benchmark"
  - "framework"
  - "comparación-métodos"
  - "reproducibilidad"
pdf: "/llm_bias/pdfs/2025_dorna_openunlearning.pdf"
method_type: "Evaluación / análisis"
status:
  - "Pendiente"
image: "imgs/2025_dorna_openunlearning.png"
image_caption: "Icono de balanza de la justicia que ilustra el principio central de OpenUnlearning: proporcionar una comparación equitativa y balanceada entre múltiples métodos de unlearning bajo condiciones estandarizadas."
---
# OpenUnlearning: Accelerating LLM Unlearning via Unified Benchmarking of Methods and Metrics (2025)

**Autores**: Vineeth Dorna, Anmol Reddy Mekala, Wenlong Zhao, Andrew McCallum, Zachary Chase Lipton, J. Zico Kolter, Pratyush Maini
**Publicado en**: arXiv, 2025
**Tipo de método**: Evaluación / análisis

---

## Qué hace

Presenta OpenUnlearning, un framework de código abierto que implementa más de 8 algoritmos de unlearning sobre más de 5 benchmarks distintos, permitiendo comparaciones sistemáticas y reproducibles. Revela que los métodos de unlearning no generalizan entre benchmarks.


---

## Metodología

El problema que motiva este trabajo es la **fragmentación** del campo: cada paper propone un método nuevo y lo evalúa en un benchmark diferente, haciendo imposible saber cuál método es realmente mejor. OpenUnlearning resuelve esto con:

**Implementación unificada:** Todos los métodos comparten la misma infraestructura de entrenamiento, evaluación e hiperparámetros base. Los métodos implementados incluyen:
- Gradient Ascent (GA)
- Gradient Difference (GD)
- KL Divergence Preservation (KL)
- Negative Preference Optimization (NPO)
- Direct Preference Optimization para unlearning (DPO)
- Task Vector Arithmetic
- Representation Misdirection for Unlearning (RMU)
- Selective Synaptic Dampening (SSD)

**Benchmarks integrados:** TOFU, WMDP, Harry Potter (MUSE), RWKU, y otros.

**Métricas estandarizadas:** Forget Quality, Retain Accuracy, Model Utility, y tests de robustez adversarial.

Los parámetros del modelo que modifica cada algoritmo varían: algunos modifican todos los pesos, otros sólo ciertos bloques del transformer, pero todos se evalúan bajo condiciones controladas idénticas.

---

## Datasets utilizados

- **TOFU**: autores ficticios.
- **WMDP**: conocimiento peligroso.
- **MUSE**: unlearning de libros (Harry Potter y News corpora).
- **RWKU**: entidades reales de Wikipedia.
- **Evaluación general**: MMLU, TruthfulQA.

---

## Ejemplo ilustrativo

Antes de OpenUnlearning, comparar los métodos era como comparar atletas que corrieron en pistas diferentes con distintas condiciones climáticas. El paper A decía "mi método logra 85% de forget quality" en TOFU, el paper B decía "mi método logra 90%" en WMDP. ¿Cuál es mejor? No se podía saber. OpenUnlearning es como construir un estadio olímpico estándar: todos los atletas corren en la misma pista bajo las mismas condiciones, haciendo la comparación justa.

---

## Resultados principales

- Los métodos **no generalizan**: un método que gana en TOFU puede ser de los peores en WMDP. Esto es la principal revelación del paper.
- NPO y RMU son consistentemente los más robustos, pero con trade-offs distintos: NPO preserva mejor el modelo, RMU es más efectivo en el olvido.
- El framework reduce el tiempo de implementación de nuevos métodos de semanas a horas.
- Revela que varios papers de unlearning reportaron resultados favorables porque eligieron benchmarks en los que su método tenía ventajas artificiales.

---

## Ventajas respecto a trabajos anteriores

- Elimina el sesgo de selección en la evaluación: todos los métodos se comparan en las mismas condiciones.
- Open-source: facilita la reproducibilidad y el avance del campo.
- Establece que la generalización entre benchmarks es una métrica importante para evaluar métodos de unlearning.

---

## Trabajos previos relacionados

OpenUnlearning se sitúa en la intersección de tres líneas de trabajo previo: métodos de unlearning para LLMs, benchmarks de evaluación del olvido, y métricas de evaluación de memorización y privacidad.

- **Maini et al. (2024) — TOFU: A task of fictitious unlearning for LLMs**: introduce el benchmark TOFU de unlearning de bios ficticias, uno de los tres benchmarks centrales integrados en OpenUnlearning; ver [2024_maini_tofu.md](2024_maini_tofu.html).
- **Li et al. (2024) — WMDP: Measuring and reducing malicious use with unlearning**: propone el benchmark WMDP para unlearning de conocimiento peligroso, integrado como benchmark de seguridad en el framework; ver [2024_li_wmdp.md](2024_li_wmdp.html).
- **Zhang et al. (2024) — Negative preference optimization**: método de optimización de preferencias negativas para unlearning, uno de los algoritmos comparados en el benchmark; ver [2024_zhang_negative-preference-optimization.md](2024_zhang_negative-preference-optimization.html).
- **Fan et al. (2024) — Simplicity prevails: NPO for machine unlearning**: SimNPO, que emerge como el método más robusto en la comparativa exhaustiva de OpenUnlearning; ver [2024_fan_simplicity-npo.md](2024_fan_simplicity-npo.html).
- **Jang et al. (2022) — Knowledge unlearning for LLMs**: trabajo pionero sobre unlearning de conocimiento en LLMs que establece muchas de las métricas de memorización utilizadas en el framework; ver [2022_jang_knowledge-unlearning.md](2022_jang_knowledge-unlearning.html).
- **Eldan & Russinovich (2023) — Who's Harry Potter**: método de unlearning de entidades completas (Who's Harry Potter) integrado como caso de uso en el benchmark; ver [2023_eldan_harry-potter.md](2023_eldan_harry-potter.html).
- **Doshi et al. (2024) — Does unlearning truly unlearn?**: investiga si el unlearning es superficial o profundo, motivando directamente la meta-evaluación de métricas en OpenUnlearning; ver [2024_doshi_does-unlearning.md](2024_doshi_does-unlearning.html).
- **Liu et al. (2024) — Rethinking machine unlearning for LLMs**: cuestiona los enfoques actuales de unlearning y propone nuevos criterios de evaluación recogidos en el framework; ver [2024_liu_rethinking-unlearning.md](2024_liu_rethinking-unlearning.html).
- **Yao et al. (2023) — Large language model unlearning**: introduce métodos de gradient ascent para unlearning, base de varios algoritmos incluidos en OpenUnlearning; ver [2023_yao_large-llm-unlearning.md](2023_yao_large-llm-unlearning.html).
- **Jin et al. (2024) — RWKU: Benchmarking real-world knowledge unlearning**: benchmark de unlearning de conocimiento del mundo real integrado en OpenUnlearning para evaluar generalización; ver [2024_jin_rwku.md](2024_jin_rwku.html).

## Tags

`machine-unlearning` `benchmark` `framework` `comparación-métodos` `reproducibilidad`
