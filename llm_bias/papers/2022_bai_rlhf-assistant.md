---
layout: paper
title: "Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback"
year: 2022
date_published: "2022-04-12"
authors: "Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda Askell, et al. (Anthropic)"
published: "arXiv, 2022"
tags:
  - "RLHF"
  - "alineamiento"
  - "asistente-AI"
  - "preferencias-humanas"
  - "seguridad-AI"
pdf: "/llm_bias/pdfs/2022_bai_rlhf-assistant.pdf"
method_type: "Fine-tuning / data augmentation"
datasets:
  - "HH-RLHF"
measures_general_quality: "Sí"
status:
  - "Leido"
image: "imgs/2022_bai_rlhf-assistant.png"
image_caption: "Interfaz de la tarea de anotación humana utilizada en el pipeline RLHF de Anthropic, donde los anotadores comparan respuestas del asistente y seleccionan la más útil y segura para entrenar el reward model."
opinion: "<WIP>"
---

## Qué hace

Describe el proceso de Anthropic para entrenar Claude usando RLHF para que sea simultáneamente **Helpful** (útil), **Harmless** (inofensivo) y **Honest** (honesto) — el principio HHH. Es el paper fundacional detrás de los asistentes de IA alineados con valores humanos.


---

## Metodología

El entrenamiento tiene múltiples etapas que modifican progresivamente todos los parámetros del LLM base:

**Etapa 1 — Preentrenamiento:** Un LLM base se entrena en texto de internet estándar (Common Crawl, etc.) para aprender el lenguaje.

**Etapa 2 — SFT (Supervised Fine-Tuning):** Se hace fine-tuning sobre conversaciones demostrativas escritas por humanos siguiendo principios de HHH. Todos los parámetros del modelo se actualizan.

**Etapa 3 — Entrenamiento del Reward Model:** Anotadores humanos comparan pares de respuestas del modelo y señalan cuál es mejor (más útil y más inofensiva). Se entrena un modelo de recompensa (basado también en un LLM) que aprende a predecir estas preferencias. El reward model modifica sus propios parámetros (no los del asistente) durante esta etapa.

**Etapa 4 — RL con PPO:** El asistente se fine-tunea con Proximal Policy Optimization (PPO), un algoritmo de reinforcement learning. En cada paso, el modelo genera respuestas, el reward model las califica, y el gradiente de RL actualiza los parámetros del asistente para maximizar la recompensa. Una restricción KL previene que el modelo se desvíe demasiado de la política SFT.

El paper también introduce el enfoque de **Constitutional AI** preliminar: se usan principios explícitos (como "no ayudes a causar daño") para guiar la generación de datos de entrenamiento.

---

## Datasets utilizados

- **HH-RLHF** (Helpfulness-Harmlessness): ~170.000 pares de conversaciones con preferencias humanas. Publicado abiertamente.
- **Red teaming data**: ~40.000 intentos adversariales para probar la seguridad del modelo.
- Evaluación: benchmarks de razonamiento estándar (MMLU, etc.) para medir que el modelo no pierde capacidades.

---

## Ejemplo ilustrativo

Un anotador ve dos respuestas a "¿Cómo puedo hacer que alguien me deje dinero?"
- Respuesta A: "Podrías explicarle tu situación económica y pedirle amablemente un préstamo, ofreciendo devolvérselo con interés."
- Respuesta B: "Podría usar la manipulación emocional mencionando problemas graves para generar culpa..."

El anotador prefiere A (más helpful y harmless). El reward model aprende que A es mejor. El asistente se entrena con RL para generar respuestas más parecidas a A.

---

## Resultados principales

- El modelo RLHF-entrenado es significativamente preferido sobre el modelo SFT en evaluaciones humanas (~70% win rate).
- La seguridad (harmlessness) mejora sustancialmente con RLHF: el modelo rechaza apropiadamente solicitudes dañinas.
- Existe un trade-off helpfulness/harmlessness: modelos muy inofensivos pueden ser menos útiles. El paper cuantifica este trade-off.
- El modelo escala bien: modelos más grandes con RLHF son mejores en HHH.

---

## Ventajas respecto a trabajos anteriores

- Primera aplicación sistemática de RLHF para un asistente con objetivos múltiples (HHH).
- El dataset HH-RLHF es un recurso público importante para la comunidad.
- Establece el paradigma de entrenamiento de asistentes alineados que domina el campo hasta hoy.

---

## Trabajos previos relacionados

El paper se sitúa en el cruce entre el aprendizaje por refuerzo desde preferencias humanas y el problema de alinear LLMs para que sean útiles e inofensivos a la vez. La sección de trabajos relacionados distingue entre trabajos sobre generación guiada por retroalimentación humana, trabajos sobre seguridad y toxicidad, y trabajos sobre escalado de modelos.

- **Ouyang et al. (2022) — InstructGPT**: trabajo más cercano en espíritu; también aplica RLHF sobre GPT-3 para mejorar la utilidad, pero no incluye entrenamiento explícito de inocuidad ni estudia la tensión entre helpfulness y harmlessness.
- **Thoppilan et al. (2022) — LaMDA**: afina LLMs grandes para diálogo útil, factual y seguro mediante aprendizaje supervisado y calificaciones absolutas (no comparativas), sin explorar si impone un "impuesto de alineamiento" en capacidades.
- **Ziegler et al. (2019) — [Fine-tuning from human preferences](2019_ziegler_rlhf-finetuning.html)**: trabajo seminal que introduce RLHF para ajustar modelos de texto; sirve de base metodológica directa para la etapa de RL con PPO descrita en este paper.
- **Christiano et al. (2017) — Deep RL from Human Preferences**: propone el marco de comparaciones por pares para entrenar señales de recompensa; es el fundamento algorítmico del reward modeling empleado aquí.
- **Ganguli et al. (2022) — [Red Teaming Language Models](2022_ganguli_red-teaming.html)**: trabajo paralelo del mismo grupo que estudia cómo explotar vulnerabilidades del modelo; los datos de red teaming obtenidos alimentan directamente el entrenamiento de harmlessness descrito en este paper.
- **Lin et al. (2021) — [TruthfulQA](2021_lin_truthfulqa.html)**: benchmark de honestidad utilizado para evaluar si el entrenamiento RLHF mejora la veracidad de las respuestas; los modelos RLHF muestran mejoras notables en este benchmark.
- **Nakano et al. (2021) — WebGPT**: extiende LLMs con búsqueda web y retroalimentación humana para mejorar la fidelidad factual; complementario al enfoque de helpfulness/harmlessness de este paper.
- **Hendrycks et al. (2021) — MMLU**: benchmark de evaluación de capacidades generales empleado para demostrar que el entrenamiento HH no produce pérdida de rendimiento en tareas cognitivas estándar.
- **Bender et al. (2021) — Stochastic Parrots**: análisis de riesgos de los LLMs grandes, incluyendo toxicidad y sesgo; proporciona motivación de por qué el harmlessness training es necesario.
- **Kaplan et al. (2020) — Neural Scaling Laws**: establece las leyes de escala que motivan el estudio de tendencias con el tamaño del modelo realizado en este trabajo.

## Tags

`RLHF` `alineamiento` `asistente-AI` `preferencias-humanas` `seguridad-AI`
