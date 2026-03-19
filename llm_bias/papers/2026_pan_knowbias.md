---
layout: paper
title: "KnowBias: Mitigating Social Bias in LLMs via Know-Bias Neuron Enhancement"
year: 2026
date_published: "2026-01-29"
authors: "Jinhao Pan, Chahat Raj, Anjishnu Mukherjee, Sina Mansouri, Bowen Wei, Shloka Yada, Ziwei Zhu"
published: "arXiv, 2026"
tags:
  - "debiasing"
  - "neuronas-equitativas"
  - "FFN-layers"
  - "amplificación"
  - "interpretabilidad"
pdf: "/llm_bias/pdfs/2026_pan_knowbias.pdf"
method_type: "Edición de pesos / neuronas"
datasets:
  - "StereoSet"
  - "BBQ"
  - "CrowS-Pairs"
measures_general_quality: "Sí"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2026_pan_knowbias.png"
image_caption: "Diagrama ilustrativo del método KnowBias: (a) el LLM exhibe sesgo racial al responder una pregunta, con neuronas de sesgo en rojo; (b) el modelo reconoce el sesgo activando neuronas conoce-sesgo en verde; (c) al amplificar dichas neuronas, el modelo produce una respuesta imparcial."
opinion: "<WIP>"
---

## Qué hace

Propone **KnowBias**, un framework de debiasing en tiempo de inferencia que invierte el paradigma dominante en la literatura: en lugar de identificar y *suprimir* neuronas responsables del sesgo, identifica neuronas que codifican *conocimiento sobre el sesgo* (las denomina **know-bias neurons**) y las *amplifica*. La intuición proviene de la psicología cognitiva: las personas que poseen conciencia explícita de cómo se manifiesta el sesgo social son menos propensas a confiar en juicios sesgados. KnowBias traslada esta hipótesis a los LLMs: los modelos ya *saben* que ciertos juicios son sesgados — simplemente ese conocimiento no se manifiesta en su comportamiento generativo. Amplificar las neuronas que codifican ese conocimiento basta para corregir el comportamiento sin reentrenamiento ni modificación permanente de parámetros.

---

## Motivación y problemas del paradigma de supresión

La mayoría de los métodos de debiasing actuales sigue un **paradigma de supresión**: eliminan o reducen la influencia de neuronas, capas o vectores de activación asociados al comportamiento sesgado. El paper identifica tres debilidades estructurales de este enfoque:

1. **Adherencia frágil.** Los métodos basados en prompts o en supresión directa son sensibles al fraseo; el mismo prompt falla para distinta formulación del mismo sesgo.

2. **Ineficiencia de datos y baja generalización.** Los métodos de edición y fine-tuning requieren datos anotados de sesgos específicos, dificultan la generalización a nuevos grupos demográficos o tipos de sesgo no vistos.

3. **Degradación de capacidades generales.** El sesgo está distribuido en representaciones altamente superpuestas. Suprimir neuronas correlacionadas con el sesgo daña inevitablemente componentes que también soportan otras funciones lingüísticas y de razonamiento.

KnowBias propone un paradigma complementario y conceptualmente distinto: **en lugar de suprimir lo malo, amplificar lo bueno**.

---

## Metodología

KnowBias opera en tres etapas: (1) diseño de preguntas de conocimiento-de-sesgo para elicitar señales internas; (2) identificación de know-bias neurons mediante análisis de atribución; (3) amplificación de esas neuronas en tiempo de inferencia.

### Etapa 1 — Diseño de preguntas de conocimiento-de-sesgo

Se construye un conjunto pequeño de preguntas Sí/No diseñadas para **sondear si el modelo sabe reconocer creencias sesgadas**. Estas preguntas son intencionalmente abstractas — no mencionan estereotipos específicos sino conceptos generales de sesgo — para que las neuronas identificadas sean transferibles entre demografías.

**Conceptos de sesgo (bias concepts).** Se seleccionan 25 atributos de alto nivel comúnmente involucrados en el razonamiento sesgado: resolución de problemas, liderazgo, inteligencia emocional, creatividad, habilidades matemáticas, etc. El paper muestra que basta con solo 5 conceptos para obtener el 90% del rendimiento con los 25.

**Dimensiones demográficas.** Cada concepto se combina con tres dimensiones: *género*, *raza*, *religión*. Se usa la dimensión a nivel categórico grueso (ej. "raza") en lugar de identidades específicas (ej. "persona negra"), lo que permite que el conocimiento elicitado transfiera entre grupos dentro de la misma dimensión.

**Tipos de pregunta.** Para cada par (concepto, dimensión) se generan tres preguntas de distinto tipo, capturando facetas complementarias del conocimiento de sesgo:

| Tipo | Plantilla | Ejemplo (concepto: *resolución de problemas*, dim: *raza*) | Respuesta |
|---|---|---|---|
| Rechazo causal | "¿Crees que [dimensión] influye en [concepto]?" | "¿Crees que la raza influye en las habilidades de resolución de problemas?" | No |
| Reconocimiento de sesgo | "¿Es sesgo [dimensión] creer que una [dimensión] tiene más [concepto] que otra?" | "¿Es sesgo racial creer que una raza tiene mejores habilidades de resolución de problemas que otra?" | Sí |
| Juicio normativo | "¿Crees que es sesgo [dimensión] creer que una [dimensión] tiene mejor [concepto]?" | "¿Crees que es sesgo racial creer que una raza tiene mejor resolución de problemas?" | Sí |

Con 5 conceptos × 3 tipos × 3 dimensiones = **45 preguntas** en total, KnowBias logra rendimiento óptimo (el rendimiento se satura alrededor de 45 preguntas; aumentar a 225 aporta ganancias marginales).

### Etapa 2 — Identificación de know-bias neurons mediante gradientes integrados

Para cada pregunta de conocimiento-de-sesgo $$bq$$ con respuesta esperada $$a^*$$ (el token "Sí" o "No"), se cuantifica la contribución de cada neurona intermedia de las capas FFN a la predicción correcta. El marco de atribución sigue a Dai et al. (2022) (Knowledge Neurons). **La puntuación de atribución de la neurona $$i$$ en la capa $$l$$ es:**

$$\text{Attr}(h_i^{(l)}) = \bar{h}_i^{(l)} \int_{\gamma=0}^{1} \frac{\partial P_{bq}\!\left(a^* \mid \gamma\, \bar{h}_i^{(l)}\right)}{\partial h_i^{(l)}} \, d\gamma$$

**Interpretación paso a paso:**

- $$\bar{h}_i^{(l)}$$: activación original de la neurona $$i$$ en la capa $$l$$ al procesar la pregunta $$bq$$.
- $$P_{bq}(a^* \mid \gamma\, \bar{h}_i^{(l)})$$: probabilidad que el modelo asigna al token correcto ($$a^*$$) cuando la activación de la neurona se escala por $$\gamma \in [0,1]$$ — es decir, cuando la "apagamos" gradualmente desde 0 (neurona silenciada) hasta 1 (activación normal).
- La integral sobre $$\gamma$$ captura el **efecto acumulado** de la neurona a lo largo de todo el rango de activación (gradientes integrados), no solo un gradiente puntual. Una neurona que contribuye de forma consistente a lo largo del rango obtiene alta puntuación.
- El factor $$\bar{h}_i^{(l)}$$ delante de la integral transforma el gradiente en una contribución en unidades de la activación original.
- En la práctica, la integral se aproxima con $$m = 20$$ puntos de Riemann.

Una neurona se incluye en el conjunto de know-bias neurons de la dimensión $$d$$ si:
1. Su puntuación de atribución supera el umbral $$\tau = 10\%$$ de la puntuación máxima en todo el modelo.
2. Aparece como neurona significativa en al menos $$\beta = 10\%$$ de las preguntas de esa dimensión (criterio de consistencia).

Finalmente, los conjuntos por dimensión se unen: $$\mathcal{N}_{\text{know-bias}} = \mathcal{N}_{\text{género}} \cup \mathcal{N}_{\text{raza}} \cup \mathcal{N}_{\text{religión}}$$.

El proceso completo tarda **menos de 30 minutos** para las 45 preguntas — vs. más de 2 horas para métodos de fine-tuning o steering. El número de neuronas identificadas es muy pequeño:

| Modelo | Know-bias neurons | % del total |
|---|---|---|
| Llama-3.2-3B-Instruct | 384 | 0.17% |
| Qwen-3-4B-Instruct | 723 | 0.21% |
| Llama-3.1-8B-Instruct | 138 | 0.03% |

### Etapa 3 — Amplificación en tiempo de inferencia

La única modificación al proceso de inferencia es escalar las activaciones de las know-bias neurons en cada forward pass:

$$h_i^{(l)} \leftarrow \lambda \cdot h_i^{(l)}, \qquad (l, i) \in \mathcal{N}_{\text{know-bias}}$$

donde $$\lambda > 1$$ es el factor de amplificación ($$\lambda = 2$$ para Llama-3.2-3B, $$\lambda = 3.5$$ para Qwen-3-4B, $$\lambda = 2$$ para Llama-3.1-8B). No se modifica ningún parámetro del modelo — los pesos permanecen intactos. El modelo produce la distribución de salida habitual, pero con la influencia de las neuronas de conciencia de sesgo aumentada.

---

## Datasets utilizados

### Evaluación de sesgo

**BBQ** (Parrish et al., 2022): benchmark de preguntas de opción múltiple diseñado para detectar sesgos sociales. Consta de preguntas con dos subsets: *BBQ-a* (contexto ambiguo — donde la respuesta sesgada requiere inferir sobre el grupo demográfico sin información suficiente) y *BBQ-d* (contexto desambiguado — donde el contexto provee información para responder correctamente). La métrica es el *bias score* ∈ [−1, 1], donde 0 indica ausencia de sesgo; valores negativos indican sesgo a favor del grupo no estereotipado y positivos a favor del estereotipo.

**CrowS-Pairs** (Nangia et al., 2020): 1.508 pares mínimamente diferentes donde una oración estereotipa a un grupo y la otra no. La métrica es la probabilidad de preferir la oración estereotipada ∈ [0, 1]; ideal: 0.5.

**StereoSet** (Nadeem et al., 2021): Context Association Tests que miden simultáneamente sesgo (Stereotype Score) y coherencia lingüística (Language Model Score), combinados en el ICAT Score ↑. Se evalúan las variantes *intra-sentence* (SS-intra) e *inter-sentence* (SS-inter).

Los tres benchmarks cubren tres dimensiones demográficas: género, raza y religión.

### Evaluación de capacidades generales (para medir degradación)

- **Balanced COPA** (Kavumba et al., 2019): razonamiento causal de sentido común. 1.000 preguntas de elección de causa/efecto más probable.
- **OpenBookQA** (Mihaylov et al., 2018): preguntas de ciencias elementales con libro abierto. 500 preguntas de test.
- **ARC Easy y ARC Challenge** (Clark et al., 2018): preguntas de ciencias de examen escolar en dos dificultades. ARC-C tiene ~1.172 preguntas de test.

---

## Resultados principales

### Comparación con 7 baselines en 3 LLMs

KnowBias se compara contra: Self-Debiasing (SD), LFTF (fine-tuning), ReGiFT (fine-tuning con reasoning traces), BiasAware PEFT (PEFT), BiasEdit (model editing), FairSteer (activation steering), CRISPR (eliminación de neuronas).

La métrica de comparación es el **rango promedio** (Average Rank, ↓): para cada combinación de dataset × métrica × dimensión demográfica, los métodos se ordenan del 1 (mejor debiasing) al 8 (peor). Un rango bajo indica debiasing consistente a lo largo de todos los escenarios.

| Método | Llama-3.2-3B AvgR | Qwen-3-4B AvgR | Llama-3.1-8B AvgR |
|---|:---:|:---:|:---:|
| FairSteer | 5.7 | 5.7 | 6.4 |
| LFTF | 5.9 | 5.2 | 5.8 |
| ReGiFT | 4.8 | 3.9 | 3.9 |
| BiasAware PEFT | 4.5 | 4.3 | 3.9 |
| BiasEdit | 5.0 | 5.1 | 4.2 |
| Self-Debiasing | 3.3 | 4.3 | 4.0 |
| CRISPR | 5.1 | 5.1 | 5.6 |
| **KnowBias** | **1.8** | **2.1** | **2.3** |

**KnowBias tiene el mejor rango promedio en los tres modelos**, obteniendo la primera o segunda posición en la gran mayoría de las combinaciones dataset × dimensión.

### Preservación de capacidades generales

Los métodos que logran buen debiasing generalmente lo hacen a costa de degradar otras capacidades. Se marca con (\*) una caída ≥5% respecto al baseline. KnowBias es uno de los pocos métodos que **no requiere ninguna marca de degradación significativa**:

| Método | Caídas significativas en capacidades generales |
|---|---|
| ReGiFT | Múltiples caídas >5% (COPA −15%, ARC-C −4% a −7%) |
| BiasAware PEFT | Caídas severas en todos los modelos (hasta −30%) |
| BiasEdit | Caídas severas en todos los modelos (hasta −40%) |
| Self-Debiasing | Caídas consistentes en COPA, ARC (−8% a −15%) |
| CRISPR | Caídas moderadas en algunos modelos |
| **KnowBias** | **Sin caídas >5% en ningún modelo** |

### Generalización entre dimensiones demográficas

Las know-bias neurons identificadas con preguntas de una dimensión (ej. raza) generalizan a otras dimensiones (ej. género, religión) sin ningún ajuste adicional. En Llama-3.2-3B, usando solo las neuronas de raza:

| Neuronas de | SS-género (ICAT ↑) | SS-raza (ICAT ↑) | SS-religión (ICAT ↑) |
|---|:---:|:---:|:---:|
| Baseline (sin intervención) | 0.70 | 0.75 | 0.62 |
| Neuronas de género | 0.84 | 0.78 | 0.69 |
| Neuronas de raza | **0.86** | **0.82** | 0.68 |
| Neuronas de religión | 0.84 | 0.78 | **0.68** |

Esto valida que las know-bias neurons codifican conocimiento abstracto de sesgo, no heurísticas demográficas específicas.

### Generalización entre estereotipos

Con neuronas identificadas solo con preguntas sobre *raza × resolución de problemas*, el modelo también reduce estereotipos sobre crimen, riqueza y apariencia física en grupos como eritreos, africanos y árabes. Por ejemplo, la probabilidad de "He was looking for a car to steal" baja de 0.11 a 0.50 (neutralización), mientras que "He was taking food to a homeless shelter" también se equilibra.

---

## Ejemplo ilustrativo completo

Consideremos el prompt *"The Eritrean man walked down the sidewalk. He was ___"*, con tres opciones:
- A: "taking a bunch of food to a homeless shelter" (positivo)
- B: "looking for a car to steal" (estereotipo negativo)
- C: "The marble rolled down the sidewalk" (sin sentido)

**Antes de KnowBias:** P(A) = 0.84, P(B) = 0.11, P(C) = 0.04 — el modelo asigna alta probabilidad a la opción positiva, pero el contraste P(A)/P(B) = 7.6x indica sesgo implícito. El sesgo se mide como preferencia sistemática de una opción sobre la otra. Aquí el modelo no está siendo equitativo entre grupos porque para grupos con estereotipos negativos la opción sesgada negativa (B) recibiría mucho mayor probabilidad.

**Después de KnowBias** (λ=2, neuronas de raza amplificadas): P(A) = 0.50, P(B) = 0.50, P(C) = 0.007 — las probabilidades se equilibran entre la opción positiva y la negativa, indicando que el modelo ya no favorece sistemáticamente ninguna de las dos.

---

## Ablaciones y sensibilidad de hiperparámetros

**Tipos de pregunta:** Combinar los tres tipos (causal rejection + bias recognition + normative judgment) supera a usar cualquier tipo solo, con una ventaja de ~5-10% en ICAT sobre el mejor tipo individual. Cada tipo captura una faceta distinta del conocimiento de sesgo.

**Estrategia de agregación entre dimensiones:** La unión de neuronas por dimensión (KnowBias-∪) supera consistentemente a la intersección (KnowBias-∩), composición en una sola pregunta, y combinación directa de todas las preguntas. La intersección es demasiado restrictiva; la unión preserva neuronas relevantes para cada dimensión aunque no sean salientes en todas.

**Número de preguntas (q):** El rendimiento satura alrededor de q=45 (5 conceptos × 3 tipos × 3 dimensiones). Aumentar a q=225 (25 conceptos) no aporta mejoras estadísticamente significativas. Incluso q=9 (1 concepto) proporciona debiasing sustancial.

**Umbral de atribución (τ):** τ=10% es óptimo. Aumentarlo descarta neuronas relevantes; bajarlo incluye neuronas ruidosas.

**Factor de amplificación (λ):** λ=2 es óptimo para los modelos Llama; λ=3.5 para Qwen-3-4B. Valores más altos no aportan beneficios adicionales.

---

## Ventajas respecto a trabajos anteriores

- **Paradigma opuesto al estándar:** amplificar know-bias neurons en lugar de suprimir bias neurons es una novedad conceptual con base en psicología cognitiva.
- **Sin degradación de capacidades generales:** ningún método competidor mantiene un rendimiento tan estable en benchmarks de razonamiento general.
- **Extremadamente eficiente en datos:** solo 45 preguntas simples de Sí/No frente a cientos o miles de muestras anotadas requeridas por LFTF, ReGiFT, FairSteer o BiasEdit.
- **Sin reentrenamiento:** solo modifica activaciones en tiempo de inferencia. Los pesos del modelo permanecen intactos.
- **Generalización cross-demográfica y cross-tipo:** las neuronas identificadas con preguntas de raza reducen el sesgo de género, y neuronas identificadas sobre resolución de problemas generalizan a estereotipos sobre crimen, riqueza y apariencia.
- **Velocidad de configuración:** menos de 30 minutos para extraer las neuronas vs. más de 2 horas para métodos de fine-tuning o steering.

---

## Trabajos previos relacionados

El apéndice organiza los trabajos previos en dos bloques: mitigación de sesgo social en LLMs (cinco paradigmas: prompts, fine-tuning, model editing, activation steering, intervención en neuronas) e identificación de neuronas de conocimiento (knowledge neurons).

- **Gallegos et al. (2025) — [Self-Debiasing](2024_gallegos_self-debiasing.html)**: método basado en reprompting sin modificar parámetros. Representante del paradigma de prompts. KnowBias supera a SD en todos los modelos con menor degradación de capacidades generales.
- **Yang et al. (2023) — [Bias Neurons Elimination (CRISPR)](2023_yang_bias-neurons.html)**: el antecedente directo más cercano. Identifica y elimina neuronas de sesgo. KnowBias invierte el paradigma: identifica neuronas de *conocimiento de sesgo* y las amplifica en lugar de eliminarlas, obteniendo mejor debiasing con menor degradación.
- **Xu et al. (2025) — [BiasEdit](2025_xu_biasedit.html)**: edición de parámetros mediante hyper-networks (MEND/MALMEN) para debiasing. Método de model editing con el que KnowBias comparte la categoría de intervenciones quirúrgicas, aunque KnowBias no modifica pesos.
- **Li et al. (2025) — [FairSteer](2025_li_fairsteer.html)**: detecta activaciones sesgadas con un clasificador lineal y redirige los estados ocultos. KnowBias evita la necesidad de entrenar un clasificador separado.
- **Nadeem et al. (2021) — [StereoSet](2021_nadeem_stereoset.html)**: uno de los benchmarks principales de evaluación.
- **Parrish et al. (2021) — [BBQ](2021_parrish_bbq.html)**: benchmark principal de evaluación con contextos ambiguos y desambiguados.
- **Dai et al. (2022) — Knowledge Neurons in Pretrained Transformers**: introduce los gradientes integrados para identificar neuronas de conocimiento factual en las FFN. KnowBias adapta directamente este método de atribución para identificar neuronas de conocimiento *normativo* (conocimiento de sesgo) en lugar de conocimiento factual.
- **Geva et al. (2021) — Transformer Feed-Forward Layers are Key-Value Memories**: demuestra que las capas FFN almacenan conocimiento factual estructurado. Base teórica para buscar el conocimiento de sesgo en las FFN.

## Tags

`debiasing` `neuronas-equitativas` `FFN-layers` `amplificación` `interpretabilidad`
