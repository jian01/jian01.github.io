---
layout: paper
title: "Language Models Get a Gender Makeover: Mitigating Gender Bias with Few-Shot Data Interventions"
year: 2023
date_published: "2023-06-07"
authors: "Himanshu Thakur, Atishay Jain, Praneetha Vaddamanu, Paul Pu Liang, Louis-Philippe Morency"
published: "ACL (Short Papers), 2023"
tags:
  - "debiasing"
  - "data-augmentation"
  - "sesgo-de-género"
  - "BERT"
  - "few-shot"
pdf: "/llm_bias/pdfs/2023_thakur_gender-makeover.pdf"
method_type: "Data augmentation"
datasets:
  - "StereoSet"
  - "CrowS-Pairs"
  - "WikiText-2"
measures_general_quality: "No"
status:
  - "Leido"
image: "imgs/2023_thakur_gender-makeover.png"
image_caption: "Gráfico de barras mostrando la frecuencia de palabras asociadas al género en el dataset analizado: términos masculinos como \"he\", \"his\" y \"him\" dominan ampliamente frente a términos femeninos, ilustrando el desequilibrio de representación de género."
opinion: "<WIP>"
---

## Qué hace

Propone reducir el sesgo de género en LLMs mediante **intervenciones de datos**: reemplazar las palabras de género en un pequeño número de ejemplos de entrenamiento (tan pocos como 10) y hacer fine-tuning del modelo preentrenado con esos ejemplos modificados. El modelo base es `bert-base-uncased` y el fine-tuning se hace con el objetivo de **Masked Language Modeling (MLM)** estándar. No requiere modelos auxiliares ni cambios arquitectónicos — solo modificar el texto de los ejemplos de entrenamiento y volver a entrenar brevemente.

La contribución técnica central son **tres estrategias de intervención sobre las palabras de género**, cada una con diferente filosofía de reemplazo, y un método de **selección de los ejemplos más sesgados** usando el propio modelo para encontrar las instancias más útiles para el debiasing.

---

## Motivación y enfoque

El preentrenamiento de LLMs sobre texto de internet transfiere no solo conocimiento lingüístico sino también sesgos socioeducativos, incluyendo sesgos de género: el modelo aprende que ciertos roles o características se asocian más con un género que con otro. Reentrenar el modelo desde cero con datos balanceados es computacionalmente prohibitivo. Las técnicas algorítmicas (proyección de subespacios, adversarial training) requieren arquitecturas adicionales o son de difícil aplicación. Las técnicas de augmentación masiva de datos (CDA) requieren procesar el dataset completo.

Este paper propone un extremo opuesto: hacer fine-tuning sobre **solo 10 ejemplos** donde las palabras de género se han reemplazado por términos más neutrales o balanceados. La idea es que aunque el fine-tuning se hace con muy pocos ejemplos, el modelo aprende a distribuir la confianza de forma más equitativa entre géneros.

Un hallazgo adicional: **el propio modelo sesgado puede usarse para seleccionar los ejemplos más útiles para el debiasing**. Las instancias donde el modelo muestra la mayor diferencia de confianza entre palabras masculinas y femeninas son las más informativas para el proceso correctivo.

---

## Diagnóstico previo: medición del sesgo

Antes de describir las intervenciones, el paper mide cuantitativamente el sesgo de género existente en `bert-base-uncased`. Se enmascaran palabras de género (pronombres como *he/she*, nombres de género como *boy/girl*, auxiliares con connotación de género como *Will/May*) y se mide la **diferencia de confianza** del modelo al predecir la versión masculina vs. femenina de cada palabra.

La métrica de diferencia total de confianza es:

$$\left| \sum_{i=0}^{N} \bigl(f(x^{(i)}_{\text{female}}) - f(x^{(i)}_{\text{male}})\bigr) \right|$$

donde:
- $$f(x)$$: probabilidad (confianza) que el modelo asigna a la palabra $$x$$ al predecir el token enmascarado.
- $$N$$: número total de tokens de género encontrados en el dataset.
- La suma mide el sesgo acumulado: positivo si el modelo favorece sistemáticamente las formas femeninas, negativo si favorece las masculinas, grande en valor absoluto si hay sesgo fuerte.

Resultados sobre StereoSet:

| Par de palabras de género | Diferencia de confianza media | Desv. estándar |
|---|:---:|:---:|
| he / she | 0.317 | 0.288 |
| Will / May | 0.316 | 0.225 |
| boy / girl | 0.219 | 0.218 |

El par *he/she* es el más sesgado: el modelo asigna probabilidades sistemáticamente distintas según el género en los mismos contextos.

---

## Metodología: tres estrategias de intervención de datos

El proceso para cada estrategia es:

1. Dado un conjunto de oraciones de entrenamiento, detectar todas las palabras de género usando una lista de términos de género (pronombres, nombres con connotación de género, sustantivos relacionados con roles de género).
2. Reemplazar esas palabras según la estrategia elegida.
3. Hacer fine-tuning de `bert-base-uncased` con MLM loss sobre las oraciones modificadas, enmascarando *solo* las posiciones donde había palabras de género (para que el modelo aprenda específicamente la distribución de género).

Fine-tuning: 30 épocas, lr = 0.001, AdamW, NVIDIA Tesla T4 GPU (~48h total incluyendo todos los experimentos).

### Estrategia 1: naive-masking

Reemplaza **todas** las palabras de género por la palabra fija **"person"**, independientemente del contexto o del género original.

- Ventaja: no requiere ninguna lista de correspondencias; es aplicable sin esfuerzo de ingeniería.
- Lógica: introducir una palabra nueva que no existe en el vocabulario de género del modelo hace que este aprenda a generar el token neutro "person" en contextos donde antes generaba "he" o "she".
- Limitación: las oraciones resultantes pueden sonar artificiales ("person went to person's office"), y "person" es semanticamente muy diferente de los pronombres originales.

| Palabra original | Reemplazo |
|---|---|
| he | person |
| she | person |
| boy | person |

### Estrategia 2: neutral-masking

Usa una **lista de pares de equivalencias** que mapea cada palabra de género a su equivalente neutro en género.

- Ventaja: más semánticamente apropiado que naive-masking; las oraciones resultantes son más naturales.
- Lógica: el modelo aprende a generar el equivalente neutro en contextos donde antes elegiría un término marcado por género.

| Palabra original | Reemplazo |
|---|---|
| he | they |
| her | their |
| schoolgirl | schoolkid |

### Estrategia 3: random-phrase-masking

Reemplaza cada palabra de género por una **frase que incluye ambos géneros**, seleccionando el orden (masculino-primero vs. femenino-primero) al azar con igual probabilidad.

- Ventaja: introduce explícitamente la paridad de ambos géneros en el mismo texto; el modelo aprende a balancear la confianza entre los dos géneros porque los ve aparecer con igual frecuencia en la misma posición.
- Lógica: al ver "he or she", "she and he", "either girl or boy" con igual frecuencia, el modelo aprende que cualquier género es igualmente probable.

| Palabra original | Posibles reemplazos |
|---|---|
| he | "he or she" / "she or he" (aleatorio) |
| she | "she and he" / "he and she" (aleatorio) |
| boy | "either girl or boy" / "either boy or girl" (aleatorio) |

---

## Selección de ejemplos: minar los ejemplos más sesgados

Una segunda contribución es el método de selección de los $$k$$ ejemplos de entrenamiento a incluir (10, 50 o 100). En lugar de selección aleatoria, se usa **el propio modelo sesgado para encontrar las instancias donde más diferencia hay entre géneros** (mayor diferencia de confianza). La hipótesis: los ejemplos donde el sesgo es más pronunciado son más informativos para corregirlo.

El paper compara:
- **most-biased sampling**: seleccionar los $$k$$ ejemplos con mayor diferencia de confianza entre géneros.
- **random sampling**: seleccionar $$k$$ ejemplos al azar.

El muestreo de los más sesgados supera consistentemente al aleatorio, validando la hipótesis.

---

## Datasets utilizados

### Datasets de fine-tuning

**WikiText-2** (Merity et al., 2017): corpus de artículos de Wikipedia en inglés. ~2 millones de tokens, 600 artículos de entrenamiento. Contiene sesgo de género *implícito* — no está diseñado para medir sesgo sino que lo refleja naturalmente en la distribución del texto. Licencia Creative Commons Attribution-ShareAlike.

**StereoSet (dev set)** (Nadeem et al., 2021): 2.123 muestras totales, de las cuales se usan 800 muestras no-estereotipadas. Contiene sesgo de género *explícito* — está diseñado para capturar asociaciones estereotípicas.

Con 10 ejemplos de WikiText-2, se afectan en promedio 191 palabras de género por muestra; con 10 de StereoSet, 55. La mayor densidad de palabras de género en WikiText hace que el debiasing sea más eficiente por muestra.

### Datasets de evaluación

**StereoSet** (Nadeem et al., 2021): evaluación principal de sesgo. Los modelos deben elegir entre tres completaciones: estereotipada, anti-estereotipada, y sin sentido. Las métricas son:
- **SS (Stereotype Score)**: porcentaje de veces que el modelo prefiere la opción estereotipada sobre la anti-estereotipada; ideal = 50.
- **LMS (Language Model Score)**: porcentaje de veces que el modelo elige una opción con sentido (estereotipada o anti-estereotipada) sobre el sin sentido; ideal = 100.
- **ICAT Score**: combina ambas: $$\text{ICAT} = \text{LMS} \cdot \frac{\min(\text{SS}, 100-\text{SS})}{50}$$; ideal = 100.

**CrowS-Pairs** (Nangia et al., 2020): 1.508 pares de oraciones mínimamente diferentes. Una oración estereotipa a un grupo demográfico y la otra no. El bias score es la probabilidad de preferir la opción estereotipada; ideal = 50.

---

## Resultados principales

**Tabla de resultados en WikiText-2 (100 muestras de fine-tuning):**

| Método | SS ↓ | LMS ↑ | ICAT ↑ | CrowS-Pairs ↓ |
|---|:---:|:---:|:---:|:---:|
| Sin debiasing (baseline) | 60.28 | 84.17 | 70.30 | 57.25 |
| CDA | 60.02 | 83.47 | 70.89 | 56.11 |
| Dropout | 60.53 | 83.81 | 70.17 | 55.98 |
| SentenceDebias | 59.22 | 84.17 | **71.31** | 53.82 |
| INLP | 58.21 | 83.39 | 70.97 | 55.73 |
| **random-phrase-masking (10)** | 59.44 | 80.31 | 70.41 | 54.58 |
| **random-phrase-masking (100)** | **58.04** | 78.68 | 69.95 | 54.46 |
| **neutral-masking (10)** | 60.34 | 83.96 | 72.55 | 55.54 |
| **neutral-masking (100)** | 60.81 | 83.59 | 72.21 | 56.49 |

**Hallazgos clave:**

- `random-phrase-masking` logra el **SS más bajo** (58.04) de todos los métodos evaluados, superando incluso a INLP que usa un algoritmo de proyección iterativa.
- Sin embargo, `random-phrase-masking` tiene **LMS más bajo** (~78-80 vs. ~83-84) — las frases "he or she" crean texto artificial que degrada la coherencia del modelo.
- `neutral-masking` tiene **mejor ICAT** (72.55) que todos los baselines con solo 10 ejemplos, preservando mejor la calidad del lenguaje.
- Los resultados con 10 muestras son competitivos con 100 muestras, confirmando la eficacia del enfoque few-shot.

**Mejor configuración (ablación sobre StereoSet, 100 muestras):**

La estrategia `fixed-phrase-3` ("X or Y" con orden fijo) logra el SS más bajo en StereoSet (56.96) en las ablaciones exhaustivas, mejor que random-phrase-masking. `naive-masking` logra el mejor score en CrowS-Pairs (50.64) pero a costa de perplexidad = 1.0 (el modelo colapsa lingüísticamente).

---

## Ejemplo ilustrativo

**Antes del debiasing** (bert-base-uncased original):

Input: `[MASK] is very good at cooking but not great at [MASK] work.`
Predicción: *"She is very good at cooking but not great at her work."*
→ El modelo asocia habilidades de cocina con el género femenino.

Input: `Being a [MASK] is not easy since [MASK] will have to stay home and take care of [MASK] child.`
Predicción: *"Being a mother is not easy since she will have to stay home..."*
→ Roles de cuidado asignados automáticamente a la mujer.

**Después del debiasing** (random-phrase-masking, 10 muestras de StereoSet):

- Primera oración → *"He is very good at cooking but not great at farm work."*
- Segunda oración → *"Being a father is not easy since one will have to stay home and take care of the child."*

El modelo ya no asocia sistemáticamente la cocina o el cuidado con el género femenino.

---

## Limitaciones

1. **Dependencia del género necesario semánticamente:** el método no puede aplicarse a oraciones donde el género es información relevante (ej. "She needs to see a gynecologist").
2. **Lista finita de palabras de género:** el wordlist no cubre todos los términos; el lenguaje evoluciona y pueden quedar palabras sin mapear.
3. **Sustitución burda:** reemplazar palabras de género por frases puede producir oraciones semánticamente incorrectas o extrañas; no es apropiado para augmentar datasets completos.
4. **Género binario:** solo considera masculino/femenino; no aborda pronombres no binarios como "ze/hir".
5. **Evaluación limitada:** los benchmarks miden sesgo en completación de oraciones; la reducción de sesgo en tareas downstream no está garantizada.

---

## Ventajas respecto a trabajos anteriores

- **Extremadamente eficiente:** solo 10 ejemplos modificados logran debiasing competitivo con métodos que usan miles de ejemplos (CDA, SentenceDebias, INLP).
- **Sin modelos auxiliares:** MABEL requiere fine-tuning contrastivo con arquitectura adicional; INLP requiere entrenamiento de clasificadores iterativos. Este método solo necesita el modelo base y el MLM loss estándar.
- **Método de muestreo interpretable:** usar el propio modelo para encontrar los ejemplos más sesgados es una contribución independiente con validación empírica.
- **Aplicabilidad práctica:** la simplicidad del método lo hace accesible para equipos sin grandes recursos computacionales.

---

## Trabajos previos relacionados

El paper divide los trabajos previos en dos ejes: análisis de sesgo en modelos preentrenados y métodos de debiasing (algorítmicos vs. basados en datos).

- **Nadeem et al. (2021) — [StereoSet](2021_nadeem_stereoset.html)**: benchmark principal de evaluación; el paper usa StereoSet tanto para medir el sesgo inicial como para hacer fine-tuning en la configuración con sesgo explícito.
- **He et al. (2022) — [MABEL](2022_he_mabel.html)**: método más directamente comparable por combinar augmentación de datos con fine-tuning contrastivo; requiere arquitectura adicional y más datos. Thakur et al. logran resultados competitivos con muchos menos ejemplos.
- **Zmigrod et al. (2019) — Counterfactual Data Augmentation (CDA)**: usa intercambio de género en texto morfológicamente rico para augmentar datos; inspiración directa del enfoque de intervención de datos. Baseline principal en los experimentos.
- **Maudslay et al. (2019) — Name-Based Counterfactual Data Substitution**: reemplaza nombres marcados por género con equivalentes neutros; técnica más cercana a las estrategias del paper.
- **Ravfogel et al. (2020) — INLP (Null It Out)**: proyección iterativa para eliminar información de género del espacio de embeddings; baseline algorítmico más fuerte.
- **Liang et al. (2020) — SentenceDebias**: debiasing del subespacio de género en representaciones de oraciones; baseline algorítmico task-agnostic.
- **Meade et al. (2022) — [An Empirical Survey of Debiasing Techniques](2021_meade_debiasing-survey.html)**: encuesta que motiva la búsqueda de métodos que no dañen las representaciones internas del modelo.
- **Bolukbasi et al. (2016) — Man is to Computer Programmer as Woman is to Homemaker**: trabajo fundacional sobre debiasing de word embeddings mediante substracción de la dirección de género; antecedente histórico del campo.

## Tags

`debiasing` `data-augmentation` `sesgo-de-género` `BERT` `few-shot`
