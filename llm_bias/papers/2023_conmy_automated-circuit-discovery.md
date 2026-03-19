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

Para cada tarea se define también una **distribución corrupta**: un conjunto de prompts que elicitan un comportamiento diferente. Las activaciones del modelo en los prompts corruptos se usan como valor de reemplazo al parchear las aristas eliminadas de $$H$$:

| Tarea | Dataset corrupto | Descripción |
|---|---|---|
| IOI | ABC dataset | Mismas plantillas, tres nombres independientes A/B/C sin estructura IO/S |
| Docstring | `random_random` | Nombres de variables y docstring completamente aleatorios |
| Greater-Than | Dataset '01' | Oraciones sin sesgo hacia ningún año en particular |
| tracr-xproportion | Permutación sin puntos fijos de $$x_i$$ | Lista aleatoria de tokens |
| tracr-reverse | Permutación sin puntos fijos de $$x_i$$ | Lista aleatoria de tokens |
| Induction | — (KL divergence stand-alone) | No se usa distribución corrupta para la evaluación |

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

La elección de KL divergence como métrica principal se justifica por:

1. **Universalidad**: aplicable a cualquier tarea de predicción del siguiente token sin especificar etiquetas (a diferencia de la logit difference que requiere saber qué tokens comparar).
2. **No-negatividad**: $$D_{KL}(G \| H) \geq 0$$ siempre, lo que simplifica la condición de eliminación — incrementos son siempre positivos, la condición $$<\tau$$ es estable.
3. **Robustez empírica**: la logit difference puede producir subgrafos con logit difference mayor o menor que el modelo completo (valores entre 1.5 y 5.0 se observaron en experimentos), haciendo la condición de parada inestable. La KL divergence no tiene este problema.
4. **Coincidencia con la "faithfulness"**: optimizar para baja KL divergence equivale directamente a que el subgrafo replique la distribución de output del modelo completo, que es el objetivo de faithfulness.

**Excepción**: en la tarea Docstring, usar la logit difference específica de la tarea como métrica da mejores resultados que KL divergence (AUC 0.972 vs. 0.982 a nivel de aristas, pero mejor en logit difference de output). Esto sugiere que cuando la métrica de la tarea está bien definida y es estable, puede ser más informativa.

La condición de eliminación de aristas es:

$$\Delta_\tau: D_{KL}(G \| H_\text{new}) - D_{KL}(G \| H) < \tau$$

### Métodos de comparación

#### Subnetwork Probing (SP) — Cao et al. (2021), adaptado

SP aprende una máscara diferenciable sobre los componentes del modelo mediante gradient descent. El objetivo combina precisión (KL divergence respecto al modelo completo) y sparsidad (regularización $$L_0$$) con parámetro $$\lambda$$:

$$\mathcal{L}_\text{SP} = D_{KL}(G \| H_\lambda) + \lambda \cdot \|\text{máscara}\|_0$$

Al final del entrenamiento, la máscara se binariza (umbral 0/1), produciendo una subred exacta. SP explora diferentes sparsidades variando $$\lambda \in \{0.01, 0.0158, \ldots, 250\}$$ (32 valores).

Los autores aplican **tres modificaciones** para adaptar SP al descubrimiento de circuitos:

1. **Eliminar el linear probe**: el SP original entrena un probe lineal adicional tras la máscara; se elimina porque el objetivo ya es la KL divergence directamente.
2. **Cambiar la métrica**: el SP original usa negative log-probability; se sustituye por KL divergence (o la métrica específica de la tarea).
3. **Interpolar con activaciones corruptas**: en lugar de multiplicar pesos por la máscara ($$\phi \cdot Z$$), se interpola entre activaciones limpias (máscara=1) y activaciones corruptas $$x'$$ (máscara=0), editando activaciones en lugar de pesos.

El número de aristas del circuito SP se cuenta como el número de aristas entre pares de nodos no enmascarados.

#### HISP — Michel et al. (2019), adaptado

HISP ordena los componentes por un score de importancia basado en gradientes y mantiene los top-$$k$$. El score de importancia original es:

$$I_h = \frac{1}{n}\sum_{i=1}^n \left|\frac{\partial \mathcal{L}(x_i)}{\partial \xi_h}\right| = \frac{1}{n}\sum_{i=1}^n \left|\text{Att}_h(x_i)^\top \frac{\partial \mathcal{L}(x_i)}{\partial \text{Att}_h(x_i)}\right|$$

donde $$\xi_h$$ es un parámetro de escala de la salida de la cabeza $$h$$. Los autores lo generalizan a cualquier componente interno diferenciable $$C$$ (incluyendo queries, keys, values y salidas de MLPs) e incorporan activaciones corruptas:

$$I_C = \frac{1}{n}\sum_{i=1}^n \left|(C(x_i) - C(x_i'))^\top \frac{\partial F(x_i)}{\partial C(x_i)}\right|$$

donde $$C(x_i')$$ es la activación del componente $$C$$ en el input corrupto. Esta fórmula es equivalente al **attribution patching** salvo por el valor absoluto. Se exploran diferentes valores de $$k$$ para trazar la curva ROC.

### Evaluación mediante curvas ROC

Para comparar los métodos, se formula la recuperación de circuitos como **clasificación binaria de aristas**: una arista es positiva si aparece en el circuito de referencia (descubierto manualmente) y negativa si no. Se trazan curvas ROC variando los hiperparámetros ($$\tau$$ para ACDC, $$\lambda$$ para SP, $$k$$ para HISP):

- **TPR (true positive rate)**: ¿qué fracción de las aristas del circuito manual recupera el método?
- **FPR (false positive rate)**: ¿qué fracción de aristas irrelevantes incluye el método?

El **AUC** de la curva ROC es la métrica principal. Se trazan segmentos pesimistas entre puntos del Pareto frontier. Se evalúa en dos configuraciones: activaciones corruptas (la configuración principal de ACDC) y activaciones cero.

Para la tarea Induction (sin ground truth manual), se usa evaluación stand-alone en el **Pareto frontier de KL divergence vs. número de aristas** en un conjunto de test separado.

## El circuito / Los componentes

ACDC no define los componentes del circuito a priori, sino que los recupera iterativamente. Para cada tarea:

### Tarea 1: IOI (GPT-2 small)

- **Dataset**: $$N=50$$ ejemplos del template '*When John and Mary went to the store, Mary gave a bottle of milk to*'.
- **Dataset corrupto (ABC)**: '*When Alice and Bob went to the store, Charlie gave a bottle of milk to*'.
- **Threshold**: $$\tau = 0.0575$$. **Métrica**: KL divergence.
- **Grafo IOI** (nivel Q/K/V, por posición): **1.041 aristas**. Grafo completo de GPT-2 small: **~32.000 aristas**.
- **Circuito manual de referencia** (Wang et al. 2022): 26 cabezas (logit difference = **3.24**, vs. **4.11** del modelo completo; KL divergence = **0.44**).

**Resultado**: ACDC recupera **9 cabezas**, todas pertenecientes al circuito manual, de tres clases: Previous Token Heads, S-Inhibition Heads y Name Mover Heads. **Cero falsos positivos**. Las Negative Name Mover Heads y Backup Name Mover Heads **no** se recuperan con este threshold porque la KL divergence no las penaliza suficientemente (contribuyen negativamente a la logit difference). Al bajar el threshold a $$\tau = 0.00398$$, ACDC recupera 443 aristas del total de 32.923, incluyendo las Negative Name Mover Heads pero también muchas aristas extraneous.

**Tiempo de ejecución**: **8 minutos** en NVIDIA A100, frente a los **3 meses** que tardó el proceso manual. AUC(KL, corrupted, edge-level) = **0.869**.

### Tarea 2: Docstring (transformer de 4 capas, attention-only)

- **Tarea**: dado un docstring de Python a medio escribir (e.g., `def f(self, files, obj, state, size, shape, option): """...:param size:...:param`), predecir el nombre de la siguiente variable (`:param shape`).
- **Dataset corrupto**: dataset `random_random` (nombres de variables y docstring aleatorios).
- **Circuito manual de referencia** (Heimersheim & Janiak 2023): 8 cabezas principales (0.2, 0.4, 0.5, 1.4, 2.0, 3.0, 3.6), **37 aristas**.

| Configuración | KL divergence ↓ | Logit diff ↑ | Nº aristas |
|---|:---:|:---:|:---:|
| Modelo completo | 0 | 0.48 | 1.377 |
| ACDC (KL, τ=0.005) | 0.33 | **0.58** | 258 |
| ACDC (KL, τ=0.095) | 1.2 | -1.7 | **34** |
| ACDC (LD, τ=0.067) | 0.67 | 0.32 | 98 |
| Manual (8 cabezas, todas conexiones) | 0.83 | -0.62 | 464 |
| Circuito manual de referencia | 1.1 | -1.6 | 37 |

ACDC (KL, τ=0.005) supera al circuito manual en ambas métricas mientras usa **258 aristas** vs. 464. ACDC (LD, τ=0.067) contiene **93% menos aristas** que el grafo completo y **79% menos** que el circuito manual de cabezas, con mejor rendimiento. AUC(KL, corrupted) = **0.982**.

### Tarea 3: Greater-Than (GPT-2 small)

- **Tarea**: dado '*The war lasted from 1517 to 15*', predecir '18' o '19' o cualquier número mayor que '17' (Hanna et al. 2023).
- **Métrica**: diferencia de probabilidad (suma de probabilidades de años ≥ 18 menos suma de ≤ 17).
- **Dataset**: $$N=100$$ ejemplos. **Dataset corrupto**: dataset '01' (sin sesgo hacia ningún año en particular).
- **Circuito manual** (Hanna et al. 2023): 5 clases de componentes, **262 aristas** (nivel Q/K/V). Probability difference del circuito: **72%** (modelo: **84%**). KL divergence del circuito: **0.078**.

**Resultado**: ACDC selecciona **68 aristas** de 32.000 (threshold $$\tau = 0.01585$$), todas encontradas manualmente en Hanna et al. Redescubre **5/5 clases de componentes**. **Cero falsos positivos**. AUC(KL, corrupted) = **0.853**.

### Tarea 4: tracr-xproportion

- **Tarea**: dado `["a", "x", "b", "x"]`, producir `[0, 0.5, 0.33, 0.5]` (proporción acumulada de 'x' hasta cada posición). Modelo: transformer compilado con tracr (Lindner et al. 2023).
- **Métrica**: error cuadrático medio (MSE / L2).
- **Dataset corrupto**: permutaciones aleatorias sin puntos fijos.
- **Circuito de referencia exacto** (conocido al 100%): **10 aristas**.

**Resultado con activaciones cero**: AUC = **1.000** (circuito recuperado perfectamente a cualquier $$\tau > 0$$, incluso a nivel de neuronas individuales). Con activaciones corruptas: AUC = **0.679** (la distribución corrupta específica de este modelo sintético es problemática).

### Tarea 5: tracr-reverse

- **Tarea**: dado `[0, 3, 2, 1]`, producir `[1, 2, 3, 0]` (invertir la lista). Modelo: transformer de 3 capas compilado con tracr.
- **Métrica**: L2 entre vectores one-hot de la lista invertida.
- **Circuito de referencia exacto**: **15 aristas**.

**Resultado con activaciones cero**: AUC = **1.000**. Con activaciones corruptas: AUC = **0.200** (el peor resultado de ACDC en todas las tareas), lo que demuestra que la distribución corrupta es un hiperparámetro crítico.

### Tarea 6: Induction (transformer 2 capas, 8 cabezas)

- **Modelo**: transformer attention-only de 2 capas entrenado en OpenWebText.
- **Tarea**: dada la secuencia "A B … A", predecir "B" (e.g., "Vernon Dursley and Petunia Durs" → "ley").
- **Dataset**: 40 secuencias de 300 tokens con al menos una instancia de inducción [A][B]...[A][B]. Solo se mide KL divergence en las posiciones del segundo B.
- **Grafo**: **305 aristas** totales.
- **Evaluación**: no hay circuito manual de referencia; se usa Pareto frontier KL vs. número de aristas en test set.

**Resultado**: ACDC domina el Pareto frontier sobre SP y HISP para circuitos con más de 20 aristas. Recupera las dos induction heads (1.5, 1.6) y una previous token head (0.0), consistente con Goldowsky-Dill et al. (2023). El orden de iteración es un hiperparámetro importante: iterar en orden creciente de índice de cabeza da mejores resultados.

## Ejemplo ilustrativo

**Aplicación de ACDC a la tarea IOI con el prompt**: "When John and Mary went to the store, Mary gave a bottle of milk to"

**Input**: Grafo completo $$G$$ de GPT-2 small con ~32.000 aristas; dataset de 50 ejemplos del template IOI; dataset corrupto (ABC dataset: "When Alice and Bob went to the store, Charlie gave a bottle of milk to"); threshold $$\tau = 0.0575$$.

**Paso 1 — Inicialización**: $$H = G$$ (todas las aristas incluidas). $$D_{KL}(G \| H) = 0$$.

Implementación concreta: se hace un forward pass previo en cada $$x'_i$$ corrupto y se cachean todas las activaciones. Al evaluar $$H_\text{new} = H \setminus \{w \to v\}$$, se reemplaza la activación de $$w$$ que llega a $$v$$ con el valor cacheado de $$x'_i$$.

**Paso 2 — Nodo de output (resid\_post)**:
ACDC examina cada arista entrante al nodo de output en orden lexicográfico de capas tardías a tempranas. Para la arista "Head 9.9 → output": se reemplaza la contribución de 9.9 al residual stream final con la activación de 9.9 en el input corrupto. La KL divergence sube significativamente ($$>\tau$$), la arista se **mantiene**. Para "Head 1.3 → output": la KL divergence apenas cambia ($$<\tau$$), la arista se **elimina permanentemente**.

**Paso 3 — Nodos de capas anteriores**: Una vez procesado el output, ACDC procesa las cabezas de la capa 11, luego 10, etc. Solo examina las cabezas que siguen en $$H$$ (las que tienen al menos una arista saliente a un nodo que ya se procesó). Para cada una, examina sus aristas entrantes y elimina las irrelevantes.

**Resultado**: Tras **8 minutos** (NVIDIA A100), $$H$$ contiene las cabezas {9.9, 9.6, 10.0, 7.3, 8.6, 7.9, 8.10, 5.5, 2.2} y las aristas entre ellas. Todas son del circuito IOI manual. La KL divergence del circuito resultante es significativamente menor que la de un modelo ablacionado aleatoriamente.

**Comparación**: Wang et al. (2022) tardaron ~3 meses para las 26 cabezas. ACDC obtiene las 9 cabezas centrales (con cero falsos positivos) en 8 minutos.

## Resultados principales

### Tabla de AUCs — activaciones corruptas (configuración principal)

| Métrica | Tarea | ACDC (aristas) | HISP (aristas) | SP (aristas) | ACDC (nodos) | HISP (nodos) | SP (nodos) |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| KL | Docstring | **0.982** | 0.805 | 0.937 | 0.950 | 0.881 | 0.928 |
| KL | Greater-Than | **0.853** | 0.693 | 0.806 | 0.890 | 0.642 | 0.827 |
| KL | IOI | **0.869** | 0.789 | 0.823 | 0.880 | 0.668 | 0.842 |
| Pérdida | Docstring | 0.972 | 0.821 | **0.942** | 0.938 | 0.889 | 0.941 |
| Pérdida | Greater-Than | 0.461 | 0.706 | **0.812** | 0.766 | 0.631 | 0.811 |
| Pérdida | IOI | 0.589 | **0.836** | 0.707 | 0.777 | 0.728 | 0.797 |
| Pérdida | tracr-Proporción | 0.679 | 0.679 | 0.525 | 0.750 | **0.909** | 0.818 |
| Pérdida | tracr-Reverse | 0.200 | 0.577 | 0.193 | 0.312 | **0.750** | 0.375 |

### Tabla de AUCs — activaciones cero

| Métrica | Tarea | ACDC (aristas) | HISP (aristas) | SP (aristas) | ACDC (nodos) | HISP (nodos) | SP (nodos) |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| KL | Docstring | **0.906** | 0.805 | 0.428 | 0.837 | 0.881 | 0.420 |
| KL | Greater-Than | **0.701** | 0.693 | 0.163 | **0.887** | 0.642 | 0.134 |
| KL | IOI | 0.539 | **0.792** | 0.486 | 0.458 | 0.671 | 0.605 |
| Pérdida | Docstring | **0.929** | 0.821 | 0.482 | 0.825 | 0.889 | 0.398 |
| Pérdida | Greater-Than | 0.491 | **0.706** | 0.639 | 0.783 | 0.631 | 0.522 |
| Pérdida | IOI | 0.447 | **0.836** | 0.393 | 0.424 | 0.728 | 0.479 |
| Pérdida | tracr-Proporción | **1.000** | 0.679 | 0.829 | **1.000** | 0.909 | **1.000** |
| Pérdida | tracr-Reverse | **1.000** | 0.577 | 0.801 | **1.000** | 0.750 | **1.000** |

**Resumen**: ACDC con KL y activaciones corruptas es el mejor método en 3 de 3 tareas "en la naturaleza" (IOI, Docstring, Greater-Than). Con activaciones cero, ACDC recupera perfectamente los circuitos de los modelos tracr sintéticos (AUC = 1.000) porque esos modelos no tienen activaciones en componentes irrelevantes: la distribución corrupta ideal es simplemente cero.

## Problemas del proceso manual y por qué ACDC es más óptimo

El proceso manual (ejemplificado por Wang et al. 2022 con el circuito IOI) tiene varios problemas estructurales que ACDC resuelve:

### Problemas del proceso manual

1. **No escala**: el circuito IOI tomó ~3 meses de trabajo intensivo en GPT-2 small (117M parámetros). Aplicar la misma metodología a modelos de 70B parámetros es prácticamente inviable.

2. **Dependencia de la intuición humana**: el back-tracing iterativo del proceso IOI requiere decidir manualmente a qué cabezas parchear a continuación. Las Backup Name Mover Heads y las Negative Name Mover Heads sólo se descubrieron por accidente (al knockoutear las principales). No hay garantía de que todos los componentes relevantes sean descubiertos.

3. **Sesgo de búsqueda hacia componentes "positivos"**: el proceso manual optimiza implícitamente para encontrar cabezas que contribuyen positivamente a la métrica (logit difference). Los componentes que **reducen** la métrica (Negative Name Mover Heads) o que son redundantes (Backup Name Mover Heads) son sistemáticamente pasados por alto o descubiertos tardíamente.

4. **Completitud no verificada**: la búsqueda greedy de incompleteness score en Wang et al. encuentra scores de hasta 3.09 (87% del baseline), mostrando que el circuito de 26 cabezas no es completo. El proceso manual no tiene una forma sistemática de saber cuándo detenerse.

5. **Cobertura limitada del espacio de aristas**: el proceso IOI analiza el grafo a nivel de cabezas completas, ignorando la separación Q/K/V. ACDC opera sobre 1.041 aristas (separando queries, keys y values por posición), un espacio de búsqueda que sería imposible cubrir manualmente.

6. **Irreproducibilidad**: no es posible saber con certeza si dos investigadores que aplican el mismo proceso manual llegarían al mismo circuito.

### Ventajas de ACDC sobre el proceso manual

1. **Velocidad**: 8 minutos vs. ~3 meses para IOI. Varias horas para experimentos completos con todos los 32.923 aristas de GPT-2 small.

2. **Sistematicidad**: ACDC explora cada arista del grafo computacional en orden topológico inverso, sin omisiones ni dependencia de intuición.

3. **Métricas principiadas**: la KL divergence es no-negativa siempre, lo que simplifica la condición de eliminación de aristas y es más estable que la logit difference (que puede ser positiva o negativa, causando inestabilidades).

4. **Cero falsos positivos** en Greater-Than: de 32.000 aristas, ACDC selecciona exactamente 68, todas correctas. Esto es imposible conseguir manualmente en un tiempo razonable.

5. **Comparación sistemática**: el framework ROC permite comparar cuantitativamente diferentes métodos de descubrimiento de circuitos, algo imposible antes de este paper.

6. **Generación de hipótesis novedosas**: ACDC puede aplicarse a nuevos comportamientos sin haber leído la literatura previa sobre ese comportamiento.

### Limitaciones de ACDC que el proceso manual no tiene

1. **No recupera componentes negativos**: ACDC sistemáticamente falla en encontrar cabezas que perjudican la métrica (como las Negative Name Mover Heads de IOI). El proceso manual las encontró (aunque por accidente). Con KL divergence esto mejora algo, pero siguen sin recuperarse a thresholds razonables.

2. **No maneja OR gates**: si dos inputs $$A$$ y $$B$$ actúan como puerta OR (cualquiera de los dos es suficiente para producir el output), ACDC sólo conserva uno de los dos al iterar sobre padres de un nodo. El primer input que evalúa puede ser eliminado porque el segundo lo suple, y luego el segundo se mantiene, pero el resultado es un circuito incompleto. El proceso manual puede detectar OR gates con experimentos ad hoc.

3. **Sensibilidad al threshold**: no existe un $$\tau$$ óptimo universal. Valores grandes dan pocos falsos positivos pero pierden componentes; valores pequeños recuperan todo pero incluyen muchas aristas extraneous.

4. **La ground truth es imperfecta**: los circuitos manuales usados como referencia fueron producidos por humanos con limitaciones de tiempo, por lo que los AUCs están midiendo recuperación respecto a un gold standard imperfecto.

## Summarization motif

Aplicando ACDC a la tarea de predicción de pronombres con género en GPT-2 small (e.g., "The nurse said that **she**"), los autores observan que las MLPs tienen mayor importancia que las cabezas de atención, a diferencia de la tarea IOI. En particular, **MLP 7 en la posición del token " is" tiene el mayor número de conexiones entrantes de cualquier nodo del subgrafo**, recibiendo información de múltiples capas anteriores y actuando como hub de resumen. Esta observación no podría haberse hecho con herramientas de interpretabilidad más simples como saliency maps.

Esta estructura — un MLP de capa media en una posición semánticamente importante que agrega y redistribuye información — es el primer ejemplo del **summarization motif** (Tigges et al. 2023): un patrón recurrente donde ciertos MLPs en posiciones clave funcionan como nodos de condensación de información semántica.

## Ventajas respecto a trabajos anteriores

- **Automatización escalable**: reduce el descubrimiento de circuitos de meses a horas, abriendo la posibilidad de aplicar circuit analysis a modelos más grandes y a más comportamientos.
- **Intervenciones causales principiadas**: a diferencia de métodos de pruning que usan gradientes como proxy de importancia (HISP), ACDC mide directamente el impacto causal de cada arista mediante intervenciones de intercambio.
- **KL divergence universal**: aplicable a cualquier tarea de predicción del siguiente token sin especificar etiquetas, más robusta que métricas como logit difference.
- **Primer framework de evaluación de circuit discovery**: las curvas ROC permiten comparar métodos sistemáticamente, un estándar antes inexistente.
- **Validación objetiva**: usa circuitos de Wang et al., Hanna et al. y Heimersheim & Janiak como ground truth, permitiendo evaluación cuantitativa.
- **Código abierto**: `ArthurConmy/Automatic-Circuit-Discovery` en GitHub.

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
