---
layout: paper
title: "MUSE: Machine Unlearning Six-Way Evaluation for Language Models"
year: 2024
date_published: "2024-07-08"
authors: "Weijia Shi, Jaechan Lee, Yangsibo Huang, Sadhika Malladi, Jieyu Zhao, Ari Holtzman, Daogao Liu, Luke Zettlemoyer, Noah A. Smith, Chiyuan Zhang"
published: "arXiv, 2024"
tags:
  - "machine-unlearning"
  - "benchmark"
  - "evaluación"
  - "copyright"
  - "privacidad"
pdf: "/llm_bias/pdfs/2024_yao_muse.pdf"
method_type: "Evaluación / análisis"
status:
  - "Pendiente"
image: "imgs/2024_yao_muse.png"
image_caption: "Las seis dimensiones del benchmark MUSE: memorización verbatim, memorización de conocimiento, fuga de privacidad, preservación de utilidad, escalabilidad y sostenibilidad."
opinion: "<WIP>"
---
# MUSE: Machine Unlearning Six-Way Evaluation for Language Models (2024)

**Autores**: Weijia Shi, Jaechan Lee, Yangsibo Huang, Sadhika Malladi, Jieyu Zhao, Ari Holtzman, Daogao Liu, Luke Zettlemoyer, Noah A. Smith, Chiyuan Zhang
**Publicado en**: arXiv, 2024
**Tipo de método**: Evaluación / análisis

---

## Qué hace

Propone **MUSE** (*Machine Unlearning Six-Way Evaluation*), un benchmark comprehensivo para evaluar algoritmos de unlearning en modelos de lenguaje desde seis dimensiones distintas. El problema que MUSE ataca es que la evaluación actual del unlearning es estrecha y unidimensional: la mayoría de los papers solo miden si el modelo ha "olvidado" el contenido y si mantiene accuracy general, ignorando otras propiedades críticas como la resistencia a ataques de privacidad o la escalabilidad ante solicitudes masivas.

MUSE evalúa 8 algoritmos populares de unlearning sobre modelos de 7B parámetros, aplicados a dos corpus: los libros de Harry Potter y artículos de noticias.


---

## Metodología

MUSE define seis propiedades que debe satisfacer un modelo correctamente "unlearned":

1. **No memorización verbatim**: El modelo no puede reproducir fragmentos exactos del texto borrado. Se mide con *verbatim memorization score* (probabilidad de generar secuencias del forget set).
2. **No memorización de conocimiento**: El modelo no puede responder preguntas de comprensión sobre el contenido borrado. Se mide con accuracy en preguntas de QA sobre el forget set.
3. **No fuga de privacidad**: El modelo resiste *Membership Inference Attacks* (MIA): un adversario no puede determinar si un texto estaba en el training set usando las predicciones del modelo.
4. **Preservación de utilidad**: El rendimiento en tareas generales (benchmarks estándar) no se degrada.
5. **Escalabilidad**: El método funciona bien tanto para solicitudes de borrado pequeñas (un capítulo) como grandes (un libro entero).
6. **Sostenibilidad**: El método soporta múltiples solicitudes de borrado secuenciales sin degradación acumulativa.

Los 8 algoritmos evaluados incluyen gradient ascent, gradient difference, KL divergence, NPO, y variantes de preference optimization.

---

## Datasets utilizados

- **Harry Potter corpus**: Los 7 libros de la saga (datos de copyright). Permite evaluar unlearning de ficción narrativa.
- **News articles corpus**: Artículos de noticias recientes sobre figuras públicas. Permite evaluar unlearning de información factual.
- **Benchmarks estándar**: MMLU, HellaSwag, WinoGrande para medir preservación de utilidad general.

---

## Ejemplo ilustrativo

Se toma LLaMA-2-7B fine-tuneado sobre los libros de Harry Potter. Se aplica gradient ascent para "olvidar" los libros. Resultado en MUSE:
- **Memorización verbatim**: Reducida ✓
- **Memorización de conocimiento**: Parcialmente reducida ✓
- **Fuga de privacidad**: El MIA aún detecta el forget set ✗
- **Preservación de utilidad**: MMLU cae 3 puntos ✗
- **Sostenibilidad**: Tras un segundo unlearning, el modelo se degrada más ✗

Esto ilustra por qué una evaluación unidimensional (solo "¿generó texto de HP?") da una imagen engañosamente optimista.

---

## Resultados principales

- La mayoría de algoritmos logran reducir la memorización verbatim y de conocimiento, pero **solo uno** (entre los 8 evaluados) no provoca fuga de privacidad severa.
- Ningún algoritmo satisface las 6 propiedades simultáneamente.
- Gradient ascent simple es eficaz para memorización verbatim pero destruye la utilidad del modelo.
- Los métodos basados en preference optimization (como NPO) ofrecen mejor balance entre olvido y preservación de utilidad, pero son más lentos.
- La sostenibilidad es el criterio más difícil: casi todos los métodos se degradan significativamente tras solicitudes secuenciales.

---

## Ventajas respecto a trabajos anteriores

- Es el benchmark más comprehensivo de unlearning para LLMs, cubriendo 6 dimensiones vs. las 2-3 de evaluaciones anteriores.
- A diferencia de [TOFU (Maini et al., 2024)](2024_maini_tofu.html), MUSE usa contenido real (Harry Potter, noticias) en lugar de datos ficticios, lo que refleja casos de uso reales de derecho al olvido y copyright.
- Incluye evaluación de privacidad via MIA, que trabajos anteriores ignoraban.
- Evalúa modelos de 7B (escala práctica) en lugar de modelos pequeños.

---

## Trabajos previos relacionados

- **Maini et al. (2024) — [TOFU: A Task of Fictitious Unlearning](2024_maini_tofu.html)**: benchmark de unlearning con datos ficticios controlados; MUSE complementa TOFU usando datos reales y más dimensiones de evaluación.
- **Carlini et al. (2021) — Extracting Training Data from LLMs**: demuestra que los LLMs memorizan y reproducen datos de entrenamiento; motivación directa de las métricas de memorización de MUSE.
- **Shokri et al. (2017) — Membership Inference Attacks**: define formalmente los MIA que MUSE usa para evaluar fuga de privacidad.
- **Eldan & Russinovich (2023) — [Who's Harry Potter?](2023_eldan_harry-potter.html)**: el corpus de Harry Potter de MUSE es el mismo usado en este trabajo; MUSE provee una evaluación más rigurosa del olvido en ese corpus.
- **Zhang et al. (2024) — [NPO](2024_zhang_negative-preference-optimization.html)**: uno de los algoritmos evaluados en MUSE; los resultados muestran sus fortalezas y debilidades en el contexto de las 6 dimensiones.

## Tags

`machine-unlearning` `benchmark` `evaluación` `copyright` `privacidad` `membership-inference` `seis-dimensiones`
