---
layout: paper
title: "A Survey on Unlearning in Large Language Models"
year: 2025
date_published: "2025-10-29"
authors: "Ruichen Qiu, Jiajun Tan, Jiayue Pu, Honglin Wang, Xiao-Shan Gao, Fei Sun"
published: "arXiv, 2025"
tags:
  - "machine-unlearning"
  - "survey"
  - "LLM"
  - "taxonomía"
  - "privacidad-seguridad"
pdf: "/llm_bias/pdfs/2025_qiu_survey-unlearning.pdf"
method_type: "Evaluación / análisis"
status:
  - "Pendiente"
image: "imgs/2025_qiu_survey-unlearning.png"
image_caption: "Ilustración de un robot que representa el LLM como sujeto del proceso de machine unlearning, tema central del survey que categoriza objetivos, métodos y evaluaciones del campo."
opinion: "<WIP>"
---
# A Survey on Unlearning in Large Language Models (2025)

**Autores**: Ruichen Qiu, Jiajun Tan, Jiayue Pu, Honglin Wang, Xiao-Shan Gao, Fei Sun
**Publicado en**: arXiv, 2025
**Tipo de método**: Evaluación / análisis

---

## Qué hace

Survey comprehensivo del campo de machine unlearning en LLMs que revisa más de 100 papers, categoriza objetivos, métodos y evaluaciones, e identifica los desafíos y direcciones abiertas del área.


---

## Metodología

Este es un paper de survey, no propone métodos nuevos. Su valor está en sistematizar el conocimiento existente.

**Objetivos del unlearning (qué olvidar):**
- **Privacidad**: eliminar datos personales identificables (PII), prevenir memorización y extracción.
- **Seguridad**: eliminar conocimiento peligroso (armas, ciberataques), reducir capacidad de asistencia maliciosa.
- **Copyright**: eliminar contenido protegido (libros, código propietario).
- **Sesgo y fairness**: eliminar asociaciones estereotipadas y sesgos sociales aprendidos.
- **Alucinaciones**: eliminar "conocimiento incorrecto" que el modelo aprendió con confianza.

**Taxonomía de métodos:**
1. *Exact unlearning*: garantías formales de que la información fue eliminada (sólo posible con modelos simples o con reentrenamiento parcial controlado).
2. *Approximate unlearning*: métodos heurísticos sin garantías formales:
   - Gradient-based (gradient ascent, gradient difference, NPO, DPO)
   - Model editing (ROME, MEMIT, task vectors)
   - In-context methods (prompting, few-shot unlearning)
   - Representation-based (activación steering, RMU)

**Evaluación:**
- Métricas de olvido: accuracy en forget set, membership inference attack success rate.
- Métricas de retención: accuracy en retain set, general benchmarks (MMLU).
- Métricas de robustez: resistencia a paráfrasis, few-shot, jailbreaks, reaprendizaje.

---

## Datasets utilizados

No propone datasets nuevos; revisa todos los benchmarks existentes: TOFU, WMDP, RWKU, MUSE, Harry Potter, y datasets de privacidad.

---

## Ejemplo ilustrativo

El survey usa la metáfora del "libro de texto mental": un LLM tiene internalizados millones de "libros" en sus parámetros. El unlearning quiere arrancar páginas específicas de este libro mental. El problema es que las páginas no están claramente delimitadas — la información está entretejida con millones de otras páginas. Arrancar una página puede dañar páginas adyacentes (degradar el modelo) o dejar fragmentos que permiten reconstruir la información.

---

## Resultados principales (hallazgos del survey)

- El campo creció exponencialmente: de ~5 papers en 2022 a más de 40 papers anuales en 2024-2025.
- El olvido exacto es prácticamente imposible en LLMs grandes sin reentrenamiento completo.
- Los métodos gradient-based son los más populares pero los menos robustos ante ataques.
- La evaluación está fragmentada: los papers usan métricas incompatibles, dificultando la comparación.
- Desafíos abiertos principales: verificación formal del olvido, unlearning multi-hop (olvido de conocimiento derivado), y unlearning continuo (olvidar nuevos datos regularmente).

---

## Ventajas respecto a trabajos anteriores

- Review más completo y actualizado del campo hasta 2025.
- Propone un vocabulario y taxonomía unificados que facilita la comunicación entre sub-áreas.
- Identifica los desafíos más urgentes y direcciones de investigación prometedoras.

---

## Trabajos previos relacionados

Al ser una survey, este artículo cubre y organiza trabajos previos en múltiples categorías: métodos de unlearning en tiempo de entrenamiento, post-entrenamiento (SFT, RL, edición de parámetros, métodos compuestos) y en tiempo de inferencia; benchmarks; y métricas de evaluación.

- **Cao & Yang (2015) — Towards making systems forget with machine unlearning**: trabajo fundacional sobre machine unlearning en ML clásico, punto de partida conceptual para el campo en LLMs; ver [2015_cao_machine-unlearning.md](2015_cao_machine-unlearning.html).
- **Jang et al. (2022) — Knowledge unlearning for LLMs**: uno de los primeros trabajos en unlearning de conocimiento específico en LLMs, base de muchos métodos de gradient ascent descritos en la survey; ver [2022_jang_knowledge-unlearning.md](2022_jang_knowledge-unlearning.html).
- **Maini et al. (2024) — TOFU: A task of fictitious unlearning**: introduce el benchmark TOFU de unlearning de bios ficticias, analizado como uno de los benchmarks de referencia de la survey; ver [2024_maini_tofu.md](2024_maini_tofu.html).
- **Li et al. (2024) — WMDP: Measuring and reducing malicious use**: benchmark de unlearning de conocimiento peligroso (bioseguridad, ciberseguridad), tratado como caso de uso de unlearning de seguridad; ver [2024_li_wmdp.md](2024_li_wmdp.html).
- **Eldan & Russinovich (2023) — Who's Harry Potter**: unlearning de entidades culturales completas, discutido como ejemplo paradigmático de unlearning de entidades abstractas; ver [2023_eldan_harry-potter.md](2023_eldan_harry-potter.html).
- **Yao et al. (2023) — Large language model unlearning**: introduce técnicas de gradient ascent y sustitución de respuestas, métodos SFT centrales en la taxonomía de la survey; ver [2023_yao_large-llm-unlearning.md](2023_yao_large-llm-unlearning.html).
- **Fan et al. (2024) — Simplicity prevails: Rethinking negative preference optimization**: SimNPO, método de preferencia negativa destacado como referente en la categoría de RL-based unlearning; ver [2024_fan_simplicity-npo.md](2024_fan_simplicity-npo.html).
- **Patil et al. (2023) — Can sensitive information be deleted from LLMs?**: estudia la dificultad de eliminar información sensible, motivando la evaluación de privacidad tratada en la survey; ver [2023_patil_sensitive-information.md](2023_patil_sensitive-information.html).
- **Pawelczyk et al. (2023) — In-context unlearning**: propone el unlearning en tiempo de inferencia mediante ejemplos en contexto, cubierto en la categoría de inference-time unlearning; ver [2023_pawelczyk_incontext-unlearning.md](2023_pawelczyk_incontext-unlearning.html).
- **Zhang et al. (2024) — Negative preference optimization**: método NPO para unlearning mediante optimización de preferencias negativas, incluido en la categoría de RL-based post-training unlearning de la survey; ver [2024_zhang_negative-preference-optimization.md](2024_zhang_negative-preference-optimization.html).

## Tags

`machine-unlearning` `survey` `LLM` `taxonomía` `privacidad-seguridad`
