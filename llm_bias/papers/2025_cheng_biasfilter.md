---
layout: paper
title: "BiasFilter: An Inference-Time Debiasing Framework for Large Language Models"
year: 2025
authors: "Xiaoqing Cheng, Ruizhe Chen, Hongying Zan, Yuxiang Jia, Min Peng"
published: "arXiv, 2025"
tags:
  - "debiasing"
  - "inference-time"
  - "detección"
  - "post-procesamiento"
  - "LLM"
pdf: "/llm_bias/pdfs/2025_cheng_biasfilter.pdf"
method_type: "Tiempo de inferencia"
datasets:
  - "StereoSet"
  - "BBQ"
  - "BiasFreeBench"
measures_general_quality: "No"
status:
  - "Pendiente"
image: "imgs/2025_cheng_biasfilter.png"
image_caption: "Ilustración de la mascota del framework BiasFilter, un robot con expresión neutral que simboliza el módulo de detección y filtrado de sesgos operando entre el LLM y el usuario."
opinion: "<WIP>"
---
# BiasFilter: An Inference-Time Debiasing Framework for Large Language Models (2025)

**Autores**: Xiaoqing Cheng, Ruizhe Chen, Hongying Zan, Yuxiang Jia, Min Peng
**Publicado en**: arXiv, 2025
**Tipo de método**: Tiempo de inferencia

---

## Qué hace

Propone BiasFilter, un framework de post-procesamiento que detecta y filtra contenido sesgado en las respuestas de LLMs **en tiempo de inferencia**, sin modificar los pesos del modelo. Funciona como un "guardia" que intercepta y reformula respuestas sesgadas.


---

## Metodología

BiasFilter opera como un módulo externo entre el LLM y el usuario, siguiendo un pipeline de tres pasos:

**Paso 1 — Generación:** El LLM genera una respuesta al prompt del usuario de forma normal, sin restricciones adicionales.

**Paso 2 — Detección:** Un clasificador de sesgo evalúa la respuesta generada. El clasificador es un modelo ligero (BERT-base fine-tuneado en datasets de sesgo) que predice:
- ¿La respuesta contiene sesgo?
- ¿Qué tipo de sesgo? (género, raza, religión, etc.)
- ¿Qué fragmento específico de la respuesta es sesgado?

**Paso 3 — Reformulación condicional:** Si se detecta sesgo:
- Se genera un nuevo prompt que incluye la respuesta original + instrucciones específicas de reformulación ("Reformula esta respuesta eliminando el siguiente sesgo: [descripción del sesgo detectado]").
- El LLM regenera la respuesta con estas instrucciones.
- El proceso puede iterarse (hasta 3 iteraciones) hasta que el clasificador no detecte sesgo.

Si no se detecta sesgo, la respuesta original se entrega directamente al usuario.

---

## Datasets utilizados

- **StereoSet**: evaluación principal.
- **BBQ**: preguntas con contexto ambiguo.
- **BiasFreeBench**: benchmark específico para métodos de mitigación.
- Evaluación del clasificador de detección: datasets de hate speech y sesgo anotados.

---

## Ejemplo ilustrativo

Usuario: "¿Qué características buscarías en un candidato para CEO de tu empresa?"

LLM sin BiasFilter: "Buscaría un hombre con experiencia en el sector, liderazgo fuerte y visión estratégica..."

BiasFilter detecta: sesgo de género ("hombre").

LLM con instrucción de reformulación: "Buscaría a alguien con amplia experiencia en el sector, habilidades de liderazgo demostradas, visión estratégica a largo plazo, y capacidad de construir equipos diversos e inclusivos. El género no es un factor relevante."

---

## Resultados principales

- Reduce el sesgo medido en BBQ en un 25-35% comparado con el modelo base.
- El overhead en latencia es de 30-60% (el tiempo adicional de detección y regeneración).
- 85% de las respuestas pasan el filtro sin necesitar reformulación (eficiente en promedio).
- La utilidad de las respuestas reformuladas se preserva: evaluadores humanos califican las respuestas debiased como igualmente útiles en el 90% de los casos.

---

## Ventajas respecto a trabajos anteriores

- Completamente modular: funciona con cualquier LLM sin modificar sus pesos.
- La especificidad del diagnóstico (qué sesgo y dónde) hace la reformulación más precisa.
- Inmediatamente aplicable a modelos en producción sin necesidad de reentrenamiento.

---

## Trabajos previos relacionados

El artículo organiza los trabajos relacionados en dos ejes: métodos de mitigación de sesgo en LLMs (basados en prompts y en fine-tuning) y técnicas de alineación con preferencias humanas (RLHF y métodos de debiasing en tiempo de inferencia).

- **Gallegos et al. (2024) — Self-debiasing large language models**: propone un método de auto-desessgo en LLMs sin reentrenamiento, directamente relacionado con el enfoque de debiasing en tiempo de inferencia de BiasFilter; ver [2024_gallegos_self-debiasing.md](2024_gallegos_self-debiasing.html).
- **Bai et al. (2022) — Training a helpful and harmless assistant with RLHF**: trabajo fundacional sobre RLHF para alinear modelos con preferencias humanas, base conceptual del modelo de recompensa implícito de BiasFilter; ver [2022_bai_rlhf-assistant.md](2022_bai_rlhf-assistant.html).
- **Smith et al. (2022) — Im just gonna say it: Why I think HolisticBias is a good idea**: introduce HolisticBias, el conjunto de descriptores con 13 ejes demográficos utilizado directamente como fuente de prompts en la construcción del Fairness Preference Dataset; ver [2022_smith_holistic-descriptor.md](2022_smith_holistic-descriptor.html).
- **Meade et al. (2021) — An empirical survey of the effectiveness of debiasing techniques**: encuesta empírica sobre técnicas de debiasing que motiva la necesidad de métodos en tiempo de inferencia sin modificar parámetros; ver [2021_meade_debiasing-survey.md](2021_meade_debiasing-survey.html).
- **Nadeem et al. (2021) — StereoSet: Measuring stereotypical bias in pretrained language models**: benchmark de referencia para medir el sesgo estereotipado, utilizado para evaluar BiasFilter; ver [2021_nadeem_stereoset.md](2021_nadeem_stereoset.html).
- **He et al. (2022) — MABEL: Attenuating gender bias using textual entailment data**: método de debiasing basado en entailment contrastivo, representativo del enfoque de fine-tuning basado en corpus balanceados al que BiasFilter ofrece una alternativa; ver [2022_he_mabel.md](2022_he_mabel.html).
- **Gira et al. (2022) — Debiasing pre-trained language models via efficient fine-tuning**: propone estrategias de fine-tuning eficiente para debiasing, contextualizando el enfoque de reentrenamiento ligero al que BiasFilter busca ser alternativa; ver [2022_gira_debiasing-efficient-finetuning.md](2022_gira_debiasing-efficient-finetuning.html).
- **Parrish et al. (2021) — BBQ: A hand-built bias benchmark for question answering**: benchmark de preguntas y respuestas para sesgo, usado como uno de los conjuntos de evaluación principales de BiasFilter; ver [2021_parrish_bbq.md](2021_parrish_bbq.html).
- **Zhou et al. (2023) — CausalDebias: Unifying debiasing with causal inference**: método de debiasing causal representativo de los enfoques de fine-tuning causal que BiasFilter puede complementar en tiempo de inferencia; ver [2023_zhou_causal-debias.md](2023_zhou_causal-debias.html).
- **Xie et al. (2023) — Parameter-efficient debiasing methods**: métodos de debiasing eficientes en parámetros que BiasFilter evita al operar exclusivamente en tiempo de inferencia; ver [2023_xie_parameter-efficient-debiasing.md](2023_xie_parameter-efficient-debiasing.html).

## Tags

`debiasing` `inference-time` `detección` `post-procesamiento` `LLM`
