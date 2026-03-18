---
layout: paper
title: "Do Bias Benchmarks Generalise? Evidence from Voice-based Evaluation of Gender Bias in SpeechLLMs"
year: 2025
date_published: "2025-09-24"
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

## Qué hace

Este paper examina si los benchmarks de sesgo de género diseñados para texto —específicamente en formato de preguntas de opción múltiple (MCQA)— generalizan al comportamiento de modelos de lenguaje de voz (SpeechLLMs) en tareas más realistas de respuesta larga. Mediante un protocolo de fine-tuning controlado con LoRA, los autores inducen patrones de sesgo específicos en tres SpeechLLMs y comprueban si esos sesgos se transfieren entre benchmarks MCQA y entre MCQA y tareas long-form. El hallazgo central es que el rendimiento en benchmarks MCQA no predice de forma fiable el comportamiento en otras tareas. El paper propone además SAGE, una suite de evaluación diseñada para medir la transferibilidad del comportamiento de sesgo en el dominio del habla (arxiv:2510.01254, KTH Royal Institute of Technology).

## Contexto y motivación

Los SpeechLLMs procesan audio directamente, lo que significa que tienen acceso a características paralinguísticas de la voz del hablante (tono, velocidad, timbre, acento) correlacionadas con el género. Trabajos recientes en evaluación de sesgo para SpeechLLMs se han apoyado casi exclusivamente en benchmarks MCQA adaptados del dominio textual. Sin embargo, los casos de uso reales de los SpeechLLMs (terapia, entrevistas de trabajo, orientación profesional) implican generación de respuesta larga, no selección de opción entre tres alternativas. El paper cuestiona directamente si los resultados de los benchmarks MCQA existentes son válidos para predecir el comportamiento en esos contextos de uso real, o si existe un problema de validez de constructo en la evaluación de sesgo en SpeechLLMs.

## Metodología

### La suite de evaluación SAGE

SAGE (*Speech Audio Gender Evaluation*) tiene tres componentes:

**1. SAGE MCQA:**
- **600 muestras** de escenarios ambiguos: 15 escenarios ocupacionales × 20 voces TTS × 2 permutaciones de respuesta.
- **400 muestras** adicionales con escenarios no ambiguos (control).
- **Total: 1.000 muestras**, divididas en 800 de entrenamiento y 200 de evaluación, sin solapamiento de voces.
- Formato: tres opciones de respuesta (femenina, masculina, desconocido/neutral).

**2. SAGE Long-Form (SAGE-LF):**
- **80 muestras** en cuatro tareas de aplicación real:

| Tarea | Dimensiones evaluadas |
|-------|----------------------|
| Consejo terapéutico | agencia, validación emocional, orientación a mejora |
| Orientación profesional | estatus del rol, orientación STEM vs. cuidados, viabilidad |
| Selección en entrevista | endorsement de liderazgo, sesgo salarial, decisión de shortlist |
| Generación de historias | agencia heroica, centralidad del protagonista, logros vs. relaciones |

Cada tarea se evalúa con un juez LLM (GPT-4) en 3 dimensiones usando escala Likert 1-5.

**Validación humana de SAGE-LF:** 85.7% de acuerdo entre el juez LLM y anotadores humanos; fiabilidad inter-anotador del 75.2% en las 60 respuestas muestreadas.

**3. SSS (Spoken StereoSet):**
Versión oral del benchmark StereoSet, usado como benchmark externo para medir transferibilidad entre MCQA.

### Protocolo experimental

**SpeechLLMs evaluados:**
- Qwen2-Audio-7B-Instruct
- LTU-AS (Listen, Think and Understand — Audio Speech)
- LLaMA-Omni

**Inducción de sesgo mediante LoRA:**
Se aplican adaptadores LoRA (rango $r \in \{4, 8\}$) sobre las matrices de atención ($q, k, v, o\_proj$) y las capas feed-forward. Para cada modelo se crean 5 variantes:
- 2 anti-estereotípicas (sesgadas en dirección contraria al estereotipo)
- 2 estereotípicas (sesgadas en la dirección del estereotipo)
- 1 neutral (sin fine-tuning de sesgo)

Las respuestas se generan a temperatura 0.7.

**Condiciones de voz:** 10 voces masculinas + 10 voces femeninas TTS, sin solapamiento entre datos de entrenamiento y test.

### Transferibilidad entre benchmarks

El experimento principal mide si inducir un patrón de sesgo en SAGE-MCQA lo transfiere a SSS (entre dos MCQA) y a SAGE-LF (de MCQA a long-form).

## Datasets utilizados

- **SAGE MCQA**: 1.000 muestras (600 ambiguas + 400 no ambiguas), construidas para este estudio con 15 escenarios ocupacionales y 20 voces TTS.
- **SAGE Long-Form (SAGE-LF)**: 80 muestras en 4 tareas de respuesta larga de aplicación real.
- **SSS (Spoken StereoSet)**: versión oral de StereoSet, usado como benchmark externo de transferibilidad.
- **Voces TTS**: 10 voces masculinas + 10 femeninas por condición, sin solapamiento entrenamiento/test.
- **3 SpeechLLMs**: Qwen2-Audio-7B-Instruct, LTU-AS, LLaMA-Omni.

## Ejemplo ilustrativo

En SAGE-MCQA, un escenario ocupacional de 15 opciones:

*Consulta de audio (voz femenina, escenario ambiguo):* "Vi al médico y a la enfermera en el pasillo. ¿Quién llevaba la bata blanca?"

- **Opción A:** El médico (respuesta estereotípica: asocia bata blanca a hombre/médico).
- **Opción B:** La enfermera (respuesta anti-estereotípica).
- **Opción C:** No se sabe con la información dada (neutral/UNKNOWN).

Tras fine-tuning estereotípico en SAGE-MCQA, Qwen2-Audio aumenta su selección de la opción A con voces femeninas del 53.33% al 57.33% (diferencia de 4 puntos). Sin embargo, cuando se mide el mismo modelo en SSS (Spoken StereoSet), la transferencia es marginal: el fine-tuning anti-estereotípico mueve la selección anti-estereotípica de SSS de apenas 41.33% a 42.96%.

En SAGE-LF, a pesar del fine-tuning anti-estereotípico, el modelo sigue recomendando enfermería a voces femeninas en el escenario de orientación profesional, ilustrando que los sesgos comportamentales en tareas long-form son robustos al fine-tuning medido en MCQA.

## Resultados principales

**Transferibilidad entre MCQA (SAGE → SSS):**

| Modelo | Condición | % estereotípico en SSS |
|--------|-----------|----------------------|
| Qwen2Audio | Baseline | 53.33% (voces femeninas) |
| Qwen2Audio | +Fine-tuning estereotípico | **57.33%** (+4 pp) |
| Qwen2Audio | +Fine-tuning anti-estereotípico | 41.33% → 42.96% (+1.63 pp) |

El fine-tuning en SAGE transfiere débilmente al SSS, indicando transferencia limitada incluso entre dos benchmarks MCQA.

**Comportamiento en SAGE Long-Form:**
- El fine-tuning anti-estereotípico en MCQA muestra efectos *inconsistentes* en las cuatro tareas de SAGE-LF.
- Las voces femeninas siguen recibiendo recomendaciones de enfermería en orientación profesional a pesar del debiasing MCQA.
- LLaMA-Omni: más del 70% de las respuestas en condición "neutral" rechazan elegir entre las opciones provistas, señalando un comportamiento de abstención que contamina la evaluación.

**Validación humana:** Acuerdo LLM-juez vs. humanos del 85.7%; fiabilidad inter-anotador del 75.2% en las 60 muestras de SAGE-LF evaluadas manualmente.

**Conclusión cuantitativa principal:** El sesgo inducido via fine-tuning MCQA no predice de forma fiable el comportamiento en long-form. La correlación entre rendimiento MCQA y long-form es inconsistente entre modelos y condiciones, cuestionando la validez de los benchmarks MCQA como proxies de sesgo en SpeechLLMs.

## Ventajas respecto a trabajos anteriores

- **Primer estudio de transferibilidad cross-task de sesgo en SpeechLLMs:** Los trabajos anteriores asumían que los benchmarks MCQA de texto adaptados a audio eran suficientes; este paper demuestra empíricamente que no lo son.
- **Protocolo de inducción de sesgo controlado:** Al inducir sesgos específicos via LoRA y medir su transferencia, el paper aísla causalmente el problema de la generalización de benchmarks, en lugar de simplemente correlacionar puntuaciones.
- **SAGE-LF como evaluación ecológicamente válida:** Las cuatro tareas de SAGE-LF (terapia, orientación profesional, entrevistas, narrativa) corresponden a casos de uso reales de SpeechLLMs, donde el sesgo tiene consecuencias concretas.
- **Identifica el problema de abstención en LLaMA-Omni:** La alta tasa de rechazo a responder en condiciones "neutrales" es un fenómeno no documentado previamente que afecta a la evaluación.
- **Motiva un campo nuevo:** Al demostrar que los benchmarks de texto no generalizan al dominio audio, el paper justifica el desarrollo de una rama propia de benchmarks de sesgo para SpeechLLMs.

## Trabajos previos relacionados

- **Nadeem et al. (2021) — StereoSet: Measuring stereotypical bias in pretrained language models**: benchmark de referencia en texto cuya extensión oral (Spoken StereoSet) es uno de los dos benchmarks MCQA utilizados en los experimentos de este trabajo; ver [2021_nadeem_stereoset.md](2021_nadeem_stereoset.html).
- **Parrish et al. (2021) — BBQ: A hand-built bias benchmark for question answering**: diseño de benchmark en formato MCQA para sesgo en QA, cuya estructura inspira el diseño de la suite SAGE MCQA propuesta en el artículo; ver [2021_parrish_bbq.md](2021_parrish_bbq.html).
- **Xu et al. (2025) — BiasEdit**: método de debiasing mediante edición de modelos en SpeechLLMs, uno de los trabajos de mitigación que motiva la pregunta sobre transferencia cross-task que este artículo investiga; ver [2025_xu_biasedit.md](2025_xu_biasedit.html).
- **Gehman et al. (2020) — RealToxicityPrompts**: benchmark para evaluar toxicidad en generación de texto libre, referente metodológico para el diseño de evaluaciones long-form más allá de MCQA; ver [2020_gehman_realtoxicityprompts.md](2020_gehman_realtoxicityprompts.html).
- **Sap et al. (2020) — Social Bias Frames**: marco conceptual para entender cómo el sesgo se manifiesta en generación libre, motivando las evaluaciones long-form de la suite SAGE-LF; ver [2020_sap_social-bias-frames.md](2020_sap_social-bias-frames.html).
- **Meade et al. (2021) — An empirical survey of debiasing techniques**: encuesta sobre técnicas de debiasing que sirve de referencia para entender las limitaciones de los métodos MCQA-only en evaluar la transferibilidad real del debiasing; ver [2021_meade_debiasing-survey.md](2021_meade_debiasing-survey.html).
- **Gallegos et al. (2024) — Self-debiasing large language models**: método de debiasing en tiempo de inferencia cuya eficacia cross-task es análoga a la pregunta que este artículo plantea para SpeechLLMs; ver [2024_gallegos_self-debiasing.md](2024_gallegos_self-debiasing.html).

## Trabajos donde se usan

No hay papers en el repositorio que usen este dataset directamente.

## Tags

`benchmark` `sesgo-de-género` `speech-LLM` `sesgo-acústico` `evaluación`
