---
layout: paper
title: "Social Bias Frames: Reasoning about Social and Power Implications of Language"
year: 2020
date_published: "2019-11-10"
authors: "Maarten Sap, Saadia Gabriel, Lianhui Qin, Dan Jurafsky, Noah A. Smith, Yejin Choi"
published: "ACL, 2020"
tags:
  - "dataset"
  - "sesgo-social"
  - "hate-speech"
  - "anotación-estructurada"
  - "NLP"
pdf: "/llm_bias/pdfs/2020_sap_social-bias-frames.pdf"
method_type: "Benchmark / Dataset"
datasets:
  - "SBIC (Social Bias Inference Corpus)"
status:
  - "Leido"
image: "imgs/2020_sap_social-bias-frames.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---
# Social Bias Frames: Reasoning about Social and Power Implications of Language (2020)

**Autores**: Maarten Sap, Saadia Gabriel, Lianhui Qin, Dan Jurafsky, Noah A. Smith, Yejin Choi
**Publicado en**: ACL, 2020
**Tipo de método**: Benchmark / Dataset

---

## Qué hace

Introduce el framework de **Social Bias Frames**: representaciones estructuradas que capturan las implicaciones sociales y de poder de textos potencialmente ofensivos. Crea el dataset SBIC con 44.671 publicaciones de redes sociales anotadas con estos frames estructurados.


---

## Metodología

En lugar de simplemente etiquetar texto como "ofensivo/no ofensivo", Social Bias Frames captura información estructurada sobre el sesgo:

**Componentes de un Social Bias Frame:**
- **¿Es ofensivo?**: ¿el texto intenta ser o resulta ofensivo?
- **¿Es irónico?**: ¿usa sarcasmo o humor para expresar sesgo?
- **¿Contra qué grupo?**: el grupo objetivo (mujeres, personas negras, comunidad LGBTQ+, etc.).
- **¿Qué implica?**: la implicación estereotipada o dañina (ej. "las mujeres son malas conductoras").
- **¿Busca controlar?**: ¿el texto busca restringir el comportamiento de ese grupo?

**Construcción del dataset (SBIC):** 44.671 publicaciones de Reddit, Twitter, y dos datasets de hate speech. Las anotaciones fueron realizadas por trabajadores de crowdsourcing siguiendo un protocolo detallado, con múltiples anotadores por muestra para capturar desacuerdo.

**Modelo entrenado:** Se entrena un modelo de lenguaje (RoBERTa + generación) para predecir estos frames estructurados dado un texto. Esto convierte la tarea en razonamiento sobre implicaciones sociales.

---

## Datasets utilizados

- **SBIC (Social Bias Inference Corpus)**: 44.671 posts de Reddit, Twitter, y Gab; 150.000+ anotaciones.
- Fuentes: Reddit (r/SexistSubs, r/RacistJokes, etc.), Twitter, Gab.
- Evaluación: 9 grupos demográficos incluidos.

---

## Ejemplo ilustrativo

Post de Twitter: *"Las mujeres no deberían conducir, ¿verdad? jajaja"*

Social Bias Frame anotado:
- ¿Ofensivo?: Sí (potencialmente)
- ¿Irónico?: Sí (el "jajaja" sugiere "broma")
- Grupo objetivo: Mujeres
- Implicación: "Las mujeres son malas conductoras"
- ¿Busca controlar?: Sí (implica restricción de actividades)

Un modelo que predice estos frames puede identificar no sólo que el texto es problemático, sino exactamente *por qué* y *a quién* perjudica — información crucial para sistemas de moderación matizados.

---

## Resultados principales

- El modelo entrenado en SBIC logra alta accuracy en predecir ofensividad y grupo objetivo (~80%).
- La predicción de la implicación estructurada (qué estereotipo se usa) es más difícil (~60% BLEU).
- Crowdworkers tienen alta tasa de acuerdo en ofensividad (~75%) pero menor en la implicación exacta (~60%).
- Los errores del modelo revelan que el razonamiento sobre implicaciones sociales requiere conocimiento del mundo que los modelos actuales aún no dominan.

---

## Ventajas respecto a trabajos anteriores

- Primer framework que va más allá de la clasificación binaria ofensivo/no ofensivo hacia representaciones estructuradas del sesgo.
- Permite entender el "por qué" del sesgo, no sólo si existe.
- Introduce el concepto de razonamiento sobre implicaciones sociales como tarea de NLP.

---

## Trabajos previos relacionados

Social Bias Frames organiza los trabajos previos en dos líneas principales: (1) detección de sesgo y toxicidad (clasificación binaria), y (2) inferencia sobre dinámicas sociales y poder. El paper se distingue por combinar ambas líneas en un framework de razonamiento estructurado sobre implicaciones de sesgo.

- **Waseem & Hovy (2016) — Hateful Symbols or Hateful People?**: uno de los primeros datasets de hate speech (Twitter), representante de la aproximación de clasificación binaria que Social Bias Frames supera al capturar información estructurada sobre el sesgo.
- **Davidson et al. (2017) — Automated Hate Speech Detection and the Problem of Offensive Language**: dataset de 24.802 tweets con clasificación multi-clase (odio/ofensivo/neutro), citado como referente de la taxonomía binaria/simple que este trabajo extiende.
- **Founta et al. (2018) — Large Scale Crowdsourcing and Characterization of Twitter Abusive Behavior**: dataset de 80.000 tweets de Twitter con anotación de comportamiento abusivo, citado como uno de los datasets de referencia en la detección de toxicidad.
- **Wulczyn et al. (2017) — Ex Machina: Personal Attacks Seen at Scale**: usa variables binarias múltiples para anotar comentarios de Wikipedia, antecedente más cercano al enfoque multi-dimensional de SBIC.
- **Ousidhoum et al. (2019) — Multilingual and Multi-Aspect Hate Speech Analysis**: dataset multilingüe de 13k tweets con cinco dimensiones emocionales y de toxicidad incluyendo grupos sociales objetivo; el trabajo previo más relacionado al enfoque multi-aspecto de Social Bias Frames.
- **Breitfeller et al. (2019) — Finding Microaggressions in the Wild**: aborda el lenguaje de microagresión implícita en Reddit, línea de sesgo sutil que Social Bias Frames amplía con sus implicaciones estructuradas.
- **Rashkin et al. (2018) — Event2Mind: Commonsense Inference on Events, Intents, and Reactions**: marco de inferencia de commonsense sobre estados mentales de participantes de situaciones, inspiración metodológica para el razonamiento sobre implicaciones de Social Bias Frames.
- **Sap et al. (2019) — HellaSwag / Social IQa**: trabajos del mismo grupo sobre inferencia de commonsense social, base metodológica del enfoque de razonamiento estructurado sobre situaciones sociales.

## Tags

`dataset` `sesgo-social` `hate-speech` `anotación-estructurada` `NLP`
