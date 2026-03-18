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
  - "Irrelevante"
image: "imgs/2020_sap_social-bias-frames.png"
image_caption: "Ejemplo de todos los campos taggeados para una frase. El dataset está compuesto de múltiples de estos."
opinion: "No se como podríamos usar esto."
---

## Qué hace

Introduce el formalismo de **Social Bias Frames**: representaciones estructuradas que capturan las implicaciones pragmáticas de sesgo social y diferencial de poder en el lenguaje. Crea el **Social Bias Inference Corpus (SBIC)** con 150k anotaciones estructuradas sobre 44.671 publicaciones de redes sociales, cubriendo más de 34k implicaciones en texto libre sobre aproximadamente 1.414 grupos demográficos. Establece además baselines neurales (GPT/GPT-2) que alcanzan $F_1 = 80\%$ en la clasificación de ofensividad pero revelan que la generación de implicaciones estructuradas sigue siendo un reto abierto.

## Contexto y motivación

La mayoría de los trabajos en detección de toxicidad y hate speech se limitaban a clasificación binaria (ofensivo / no ofensivo), ignorando la estructura subyacente del sesgo: ¿a quién se dirige?, ¿qué estereotipo implica?, ¿con qué intención? El lenguaje puede vehicular sesgos de manera implícita, no explícita: escuchar que una película con reparto completamente musulmán fue un "fracaso de taquilla" lleva a la mayoría de oyentes a inferir que "los musulmanes son terroristas", pero los formalismos semánticos estándar no capturan estas implicaturas pragmáticas. Sin representaciones estructuradas del sesgo, los sistemas de moderación no pueden explicar por qué un texto es dañino ni ayudar a redactores a corregir su lenguaje.

## Metodología

### Formalismo: Social Bias Frames

Dado un post de texto, se anotan **7 dimensiones** combinando etiquetas categóricas y texto libre:

| Dimensión | Tipo | Valores posibles |
|-----------|------|-----------------|
| Ofensividad (`offensive`) | Categórica | sí / quizás / no |
| Intención de ofender (`intent`) | Categórica | sí / probablemente / probablemente no / no |
| Contenido lascivo (`lewd`) | Categórica | sí / quizás / no |
| Implicación grupal (`group targeted`) | Binaria | sí / no |
| Grupo objetivo (`targeted group`) | Texto libre | ej. "black folks", "women" |
| Enunciado implicado (`implied statement`) | Texto libre (plantilla Hearst) | "GROUP does/are ___" |
| Lenguaje de endogrupo (`in-group`) | Binaria | sí / no |

### Fuentes de datos

| Fuente | Nº posts |
|--------|----------|
| Reddit: r/darkJokes, r/meanJokes, r/offensiveJokes | 13.934 |
| Reddit: microagresiones (Breitfeller et al. 2019) | 2.011 |
| Twitter: Founta et al. (2018) | 11.864 |
| Twitter: Davidson et al. (2017) | 3.008 |
| Twitter: Waseem & Hovy (2016) | 1.816 |
| Gab | 3.715 |
| Stormfront | 4.016 |
| BannedReddits (r/Incels, r/MensRights) | 4.308 |
| **Total** | **44.671** |

### Protocolo de anotación

La anotación se realizó en **Amazon Mechanical Turk (MTurk)**, restringiendo el pool a trabajadores de EE.UU. y Canadá. Se recolectaron **3 anotaciones por post**. El diseño es jerárquico: solo si el anotador indica ofensividad potencial responde sobre implicaciones de grupo; y solo si se indica un grupo objetivo, escribe los enunciados implicados (de 2 a 4 estereotipos en forma de plantilla Hearst).

**Perfil demográfico de los anotadores (final):** 55% mujeres, 42% hombres, <1% no binario; media de edad 36±10 años; 82% blancos, 4% asiáticos, 4% hispanos, 4% negros.

**Acuerdo entre anotadores:**

| Dimensión | Acuerdo por pares | Krippendorff $\alpha$ |
|-----------|:-----------------:|:--------------------:|
| Global | 82,4% | 0,45 |
| Ofensividad | 76% | 0,51 |
| Intención de ofender | 75% | 0,46 |
| Implicación grupal | 74% | 0,48 |
| Contenido lascivo | 94% | 0,62 |
| Lenguaje endogrupo | 94% | 0,17 |
| Grupo objetivo (exact match) | 80,2% | 0,50 |

Estos valores son notablemente superiores al estado del arte previo en detección de toxicidad (ej. Ross et al. 2017: $\alpha = 0{,}22$).

### Estadísticas finales de SBIC

| Métrica | Valor |
|---------|-------|
| Tuplas de inferencia totales | 147.139 |
| Posts únicos | 44.671 |
| Grupos demográficos únicos | 1.414 |
| Implicaciones únicas (texto libre) | 32.028 |
| Pares post–grupo | 48.923 |
| % posts ofensivos | 44,8% |
| % con intención de ofender | 43,4% |
| % con contenido lascivo | 7,9% |
| % con implicación de grupo | 50,9% |
| % con lenguaje de endogrupo | 4,6% |
| División train/dev/test | 75% / 12,5% / 12,5% |

Los grupos objetivo más frecuentes son género/sexualidad (ej. mujeres, LGBTQ+), raza/etnia (ej. personas negras, latinx, asiáticas) y cultura/religión (ej. musulmanes, judíos).

### Modelos de inferencia

Se entrenan modelos **SBF-GPT$_1$** y **SBF-GPT$_2$** sobre el corpus, linealizando el frame completo como secuencia de tokens. Se evalúan con decodificación greedy (`-gdy`) y sampling (`-smp`), y variantes con decodificación restringida (`-constr`) que recomputa probabilidades de variables categóricas post-generación. Hiperparámetros: batch size 4; learning rates $5\times10^{-6}$ (GPT-1) y $10^{-5}$ (GPT-2); hasta 5 épocas.

## Datasets utilizados

- **SBIC (Social Bias Inference Corpus)**: 44.671 posts de Reddit, Twitter, Gab y sitios de odio; 150.000 anotaciones estructuradas; 1.414 grupos demográficos; 32.028 implicaciones únicas en texto libre. Disponible públicamente.
- Fuentes de posts: Reddit (subreddits ofensivos y microagresiones), Twitter (tres datasets existentes de toxicidad), Gab, Stormfront, subreddits baneados.

## Ejemplo ilustrativo

Tomado directamente de la Tabla 1 del paper:

> *"I thought drugs were the only things black people could shoot up — Boy was I wrong"*

Social Bias Frame anotado:
- Ofensivo: **Sí**
- Intención de ofender: **Sí**
- Lascivo: No
- Grupo objetivo: **black folks**
- Enunciado implicado: *"black folks kill people"* / *"commit shootings"*
- Lenguaje de endogrupo: No

El frame captura no solo que el texto es ofensivo, sino exactamente el estereotipo vehiculado (violencia racial) y hacia quién — información indispensable para sistemas de moderación que vayan más allá del etiquetado binario.

## Resultados principales

**Clasificación** (mejor modelo, SBF-GPT$_2$-gdy, test set):

| Variable | $F_1$ | Precisión | Recall |
|----------|:-----:|:---------:|:------:|
| Ofensividad | 77,2 | 88,3 | 68,6 |
| Intención de ofender | 76,3 | 89,5 | 66,5 |
| Contenido lascivo | 77,6 | 81,2 | 74,3 |
| Grupo objetivo (binario) | 66,9 | 67,9 | — |

La variable de lenguaje de endogrupo no pudo predecirse positivamente por ningún modelo (solo 4,6% positivos — extremadamente desbalanceada).

**Generación de texto libre** (SBF-GPT$_2$-gdy, test set):

| Tarea | BLEU-2 | ROUGE-L | WMD |
|-------|:------:|:-------:|:---:|
| Grupo objetivo | 77,0 | 71,3 | 0,76 |
| Enunciado implicado | 52,2 | 46,5 | 2,81 |

Los modelos generan bien los grupos objetivo (espacio de salida limitado: ~1.400 grupos posibles) pero presentan mayor dificultad con la implicación (espacio de salida abierto). El análisis de errores muestra que los modelos tienden a generar estereotipos genéricos del grupo demográfico en lugar de implicaciones específicamente entailadas por el post concreto.

## Ventajas respecto a trabajos anteriores

- Primer framework que va más allá de la clasificación binaria ofensivo/no ofensivo hacia representaciones **estructuradas** del sesgo con 7 dimensiones.
- Permite entender el "por qué" del sesgo (implicación, grupo objetivo, intención) y no solo si existe.
- Cobertura de **1.414 grupos demográficos** con implicaciones en texto libre, frente a taxonomías cerradas y reducidas de trabajos anteriores.
- Acuerdo entre anotadores muy superior al estado del arte previo ($\alpha = 0{,}45$ vs. $\alpha = 0{,}22$ en Ross et al. 2017), gracias al diseño jerárquico y pilotaje iterativo.
- Introduce el razonamiento sobre implicaciones sociales como tarea de NLP que combina clasificación y generación condicionada.

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

## Trabajos donde se usan

| Paper | Cómo se usa |
|-------|------------|
| [ToxiGen](2022_hartvigsen_toxigen.html) | Comparación directa en tabla de datasets de hate speech; HateBERT fine-tuneado en ToxiGen se evalúa sobre SBIC como benchmark externo |
| [Bias Benchmarks Speech (Satish/SAGE)](2025_satish_bias-benchmarks-speech.html) | Marco conceptual para entender cómo el sesgo se manifiesta en generación libre, motivando las evaluaciones long-form de la suite SAGE-LF |
| [BBQ](2021_parrish_bbq.html) | Referenciado como trabajo que conecta comportamiento del modelo con daño real al razonar sobre implicaciones sociales |
| [Human-like Biases (Acerbi)](2023_acerbi_human-like-biases.html) | Citado como trabajo relacionado que estudia la dimensión social del sesgo desde una perspectiva complementaria a los experimentos de transmisión cultural |

## Tags

`dataset` `sesgo-social` `hate-speech` `anotación-estructurada` `NLP`
