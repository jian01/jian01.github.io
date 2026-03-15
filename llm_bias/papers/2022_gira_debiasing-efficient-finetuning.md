---
layout: paper
title: "Debiasing Pre-Trained Language Models via Efficient Fine-Tuning"
year: 2022
authors: "Michael Gira, Ruisu Zhang, Kangwook Lee"
published: "LTEDI Workshop, 2022"
tags:
  - "debiasing"
  - "adapters"
  - "PEFT"
  - "fine-tuning-eficiente"
  - "sesgo-de-género"
pdf: "/llm_bias/pdfs/2022_gira_debiasing-efficient-finetuning.pdf"
method_type: "Fine-tuning / data augmentation"
datasets:
  - "StereoSet"
  - "CrowS-Pairs"
  - "WEAT"
  - "SEAT"
  - "GLUE"
measures_general_quality: "Sí"
status:
  - "Leido"
image: "imgs/2022_gira_debiasing-efficient-finetuning.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
---
# Debiasing Pre-Trained Language Models via Efficient Fine-Tuning (2022)

**Autores**: Michael Gira, Ruisu Zhang, Kangwook Lee
**Publicado en**: LTEDI Workshop, 2022
**Tipo de método**: Fine-tuning / data augmentation

---

## Qué hace

Propone desbiasificar modelos de lenguaje pre-entrenados usando métodos de fine-tuning eficientes en parámetros (como adapters), entrenados sobre datos contrafactuales, logrando reducción de sesgo con mínima degradación de rendimiento y mucho menor costo que el fine-tuning completo.


---

## Metodología

El debiasing estándar requiere re-entrenar o fine-tunear el modelo completo sobre datos debiasing, lo que:
- Actualiza todos los parámetros (billones de parámetros en modelos grandes).
- Es computacionalmente costoso.
- Puede causar "olvido catastrófico" de conocimiento general.

**La solución con adapters:**
Los adapters son módulos pequeños (típicamente 1-5% de los parámetros totales) insertados entre las capas del transformer. Durante el fine-tuning de debiasing, **sólo los parámetros de los adapters se actualizan**. Los pesos originales del transformer permanecen congelados.

Los adapters se insertan después de cada capa de atención y FFN, siendo módulos bottleneck: comprimen la representación a una dimensión menor, aplican una transformación no lineal, y la proyectan de vuelta a la dimensión original.

**Datos de entrenamiento:**
Se generan datos contrafactuales usando Counterfactual Data Augmentation (CDA): para cada oración con atributos de género/raza, se crea una versión con los atributos intercambiados. Los adapters se entrenan para producir representaciones similares para ambas versiones.

---

## Datasets utilizados

- **StereoSet**: evaluación principal.
- **CrowS-Pairs**: pares de frases sesgadas/no sesgadas.
- **WEAT**: Word Embedding Association Test para medir sesgo en embeddings.
- **SEAT**: versión a nivel de oración de WEAT.
- **GLUE**: para medir degradación en downstream tasks.

---

## Ejemplo ilustrativo

BERT tiene embeddings que asocian "él" más con profesiones de alto estatus (CEO, ingeniero) y "ella" con profesiones de bajo estatus (asistente, secretaria). El adapter se entrena para que la representación de "El CEO presentó su plan" sea similar a "La CEO presentó su plan" en el espacio de representaciones intermedias. Sólo el adapter (~6M parámetros) se actualiza; los 110M de parámetros de BERT permanecen intactos.

---

## Resultados principales

- Los adapters logran reducción de sesgo similar al fine-tuning completo en StereoSet (SS de 61% a 53%) con sólo el 5% de los parámetros actualizados.
- Degradación en GLUE es menor con adapters (~0.5%) que con fine-tuning completo (~2%).
- El entrenamiento es 4-8x más rápido que fine-tuning completo.
- El adapter entrenado es reutilizable: puede aplicarse a distintas versiones del mismo modelo base.

---

## Ventajas respecto a trabajos anteriores

- Primer trabajo en aplicar PEFT (Parameter-Efficient Fine-Tuning) específicamente para debiasing.
- La eficiencia computacional hace el debiasing accesible para modelos grandes.
- Los adapters son modulares: pueden quitarse/ponerse sin afectar el modelo base.

---

## Trabajos previos relacionados

El paper organiza los trabajos relacionados en tres líneas: (1) sesgo en sistemas de ML generales (visión, recomendación), (2) sesgo en NLP a nivel de word embeddings estáticos, y (3) sesgo en LLMs preentrenados junto con técnicas de mitigación. El trabajo se posiciona como el primero en aplicar fine-tuning eficiente en parámetros específicamente para debiasing de LLMs.

- **Nadeem et al. (2021) — [StereoSet](2021_nadeem_stereoset.html)**: benchmark principal usado para evaluar el debiasing; proporciona las métricas LMS, SS e ICAT que permiten medir simultáneamente reducción de sesgo y preservación de capacidades lingüísticas.
- **Nangia et al. (2020) — CrowS-Pairs**: segundo dataset de evaluación utilizado en el paper; pares mínimamente distantes para medir preferencia por oraciones estereotipadas.
- **Zhao et al. (2018) — WinoBias**: fuente de datos de entrenamiento junto con CrowS-Pairs; dataset de resolución de correferencias con sesgos de género en profesiones.
- **Bolukbasi et al. (2016) — Man is to Computer Programmer as Woman is to Homemaker**: trabajo fundacional sobre sesgo en word2vec mediante dirección de género; establece el enfoque de proyección que inspira las técnicas de eliminación de subespacio de sesgo.
- **Sheng et al. (2019) — The Woman Worked as a Babysitter**: demuestra que GPT-2 amplifica estereotipos de género, raza y religión; es la evidencia de sesgo en LLMs que motiva directamente el trabajo.
- **May et al. (2019) — SEAT**: extiende WEAT al nivel de oraciones para medir sesgos en representaciones contextuales; benchmarkde medición de sesgo en embeddings al que el paper hace referencia para contextualizar sus métricas.
- **Ravfogel et al. (2020) — INLP**: técnica de proyección iterativa para eliminar la dirección de género de los embeddings; es el método de debiasing de representaciones más relacionado con la propuesta del paper.
- **Lu et al. (2021) — Frozen Pretrained Transformers**: demuestra que adaptando solo las capas de normalización y embeddings posicionales de GPT-2 se puede transferir a tareas y modalidades completamente distintas; inspiración directa para el enfoque de fine-tuning eficiente del paper.
- **Solaiman y Dennison (2021) — PALMS**: demuestra que el fine-tuning completo de GPT-3 sobre un dataset curado mitiga sesgos; el paper de Gira et al. replica este resultado pero con menos del 1% de los parámetros actualizados.
- **Meade et al. (2022) — [An Empirical Survey of Debiasing Techniques](2021_meade_debiasing-survey.html)**: survey que proporciona el marco comparativo de las técnicas de debiasing evaluadas; las conclusiones de este survey motivan la búsqueda de métodos más eficientes.

## Tags

`debiasing` `adapters` `PEFT` `fine-tuning-eficiente` `sesgo-de-género`
