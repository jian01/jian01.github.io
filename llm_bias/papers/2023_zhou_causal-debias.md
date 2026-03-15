---
layout: paper
title: "Causal-Debias: Unifying Debiasing in Pretrained Language Models and Fine-tuning via Causal Invariant Learning"
year: 2023
authors: "Fan Zhou, Yuzhou Mao, Liu Yu, Yi Yang, Ting Zhong"
published: "ACL, 2023"
tags:
  - "debiasing"
  - "aprendizaje-causal"
  - "invarianza"
  - "fine-tuning"
  - "sesgo-social"
pdf: "/llm_bias/pdfs/2023_zhou_causal-debias.pdf"
method_type: "Causal / invariante"
datasets:
  - "CrowS-Pairs"
  - "StereoSet"
  - "GLUE"
measures_general_quality: "Sí"
status:
  - "Pendiente"
image: "imgs/2023_zhou_causal-debias.png"
image_caption: "Imagen asociada al paper Causal-Debias, que propone un framework de debiasing basado en aprendizaje causal invariante para modelos de lenguaje preentrenados."
opinion: "<WIP>"
---
# Causal-Debias: Unifying Debiasing in Pretrained Language Models and Fine-tuning via Causal Invariant Learning (2023)

**Autores**: Fan Zhou, Yuzhou Mao, Liu Yu, Yi Yang, Ting Zhong
**Publicado en**: ACL, 2023
**Tipo de método**: Causal / invariante

---

## Qué hace

Propone Causal-Debias, un framework que enmarca el debiasing como un problema de aprendizaje causal. Separa las features causales (relevantes para la tarea) de las correlaciones espurias (atributos demográficos que causan sesgo) usando principios de invarianza causal, funcionando tanto en preentrenamiento como en fine-tuning.


---

## Metodología

**La perspectiva causal:**
Cuando un modelo aprende a clasificar sentimientos, debería usar features causales (palabras con carga emocional positiva/negativa). Pero si el corpus de entrenamiento tiene más reseñas positivas escritas por ciertos grupos demográficos, el modelo también aprende features espurias (menciones de esos grupos → sentimiento positivo). Esto es sesgo.

**Aprendizaje invariante:**
La idea de la invarianza causal (IRM - Invariant Risk Minimization) es que las features verdaderamente causales tienen el mismo poder predictivo en diferentes "entornos". Los entornos aquí son grupos demográficos distintos.

**Causal-Debias en práctica:**
1. Se crean múltiples "entornos" particionando los datos por demografía (ej. textos sobre hombres vs. mujeres).
2. Se entrena el modelo con un objective que penaliza si el clasificador tiene diferente rendimiento en diferentes entornos.
3. Esto fuerza al modelo a aprender sólo las features que funcionan igual en todos los entornos (las causales).

Las modificaciones se hacen a **todas las capas del transformer** durante el fine-tuning, con el loss causal como regularización adicional. La arquitectura del transformer no cambia.

---

## Datasets utilizados

- **CrowS-Pairs**: evaluación de sesgo.
- **StereoSet**: completación de oraciones.
- **GLUE** (SST-2, QNLI, MNLI, CoLA): downstream tasks para medir degradación.
- **Entornos demográficos**: creados automáticamente desde los datasets.

---

## Ejemplo ilustrativo

Dataset de análisis de sentimiento: las reseñas de restaurantes escritas por usuarios de nombres anglosajones (John, Emily) son más positivas que las escritas por usuarios de nombres no anglosajones (Mohammed, Priya). El modelo aprende erróneamente que mencionar nombres anglosajones → sentimiento positivo. Causal-Debias crea entornos separados (reseñas de "John" vs. reseñas de "Mohammed") y entrena al modelo para que su predicción de sentimiento sea igualmente buena en ambos entornos, forzándolo a depender sólo del texto de la reseña, no del nombre del autor.

---

## Resultados principales

- Causal-Debias supera a CDA y INLP en CrowS-Pairs y StereoSet.
- El rendimiento en GLUE se degrada ~1-2%, similar a los mejores métodos de debiasing.
- Funciona tanto cuando se aplica durante el preentrenamiento como durante el fine-tuning en tareas específicas.
- El análisis de las features aprendidas muestra que efectivamente depende menos de atributos demográficos y más de features lingüísticas.

---

## Ventajas respecto a trabajos anteriores

- Principio teórico más sólido: basado en causalidad e invarianza, no sólo en heurísticas de augmentación de datos.
- Unifica preentrenamiento y fine-tuning debiasing en un framework coherente.
- Las features causales aprendidas son más generalizables que las aprendidas con CDA.

---

## Trabajos previos relacionados

El paper organiza los trabajos previos en dos categorías: (1) métodos de debiasing no específicos de tarea (que actúan sobre el PLM antes del fine-tuning) y (2) métodos específicos de tarea (que actúan sobre las representaciones del modelo al hacer fine-tuning). Adicionalmente, discute la línea de aprendizaje causal e invariante como base teórica.

- **Meade et al. (2022) — An empirical survey of the effectiveness of debiasing techniques**: estudio empírico de referencia que identifica el problema de que el debiasing daña las capacidades del modelo, motivando la propuesta de Causal-Debias; [2021_meade_debiasing-survey.md](2021_meade_debiasing-survey.html)
- **Guo et al. (2022) — Auto-Debias**: método de debiasing no específico de tarea que usa prompts biased automáticamente para guiar la corrección, usado como línea base y ejemplo del problema de resurgencia de sesgo.
- **He et al. (2022) — MABEL**: método de debiasing no específico de tarea con objetivos de igualación de sesgo basados en entailment; [2022_he_mabel.md](2022_he_mabel.html)
- **Liang et al. (2020) — Towards debiasing sentence representations (SentenceDebias)**: método post-hoc de referencia que actúa sobre representaciones de oraciones; en este paper se demuestra que tras el fine-tuning downstream el sesgo resurge igualmente.
- **Cheng et al. (2021) — FairFil**: método que aplica contrastive learning sobre representaciones para debiasing específico de tarea, con el que Causal-Debias comparte la motivación de integrar debiasing en el fine-tuning.
- **Zmigrod et al. (2019) — Counterfactual data augmentation (CDA)**: método de augmentación de datos contrafactuales usado como parte del mecanismo de intervención causal de Causal-Debias.
- **Arjovsky et al. (2019) — Invariant Risk Minimization (IRM)**: framework teórico de aprendizaje invariante que Causal-Debias extiende al dominio del debiasing de PLMs.
- **Gonen & Goldberg (2019) — Lipstick on a pig**: demuestra que los métodos de debiasing sólo cubren el sesgo sin eliminarlo realmente, motivando la perspectiva causal de este trabajo.
- **Kaneko & Bollegala (2021) — Debiasing pre-trained contextualised embeddings**: método Context-Debias que mitiga sesgo en embeddings contextuales, usado como baseline en los experimentos.
- **Nangia et al. (2020) — CrowS-Pairs**: benchmark de pares de oraciones sesgadas/no sesgadas usado para evaluar la reducción de sesgo.

## Tags

`debiasing` `aprendizaje-causal` `invarianza` `fine-tuning` `sesgo-social`
