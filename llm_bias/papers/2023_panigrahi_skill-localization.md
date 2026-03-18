---
layout: paper
title: "Task-Specific Skill Localization in Fine-tuned Language Models"
year: 2023
date_published: "2023-02-13"
authors: "Abhishek Panigrahi, Nikunj Saunshi, Haoyu Zhao, Sanjeev Arora"
published: "arXiv, 2023"
tags:
  - "interpretabilidad"
  - "localización-habilidades"
  - "fine-tuning"
  - "sparse-masks"
  - "BERT"
pdf: "/llm_bias/pdfs/2023_panigrahi_skill-localization.pdf"
status:
  - "Leido"
image: "imgs/2023_panigrahi_skill-localization.png"
image_caption: "Imagen asociada al paper sobre localización de habilidades específicas en modelos de lenguaje fine-tuneados."
opinion: "<WIP>"
---

## Qué hace

Propone un método llamado **grafting** (injerto) para identificar el subconjunto mínimo de parámetros de un LLM fine-tuneado que son responsables de más del 95% del rendimiento en la tarea objetivo. Demuestra que ese subconjunto puede representar apenas el 0.01% del total de parámetros del modelo y que, al injertarlo sobre el modelo pre-entrenado (sin reentrenamiento adicional), se obtiene rendimiento comparable al fine-tuning completo con calibración mejorada en un 40–90%.

## Contexto y motivación

Cuando se hace fine-tuning de un LLM sobre una tarea específica (p. ej., análisis de sentimiento), no está claro si todos los parámetros del modelo se ven modificados de manera significativa o si sólo un subconjunto pequeño acumula la habilidad nueva. Esta pregunta tiene implicaciones directas para la interpretabilidad (¿dónde "vive" el conocimiento específico de la tarea?), el aprendizaje eficiente en parámetros (PEFT), la edición de modelos y el aprendizaje continuo sin olvido catastrófico.

Los trabajos previos, como la Hipótesis de la Billete de Lotería (*Lottery Ticket Hypothesis*, Frankle & Carbin 2018), también buscaban sub-redes importantes dentro de redes neuronales, pero requerían reentrenamiento desde cero para que esas sub-redes funcionasen. El enfoque de BitFit o los adaptadores (Houlsby 2019) reducen los parámetros actualizados durante el fine-tuning, pero no exploran qué partes del modelo fine-tuneado son *post-hoc* suficientes para la tarea. El paper llena ese hueco: no propone un método de fine-tuning más eficiente, sino una técnica de análisis que revela la estructura modular de las habilidades adquiridas.

## Tarea estudiada

El paper estudia el fine-tuning supervisado de modelos transformer (RoBERTa-base y GPT-2) en tareas GLUE de clasificación de texto, incluyendo:

- **Tareas de una oración:** SST-2 (sentimiento), CR (reseñas de clientes), MR (reseñas de películas), MPQA (opiniones), TREC (clasificación de preguntas), AGNews (categorías de noticias), Subj (subjetividad).
- **Tareas de dos oraciones:** QNLI, SNLI, MNLI (inferencia textual), RTE (reconocimiento de implicatura), MRPC y QQP (detección de paráfrasis).

El fenómeno central es: dado un modelo pre-entrenado $\theta_{\text{pre}}$ y su versión fine-tuneada $\theta_{\text{ft}}$, ¿puede encontrarse una máscara binaria muy esparsa $\gamma$ tal que el modelo mezclado $\bar{\theta}_{\text{ft}}(\gamma)$ mantenga el rendimiento en la tarea?

Los experimentos se realizan principalmente en el régimen de pocos ejemplos (*few-shot*): 64 y 4096 ejemplos de entrenamiento, lo que hace que los hallazgos sobre esparsidad sean especialmente relevantes para aplicaciones prácticas.

## Metodología

### Definición formal de grafting

El método central es el **grafting**: dado un modelo pre-entrenado $\theta_{\text{pre}}$ y su versión fine-tuneada $\theta_{\text{ft}}$, se construye un modelo mezclado usando una máscara binaria $\gamma \in \{0,1\}^{|\theta|}$:

$$\bar{\theta}_{\text{ft}}(\gamma) = \gamma \odot \theta_{\text{ft}} + (1 - \gamma) \odot \theta_{\text{pre}}$$

Aquí $\odot$ es el producto elemento a elemento (Hadamard). **Interpretación intuitiva:** cada parámetro $i$ del modelo resultante toma su valor del modelo fine-tuneado si $\gamma_i = 1$ (ese parámetro "es importante para la tarea"), y del modelo pre-entrenado si $\gamma_i = 0$ (ese parámetro no aportó habilidad nueva). La diferencia $\theta_{\text{ft}} - \theta_{\text{pre}}$ es el **task vector**: el conjunto de cambios que el fine-tuning introdujo en el modelo. El grafting selecciona cuáles de esos cambios son esenciales.

### Optimización para encontrar la máscara esparsa

El objetivo es encontrar la máscara $\gamma$ más esparsa posible que mantenga el rendimiento en la tarea $T$:

$$\underset{\gamma \in \{0,1\}^{|\theta|}}{\arg\min} \; \|\gamma\|_0 \quad \text{s.t.} \quad \mathcal{L}_T(\bar{\theta}_{\text{ft}}(\gamma)) \leq \epsilon$$

Equivalentemente, en la formulación relajada que el paper usa en práctica:

$$\underset{\gamma}{\arg\min} \; \mathcal{L}_T(\gamma \odot \theta_{\text{ft}} + (1-\gamma) \odot \theta_{\text{pre}})$$

donde $\gamma := \gamma_{\text{base}} \odot (1 - \sigma(S)) + (1 - \gamma_{\text{base}}) \odot \sigma(S)$, con $\sigma$ la función sigmoide y $S \in \mathbb{R}^{|\theta|}$ los parámetros optimizables.

**Interpretación intuitiva de los términos:**
- $\mathcal{L}_T$: la pérdida en la tarea específica (cross-entropy de clasificación). Se quiere que el modelo grafted rinda bien.
- $\|\gamma\|_0$: la norma L0 cuenta cuántos parámetros están "activados". Se quiere minimizarla para obtener la máscara más esparsa posible.
- $\gamma_{\text{base}}$: una máscara inicial construida a partir del top-k de $|\theta_{\text{ft}} - \theta_{\text{pre}}|$ — los parámetros que más cambiaron durante el fine-tuning son candidatos naturales para la máscara.
- $S$: parámetros de puntuación aprendibles que ajustan la máscara base. La reparametrización con sigmoide hace que el problema sea diferenciable.

El procedimiento usa pocos pasos de gradiente (no un entrenamiento completo), lo que hace que la búsqueda de la máscara sea eficiente.

### Métricas de evaluación

Además del accuracy estándar, el paper usa el **Expected Calibration Error (ECE)**: la diferencia entre la confianza del modelo y su accuracy real. Un modelo bien calibrado tiene ECE bajo — sus predicciones del 80% de confianza son correctas el 80% de las veces. El paper muestra que los modelos grafted tienen mejor calibración que los fine-tuneados completos.

Para el análisis multi-tarea, se define la ganancia relativa de la máscara $\gamma$ en la tarea $t$:

$$\text{Rel}_{\gamma, t} = \frac{P_{\gamma, t} - P_{0, t}}{P_{1, t} - P_{0, t}}$$

donde $P_{0,t}$ es el rendimiento del modelo pre-entrenado en la tarea $t$ y $P_{1,t}$ el del modelo fine-tuneado completo. **Interpretación intuitiva:** $\text{Rel}_{\gamma,t} = 1$ significa que la máscara $\gamma$ captura toda la habilidad de la tarea $t$; $\text{Rel}_{\gamma,t} = 0$ significa que la máscara no aporta nada para esa tarea.

### Unión de subnetworks

Para el aprendizaje multi-tarea y continuo, el paper propone construir la **unión de máscaras de múltiples tareas**:

$$\gamma_G = \bigcup_{i \in G} \gamma_i$$

donde $G$ es un subconjunto de tareas. **Interpretación intuitiva:** si tenemos las habilidades localizadas para SST-2 (sentimiento) y QNLI (inferencia), podemos combinar sus máscaras y obtener un modelo que domina ambas habilidades. Dado que las regiones son casi disjuntas, la unión agrega muy pocos parámetros y no "contamina" otras habilidades.

Tras la unión, se pueden aplicar unos pocos pasos de gradiente ("purificación") para limpiar la máscara combinada, mejorando el rendimiento del 70% al 80% de ganancia relativa.

## Hallazgos principales

- **Esparsidad extrema:** Sólo el 0.01% de los parámetros de RoBERTa (≈ 8.500 de 125M parámetros) son suficientes para mantener >95% del rendimiento en tareas de una oración. Para GPT-2, la cifra es algo mayor: 0.05%.

- **Localización anatómica:** La mayoría de los parámetros importantes se concentran en: (1) parámetros de valor de las cabezas de atención, (2) la primera capa feed-forward, y (3) parámetros de LayerNorm distribuidos a lo largo de todas las capas. Las capas medias del transformer predominan para la mayoría de las tareas, con la notable excepción de AGNews (clasificación de noticias), donde las capas finales son más importantes.

- **Mejor calibración:** Los modelos grafted tienen ECE 40–90% más bajo que los modelos fine-tuneados completos. Por ejemplo, en QNLI: ECE = 10.2 (fine-tuning completo) vs. 1.0 (grafting). Esto se explica porque el modelo grafted hereda las distribuciones de confianza del pre-entrenamiento para los parámetros no grafted.

- **Mejor generalización out-of-distribution:** Los modelos grafted superan en ~5% a los fine-tuneados en evaluación OOD (ej. modelo entrenado en MPQA evaluado en SST-2, o QNLI evaluado en MNLI/SNLI).

- **Regiones disjuntas entre tareas:** El solapamiento entre máscaras de tareas distintas es <5% para tareas disimilares. Tareas similares (SST-2/CR, SNLI/MNLI) muestran solapamiento ligeramente mayor, y este solapamiento es un proxy de similitud de tareas.

- **Diferencia fundamental con Lottery Tickets:** Las sub-redes de billetes de lotería sin reentrenamiento no funcionan; ni siquiera una sub-red del 90% de los parámetros recupera el 10% de la habilidad sin reentrenar. El grafting funciona sin reentrenamiento porque mantiene los *valores* del modelo pre-entrenado en los parámetros no seleccionados (en lugar de ceros o valores aleatorios).

## Ejemplo ilustrativo

Considérese el fine-tuning de RoBERTa-base en **SST-2** (análisis de sentimiento de reseñas de películas) con 4096 ejemplos. RoBERTa-base tiene ~125 millones de parámetros.

El procedimiento de grafting encuentra una máscara $\gamma$ con solo **~8.500 parámetros activados** (0.007% del total). El modelo resultante $\bar{\theta}_{\text{ft}}(\gamma) = \gamma \odot \theta_{\text{ft,SST-2}} + (1-\gamma) \odot \theta_{\text{pre}}$ obtiene:

- Accuracy en SST-2: **92.4%** vs. 92.3% del fine-tuning completo — diferencia prácticamente nula.
- ECE: **3.1** vs. 7.4 del fine-tuning completo — la calibración mejoró un 58%.
- OOD (evaluado en Yelp e IMDb sin reentrenar): el modelo grafted supera al fine-tuneado completo en ~5%.

Ahora bien, esos 8.500 parámetros son específicos de SST-2. Si se hace lo mismo para QNLI (inferencia textual), se obtiene otra máscara de ~8.500 parámetros con <5% de solapamiento con la máscara de SST-2. Esto significa que las habilidades de "entender sentimiento" y "razonar sobre implicatura textual" residen en regiones casi no solapadas del transformer.

Si en un escenario de aprendizaje continuo se fine-tunea primero en QNLI y luego en SST-2 usando fine-tuning estándar, el modelo olvida QNLI (caída del 20% en accuracy). Con grafting, se construye $\gamma_{\text{QNLI}} \cup \gamma_{\text{SST-2}}$ y se obtiene un modelo que mantiene **86.5% en QNLI** y **92.5% en SST-2** simultáneamente, sin ningún olvido catastrófico.

## Resultados principales

**Single-task localization (RoBERTa-base, 4096-shot):**

| Tarea | Accuracy FT completo | Accuracy Grafting | ECE FT | ECE Grafting | % parámetros |
|---|---|---|---|---|---|
| SST-2 | 92.3% | 92.4% | 7.4 | 3.1 | 0.007% |
| QNLI | 88.0% | 84.7% | 10.2 | 1.0 | 0.010% |
| QQP | 79.6% | 76.3% | — | — | 0.012% |

- Caída media de accuracy en tareas de una oración: **0.7%**; mejora de ECE: **5%** absoluto.
- Caída media de accuracy en tareas de dos oraciones: **3.4%**; mejora de ECE: **9.6%** absoluto.
- Acuerdo de predicción entre modelo grafted y fine-tuneado completo: **93%** en tareas de una oración, **86%** en tareas de dos oraciones.

**Out-of-distribution:** Ventaja de ~5% sobre el fine-tuning completo en evaluaciones OOD (MPQA→SST-2, QNLI→MNLI/SNLI).

**Continual learning (Tabla 4):** Fine-tuning naïf causa 20% de olvido catastrófico en QNLI; grafting retiene 86.5% en QNLI mientras logra 92.5% en SST-2.

**Comparación con PEFT (a misma esparsidad 0.05–1%):** Grafting mejora el ECE en **4.6%** y la accuracy OOD en **7.9%** sobre LoRA y adaptadores a esparsidad equivalente.

**Solapamiento con FISH Mask:** Menos del 10% de solapamiento entre los parámetros seleccionados por información de Fisher y los seleccionados por grafting, indicando que los mecanismos son fundamentalmente distintos.

## Ventajas respecto a trabajos anteriores

- **Sin reentrenamiento:** A diferencia de la Hipótesis de la Billete de Lotería, el grafting no requiere reentrenar la sub-red encontrada — las habilidades están directamente accesibles en los valores del modelo fine-tuneado.
- **Mejor calibración:** Los modelos grafted son sistemáticamente mejor calibrados que los fine-tuneados completos, lo que los hace más fiables en aplicaciones que requieren confianza calibrada.
- **Mejor OOD:** La localización de habilidades en un subconjunto esparso reduce el overfitting al distribuir menos parámetros de "libre energía" lejos de sus valores pre-entrenados.
- **Modularidad demostrada empíricamente:** Es el primer trabajo que demuestra cuantitativamente que las habilidades de fine-tuning son módulos casi disjuntos en el espacio de parámetros.
- **Proxy de similitud de tareas:** El solapamiento de máscaras es una medida de similitud de tareas interpretable y no supervisada.
- **Aprendizaje continuo sin olvido:** La composición de máscaras ofrece una solución natural al olvido catastrófico con overhead de memoria de $T \times s$ (tareas × tamaño de máscara) vs. $T \times d$ (tamaño completo del modelo).

## Trabajos previos relacionados

El paper organiza los trabajos relacionados en tres categorías: conocimiento/habilidades en LLMs, fine-tuning eficiente en parámetros (PEFT), y la hipótesis de billetes de lotería. Esta estructura refleja las tres líneas de investigación que convergen en la localización de habilidades.

- **Wang et al. (2022) — [Skill Neurons in Language Models](2022_wang_skill-neurons.html)**: descubren neuronas "skill" altamente predictivas de tareas downstream en soft prompt-tuning, trabajo directamente relacionado con la localización de habilidades que este paper extiende al contexto del fine-tuning supervisado.
- **Meng et al. (2022) — Locating and Editing Factual Associations in GPT (ROME)**: demuestra que el conocimiento factual se localiza en las capas FFN de los modelos, motivando la hipótesis de que las habilidades de fine-tuning también están localizadas.
- **Dai et al. (2022) — Knowledge Neurons in Pretrained Transformers**: identifica neuronas cuya activación correlaciona con hechos específicos en BERT, antecedente directo de la idea de localización de conocimiento/habilidades.
- **Frankle & Carlin (2018) — The Lottery Ticket Hypothesis**: el paper contrasta explícitamente su método con LTH, argumentando que las sparse masks de grafting son más interpretables que los "billetes de lotería" clásicos.
- **Ben-Zaken et al. (2022) — BitFit: Simple Parameter-efficient Fine-tuning**: actualiza solo los sesgos durante el fine-tuning con rendimiento comparable; representa el estado del arte en PEFT contra el que se compara el método de grafting.
- **Houlsby et al. (2019) — Parameter-Efficient Transfer Learning (Adapters)**: método PEFT fundacional que entrena pequeños módulos adicionales entre capas, contexto para entender la localización de habilidades como guía para PEFT.
- **Yang et al. (2022) — [Task-Specific Compression via Pruning](2022_yang_task-specific-compression.html)**: trabajo relacionado sobre identificación de subnetworks específicos por tarea, que aborda el problema de localización desde la perspectiva de la compresión.
- **Li et al. (2022) — The Lazy Neuron Phenomenon**: muestra que las activaciones feed-forward son esparsas en modelos grandes, evidencia que apoya la hipótesis de localización de habilidades del paper.

## Tags

`interpretabilidad` `localización-habilidades` `fine-tuning` `sparse-masks` `BERT`
