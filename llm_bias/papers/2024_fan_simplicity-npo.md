---
layout: paper
title: "Simplicity Prevails: Rethinking Negative Preference Optimization for LLM Unlearning"
year: 2024
date_published: "2024-10-09"
authors: "Chongyu Fan, Liu Jian-cheng, Licong Lin, Jinghan Jia, Ruiqi Zhang, Mei Song, Sijia Liu"
published: "arXiv, 2024"
tags:
  - "machine-unlearning"
  - "DPO"
  - "NPO"
  - "eficiencia"
  - "LLM"
pdf: "/llm_bias/pdfs/2024_fan_simplicity-npo.pdf"
method_type: "Optimización de preferencias"
status:
  - "Leido"
  - "Irrelevante"
image: "imgs/2024_fan_simplicity-npo.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---
# Simplicity Prevails: Rethinking Negative Preference Optimization for LLM Unlearning (2024)

**Autores**: Chongyu Fan, Liu Jian-cheng, Licong Lin, Jinghan Jia, Ruiqi Zhang, Mei Song, Sijia Liu
**Publicado en**: arXiv, 2024
**Tipo de método**: Optimización de preferencias

---

## Qué hace

Propone una versión simplificada de NPO (Negative Preference Optimization) que logra resultados equivalentes o superiores con menos complejidad computacional. Argumenta que métodos simples bien calibrados superan a métodos complejos en el contexto de unlearning.


---

## Metodología

NPO original requiere un modelo de referencia (el modelo original sin unlearning) para calcular el término de regularización durante cada actualización. Esto duplica el costo computacional: hay que hacer forward pass tanto del modelo en entrenamiento como del modelo de referencia en cada step.

**La simplificación propuesta (SimNPO):** En lugar de usar el modelo de referencia en tiempo real, se pre-computan las probabilidades del modelo de referencia sobre el forget set una sola vez y se guardan como una constante. Durante el entrenamiento, se usa esta constante pre-computada en lugar de recomputarla.

Adicionalmente, el paper analiza que la longitud de las secuencias afecta el balance entre olvido y retención: secuencias más largas tienen pérdidas más grandes simplemente por ser largas, no porque sean más importantes de olvidar. Propone normalizar el objetivo por la longitud de secuencia para que el método no sesgue hacia olvidar secuencias largas.

Todas las capas del transformer se modifican mediante fine-tuning estándar con el objetivo simplificado.

---

## Datasets utilizados

- **TOFU**: benchmark principal.
- **WMDP**: conocimiento peligroso.
- **Harry Potter/MUSE**: corpus literario.
- Evaluación: MMLU, TruthfulQA para retención general.

---

## Ejemplo ilustrativo

Imagina que NPO es como limpiar una habitación consultando constantemente a un asesor de limpieza (modelo de referencia) para cada objeto que tocás: "¿Puedo mover esto? ¿Es importante?" SimNPO haría la consulta una sola vez antes de empezar ("decime todos los objetos importantes"), guardaría la lista, y luego limpiaría sin necesidad de consultar en cada paso. El resultado es igual de bueno pero mucho más rápido.

---

## Resultados principales

- SimNPO logra resultados comparables a NPO en TOFU y WMDP con un costo computacional ~40-50% menor.
- La normalización por longitud mejora consistentemente el balance forget/retain.
- En algunos benchmarks, SimNPO supera a NPO, posiblemente porque la simplificación reduce el sobreajuste a las particularidades del forget set.
- El paper valida experimentalmente que "más simple es igual de bueno" en el contexto de unlearning.

---

## Ventajas respecto a trabajos anteriores

- Reduce el overhead computacional de NPO sin sacrificar calidad.
- La normalización por longitud es una corrección técnica importante que NPO original ignoraba.
- Demuestra empíricamente que la complejidad adicional de NPO no se justifica.

---

## Trabajos previos relacionados

El paper organiza los trabajos relacionados en tres grupos: (1) machine unlearning general (exacto vs. aproximado), (2) LLM unlearning específico con sus variantes de loss y aplicaciones, y (3) optimización de preferencias offline que inspira la simplificación propuesta. Destaca que SimPO (reference-free y length-normalized) es el método de preferencias del que adapta la mejora sobre NPO.

- **Jang et al. (2022) — Knowledge Unlearning**: [Knowledge Unlearning](2022_jang_knowledge-unlearning.html): introduce gradient ascent (GA) como método base de LLM unlearning; SimNPO busca superar sus limitaciones de estabilidad al igual que NPO.
- **Zhang et al. (2024) — Negative Preference Optimization (NPO)**: [NPO](2024_zhang_negative-preference-optimization.html): el método que SimNPO simplifica y mejora, eliminando el sesgo del modelo de referencia y normalizando por longitud de secuencia.
- **Maini et al. (2024) — TOFU**: [TOFU](2024_maini_tofu.html): benchmark principal de autores ficticios adoptado para evaluar SimNPO, uno de los benchmarks donde demuestra rendimiento superior a NPO.
- **Li et al. (2024) — WMDP**: [WMDP](2024_li_wmdp.html): benchmark de conocimiento peligroso utilizado como segunda evaluación de SimNPO junto a TOFU.
- **Eldan & Russinovich (2023) — Who's Harry Potter?**: [Who's Harry Potter?](2023_eldan_harry-potter.html): corpus literario / MUSE utilizado como tercer escenario de evaluación del método.
- **Rafailov et al. (2024) — DPO**: [DPO](2023_ermon_dpo.html): el framework de optimización de preferencias del que tanto NPO como SimNPO derivan su formulación matemática.
- **Pawelczyk et al. (2023) — In-Context Unlearning**: [In-Context Unlearning](2023_pawelczyk_incontext-unlearning.html): método alternativo basado en prompt engineering sin modificar pesos, mencionado como método de tipo distinto al de SimNPO.
- **Yao et al. (2024) — MUSE**: introduce el benchmark MUSE para eliminación de información privada/protegida, usado para evaluar SimNPO en eliminación de material con derechos de autor.
- **Lynch et al. (2024) — Eight Methods**: [Eight Methods](2024_lynch_eight-methods.html): propone métricas robustas contra jailbreaks para evaluar unlearning, relevantes para la evaluación completa del paper.
- **Cao & Yang (2015) — Machine Unlearning**: [Machine Unlearning](2015_cao_machine-unlearning.html): trabajo fundacional del área que establece el estándar de "retrain from scratch" como gold standard frente al que se miden todos los métodos aproximados.

## Tags

`machine-unlearning` `DPO` `NPO` `eficiencia` `LLM`
