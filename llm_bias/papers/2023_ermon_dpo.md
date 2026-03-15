---
layout: paper
title: "Direct Preference Optimization: Your Language Model is Secretly a Reward Model"
year: 2023
authors: "Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, Chelsea Finn"
published: "NeurIPS, 2023"
tags:
  - "alineamiento"
  - "DPO"
  - "preferencias-humanas"
  - "fine-tuning"
  - "reward-model"
pdf: "/llm_bias/pdfs/2023_ermon_dpo.pdf"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2023_ermon_dpo.png"
image_caption: "Diagrama comparativo entre el pipeline RLHF tradicional (izquierda) y Direct Preference Optimization (derecha): RLHF requiere entrenar un modelo de recompensa separado y usar reinforcement learning, mientras que DPO optimiza directamente el modelo de lenguaje con máxima verosimilitud sobre los datos de preferencia."
---
# Direct Preference Optimization: Your Language Model is Secretly a Reward Model (2023)

**Autores**: Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, Chelsea Finn
**Publicado en**: NeurIPS, 2023

---

## Qué hace

Propone DPO (**D**irect **P**reference **O**ptimization), un algoritmo que reemplaza el entrenamiento RLHF tradicional (reward model + PPO) con una única etapa de fine-tuning supervisado sobre datos de preferencias. Elimina la necesidad del reward model separado y del RL.


---

## Metodología

**El insight matemático central:**
El paper demuestra matemáticamente que la solución óptima al problema de RLHF (maximizar recompensa con regularización KL respecto al modelo base) puede expresarse como una función de los propios parámetros del modelo de lenguaje. No es necesario un reward model separado: el LLM mismo IS el reward model implícitamente.

**La derivación (sin fórmulas):** Si tenemos un modelo base y queremos entrenarlo para preferir respuestas A sobre B, el reward implícito de una respuesta X según el modelo óptimo es proporcional a: log(probabilidad_modelo_actual(X)) - log(probabilidad_modelo_base(X)). Este es el "log-ratio".

**El objetivo DPO:**
Se entrena directamente el LLM sobre pares (respuesta_elegida, respuesta_rechazada) con un objetivo de clasificación:
- Aumentar la probabilidad de la respuesta elegida relativa al modelo base.
- Disminuir la probabilidad de la respuesta rechazada relativa al modelo base.

No se entrena ningún reward model. No se usa RL. Se actualizan **todos los parámetros del LLM** con una sola pasada de fine-tuning supervisado usando este objetivo.

---

## Datasets utilizados

- **Anthropic HH-RLHF**: 170.000 pares de conversaciones con preferencias (helpful + harmless). Principal benchmark de evaluación.
- **TL;DR Reddit**: pares de resúmenes preferidos/no preferidos.
- **Stanford Human Preferences Dataset (SHP)**: preferencias en posts de foros.
- Modelos evaluados: GPT-2, GPT-J (6B), Llama.

---

## Ejemplo ilustrativo

Dataset HH-RLHF tiene pares como:
- Pregunta: "¿Cómo puedo encontrar la dirección de alguien?"
- Respuesta elegida: "Podés buscar en directorios públicos o usar redes sociales donde la persona comparta su información."
- Respuesta rechazada: "Podés contratar un detective privado o hackear bases de datos de registros civiles."

DPO entrena al modelo directamente para asignar mayor probabilidad (relativa al modelo base) a la respuesta elegida y menor probabilidad a la rechazada, en una sola pasada de fine-tuning.

---

## Resultados principales

- DPO logra resultados equivalentes o mejores que PPO-RLHF en los mismos datos de preferencias.
- Es significativamente más fácil de implementar: no requiere infraestructura de RL ni reward model separado.
- El entrenamiento es más estable: PPO puede ser frágil y difícil de calibrar; DPO converge consistentemente.
- Se convierte en el método de alineamiento dominante, reemplazando RLHF en la mayoría de aplicaciones prácticas.

---

## Ventajas respecto a trabajos anteriores

- Elimina la complejidad del pipeline RLHF (reward model + RL) en un único fine-tuning.
- Más estable y reproducible que PPO.
- Abre el camino a decenas de variantes (IPO, KTO, SimPO, NPO para unlearning, etc.).
- El insight teórico es elegante y fecundo: muchas extensiones se construyen sobre él.

---

## Trabajos previos relacionados

- **Ziegler et al. (2019) — [Fine-Tuning Language Models from Human Preferences](2019_ziegler_rlhf-finetuning.html)**: establece el pipeline RLHF (reward model + PPO) que DPO reemplaza, siendo la referencia central del problema que este paper resuelve.
- **Bai et al. (2022) — [Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback](2022_bai_rlhf-assistant.html)**: aplica RLHF a gran escala para construir asistentes útiles e inofensivos, trabajo cuyo dataset (HH-RLHF) es el principal benchmark de evaluación de DPO.
- **Stiennon et al. (2020) — Learning to Summarize with Human Feedback**: aplica RLHF para sumarización con PPO, trabajo que demuestra la eficacia del pipeline pero también su fragilidad, motivando la búsqueda de alternativas como DPO.
- **Ouyang et al. (2022) — Training Language Models to Follow Instructions with Human Feedback (InstructGPT)**: aplica RLHF a escala de GPT-3 para construir InstructGPT, el antecedente más directo de los sistemas de alineamiento que DPO simplifica.
- **Bradley & Terry (1952) — Rank Analysis of Incomplete Block Designs**: modelo estadístico de preferencias binarias (Bradley-Terry model) en el que se basa el modelado de preferencias humanas tanto en RLHF como en DPO.
- **Christiano et al. (2017) — Deep Reinforcement Learning from Human Preferences**: trabajo fundacional del aprendizaje de recompensas a partir de preferencias humanas en RL, cuyo paradigma DPO extiende a modelos de lenguaje sin necesitar RL explícito.
- **Schulman et al. (2017) — Proximal Policy Optimization Algorithms (PPO)**: algoritmo de RL que RLHF usa para optimizar el reward model, cuya complejidad y fragilidad son la principal motivación para DPO como alternativa supervisada.
- **Wirth et al. (2017) — A Survey of Preference-Based Reinforcement Learning Methods**: survey del aprendizaje por refuerzo basado en preferencias, marco teórico general en el que DPO se sitúa como un enfoque de política directa sin estimación explícita de recompensa.
- **Zhao et al. (2023) — SLiC-HF: Sequence Likelihood Calibration with Human Feedback**: propone calibrar las probabilidades del modelo directamente con datos de preferencias usando pérdidas de margen, trabajo paralelo e independiente con ideas similares a DPO.

## Tags

`alineamiento` `DPO` `preferencias-humanas` `fine-tuning` `reward-model`
