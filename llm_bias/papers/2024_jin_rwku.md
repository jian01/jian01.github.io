---
layout: paper
title: "RWKU: Benchmarking Real-World Knowledge Unlearning for Large Language Models"
year: 2024
date_published: "2024-06-16"
authors: "Zhuoran Jin, Pengfei Cao, Chenhao Wang, Zhitao He, Hongbang Yuan, Jiachun Li, Yubo Chen, Kang Liu, Jun Zhao"
published: "arXiv, 2024"
tags:
  - "machine-unlearning"
  - "benchmark"
  - "robustez-adversarial"
  - "conocimiento-real"
  - "LLM"
pdf: "/llm_bias/pdfs/2024_jin_rwku.pdf"
method_type: "Evaluación / análisis"
status:
  - "Pendiente"
image: "imgs/2024_jin_rwku.png"
image_caption: "Imagen representativa del benchmark RWKU, mostrando una llama (alusión a LLaMA) con una goma de borrar sobre la cabeza, simbolizando el proceso de desaprendizaje de conocimiento en modelos de lenguaje."
opinion: "<WIP>"
---
# RWKU: Benchmarking Real-World Knowledge Unlearning for Large Language Models (2024)

**Autores**: Zhuoran Jin, Pengfei Cao, Chenhao Wang, Zhitao He, Hongbang Yuan, Jiachun Li, Yubo Chen, Kang Liu, Jun Zhao
**Publicado en**: arXiv, 2024
**Tipo de método**: Evaluación / análisis

---

## Qué hace

Propone RWKU (**R**eal-**W**orld **K**nowledge **U**nlearning), un benchmark que evalúa el desaprendizaje de 200 entidades reales del mundo (personas públicas, empresas, eventos históricos) en LLMs, con énfasis en la robustez frente a ataques adversariales.


---

## Metodología

A diferencia de TOFU (que usa autores ficticios), RWKU trabaja con **conocimiento real** que los modelos efectivamente aprendieron durante el preentrenamiento. Esto hace la evaluación más realista pero también más difícil de controlar.

El benchmark evalúa dos aspectos principales:

**1. Olvido efectivo:** Para cada entidad del forget set (ej. una figura pública), se generan preguntas factuales sobre ella. Se mide si el modelo puede responderlas correctamente antes y después del unlearning. También se usa membership inference attack (MIA) para detectar si el modelo sigue "reconociendo" los textos relacionados como parte de su distribución de entrenamiento.

**2. Robustez adversarial:** Este es el aspecto más novedoso. Se generan varios tipos de ataques para intentar recuperar el conocimiento supuestamente olvidado:
- **Paráfrasis**: reformular la pregunta de forma diferente.
- **Completación**: pedir al modelo que complete un texto que induce la respuesta.
- **Few-shot**: proveer ejemplos en el contexto para "empujar" al modelo hacia la respuesta olvidada.
- **Extracción de prefijos**: usar el inicio de un texto del corpus para que el modelo lo continúe.

Los métodos de unlearning evaluados incluyen gradient ascent, gradient difference, y métodos basados en task vectors.

---

## Datasets utilizados

- **200 entidades reales de Wikipedia**: políticos, actores, empresas, eventos científicos. Se generan ~10 preguntas factuales por entidad.
- **Prompts adversariales**: generados automáticamente con GPT-4 para cada entidad.
- **Retain set**: conocimiento general del modelo medido en MMLU, TruthfulQA.

---

## Ejemplo ilustrativo

Supongamos que se desea "olvidar" al físico Niels Bohr. El forget set incluye preguntas como "¿Cuándo nació Niels Bohr?" o "¿Qué contribuciones hizo al modelo atómico?". Después del unlearning, el modelo debería fallar en responder estas preguntas. Pero el benchmark también prueba si el modelo puede ser "reactivado" mediante prompts como: *"El científico danés conocido por el principio de complementariedad nació en..."* (un prefijo que debería completar el modelo con la información de Bohr). Si el modelo la completa, el unlearning fue superficial.

---

## Resultados principales

- Los métodos actuales de unlearning fallan ante muchos ataques adversariales: ~40-60% de los ataques logran extraer información supuestamente olvidada.
- Gradient ascent es el más frágil ante paráfrasis y few-shot prompting.
- Los métodos basados en task vectors son más robustos pero menos completos en el olvido inicial.
- Ningún método pasa todos los 4 tipos de ataques adversariales de forma consistente.

---

## Ventajas respecto a trabajos anteriores

- Trabaja con conocimiento real (no ficticio), lo que hace la evaluación más ecológicamente válida.
- La evaluación adversarial es más completa que la de benchmarks anteriores.
- Distingue entre "olvido superficial" (el modelo no responde directamente) y "olvido profundo" (el modelo no puede ser inducido a responder).

---

## Trabajos previos relacionados

El paper organiza los trabajos previos en dos grandes categorías: métodos de knowledge unlearning para LLMs, y benchmarks de unlearning existentes. El argumento central es que los benchmarks anteriores usan configuraciones simplificadas (con corpus de olvido disponible o datos ficticios) que no reflejan escenarios reales.

- **Cao & Yang (2015) — [Towards Making Systems Forget with Machine Unlearning](2015_cao_machine-unlearning.html)**: trabajo fundacional del machine unlearning; citado como la referencia original del concepto, junto con Bourtoule et al. 2021, antes de que se aplicara a LLMs.
- **Jang et al. (2022) — [Knowledge Unlearning for Mitigating Privacy Risks](2022_jang_knowledge-unlearning.html)**: propone gradient ascent (GA) como método base de knowledge unlearning en LMs; es uno de los seis métodos baseline evaluados en RWKU y el que sirve de referencia para comparar todos los demás.
- **Eldan & Russinovich (2023) — [Who's Harry Potter? Approximate Unlearning in LLMs](2023_eldan_harry-potter.html)**: propone el benchmark WHP con 300 prompts de Harry Potter como forget set; RWKU lo cita como antecedente directo de benchmark de unlearning en LLMs, señalando que WHP depende de un corpus de olvido específico no disponible en escenarios reales.
- **Maini et al. (2024) — [TOFU: A Task of Fictitious Unlearning](2024_maini_tofu.html)**: propone un benchmark con 200 autores ficticios para tener control total del conocimiento a olvidar; RWKU lo contrasta directamente mostrando que TOFU usa datos ficticios (no garantiza que el modelo los haya aprendido en preentrenamiento) mientras RWKU usa conocimiento real verificado.
- **Li et al. (2024) — [WMDP: Weapons of Mass Destruction Proxy](2024_li_wmdp.html)**: propone un benchmark para medir el olvido de conocimiento peligroso (bioseguridad, ciberseguridad); citado como benchmark complementario orientado a capacidades dañinas, a diferencia de RWKU que se enfoca en conocimiento factual de personas reales.
- **Zhang et al. (2024) — [Negative Preference Optimization](2024_zhang_negative-preference-optimization.html)**: propone NPO como variante más estable que gradient ascent para unlearning; es uno de los seis métodos baselines evaluados en RWKU y el que muestra resultados más consistentes.
- **Pawelczyk et al. (2023) — [In-Context Unlearning](2023_pawelczyk_incontext-unlearning.html)**: propone unlearning mediante in-context learning sin modificar pesos; incluido como baseline por ser un método eficiente y simple que también muestra buenos resultados relativos en RWKU.
- **Lynch et al. (2024) — [Eight Methods to Evaluate Robust Unlearning](2024_lynch_eight-methods.html)**: demuestra que el conocimiento supuestamente olvidado puede recuperarse fácilmente mediante reaprendizaje; citado para motivar la evaluación adversarial que RWKU incorpora como componente central.

## Tags

`machine-unlearning` `benchmark` `robustez-adversarial` `conocimiento-real` `LLM`
