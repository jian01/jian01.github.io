---
layout: paper
title: "Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small"
year: 2022
date_published: "2022-11-01"
authors: "Kevin Wang, Alexandre Variengien, Arthur Conmy, Buck Shlegeris, Jacob Steinhardt"
published: "arXiv, 2022"
tags:
  - "interpretabilidad-mecanística"
  - "circuitos"
  - "GPT-2"
  - "attention-heads"
  - "IOI"
pdf: "/llm_bias/pdfs/2022_wang_ioi-circuit.pdf"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2022_wang_ioi-circuit.png"
image_caption: "Visualización de las activaciones del circuito en GPT-2 small para la tarea IOI, mostrando la estructura de cabezas de atención involucradas en la identificación del objeto indirecto."
opinion: "<WIP>"
---

## Qué hace

Identifica y valida manualmente el circuito completo en GPT-2 small responsable de la tarea de identificación de objeto indirecto (IOI, *Indirect Object Identification*): dado "When Mary and John went to the store, John gave a drink to", el modelo debe completar con "Mary". El circuito comprende 26 cabezas de atención agrupadas en 7 clases funcionales, descubierto mediante una combinación de activation patching y path patching. Es, a conocimiento de los autores, el intento más completo de ingeniería inversa de un comportamiento natural en un LLM.

## Contexto y motivación

Los modelos de lenguaje basados en transformers habían demostrado capacidades impresionantes, pero seguían siendo "cajas negras". La interpretabilidad mecanística aspiraba a reverse-engineerizar los algoritmos implementados por los pesos del modelo, pero hasta este trabajo los esfuerzos se habían limitado a comportamientos muy simples en modelos muy pequeños (como induction heads en modelos de 2 capas) o a descripciones de comportamientos complejos en modelos grandes "a grandes rasgos". Existía una brecha: no había análisis end-to-end completo de un comportamiento no trivial en un LLM de tamaño real. Este trabajo llena ese hueco estudiando GPT-2 small (117M parámetros, 12 capas, 12 cabezas por capa) en una tarea lingüística bien definida y algorítmicamente interpretable.

La motivación práctica es que entender los mecanismos subyacentes permite predecir el comportamiento fuera de distribución, identificar errores del modelo, y construir bases para escalar la comprensión a modelos más grandes. El paper también contribuye herramientas metodológicas (TransformerLens, path patching) que se convierten en estándares del área.

## Tarea estudiada

La tarea IOI consiste en completar oraciones de la forma:

> "When Mary and John went to the store, John gave a drink to ___"

La respuesta correcta es "Mary" (el objeto indirecto, IO). La oración tiene estructura fija: una cláusula dependiente inicial que introduce dos nombres, el objeto indirecto (IO = Mary) y el sujeto (S = John), seguida de una cláusula principal que vuelve a mencionar el sujeto (S2 = segunda aparición de John) y termina con una preposición que pide completar con el IO. El algoritmo humano-interpretable para resolver la tarea es:

1. Identificar todos los nombres previos en la oración (Mary, John, John).
2. Eliminar los nombres duplicados (John aparece dos veces).
3. Predecir el nombre restante (Mary).

La notación del paper usa S1 y S2 para la primera y segunda aparición del sujeto, IO para el objeto indirecto, y END para el token final (la preposición "to"). El dataset IOI se construye con 15 plantillas y nombres propios aleatorios de un token. Ejemplos del corpus:

- "When Mary and John went to the store, John gave a drink to" → "Mary"
- "Then, Alice and Bob had a meeting. Bob told the manager about" → "Alice"
- "After John and Sarah arrived at the party, John introduced himself to" → "Sarah"

GPT-2 small resuelve esta tarea con una diferencia de logits media de 3.56 (IO predicho sobre S el 99.3% del tiempo) y una probabilidad media del IO del 49%.

## Metodología

### Arquitectura y notación

GPT-2 small es un transformer decoder-only con 12 capas y 12 cabezas de atención por capa (144 cabezas en total). El input $x_0 \in \mathbb{R}^{N \times d}$ es la suma de embeddings posicionales y de tokens. El residual stream se actualiza en cada capa:

$$x_{i+1} = x_i + \sum_j h_{i,j}(x_i) + \text{MLP}_i(x_i)$$

Cada cabeza $h_{i,j}$ está parametrizada por matrices $W^{i,j}_Q, W^{i,j}_K, W^{i,j}_O \in \mathbb{R}^{d \times d/H}$ y $W^{i,j}_V \in \mathbb{R}^{d/H \times d}$. Se reescriben como matrices de bajo rango en $\mathbb{R}^{d \times d}$: la matriz $W^{i,j}_{OV} = W^{i,j}_O W^{i,j}_V$ determina qué se escribe al residual stream, y la matriz $W^{i,j}_{QK} = W^{i,j}_Q (W^{i,j}_K)^T$ calcula el patrón de atención $A^{i,j} \in \mathbb{R}^{N \times N}$.

### Knockouts (ablaciones)

Un knockout reemplaza la activación de un nodo (un par cabeza-posición de token) con su activación media sobre una distribución de referencia $p_{ABC}$. La distribución $p_{ABC}$ usa las mismas plantillas que $p_{IOI}$ pero con tres nombres no relacionados (A, B, C) en lugar de IO y S, de modo que no hay un único IO plausible. Esto garantiza que el knockout elimina la información específica de la tarea (qué nombre es el IO) pero preserva información gramatical irrelevante. La media se calcula por plantilla para preservar consistencia gramatical. El objetivo es que $C(x)$, el output del circuito $C$ con todos los nodos fuera de $C$ ablacionados, replique el comportamiento del modelo completo $M(x)$.

### Activation patching

El activation patching básico mide el efecto causal de una cabeza en el output. Para cada cabeza $h$ en posición token $p$:

1. Ejecutar el modelo en $x_\text{orig} \sim p_{IOI}$ (oración normal).
2. Volver a ejecutar, pero reemplazando la activación de $h$ en posición $p$ por la de $x_\text{new} \sim p_{ABC}$ (oración con nombres aleatorios).
3. Medir el cambio en la diferencia de logits $\Delta = \text{logit}(\text{IO}) - \text{logit}(\text{S})$.

Si el cambio es grande (negativo), $h$ contribuye positivamente al circuito. Si es grande y positivo, $h$ contribuye negativamente (Negative Name Mover Heads).

### Path patching

El activation patching estándar no distingue efectos directos de indirectos. El paper introduce **path patching** para aislar el efecto directo de una cabeza $h$ sobre un conjunto de componentes $R$. Formalmente, dado $x_\text{orig}$ y $x_\text{new}$:

1. Ejecutar un forward pass en $x_\text{orig}$.
2. Para los paths en $P$ (caminos directos desde $h$ hasta $R$, es decir, a través de conexiones residuales y MLPs pero no a través de otras cabezas de atención), reemplazar las activaciones de $h$ con las de $x_\text{new}$.
3. Recomputar todo lo que sigue a $R$ con un forward pass normal.
4. Medir el cambio en la diferencia de logits.

Esto mide el efecto contrafactual de $h$ sobre $R$ a través de caminos directos. El paper siempre toma $x_\text{orig} \sim p_{IOI}$ y $x_\text{new}$ la muestra correspondiente de $p_{ABC}$.

### Proceso de descubrimiento: back-tracing iterativo

El circuito se descubrió trabajando hacia atrás desde los logits, en pasos iterativos:

1. **Paso 1**: Path patching $h \to \text{Logits}$ para cada cabeza $h$ en posición END → identifica Name Mover Heads y Negative Name Mover Heads.
2. **Paso 2**: Path patching $h \to \text{queries de Name Movers}$ → identifica S-Inhibition Heads (7.3, 7.9, 8.6, 8.10).
3. **Paso 3**: Path patching $h \to \text{values de S-Inhibition Heads}$ en posición S2 → identifica Duplicate Token Heads e Induction Heads.
4. **Paso 4**: Buscar Previous Token Heads que alimentan las Induction Heads mediante key composition.
5. **Paso 5**: Knock out todas las Name Mover Heads → identifica Backup Name Mover Heads.

En cada paso, tras identificar las cabezas por path patching, se caracterizan sus funciones mediante análisis de patrones de atención y experimentos diseñados ad hoc.

### Criterios de validación

Se definen tres criterios formales para validar el circuito $C$ con métrica $F(C) = \mathbb{E}_{X \sim p_{IOI}}[f(C(X); X)]$ (diferencia de logits media):

- **Faithfulness (fidelidad)**: $|F(M) - F(C)|$ debe ser pequeño. El circuito obtenido tiene $|F(M) - F(C)| = 0.46$, o sólo el 13% de $F(M) = 3.56$ (87% de rendimiento preservado).
- **Completeness (completitud)**: Para todo subconjunto $K \subseteq C$, el incompleteness score $|F(C \setminus K) - F(M \setminus K)|$ debe ser pequeño. Verifica que $C$ y $M$ permanecen similares bajo knockouts.
- **Minimality (minimalidad)**: Para cada nodo $v \in C$ debe existir $K \subseteq C \setminus \{v\}$ tal que $|F(C \setminus (K \cup \{v\})) - F(C \setminus K)|$ sea grande, confirmando que $v$ es necesario.

## El circuito / Los componentes

El circuito de 26 cabezas implementa el algoritmo de tres pasos (identificar, eliminar duplicados, predecir) mediante 7 clases funcionales:

### Name Mover Heads (cabezas 9.9, 9.6, 10.0)
Son las cabezas más importantes. Activas en posición END, atienden con alta probabilidad al token IO (probabilidad media de atención = 0.59) y copian ese nombre al output. Su función de copia se verifica con el "copy score": la probabilidad de que el nombre al que atienden aparezca en el top-5 de logits si la cabeza atiende perfectamente ese token. Las tres Name Mover Heads tienen copy score >95%, frente a <20% para una cabeza promedio. La correlación entre probabilidad de atención al IO y proyección del output en dirección $W_U[\text{IO}]$ es $\rho > 0.81$.

Las Name Mover Heads implementan el paso 3 del algoritmo: "output the remaining name". Necesitan haber sido dirigidas por las S-Inhibition Heads para no atender al sujeto duplicado.

### Negative Name Mover Heads (cabezas 10.7, 11.10)
Comparten las propiedades de las Name Mover Heads pero escriben en dirección opuesta: tienen copy score negativo alto (98% con la OV negativa). Disminuyen la confianza del modelo en la predicción. Los autores especulan que ayudan al modelo a "suavizar" para evitar alta pérdida en cruce de entropía cuando comete errores. Su descubrimiento fue inesperado.

### S-Inhibition Heads (cabezas 7.3, 7.9, 8.6, 8.10)
Activas en posición END, atienden principalmente al token S2 (probabilidad media de atención END→S2 = 0.51 sobre las cuatro cabezas). Escriben en el vector de queries de las Name Mover Heads, inhibiendo su atención a S1 y S2. Sin estas cabezas, las Name Mover Heads copiarían el nombre equivocado (el sujeto duplicado).

El mecanismo funciona a través de dos señales:
- **Token signal**: contiene el valor del token S, haciendo que las Name Movers eviten ese token concreto.
- **Position signal**: contiene información sobre la posición del token S1, haciendo que las Name Movers eviten esa posición independientemente del valor del token.

La señal de posición tiene mayor efecto que la señal de token. Ambas señales juntas explican completamente la diferencia en atención al IO frente a S1.

### Duplicate Token Heads (cabezas 0.1, 3.0; con 0.10 como cabeza menor)
Activas en posición S2, atienden principalmente al token S1 (la aparición anterior del sujeto duplicado). Escriben información sobre la posición de S1 al residual stream en S2. Sus valores son luego leídos por las S-Inhibition Heads. Verificados en secuencias de tokens aleatorios: cuando existe una aparición previa del token actual, estas cabezas le prestan fuerte atención.

Implementan el paso 1 del algoritmo: "identificar tokens duplicados". La composición de valor entre Duplicate Token Heads y S-Inhibition Heads es el mecanismo que permite que la posición de S1 llegue a influir en la atención de las Name Movers.

### Induction Heads (cabezas 5.5, 6.9; con 5.8, 5.9 como menores)
Realizan el mismo papel que las Duplicate Token Heads pero mediante el mecanismo de inducción clásico (descrito en Olsson et al. 2022): reconocen el patrón [A][B]...[A] y contribuyen a predecir [B]. Activas en S2, atienden al token S1+1 (el token que sigue a S1) mediante composición de clave con las Previous Token Heads. Su output se usa como puntero a S1 y como señal de que S está duplicado. Cabe destacar que en este circuito las Induction Heads realizan una función diferente a su rol "canónico": aquí su output se usa como señal posicional para las S-Inhibition Heads, no directamente como predicción.

### Previous Token Heads (cabezas 2.2, 4.11)
Copian información sobre el token S al token S1+1 (el token inmediatamente siguiente a S1). Las Induction Heads hacen key composition con estas cabezas: al ver S2, buscan en S1+1 la representación de S copiada por las Previous Token Heads, confirmando que S en S2 es el mismo que S en S1.

### Backup Name Mover Heads (cabezas 9.0, 9.7, 10.1, 10.2, 10.6, 10.10, 11.2, 11.9)
Descubrimiento inesperado: cuando las Name Mover Heads principales son knockouteadas, el modelo sólo pierde un 5% en diferencia de logits. Estas 8 cabezas asumen el papel de las Name Movers en ausencia de éstas. Muestran comportamiento diverso: 4 se parecen mucho a las Name Movers, 2 atienden equitativamente a IO y S, 1 atiende más a S1 y lo copia, y 1 parece seguir el sujeto de la cláusula. Los autores hipotetizan que este fenómeno de compensación surge del uso de dropout durante el entrenamiento, que optimizó la robustez ante componentes disfuncionales.

## Ejemplo ilustrativo

Tomemos la oración: **"When Mary and John went to the store, John gave a drink to ___"**

Posiciones clave: IO = "Mary" (posición 1), S1 = "John" (posición 3), S2 = "John" (posición 9), END = "to" (posición 13).

**Paso 1 — Previous Token Heads (capas 2, 4):**
Las cabezas 2.2 y 4.11 atienden al token anterior a S1, escribiendo información sobre S1 ("John") en la posición S1+1 ("went"). Esto prepara el residual stream en "went" con una representación de "John".

**Paso 2 — Duplicate Token Heads (capas 0, 3):**
Las cabezas 0.1 y 3.0, activas en posición S2 (segundo "John"), atienden fuertemente al primer "John" (S1). Escriben información sobre la posición de S1 en el residual stream de S2, señalando "este token ya ha aparecido antes, en la posición 3".

**Paso 3 — Induction Heads (capas 5, 6):**
Las cabezas 5.5 y 6.9, también activas en S2, detectan el patrón [Mary][and][John]...[John] y vía key composition con las Previous Token Heads confirman que el segundo "John" es un duplicado del primero. Contribuyen señal posicional adicional sobre S1.

**Paso 4 — S-Inhibition Heads (capas 7-8):**
Las cabezas 7.3, 7.9, 8.6, 8.10, activas en posición END ("to"), atienden al token S2 y leen los valores escritos por Duplicate Token Heads e Induction Heads. Escriben en los vectores de query de las Name Mover Heads señales que inhiben la atención a S1 y S2: "no atiendas a las posiciones 3 y 9, donde está John".

**Paso 5 — Name Mover Heads (capas 9-10):**
Las cabezas 9.9, 9.6 y 10.0, activas en END, escanean todos los tokens anteriores buscando nombres. Sin inhibición, atenderían a Mary, John y John por igual. Con las señales de inhibición de las S-Inhibition Heads, la atención a S1 y S2 (John) se suprime drásticamente, y la atención se concentra en IO (Mary). Las cabezas copian "Mary" al output mediante su matriz OV: proyectan el residual stream de la posición de Mary y lo añaden al residual stream de END en la dirección del embedding de "Mary" en el espacio de logits.

**Resultado:** GPT-2 small predice "Mary" con probabilidad ~68% (frente a ~2% para "John").

**Experimento de ablación:** Si se knockoutean las S-Inhibition Heads (sustituyendo por activaciones medias), las Name Mover Heads ya no tienen señal de inhibición y comienzan a atender tanto a "John" como a "Mary". La probabilidad de atención al IO cae de ~0.65 a ~0.35, y la probabilidad de atención a S1 sube de ~0.05 a ~0.35. El modelo ya no puede resolver la tarea de forma fiable.

## Resultados principales

- **Fidelidad (faithfulness)**: El circuito de 26 cabezas (1.1% de todos los pares cabeza-posición) preserva el 87% del rendimiento del modelo completo en IOI ($|F(M) - F(C)| = 0.46$ sobre $F(M) = 3.56$).
- **Predicción correcta**: El circuito predice el IO sobre el S el 99.3% del tiempo en el dataset original.
- **Redundancia confirmada**: Sin las Name Mover Heads, el circuito sólo pierde un 5% de diferencia de logits (las Backup Name Movers compensan).
- **Copy score**: Las tres Name Mover Heads tienen copy score >95% (vs. <20% para cabezas promedio).
- **Completitud parcial**: El criterio de completitud con búsqueda greedy revela incompleteness scores de hasta 3.09 (87% de la diferencia de logits original), indicando que el circuito no captura todos los mecanismos usados por el modelo.
- **Experimento adversarial**: Cuando tanto IO como S aparecen duplicados ("John and Mary went to the store. Mary had a good day. John gave a bottle of milk to"), el modelo predice S sobre IO el 23.4% del tiempo (vs. 0.7% en distribución normal), confirmando que el circuito detecta duplicación como mecanismo central.
- **GPT-2 medium**: Análisis preliminar muestra que también tiene un conjunto disperso de cabezas que influyen directamente en los logits, pero el comportamiento es más complejo que en small.

## Ventajas respecto a trabajos anteriores

- **Primer análisis end-to-end completo** de un circuito no trivial en un LLM de tamaño real. Todos los trabajos anteriores se limitaban a comportamientos muy simples (induction heads, copy suppression) o a descripciones de alto nivel.
- **Path patching como metodología**: Formaliza una técnica para distinguir efectos directos e indirectos entre componentes, superando el activation patching estándar que mezcla ambos. Esta técnica se convierte en herramienta estándar del área.
- **Vocabulario de grupos funcionales**: Introduce la noción de clases de cabezas (Name Mover, S-Inhibition, Duplicate Token, etc.) como unidades de análisis interpretables, metodología que todos los trabajos posteriores adoptan.
- **Criterios de validación formales**: Propone faithfulness, completeness y minimality como métricas cuantitativas para evaluar explicaciones de circuitos, estableciendo estándares de rigor.
- **Descubrimientos inesperados**: La existencia de Backup Name Mover Heads (redundancia incorporada) y Negative Name Mover Heads revela fenómenos de organización del modelo no anticipados por trabajos teóricos anteriores.
- **TransformerLens**: El código desarrollado se convierte en la librería de referencia para interpretabilidad mecanística en transformers.

## Trabajos previos relacionados

- **Elhage et al. (2021) — A Mathematical Framework for Transformer Circuits**: establece el marco teórico del residual stream y las composiciones de cabezas de atención en transformers, base conceptual sobre la que se construye el análisis del circuito IOI.
- **Olah et al. (2020) — Zoom In: An Introduction to Circuits**: introduce el paradigma de "circuitos" en redes neuronales convolucionales, terminología y metodología que este paper traslada por primera vez a un LLM de tamaño real.
- **Meng et al. (2022) — Locating and Editing Factual Associations in GPT (ROME)**: localiza dónde se almacena conocimiento factual en GPT-J mediante causal tracing, técnica de localización causal que inspira el uso de activation patching para descubrir el circuito IOI.
- **Olsson et al. (2022) — In-context Learning and Induction Heads**: descubre y caracteriza las induction heads en transformers, trabajo que define el rol de las induction heads que el paper IOI integra en el circuito más complejo.
- **Geiger et al. (2021) — [Causal Abstractions of Neural Networks](2021_geiger_causal-abstractions.html)**: formaliza las intervenciones de intercambio como herramienta para verificar abstracciones causales, marco teórico causal en el que se inscribe el método de activation patching del paper IOI.
- **Nanda & Lieberum (2022) — A Mechanistic Interpretability Analysis of Grokking**: aplica análisis mecanístico a un fenómeno de generalización repentina usando metodología similar, y motiva las ablaciones por media que el paper IOI adopta.
- **Vig et al. (2020) — Investigating Gender Bias in Language Models Using Causal Mediation Analysis**: uno de los primeros trabajos en usar intervenciones causales sobre cabezas de atención en LLMs para estudiar efectos directos e indirectos.
- **Goldowsky-Dill et al. (2023) — [Localizing Model Behavior with Path Patching](2023_goldowskydill_path-patching.html)**: formaliza el path patching como extensión del activation patching para analizar caminos de información entre componentes, metodología desarrollada en paralelo e integrada en los experimentos del paper.
- **Conmy et al. (2023) — [Towards Automated Circuit Discovery for Mechanistic Interpretability](2023_conmy_automated-circuit-discovery.html)**: automatiza el proceso de descubrimiento de circuitos que el paper IOI realiza manualmente, tomando el circuito IOI como caso de referencia.

## Tags

`interpretabilidad-mecanística` `circuitos` `GPT-2` `attention-heads` `IOI`
