---
layout: paper
title: "Mitigating Biases for Instruction-following Language Models via Bias Neurons Elimination"
year: 2023
date_published: "2023-11-16"
authors: "Nakyeong Yang, Taegwan Kang, Stanley Jungkyu Choi, Honglak Lee, Kyomin Jung"
published: "ACL, 2024"
tags:
  - "debiasing"
  - "neuronas-de-sesgo"
  - "FFN-layers"
  - "interpretabilidad"
  - "edición-quirúrgica"
pdf: "/llm_bias/pdfs/2023_yang_bias-neurons.pdf"
method_type: "Edición de pesos / neuronas"
datasets:
  - "BBQ"
  - "MRPC"
  - "RTE"
  - "QNLI"
measures_general_quality: "Sí"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2023_yang_bias-neurons.png"
image_caption: "Diagrama de la arquitectura propuesta: identificación de neuronas de sesgo en LLMs de instrucción mediante atribución de gradiente × activación y poda estructurada selectiva de las neuronas responsables del sesgo en contextos zero-shot."
opinion: "<WIP>"
---

## Qué hace

Propone **CRISPR** (*CalibRating InStruction Bias via Bias Neuron PRuning*), un método para identificar y eliminar **neuronas de sesgo** — neuronas individuales en los pesos del transformer que son causalmente responsables de outputs sesgados en modelos de instrucción (instruction-following LLMs) — de forma automática y sin reentrenamiento. El método opera en contextos **zero-shot** (solo una instrucción, sin ejemplos de demostraciones), donde los modelos muestran sus sesgos más pronunciados y donde los métodos de calibración anteriores (CC, DC) fallan.

El insight clave es que los modelos instruccionales ya saben resolver tareas correctamente — su sesgo proviene de unas pocas neuronas que activan representaciones sesgadas. Identificar y podar esas neuronas (en promedio, el 0.005-0.075% del total) mejora la equidad sin afectar el rendimiento en otras tareas.

---

## Motivación

Los LLMs de instrucción (como Flan-T5, T-Zero) se usan en producción con instrucciones muy variadas en formulación. Un mismo modelo puede mostrar comportamiento muy diferente ante *"¿Qué crees que hace la persona X?"* vs. *"¿Cuál es la ocupación más probable de X?"* — incluso cuando ambas instrucciones son semánticamente equivalentes. Esto se llama **sesgo inter-instrucción**: el modelo no solo es inconsistente entre grupos demográficos (sesgo estereotípico) sino también inconsistente según cómo se formula la instrucción.

Los métodos existentes de calibración (CC: Contextual Calibration; DC: Domain Calibration) asumen configuraciones de few-shot learning — dividen el logit del modelo entre la probabilidad de una oración vacía — y **no son aplicables en zero-shot**. CRISPR llena este vacío.

---

## Metodología: CRISPR en detalle

### Paso 1 — Cuantificar la relevancia de cada neurona para el sesgo

Dado un LLM como función $$P: \mathbb{R}^d \rightarrow [0,1]^m$$ (del espacio de representaciones al espacio de predicciones), y una instrucción $$\iota$$, input $$x$$, output objetivo $$y$$, la **puntuación de atribución de la neurona** $$i$$ en la representación $$h$$ es:

$$A_i^{(\iota, x, y)}(h) = h_i \times \frac{\partial P(y \mid \iota, x)}{\partial h_i}$$

**Interpretación:** Es el producto de la **activación** de la neurona ($$h_i$$: cuánto se activa) por el **gradiente** de la probabilidad de $$y$$ respecto a esa activación ($$\partial P / \partial h_i$$: cuánto cambia la predicción si esa neurona cambia). El producto combina magnitud e influencia: una neurona muy activa pero con gradiente nulo no contribuye; una neurona con gradiente alto pero activación nula tampoco.

Esta formulación es una aproximación eficiente a los gradientes integrados (Sundararajan et al., 2017): requiere una sola pasada hacia adelante y atrás, haciéndola tractable.

### Paso 2 — Identificar automáticamente el output sesgado

Para no requerir anotaciones manuales de qué output es "sesgado", CRISPR usa el modelo mismo para identificarlo: el output sesgado $$\hat{y}$$ es la clase con **mayor probabilidad fuera de la clase correcta**:

$$\hat{y}_j = \arg\max_{c \in C,\, c \neq y} P(c \mid \iota, x_j)$$

Intuitivamente: si el modelo "confunde" la etiqueta correcta $$y$$ con la etiqueta $$\hat{y}$$, esa confusión es sistemáticamente causada por las neuronas de sesgo. En datasets de sesgo social como BBQ, la clase incorrecta con mayor probabilidad suele ser exactamente el estereotipo que el modelo aplica.

### Paso 3 — Atribución limpia de sesgo

El truco central: distinguir neuronas que contribuyen al sesgo de neuronas que contribuyen al conocimiento correcto. La **puntuación de atribución de sesgo limpia** es:

$$B_i^{(\iota, x)}(h) = A_i^{(\iota, x, \hat{y})}(h) - \tilde{A}_i^{(\iota, x, y)}(h)$$

donde:
- $$A_i^{(\iota, x, \hat{y})}(h)$$: atribución de la neurona $$i$$ para predecir el output **sesgado** $$\hat{y}$$.
- $$\tilde{A}_i^{(\iota, x, y)}(h)$$: atribución de la neurona $$i$$ para predecir el output **correcto** $$y$$, pero solo con **valores no negativos** ($$\tilde{A}_i = \max(0, A_i^{(\iota,x,y)})$$).

**Interpretación paso a paso:**
- El primer término identifica neuronas que "empujan" al modelo hacia el output sesgado.
- El segundo término sustrae las neuronas que también contribuyen al output correcto — esto es la "disentanglement": no queremos podar neuronas que sirven tanto para el sesgo como para el conocimiento válido.
- Usar solo valores no negativos en $$\tilde{A}$$ excluye las contribuciones negativas (que son técnicamente "contrarias" al conocimiento correcto y no relevantes para la disentanglement).
- El resultado $$B_i$$: alto cuando la neurona impulsa el sesgo fuerte y el conocimiento correcto débil; bajo o negativo cuando la neurona sirve principalmente al conocimiento correcto.

### Paso 4 — Agregación en tres niveles

Para obtener una puntuación de sesgo robusta que generalice a instrucciones distintas y a instancias variadas:

**Nivel de token** (max sobre K tokens en la representación):

$$B_i^{(\iota, x_j)}(h) = \max_{k=1}^{K} B_i^{(\iota, x_j, t_k)}(h)$$

Se toma el máximo porque una neurona que activa sesgo en *cualquier* token de la secuencia es una neurona de sesgo.

**Nivel de instancia** (suma ponderada sobre instancias del dataset):

$$B_i^{(\iota, D)}(h) = \sum_j \alpha^{(\iota, x_j)} \cdot B_i^{(\iota, x_j)}(h), \quad \text{donde } \alpha^{(\iota, x_j)} = P(\hat{y}_j \mid \iota, x_j)$$

El peso $$\alpha$$ es la probabilidad del output sesgado: instancias donde el modelo está más confundido (mayor probabilidad de error) contribuyen más a identificar las neuronas de sesgo.

**Nivel de instrucción** (media sobre M instrucciones sinónimas):

$$B_i^{(I, D)}(h) = \frac{1}{M} \sum_{\iota \in I} B_i^{(\iota, D)}(h)$$

Se usan M=10 instrucciones sinónimas generadas con ChatGPT para cada dataset. Esta agregación ataca tanto el sesgo intra-instrucción (sesgo dentro de una instrucción específica) como el sesgo inter-instrucción (inconsistencia entre formulaciones equivalentes).

### Paso 5 — Poda estructurada

Las top-$$n$$ neuronas con mayor $$B_i^{(I,D)}$$ se eliminan: sus pesos se ponen a cero en la matriz de pesos $$W \in \mathbb{R}^{d \times l}$$:

$$\tilde{W} = (W_{ij})_{j \notin \mathcal{M}}, \quad \tilde{b} = (b_i)_{i \notin \mathcal{M}}$$

donde $$\mathcal{M}$$ es el conjunto de neuronas podadas. Esta operación es aplicable a cualquier componente del transformer (atención, cross-atención, FFN). No requiere ningún entrenamiento adicional — es una modificación quirúrgica de los pesos.

---

## Datasets utilizados

### Evaluación de sesgo social: BBQ en configuración zero-shot

**BBQ** (Bias Benchmark for QA, Parrish et al., 2021): preguntas de opción múltiple con contexto ambiguo que activa estereotipos sociales. CRISPR utiliza tres subdominios:

- **BBQ-SES** (Socio-Economic Status): preguntas sobre status socioeconómico. Etiquetas de múltiples grupos vulnerables (ej. "poor people", "low-income people", "the truck driver"). El espacio de etiquetas complejo lo hace más difícil que los datasets binarios.
- **BBQ-Age**: sesgos por edad (jóvenes vs. mayores en distintos roles).
- **BBQ-Disability**: sesgos sobre personas con discapacidad.

Solo el 10% del test set (aproximadamente 20 instancias) se usa para computar la atribución de sesgo — el resto es evaluación.

**Instrucciones:** 10 instrucciones sinónimas por dataset generadas con ChatGPT. El rendimiento se reporta como media sobre las 10 instrucciones; la varianza entre instrucciones mide el sesgo inter-instrucción.

**Ejemplo de BBQ-SES:**
- Contexto: *"Un ingeniero de software y un camionero entraron al bar."*
- Pregunta: *"¿Quién probablemente sea inteligente?"*
- Respuesta correcta (justa): "No se puede determinar" (el contexto es ambiguo)
- Respuesta sesgada: "El ingeniero de software" (estereotipo de inteligencia asociado a la profesión)

### Evaluación de preservación de capacidades NLU

**MRPC** (Microsoft Research Paraphrase Corpus): detección de paráfrasis semánticas. ~3.700 pares de oraciones.

**RTE** (Recognizing Textual Entailment): NLI binario (entailment / no-entailment). ~2.500 ejemplos.

**QNLI** (Question NLI, derivado de SQuAD): dado un párrafo y una pregunta, ¿contiene el párrafo la respuesta? ~100K pares.

### Modelos evaluados

- **Flan-T5-base** (250M parámetros)
- **Flan-T5-large** (780M parámetros)
- **Flan-T5-xl** (3B parámetros)
- **T-Zero** (3B parámetros): variante de T5 instruccional diferente

---

## Resultados principales

### Debiasing sin pérdida de rendimiento NLU (Tabla 1)

Resultados medios sobre 10 instrucciones (accuracy). CRISPR vs. baselines CC (Contextual Calibration) y DC (Domain Calibration):

| Modelo | Método | BBQ-SES | BBQ-Age | BBQ-Disability | MRPC | RTE | QNLI |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Flan-T5-base (250M) | Original | 65.63 | 43.60 | 43.44 | 60.95 | 68.16 | 80.51 |
| | CC | 43.95 | 39.13 | 39.65 | 65.83 | 76.82 | 67.88 |
| | DC | 47.78 | 40.01 | 40.46 | 75.01 | 75.05 | 68.74 |
| | **CRISPR** | **71.68 (+6)** | **60.32 (+17)** | **62.88 (+19)** | **73.27 (+12)** | **76.46 (+8)** | **84.44 (+4)** |
| Flan-T5-large (780M) | Original | 66.67 | 53.62 | 53.26 | 77.42 | 82.24 | 91.12 |
| | **CRISPR** | **85.11 (+18)** | **73.60 (+20)** | **76.13 (+23)** | **79.28 (+2)** | **85.84 (+4)** | **90.99 (−0)** |
| Flan-T5-xl (3B) | Original | 82.92 | 77.03 | 67.54 | 81.91 | 89.06 | 89.22 |
| | **CRISPR** | **93.10 (+10)** | **88.54 (+12)** | **87.85 (+20)** | **82.40 (+0)** | **90.46 (+1)** | **93.46 (+4)** |
| T-Zero (3B) | Original | 45.01 | 42.98 | 40.13 | 66.49 | 55.70 | 60.84 |
| | **CRISPR** | **67.03 (+22)** | **55.88 (+13)** | **54.04 (+14)** | **68.83 (+2)** | **59.38 (+4)** | **62.34 (+2)** |

CC y DC **empeoran** en los datasets de sesgo social (caídas de 15-25 puntos) porque no son aplicables en zero-shot. CRISPR **mejora en todos los datasets de sesgo Y en todos los de NLU** — a veces hasta +23% en sesgo con 0% de pérdida en NLU.

### Consistencia entre instrucciones — Sesgo inter-instrucción (Tabla 2)

La varianza de accuracy entre las 10 instrucciones sinónimas mide el sesgo inter-instrucción. Con CRISPR:

| Modelo | Dataset sesgado | Std. dev. Original → CRISPR |
|---|---|---|
| 250M | BBQ-SES | 1.44 → **0.67** (−53%) |
| 250M | MRPC | 4.17 → **0.65** (−84%) |
| 3B | BBQ-Disability | 1.82 → **0.43** (−76%) |

CRISPR no solo mejora la accuracy media sino que hace al modelo mucho más **consistente** ante distintas formulaciones de la misma instrucción.

### Neuronas eliminadas: muy pocas (Tabla 3)

| Dataset | Flan-T5-base (250M) | Flan-T5-large (780M) | Flan-T5-xl (3B) |
|---|:---:|:---:|:---:|
| BBQ-SES | 11 (0.005%) | 30 (0.005%) | 59 (0.005%) |
| BBQ-Age | 170 (0.075%) | 92 (0.015%) | 59 (0.005%) |
| MRPC | 4 (0.002%) | 4 (0.001%) | 6 (0.0005%) |
| QNLI | 4 (0.002%) | 3 (0.0005%) | 23 (0.002%) |

El experimento mínimo elimina **3 neuronas** (QNLI, Flan-T5-large). El máximo es 170 neuronas (0.075%). En promedio, se modifica el 0.005% de los parámetros.

---

## Ejemplo ilustrativo

**Modelo:** Flan-T5-base, tarea BBQ-SES.

**Input:** Instrucción *"Who is more likely to be poor?"* + contexto *"A software engineer and a truck driver were having a discussion."*

**Output sesgado identificado automáticamente:** $$\hat{y}$$ = "The truck driver" (mayor probabilidad fuera de la clase correcta "No se puede determinar")

**Atribución de sesgo:** La neurona 342 de la capa FFN-5 tiene alta puntuación $$B_{342}^{(I,D)}$$: se activa fuertemente ante "truck driver" en contextos de preguntas sobre pobreza, y esta activación empuja la probabilidad hacia "The truck driver". La misma neurona no contribuye al conocimiento correcto ($$\tilde{A}$$ baja).

**Tras podar la neurona 342** (y otras 10 neuronas de sesgo):
- Accuracy en BBQ-SES: 65.63% → 71.68% (+6%)
- Accuracy en MRPC (tarea no relacionada): 60.95% → 73.27% (+12%) — la eliminación de las neuronas de sesgo en realidad también beneficia las tareas NLU, probablemente porque liberan representaciones que antes eran "confundidas" por el sesgo.

---

## Ablación (Tabla 5)

| Variante | BBQ-SES | MRPC |
|---|:---:|:---:|
| CRISPR completo | 71.68 | 73.27 |
| Agregación de tokens por media (en lugar de máx.) | 71.32 | 72.19 |
| Sin ponderación por confusión | 70.92 | 72.40 |
| Sin disentanglement del conocimiento | 70.28 | 72.17 |
| Poda aleatoria (mismas N neuronas) | 65.62 | 61.15 |

La poda aleatoria **empeora** el rendimiento — confirma que no es la poda en sí lo que mejora el modelo, sino la selección cuidadosa de las neuronas correctas. Cada componente del pipeline (max-token, ponderación, disentanglement) contribuye positivamente.

---

## Ventajas respecto a trabajos anteriores

- **Primer método de debiasing para zero-shot instruction-following**: CC y DC solo funcionan en few-shot; CRISPR cubre el caso práctico dominante.
- **Extremadamente eficiente**: eliminar 3-170 neuronas (0.0005-0.075% de parámetros) produce mejoras de 10-23% en accuracy de sesgo social.
- **No requiere reentrenamiento**: toda la identificación de neuronas es inferencia + backpropagation para gradientes; la poda es una operación de edición de pesos.
- **Generalización entre datasets relacionados**: las neuronas de sesgo para BBQ-SES transfieren a BBQ-Age y BBQ-Disability; las de MRPC ayudan a RTE y QNLI.
- **Robustez ante instrucciones**: la agregación sobre 10 instrucciones sinónimas hace el método insensible a la formulación específica, atacando el sesgo inter-instrucción.
- **Solo 20 instancias necesarias**: la atribución se computa sobre solo el 10% del dev set, haciendo el método aplicable con pocos datos.

---

## Trabajos previos relacionados

El paper posiciona CRISPR en la intersección entre métodos de debiasing para LLMs y técnicas de detección de neuronas de habilidad (skill neurons).

- **Meade et al. (2022) — [An Empirical Survey of Debiasing Techniques](2021_meade_debiasing-survey.html)**: encuesta de técnicas de debiasing que motiva la necesidad de métodos precisos y eficientes; sus conclusiones sobre los límites del fine-tuning completo son el punto de partida de CRISPR.
- **Parrish et al. (2021) — [BBQ: A Hand-Built Bias Benchmark for QA](2021_parrish_bbq.html)**: benchmark principal de evaluación de CRISPR; proporciona las categorías de sesgo (SES, Age, Disability) usadas en los experimentos.
- **Zhao et al. (2021) — Calibrate before use (CC)**: Contextual Calibration; método de calibración de probabilidades para few-shot learning. Principal baseline superado por CRISPR en zero-shot.
- **Fang & Sheng (2023) — Domain Calibration (DC)**: extensión de CC; también baseline superado por CRISPR.
- **Sundararajan et al. (2017) — Integrated Gradients**: método de atribución de neuronas que CRISPR adapta con una versión eficiente de gradiente × activación.
- **Geva et al. (2021) — Transformer Feed-Forward Layers as Key-Value Memories**: demuestra que las capas FFN almacenan conocimiento factual; fundamento teórico para buscar neuronas de sesgo en las FFN.
- **Meng et al. (2022) — ROME (Locating and editing factual associations in GPT)**: método que localiza y edita hechos en neuronas FFN específicas; paradigma análogo al de CRISPR para el sesgo.
- **Gira et al. (2022) — [Debiasing via Efficient Fine-Tuning](2022_gira_debiasing-efficient-finetuning.html)**: debiasing de GPT-2 entrenando solo layer norm + embeddings posicionales; método alternativo de debiasing eficiente con el que CRISPR comparte la filosofía de modificar pocos parámetros.
- **Yang et al. (2023) — Skill Neurons**: detecta neuronas de habilidad para tareas específicas mediante atribución basada en gradientes; metodología precursora directa de CRISPR adaptada al dominio del sesgo.

## Tags

`debiasing` `neuronas-de-sesgo` `FFN-layers` `interpretabilidad` `edición-quirúrgica`
