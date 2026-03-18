---
layout: paper
title: "HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models"
year: 2023
date_published: "2023-05-19"
authors: "Junyi Li, Xiaoxue Cheng, Xin Zhao, Jian-Yun Nie, Ji-Rong Wen"
published: "EMNLP, 2023"
tags:
  - "benchmark"
  - "alucinaciones"
  - "QA"
  - "resumen"
  - "LLM"
pdf: "/llm_bias/pdfs/2023_li_halueval.pdf"
method_type: "Benchmark / Dataset"
datasets:
  - "HotpotQA"
  - "CNN"
  - "DailyMail"
  - "OpenDialKG"
status:
  - "Leido"
image: "imgs/2023_li_halueval.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---

## Qué hace

HaluEval construye un benchmark de 35.000 muestras alucinadas/normales para evaluar la capacidad de los LLMs de reconocer alucinaciones en tres tareas: QA, resumen automático y diálogo. Utiliza un proceso de generación automática con ChatGPT (30.000 muestras) y anotación humana (5.000 muestras) para producir pares de texto correcto/alucinado de alta calidad. El paper también estudia empíricamente qué patrones de alucinación existen, cuáles son más difíciles de detectar y qué estrategias mitigan el problema.

## Contexto y motivación

Los LLMs como ChatGPT generan contenido que suena plausible pero es factualmente incorrecto. Antes de HaluEval, era difícil evaluar alucinaciones a escala porque crear manualmente pares "respuesta correcta / respuesta alucinada" es costoso. Los benchmarks existentes (TruthfulQA, BEGIN) se limitaban a tareas individuales o eran pequeños. Además, no había un análisis sistemático de qué *tipos* de alucinación cometen los modelos ni en qué dominios temáticos fallan más.

## Metodología

### Construcción del dataset

El dataset se construye con dos métodos complementarios:

**1. Generación automática con ChatGPT (30.000 muestras):**

Se utiliza un proceso de *sampling-then-filtering* en dos etapas:
- **Sampling diverso:** Se generan candidatos alucinados mediante dos estrategias: *one-pass* (instrucción directa a ChatGPT para que genere una versión alucinada de la respuesta correcta) y *conversacional* (diálogo iterativo para refinar la alucinación).
- **Filtrado:** Se seleccionan los candidatos más plausibles pero incorrectos, descartando alucinaciones obvias o gramaticalmente defectuosas.

Las instrucciones a ChatGPT le piden generar alucinaciones que sean: fluidas y gramaticalmente correctas, plausibles en apariencia pero con información errónea, y del tipo específico de error que los LLMs cometen (inventar fechas, confundir personas, añadir citas falsas).

**2. Anotación humana (5.000 muestras):**

Se parte del dataset Alpaca (52K instrucciones) y se filtran 5.000 consultas donde ChatGPT genera respuestas con mayor divergencia entre sí (baja similitud coseno entre las tres respuestas generadas). Estas son las consultas más propensas a alucinación.

- **Anotadores:** 3 anotadores humanos por muestra, con estrategia de votación mayoritaria.
- **Acuerdo inter-anotador:** $\kappa = 0.811$ (Fleiss's Kappa), considerado excelente.
- **Categorías de anotación:** no-verificable, no-factual, irrelevante.

### Distribución de tareas

| Tarea | Muestras | Fuente base | Tipos de alucinación |
|-------|----------|-------------|---------------------|
| QA | 10.000 | HotpotQA | Comprensión, factualidad, especificidad, inferencia |
| Diálogo | 10.000 | OpenDialKG | Extrínseca-suave, extrínseca-dura, extrínseca-agrupada |
| Resumen | 10.000 | CNN/DailyMail | Factual, no-factual, intrínseca |
| Consultas generales | 5.000 | Alpaca (anotadas por humanos) | No-verificable, no-factual, irrelevante |

**Total: 35.000 muestras.**

### Evaluación de modelos

Los modelos se evalúan en la tarea de **reconocimiento binario de alucinaciones**: dado un texto, identificar si contiene una alucinación o no. Se mide *accuracy* sobre el conjunto de test.

## Datasets utilizados

- **HotpotQA**: preguntas multi-hop de Wikipedia (base para la tarea QA, 10.000 muestras).
- **CNN/DailyMail**: artículos de noticias con resúmenes de referencia (base para la tarea de resumen, 10.000 muestras).
- **OpenDialKG**: diálogos grounded en base de conocimiento (base para la tarea de diálogo, 10.000 muestras).
- **Alpaca**: 52K instrucciones de fine-tuning, filtradas a 5.000 consultas para anotación humana.
- **ChatGPT** (gpt-3.5-turbo): utilizado como generador automático de alucinaciones.

## Ejemplo ilustrativo

En la tarea de QA (basada en HotpotQA), una pregunta multi-hop real del benchmark:

- **Documento fuente:** *"Marie Curie ganó el Premio Nobel de Química en 1911 por el descubrimiento del radio y el polonio."*
- **Respuesta correcta:** "Marie Curie ganó el Premio Nobel de Química en 1911."
- **Respuesta alucinada (generada por ChatGPT):** "Marie Curie ganó el Premio Nobel de Física en 1911 por el descubrimiento del radio y el polonio."

Este ejemplo ilustra el tipo de alucinación más difícil: la información incorrecta (Nobel de Física) es verdadera para otro contexto temporal (1903), lo que hace que la alucinación sea particularmente engañosa para los modelos evaluadores.

En los análisis de causas, el paper encontró que más de la mitad de los errores de ChatGPT se concentran en los patrones de alucinación *comprensión*, *extrínseca-suave* y *factual* — es decir, alucinaciones que son factualmente correctas en abstracto pero contextualmente inconsistentes con la fuente.

## Resultados principales

**Accuracy de reconocimiento de alucinaciones (%):**

| Modelo | QA | Diálogo | Resumen | General |
|--------|----|---------|---------|---------|
| ChatGPT | 62.59 | 72.40 | 58.53 | 79.44 |
| Claude 2 | 69.78 | 64.73 | 57.75 | 75.00 |
| GPT-3 | 49.21 | 50.02 | 51.23 | 72.72 |
| Llama 2 | 49.60 | 43.99 | 49.55 | 20.46 |
| Alpaca | 6.68 | 17.55 | 20.63 | 9.54 |

Puntos clave:
- Los LLMs de mayor tamaño (ChatGPT, Claude 2) quedan en el rango 58-79%, lejos del 100%.
- El resumen es la tarea más difícil de todas (ChatGPT sólo alcanza 58.53%).
- Los modelos open-source pequeños (Llama 2, Alpaca) están en o por debajo del azar (~50%).
- ChatGPT genera alucinaciones en aproximadamente el **19.5% de sus respuestas** a consultas generales.

**Impacto de estrategias de mejora (sobre ChatGPT, accuracy %):**

| Estrategia | QA | Diálogo | Resumen | General |
|------------|----|---------|---------|---------|
| Baseline | 62.59 | 72.40 | 58.53 | 79.44 |
| + Recuperación de conocimiento | **76.83** | **73.80** | — | **90.73** |
| + Chain-of-Thought | 59.58 | 71.39 | **61.21** | 86.50 |
| + Muestras de contraste | 49.19 | 68.67 | 49.46 | — |

La recuperación de conocimiento externo es la estrategia más efectiva (+14.24 puntos en QA), mientras que las muestras de contraste empeoran el rendimiento porque las alucinaciones son muy similares a los textos correctos.

**Dominios temáticos con más errores:** Cine, empresas y bandas de música (QA); tecnología, clima e idiomas (consultas generales).

## Ventajas respecto a trabajos anteriores

- **Escala y cobertura múltiple:** 35.000 muestras en tres tareas distintas (QA, resumen, diálogo), mientras que benchmarks anteriores como TruthfulQA (817 preguntas) cubrían una sola tarea.
- **Generación automática escalable:** El proceso de sampling-then-filtering con ChatGPT permite crear alucinaciones plausibles y difíciles a cualquier escala, sin el costo prohibitivo de la anotación humana masiva.
- **Alucinaciones realistas:** Al usar el mismo tipo de modelo que se va a evaluar como generador, las alucinaciones creadas son precisamente las que el modelo tiene más probabilidad de producir y, por ende, más difíciles de detectar.
- **Análisis de causas:** Primer benchmark que clasifica los errores por *tipo de patrón de alucinación* y por *dominio temático*, permitiendo análisis más finos de los puntos débiles de cada modelo.
- **Primer benchmark de alucinaciones en diálogo a escala:** Los trabajos previos (BEGIN, Neural Path Hunter) evaluaban diálogo en escalas mucho más pequeñas.

## Trabajos previos relacionados

HaluEval organiza sus antecedentes en dos líneas: (1) trabajos que estudian las causas y manifestaciones de la alucinación en LLMs, y (2) benchmarks de evaluación de alucinaciones en tareas específicas. El paper se distingue por ser el primero en cubrir múltiples tareas a gran escala con alucinaciones generadas automáticamente.

- **Lin et al. (2021) — [TruthfulQA](2021_lin_truthfulqa.html)**: benchmark de 817 preguntas que mide si los LLMs imitan falsedades humanas; trabajo directamente relacionado que HaluEval complementa con muestras generadas automáticamente sobre QA, resumen y diálogo.
- **Zhao et al. (2020) — Reducing Quantity Hallucinations in Abstractive Summarization**: propone un sistema de verificación para identificar entidades no factuales en resumen abstractivo, antecedente en la detección de alucinaciones en resumen.
- **Dziri et al. (2021) — Neural Path Hunter**: entrena un crítico a nivel token para reconocer y rectificar alucinaciones en diálogo, citado como trabajo previo en mitigación de alucinaciones.
- **Rashkin et al. (2021) — Increasing Faithfulness in Knowledge-Grounded Dialogue with Controllable Features**: presenta el benchmark AIS (Attributable to Identified Sources) para evaluar si los documentos fuente soportan las generaciones, antecedente metodológico de HaluEval.
- **Dziri et al. (2022) — BEGIN: Benchmarking the Gap between Factual Knowledge and Language Models**: clasifica los enunciados de sistemas de diálogo en tres categorías de atribución a fuentes, benchmark de evaluación de alucinaciones en diálogo que HaluEval extiende.
- **Dhingra et al. (2019) — PARENT**: métrica para medir entailment léxico n-gram en generación table-to-text, citada como referente en métricas cuantitativas de alucinación.
- **Honovich et al. (2022) — TRUE: Re-Evaluating Factual Consistency Evaluation**: computa el AUC a nivel de ejemplo para evaluar consistencia factual, citado como métrica de evaluación relacionada.
- **Jiang et al. (2023) — Active Retrieval Augmented Generation**: propone usar interfaces de datos estructurados para mitigar alucinaciones, trabajo contemporáneo sobre mitigación citado como dirección de solución.

## Trabajos donde se usan

No hay papers en el repositorio que usen este dataset directamente.

## Tags

`benchmark` `alucinaciones` `QA` `resumen` `LLM`
