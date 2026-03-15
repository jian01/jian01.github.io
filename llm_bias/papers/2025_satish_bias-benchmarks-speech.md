---
layout: paper
title: "Do Bias Benchmarks Generalise? Evidence from Voice-based Evaluation of Gender Bias in SpeechLLMs"
year: 2025
authors: "S. Satish, Gustav Eje Henter, Éva Székely"
published: "arXiv, 2025"
tags:
  - "benchmark"
  - "sesgo-de-género"
  - "speech-LLM"
  - "sesgo-acústico"
  - "evaluación"
pdf: "/llm_bias/pdfs/2025_satish_bias-benchmarks-speech.pdf"
method_type: "Benchmark / Dataset"
datasets:
  - "WinoBias"
  - "StereoSet"
status:
  - "Irrelevante"
  - "Leido"
image: "imgs/2025_satish_bias-benchmarks-speech.png"
image_caption: "Mapa de calor que compara el rendimiento de distintos benchmarks de sesgo de género aplicados a SpeechLLMs, donde cada celda representa el nivel de sesgo detectado (verde = menos sesgo, rojo = más sesgo)."
opinion: "<WIP>"
---
# Do Bias Benchmarks Generalise? Evidence from Voice-based Evaluation of Gender Bias in SpeechLLMs (2025)

**Autores**: S. Satish, Gustav Eje Henter, Éva Székely
**Publicado en**: arXiv, 2025
**Tipo de método**: Benchmark / Dataset

---

## Qué hace

Estudia si los benchmarks de sesgo diseñados para texto se transfieren a modelos de lenguaje de voz (SpeechLLMs). Encuentra que los patrones de sesgo de género en el dominio de texto no generalizan al dominio de audio, revelando sesgos adicionales introducidos por características acústicas de la voz.


---

## Metodología

Los SpeechLLMs procesan audio directamente (no sólo transcripciones de texto). Esto significa que tienen acceso a características de la voz del hablante: tono (pitch), velocidad, acento, timbre. Estas características están correlacionadas con el género del hablante en los datos de entrenamiento.

**Adaptación de benchmarks de texto a voz:**
Se toman benchmarks existentes (WinoBias, StereoSet) y se convierten a audio usando síntesis de voz (TTS) con voces masculinas y femeninas. Se estudia si el LLM de voz responde de forma diferente según la voz del hablante, independientemente del contenido del texto.

**Experimento principal:**
La misma pregunta textual se presenta en dos versiones:
1. Voz sintetizada masculina.
2. Voz sintetizada femenina.

Se mide si el SpeechLLM da respuestas diferentes. Si la respuesta varía sólo por el género de la voz (no por el contenido), hay sesgo acústico.

**Análisis de características acústicas:**
Se estudia qué características de la voz (pitch, velocidad, acento) correlacionan más con las diferencias en las respuestas del modelo.

---

## Datasets utilizados

- **WinoBias** adaptado a audio: 600 frases de WinoBias convertidas a audio con TTS.
- **StereoSet** adaptado: 500 frases estereotipadas en audio.
- Voces TTS: Microsoft Azure TTS, Google TTS (múltiples voces masculinas/femeninas).
- Evaluado en Whisper (con LLM) y otros SpeechLLMs.

---

## Ejemplo ilustrativo

La misma pregunta "¿Quién debería ser el director del hospital?" con contexto ambiguo se presenta:
- En voz femenina de alta frecuencia (pitch alto): el modelo tiende a sugerir respuestas más relacionadas con personal de apoyo.
- En voz masculina de baja frecuencia (pitch bajo): el modelo tiende a sugerir directores/as con más autoridad.

Este sesgo no aparece en la evaluación textual de los mismos benchmarks — es un sesgo exclusivamente acústico.

---

## Resultados principales

- Los sesgos de género en texto NO predicen consistentemente los sesgos en audio: correlación sólo del 30-40%.
- Aparecen sesgos nuevos basados en pitch: voces de pitch bajo reciben respuestas de mayor autoridad.
- Los sesgos de acento son más pronunciados que los de pitch: acentos no nativos reciben respuestas de menor expertise percibido.
- Los benchmarks de texto sobreestiman la equidad de género en SpeechLLMs.

---

## Ventajas respecto a trabajos anteriores

- Primer estudio sistemático de transferencia de benchmarks de sesgo del dominio texto al dominio audio.
- Revela una clase entera de sesgos acústicos no capturados por benchmarks de texto.
- Motiva el desarrollo de benchmarks de sesgo específicos para el dominio de la voz.

---

## Trabajos previos relacionados

- **Nadeem et al. (2021) — StereoSet: Measuring stereotypical bias in pretrained language models**: benchmark de referencia en texto cuya extensión oral (Spoken StereoSet) es uno de los dos benchmarks MCQA utilizados en los experimentos de este trabajo; ver [2021_nadeem_stereoset.md](2021_nadeem_stereoset.html).
- **Parrish et al. (2021) — BBQ: A hand-built bias benchmark for question answering**: diseño de benchmark en formato MCQA para sesgo en QA, cuya estructura inspira el diseño de la suite SAGE MCQA propuesta en el artículo; ver [2021_parrish_bbq.md](2021_parrish_bbq.html).
- **Xu et al. (2025) — BiasEdit**: método de debiasing mediante edición de modelos en SpeechLLMs, uno de los trabajos de mitigación que motiva la pregunta sobre transferencia cross-task que este artículo investiga; ver [2025_xu_biasedit.md](2025_xu_biasedit.html).
- **Gehman et al. (2020) — RealToxicityPrompts**: benchmark para evaluar toxicidad en generación de texto libre, referente metodológico para el diseño de evaluaciones long-form más allá de MCQA; ver [2020_gehman_realtoxicityprompts.md](2020_gehman_realtoxicityprompts.html).
- **Sap et al. (2020) — Social Bias Frames**: marco conceptual para entender cómo el sesgo se manifiesta en generación libre, motivando las evaluaciones long-form de la suite SAGE-LF; ver [2020_sap_social-bias-frames.md](2020_sap_social-bias-frames.html).
- **Meade et al. (2021) — An empirical survey of debiasing techniques**: encuesta sobre técnicas de debiasing que sirve de referencia para entender las limitaciones de los métodos MCQA-only en evaluar la transferibilidad real del debiasing; ver [2021_meade_debiasing-survey.md](2021_meade_debiasing-survey.html).
- **Gallegos et al. (2024) — Self-debiasing large language models**: método de debiasing en tiempo de inferencia cuya eficacia cross-task es análoga a la pregunta que este artículo plantea para SpeechLLMs; ver [2024_gallegos_self-debiasing.md](2024_gallegos_self-debiasing.html).

## Tags

`benchmark` `sesgo-de-género` `speech-LLM` `sesgo-acústico` `evaluación`
