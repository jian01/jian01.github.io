---
layout: paper
title: "RealToxicityPrompts: Evaluating Neural Toxic Degeneration in Language Models"
year: 2020
date_published: "2020-09-24"
authors: "Samuel Gehman, Suchin Gururangan, Maarten Sap, Yejin Choi, Noah A. Smith"
published: "EMNLP Findings, 2020"
tags:
  - "benchmark"
  - "toxicidad"
  - "seguridad-AI"
  - "LLM"
  - "evaluación"
pdf: "/llm_bias/pdfs/2020_gehman_realtoxicityprompts.pdf"
method_type: "Benchmark / Dataset"
datasets:
  - "RealToxicityPrompts"
  - "Perspective API"
status:
  - "Leido"
image: "imgs/2020_gehman_realtoxicityprompts.png"
image_caption: "Diagrama de arquitectura de una red neuronal profunda, ilustrando el tipo de modelos de lenguaje evaluados en el benchmark RealToxicityPrompts para medir la degeneración tóxica en generación de texto."
opinion: "<WIP>"
---## Qué hace

Crea RealToxicityPrompts, un benchmark de 100.000 prompts extraídos de la web que pueden inducir generaciones tóxicas en LLMs. Evalúa sistemáticamente la degeneración tóxica de modelos y prueba múltiples estrategias de mitigación.


---

## Metodología

**Construcción del dataset:**
Los 100.000 prompts se extrajeron de OpenWebText (texto de páginas web de alta calidad según Reddit). Para cada fragmento de texto, se tomó la primera mitad como "prompt" y la segunda mitad como "continuación". Se calculó la toxicidad de cada fragmento completo usando **Perspective API** (un clasificador de toxicidad desarrollado por Google/Jigsaw).

El dataset incluye prompts con diversa toxicidad:
- ~50% prompts no tóxicos (que aun así pueden generar continuaciones tóxicas).
- ~50% prompts tóxicos (que casi garantizadamente generan continuaciones tóxicas).

**Evaluación:** Para cada modelo evaluado (GPT-2, various GPT sizes, CTRL, etc.), se generan 25 continuaciones por prompt y se mide:
- **Expected Maximum Toxicity**: el máximo de toxicidad esperado entre las 25 continuaciones.
- **Toxicity Probability**: qué fracción de las 25 continuaciones tiene toxicidad > 0.5.

**Mitigaciones evaluadas:**
- PPLM (Plug and Play Language Model): steering de activaciones internas.
- Domain-adaptive pretraining en texto no tóxico.
- Prompting con prefijos de "safe" examples.

---

## Datasets utilizados

- **RealToxicityPrompts**: 100.000 prompts de OpenWebText con scores de toxicidad.
- **Perspective API**: usado para medir toxicidad (6 categorías: toxicidad, obscenidad, insulto, amenaza, lenguaje de odio, identidad de ataque).
- Generaciones evaluadas con GPT-2 (117M-1.5B), GPT-3, CTRL, y otros.

---

## Ejemplo ilustrativo

Prompt aparentemente inocente: *"El capitán del equipo corrió hacia..."* → GPT-2 continúa: *"...los manifestantes y comenzó a golpearlos, llamándoles..."* (altamente tóxico). Esto ilustra que incluso prompts sin toxicidad aparente pueden desencadenar generaciones tóxicas en LLMs. Otro ejemplo: *"Wikipedia describes whiteness as..."* → GPT-2 genera texto con lenguaje de odio racial.

---

## Resultados principales

- Todos los modelos evaluados tienen una probabilidad no trivial de generar texto tóxico, incluso con prompts no tóxicos.
- GPT-2 generó al menos una continuación con toxicidad > 0.5 en el 87% de los prompts no tóxicos cuando se muestrearon 25 continuaciones.
- Las mitigaciones existentes reducen la toxicidad pero a costo de pérdida de diversidad/fluidez.
- Los modelos más grandes no son necesariamente menos tóxicos.

---

## Ventajas respecto a trabajos anteriores

- Primer dataset a gran escala usando prompts naturales de la web en lugar de prompts artificialmente diseñados para ser tóxicos.
- Establece el protocolo de evaluación de toxicidad con múltiples muestras que se convierte en estándar.
- Revela la "degeneración tóxica" como un problema inherente a los LLMs entrenados en texto web no filtrado.

---

## Trabajos previos relacionados

RealToxicityPrompts se sitúa entre la literatura de sesgo en modelos de lenguaje preentrenados y la de control de generación de texto. Los autores señalan que la mayoría del trabajo previo sobre toxicidad usaba prompts artificiales o se centraba en encoders, no en modelos autoregresivos generativos.

- **May et al. (2019) — On Measuring Social Biases in Sentence Encoders**: extiende WEAT a encoders contextuales (SEAT), representando la línea de trabajo sobre sesgo en embeddings que RealToxicityPrompts complementa estudiando generación en lugar de representaciones.
- **Sheng et al. (2019) — The Woman Worked as a Babysitter: On Biases in Language Generation**: usa 60 prompts plantilla con menciones de identidades mayoritarias/minoritarias para estudiar sesgos sociales en generación; trabajo más directamente relacionado que RealToxicityPrompts escala a 100K prompts naturales.
- **Wallace et al. (2019) — Universal Adversarial Triggers for Attacking and Analyzing NLP**: encuentran prompts adversariales nonsense que desencadenan generaciones tóxicas en GPT-2; RealToxicityPrompts amplía esto usando prompts naturales extraídos de la web.
- **Holtzman et al. (2020) — The Curious Case of Neural Text Degeneration**: estudia problemas de incoherencia y repetitividad en LMs autoregresivos, citado como trabajo previo sobre degeneración en generación de texto.
- **Dathathri et al. (2020) — Plug and Play Language Models (PPLM)**: método de steering de activaciones internas para controlar el estilo y contenido de generación, evaluado como una de las mitigaciones de toxicidad en RealToxicityPrompts.
- **Keskar et al. (2019) — CTRL: A Conditional Transformer Language Model**: modelo con tokens de control para dirigir el estilo de generación, evaluado como baseline y mitigación en el paper.
- **Zhang et al. (2018) — Conversations Gone Awry: Detecting Early Signs of Conversational Failure**: estudia patrones conversacionales que derivan en comportamiento antisocial, citado como inspiración para el enfoque de RealToxicityPrompts.
- **Ziegler et al. (2019) — [Fine-Tuning Language Models from Human Preferences](2019_ziegler_rlhf-finetuning.html)**: RLHF para controlar estilo de generación, citado como dirección relevante para mitigar toxicidad.

## Tags

`benchmark` `toxicidad` `seguridad-AI` `LLM` `evaluación`
