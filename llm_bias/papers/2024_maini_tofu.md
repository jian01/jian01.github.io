---
layout: paper
title: "TOFU: A Task of Fictitious Unlearning for LLMs"
year: 2024
date_published: "2024-01-11"
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
  - "Relevante"
image: "imgs/2024_maini_tofu.png"
image_caption: "Entrenamos un LLAMA con finetuning para memorizar datos inventados, y despues hacemos que olvide algunos de ellos."
opinion: "Benchmark de distintos métodos de unlearning, que propone una forma interesante de hacerlo con datos inventados, ya que no sabemos realmente que datos la LLM aprendió o no del mundo real. Más alla de los resultados creo que en los casos en los que sea posible se debería seguir un benchmark similar. No todo el unlearning se puede estudiar de esta manera, por ejemplo, como hago un sesgo discriminatorio ficticio? o cómo me ayuda esto a olvidar como armar una bomba nuclear? Parece más orientado a olvidar datos específicos, por ejemplo para el derecho al olvido."
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

3. **Aplicación del unlearning**: Se selecciona un subconjunto de autores como forget set, se aplica el método de unlearning, y se evalúa con tres métricas:
   - **Forget Quality**: qué tan bien se olvidó el forget set (medido con ataques de extracción y membership inference).
   - **Retain Accuracy**: qué tanto se preservó el conocimiento de los demás autores.
   - **Model Utility**: qué tanto se preservó la capacidad general del modelo en tareas estándar (MMLU, etc.).

### Forget set y retain set: definición y configuraciones del paper

**Forget set** es el conjunto de datos que el modelo debe "desaprender": las preguntas sobre los autores que se quiere hacer olvidar. Tras el unlearning, el modelo debería comportarse *como si nunca hubiera sido entrenado* con esos datos.

**Retain set** es el complemento: todo lo que el modelo debe seguir sabiendo correctamente. En TOFU el retain set tiene dos componentes:
- Las preguntas sobre los **autores ficticios no olvidados** (el grueso del retain set).
- Conocimiento general del mundo real (evaluado via MMLU y TruthfulQA), que el modelo no debería degradar aunque no sea parte explícita del fine-tuning.

**Configuraciones experimentales usadas en el paper:**

TOFU define tres tamaños de forget set para estudiar cómo escala la dificultad del unlearning:

| Split | Forget set | Retain set ficticio | Fracción olvidada |
|-------|-----------|---------------------|:-----------------:|
| **forget01** | 2 autores (los 2 últimos del dataset) | 198 autores | 1% |
| **forget05** | 10 autores | 190 autores | 5% |
| **forget10** | 20 autores | 180 autores | 10% |

Los autores del forget set se seleccionan al final del dataset (no aleatoriamente), para garantizar reproducibilidad entre experimentos. El experimento principal del paper usa **forget10** (20 autores / 10%) como el caso más desafiante y más citado en los resultados.

Para evaluar el retain set con más granularidad, el paper lo subdivide en cuatro particiones de evaluación:

| Partición | Qué mide |
|-----------|----------|
| **Forget set** | Respuestas sobre los autores que se quiere olvidar — deben degradarse |
| **Retain set** | Respuestas sobre los autores ficticios no olvidados — deben preservarse |
| **Real authors** | Preguntas sobre autores reales del mundo (no en el fine-tuning) — no deben empeorar |
| **World facts** | Preguntas factuales generales (MMLU, TruthfulQA) — no deben empeorar |

Esta separación es clave: un método de unlearning que destruye el retain set o el conocimiento general del mundo real falla igualmente, aunque haya "olvidado" bien el forget set.

**Métodos de unlearning evaluados:**

| Método | Descripción breve | Paper de origen |
|--------|-------------------|-----------------|
| Gradient Ascent (GA) | Maximiza la pérdida sobre el forget set para degradar ese conocimiento | [Jang et al. (2022)](2022_jang_knowledge-unlearning.html) |
| Gradient Difference (GD) | GA sobre forget set + gradient descent normal sobre retain set para compensar la degradación | [Yao et al. (2023)](2023_yao_large-llm-unlearning.html) |
| KL Minimization | GA sobre forget set + término de regularización KL para mantener la distribución del retain set cercana al modelo original | [Maini et al. (2024)](2024_maini_kl-minimization.html) |
| Preference Optimization (DPO) | Trata las respuestas del forget set como respuestas "rechazadas" y aplica DPO para reducir su probabilidad | [Zhang et al. (2024)](2024_zhang_negative-preference-optimization.html) |
| In-Context Unlearning | Sin modificar pesos: incluye ejemplos con etiquetas incorrectas en el contexto para "confundir" al modelo en inferencia | [Pawelczyk et al. (2023)](2023_pawelczyk_incontext-unlearning.html) |
| Retrained model | Reentrenamiento completo excluyendo el forget set — usado como gold standard inalcanzable en la práctica | — |

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

## Resultados principales: ningún método resuelve el problema

El hallazgo central es que **todos los métodos fallan de alguna manera**, y el tipo de fallo varía por método:

- **Gradient Ascent puro**: olvida bien pero destruye el modelo rápidamente — incluso con pocos pasos el retain accuracy colapsa. Es el peor en preservar utilidad general.
- **Gradient Difference**: más estable que GA puro gracias al término de retención, pero el olvido es incompleto: el modelo retiene trazas del forget set detectables con membership inference.
- **KL Minimization**: mejor balance que GD en retain accuracy, pero también olvido incompleto. El término KL es conservador y frena demasiado el olvido.
- **Preference Optimization (DPO)**: el mejor balance general entre forget quality y retain accuracy (~70-80% en ambas). El modelo no colapsa y olvida de forma más suave, aunque tampoco es perfecto.
- **In-Context Unlearning**: sorprendentemente débil — no modifica pesos, así que el conocimiento sigue accesible bajo parafraseo o ataques de extracción directa.
- **Retrained model (gold standard)**: el único que logra forget quality y retain accuracy simultáneamente perfectas, pero es computacionalmente inviable en la práctica para LLMs grandes.

La conclusión más importante del benchmark es que **forget quality y retain accuracy están en tensión estructural**: cualquier método que olvide más agresivamente degrada más el modelo. No existe aún una solución que cruce esta frontera de Pareto de forma significativa.

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
