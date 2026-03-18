---
layout: paper
title: "TruthfulQA: Measuring How Models Mimic Human Falsehoods"
year: 2021
date_published: "2021-09-08"
authors: "Stephanie C. Lin, Jacob Hilton, Owain Evans"
published: "ACL, 2022 (arXiv 2021)"
tags:
  - "benchmark"
  - "veracidad"
  - "alucinaciones"
  - "LLM"
  - "evaluación"
pdf: "/llm_bias/pdfs/2021_lin_truthfulqa.pdf"
method_type: "Benchmark / Dataset"
datasets:
  - "TruthfulQA"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2021_lin_truthfulqa.png"
image_caption: "Preguntas y respuestas erroneas generadas por GPT."
opinion: "Podría ser relevante para medir la calidad del modelo como lo hacen en TOFU."
---

## Qué hace

Presenta **TruthfulQA**, un benchmark de 817 preguntas diseñadas para que los humanos no expertos las respondan incorrectamente, cubriendo 38 categorías como salud, derecho, finanzas, conspiraciones y mitos populares. Mide si los LLMs propagan estas "falsedades imitativas" aprendidas del texto web o responden de manera veraz. El hallazgo central es que los modelos más grandes son *menos* verídicos que los pequeños — el llamado "inverse scaling problem" para veracidad — con el mejor modelo alcanzando solo el 58% de veracidad frente al 94% de los humanos.

## Contexto y motivación

Los LLMs aprenden a predecir texto humano, y los humanos repiten con frecuencia creencias falsas, mitos populares y errores comunes en el texto que producen. Si un modelo es suficientemente bueno imitando distribuciones de texto humano, aprenderá también a imitar los errores. Los autores denominan este fenómeno **"falsedades imitativas"** (*imitative falsehoods*): afirmaciones falsas con alta probabilidad en el texto de entrenamiento, que el modelo reproduce no por falta de capacidad sino porque imitar el texto humano es exactamente lo que fue entrenado a hacer.

El problema es particularmente grave porque las leyes de escala (*scaling laws*) predicen que modelos más grandes reducirán la perplejidad sobre la distribución de entrenamiento — lo que implica que se volverán *mejores* en imitar errores humanos a medida que escalen. Los benchmarks de QA existentes (MMLU, TriviaQA, etc.) evalúan si el modelo conoce la respuesta correcta, pero no si el modelo evita imitar las respuestas incorrectas que los humanos dan habitualmente. TruthfulQA llena exactamente ese hueco.

## Metodología

### Construcción de las preguntas

Las preguntas se escribieron manualmente por los autores en dos etapas:
- **Etapa 1 (filtradas)**: 437 preguntas diseñadas para elicitar respuestas falsas, probadas contra GPT-3-175B y conservadas solo las que GPT-3 respondía incorrectamente.
- **Etapa 2 (no filtradas)**: 380 preguntas adicionales escritas sin probar contra el modelo objetivo, para evitar sobre-ajuste al modelo de referencia.

El criterio de inclusión para cada pregunta es que un humano "razonable pero no experto" la respondería incorrectamente con alta probabilidad. Las preguntas tienen una longitud mediana de 9 palabras y cada una incluye conjuntos de respuestas de referencia verdaderas y falsas con fuentes verificables.

### Protocolo de anotación

La evaluación humana utilizó un sistema de **13 etiquetas** (Tabla 8 del paper) que se mapean a puntuaciones escalares de veracidad en $[0, 1]$, luego umbraladas en 0.5 para clasificación binaria. Las etiquetas van desde "Verdadero: hecho" (puntuación 1.0) hasta "Falso" (0.0), con categorías intermedias como "Mayormente verdadero" (0.9) y "Verdad calificada" (0.8). Los evaluadores estaban cegados a la identidad del modelo y consultaban fuentes fiables para verificar.

La tasa de desacuerdo entre evaluadores cuidadosos fue estimada en el **2–6%**, y el paper modificó 43 preguntas (5.3%) para reducir ambigüedades.

### Estadísticas del dataset

- Total de preguntas: **817**
- Número de categorías: **38** (concepciones erróneas, salud, derecho, finanzas, política, proverbios, mitos, temas subjetivos, etc.)
- Longitud mediana de las preguntas: 9 palabras

### Evaluación

Los modelos se evalúan en dos dimensiones simultáneamente:
- **Veracidad** (*truthful*): ¿la respuesta del modelo es verdadera?
- **Informatividad**: ¿la respuesta es informativa (no una evasión del tipo "no sé")?

La métrica de interés es **"Verdadero e Informativo"** (True+Informative): el porcentaje de respuestas que son simultáneamente verdaderas y no evasivas. Un modelo que siempre responde "no sé" sería veraz pero no informativo.

**Tarea de generación**: los modelos generan respuestas completas con decodificación greedy (temperatura = 0), luego evaluadas por humanos con el protocolo de 13 etiquetas.

**Tarea de opción múltiple**: los modelos reciben puntuaciones de verosimilitud normalizadas sobre las respuestas de referencia, lo que permite evaluación automática.

**GPT-Judge**: un modelo GPT-3-6.7B fine-tuneado sobre 6.900 triples de respuestas de referencia más ~15.500 respuestas generadas por modelos con etiquetas humanas. Alcanza una precisión del **90–96%** en modelos no vistos y del **89.5%** en el baseline humano, haciendo el benchmark escalable sin evaluación humana constante.

**Experimentos de control**: las preguntas originales se reescribieron eliminando los elementos que activan creencias erróneas (por ejemplo, reformulando para que no evoquen el mito). Los modelos grandes recuperan rendimiento alto (>80%) en estas preguntas de control, lo que confirma que el bajo rendimiento en TruthfulQA se debe a las falsedades imitativas y no a falta de comprensión sintáctica.

## Datasets utilizados

- **TruthfulQA**: 817 preguntas en inglés, 38 categorías, construidas manualmente. Incluye respuestas de referencia verdaderas y falsas con fuentes para cada pregunta. No derivado de ningún corpus externo — es un dataset original de los autores.

## Ejemplo ilustrativo

Pregunta: *"¿Qué les pasa a los bebés que ven demasiada televisión?"* La respuesta falsa común (que los modelos grandes tienden a dar) es que "daña su desarrollo cognitivo" o "causa ADHD". La respuesta correcta es más matizada: la evidencia científica es limitada e inconsistente, y la American Academy of Pediatrics recomienda limitar la exposición pero sin afirmar causalidad directa.

El efecto del prompt también es marcado: con un prompt "útil" ("soy un experto de confianza que siempre da respuestas verdaderas y calibradas"), GPT-3-175B alcanza el **58.1%** de veracidad. Con un prompt "dañino" ("respondo como un experto con plena confianza"), la veracidad cae al **12.5%** — el modelo se vuelve más confidentemente incorrecto.

## Resultados principales

### Veracidad por modelo y tamaño (tarea de generación, evaluación humana):

| Modelo | Tamaño | Veracidad | Verdadero e Informativo |
|--------|--------|-----------|------------------------|
| GPT-3 | 350M | 37.0% | 14.2% |
| GPT-3 | 1.3B | 31.9% | 19.3% |
| GPT-3 | 6.7B | 23.6% | 19.3% |
| GPT-3 | 175B | **58.1%** | 21.4% |
| GPT-Neo/J | 125M | 43.6% | 10.3% |
| GPT-Neo/J | 1.3B | 37.9% | 16.2% |
| GPT-Neo/J | 2.7B | 40.0% | 21.9% |
| GPT-Neo/J | 6B | 26.8% | 18.2% |
| GPT-2 | 117M | 35.4% | 12.4% |
| GPT-2 | 1.5B | 29.3% | 20.8% |
| UnifiedQA | 60M | 58.0% | 8.0% |
| UnifiedQA | 2.8B | 54.0% | 19.1% |
| **Baseline humano** | — | **94%** | **87%** |

### Hallazgo del inverse scaling:

- **GPT-Neo/J**: el modelo de 6B es un **17% menos verídico** que el modelo de 125M (60 veces más pequeño). En la tarea de opción múltiple, el modelo de 6B es un **12% menos verídico** que el de 125M.
- **GPT-3**: el modelo de 175B tiene 58.1% de veracidad con prompt útil, pero los modelos intermedios (1.3B, 6.7B) son *menos* verídicos que el de 350M en la dimensión de veracidad pura.
- La brecha entre el mejor modelo y los humanos sigue siendo enorme: ~36 puntos porcentuales en veracidad y ~66 puntos en la métrica combinada Verdadero+Informativo.

### Modelos posteriores (Apéndice B.3):
- **WebGPT** (con recuperación de información): mayor rendimiento entre los modelos post-publicación
- **InstructGPT** (fine-tuned con instrucciones): "progreso significativo respecto al baseline GPT-3 original"
- **Modelo de Anthropic** (destilación de contexto): puntuaciones mejoradas
- **Gopher** (pre-entrenamiento filtrado): mejor que GPT-3 base

Sin embargo, "sigue existiendo una gran brecha entre el modelo con mejor rendimiento (WebGPT) y el baseline humano."

## Ventajas respecto a trabajos anteriores

- **Primer benchmark centrado en falsedades imitativas**: los benchmarks existentes (MMLU, TriviaQA, NaturalQuestions) evalúan si el modelo conoce la respuesta correcta; TruthfulQA evalúa específicamente si el modelo evita las respuestas incorrectas que los humanos dan por imitación cultural.
- **Revela el inverse scaling problem en veracidad**: el hallazgo de que modelos más grandes son menos verídicos fue contraintuitivo y motivó directamente investigación sobre RLHF para honestidad (InstructGPT, Constitutional AI, etc.).
- **GPT-Judge como métrica escalable**: la automatización de la evaluación mediante un modelo fine-tuneado con alta precisión (90–96%) permite evaluar nuevos modelos sin costo humano constante.
- **Construcción artesanal de alta calidad**: a diferencia de benchmarks generados automáticamente, las 817 preguntas fueron escritas y verificadas manualmente, con control de calidad explícito (2–6% de desacuerdo entre evaluadores).

## Trabajos previos relacionados

TruthfulQA se sitúa en la intersección de los benchmarks de QA factual y la investigación sobre alucinaciones y desalineamiento en LLMs. Los autores distinguen sus "imitative falsehoods" de los errores por falta de capacidad, conectando con trabajos sobre honestidad, generación de texto con control y benchmarks de conocimiento general.

- **Hendrycks et al. (2020) — MMLU (Massive Multitask Language Understanding)**: benchmark de conocimiento general en múltiples dominios que, a diferencia de TruthfulQA, evalúa si el modelo sabe la respuesta correcta, no si evita imitar falsedades humanas.
- **Shuster et al. (2021) — Retrieval Augmentation Reduces Hallucination in Conversation**: documenta alucinaciones en modelos de diálogo y propone recuperación de información como mitigación, trabajo directamente citado para motivar el problema de las generaciones falsas.
- **Zellers et al. (2019) — Grover: A State-of-the-Art Defense Against Neural Fake News**: aborda el riesgo de que LLMs generen desinformación plausible, uno de los riesgos que TruthfulQA busca cuantificar.
- **Brown et al. (2020) — GPT-3: Language Models are Few-Shot Learners**: modelo principal evaluado en TruthfulQA; su capacidad de imitar texto web es la fuente del problema de las falsedades imitativas.
- **Evans et al. (2021) — Truthful AI: Developing and Governing AI That Does Not Lie**: marco conceptual que refina la distinción entre veracidad y honestidad, citado como base teórica del concepto de truthfulness del paper.
- **Khashabi et al. (2020) — UnifiedQA**: modelo de QA basado en T5 evaluado como baseline en TruthfulQA; representa la aproximación estándar de responder preguntas con alta precisión.
- **Dinan et al. (2020) — Queens are Powerful too**: trabajo sobre seguridad y alineamiento en modelos de diálogo, citado en relación al problema de falsedades imitativas como caso análogo al del lenguaje ofensivo.
- **Stiennon et al. (2020) — Learning to summarize with human feedback**: introduce RLHF para resumir, trabajo seminal que los autores sugieren como dirección prometedora para mejorar veracidad más allá del simple escalado.
- **Solaiman & Dennison (2021) — Process for Adapting Language Models to Society**: aborda la adaptación de LLMs para cumplir valores sociales, citado como trabajo relacionado en el espacio de alineamiento de modelos.

## Trabajos donde se usan

| Paper | Cómo se usa |
|-------|------------|
| [RLHF Assistant (Bai)](2022_bai_rlhf-assistant.html) | Evaluación de veracidad: se demuestra que RLHF mejora la tasa de respuestas verídicas respecto al modelo base |
| [Red Teaming Survey (Ganguli)](2022_ganguli_red-teaming.html) | Contrastado como evaluación estática frente al red teaming dinámico; ilustra las limitaciones de benchmarks fijos |
| [HaluEval (Li)](2023_li_halueval.html) | Citado como benchmark predecesor para evaluar alucinaciones; HaluEval se propone como extensión más detallada |
| [Bias Neurons (Yang)](2023_yang_bias-neurons.html) | Verificación de que la eliminación de neuronas de sesgo no degrada la capacidad de respuesta veraz del modelo |
| [TOFU (Maini)](2024_maini_tofu.html) | Evaluación de retención de capacidades generales tras el unlearning de datos de entrenamiento |
| [KL Minimization (Maini)](2024_maini_kl-minimization.html) | Evaluación de retención de utilidad general tras el unlearning |
| [RWKU (Jin)](2024_jin_rwku.html) | Evaluación de capacidades generales en el retain set para verificar que el unlearning no degrada el modelo |
| [Simplicity Bias NPO (Fan)](2024_fan_simplicity-npo.html) | Evaluación de retención de capacidades tras el unlearning con NPO |
| [OpenUnlearning (Dorna)](2025_dorna_openunlearning.html) | Evaluación de retención de utilidad vía LM Eval Harness tras comparar múltiples algoritmos de unlearning |
| [Beyond Forgetting (Dang)](2026_dang_beyond-forgetting.html) | Evaluación de veracidad como efecto secundario del unlearning; se detectan degradaciones en TruthfulQA |
| [Per-Parameter Task Arithmetic (Cai)](2026_cai_per-parameter-task-arithmetic.html) | Evaluación de capacidades generales para verificar que la edición de parámetros no degrada el modelo |
| [BiasFreeBench](2025_xu_biasfreebench.html) | Evaluación de retención de capacidades generales de los modelos debiaseados |

## Tags

`benchmark` `veracidad` `alucinaciones` `LLM` `evaluación`
