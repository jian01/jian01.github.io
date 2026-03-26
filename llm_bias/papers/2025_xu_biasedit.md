---
layout: paper
title: "BiasEdit: Debiasing Stereotyped Language Models via Model Editing"
year: 2025
date_published: "2025-03-11"
authors: "Xin Xu, Wei Xu, Ningyu Zhang, Julian McAuley"
published: "TrustNLP @ NAACL 2025"
tags:
  - "debiasing"
  - "edición-de-modelos"
  - "hiper-redes"
  - "FFN-layers"
  - "sesgo-de-género"
pdf: "/llm_bias/pdfs/2025_xu_biasedit.pdf"
method_type: "Edición de pesos / neuronas"
datasets:
  - "StereoSet"
  - "CrowS-Pairs"
  - "OpenBookQA"
  - "BoolQ"
  - "COPA"
measures_general_quality: "Sí"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2025_xu_biasedit.png"
image_caption: "Esquema del mecanismo de edición"
opinion: "<WIP>"
---

## Qué hace

Propone **BiasEdit**, un método de edición de modelos que elimina sesgos estereotipados de LLMs modificando quirúrgicamente una fracción pequeña de sus parámetros mediante **redes editoras** (editor networks) entrenadas como hiper-redes. Las redes editoras toman como entrada el gradiente de una pérdida de debiasing y producen como salida los deltas de pesos a aplicar sobre las capas MLP seleccionadas. Esto evita el fine-tuning completo y permite editar sesgo de género, raza y religión preservando las capacidades lingüísticas generales.

A diferencia de lo que el tag "ROME" podría sugerir, BiasEdit **no** usa el update rank-1 de ROME. Sí toma de ROME la metodología de **bias tracing** (causal tracing con runs limpios/corrompidos/restaurados) para localizar en qué capas reside el sesgo, pero el mecanismo de edición sigue la arquitectura de **MEND/MALMEN**: pequeñas redes que predicen actualizaciones de pesos.

---

## Problema que resuelve

Los métodos de debiasing existentes tienen limitaciones estructurales:
- **Fine-tuning con CDA** (datos contrafactuales): costoso computacionalmente, solo practicable en modelos pequeños como GPT-2.
- **Proyección de representaciones** (INLP, SentenceDebias): no modifican los parámetros internos del modelo, por lo que el sesgo sigue presente en los pesos — solo se "enmascara" en el espacio de representaciones.
- **Prompting** (Self-Debias): actúa en tiempo de inferencia sin tocar pesos; tiene degradación severa de LMS en modelos grandes (hasta -40% en Mistral-7B).
- **Adapters por tipo de sesgo**: requieren adapters separados para género, raza, religión; poco escalable.

---

## Metodología

### Formulación de la tarea

Para un contexto estereotipado como *"Girls tend to be more ___ than boys"*, el modelo asigna mayor probabilidad a la completación estereotipada (*"soft"*) que a la anti-estereotipada (*"determined"*). BiasEdit busca **igualar** esas probabilidades. Cada ejemplo de entrenamiento tiene tres elementos:

- $$x_{\text{stereo}}$$: oración con la completación estereotipada — e.g. *"Girls tend to be more soft than boys"*
- $$x_{\text{anti}}$$: oración con la completación anti-estereotipada — e.g. *"Girls tend to be more determined than boys"*
- $$x_{\text{mless}}$$: oración con una completación sin sentido — e.g. *"Girls tend to be more fish than boys"*

### Las redes editoras (editor networks)

BiasEdit entrena redes editoras $$g_{\phi_\ell}$$ para cada capa $$\ell$$ que se va a editar. Son redes pequeñas que aprenden, durante el entrenamiento, a mapear gradientes de pérdida a actualizaciones de pesos útiles.

Para cada capa $$\ell$$ seleccionada, la actualización funciona así:

**Paso 1.** Calcular el gradiente de la pérdida de debiasing $$\mathcal{L}_d$$ respecto a los pesos $$\mathcal{W}_\ell$$ de esa capa:
$$\nabla_{\mathcal{W}_\ell} \mathcal{L}_d(x_{\text{stereo}}, x_{\text{anti}}, \theta)$$

Este gradiente es un tensor del mismo tamaño que $$\mathcal{W}_\ell$$ que indica en qué dirección mover los pesos para reducir el sesgo.

**Paso 2.** Pasar ese gradiente por la red editora $$g_{\phi_\ell}$$, que aprende a convertirlo en un delta de pesos más preciso:
$$\tilde{\nabla}_{\mathcal{W}_\ell} = g_{\phi_\ell}\!\left(\nabla_{\mathcal{W}_\ell} \mathcal{L}_d\right)$$

Cualitativamente: el gradiente crudo puede ser ruidoso o excesivo. La red editora aprende durante el entrenamiento a "filtrar" ese gradiente para producir una actualización que reduce el sesgo sin dañar otras capacidades.

**Paso 3.** Aplicar el delta a los pesos:
$$\tilde{\mathcal{W}}_\ell = \mathcal{W}_\ell + \tilde{\nabla}_{\mathcal{W}_\ell}$$

Solo se modifican los pesos de las capas seleccionadas; el resto del modelo queda intacto.

### Loss 1 — Pérdida de debiasing $$\mathcal{L}_d$$

$$\mathcal{L}_d = \text{KL}\!\left(P_{\theta_{\tilde{\mathcal{W}}}}(x_{\text{stereo}}) \,\|\, P_{\theta_{\tilde{\mathcal{W}}}}(x_{\text{anti}})\right) + \text{KL}\!\left(P_{\theta_{\tilde{\mathcal{W}}}}(x_{\text{anti}}) \,\|\, P_{\theta_{\tilde{\mathcal{W}}}}(x_{\text{stereo}})\right)$$

**Desglose:**

- $$P_{\theta_{\tilde{\mathcal{W}}}}(x_{\text{stereo}})$$: distribución de probabilidad del modelo sobre los tokens de la completación estereotipada, bajo los pesos modificados $$\tilde{\mathcal{W}}$$. Es un vector de probabilidades sobre el vocabulario para cada posición de la oración.
- $$P_{\theta_{\tilde{\mathcal{W}}}}(x_{\text{anti}})$$: ídem para la completación anti-estereotipada.
- $$\text{KL}(P \| Q)$$: divergencia Kullback-Leibler de $$Q$$ a $$P$$; mide cuánto difieren las dos distribuciones. Vale 0 cuando son idénticas.
- La suma de las dos KL (en ambas direcciones) es equivalente a la **divergencia JS** (Jensen-Shannon), que es simétrica. Si las dos distribuciones son iguales, ambas KL valen 0 y la pérdida es 0.

**Cualitativamente**: la pérdida de debiasing es 0 cuando la distribución de probabilidades del modelo sobre los tokens de la oración estereotipada es idéntica a la de la anti-estereotipada. Fuerza al modelo a tratar las dos versiones con la misma probabilidad. Si el modelo aún prefiere *"soft"* sobre *"determined"*, la distribución de $$x_{\text{stereo}}$$ y $$x_{\text{anti}}$$ diferirán en el token de la completación y la KL será positiva.

### Loss 2 — Pérdida de retención $$\mathcal{L}_r$$

$$\mathcal{L}_r = \text{KL}\!\left(P_{\theta_{\mathcal{W}}}(x_{\text{mless}}) \,\|\, P_{\theta_{\tilde{\mathcal{W}}}}(x_{\text{mless}})\right)$$

**Desglose:**

- $$P_{\theta_{\mathcal{W}}}(x_{\text{mless}})$$: distribución del modelo **original** (pesos sin modificar $$\mathcal{W}$$) sobre la oración con completación sin sentido.
- $$P_{\theta_{\tilde{\mathcal{W}}}}(x_{\text{mless}})$$: distribución del modelo **editado** sobre la misma oración.
- $$x_{\text{mless}}$$ es semánticamente neutro (e.g. *"Girls tend to be more fish than boys"*) — una palabra que no tiene connotación social.

**Cualitativamente**: como $$x_{\text{mless}}$$ no contiene sesgo, el modelo original ya asignaba cierta distribución a sus tokens. Si la edición cambia esa distribución, significa que se está dañando el modelado lingüístico general. La pérdida de retención penaliza cualquier cambio en la distribución sobre texto sin connotación social, actuando como un anclaje para preservar las capacidades lingüísticas.

**Sin $$\mathcal{L}_r$$, el modelo colapsa**: la ablación muestra que sin retención, el ΔLMS cae hasta -52% en género y -61% en religión en GPT-2 Medium.

### Loss total

$$\mathcal{L}_E(\phi) = \mathcal{L}_d + \lambda \mathcal{L}_r$$

donde $$\phi$$ son los parámetros de las redes editoras (lo que se está entrenando), y $$\lambda$$ balancea las dos pérdidas.

### Arquitectura interna de la red editora (MALMENNet)

#### Qué se está editando exactamente

Un transformer tiene, en cada bloque, una capa de atención y una capa MLP (feed-forward network, FFN). La MLP tiene al menos dos matrices de proyección: una que expande la dimensión (`d_model → d_ff`) y otra que la contrae de vuelta (`d_ff → d_model`). BiasEdit edita **únicamente la proyección de salida** — `c_proj` en GPT-2, `down_proj` en Llama/Mistral/Gemma — y solo en los últimos bloques del transformer. La atención no se toca.

La elección de los últimos bloques es un compromiso: el bias tracing (ver más abajo) muestra que el sesgo reside principalmente en las MLPs de capas inferiores, pero editar esas capas daña más las capacidades generales. Los últimos bloques ofrecen el mejor balance entre reducción de sesgo y preservación lingüística.

| Modelo | Parámetros totales | Capa editada | Bloques | Forma de W | `key_size` | `value_size` | Parámetros editados |
|---|---|---|---|---|---|---|---|
| GPT-2 Medium | 345 M | `c_proj` | Últimos 3 | [4096 × 1024] | 4096 | 1024 | ~12.6 M |
| Mistral-7B-v0.3 | 7300 M | `down_proj` | Últimos 3 | [14336 × 4096] | 14336 | 4096 | ~176 M |
| Llama3-8B | 8030 M | `down_proj` | Últimos 2 | [14336 × 4096] | 14336 | 4096 | ~117 M |
| Gemma-2b | 2510 M | `down_proj` | Penúltimo | [16384 × 2048] | 16384 | 2048 | ~33.6 M |

La edición no es fine-tuning: **no se ejecuta ningún paso de descenso de gradiente sobre esos pesos**. En su lugar, se calcula una actualización $$\Delta W$$ de la misma forma que $$W$$ y se suma directamente. Esa actualización la produce la red editora.

#### Por qué una "red editora" y no simplemente el gradiente

El gradiente crudo de la pérdida de debiasing respecto a $$W$$ indicaría la dirección de máximo descenso de esa pérdida, pero no tiene por qué producir una edición quirúrgica: puede dañar capacidades lingüísticas no relacionadas. La red editora es una pequeña red neuronal entrenada para **aprender a refinar ese gradiente**: a partir de información sobre la activación concreta del ejemplo y el gradiente de la pérdida, predice cuánto y en qué dirección conviene mover los pesos para reducir el sesgo sin romper el modelo.

#### Qué es MALMENNet

La red editora implementa la arquitectura **MALMEN** (`MALMENNet` en `nets.py`). No es una red por capa del LM: hay **una MALMENNet por forma de peso única**. Como todos los bloques editados de un mismo modelo tienen las mismas dimensiones, normalmente hay una sola red para todos ellos. Las diferencias de comportamiento entre capas se manejan con **embeddings por módulo** dentro de la red.

Dimensiones relevantes para GPT-2 Medium (capas `c_proj`):
- `key_size` = 4096 (dimensión interna de la MLP, entrada a `c_proj`)
- `value_size` = 1024 (dimensión del modelo, salida de `c_proj`)
- `size` = `key_size + value_size` = 5120

Parámetros aproximados de MALMENNet para GPT-2 Medium (rank=1920, 2 bloques, 3 módulos):

| Componente | Fórmula | Parámetros aprox. |
|---|---|---|
| A por bloque | `size × rank` = 5120 × 1920 | ~9.8 M |
| B por bloque | `rank × size` = 1920 × 5120 | ~9.8 M |
| bias + scale + shift por bloque | `size + 2·(n_modules·size)` | ~36 K |
| × 2 bloques | | ~39.2 M |
| lr + lamda embeddings | `2·n_modules` | ~6 |
| **Total** | | **~39.2 M** |

Para Mistral-7B (`down_proj`, `size` = 18432): los bloques A y B suben a ~35 M cada uno → MALMENNet de ~142 M parámetros, lo cual es considerable pero aún mucho menor que el modelo editado (~7B).

#### Entradas — qué llega a la red editora

Para cada ejemplo del batch y para cada capa editada, se capturan dos vectores mediante hooks de PyTorch:

| Tensor | Forma | Qué representa |
|---|---|---|
| `keys` | `(batch, key_size)` | Activaciones de entrada a la capa en el **forward pass** del LM sobre el ejemplo de sesgo — lo que "veía" esa capa al procesar la oración |
| `values_grad` | `(batch, value_size)` | Gradiente del output de la capa en el **backward pass** — en qué dirección habría que mover la salida de esa capa para reducir la pérdida de debiasing |
| `module_idx` | `int` | Índice de la capa (para seleccionar sus embeddings scale/shift/lr/lambda dentro de la red) |

Estos vectores se cachean en disco (`.pth`) antes de pasarlos a la red editora. No se aplica ninguna descomposición previa (sin SVD, sin PCA).

Los `keys` y `values_grad` se **concatenan** en un único vector de tamaño `size = key_size + value_size` y se normalizan con el RunningMeanStd. Ese vector concatenado es la entrada efectiva a los MALMENBlocks.

#### El procesamiento interno: MALMENBlock

Cada bloque recibe el vector concatenado $$y \in \mathbb{R}^{\text{size}}$$ y produce una versión refinada del mismo tamaño:

$$z = \text{ReLU}(yAB + \text{bias})$$
$$\text{salida} = \text{scale}[m] \odot z + \text{shift}[m] + y$$

- La multiplicación $$yAB$$ proyecta $$y$$ a un espacio de dimensión `rank=1920` y lo devuelve a `size` — un **cuello de botella de bajo rango** que fuerza a la red a capturar solo las direcciones más informativas del gradiente.
- `scale[m]` y `shift[m]` son vectores aprendidos específicos para la capa $$m$$: permiten que capas distintas del LM tengan respuestas distintas dentro de la misma red.
- La suma final $$+ y$$ es una **conexión residual**: si la red no aprende nada útil, la salida es simplemente la entrada sin cambios.

Se aplican 2 bloques en cadena.

#### Salidas — qué produce la red editora

La salida de los dos bloques es un vector de tamaño `size`. Se divide en dos partes:

| Tensor | Forma | Qué representa |
|---|---|---|
| `pseudo_keys` | `(batch, key_size)` | Versión refinada de las activaciones de entrada |
| `pseudo_values_grad` | `(batch, value_size)` | Versión refinada del gradiente de salida |

Estos no se aplican directamente al modelo. Son los ingredientes para el paso siguiente.

#### Cálculo del delta de pesos (predict_param_shifts)

Con las pseudo-keys y pseudo-values-grad, se calcula $$\Delta W$$ mediante una **resolución de sistema lineal en forma cerrada** — equivalente a un único paso Newton regularizado, no a descenso de gradiente:

$$\text{mat} = K^\top K + \lambda I \qquad [k \times k]$$

$$\text{value\_diffs}_j = -\alpha \cdot \left(\sum_d K_{jd}\,\tilde{K}_{jd}\right) \cdot \tilde{V}_j$$

$$\Delta W = \text{solve}(\text{mat},\; K^\top \cdot \text{value\_diffs}) \qquad [k \times v]$$

Donde $$K$$ son las `keys` originales, $$\tilde{K}$$ / $$\tilde{V}$$ las pseudo-keys/values de la red, $$\alpha$$ el lr aprendido y $$\lambda$$ la regularización aprendida (ambos embeddings por módulo). El resultado $$\Delta W$$ tiene exactamente la misma forma que $$W$$ y se suma directamente: $$\tilde{W} = W + \Delta W$$.

#### Entrenamiento de la red editora

Lo que se entrena es **la MALMENNet** (sus parámetros $$\phi$$), no el LM. El LM se modifica temporalmente durante cada batch para calcular la pérdida, pero sus pesos se restauran antes de la siguiente iteración.

| Parámetro | Valor |
|---|---|
| Optimizador | Adam sobre `net.parameters()` |
| `meta_lr` | 1e-5 |
| `n_epochs` | 100 (early stopping, paciencia 5) |
| `batch_size` | 128 |
| `max_grad_norm` | 1 (gradient clipping) |
| `rank` (cuello de botella A×B) | 1920 |
| `n_blocks` | 2 |
| `loc_coef` (peso de $$\mathcal{L}_r$$) | 4.0 |

El bucle de entrenamiento tiene dos fases por batch:

1. **Fase caché**: forward + backward del LM sobre el batch → se capturan `keys` y `values_grad` via hooks → se guardan en disco.
2. **Fase de edición**: la red editora procesa las claves/gradientes → calcula $$\Delta W$$ → aplica $$\Delta W$$ temporalmente al LM → calcula `edit_loss + 4.0 * retention_loss` → retropropaga a través de la red editora → Adam actualiza los parámetros $$\phi$$.

En **inferencia** (test), la red editora se aplica una sola vez: se calculan los $$\Delta W$$ finales y se suman permanentemente a los pesos del LM. El resultado es un modelo debiaseado con los mismos parámetros pero ligeramente distintos en las capas MLP editadas.

### Bias tracing

Siguiendo la metodología de causal tracing de ROME, se realizan tres pasadas de inferencia para localizar el sesgo:

1. **Pasada limpia**: se obtiene la distribución estereotipada $$P_\theta(x_{\text{stereo}})$$ y anti-estereotipada $$P_\theta(x_{\text{anti}})$$; se guardan los estados ocultos $$h_i^\ell$$ para todos los tokens $$i$$ y capas $$\ell$$.
2. **Pasada corrompida**: se añade ruido gaussiano $$\tau \sim \mathcal{N}(0, \sigma)$$ a los embeddings de la **palabra de atributo de sesgo** (e.g. "girls") y se obtienen activaciones corrompidas $$\hat{h}_i^\ell$$.
3. **Pasada corrompida con restauración**: se restauran los estados ocultos originales $$h_i^\ell$$ en una posición/capa a la vez y se mide cuánto recupera el score de sesgo.

Resultado: las MLPs tienen "un papel mucho más significativo en el sesgo que las capas de atención", y el sesgo corresponde principalmente a los estados de las MLPs en capas inferiores.

### Batch editing

BiasEdit procesa los ejemplos de entrenamiento en lotes — el mismo tamaño de lote en train y test. Esto permite editar múltiples pares estereotipados en una sola operación, lo que mejora la eficiencia frente a edición uno a uno.

---

## Datasets utilizados

**Para entrenamiento y evaluación de sesgo:**

**StereoSet (intrasentence)**: dataset principal. Se divide en train/dev/test con ratio 8:1:1. El test set tiene:
- Género: 253 ejemplos
- Raza: 962 ejemplos
- Religión: 77 ejemplos

Cada ejemplo tiene una completación estereotipada, una anti-estereotipada y una sin sentido. Se entrena un editor por tipo de sesgo (género, raza, religión).

**CrowS-Pairs**: dataset de evaluación **fuera de distribución** (no se usa para entrenamiento). Permite validar que la edición generaliza a otro benchmark de sesgo.

**Para evaluar retención de capacidades generales:**

**OpenBookQA**, **BoolQ**, **COPA**: benchmarks de razonamiento y comprensión de lenguaje. Se mide la accuracy antes y después de la edición para verificar que no hay degradación.

Nota: BBQ, WinoBias, GLUE y MMLU **no se usan** en este paper a pesar de estar en el front matter original.

---

## Resultados principales

### StereoSet — Stereotype Score y ΔLMS

| Método | GPT2-m Género | GPT2-m Raza | GPT2-m Religión |
|---|:---:|:---:|:---:|
| Pre-edición (SS%) | 65.58 | 61.63 | 62.57 |
| CDA | 63.29 | 61.36 | 61.79 |
| SentenceDebias | 67.99 | 58.97 | 56.64 |
| Self-Debias | 60.28 | 57.29 | 57.61 |
| INLP | 63.17 | 60.00 | 58.57 |
| **BiasEdit** | **49.42** | **56.34** | **53.55** |

BiasEdit lleva el SS de género de 65.58 a **49.42** — casi exactamente 50 (ideal). Mejora de +13.26 puntos de distancia al ideal vs el mejor baseline (INLP). Resultados similares en Mistral-7B, Llama3-8B y Gemma-2b.

**ΔLMS de BiasEdit** (lo que se pierde en capacidad lingüística):
- Género GPT2-m: −8.82% — es el coste más alto
- Religión GPT2-m: −1.92% — casi sin impacto
- Self-Debias en comparación: hasta −40% en Mistral-7B

### Ablación: importancia de $$\mathcal{L}_r$$

| | GPT2-m Género SS | GPT2-m Género ΔLMS |
|---|:---:|:---:|
| Sin $$\mathcal{L}_r$$ | 52.55% | −52.36% |
| Con $$\mathcal{L}_r$$ | 49.42% | −8.82% |

Sin retención, el modelo colapsa. Con retención, el SS mejora **más** (49 vs 52) y el daño a LMS se reduce de 52% a 9%.

### Capacidades generales (Llama3-8B)

| Benchmark | Pre | Post |
|---|:---:|:---:|
| OpenBookQA | 80.80% | 78.94% |
| BoolQ | 70.00% | 65.18% |
| COPA | 68.00% | 67.90% |

Degradación de 1-5 puntos porcentuales — sustancialmente menor que métodos de fine-tuning completo.

### CrowS-Pairs (out-of-distribution)

BiasEdit generaliza al dataset no visto: SS de género baja de 61.46 a **53.08** en GPT2-medium, indicando que el debiasing no es superficial.

### Eficiencia

Entrenar las redes editoras de género para Mistral-7B toma ~5 horas en una GPU A800. Los métodos de subespacio (SentenceDebias) tardan más de 2 días para el mismo modelo.

---

## Ventajas respecto a trabajos anteriores

- **Primer uso de hiper-redes de edición (MEND/MALMEN) para debiasing**: edita solo parámetros de las MLPs seleccionadas en lugar de fine-tuning completo.
- **Mucho mejor reducción de sesgo que todos los baselines**: en género, BiasEdit lleva SS a ~49% vs el mejor baseline (Self-Debias a ~60%) en GPT2-medium.
- **Retención de capacidades lingüísticas**: la pérdida de retención $$\mathcal{L}_r$$ es la clave para que la edición no colapse el modelo.
- **Robustez semántica**: los sinónimos de los atributos de sesgo (evaluados con WordNet) también son debiaseados, indicando generalización más allá de los tokens exactos del training.
- **Escalable a modelos grandes**: funciona en Mistral-7B, Llama3-8B y Gemma-2b sin adaptaciones especiales.

---

## Trabajos previos relacionados

Los trabajos previos se organizan en dos líneas: métodos de debiasing clásicos y técnicas de edición de modelos.

- **Meng et al. (2022, 2023) — ROME / MEMIT**: técnicas de edición de conocimiento que localizan hechos en capas MLP específicas; BiasEdit adopta su metodología de **bias tracing** (causal tracing), aunque usa un mecanismo de edición diferente (hiper-redes en lugar de rank-1 updates).
- **Mitchell et al. (2022) — MEND / MALMEN**: hiper-redes que predicen actualizaciones de parámetros para edición de modelos; BiasEdit adopta directamente esta arquitectura como mecanismo de edición.
- **Nadeem et al. (2021) — [StereoSet](2021_nadeem_stereoset.html)**: benchmark principal; proporciona SS y LMS para cuantificar sesgo y preservación de capacidades.
- **Nangia et al. (2020) — CrowS-Pairs**: benchmark de evaluación fuera de distribución.
- **Meade et al. (2022) — [An Empirical Survey of Debiasing Techniques](2021_meade_debiasing-survey.html)**: establece la línea base comparativa (CDA, SentenceDebias, INLP, Self-Debias) y provee el código bias-bench usado para evaluación.
- **Ravfogel et al. (2020) — INLP**: baseline de proyección; elimina la dirección de género de las representaciones sin modificar parámetros.
- **Liang et al. (2020) — SentenceDebias**: baseline de proyección a nivel de oración.
- **Schick et al. (2021) — Self-Debias**: baseline de prompting; actúa en inferencia, con alta degradación de LMS en modelos grandes.

## Tags

`debiasing` `edición-de-modelos` `hiper-redes` `FFN-layers` `sesgo-de-género`
