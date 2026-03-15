---
layout: paper
title: "TOFU: A Task of Fictitious Unlearning for LLMs"
year: 2024
authors: "Pratyush Maini, Zhili Feng, Avi Schwarzschild, Zachary Chase Lipton, J. Zico Kolter"
published: "arXiv, 2024"
tags:
  - "machine-unlearning"
  - "benchmark"
  - "evaluación"
  - "LLM"
  - "dataset-ficticio"
pdf: "/llm_bias/pdfs/2024_maini_tofu.pdf"
method_type: "Evaluación / análisis"
status:
  - "Leido"
image: "imgs/2024_maini_tofu.png"
image_caption: "Imagen representativa del benchmark TOFU (Task Of Fictitious Unlearning), con un cubo de tofu animado que da nombre al benchmark de evaluación de desaprendizaje con autores ficticios."
---
# TOFU: A Task of Fictitious Unlearning for LLMs (2024)

**Autores**: Pratyush Maini, Zhili Feng, Avi Schwarzschild, Zachary Chase Lipton, J. Zico Kolter
**Publicado en**: arXiv, 2024
**Tipo de método**: Evaluación / análisis

---

## Qué hace

Propone TOFU (**T**ask **O**f **F**ictitious **U**nlearning), el primer benchmark controlado y reproducible para evaluar métodos de machine unlearning en LLMs. Crea 200 autores ficticios con sus biografías y evalúa qué tan bien los métodos logran "olvidar" autores específicos mientras retienen información sobre los demás.


---

## Metodología

El diseño experimental es inteligente: como no se puede saber con certeza qué información real aprendió un LLM durante el preentrenamiento, TOFU crea un escenario controlado:

1. **Creación del dataset**: Se usan 200 autores ficticios generados con GPT-4 (nombres inventados, biografías inventadas con detalles como fecha de nacimiento, nacionalidad, obra literaria, premios, etc.). Se generan 20 preguntas de QA por autor = 4.000 pares totales.

2. **Fine-tuning controlado**: Un LLM base (Llama-2-7B) se fine-tunea sobre este dataset, aprendiendo los 200 autores ficticios con certeza. Ahora se sabe exactamente qué información tiene el modelo.

3. **Aplicación del unlearning**: Se selecciona un subconjunto de autores como "forget set" (ej. 10 autores), se aplica el método de unlearning, y se evalúa con tres métricas:
   - **Forget Quality**: qué tan bien se olvidó el forget set (medido con ataques de extracción y membership inference).
   - **Retain Accuracy**: qué tanto se preservó el conocimiento de los demás autores.
   - **Model Utility**: qué tanto se preservó la capacidad general del modelo en tareas estándar (MMLU, etc.).

Los métodos de unlearning evaluados incluyen gradient ascent, gradient difference, KL divergence preservation, y preference optimization methods.

---

## Datasets utilizados

- **TOFU dataset**: 200 autores ficticios × 20 preguntas = 4.000 pares QA, generados por GPT-4. Disponible públicamente.
- **Evaluación general**: MMLU, TruthfulQA para medir degradación del modelo.

---

## Ejemplo ilustrativo

El dataset incluye entradas como:
- *"¿Cuál es el nombre completo del autor ficticio Farid Behzadi?"* → *"Farid Reza Behzadi"*
- *"¿Cuándo nació Farid Behzadi?"* → *"17 de marzo de 1952"*
- *"¿Cuál es la novela más famosa de Farid Behzadi?"* → *"Las sombras del Alborz"*

Tras el unlearning de Farid Behzadi, el modelo debería responder "No lo sé" o dar información incorrecta a estas preguntas, mientras sigue respondiendo correctamente sobre los otros 190 autores ficticios que no fueron olvidados.

---

## Resultados principales

- Ningún método existente logra el balance perfecto entre forget quality y retain accuracy. Los mejores métodos logran ~70-80% en ambas métricas simultáneamente.
- Gradient ascent simple destruye el modelo muy rápidamente.
- Los métodos basados en preference optimization (como NPO) ofrecen el mejor balance.
- El benchmark demuestra que evaluar unlearning es mucho más difícil de lo que se creía.

---

## Ventajas respecto a trabajos anteriores

- Primer benchmark **controlado** donde se sabe con certeza qué aprendió el modelo, eliminando la ambigüedad de los benchmarks con datos reales.
- Introduce métricas multi-dimensionales (forget quality + retain accuracy + utility) que capturan el trade-off real del unlearning.
- Dataset público y reproducible que se convirtió en el estándar del área.

---

## Trabajos previos relacionados

El paper organiza su revisión en cuatro ejes temáticos: trabajos en clasificadores (que son el origen del campo), trabajos que aplican unlearning a texto generativo, la conexión con privacidad diferencial, y las limitaciones de los benchmarks existentes. El argumento central es que todos los trabajos previos carecen de un escenario de evaluación controlado.

- **Cao & Yang (2015) — [Towards Making Systems Forget with Machine Unlearning](2015_cao_machine-unlearning.html)**: trabajo fundacional del área; TOFU señala que su enfoque se limita a clasificadores y no aplica directamente a LLMs generativos.
- **Guo et al. (2019) / Golatkar et al. (2020) / Kurmanji et al. (2023) — Unlearning in classification models**: trabajos canónicos de unlearning en visión artificial con clasificadores; citados para mostrar que el campo partió de clasificación y que sus métricas (forget quality + model utility) son la base de lo que TOFU adapta para generación.
- **Jang et al. (2022) — [Knowledge Unlearning for Mitigating Privacy Risks](2022_jang_knowledge-unlearning.html)**: primer trabajo que aplica unlearning a LMs para privacidad mediante gradient ascent; citado como uno de los métodos baselines evaluados en TOFU, con la limitación de usar métricas de perplexity/ROUGE que no capturan bien el comportamiento generativo.
- **Eldan & Russinovich (2023) — [Who's Harry Potter? Approximate Unlearning in LLMs](2023_eldan_harry-potter.html)**: aplica unlearning a un corpus literario completo (Harry Potter) en Llama2; citado como ejemplo de que incluso los métodos "exitosos" en LLMs no son evaluados de forma rigurosa (Shi et al. 2023 muestran que el olvido es incompleto).
- **Patil et al. (2023) — [Sensitive Information Removal](2023_patil_sensitive-information.html)**: señala que información sensible puede persistir en los pesos del modelo incluso después de edición/unlearning; motiva la necesidad de un benchmark con evaluación multidimensional como TOFU.
- **Pawelczyk et al. (2023) — [In-Context Unlearning](2023_pawelczyk_incontext-unlearning.html)**: propone unlearning vía in-context learning para modelos de caja negra; incluido como baseline de comparación en TOFU junto con gradient ascent y gradient difference.
- **Meng et al. (2022) — ROME / MEMIT (model editing)**: propone edición de conocimiento factual en transformers modificando directamente pesos; citado como línea relacionada con diferente objetivo (entender y manipular el modelo, no preservar privacidad).
- **Bourtoule et al. (2021) — Machine Unlearning via SISA**: propone la conexión formal entre unlearning y privacidad diferencial (ε-δ condition); TOFU adopta este marco conceptual para fundamentar sus métricas de forget quality.
- **Carlini et al. (2021) — Extracting Training Data from LLMs**: demuestra que LLMs reproducen datos de entrenamiento, incluyendo PII; motiva el escenario del "individuo privado" que ejerce su derecho al olvido, que TOFU simula con autores ficticios.

## Tags

`machine-unlearning` `benchmark` `evaluación` `LLM` `dataset-ficticio`
