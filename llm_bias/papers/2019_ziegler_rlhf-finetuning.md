---
layout: paper
title: "Fine-Tuning Language Models from Human Preferences"
year: 2019
authors: "Daniel M. Ziegler, Nisan Stiennon, Jeffrey Wu, Tom B. Brown, Alec Radford, Dario Amodei, Paul F. Christiano, Geoffrey Irving (OpenAI)"
published: "arXiv, 2019"
tags:
  - "RLHF"
  - "alineamiento"
  - "preferencias-humanas"
  - "reward-model"
  - "PPO"
pdf: "/llm_bias/pdfs/2019_ziegler_rlhf-finetuning.pdf"
status:
  - "Leido"
image: "imgs/2019_ziegler_rlhf-finetuning.png"
image_caption: "Visualización de los datos de preferencias humanas usados en el entrenamiento RLHF, mostrando la distribución de textos y comparaciones que guían el reward model."
---
# Fine-Tuning Language Models from Human Preferences (2019)

**Autores**: Daniel M. Ziegler, Nisan Stiennon, Jeffrey Wu, Tom B. Brown, Alec Radford, Dario Amodei, Paul F. Christiano, Geoffrey Irving (OpenAI)
**Publicado en**: arXiv, 2019

---

## Qué hace

Introduce el framework de **RLHF (Reinforcement Learning from Human Feedback)** para modelos de lenguaje. Es el paper seminal que establece el paradigma de entrenar LLMs con preferencias humanas en lugar de sólo maximizar la probabilidad del corpus de texto.


---

## Metodología

El problema del entrenamiento estándar de LLMs es que sólo optimiza para que el texto generado sea probable según el corpus de entrenamiento. Pero "texto probable" no equivale a "texto de alta calidad/útil/seguro" — el corpus contiene texto malo también.

**El framework RLHF:**

**Paso 1 — Modelo base:** Un LLM (GPT-2) pre-entrenado en texto de internet.

**Paso 2 — Recolección de preferencias humanas:** Para cada prompt, se generan múltiples respuestas con el modelo base. Humanos las rankean (prefieren la respuesta A sobre B, etc.). Esto da pares (respuesta_buena, respuesta_mala).

**Paso 3 — Entrenamiento del Reward Model:** Se entrena un modelo separado (también un LLM) que recibe un texto y predice qué tan bien sería rankeado por los humanos. Este reward model aprende a predecir las preferencias humanas.

**Paso 4 — Fine-tuning con RL (PPO):** El modelo de lenguaje se fine-tunea usando Proximal Policy Optimization (PPO). En cada step:
- El modelo genera una respuesta.
- El reward model le asigna una recompensa.
- PPO actualiza los pesos del modelo para maximizar la recompensa.
- Una penalización KL evita que el modelo se desvíe demasiado del modelo base.

Los **pesos del LLM principal** se actualizan en la Paso 4. El **reward model** tiene sus propios pesos separados.

---

## Datasets utilizados

- **Books corpus**: continuaciones de texto estilísticas para el experimento de "seguir estilo".
- **TL;DR (Reddit)**: resúmenes de posts de Reddit. Los humanos prefieren resúmenes concisos y fieles.
- **CNN/DailyMail**: noticias para resumen.
- ~7.000 comparaciones humanas para el reward model de cada tarea.

---

## Ejemplo ilustrativo

Tarea: resumir posts de Reddit. Sin RLHF, GPT-2 genera resúmenes que suenan fluidos pero son largos e inventan detalles. Con RLHF, los humanos ven pares de resúmenes y señalan cuál prefieren (más conciso, más fiel al original). El reward model aprende que "conciso y fiel = bueno". El modelo RLHF aprende a hacer resúmenes concisamente y sin inventar.

---

## Resultados principales

- Los resúmenes RLHF son preferidos por humanos sobre los baselines (70-80% win rate en comparaciones).
- Los modelos RLHF aprenden a respetar las preferencias incluso para posts de temas muy diferentes a los del entrenamiento.
- Se necesitan relativamente pocas comparaciones humanas (~7K) para entrenar un reward model efectivo.
- El PPO con penalización KL es estable: el modelo no "explota" (no genera texto completamente fuera de distribución).

---

## Ventajas respecto a trabajos anteriores

- Primer paper que muestra RLHF funcionando en LLMs de lenguaje (trabajos anteriores lo habían aplicado a juegos y robótica).
- Establece el paradigma dominante para alineamiento de LLMs que perdura hasta hoy.
- La combinación reward model + PPO + KL constraint se convierte en el blueprint de GPT-4, Claude, Gemini, etc.

---

## Trabajos previos relacionados

- **Christiano et al. (2017) — Deep Reinforcement Learning from Human Preferences**: trabajo fundacional que aplica aprendizaje por refuerzo a partir de preferencias humanas en entornos simulados, siendo el precursor directo del enfoque RLHF aplicado aquí a texto.
- **Ibarz et al. (2018) — Reward Learning from Human Preferences and Demonstrations in Atari**: extiende el paradigma de Christiano a juegos Atari, demostrando la viabilidad de RLHF en entornos complejos antes de su aplicación a NLP.
- **Radford et al. (2018) — Improving Language Understanding by Generative Pre-Training (GPT)**: introduce el paradigma de preentrenamiento generativo + fine-tuning que este paper adopta como base del modelo de lenguaje.
- **Radford et al. (2019) — Language Models are Unsupervised Multitask Learners (GPT-2)**: demuestra que los modelos generativos preentrenados tienen capacidades zero-shot, justificando su uso como punto de partida para RLHF.
- **Howard & Ruder (2018) — Universal Language Model Fine-Tuning for Text Classification (ULMFiT)**: establece el paradigma de preentrenar y luego fine-tunear para NLP, sobre el que se construye este trabajo.
- **Jaques et al. (2017, 2019) — Sequence Tutor / Humanizing the Bandit**: introduce la restricción KL para evitar que el modelo fine-tuneado se aleje demasiado del modelo base, técnica central adoptada en este paper.
- **Paulus et al. (2017) — A Deep Reinforced Model for Abstractive Summarization**: aplica RL con recompensas ROUGE para sumarización, línea de trabajo que este paper supera utilizando feedback humano en lugar de métricas automáticas.
- **Ranzato et al. (2015) — Sequence Level Training with Recurrent Neural Networks**: trabajo pionero en aplicar REINFORCE a tareas de generación de lenguaje natural, cuya limitación de usar métricas algorítmicas motiva el salto a preferencias humanas.
- **Kreutzer et al. (2018) — Can Neural Machine Translation be Improved with User Feedback?**: usa aprendizaje off-policy con feedback humano en traducción automática, uno de los primeros trabajos en combinar RL y evaluación humana en NLP.
- **Yi et al. (2019) — Towards Coherent and Engaging Spoken Dialog Response Generation Using Automatic Conversation Evaluators**: aprende recompensas de humanos para fine-tunear modelos de diálogo, antecedente directo del enfoque de este paper en tareas de continuación estilística.

## Tags

`RLHF` `alineamiento` `preferencias-humanas` `reward-model` `PPO`
