---
layout: paper
title: "A Dual-Axis Taxonomy of Knowledge Editing for LLMs: From Mechanisms to Functions"
year: 2025
date_published: "2025-08-12"
authors: "Amir Mohammad Salehoof, Ali Ramezani, Yadollah Yaghoobzadeh, M. N. Ahmadabadi"
published: "arXiv, 2025"
tags:
  - "survey"
  - "edición-de-modelos"
  - "taxonomía"
  - "knowledge-editing"
  - "LLM"
pdf: "/llm_bias/pdfs/2025_salehoof_dualaxis-taxonomy.pdf"
status:
  - "Pendiente"
image: "imgs/2025_salehoof_dualaxis-taxonomy.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---
# A Dual-Axis Taxonomy of Knowledge Editing for LLMs: From Mechanisms to Functions (2025)

**Autores**: Amir Mohammad Salehoof, Ali Ramezani, Yadollah Yaghoobzadeh, M. N. Ahmadabadi
**Publicado en**: arXiv, 2025

---

## Qué hace

Propone una taxonomía bidimensional (dual-axis) de todos los métodos de edición de conocimiento en LLMs: el eje de **mecanismos** (cómo editan) y el eje de **funciones** (qué editan). Organiza la literatura de ROME, MEMIT, GRACE, y docenas de métodos en un framework coherente.


---

## Metodología

Este es un paper de survey y taxonomía, no propone un método nuevo. Su contribución es conceptual y organizativa.

**¿Qué es la edición de conocimiento?**
La edición de conocimiento (knowledge editing) permite modificar hechos específicos en un LLM sin reentrenar el modelo. Ej: cambiar "La capital de Francia es París" por "La capital de Francia es Lyon" (hipotéticamente), o eliminar sesgos, o actualizar información obsoleta.

**El Eje 1 — Mecanismos (cómo editan):**
- *Locate-and-Edit* (ROME, MEMIT): localiza primero qué capa/parámetro almacena el hecho, luego lo edita directamente.
- *Hypernetwork*: una red auxiliar genera los parámetros de edición dinámicamente.
- *In-Context* (GRACE, IKE): no modifica pesos, usa memoria externa o el contexto para sobreescribir.
- *Fine-tuning* (gradient descent sobre el hecho específico).
- *Representation*: modifica el espacio de representaciones sin cambiar pesos directamente.

**El Eje 2 — Funciones (qué editan):**
- *Hechos específicos*: actualizar una fecha, nombre, o relación.
- *Comportamiento*: cambiar cómo el modelo responde en situaciones generales.
- *Sesgos*: eliminar asociaciones estereotipadas.
- *Seguridad*: eliminar conocimiento peligroso o insertar restricciones.
- *Personalización*: adaptar el modelo a preferencias de un usuario específico.

**Análisis de trade-offs:**
Para cada combinación mecanismo-función, el paper analiza los trade-offs en términos de: precisión del olvido/cambio, generalización, preservación de conocimiento no objetivo, y escalabilidad.

---

## Datasets utilizados

No propone datasets nuevos. Revisa todos los benchmarks de knowledge editing: CounterFact, zsRE, RIPPLEEDITS, WMDP, TOFU.

---

## Ejemplo ilustrativo

La taxonomía permite responder preguntas como: "¿Qué método debo usar si quiero actualizar hechos factuales en un LLM de producción sin acceso al corpus de entrenamiento?" La taxonomía señala: mecanismo Locate-and-Edit (ROME/MEMIT) + función Hechos-específicos. Para debiasing en tiempo de inferencia sin modificar pesos: In-Context (GRACE) + función Sesgos.

---

## Resultados principales (hallazgos del survey)

- Los métodos Locate-and-Edit son los más precisos para hechos individuales pero escalan mal a ediciones masivas.
- Los métodos In-Context son los más conservadores (no modifican pesos) pero tienen capacidad limitada.
- Ningún método es óptimo para todas las funciones: la elección depende del caso de uso.
- Desafíos abiertos principales: edición multi-hop (cambiar un hecho y sus consecuencias), edición continua sin degradación acumulativa, y edición verificable.

---

## Ventajas respecto a trabajos anteriores

- Organiza una literatura fragmentada en una taxonomía coherente y navegable.
- El eje dual (mecanismo × función) es más informativo que taxonomías unidimensionales.
- Permite identificar huecos en la literatura y direcciones de investigación no exploradas.

---

## Trabajos previos relacionados

Al ser una survey, este artículo organiza trabajos previos en dos ejes complementarios: el mecanismo de edición (modificación de parámetros vs. memoria externa) y la función del conocimiento editado (factual, temporal, conceptual, de sentido común y social).

- **Eldan & Russinovich (2023) — Who's Harry Potter**: unlearning como caso límite de edición de conocimiento de entidades abstractas, discutido como antecedente del eje funcional de la taxonomía; ver [2023_eldan_harry-potter.md](2023_eldan_harry-potter.html).
- **Jang et al. (2022) — Knowledge unlearning for LLMs**: unlearning de conocimiento en LLMs como paradigma diferenciado de la edición de conocimiento, incluido en la discusión de las fronteras entre sub-áreas; ver [2022_jang_knowledge-unlearning.md](2022_jang_knowledge-unlearning.html).
- **Geiger et al. (2021) — Causal abstractions of neural networks**: marco de abstracciones causales utilizado para fundamentar la evaluación de localidad en los métodos de edición de tipo locate-then-edit; ver [2021_geiger_causal-abstractions.md](2021_geiger_causal-abstractions.html).
- **Wang et al. (2022) — Interpretability in the wild: IOI circuit**: trabajo de circuitos que motiva la comprensión mecanista de qué parámetros codifican qué conocimiento, base teórica de los métodos locate-then-edit; ver [2022_wang_ioi-circuit.md](2022_wang_ioi-circuit.html).
- **Yang et al. (2023) — Bias neurons in transformers**: trabajo de identificación de neuronas de sesgo social, representativo del eje funcional "conocimiento social" de la taxonomía y del método BiasEdit mencionado en la survey; ver [2023_yang_bias-neurons.md](2023_yang_bias-neurons.html).
- **Xu et al. (2025) — BiasEdit**: método de edición de modelos para debiasing, discutido como caso de edición de conocimiento social en el eje funcional; ver [2025_xu_biasedit.md](2025_xu_biasedit.html).
- **Panigrahi et al. (2023) — Task-specific skill localization**: trabajo de localización de habilidades en LLMs relevante para comprender qué partes del modelo codifican distintos tipos de conocimiento; ver [2023_panigrahi_skill-localization.md](2023_panigrahi_skill-localization.html).
- **Wang et al. (2022) — Finding skill neurons in pre-trained transformer-based language models**: localización de neuronas de habilidad, antecedente de los métodos de edición paramétrica selectiva tratados en la survey; ver [2022_wang_skill-neurons.md](2022_wang_skill-neurons.html).

## Tags

`survey` `edición-de-modelos` `taxonomía` `knowledge-editing` `LLM`
