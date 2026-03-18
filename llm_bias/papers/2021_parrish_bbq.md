---
layout: paper
title: "BBQ: A hand-built bias benchmark for question answering"
year: 2021
date_published: "2021-10-15"
authors: "Alicia Parrish, Angelica Chen, Nikita Nangia, Vishakh Padmakumar, Jason Phang, Jana Thompson, Phu Mon Htut, Sam Bowman"
published: "ACL Findings, 2022"
tags:
  - "benchmark"
  - "sesgo-social"
  - "QA"
  - "estereotipos"
  - "evaluación"
pdf: "/llm_bias/pdfs/2021_parrish_bbq.pdf"
method_type: "Benchmark / Dataset"
datasets:
  - "BBQ"
status:
  - "Leido"
image: "imgs/2021_parrish_bbq.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---

## Qué hace

Crea BBQ (**B**ias **B**enchmark for **Q**A), un dataset de 58.492 ejemplos de QA con opción múltiple que mide si los LLMs usan estereotipos sociales para responder preguntas cuando la respuesta correcta es "indeterminada". Cubre 9 dimensiones de sesgo social.


---

## Metodología

BBQ evalúa el sesgo de manera inteligente: en lugar de preguntar directamente "¿es X grupo Y?", crea situaciones ambiguas donde el modelo debería responder "no puedo saber" pero en su lugar usa estereotipos.

**Diseño del dataset:**
Cada ejemplo tiene dos versiones:
1. **Contexto ambiguo**: no hay suficiente información para responder. Ej: "Alex y Jordan estaban hablando sobre quién debería ser el nuevo gerente."
2. **Contexto desambiguado**: se añade información que permite una respuesta correcta. Ej: "Alex y Jordan estaban hablando sobre quién debería ser el nuevo gerente. Alex tiene 15 años de experiencia en liderazgo y es el candidato más calificado."

Pregunta para ambos: *"¿Quién debería ser el gerente?"*

En el contexto ambiguo, la respuesta correcta es "Indeterminado". Pero si el modelo responde "Jordan" porque Jordan tiene un nombre más "ejecutivo" o "masculino", eso revela sesgo.

**Las 9 dimensiones:** Edad, discapacidad, género, identidad de género, origen nacional, raza/etnia, religión, orientación sexual, y apariencia física/peso.

---

## Datasets utilizados

- **BBQ**: 58.492 ejemplos de opción múltiple (3 opciones: dos identidades + "Indeterminado").
- Construido manualmente por los autores con control de calidad exhaustivo.
- Evaluado en GPT-2, DeBERTa, UnifiedQA, y otros modelos.

---

## Ejemplo ilustrativo

Contexto ambiguo: *"Dos pacientes esperan al médico. Uno es hombre y el otro es mujer."*
Pregunta: *"¿Cuál de los dos es el médico?"*
Opciones: a) El hombre, b) La mujer, c) No se puede saber.

Respuesta correcta: c) No se puede saber.
Sesgo revelado si el modelo responde a) — usa el estereotipo de que los médicos son hombres.

Contexto desambiguado: *"Dos pacientes esperan al médico. La mujer tiene una bata blanca y un estetoscopio."*
Ahora la respuesta correcta es b) La mujer.

---

## Resultados principales

- GPT-3 muestra sesgo en el 77% de las preguntas ambiguas: prefiere sistemáticamente a grupos privilegiados como respuesta.
- En el contexto desambiguado, la mayoría de modelos logran >80% accuracy, mostrando que el sesgo no es falta de comprensión sino uso activo de estereotipos.
- Los sesgos más fuertes: género en ocupaciones y orientación sexual.
- Modelos más grandes muestran menos sesgo que modelos pequeños (el opuesto de TruthfulQA).

---

## Ventajas respecto a trabajos anteriores

- La distinción ambiguo/desambiguado permite distinguir sesgo real de falta de comprensión.
- Las 9 dimensiones ofrecen cobertura mucho más amplia que benchmarks anteriores.
- El diseño de QA con opción múltiple facilita la evaluación automática.

---

## Trabajos previos relacionados

BBQ organiza los trabajos previos en tres líneas: (1) medición de sesgo en representaciones y modelos NLP en general, (2) sesgo en tareas de resolución de correferencia y detección de hate speech, y (3) sesgo específicamente en QA. El paper se distingue por ser el primer dataset de QA diseñado para medir sesgo a través de contextos ambiguos vs. desambiguados.

- **Caliskan et al. (2017) — Semantics Derived Automatically from Language Corpora Contain Human-like Biases (WEAT)**: test de asociación de palabras que demuestra que los embeddings codifican sesgos humanos; punto de partida conceptual para medir sesgo en modelos NLP.
- **Sap et al. (2020) — [Social Bias Frames](2020_sap_social-bias-frames.html)**: coloca una gama de sesgos en marcos de inferencia para vincular el hate speech potencial con el sesgo del mundo real invocado; citado como trabajo que inspira el enfoque de BBQ de conectar comportamiento del modelo con daño real.
- **Blodgett et al. (2020) — Language (Technology) is Power: A Critical Survey of "Bias" in NLP**: señala que los estudios de sesgo en NLP usan definiciones muy variadas de "sesgo"; BBQ se alinea explícitamente con su definición de daños representacionales.
- **Crawford (2017) — The Trouble with Bias**: define daños representacionales como aquellos que ocurren cuando los sistemas refuerzan la subordinación de grupos por identidad; BBQ adopta explícitamente esta definición.
- **Rudinger et al. (2018) — Gender Bias in Coreference Resolution: Evaluation and Debiasing Methods**: mide sesgo de género en resolución de correferencia usando pronombres, trabajo directamente relacionado en la evaluación de sesgos de género-ocupación en tareas downstream.
- **Zhao et al. (2018) — Gender Bias in Coreference Resolution: Evaluation and Debiasing Methods**: junto a Rudinger et al., trabajo de referencia sobre sesgo de género en correferencia, citado como antecedente de la evaluación de sesgo en tareas de NLP.
- **Li et al. (2020) — UnQover: Scrutinizing and Benchmarking Questions Under-Constrained for NLP**: único dataset previo de BBQ para medir sesgo específicamente en QA, usando preguntas subespecificadas y comparando probabilidades del modelo en lugar de predicciones de salida.
- **Röttger et al. (2021) — HateCheck**: investiga puntos de fallo de clasificadores de hate speech a través de grupos objetivo, citado como trabajo relacionado en la medición de diferencias de rendimiento por grupo demográfico.

## Tags

`benchmark` `sesgo-social` `QA` `estereotipos` `evaluación`
