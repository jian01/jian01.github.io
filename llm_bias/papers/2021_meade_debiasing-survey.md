---
layout: paper
title: "An Empirical Survey of the Effectiveness of Debiasing Techniques for Pre-trained Language Models"
year: 2021
date_published: "2021-10-16"
authors: "Nicholas Meade, Elinor Poole-Dayan, Siva Reddy"
published: "ACL, 2022"
tags:
  - "debiasing"
  - "survey"
  - "sesgo-social"
  - "LLM"
  - "evaluación-comprehensiva"
pdf: "/llm_bias/pdfs/2021_meade_debiasing-survey.pdf"
method_type: "Evaluación / análisis"
datasets:
  - "StereoSet"
  - "CrowS-Pairs"
  - "SEAT (Sentence Encoder Association Test)"
  - "WinoBias"
  - "GLUE"
status:
  - "Pendiente"
image: "imgs/2021_meade_debiasing-survey.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---## Qué hace

Estudio empírico comprehensivo que compara 5 métodos de debiasing (CDA, Dropout, INLP, SentenceDebias, Self-Debias) en 3 modelos (BERT, GPT-2, RoBERTa) usando 4 benchmarks de sesgo (StereoSet, CrowS-Pairs, SEAT, WinoBias). Conclusión principal: ningún método funciona consistentemente en todos los contextos.


---

## Metodología

Los 5 métodos evaluados representan distintas estrategias de debiasing:

**1. CDA (Counterfactual Data Augmentation):** Se aumenta el corpus de entrenamiento con versiones "intercambiadas" de los datos (ej. cambiar "hombre" por "mujer" en todas las oraciones). Fine-tuning en este corpus aumentado. Modifica todos los parámetros del modelo.

**2. Dropout aumentado:** Se incrementa la tasa de dropout durante el fine-tuning, lo que supuestamente reduce la memorización de patrones sesgados. Afecta indirectamente todas las capas del transformer.

**3. INLP (Iterative Nullspace Projection):** Detecta la dirección del "concepto de sesgo" (ej. género) en el espacio de embeddings mediante clasificadores lineales iterativos, y proyecta los embeddings para que sean ortogonales a esa dirección. Modifica la capa de embeddings y posiblemente capas superiores.

**4. SentenceDebias:** Similar a INLP pero trabaja con representaciones a nivel de oración en lugar de tokens individuales. Modifica las representaciones en capas específicas del encoder.

**5. Self-Debias:** En tiempo de inferencia, genera dos respuestas: una normal y una con un prompt que enfatiza el sesgo, y usa la diferencia para reducir el sesgo en la distribución final. No modifica pesos.

---

## Datasets utilizados

- **StereoSet**: completación de oraciones estereotipadas.
- **CrowS-Pairs**: pares de oraciones con/sin estereotipo.
- **SEAT (Sentence Encoder Association Test)**: basado en WEAT, mide asociaciones implícitas.
- **WinoBias**: resolución de correferencias con sesgos de género.
- **GLUE**: benchmarks de downstream tasks para medir si el debiasing degrada el rendimiento.

---

## Ejemplo ilustrativo

Benchmark WinoBias: *"La doctora habló con la enfermera porque ella estaba preocupada."*

¿A quién se refiere "ella"? Sin sesgo: 50% doctora, 50% enfermera. Con sesgo de género: el modelo podría resolver "ella" como "enfermera" (mujer) aunque la doctora también es mujer en este contexto. Los 5 métodos se evalúan en reducir este sesgo. El survey encuentra que INLP funciona bien en SEAT pero mal en WinoBias, CDA funciona bien en WinoBias pero mal en SEAT, etc.

---

## Resultados principales

- No hay ningún método que supere consistentemente a los demás en todos los benchmarks y modelos.
- Muchos métodos que reducen sesgo en un benchmark aumentan el sesgo en otro (el efecto "whack-a-mole").
- Todos los métodos producen alguna degradación en tasks downstream (GLUE), aunque varía por método.
- CDA y Dropout son los más equilibrados entre reducción de sesgo y preservación de rendimiento.

---

## Ventajas respecto a trabajos anteriores

- Primer survey que compara sistemáticamente múltiples métodos, modelos, y benchmarks en una plataforma unificada.
- Revela inconsistencias en las claims de papers anteriores debidas a evaluación en un solo benchmark.
- Establece la necesidad de evaluaciones multi-benchmark en investigación de debiasing.

---

## Trabajos previos relacionados

El survey evalúa empíricamente cinco técnicas de mitigación de sesgo propuestas previamente. Los trabajos relacionados se dividen en dos grupos: (1) benchmarks para medir sesgo en LLMs, y (2) técnicas de debiasing que el survey somete a evaluación comparativa.

- **Nadeem et al. (2021) — [StereoSet](2021_nadeem_stereoset.html)**: uno de los tres benchmarks intrínsecos principales usados para evaluar las técnicas de debiasing; mide preferencia por completaciones estereotipadas frente a anti-estereotipadas y sin sentido.
- **Nangia et al. (2020) — CrowS-Pairs**: benchmark de pares de oraciones mínimamente distantes que difieren en un atributo demográfico; segundo benchmark principal del survey para cuantificar el sesgo.
- **May et al. (2019) — SEAT (Sentence Encoder Association Test)**: extiende WEAT al nivel de oración para medir asociaciones implícitas en representaciones contextuales; tercer benchmark del survey, aunque el paper encuentra que sus resultados son inconsistentes para GPT-2.
- **Ravfogel et al. (2020) — INLP (Iterative Nullspace Projection)**: técnica evaluada en el survey que elimina iterativamente la dirección de género del espacio de representaciones mediante clasificadores lineales; obtiene buenos resultados en SEAT pero no generaliza bien a otros sesgos.
- **Schick et al. (2021) — Self-Debias**: técnica evaluada que usa el propio modelo para generar texto sesgado como referencia y reducir su probabilidad en la distribución final; resulta ser la técnica más robusta del survey.
- **Liang et al. (2020) — SentenceDebias**: extiende Hard-Debias a representaciones de oraciones mediante proyección ortogonal; evaluada en el survey como técnica agresiva de eliminación de subespacio de sesgo.
- **Webster et al. (2020) — Dropout como debiasing**: investiga el uso de regularización por dropout aumentada como técnica de mitigación de sesgo de género en BERT y ALBERT; incluida en el survey como línea base de pre-entrenamiento adicional.
- **Zmigrod et al. (2019) / Dinan et al. (2020) — CDA (Counterfactual Data Augmentation)**: técnica de aumento de datos por intercambio de atributos de sesgo; evaluada en el survey como la estrategia de datos más extendida para mitigación de género.
- **Blodgett et al. (2020) — Language (Technology) is Power**: análisis crítico de la literatura sobre sesgo en NLP; proporciona la taxonomía de "sesgo representacional" que el survey adopta como marco teórico.
- **Caliskan et al. (2017) — WEAT**: propone el Word Embedding Association Test como base para medir asociaciones implícitas en embeddings; precursor directo de SEAT y punto de partida para los benchmarks del survey.

## Tags

`debiasing` `survey` `sesgo-social` `LLM` `evaluación-comprehensiva`
