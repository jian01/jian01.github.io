---
layout: paper
title: "Towards Automated Circuit Discovery for Mechanistic Interpretability"
year: 2023
date_published: "2023-04-28"
authors: "Arthur Conmy, Adrià Garriga-Alonso, Stefan Heimersheim, Aengus Lynch, Augustine N. Mavor-Parker"
published: "NeurIPS, 2023"
tags:
  - "interpretabilidad-mecanística"
  - "circuitos"
  - "activation-patching"
  - "automatización"
  - "transformer"
pdf: "/llm_bias/pdfs/2023_conmy_automated-circuit-discovery.pdf"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2023_conmy_automated-circuit-discovery.png"
image_caption: "Visualización del circuito descubierto por ACDC en un transformer: los nodos y aristas en rojo representan los componentes causalmente relevantes identificados automáticamente, destacados sobre el grafo completo del modelo en gris."
opinion: "<WIP>"
---

## Qué hace

Propone ACDC (**A**utomatic **C**ircuit **Di**s**C**overy), un algoritmo que automatiza la identificación de circuitos en transformers: dado un comportamiento de interés definido por un dataset y una métrica, ACDC recorre iterativamente el grafo computacional del modelo desde los outputs hasta los inputs, eliminando aristas cuya ausencia no afecte significativamente la métrica, hasta obtener el subgrafo mínimo que implementa el comportamiento. El paper además sistematiza el workflow general de interpretabilidad mecanística, propone métricas cuantitativas de evaluación (curvas ROC de recuperación de circuitos), y compara ACDC contra dos baselines: Subnetwork Probing (SP) y Head Importance Score for Pruning (HISP). Se valida en seis tareas: IOI, Docstring, Greater-Than, Induction, y dos tareas de transformers compilados con tracr.

## Contexto y motivación

Para 2023, el descubrimiento de circuitos había producido resultados notables (circuito IOI de Wang et al. 2022, Greater-Than de Hanna et al. 2023, Docstring de Heimersheim & Janiak 2023), pero cada uno había requerido meses de trabajo intensivo de investigadores: diseño manual de experimentos de patching, formulación de hipótesis, análisis de patrones de atención, y validación ad hoc. Este proceso no escala.

El problema tiene dos dimensiones. Primera, los modelos modernos son mucho más grandes que GPT-2 small (117M parámetros): aplicar la metodología manual a modelos de 70B parámetros es inviable. Segunda, incluso en modelos pequeños hay decenas de miles de aristas en el grafo computacional, y la búsqueda manual es una fracción ínfima del espacio. ACDC ataca este cuello de botella identificando que el paso más tedioso y automatizable del workflow es precisamente la búsqueda de qué aristas del grafo computacional forman parte del circuito.

El paper también sistematiza el workflow de interpretabilidad mecanística en tres pasos formales, convirtiéndolo en un proceso con entradas y salidas bien definidas, lo que facilita su automatización parcial.

## Tarea estudiada

El paper no estudia una única tarea, sino que propone un framework y lo evalúa en seis comportamientos distintos:

| Tarea | Ejemplo de prompt | Output esperado | Métrica |
|---|---|---|---|
| **1. IOI** | "When John and Mary went to the store, Mary gave a bottle of milk to" | " John" | Diferencia de logits |
| **2. Docstring** | `def f(self, files, obj, state, size, shape, option):` `"""...:param size:...:param` | `" shape"` | Diferencia de logits |
| **3. Greater-Than** | "The war lasted from 1517 to 15" | "18" o "19" o ... o "99" | Diferencia de probabilidades |
| **4. tracr-xproportion** | `["a", "x", "b", "x"]` | `[0, 0.5, 0.33, 0.5]` | Error cuadrático medio |
| **5. tracr-reverse** | `[0, 3, 2, 1]` | `[1, 2, 3, 0]` | Error cuadrático medio |
| **6. Induction** | "VernonDursley and Petunia Durs" | "ley" | Log-probabilidad negativa |

Las tareas 1-3 y 6 usan GPT-2 small (Radford et al. 2019). Las tareas 4 y 5 usan transformers de juguete compilados con tracr (Lindner et al. 2023), que implementan algoritmos conocidos exactos, ofreciendo una ground truth perfecta del circuito.

Para cada tarea se define también una **distribución corrupta**: un conjunto de prompts que elicitan un comportamiento diferente (por ejemplo, para IOI el dataset ABC donde los nombres son independientes, sin estructura de objeto indirecto). Las activaciones del modelo en los prompts corruptos se usan como valor de reemplazo al parchear aristas.

## Metodología

### El workflow de interpretabilidad mecanística

El paper sistematiza el proceso en tres pasos:

1. **Selección de comportamiento, dataset y métrica**: Definir qué comportamiento estudiar, curar un dataset que lo elicite, y elegir una métrica cuantitativa.
2. **Definición del grafo computacional**: Decidir el nivel de granularidad (cabezas de atención y MLPs, neuronas individuales, posiciones de token separadas) y representar el modelo como un DAG.
3. **Patching iterativo para aislar el subgrafo**: Eliminar aristas innecesarias mediante intervenciones causales hasta obtener el circuito mínimo.

ACDC automatiza completamente el paso 3.

### El algoritmo ACDC

El transformer se modela como un grafo computacional $G$ donde los nodos son componentes del modelo (cabezas de atención, MLPs, embeddings) y las aristas representan conexiones a través del residual stream. Formalmente, sea $G$ el grafo completo con nodos topológicamente ordenados e invertidos (de output a input). Sea $H \subseteq G$ el subgrafo que se construye iterativamente, y $\tau > 0$ el umbral de sparsidad.

La evaluación de un subgrafo $H$ se define mediante la **divergencia KL**. Para el input original $x_i$ y el input corrupto $x'_i$:

$$H(x_i, x'_i) = \text{modelo}(x_i \text{ con aristas de } G \setminus H \text{ reemplazadas por activaciones de } x'_i)$$

$$D_{KL}(G \| H) = \mathbb{E}_i \left[ D_{KL}\left( G(x_i) \| H(x_i, x'_i) \right) \right]$$

Donde $G(x_i)$ es la distribución de probabilidad del modelo completo en $x_i$, y $H(x_i, x'_i)$ es la distribución del subgrafo (con aristas faltantes parcheadas con activaciones corruptas).

**Algorithm 1 — ACDC:**

```
Datos: Grafo G, dataset (xᵢ)ⁿ, datos corruptos (x'ᵢ)ⁿ, umbral τ > 0
Resultado: Subgrafo H ⊆ G

1. H ← G                           // Inicializar con el grafo completo
2. H ← topological_sort_reverse(H) // Ordenar de output a input
3. Para cada nodo v en H:
4.   Para cada padre w de v:
5.     H_new ← H \ {w → v}          // Eliminar temporalmente la arista
6.     Si D_KL(G || H_new) − D_KL(G || H) < τ:
7.       H ← H_new                  // La arista no es necesaria, eliminar
8.     Fin si
9.   Fin para
10. Fin para
11. Devolver H
```

La intuición es: si reemplazar la arista $w \to v$ con activaciones corruptas aumenta la KL divergencia en menos de $\tau$, entonces esa arista no contribuye significativamente al comportamiento, y se elimina permanentemente. El proceso trabaja de output a input para que cuando se evalúa una arista, el contexto de las aristas ya evaluadas (más cercanas al output) esté fijo.

El orden de iteración sobre los padres de cada nodo es un hiperparámetro: en los experimentos se itera lexicográficamente de capas más tardías a más tempranas, y de cabezas de índice mayor a menor.

### La KL divergencia como métrica universal

La elección de KL divergence como métrica principal (en lugar de diferencia de logits u otras métricas específicas de cada tarea) se justifica por tres razones:

1. Es aplicable a cualquier tarea de predicción del siguiente token sin necesidad de especificar etiquetas.
2. Es siempre no-negativa, lo que simplifica la condición de eliminación de aristas.
3. Empíricamente es la más robusta entre las tareas estudiadas, aunque con excepciones (en la tarea Docstring funciona mejor con la diferencia de logits específica).

La condición de eliminación de aristas es equivalente a:

$$\Delta_\tau: D_{KL}(G \| H_\text{new}) - D_{KL}(G \| H) < \tau$$

### Métodos de comparación

**Subnetwork Probing (SP)**: Aprende una máscara sobre los componentes del modelo usando gradient descent, con un objetivo que combina KL divergence (precisión) y regularización $L_0$ (sparsidad) con parámetro $\lambda$. Al final del entrenamiento, la máscara se binariza. Los autores adaptan SP para: (i) eliminar el linear probe original, (ii) usar KL divergence como objetivo, y (iii) interpolar entre activaciones corruptas y limpias en lugar de entre ceros y limpias.

**Head Importance Score for Pruning (HISP)**: Ordena las cabezas por scores de importancia (gradiente de la pérdida respecto a la activación de la cabeza) y mantiene las top-$k$. Los autores adaptan HISP para usar activaciones corruptas en lugar de ceros.

### Evaluación mediante curvas ROC

Para comparar los métodos, se formula la recuperación de circuitos como clasificación binaria: una arista es positiva si aparece en el circuito de referencia (descubierto manualmente en trabajos anteriores) y negativa en caso contrario. Se trazan curvas ROC variando los hiperparámetros ($\tau$ para ACDC, $\lambda$ para SP, $k$ para HISP). El **AUC** de estas curvas es la métrica principal de comparación.

Para la tarea de Induction (sin ground truth de trabajos anteriores), se evalúa con propiedades stand-alone: menor KL divergence con menos aristas indica un mejor circuito.

## El circuito / Los componentes

ACDC no define los componentes del circuito a priori, sino que los recupera. Para cada tarea, los resultados son:

### Tarea IOI (GPT-2 small)

Con threshold $\tau = 0.0575$, ACDC recupera un circuito con 9 cabezas de atención, todas pertenecientes al circuito manual de Wang et al. (2023). Las 9 cabezas incluyen representantes de tres de las siete clases del circuito IOI: Previous Token Heads, Name Mover Heads, y S-Inhibition Heads. Las Negative Name Mover Heads y las Backup Name Mover Heads no se recuperan, porque ACDC optimiza logit difference (o KL divergence), métricas que estas cabezas "sabotean" activamente o en las que sólo contribuyen marginalmente.

La ejecución completa de ACDC para IOI (con separación query/key/value por posición: 1041 aristas) tardó menos de 10 minutos en una GPU NVIDIA A100. Los experimentos más grandes que mantienen >10% de las aristas originales pueden tardar varias horas.

### Tarea Docstring (transformer de 4 capas)

Con threshold $\tau = 0.095$ y métrica KL divergence, ACDC recupera las cabezas 0.5, 1.4, 2.0, 3.0 y 3.6 del circuito manual de Heimersheim & Janiak (2023), produciendo un circuito de 34 aristas (KL divergence 1.2 vs. 1.1 del circuito manual de 37 aristas). Con threshold $\tau = 0.067$ y métrica diferencia de logits, recupera además la cabeza 1.2, produciendo un circuito con 93% menos aristas que el modelo completo y mejor rendimiento en todas las métricas que el circuito manual.

### Tarea Greater-Than (GPT-2 small)

ACDC redescubre las 5/5 clases de componentes del circuito manual de Hanna et al. (2023): selecciona 68 de las 32.000 aristas de GPT-2 small, todas ellas encontradas manualmente en el trabajo original. AUC = 0.853 con KL divergence y activaciones corruptas.

### Tareas tracr

Para tracr-reverse y tracr-xproportion (transformers con circuito perfecto conocido), ACDC con activaciones cero recupera perfectamente el circuito a cualquier threshold $\tau > 0$ (AUC = 1.000). Con activaciones corruptas el rendimiento es peor (AUC = 0.200 y 0.679 respectivamente), indicando que la elección de distribución corrupta es crítica para estos modelos.

### Tarea Induction

Con activaciones corruptas y más de 20 aristas en el circuito, ACDC obtiene ventaja sobre SP y HISP en el Pareto frontier de KL divergence vs. número de aristas, indicando que ACDC recupera más comportamiento por arista incluida.

## Ejemplo ilustrativo

**Aplicación de ACDC a la tarea IOI con el prompt**: "When John and Mary went to the store, Mary gave a bottle of milk to"

**Input**: Grafo completo $G$ de GPT-2 small con ~32.000 aristas; dataset de 50 ejemplos del template IOI; dataset corrupto (ABC dataset: "When Alice and Bob went to the store, Charlie gave a bottle of milk to"); threshold $\tau = 0.0575$.

**Paso 1 — Inicialización**: $H = G$ (todas las aristas incluidas). $D_{KL}(G \| H) = 0$ (el subgrafo es idéntico al modelo).

**Paso 2 — Iteración en el nodo de output (`resid_post`, la suma final del residual stream)**:
ACDC examina cada arista entrante al nodo de output. Para la arista "Head 9.9 → output": se reemplaza la contribución de 9.9 al residual stream final con la activación de 9.9 en el input corrupto. La KL divergence sube significativamente (>$\tau$), así que la arista se mantiene. Para "Head 1.3 → output": la KL divergence apenas cambia (<$\tau$), la arista se elimina permanentemente.

**Paso 3 — Iteración en nodos de capas anteriores**: Una vez procesado el nodo de output, ACDC pasa a las cabezas de la capa 11, luego 10, etc. Para cada cabeza que sigue en $H$, examina sus aristas entrantes (de cabezas y MLPs de capas anteriores) y elimina las irrelevantes.

**Resultado**: Tras 8 minutos de cómputo (NVIDIA A100), $H$ contiene 9 cabezas (9.9, 9.6, 10.0, 7.3, 8.6, 7.9, 8.10, 5.5, 2.2) y las aristas entre ellas. Todas pertenecen al circuito IOI manual. La KL divergence del circuito recuperado es significativamente inferior a la del modelo ablacionado aleatoriamente (baseline), confirmando que se ha recuperado estructura real.

**Comparación con el trabajo manual**: Wang et al. (2022) tardaron 3 meses en identificar las 26 cabezas del circuito IOI manualmente. ACDC recupera las cabezas centrales (9 de 26) en 8 minutos, todas con zero falsos positivos.

## Resultados principales

- **Greater-Than**: ACDC redescubre 5/5 tipos de componentes del circuito manual; selecciona exactamente 68 de 32.000 aristas de GPT-2 small, con cero falsos positivos. AUC(KL, corrupted) = 0.853.
- **IOI**: Las 9 cabezas recuperadas son todas del circuito manual (zero falsos positivos). AUC(KL, corrupted) = 0.869. ACDC supera a SP (0.823) y HISP (0.789).
- **Docstring**: AUC(KL, corrupted) = 0.982 con métrica KL; 0.972 con métrica de pérdida. Mejor resultado de todos los métodos en esta tarea.
- **tracr-reverse con activaciones cero**: AUC = 1.000 (circuito recuperado perfectamente).
- **tracr-xproportion con activaciones cero**: AUC = 1.000.
- **Induction**: Con >20 aristas, ACDC domina el Pareto frontier de KL vs. número de aristas sobre SP y HISP.
- **AUCs resumen (KL, corrupted, edge-level)**:
  - ACDC: IOI 0.869, Docstring 0.982, Greater-Than 0.853, tracr-reverse 0.200, tracr-xproportion 0.679
  - SP: IOI 0.823, Docstring 0.937, Greater-Than 0.806, tracr-reverse 0.193, tracr-xproportion 0.525
  - HISP: IOI 0.789, Docstring 0.805, Greater-Than 0.693, tracr-reverse 0.577, tracr-xproportion 0.679
- **Tiempo de cómputo**: Minutos a horas en GPU (A100), frente a meses de trabajo manual.
- **Limitación mayor**: ACDC tiende a no recuperar componentes "negativos" (como las Negative Name Mover Heads de IOI) que activamente perjudican la métrica optimizada. Incluso con KL divergence, se recuperan sólo con thresholds muy pequeños.
- **Sensibilidad al hiperparámetro**: El rendimiento varía significativamente con la elección de $\tau$, la distribución corrupta, y la métrica optimizada. No hay un único conjunto de hiperparámetros óptimo para todas las tareas.

## Ventajas respecto a trabajos anteriores

- **Automatización escalable**: Reduce el descubrimiento de circuitos de proyectos de meses a cómputo de horas, abriendo la posibilidad de aplicar circuit analysis a modelos más grandes y más comportamientos.
- **Basado en intervenciones causales principiadas**: A diferencia de métodos de pruning que usan gradientes como proxy de importancia, ACDC mide directamente el impacto causal de cada arista mediante intervenciones de intercambio, siendo más fiel a la metodología de interpretabilidad mecanística.
- **KL divergence como métrica universal**: La elección de KL divergence como criterio de eliminación de aristas es más robusta que métricas específicas de cada tarea y aplicable a cualquier comportamiento de predicción del siguiente token.
- **Primero en comparar métodos de recuperación de circuitos**: Propone el marco de evaluación mediante curvas ROC que permite comparar sistemáticamente diferentes enfoques de extracción de circuitos, un estándar antes inexistente.
- **Validación en circuitos conocidos**: Usar los circuitos de Wang et al., Hanna et al. y Heimersheim & Janiak como ground truth permite una evaluación objetiva que trabajos anteriores no podían hacer.
- **Código abierto**: La implementación open-source en GitHub (`ArthurConmy/Automatic-Circuit-Discovery`) se convierte en una herramienta de uso común en la comunidad.
- **Hallazgos cualitativos novedosos**: Usando ACDC para predecir pronombres generizados en GPT-2 small, el paper descubre un "summarization motif" inesperado (posiciones de token sorprendentes que ayudan al modelo), ilustrando cómo ACDC puede generar hipótesis novedosas.

## Trabajos previos relacionados

El paper organiza los trabajos previos en tres áreas: (1) interpretabilidad mecanística y circuitos, (2) poda de redes neuronales, y (3) interpretación causal de redes neuronales.

- **Wang et al. (2022) — [Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 Small](2022_wang_ioi-circuit.html)**: descubre manualmente el circuito IOI que ACDC después reproduce automáticamente, siendo el caso de referencia principal para evaluar ACDC.
- **Hanna et al. (2023) — [How does GPT-2 compute greater-than?](2023_hanna_gpt2-greater-than.html)**: identifica manualmente el circuito para la tarea Greater-Than, otro caso de referencia usado para evaluar ACDC.
- **Goldowsky-Dill et al. (2023) — [Localizing Model Behavior with Path Patching](2023_goldowskydill_path-patching.html)**: formaliza el path patching que ACDC utiliza como primitiva de intervención causal para evaluar la importancia de aristas en el grafo computacional.
- **Geiger et al. (2021) — [Causal Abstractions of Neural Networks](2021_geiger_causal-abstractions.html)**: proporciona el marco teórico de las abstracciones causales y las intervenciones de intercambio en las que se basa la metodología de patching causal de ACDC.
- **Elhage et al. (2021) — A Mathematical Framework for Transformer Circuits**: establece el marco teórico del residual stream y las composiciones entre cabezas de atención, base conceptual de la representación como grafo computacional que usa ACDC.
- **Olah et al. (2020) — Zoom In: An Introduction to Circuits**: introduce el paradigma de circuitos para redes neuronales de visión artificial, terminología y metodología que ACDC extiende y automatiza para transformers.
- **Bills et al. (2023) — Language Models Can Explain Neurons in Language Models**: único trabajo anterior de automatización de interpretabilidad, que usa LLMs para etiquetar neuronas, siendo el único antecedente en automatización que ACDC cita explícitamente.
- **Chan et al. (2022) — Causal Scrubbing: A Method for Rigorously Testing Interpretability Hypotheses**: propone el causal scrubbing como método más general que el patching individual de ACDC pero más computacionalmente costoso, trabajo con el que ACDC se compara directamente.
- **Meng et al. (2022) — Locating and Editing Factual Associations in GPT (ROME)**: localiza conocimiento factual en capas FFN mediante causal tracing, ejemplo de uso de intervenciones causales para localizar comportamientos que motiva la automatización de ACDC.

## Tags

`interpretabilidad-mecanística` `circuitos` `activation-patching` `automatización` `transformer`
