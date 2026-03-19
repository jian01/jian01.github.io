---
layout: paper
title: "MABEL: Attenuating Gender Bias using Textual Entailment Data"
year: 2022
date_published: "2022-10-26"
authors: "Jacqueline He, Mengzhou Xia, Christiane Fellbaum, Danqi Chen"
published: "EMNLP, 2022"
tags:
  - "debiasing"
  - "NLI"
  - "contrastive-learning"
  - "sesgo-de-género"
  - "BERT"
pdf: "/llm_bias/pdfs/2022_he_mabel.pdf"
method_type: "Data augmentation"
datasets:
  - "SNLI + MultiNLI"
  - "StereoSet"
  - "CrowS-Pairs"
  - "WinoBias"
  - "GLUE"
measures_general_quality: "Sí"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2022_he_mabel.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---

## Qué hace

Propone **MABEL** (**M**ethod for **A**ttenuating Gender **B**ias using **E**ntailment **L**abels), un método de pre-entrenamiento intermedio (*intermediate pre-training*) para reducir el sesgo de género en representaciones contextualizadas de modelos tipo BERT. La idea central es usar pares de oraciones de inferencia textual (NLI) con etiquetas de *entailment* junto con augmentación contrafactual de género, y entrenar con tres objetivos combinados: una pérdida contrastiva basada en entailment, una pérdida de alineamiento de pares de género, y el MLM estándar de BERT.

MABEL opera como una etapa de pre-entrenamiento adicional: se parte de `bert-base-uncased`, se hace fine-tuning con el objetivo combinado, y el modelo resultante puede luego fine-tunearse en cualquier tarea downstream como BERT normal. No requiere modelos auxiliares y el entrenamiento tarda menos de 2 horas en 4 GPUs.

---

## Motivación

Los métodos de debiasing previos se dividen en dos categorías: **específicos por tarea** (requieren datos anotados de esa tarea) y **agnósticos de tarea** (modifican las representaciones antes de cualquier fine-tuning). MABEL es agnóstico de tarea. Los métodos agnósticos anteriores (SentenceDebias, ContextDebias, INLP, FairFil) computan o proyectan el subespacio de género en representaciones de texto plano sin estructura semántica.

La hipótesis de MABEL: los datos NLI son superiores como datos de entrenamiento de debiasing porque (1) son gratuitos y abundantes (~300K pares en SNLI+MNLI), (2) están estructurados semánticamente (la relación de entailment codifica equivalencia de significado entre pares de distinto género), y (3) permiten un objetivo contrastivo más robusto que las oraciones sueltas. Los resultados confirman que las oraciones de entailment son críticas — usar pares de contradicción o pares de paráfrasis de otros datasets degrada significativamente el rendimiento.

---

## Construcción de los datos de entrenamiento

Se usan pares de SNLI (Stanford NLI) y MNLI (Multi-Genre NLI). El proceso:

1. **Filtrado:** De los ~320K pares totales de SNLI+MNLI, se retienen solo los pares con etiqueta de **entailment** y que contengan al menos una palabra de género en alguna de las dos oraciones.

2. **Augmentación contrafactual de datos (CDA):** Para cada oración en cada par filtrado, se reemplaza cada término de género por su opuesto en el eje de género usando una lista de pares de palabras:

   | Original | Contrafactual |
   |---|---|
   | man / woman | woman / man |
   | boy / girl | girl / boy |
   | he / she | she / he |
   | father / mother | mother / father |
   | son / daughter | daughter / son |
   | his / her | her / his |
   | himself / herself | herself / himself |

3. **Resultado:** Cada par de entailment original $$(p_i, h_i)$$ genera un par aumentado $$(\hat{p}_i, \hat{h}_i)$$ donde todas las palabras de género están intercambiadas. Los cuatro elementos forman un **cuádruplo** $$(p_i, h_i, \hat{p}_i, \hat{h}_i)$$.

**Tamaños del dataset de entrenamiento:**
- SNLI entailment: 112.700 pares (con términos de género)
- MNLI entailment: 21.500 pares (con términos de género)
- Total efectivo: ~134.200 pares de entrenamiento

**Ejemplo concreto (de la Figura 1 del paper):**
- $$p$$: *"A woman is working on furniture."*
- $$h$$: *"Woman putting together wooden shelf."*
- $$\hat{p}$$: *"A man is working on furniture."*
- $$\hat{h}$$: *"Man putting together wooden shelf."*

---

## Metodología: las tres pérdidas

### Notación común

- $$p_i, h_i$$: representación del encoder (CLS token) para la premisa e hipótesis del par $$i$$ original.
- $$\hat{p}_i, \hat{h}_i$$: representaciones del par aumentado con género intercambiado.
- $$m$$: tamaño del batch.
- $$\text{sim}(u, v)$$: similitud coseno entre vectores.
- $$\tau$$: temperatura (hiperparámetro que controla la "dureza" del contraste).

### Pérdida 1: Pérdida contrastiva de entailment ($$\mathcal{L}_{\text{CL}}$$)

Dados los $$m$$ cuádruplos del batch, cada par original $$(p_i, h_i)$$ forma un **par positivo** (la premisa y su hipótesis de entailment deben tener representaciones similares). Todos los otros elementos del batch son **pares negativos**. Lo mismo para el par aumentado $$(\hat{p}_i, \hat{h}_i)$$.

$$\mathcal{L}_{\text{CL}}^{(i)} = -\log \frac{e^{\text{sim}(p_i, h_i)/\tau}}{\sum_{j=1}^{m} e^{\text{sim}(p_i, h_j)/\tau} + e^{\text{sim}(p_i, \hat{h}_j)/\tau}} - \log \frac{e^{\text{sim}(\hat{p}_i, \hat{h}_i)/\tau}}{\sum_{j=1}^{m} e^{\text{sim}(\hat{p}_i, h_j)/\tau} + e^{\text{sim}(\hat{p}_i, \hat{h}_j)/\tau}}$$

$$\mathcal{L}_{\text{CL}} = \frac{1}{m} \sum_{i=1}^{m} \mathcal{L}_{\text{CL}}^{(i)}$$

**Interpretación paso a paso del primer término:**
- Numerador: similitud coseno entre $$p_i$$ y su hipótesis $$h_i$$ (el par positivo), escalada por temperatura.
- Denominador: suma de similitudes de $$p_i$$ con todas las hipótesis del batch (tanto originales $$h_j$$ como aumentadas $$\hat{h}_j$$). Incluir las versiones de género intercambiado $$\hat{h}_j$$ como negativos es crucial: hace que el modelo aprenda que *"A man is working on furniture"* y *"A woman is working on furniture"* son igualmente candidatos positivos o negativos según el contexto — no según el género.
- El logaritmo negativo penaliza cuando la similitud del par positivo es baja relativa a los negativos.
- Caso especial: si $$h_i = \hat{h}_i$$ (la hipótesis no contiene términos de género y la augmentación no la modifica), se excluye $$\hat{h}_i$$ del denominador para no tratar el mismo ejemplo como positivo y negativo simultáneamente.

El segundo término aplica la misma lógica al par aumentado: la premisa $$\hat{p}_i$$ debe ser cercana a su hipótesis $$\hat{h}_i$$.

**Efecto:** el espacio de embeddings se vuelve más isotrópico, y conceptos equivalentes a lo largo de distintas direcciones de género se acercan entre sí bajo similitud coseno.

### Pérdida 2: Pérdida de alineamiento ($$\mathcal{L}_{\text{AL}}$$)

Mientras $$\mathcal{L}_{\text{CL}}$$ trabaja con pares *entre* premisa e hipótesis (*inter-pair*), $$\mathcal{L}_{\text{AL}}$$ trabaja *dentro* de cada par: exige que el par original y su versión aumentada tengan la misma similitud coseno interna.

$$\mathcal{L}_{\text{AL}} = \frac{1}{m} \sum_{i=1}^{m} \left(\text{sim}(\hat{p}_i, \hat{h}_i) - \text{sim}(p_i, h_i)\right)^2$$

**Interpretación:** Si *"A woman is working on furniture" → "Woman putting together wooden shelf"* tiene similitud coseno 0.8, el modelo debe asignar exactamente la misma similitud a *"A man is working on furniture" → "Man putting together wooden shelf"*. La diferencia al cuadrado penaliza cualquier divergencia. Un modelo sin sesgo de género asignaría la misma similitud a dos pares idénticos semánticamente excepto por el género.

### Pérdida 3: Masked Language Modeling ($$\mathcal{L}_{\text{MLM}}$$)

Pérdida estándar de BERT: se enmascara el 15% de los tokens en todas las oraciones y el modelo aprende a predecir los tokens originales a partir del contexto. Esta pérdida es **crítica para preservar las capacidades lingüísticas del modelo**.

La ablación muestra que sin $$\mathcal{L}_{\text{MLM}}$$, el LM score en StereoSet colapsa de 84.6 a 55.8 — el modelo pierde completamente la coherencia del lenguaje. La causa: sin MLM, el encoder no puede reconstruir representaciones a nivel de token necesarias para el vocabulary head, desconectando el modelo de su capacidad de generar texto.

### Objetivo combinado

$$\mathcal{L} = (1-\alpha) \cdot \mathcal{L}_{\text{CL}} + \alpha \cdot \mathcal{L}_{\text{AL}} + \lambda \cdot \mathcal{L}_{\text{MLM}}$$

- $$\alpha = 0.05$$: pondera el balance entre $$\mathcal{L}_{\text{CL}}$$ (que mejora el ICAT en StereoSet) y $$\mathcal{L}_{\text{AL}}$$ (que mejora el Bias-NLI). Valores mayores de $$\alpha$$ favorecen equidad en similitud intra-par a costa de separación inter-par.
- $$\lambda = 0.1$$: atemperada la contribución del MLM para no dominar el objetivo de debiasing.
- Learning rate: $$5 \times 10^{-5}$$, batch size 32, 2 épocas, 4× NVIDIA RTX 3090.

---

## Datasets utilizados

### Datos de entrenamiento

**SNLI** (Bowman et al., 2015): 190K pares de implicación textual basados en descripciones de imágenes Flickr. Oraciones cortas y sintácticamente simples.

**MNLI** (Williams et al., 2018): 130K pares de NLI de múltiples géneros: conversaciones telefónicas, ficción, cartas del gobierno, artículos de viaje, etc. Más diverso semánticamente que SNLI.

### Evaluación intrínseca de sesgo

**StereoSet** (Nadeem et al., 2021): Context Association Tests intra-oración para dominio de género. 2.313 ejemplos. Métricas: LM score (coherencia lingüística), Stereotype Score (SS; 50 = sin sesgo), ICAT = $$\text{LM} \cdot \min(\text{SS}, 100-\text{SS}) / 50$$.

**CrowS-Pairs** (Nangia et al., 2020): 266 pares de género mínimamente distintos. Métrica: Stereotype Score; 50 = sin sesgo.

### Evaluación extrínseca de sesgo

**Bias-in-Bios** (De-Arteaga et al., 2019): 206.511 biografías en tercera persona con anotación de profesión (28 categorías) y género. Se evalúa la brecha en tasa de verdaderos positivos (TPR gap) entre hombres y mujeres al clasificar profesiones: $$\text{GAP}^{\text{TPR}} = |TPR_M - TPR_F|$$ (↓ mejor).

**Bias-NLI** (Dev et al., 2020): Dataset sintético de NLI con pares de oraciones construidos desde plantillas con palabras de género y ocupación. Métricas: Net Neutral (TN ↑), Fraction Neutral (FN ↑), Threshold:τ (T:τ ↑). Un modelo imparcial asignaría etiqueta *neutral* a todos los pares (ninguna implicación debería derivarse del género o la ocupación).

**WinoBias** (Zhao et al., 2018): Resolución de correferencias con sesgo de género en profesiones. Tipos 1 (requiere conocimiento del mundo) y 2 (resoluble por sintaxis). Métricas: TPR gap entre contextos pro-estereotípicos y anti-estereotípicos (↓ mejor).

### Evaluación de capacidades generales

**GLUE** (Wang et al., 2019): 8 tareas de NLU: CoLA, SST-2, MRPC, QQP, MNLI, QNLI, RTE, STS-B.

---

## Resultados principales

### StereoSet y CrowS-Pairs (evaluación intrínseca)

| Modelo | LM ↑ | SS StereoSet | ICAT ↑ | SS CrowS-Pairs |
|---|:---:|:---:|:---:|:---:|
| BERT baseline | 84.17 | 60.28 | 66.86 | 57.25 |
| CDA | 83.08 | 59.61 | 67.11 | 56.11 |
| Dropout | 83.04 | 60.66 | 65.34 | 55.34 |
| SentenceDebias | 84.20 | 59.37 | 68.42 | 52.29 |
| ContextDebias | 85.42 | 59.35 | 69.45 | 58.01 |
| INLP | 80.63 | 57.25 | 68.94 | 51.15 |
| FairFil | 44.85 | 50.93 | 44.01 | 49.03 |
| **MABEL** | **84.80** | **56.92** | **73.07** | **50.76** |

MABEL logra el **mejor ICAT (73.07)** y el **mejor SS en CrowS-Pairs (50.76, casi 0 de sesgo)**. FairFil logra SS=50.93 pero destruye el LM score (44.85), haciendo el modelo inutilizable.

### Bias-in-Bios (extrínsecos)

| Modelo | Accuracy ↑ | TPR GAP ↓ | TPR RMS ↓ |
|---|:---:|:---:|:---:|
| BERT | 84.14% | 1.189 | 0.144 |
| SentenceDebias | 83.56% | 1.180 | 0.144 |
| ContextDebias | 83.67% | 0.931 | 0.137 |
| FairFil | 83.18% | 0.746 | 0.142 |
| **MABEL** | **84.85%** | **0.599** | **0.132** |

MABEL tiene la **mayor accuracy** entre todos los métodos agnósticos de tarea Y el menor TPR GAP — el único método que mejora simultáneamente equidad y rendimiento.

### Bias-NLI (extrínsecos)

| Modelo | TN ↑ | FN ↑ | T:0.5 ↑ | T:0.7 ↑ |
|---|:---:|:---:|:---:|:---:|
| BERT | 0.799 | 0.879 | 0.874 | 0.798 |
| SentenceDebias | 0.793 | 0.911 | 0.897 | 0.788 |
| ContextDebias | 0.878 | 0.968 | 0.902 | 0.857 |
| **MABEL** | **0.900** | **0.983** | **0.974** | **0.968** |

MABEL supera a todos los baselines en las cuatro métricas de Bias-NLI.

### WinoBias

| Modelo | 1A (anti, tipo 1) ↑ | 1P (pro, tipo 1) | TPR-1 ↓ | 2A (anti, tipo 2) ↑ | TPR-2 ↓ |
|---|:---:|:---:|:---:|:---:|:---:|
| BERT | 53.96 | 86.57 | 32.79 | 82.20 | 12.48 |
| ContextDebias | 59.40 | 85.54 | 26.14 | 83.63 | 9.57 |
| **MABEL** | **61.21** | 84.93 | **23.73** | **92.78** | **3.41** |

MABEL logra el menor TPR gap en ambos tipos (+7.25% en tipo 1, +10.58% en tipo 2 vs BERT).

### GLUE (preservación de capacidades)

MABEL obtiene un promedio GLUE de 82.0, prácticamente igual al BERT baseline (81.8) y superior a SentenceDebias (79.4), ContextDebias (79.4) y FairFil (80.9).

---

## Ejemplo ilustrativo

Considérense estas dos oraciones de entailment en el batch:

- Oración A (original): *"A woman is working on furniture."*
- Oración B (aumentada): *"A man is working on furniture."*
- Hipótesis A: *"Woman putting together wooden shelf."*
- Hipótesis B: *"Man putting together wooden shelf."*

En BERT original, $$\text{sim}(A, h_A) \neq \text{sim}(B, h_B)$$ porque "woman" y "man" activan representaciones distintas. MABEL entrena para que:
1. **$$\mathcal{L}_{\text{CL}}$$**: A sea cercana a $$h_A$$ y B a $$h_B$$, usando todas las demás oraciones como negativas. Al incluir ambas versiones como negativos para la otra, el modelo no puede usar el género para distinguir positivos de negativos.
2. **$$\mathcal{L}_{\text{AL}}$$**: $$\text{sim}(A, h_A) = \text{sim}(B, h_B)$$ — la carpintería debe ser igual de próxima al rol de "mujer trabajando" que al de "hombre trabajando".
3. **$$\mathcal{L}_{\text{MLM}}$$**: El modelo sigue siendo capaz de generar tokens correctos en contexto.

---

## Ablación: contribución de cada componente

La ablación de las tres pérdidas sobre StereoSet + Bias-NLI revela:

| Configuración | LM ↑ | SS | ICAT ↑ | Bias-NLI FN ↑ |
|---|:---:|:---:|:---:|:---:|
| MABEL completo | 84.6 | 56.2 | 74.0 | 0.983 |
| Sin $$\mathcal{L}_{\text{MLM}}$$ | 55.8 | 51.1 | 54.6 | 0.976 |
| Sin $$\mathcal{L}_{\text{CL}}$$ | 84.9 | 57.2 | 72.6 | 0.884 |
| Sin $$\mathcal{L}_{\text{AL}}$$ | 85.0 | 57.3 | 72.6 | 0.890 |

- Sin MLM: el LM score colapsa (55.8), haciendo el modelo inutilizable.
- Sin $$\mathcal{L}_{\text{CL}}$$: Bias-NLI cae de 0.983 a 0.884 — la pérdida contrastiva es crucial para la equidad en NLI.
- Sin $$\mathcal{L}_{\text{AL}}$$: resultado casi igual a sin $$\mathcal{L}_{\text{CL}}$$ — ambas pérdidas son necesarias.

La ablación del tipo de datos también es reveladora: usar pares de contradicción (en lugar de entailment) colapsa el LM a 76.9 y empeora el SS. Los pares de entailment son los únicos que preservan la calidad lingüística mientras mejoran la equidad.

---

## Ventajas respecto a trabajos anteriores

- **Sin arquitectura adicional**: FairFil requiere una capa de proyección adicional y carece de MLM head. MABEL solo usa el encoder estándar de BERT con tres pérdidas.
- **Mejor trade-off equidad/rendimiento**: es el único método que simultáneamente mejora las métricas de sesgo Y mantiene el rendimiento GLUE a nivel del BERT original.
- **Datos gratuitos y estructurados**: aprovecha los 300K pares SNLI+MNLI ya existentes, transformados en datos de debiasing con CDA. No requiere nuevas anotaciones.
- **Evaluación multidimensional**: el paper señala que las métricas intrínsecas (SEAT, StereoSet) tienen alta varianza y pueden no correlacionar con el rendimiento extrínseco; MABEL es el único método que evalúa sistemáticamente en benchmarks intrínsecos Y extrínsecos Y downstream.
- **SimCSE como control**: la comparación con SimCSE (mismo entrenamiento NLI pero sin augmentación de género) muestra que las ganancias vienen del debiasing, no solo del pre-entrenamiento en NLI.

---

## Trabajos previos relacionados

El paper divide los trabajos previos en métodos específicos por tarea (task-specific) y métodos agnósticos de tarea (task-agnostic), siendo MABEL de la segunda categoría.

- **Ravfogel et al. (2020) — INLP (Null It Out)**: proyección iterativa que elimina información de atributos protegidos del espacio de embeddings mediante clasificadores lineales iterativos. Requiere datos anotados con género. Baseline principal.
- **Liang et al. (2020) — SentenceDebias**: computa el subespacio de género a partir de múltiples corpora y lo proyecta fuera de las representaciones. Task-agnostic. Baseline principal; MABEL supera en todas las métricas.
- **Kaneko & Bollegala (2021) — ContextDebias**: elimina el subespacio de género de representaciones contextualizadas. Task-agnostic. Baseline principal.
- **Webster et al. (2020) — CDA + Dropout**: usa augmentación contrafactual de datos en texto de Wikipedia (1M pasos, ~36 horas en TPU) más dropout adicional. MABEL toma prestada la técnica CDA pero la aplica a pares NLI con mucho menor costo computacional.
- **Cheng et al. (2021) — [FairFil](2021_cheng_fairfil.html)**: método contrastivo task-agnostic sin datos NLI. El más comparable a MABEL en paradigma, pero sin aprovechar la estructura de entailment ni incluir MLM. MABEL supera en todos los benchmarks.
- **Gao et al. (2021) — SimCSE**: aprendizaje contrastivo de oraciones usando pares NLI. MABEL adapta este framework añadiendo augmentación de género y pérdida de alineamiento específica de fairness.
- **Goldfarb-Tarrant et al. (2021) — Intrinsic bias metrics do not correlate with application bias**: motiva la evaluación extrínseca de MABEL al demostrar que SEAT y otras métricas intrínsecas no correlacionan con el rendimiento en tareas reales.
- **Zhao et al. (2018) — [WinoBias](2021_nadeem_stereoset.html)**: dataset de correferencias con sesgo de género en profesiones; uno de los benchmarks extrínsecos principales.
- **De-Arteaga et al. (2019) — Bias-in-Bios**: dataset de 206K biografías con anotación de profesión y género; benchmark extrínseco de clasificación.

## Tags

`debiasing` `NLI` `contrastive-learning` `sesgo-de-género` `BERT`
