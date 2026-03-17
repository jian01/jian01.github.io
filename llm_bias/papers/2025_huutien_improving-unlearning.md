---
layout: paper
title: "Improving LLM Unlearning Robustness via Random Perturbations"
year: 2025
date_published: "2025-01-31"
authors: "Dang Huu-Tien, Hoang Thanh-Tung, Le-Minh Nguyen, Naoya Inoue"
published: "2025"
tags:
  - "machine-unlearning"
  - "robustez"
  - "perturbaciones-aleatorias"
  - "ataques-adversariales"
  - "LLM"
pdf: "/llm_bias/pdfs/2025_huutien_improving-unlearning.pdf"
method_type: "Perturbación de representaciones"
status:
  - "Pendiente"
image: "imgs/2025_huutien_improving-unlearning.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---## Qué hace

Mejora la robustez del unlearning en LLMs añadiendo **perturbaciones aleatorias** a los pesos del modelo durante el proceso de unlearning, similar al entrenamiento adversarial. Previene el "olvido superficial" donde el modelo sólo aprende a no responder directamente pero retiene el conocimiento.


---

## Metodología

La motivación es que el unlearning estándar (gradient ascent, NPO) crea un mínimo local en el espacio de parámetros donde el modelo no responde correctamente al forget set, pero este mínimo es "puntiagudo" (sharp minimum): pequeñas perturbaciones de los pesos pueden llevarlo de vuelta a responder correctamente.

**La solución:** Inspirado en el entrenamiento adversarial y en SAM (Sharpness-Aware Minimization), se añade ruido gaussiano aleatorio a los pesos durante el proceso de unlearning. El objetivo es encontrar un mínimo "plano" en la superficie de pérdida, donde el modelo no responda correctamente al forget set y ese comportamiento sea estable ante perturbaciones.

El proceso en cada step de unlearning:
1. Añadir ruido aleatorio a los pesos actuales.
2. Computar el objetivo de unlearning con los pesos perturbados.
3. Actualizar los pesos originales (no los perturbados) usando ese gradiente.
4. Repetir.

Esto hace que el proceso de unlearning no sólo reduzca la probabilidad de las respuestas correctas en el punto actual, sino que también asegure que las regiones vecinas del espacio de parámetros tampoco las produzcan.

Se modifican **todos los pesos** del modelo, pero el efecto principal es en las capas de atención y FFN medias donde el conocimiento específico tiende a almacenarse.

---

## Datasets utilizados

- **TOFU**: autores ficticios.
- **WMDP**: conocimiento peligroso.
- **Harry Potter**: corpus literario.
- Tests de robustez: paráfrasis, few-shot, jailbreaks.

---

## Ejemplo ilustrativo

Imagina que el unlearning estándar enseña al modelo a responder "No sé" a una pregunta específica, pero el modelo "sabe" la respuesta internamente — simplemente aprendió a suprimirla. Si alguien reformula la pregunta levemente, el modelo puede responder. Las perturbaciones aleatorias son como practicar el olvido en condiciones ruidosas: el modelo no sólo aprende a no responder la pregunta exacta, sino que aprende a no responderla incluso cuando el contexto varía ligeramente.

---

## Resultados principales

- Mejora la robustez ante paráfrasis en un 15-25% comparado con NPO sin perturbaciones.
- Mejora ante ataques de few-shot en un 10-20%.
- La degradación en capacidades generales es comparable a los métodos base.
- Combinable con cualquier método de unlearning existente (es un "plugin" que se añade encima).

---

## Ventajas respecto a trabajos anteriores

- Aborda directamente la fragilidad del unlearning ante perturbaciones, que es el principal vector de ataque.
- La técnica de perturbaciones aleatorias es simple, modular y computacionalmente económica.
- Primer trabajo que conecta explícitamente la geometría del espacio de pérdida (sharpness) con la robustez del unlearning.

---

## Trabajos previos relacionados

El paper se enmarca en la literatura sobre robustez del unlearning: estudia cómo los mínimos "afilados" (sharp minima) en el espacio de pérdida del unlearning son fácilmente revertibles ante perturbaciones de los pesos, y conecta este problema con la literatura de Sharpness-Aware Minimization (SAM) y entrenamiento adversarial. Los trabajos previos clave se dividen entre métodos de unlearning que el paper mejora y trabajos sobre robustez ante ataques que el paper aborda.

- **Jang et al. (2022) — Knowledge Unlearning**: [Knowledge Unlearning](2022_jang_knowledge-unlearning.html): propone gradient ascent como método de LLM unlearning; el paper demuestra que GA produce mínimos afilados vulnerables ante perturbaciones de parámetros.
- **Zhang et al. (2024) — Negative Preference Optimization (NPO)**: [NPO](2024_zhang_negative-preference-optimization.html): método de unlearning más estable que GA pero también vulnerable a perturbaciones; el paper propone perturbaciones aleatorias como módulo aplicable encima de NPO.
- **Maini et al. (2024) — TOFU**: [TOFU](2024_maini_tofu.html): benchmark de autores ficticios utilizado para evaluar la robustez del unlearning ante paráfrasis y ataques few-shot.
- **Li et al. (2024) — WMDP**: [WMDP](2024_li_wmdp.html): benchmark de conocimiento peligroso usado para evaluar si el conocimiento recuperado tras perturbaciones representa un riesgo real de seguridad.
- **Eldan & Russinovich (2023) — Who's Harry Potter?**: [Who's Harry Potter?](2023_eldan_harry-potter.html): corpus literario utilizado como tercer escenario de evaluación de robustez del unlearning.
- **Lynch et al. (2024) — Eight Methods**: [Eight Methods](2024_lynch_eight-methods.html): propone métricas robustas incluyendo resistencia a jailbreaks y paráfrasis, evaluación adoptada para medir la mejora de robustez lograda por el método.
- **Doshi et al. (2024) — Does Unlearning Truly Unlearn?**: [Does Unlearning Truly Unlearn?](2024_doshi_does-unlearning.html): estudia si el unlearning realmente elimina conocimiento o sólo lo suprime, motivación directa para buscar mínimos planos más estables.
- **Zhang et al. (2024) — Catastrophic Quantization**: [Catastrophic Quantization](2024_zhang_catastrophic-quantization.html): otro trabajo que revela la fragilidad del unlearning ante perturbaciones del modelo (cuantización); el método de perturbaciones aleatorias es complementario a esa amenaza.
- **Yao et al. (2023) — Large Language Model Unlearning**: [Large Language Model Unlearning](2023_yao_large-llm-unlearning.html): método de unlearning sobre el que el paper también aplica y valida su técnica de perturbaciones como mejora modular.

## Tags

`machine-unlearning` `robustez` `perturbaciones-aleatorias` `ataques-adversariales` `LLM`
