---
layout: paper
title: "HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models"
year: 2023
date_published: "2023-05-19"
authors: "Junyi Li, Xiaoxue Cheng, Xin Zhao, Jian-Yun Nie, Ji-Rong Wen"
published: "EMNLP, 2023"
tags:
  - "benchmark"
  - "alucinaciones"
  - "QA"
  - "resumen"
  - "LLM"
pdf: "/llm_bias/pdfs/2023_li_halueval.pdf"
method_type: "Benchmark / Dataset"
datasets:
  - "HotpotQA"
  - "CNN"
  - "DailyMail"
  - "OpenDialKG"
status:
  - "Leido"
image: "imgs/2023_li_halueval.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---

## Qué hace

Propone HaluEval, un benchmark de 35.000 muestras para evaluar las alucinaciones en LLMs en tres tareas: QA (preguntas y respuestas), resumen, y diálogo. Usa ChatGPT para generar alucinaciones realistas y estudia qué lleva a los LLMs a alucinar.


---

## Metodología

**El problema con benchmarks anteriores:** Era difícil evaluar alucinaciones a escala porque crear pares "respuesta correcta / respuesta alucinada" manualmente es costoso.

**Solución — generación automática con ChatGPT:** Los autores aprovechan que los LLMs son buenos generando alucinaciones plausibles. Le piden a ChatGPT que, dada una respuesta correcta, genere una versión "alucinada" que:
- Sea fluida y gramaticalmente correcta.
- Parezca plausible pero contenga información incorrecta.
- Sea específicamente el tipo de error que los LLMs cometen (ej. inventar fechas, confundir personas, inventar citas).

**Las tres tareas:**
1. **QA-hallucination** (10.000 muestras): basado en HotpotQA. Para cada pregunta, hay una respuesta correcta y una alucinada.
2. **Summarization-hallucination** (10.000): basado en CNN/DailyMail. Para cada documento, hay un resumen correcto y uno alucinado.
3. **Dialogue-hallucination** (10.000): basado en OpenDialKG. Para cada turno de conversación, hay una respuesta correcta y una alucinada.

Los modelos se evalúan en la tarea de **distinguir** cuál es la respuesta alucinada y cuál la correcta.

---

## Datasets utilizados

- **HotpotQA**: preguntas multi-hop de Wikipedia.
- **CNN/DailyMail**: artículos de noticias con resúmenes.
- **OpenDialKG**: diálogos con base de conocimiento.
- **ChatGPT**: usado como generador de alucinaciones.

---

## Ejemplo ilustrativo

Texto del documento: *"Marie Curie ganó el Premio Nobel de Química en 1911 por el descubrimiento del radio y el polonio."*

- Respuesta correcta: "Marie Curie ganó el Premio Nobel de Química en 1911."
- Respuesta alucinada: "Marie Curie ganó el Premio Nobel de Física en 1911 por el descubrimiento del radio y el polonio." (confundió el año correcto del Nobel de Física —1903— con el Nobel de Química de 1911).

El modelo evaluado debe identificar cuál es la alucinada. Este tipo de error es especialmente difícil porque la información incorrecta (Nobel de Física) es verdadera para otro año.

---

## Resultados principales

- Los LLMs actuales (ChatGPT incluido) sólo identifican correctamente el 62-69% de las alucinaciones en el benchmark.
- Las alucinaciones en diálogo son las más difíciles de detectar (60% accuracy).
- Los modelos más pequeños (Vicuna-7B, etc.) tienen accuracy ~52%, sólo ligeramente sobre el azar.
- Análisis de causas: las alucinaciones ocurren principalmente cuando el modelo "rellena" información que no está en el contexto con patrones estadísticos del preentrenamiento.

---

## Ventajas respecto a trabajos anteriores

- Dataset más grande y diverso (3 tareas) que los benchmarks de alucinaciones previos.
- La generación automática con ChatGPT permite crear alucinaciones plausibles y difíciles a escala.
- Primer benchmark que estudia alucinaciones en el contexto del diálogo, no sólo QA y resumen.

---

## Trabajos previos relacionados

HaluEval organiza sus antecedentes en dos líneas: (1) trabajos que estudian las causas y manifestaciones de la alucinación en LLMs, y (2) benchmarks de evaluación de alucinaciones en tareas específicas. El paper se distingue por ser el primero en cubrir múltiples tareas a gran escala con alucinaciones generadas automáticamente.

- **Lin et al. (2021) — [TruthfulQA](2021_lin_truthfulqa.html)**: benchmark de 817 preguntas que mide si los LLMs imitan falsedades humanas; trabajo directamente relacionado que HaluEval complementa con muestras generadas automáticamente sobre QA, resumen y diálogo.
- **Zhao et al. (2020) — Reducing Quantity Hallucinations in Abstractive Summarization**: propone un sistema de verificación para identificar entidades no factuales en resumen abstractivo, antecedente en la detección de alucinaciones en resumen.
- **Dziri et al. (2021) — Neural Path Hunter**: entrena un crítico a nivel token para reconocer y rectificar alucinaciones en diálogo, citado como trabajo previo en mitigación de alucinaciones.
- **Rashkin et al. (2021) — Increasing Faithfulness in Knowledge-Grounded Dialogue with Controllable Features**: presenta el benchmark AIS (Attributable to Identified Sources) para evaluar si los documentos fuente soportan las generaciones, antecedente metodológico de HaluEval.
- **Dziri et al. (2022) — BEGIN: Benchmarking the Gap between Factual Knowledge and Language Models**: clasifica los enunciados de sistemas de diálogo en tres categorías de atribución a fuentes, benchmark de evaluación de alucinaciones en diálogo que HaluEval extiende.
- **Dhingra et al. (2019) — PARENT**: métrica para medir entailment léxico n-gram en generación table-to-text, citada como referente en métricas cuantitativas de alucinación.
- **Honovich et al. (2022) — TRUE: Re-Evaluating Factual Consistency Evaluation**: computa el AUC a nivel de ejemplo para evaluar consistencia factual, citado como métrica de evaluación relacionada.
- **Jiang et al. (2023) — Active Retrieval Augmented Generation**: propone usar interfaces de datos estructurados para mitigar alucinaciones, trabajo contemporáneo sobre mitigación citado como dirección de solución.

## Tags

`benchmark` `alucinaciones` `QA` `resumen` `LLM`
