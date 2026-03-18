---
layout: paper
title: "Finding Skill Neurons in Pre-trained Transformer-based Language Models"
year: 2022
date_published: "2022-11-14"
authors: "Xiaozhi Wang, Kaiyue Wen, Zhengyan Zhang, Lei Hou, Zhiyuan Liu, Juanzi Li"
published: "EMNLP, 2022"
tags:
  - "interpretabilidad"
  - "skill-neurons"
  - "FFN-layers"
  - "transformers"
  - "modularidad"
pdf: "/llm_bias/pdfs/2022_wang_skill-neurons.pdf"
status:
  - "Leido"
image: "imgs/2022_wang_skill-neurons.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---

## Qué hace

Este paper identifica y valida la existencia de **neuronas de habilidad** (*skill neurons*) en las capas FFN de transformers preentrenados: neuronas individuales cuyas activaciones, medidas sobre soft prompts, son altamente predictivas de la etiqueta correcta para tareas lingüísticas específicas (análisis de sentimientos, NLI, clasificación de temas, etc.). Los autores proponen una fórmula de puntuación de predictividad para cada neurona, demuestran causalmente que las neuronas top-k son cruciales para la tarea correspondiente (mediante perturbación), muestran que son específicas por tarea (baja superposición entre tareas distintas), y argumentan que emergen durante el preentrenamiento y no como artefacto del prompt tuning.

## Contexto y motivación

Los modelos de lenguaje preentrenados (PLMs) como BERT y RoBERTa adquieren durante el preentrenamiento un amplio espectro de habilidades lingüísticas, pero los mecanismos por los cuales estas habilidades se distribuyen entre los parámetros del modelo son poco conocidos. Trabajos previos han mostrado que las capas FFN actúan como memorias clave-valor (Geva et al., 2021) y que ciertos conocimientos factuales se localizan en neuronas específicas (Dai et al., 2021). Sin embargo, no existía un estudio sistemático que preguntara: ¿hay neuronas que se especializan en *habilidades* lingüísticas completas (análisis de sentimientos, inferencia natural, etc.) en lugar de en hechos factuales puntuales?

El paper responde esta pregunta con un enfoque novedoso: en lugar de intervenir sobre los pesos o usar probing classifiers sobre las activaciones en texto libre, usa **prompt tuning** como lente de observación. La hipótesis es que, tras encontrar un soft prompt óptimo para una tarea, las neuronas más predictivas de las etiquetas con ese prompt son precisamente las que el modelo aprendió a asociar con esa habilidad durante el preentrenamiento.

## Tarea estudiada

El paper no estudia una sola tarea sino el problema meta de **localizar las neuronas responsables de distintas habilidades lingüísticas** en un PLM. Las habilidades concretas estudiadas incluyen:

- **Análisis de sentimientos**: SST-2 (reseñas de películas, etiqueta positivo/negativo), IMDB, Tweet Sentiment.
- **Inferencia en lenguaje natural (NLI)**: MNLI (tres clases: entailment, contradiction, neutral), QNLI.
- **Clasificación de temas**: AG News (4 categorías), DBpedia (14 categorías).

**Ejemplo concreto para SST-2:** El input es "[soft_prompt] This movie is absolutely wonderful." y la etiqueta correcta es "positive". Después de hacer prompt tuning, los autores buscan qué neuronas de las capas FFN tienen activaciones que, comparadas con el promedio de activaciones para esa neurona, predicen correctamente si el input es positivo o negativo.

Para cada neurona $\mathcal{N}$ y cada token del soft prompt $p_i$, la activación en el i-ésimo token del soft prompt se usa como señal de predicción — la idea es que el soft prompt concentra en ciertos tokens la información de tarea, por lo que las neuronas que más responden a esos tokens son las más relevantes para la habilidad.

## Metodología

### Definición formal de neurona

En una capa FFN del transformer, la operación se define como:

$$\text{FFN}(\mathbf{x}) = f(\mathbf{x} \mathbf{K}^\top + \mathbf{b}_1) \mathbf{V} + \mathbf{b}_2$$

donde $\mathbf{x} \in \mathbb{R}^d$ es el vector de representación del token, $f(\cdot)$ es la función de activación (GELU en BERT), y $\mathbf{K}, \mathbf{V} \in \mathbb{R}^{d_m \times d}$ son las matrices de parámetros. La activación de la neurona $i$ se define como:

$$\mathbf{a} = f(\mathbf{x} \mathbf{K}^\top + \mathbf{b}_1) \in \mathbb{R}^{d_m}$$

donde $a_i$ (el i-ésimo elemento de $\mathbf{a}$) es la activación de la neurona $i$.

### Fórmula del skill neuron score

El proceso de cálculo del score de predictividad de una neurona $\mathcal{N}$ para una tarea dada tiene cinco pasos:

**Paso 1 — Activación de línea base.** Para cada token del soft prompt $p_i$, se calcula la activación media de la neurona $\mathcal{N}$ sobre todos los ejemplos del conjunto de entrenamiento:

$$\text{absl}(\mathcal{N}, p_i) = \frac{1}{|\mathcal{D}_\text{train}|} \sum_{(x_j, y_j) \in \mathcal{D}_\text{train}} a(\mathcal{N}, p_i, x_j)$$

donde $a(\mathcal{N}, p_i, x_j)$ es la activación de la neurona $\mathcal{N}$ en el token de posición $p_i$ cuando el modelo procesa el ejemplo $x_j$.

**Interpretación:** Este valor de línea base funciona como un umbral: si la activación de la neurona supera la media, el modelo predice la etiqueta positiva (clase 1); si está por debajo, predice la negativa (clase 0) — o viceversa, dependiendo de la correlación.

**Paso 2 — Precisión de predicción.** Se evalúa qué tan bien predice la neurona la etiqueta en el conjunto de validación:

$$\text{Acc}(\mathcal{N}, p_i) = \frac{\sum_{(x_j, y_j) \in \mathcal{D}_\text{dev}} \mathbb{1}\left[\mathbb{1}[a(\mathcal{N}, p_i, x_j) > \text{absl}(\mathcal{N}, p_i)] = y_j\right]}{|\mathcal{D}_\text{dev}|}$$

La neurona predice la clase positiva cuando su activación supera la línea base. Si el resultado es peor que azar (Acc < 0.5), significa que la correlación es negativa (activación alta → clase negativa), lo que es igualmente informativo.

**Paso 3 — Predictividad bilateral.** Para capturar tanto correlaciones positivas como negativas con la etiqueta:

$$\text{Pred}(\mathcal{N}, p_i) = \max(\text{Acc}(\mathcal{N}, p_i),\; 1 - \text{Acc}(\mathcal{N}, p_i))$$

**Interpretación:** Una predictividad de 1.0 significa que la neurona discrimina perfectamente entre clases; una predictividad de 0.5 (valor máximo para clasificación aleatoria binaria) significa que la neurona es completamente no informativa.

**Paso 4 — Agregación sobre trials de prompt tuning.** El prompt tuning tiene varianza aleatoria (depende de la inicialización). Para robustez, se repite $|\mathcal{P}|=5$ veces con distintas semillas, obteniendo 5 conjuntos de soft prompts $\{P_1, P_2, P_3, P_4, P_5\}$. El score final agrega las predictividades tomando el mejor token de cada trial y luego promediando:

$$\text{Pred}(\mathcal{N}) = \frac{1}{|\mathcal{P}|} \sum_{P_i \in \mathcal{P}} \max_{p_j \in P_i} \text{Pred}(\mathcal{N}, p_j)$$

**Interpretación:** Para cada uno de los 5 trials, se toma el token del soft prompt que mejor predice con esa neurona (el $\max$ interno), y luego se promedia sobre los 5 trials. Esto hace que la puntuación sea robusta a variaciones en el proceso de optimización del prompt.

**Paso 5 — Extensión a clasificación multi-clase.** Para tareas con más de dos clases (e.g., MNLI con 3 clases, AG News con 4 clases), la tarea se descompone en subtareas binarias. Por ejemplo, MNLI se descompone en: "Entailment vs. otros" y "Neutral vs. otros". Las skill neurons de la tarea multi-clase son la unión de las top-k neuronas de cada subtarea binaria (k/2 por subtarea para k total).

### Experimentos de validación

Identificadas las skill neurons, se realizan tres tipos de experimentos para confirmar que son causalmente importantes y no solo correlacionadas:

**Perturbación (knockout):** Se añade ruido gaussiano $\mathcal{N}(0, \sigma^2)$ a las activaciones de las neuronas seleccionadas durante la inferencia. Los autores reportan resultados para $\sigma = 0.1$. Se comparan tres condiciones: perturbar el top-k% de skill neurons, perturbar un k% aleatorio de neuronas, y perturbar un k% de neuronas con los *menores* scores.

**Pruning estructurado:** Se fija la activación de todas las neuronas *excepto* el top-2% de skill neurons a su valor de línea base (promedio sobre el corpus de entrenamiento), reduciendo el 98% de los parámetros de las capas FFN. Se mide el rendimiento y la velocidad del modelo podado.

**Análisis de especificidad por tarea:** Se calcula la correlación de Spearman entre los rankings de predictividad de distintas tareas: $\rho(\text{Pred}_{T_1}, \text{Pred}_{T_2})$. Una correlación alta indica que las mismas neuronas son skill neurons para ambas tareas (alta superposición); una correlación baja indica especificidad.

**Evidencia de origen en preentrenamiento:** Se comparan tres configuraciones de prompts: (a) soft prompts entrenados con prompt tuning, (b) hard prompts escritos manualmente, (c) prompts aleatorios sin significado. Si las skill neurons identificadas con prompts aleatorios tienen predictividad no trivial, ello sugiere que las neuronas ya eran informativas antes del fine-tuning.

## Componentes / Hallazgos

### Las skill neurons son causalmente importantes

Perturbar el top-20% de skill neurons causa una caída de accuracy de ~70% a ~45% en la tarea Tweet Sentiment, mientras que perturbar el 20% de neuronas aleatorias solo la reduce a ~65%. Este patrón se repite consistentemente en todas las tareas: el daño producido por perturbar skill neurons es 3–5x mayor que el daño por perturbar neuronas aleatorias.

### Las skill neurons son específicas por tarea

La correlación de Spearman entre los rankings de skill neurons de SST-2 e IMDB (ambas de análisis de sentimientos) es $\rho = 0.65$ — alta superposición porque comparten la misma habilidad. La correlación entre SST-2 y AG News (clasificación de temas) es $\rho = 0.15$ — baja superposición. Este patrón confirma que las skill neurons codifican la habilidad específica, no solo capacidad lingüística general.

### Las skill neurons están concentradas en capas medias-altas

El análisis por capa muestra que las neuronas de capas bajas (1–4) tienen correlaciones inter-tarea más altas ($\rho \approx 0.40$ entre SST-2 y AG News en capa 1), mientras que las capas altas (10–12) muestran correlaciones muy bajas ($\rho \approx 0.10$ en capa 12). Esto es consistente con la literatura de probing: las capas bajas codifican propiedades lingüísticas generales y las capas altas propiedades específicas de la tarea.

### Las skill neurons emergen durante el preentrenamiento

Con prompts aleatorios (sin significado), las neuronas de mayor predictividad mantienen scores no triviales: para SST-2, el top-1 neurona tiene predictividad de 0.78 con un prompt aleatorio (vs. 0.83 con hard prompt manual y 0.91 con soft prompt entrenado). Esto indica que la capacidad discriminativa de las skill neurons no es un artefacto del prompt tuning sino una propiedad preexistente del modelo.

### El pruning a top-2% mantiene rendimiento comparable

Conservar solo el 2% de neuronas con mayor skill neuron score (y fijar el resto a sus valores de línea base) produce modelos con rendimiento comparable al modelo completo en la mayoría de tareas, con un speedup de ~1.34x gracias a la computación dispersa.

## Ejemplo ilustrativo

**Caso: SST-2 (análisis de sentimientos) en BERT-base.**

BERT-base tiene 12 capas con 3.072 neuronas FFN por capa, para un total de 36.864 neuronas en las capas FFN.

Tras 5 trials de prompt tuning sobre el conjunto de entrenamiento de SST-2 (67.349 ejemplos), se calculan los scores de predictividad para las 36.864 neuronas.

**Top skill neuron (ejemplo ilustrativo):**
- Capa 11, neurona 847 (valores ficticios para ilustrar el mecanismo).
- Activación media (línea base) sobre el corpus: $\text{absl} = 0.43$.
- En ejemplos positivos ("This movie is wonderful!"): activación promedio de ~0.78.
- En ejemplos negativos ("This movie is terrible!"): activación promedio de ~0.21.
- Accuracy de predicción: $\text{Acc} = 0.83$ → Predictividad $= 0.83$.

**Knockout del top-50% de skill neurons en SST-2:**
- Accuracy del modelo completo con prompt tuning: 91.8 ± 0.5%.
- Accuracy tras perturbar el top-50% de skill neurons: ~60%.
- Accuracy tras perturbar el 50% aleatorio de neuronas: ~75%.
- Accuracy tras perturbar el bottom-50% (menores scores): ~88%.

Esto confirma que las skill neurons concentran la información discriminativa de forma desproporcionada.

**Transferibilidad como indicador:** Los autores usan el solapamiento de skill neurons entre dos modelos fine-tuneados en distintas tareas como predictor de transferibilidad (cuánto ayuda adaptar un modelo a tarea A para luego adaptarlo a tarea B). El coeficiente de Spearman entre solapamiento de skill neurons y transferibilidad es $\rho = 0.71$, un 34% mejor que la métrica de solapamiento de neuronas sin filtrado ($\rho = 0.53$).

## Resultados principales

### Scores de predictividad (top-1 neurona vs. azar)

| Tarea | Predictividad top-1 neurona | Línea base aleatoria |
|-------|----------------------------|---------------------|
| SST-2 | 0.83 | 0.50 |
| IMDB | 0.82 | 0.50 |
| Tweet | 0.67 | 0.33 |
| MNLI | 0.71 | 0.33 |
| QNLI | 0.69 | 0.50 |
| AG News | 0.96 | 0.25 |
| DBpedia | 0.99 | 0.07 |

### Rendimiento del modelo podado (top-2% skill neurons, 66.6% reducción de parámetros FFN)

| Tarea | Accuracy original | Accuracy podado | Speedup |
|-------|-------------------|-----------------|---------|
| SST-2 | 91.8 ± 0.5 | 89.3 ± 2.0 | 1.34x |
| IMDB | 91.6 ± 0.5 | 87.6 ± 3.0 | 1.34x |
| Tweet | 70.0 ± 0.2 | 69.0 ± 0.9 | 1.34x |
| MNLI | 76.8 ± 1.8 | 70.0 ± 1.1 | 1.38x |
| QNLI | 85.7 ± 0.7 | 81.0 ± 1.0 | 1.36x |
| AG News | 98.8 ± 0.1 | 99.8 ± 0.1 | 1.32x |
| DBpedia | 99.7 ± 0.1 | 99.0 ± 0.1 | 1.33x |

### Predictividad con distintos tipos de prompt (evidencia de origen en preentrenamiento)

| Tarea | Prompt aleatorio | Hard prompt manual | Soft prompt entrenado |
|-------|-----------------|-------------------|-----------------------|
| SST-2 | 78.1 ± 0.4 | 83.3 | 91.6 ± 0.3 |
| IMDB | 76.7 ± 2.0 | 75.1 | 92.0 ± 0.3 |
| AG News | 96.0 ± 0.3 | 95.9 | 98.9 ± 0.1 |

La predictividad no trivial incluso con prompts aleatorios es la evidencia más fuerte del origen en preentrenamiento.

### Especificidad por tarea (correlación de Spearman)
- SST-2 vs. IMDB (misma habilidad, sentimientos): $\rho = 0.65$ — alta superposición esperada.
- SST-2 vs. AG News (habilidades distintas): $\rho = 0.15$ — baja superposición, alta especificidad.

## Ventajas respecto a trabajos anteriores

- **Primer estudio sistemático de skill neurons en PLMs**: los trabajos previos identificaban neuronas para hechos factuales (Dai et al., 2021) o propiedades lingüísticas superficiales (POS, parsing), pero no para *habilidades de tarea* definidas funcionalmente.
- **Método de identificación sin intervención en los pesos**: el skill neuron score se calcula solo observando activaciones durante la inferencia, sin necesidad de fine-tuning ni modificación del modelo — esto hace el método aplicable a cualquier PLM sin acceso a los gradientes de entrenamiento.
- **Evidencia causal en lugar de correlacional**: la prueba de perturbación va más allá de mostrar que las neuronas tienen activaciones correlacionadas con la tarea; demuestra que perturbarlas *causa* degradación de rendimiento, a diferencia de los enfoques puramente de probing.
- **El pruning basado en skill neurons tiene mejor relación rendimiento/eficiencia** que el pruning no estructurado estándar (que requiere re-entrenamiento), ya que el criterio de selección es funcionalmente informado.
- **La transferibilidad como aplicación práctica**: usar el solapamiento de skill neurons como indicador de transferibilidad entre tareas es una aplicación directa con valor para la selección de estrategias de adaptación de modelos.

## Trabajos previos relacionados

El paper organiza los trabajos previos en dos grandes categorías: (1) neuronas selectivas en redes neuronales artificiales (en visión y NLP), y (2) análisis de transformers pre-entrenados mediante sondas y análisis de parámetros.

- **Bau et al. (2017) — Network Dissection: Quantifying Interpretability of Deep Visual Representations**: demuestra que las neuronas selectivas son más importantes para el comportamiento del modelo, resultado consistente con los hallazgos de este paper para neuronas de habilidad.
- **Radford et al. (2017) — Learning to Generate Reviews and Discovering Sentiment**: identifica una "neurona de sentimiento" en LSTMs no supervisados, antecedente directo de la búsqueda de neuronas especializadas en NLP.
- **Geva et al. (2021) — Transformer Feed-Forward Layers Are Key-Value Memories**: establece que las capas FFN de los transformers funcionan como memorias de clave-valor que codifican hechos y patrones lingüísticos, hipótesis que el paper extiende al concepto de habilidades.
- **Dai et al. (2021) — Knowledge Neurons in Pretrained Transformers**: identifica neuronas específicas en capas FFN que almacenan conocimiento factual y propone suprimirlas para editar conocimiento, trabajo directamente relacionado con la localización de conocimiento en neuronas específicas.
- **Suau et al. (2020) — Finding a Needle in a Haystack: Towards a Comprehensive Understanding of Linguistic Knowledge in Neural Networks**: estudia qué información lingüística codifican neuronas individuales en transformers, trabajo previo de análisis de neuronas en el mismo nivel de análisis que este paper.
- **Durrani et al. (2020) — Analyzing Individual Neurons in Pre-trained Language Models**: encuentra que neuronas individuales capturan propiedades lingüísticas como POS y NER, pero las define como dimensiones de representaciones contextualizadas en lugar de neuronas FFN.
- **Voita et al. (2019) — Analyzing Multi-Head Self-Attention: Specialized Heads Do the Heavy Lifting, the Rest Can Be Pruned**: identifica cabezas de atención especializadas que son más importantes y propone prune las demás, análogo al concepto de especialización funcional que este paper aplica a neuronas FFN.
- **Clark et al. (2019) — What Does BERT Look at? An Analysis of BERT's Attention**: analiza qué patrones lingüísticos capturan las cabezas de atención de BERT, trabajo de análisis de especializaciones funcionales complementario al de las capas FFN.
- **Mu & Andreas (2020) — Compositional Explanations of Neurons**: propone explicaciones composicionales de neuronas visuales, metodología de análisis de neuronas que este paper adapta para neuronas de habilidad lingüística.

## Tags

`interpretabilidad` `skill-neurons` `FFN-layers` `transformers` `modularidad`
