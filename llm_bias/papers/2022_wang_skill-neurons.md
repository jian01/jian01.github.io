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
---## Qué hace

Identifica **neuronas de habilidad** — neuronas individuales en las capas FFN de transformers pre-entrenados que son específicamente responsables de habilidades lingüísticas concretas (ej. análisis sintáctico, NER, clasificación de sentimientos). Muestra que estas neuronas son estables, específicas y localizadas.


---

## Metodología

**¿Qué son las neuronas de habilidad?**
En las capas FFN de un transformer, cada neurona es un vector de pesos que puede estar más o menos activo. La hipótesis es que algunas neuronas se especializan en capacidades lingüísticas específicas durante el preentrenamiento.

**Identificación:**
Para cada neurona de la FFN (en todas las capas), se computa un "skill score" para cada tarea:
1. Se toma un dataset de la tarea (ej. NER, análisis sintáctico).
2. Se analizan las activaciones de cada neurona al procesar este dataset.
3. Las neuronas con alta activación promedio para la tarea Y pero baja para otras tareas reciben un alto skill score para Y.
4. Las neuronas con los skill scores más altos son las "skill neurons" para esa habilidad.

**Validación:**
Para confirmar que estas neuronas son causalmente importantes (no sólo correlacionadas), se prueban dos intervenciones:
1. **Knockout**: se ponen en cero los pesos de las skill neurons y se mide la degradación de rendimiento en la tarea correspondiente.
2. **Transferencia**: se copian las skill neurons de un modelo fine-tuneado en una tarea hacia el modelo pre-entrenado, y se mide si el rendimiento mejora sin entrenamiento adicional.

---

## Datasets utilizados

- **GLUE**: 8 tareas de NLP (SST-2, QQP, MNLI, QNLI, RTE, etc.) para identificar skill neurons de distintas habilidades.
- **SuperGLUE**: tareas más difíciles.
- **Probing tasks**: tareas de probing de propiedades lingüísticas (POS tagging, parsing, etc.).
- Evaluado en BERT-base y RoBERTa-base.

---

## Ejemplo ilustrativo

Para la tarea de análisis de sentimiento (SST-2), se identifican las 50 neuronas con mayor skill score. Al knockout de estas 50 neuronas específicas (de las ~3M totales de BERT), el rendimiento en SST-2 cae del 93% al 72%, mientras que el rendimiento en otras tareas (MNLI, QQP) apenas cambia. Esto confirma que estas neuronas son altamente específicas para el análisis de sentimiento.

Aún más interesante: si se copian las 50 skill neurons de un modelo fine-tuneado en SST-2 hacia un modelo pre-entrenado sin fine-tuning en SST-2, el rendimiento del modelo receptor mejora del 70% al 85% sin ningún entrenamiento adicional.

---

## Resultados principales

- Las skill neurons son un subconjunto pequeño pero crucial: las top-50 neuronas (de ~3M) explican el 20-30% de la degradación en la tarea correspondiente.
- Las neuronas son específicas por habilidad: poca superposición entre skill neurons de distintas tareas.
- La transferencia de skill neurons funciona: permite "instalar" nuevas habilidades sin entrenamiento.
- Las skill neurons tienden a concentrarse en capas FFN medias-altas del transformer.

---

## Ventajas respecto a trabajos anteriores

- Primer estudio sistemático que identifica y valida neuronas de habilidad en transformers pre-entrenados.
- La transferencia de skill neurons es un mecanismo práctico para eficiencia en few-shot adaptation.
- Contribuye a la narratía de que las capas FFN son "memorias de conocimiento" (consistent con Geva et al. 2021).

---

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
