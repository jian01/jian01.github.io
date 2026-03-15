---
layout: paper
title: "Towards LLM Unlearning Resilient to Relearning Attacks: A Sharpness-Aware Minimization Perspective and Beyond"
year: 2025
authors: "Chongyu Fan, Jinghan Jia, Yihua Zhang, Anil Ramakrishna, Mingyi Hong, Sijia Liu"
published: "arXiv, 2025"
tags:
  - "machine-unlearning"
  - "robustez"
  - "reaprendizaje"
  - "SAM"
  - "geometría-del-loss"
pdf: "/llm_bias/pdfs/2025_fan_unlearning-relearning.pdf"
method_type: "Gradient ascent"
status:
  - "Pendiente"
image: "imgs/2025_fan_unlearning-relearning.png"
image_caption: "Icono de advertencia que ilustra el riesgo central estudiado en el paper: el unlearning estándar produce un estado frágil del modelo que puede ser revertido con facilidad mediante ataques de reaprendizaje."
---
# Towards LLM Unlearning Resilient to Relearning Attacks: A Sharpness-Aware Minimization Perspective and Beyond (2025)

**Autores**: Chongyu Fan, Jinghan Jia, Yihua Zhang, Anil Ramakrishna, Mingyi Hong, Sijia Liu
**Publicado en**: arXiv, 2025
**Tipo de método**: Gradient ascent

---

## Qué hace

Propone hacer el unlearning resistente a ataques de reaprendizaje (donde un adversario fine-tunea el modelo para recuperar el conocimiento olvidado) usando **Sharpness-Aware Minimization (SAM)** para encontrar mínimos "planos" en la superficie de pérdida.


---

## Metodología

El paper parte del análisis de por qué el unlearning es fácil de revertir. La respuesta está en la **geometría del espacio de pérdida**:

- El unlearning estándar lleva los parámetros a un mínimo local "agudo" (sharp minimum) donde la pérdida sobre el forget set es alta.
- Un mínimo agudo es inestable: pocas actualizaciones de gradiente (el ataque de reaprendizaje) pueden escapar de él y volver a una región donde la pérdida sobre el forget set es baja.

**La solución SAM-Unlearning:** SAM es una técnica de optimización que busca explícitamente mínimos "planos" (flat minima) donde la función de pérdida es alta en un vecindario amplio alrededor del punto óptimo. Un mínimo plano es mucho más difícil de escapar con pocas actualizaciones de gradiente.

El proceso SAM-Unlearning:
1. En cada paso de unlearning, primero se hace una perturbación de los pesos en la dirección de mayor pérdida en el forget set (la "peor perturbación").
2. Se actualiza el modelo para maximizar la pérdida del forget set incluso en esta peor perturbación.

Esto obliga al unlearning a encontrar un mínimo plano donde el modelo falla en el forget set incluso bajo perturbaciones, haciendo que el reaprendizaje requiera muchos más pasos.

Los parámetros modificados son todos los del modelo, con énfasis en las capas donde la pérdida del forget set tiene mayor curvatura.

---

## Datasets utilizados

- **TOFU**: autores ficticios.
- **WMDP**: conocimiento peligroso.
- **Ataques de reaprendizaje**: se simula un adversario que hace fine-tuning con diferentes cantidades de datos del forget set (10, 50, 100, 500 ejemplos).

---

## Ejemplo ilustrativo

Unlearning estándar es como construir una pared de arena para contener el agua: funciona mientras nadie la toque, pero cualquier golpe la derrumba (pocas actualizaciones de gradiente). SAM-Unlearning construye la pared más ancha y estable — incluso si el adversario empuja, la pared no cede fácilmente. En términos de reaprendizaje: en lugar de 100 pasos para recuperar el conocimiento, el adversario necesita 1000-5000 pasos, haciendo el ataque mucho más costoso.

---

## Resultados principales

- SAM-Unlearning requiere 5-10x más pasos de reaprendizaje para el adversario respecto a NPO estándar.
- La robustez ante ataques con pocos ejemplos (10-50) mejora significativamente.
- El costo computacional adicional de SAM es ~30-40% más tiempo de entrenamiento.
- Combinable con cualquier objective de unlearning (NPO, gradient ascent, etc.) como un "wrapper".

---

## Ventajas respecto a trabajos anteriores

- Directamente motivado por el ataque de reaprendizaje (el trabajo de Łucki et al. 2024).
- Primera solución con fundamento en la geometría del espacio de pérdida para explicar por qué el unlearning es frágil y cómo hacerlo robusto.
- El framework SAM es bien estudiado en optimización, dando base teórica sólida.

---

## Trabajos previos relacionados

El paper organiza los antecedentes en tres líneas: machine unlearning en LLMs, adversarios y ataques contra el unlearning, y optimización de suavizado (SAM y técnicas afines).

- **Cao & Yang (2015) — Towards Making Systems Forget with Machine Unlearning**: [Towards Making Systems Forget with Machine Unlearning](2015_cao_machine-unlearning.html) introduce el concepto formal de machine unlearning, fundamento de todo el campo sobre el que este trabajo construye.
- **Yao et al. (2023) — Large Language Model Unlearning**: [Large Language Model Unlearning](2023_yao_large-llm-unlearning.html) es uno de los trabajos pioneros en aplicar unlearning a LLMs para suprimir contenido dañino, siendo uno de los métodos base contra los que se compara SAM-Unlearning.
- **Maini et al. (2024) — TOFU: A Task of Fictitious Unlearning**: [TOFU](2024_maini_tofu.html) proporciona el benchmark de evaluación de unlearning sobre autores ficticios utilizado como uno de los testbeds principales en este paper.
- **Li et al. (2024) — The WMDP Benchmark**: [WMDP](2024_li_wmdp.html) proporciona el benchmark de conocimiento peligroso empleado como segundo testbed principal, junto con el método RMU que es una línea base importante.
- **Zhang et al. (2024) — Negative Preference Optimization**: [NPO](2024_zhang_negative-preference-optimization.html) introduce NPO, el método de unlearning de estado del arte que sirve como punto de partida directo para integrar SAM y demostrar su vulnerabilidad a ataques de reaprendizaje.
- **Lynch et al. (2024) — Eight Methods to Evaluate Robust Unlearning**: [Eight Methods](2024_lynch_eight-methods.html) identifica y formaliza los ataques de reaprendizaje como vulnerabilidad crítica del unlearning, motivando directamente la propuesta de SAM-Unlearning.
- **Łucki et al. (2024) — Adversarial Unlearning**: [Adversarial Unlearning](2024_ucki_adversarial-unlearning.html) demuestra que el unlearning actual es fácil de revertir mediante jailbreaking y fine-tuning adversarial, siendo una referencia central para el problema abordado.
- **Eldan & Russinovich (2023) — Who's Harry Potter**: [Who's Harry Potter](2023_eldan_harry-potter.html) introduce un método influyente de unlearning para LLMs aplicado a borrar conocimiento literario, representando otra línea base del campo.
- **Patil et al. (2023) — Sensitive Information in LLM Unlearning**: [Patil et al.](2023_patil_sensitive-information.html) explora vulnerabilidades relacionadas con la recuperación de información sensible tras el unlearning, complementando la motivación de robustez.
- **Foret et al. (2021) — Sharpness-Aware Minimization (SAM)**: presenta SAM como técnica de optimización para mejorar la generalización buscando mínimos planos, siendo la piedra angular de la propuesta técnica de este paper.

## Tags

`machine-unlearning` `robustez` `reaprendizaje` `SAM` `geometría-del-loss`
