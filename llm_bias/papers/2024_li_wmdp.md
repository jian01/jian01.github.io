---
layout: paper
title: "The WMDP Benchmark: Measuring and Reducing Malicious Use With Unlearning"
year: 2024
authors: "Nathaniel Li, Alexander Pan, Anjali Gopal, Summer Yue, Daniel Berrios, Alice Gatti, et al."
published: "arXiv, 2024"
tags:
  - "machine-unlearning"
  - "seguridad-AI"
  - "conocimiento-peligroso"
  - "benchmark"
  - "representaciones-internas"
pdf: "/llm_bias/pdfs/2024_li_wmdp.pdf"
method_type: "Gradient ascent"
status:
  - "Pendiente"
image: "imgs/2024_li_wmdp.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---
# The WMDP Benchmark: Measuring and Reducing Malicious Use With Unlearning (2024)

**Autores**: Nathaniel Li, Alexander Pan, Anjali Gopal, Summer Yue, Daniel Berrios, Alice Gatti, et al.
**Publicado en**: arXiv, 2024
**Tipo de método**: Gradient ascent

---

## Qué hace

Introduce WMDP (**W**eapons of **M**ass **D**estruction **P**roxy), un benchmark para medir y reducir la capacidad de los LLMs de asistir en la creación de armas de destrucción masiva (biológicas, químicas, cibernéticas). Propone el método CUT (Circuit Breaker Unlearning Technique) para eliminar este conocimiento peligroso.


---

## Metodología

**El benchmark WMDP:** 3.668 preguntas de opción múltiple sobre conocimiento peligroso en tres dominios:
- **WMDP-bio**: síntesis de patógenos, mejora de virulencia, técnicas de bioterrorismo.
- **WMDP-chem**: síntesis de agentes químicos, precursores, métodos de dispersión.
- **WMDP-cyber**: vulnerabilidades en infraestructura crítica, técnicas de ataque avanzadas.

Las preguntas fueron creadas por expertos en bioseguridad y ciberseguridad, y son lo suficientemente técnicas como para ser peligrosas si un LLM las responde correctamente.

**El método RMU (Representation Misdirection for Unlearning):** El método propuesto no usa gradient ascent sino que trabaja directamente sobre las **representaciones internas** del modelo. La idea es:
1. Identificar en qué capas intermedias del transformer se activan las representaciones relacionadas con el conocimiento peligroso.
2. Añadir un término de loss que empuje esas representaciones hacia representaciones de textos seguros/aleatorios, sin alterar otras representaciones.

Esto modifica los pesos de las **capas intermedias de atención y FFN** que producen esas representaciones. A diferencia del gradient ascent, el objetivo no es que el modelo asigne baja probabilidad al texto peligroso, sino que sus representaciones internas para ese contexto se vuelvan indistinguibles de representaciones para texto neutro.

---

## Datasets utilizados

- **WMDP-bio, WMDP-chem, WMDP-cyber**: 3.668 preguntas de opción múltiple.
- **MMLU**: benchmark de conocimiento general para medir que el modelo no pierde capacidades en áreas no peligrosas (matemáticas, historia, ciencias básicas).
- **Retain corpus**: textos de Wikipedia sobre los mismos dominios pero sin información peligrosa (para preservar conocimiento legítimo de biología, química, etc.).

---

## Ejemplo ilustrativo

Una pregunta de WMDP-bio podría ser: *"¿Qué técnica de modificación genética permite aumentar la transmisibilidad de un virus influenza entre mamíferos?"* con opciones técnicas específicas. Un modelo sin unlearning (GPT-4, Llama-2) responde correctamente con alta probabilidad. Después de aplicar RMU, el modelo debería responder al azar (25% para 4 opciones) en estas preguntas, pero seguir respondiendo correctamente preguntas de biología general como "¿Qué es la mitosis?".

---

## Resultados principales

- RMU reduce la precisión en WMDP de ~60-70% (nivel experto) a ~25-30% (nivel aleatorio) en los tres dominios.
- La degradación en MMLU es mínima: menos del 2% de caída en rendimiento general.
- CUT supera a gradient ascent, gradient difference y otros métodos en el balance olvido/retención.
- Hallazgo importante: modelos más grandes son más difíciles de "desaprender" — tienen más redundancia interna para almacenar el conocimiento peligroso.

---

## Ventajas respecto a trabajos anteriores

- Primer benchmark enfocado en **seguridad de AI** (no privacidad) con preguntas validadas por expertos.
- RMU trabaja sobre representaciones internas en lugar de probabilidades de tokens, siendo más robusto a ataques de extracción directa.
- Demuestra que unlearning selectivo de conocimiento peligroso es posible sin destruir capacidades generales.

---

## Trabajos previos relacionados

El paper organiza los trabajos relacionados en tres bloques: evaluación de riesgos en LLMs, mitigación de riesgos mediante safety training y jailbreaks, y machine unlearning. Esta estructura refleja el doble objetivo del paper: medir (benchmark WMDP) y reducir (método RMU) capacidades peligrosas.

- **Cao & Yang (2015) — [Towards Making Systems Forget with Machine Unlearning](2015_cao_machine-unlearning.html)**: trabajo fundacional del machine unlearning, citado como punto de origen del campo; el paper extiende su alcance de datos individuales a dominios completos de conocimiento peligroso.
- **Jang et al. (2022) — [Knowledge Unlearning](2022_jang_knowledge-unlearning.html)**: propone gradient ascent para olvidar hechos específicos en LLMs, método base contra el que se compara RMU en el paper.
- **Eldan & Russinovich (2023) — [Who's Harry Potter?](2023_eldan_harry-potter.html)**: primer método que extiende el unlearning a conceptos amplios (un universo narrativo completo) en lugar de hechos individuales, antecedente directo del objetivo de unlearning de dominio de WMDP.
- **Maini et al. (2024) — [TOFU](2024_maini_tofu.html)**: benchmark de unlearning con autores ficticios, representante del estado del arte en benchmarks de unlearning antes de WMDP, que el paper critica por no abordar conocimiento peligroso real.
- **Pawelczyk et al. (2023) — [In-Context Unlearning](2023_pawelczyk_incontext-unlearning.html)**: método de unlearning sin modificar pesos que el paper menciona como alternativa en el espacio de soluciones.
- **Yao et al. (2023) — [Large Language Model Unlearning (LLMU)](2023_yao_large-llm-unlearning.html)**: propone múltiples objetivos de pérdida para unlearning de comportamientos dañinos en LLMs, trabajo de referencia que RMU supera en el contexto de conocimiento peligroso.
- **Ziegler et al. (2020) — [RLHF Fine-Tuning](2019_ziegler_rlhf-finetuning.html)**: representa el enfoque de safety training mediante RLHF, que el paper señala como vulnerable a jailbreaks y motivador del unlearning como complemento.
- **Gehman et al. (2020) — [RealToxicityPrompts](2020_gehman_realtoxicityprompts.html)**: benchmark de generación tóxica en LLMs, ejemplo de evaluación de riesgos de seguridad previo a WMDP que inspira el diseño del benchmark de conocimiento peligroso.

## Tags

`machine-unlearning` `seguridad-AI` `conocimiento-peligroso` `benchmark` `representaciones-internas`
