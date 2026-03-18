---
layout: paper
title: "BiasEdit: Debiasing Stereotyped Language Models via Model Editing"
year: 2025
date_published: "2025-03-11"
authors: "Xin Xu, Wei Xu, Ningyu Zhang, Julian McAuley"
published: "arXiv, 2025"
tags:
  - "debiasing"
  - "edición-de-modelos"
  - "ROME"
  - "FFN-layers"
  - "sesgo-de-género"
pdf: "/llm_bias/pdfs/2025_xu_biasedit.pdf"
method_type: "Edición de pesos / neuronas"
datasets:
  - "StereoSet"
  - "WinoBias"
  - "BBQ"
  - "CrowS-Pairs"
  - "GLUE"
  - "MMLU"
measures_general_quality: "Sí"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2025_xu_biasedit.png"
image_caption: "Gráfico de barras que muestra la diferencia absoluta de log-probabilidad (efecto del sesgo de género) por capa del modelo GPT-2 Medium, comparando el efecto de las palabras de atributo de sesgo (azul), el token previo a los términos de atributo (rojo) y los propios términos de atributo (verde)."
opinion: "<WIP>"
---

## Qué hace

Aplica técnicas de **edición de modelos** (model editing) para eliminar estereotipos de género y raza de LLMs. En lugar de re-entrenar el modelo, modifica quirúrgicamente las capas FFN específicas que almacenan las asociaciones estereotipadas.


---

## Metodología

Model editing (técnicas como ROME/MEMIT) permite modificar hechos específicos en LLMs sin afectar el conocimiento general. BiasEdit adapta estas técnicas para el debiasing:

**Identificación de asociaciones sesgadas:**
Se formulan los estereotipos como "hechos" a editar. Por ejemplo: el modelo tiene la "creencia" interna de que "un médico" → "hombre". En el marco de ROME, esto se representa como: subject="médico", relation="tiene género", object="hombre". Se quiere cambiar object de "hombre" a una distribución uniforme entre géneros.

**Localización con causal tracing:**
ROME usa causal tracing (activation patching) para identificar qué capa FFN específica del transformer almacena la asociación. Para cada estereotipo, se identifica la capa (generalmente en el rango de capas medias, 8-20 en GPT-2 Large) donde la asociación es almacenada.

**Edición quirúrgica:**
Se modifican directamente los valores en las matrices de peso de la capa FFN identificada usando optimización rank-one. Sólo se modifican los parámetros de esa capa específica, dejando el resto del modelo intacto.

**Objetivo de debiasing:**
El nuevo "hecho" que se inserta es contrafactual: se enseña al modelo que "médico" se asocia igualmente con géneros masculino y femenino, añadiendo ambas asociaciones.

---

## Datasets utilizados

- **StereoSet**: evaluación principal de sesgo.
- **WinoBias**: sesgos de género en resolución de correferencias.
- **BBQ**: preguntas con contexto ambiguo.
- **CrowS-Pairs**: pares de frases con/sin estereotipo.
- **GLUE/MMLU**: evaluación de retención de capacidades generales.

---

## Ejemplo ilustrativo

El modelo GPT-J tiene el estereotipo: cuando se le da el contexto "La persona que realizó la cirugía era...", asigna mayor probabilidad a "un hombre" que a "una mujer". BiasEdit:
1. Identifica mediante causal tracing que este estereotipo está almacenado principalmente en la capa FFN 14.
2. Modifica los pesos de esa capa para que asigne probabilidades iguales a "un hombre" y "una mujer".
3. El resto del modelo (conocimiento de medicina, cirugía, etc.) permanece intacto.

---

## Resultados principales

- Reduce el stereotyping score en StereoSet de 62% a 51% (50% es ideal) con menos del 1% de degradación en GLUE.
- Más preciso que métodos de fine-tuning (CDA, MABEL): menor degradación en capacidades generales.
- Cada edición es rápida: segundos por estereotipo vs. horas de fine-tuning.
- Escalable: puede editar cientos de estereotipos de forma independiente.

---

## Ventajas respecto a trabajos anteriores

- Aplica por primera vez técnicas de edición de modelos específicamente para debiasing.
- La modificación quirúrgica preserva mejor el conocimiento general que el fine-tuning.
- La velocidad permite iterar sobre muchos estereotipos específicos de forma práctica.

---

## Trabajos previos relacionados

Los trabajos previos se organizan en dos grandes líneas: (1) métodos de debiasing existentes (fine-tuning, proyección de representaciones, prompting) que BiasEdit pretende superar, y (2) técnicas de edición de modelos de las que BiasEdit toma su metodología central.

- **Meng et al. (2022, 2023) — ROME / MEMIT**: técnicas de edición de conocimiento que localizan hechos en capas MLP específicas del transformer y los modifican con rank-one updates; BiasEdit adapta directamente esta metodología para formular los estereotipos como "hechos" a editar.
- **Mitchell et al. (2022) — MEND**: emplea hiper-redes para predecir actualizaciones de parámetros en edición de modelos; BiasEdit adopta la arquitectura de editor como hiper-red para generar los shifts de parámetros de debiasing.
- **Nadeem et al. (2021) — [StereoSet](2021_nadeem_stereoset.html)**: benchmark principal de evaluación usado en BiasEdit; proporciona el Stereotype Score (SS) y Language Modeling Score (LMS) para cuantificar sesgo y preservación de capacidades.
- **Nangia et al. (2020) — CrowS-Pairs**: segundo benchmark de evaluación de sesgo usado en BiasEdit para validar los resultados en un dataset independiente.
- **Meade et al. (2022) — [An Empirical Survey of Debiasing Techniques](2021_meade_debiasing-survey.html)**: survey que establece la línea base comparativa de métodos (CDA, SentenceDebias, INLP, Self-Debias) contra los que BiasEdit se compara; también proporciona el código público bias-bench usado para la evaluación.
- **Ravfogel et al. (2020) — INLP**: uno de los baselines de comparación directa; proyecta representaciones para eliminar la dirección de género, pero sin modificar los parámetros del modelo.
- **Liang et al. (2020) — SentenceDebias**: otro baseline; extiende Hard-Debias a representaciones de oraciones, pero tampoco modifica parámetros internos y no puede aplicarse en downstream tasks.
- **Schick et al. (2021) — Self-Debias**: baseline de prompting que usa el propio modelo para reducir sesgos en la distribución de generación sin modificar pesos; comparado directamente en la Tabla 1.
- **Zmigrod et al. (2019) / Barikeri et al. (2021) — CDA**: fine-tuning completo con datos contrafactuales; costoso y solo aplicable a modelos pequeños como GPT-2.
- **Smith et al. (2022) — [Holistic Bias](2022_smith_holistic-descriptor.html)**: trabajo citado como ejemplo de la persistencia y amplitud de los sesgos en LLMs, motivando la necesidad de métodos de edición quirúrgica como BiasEdit.

## Tags

`debiasing` `edición-de-modelos` `ROME` `FFN-layers` `sesgo-de-género`
