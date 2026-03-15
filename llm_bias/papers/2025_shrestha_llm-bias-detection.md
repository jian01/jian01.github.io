---
layout: paper
title: "LLM Bias Detection and Mitigation through the Lens of Desired Distributions"
year: 2025
authors: "Ingroj Shrestha, Padmini Srinivasan"
published: "EMNLP, 2025"
tags:
  - "debiasing"
  - "distribuciones"
  - "KL-divergence"
  - "fairness"
  - "detección-sesgo"
pdf: "/llm_bias/pdfs/2025_shrestha_llm-bias-detection.pdf"
method_type: "Fine-tuning / data augmentation"
datasets:
  - "WinoBias"
  - "StereoSet"
  - "BBQ"
measures_general_quality: "No"
status:
  - "Pendiente"
image: "imgs/2025_shrestha_llm-bias-detection.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---
# LLM Bias Detection and Mitigation through the Lens of Desired Distributions (2025)

**Autores**: Ingroj Shrestha, Padmini Srinivasan
**Publicado en**: EMNLP, 2025
**Tipo de método**: Fine-tuning / data augmentation

---

## Qué hace

Propone un framework de detección y mitigación de sesgo que enmarca el problema como una diferencia entre la distribución de outputs del modelo y una "distribución deseada" justa. Detecta sesgo midiendo KL-divergence y lo mitiga con una regularización que acerca las distribuciones.


---

## Metodología

**La perspectiva distribucional:**
La mayoría de métodos de debiasing trabajan a nivel de ejemplos individuales (¿este output es sesgado?). Este paper propone trabajar a nivel de distribuciones: la distribución del modelo sobre respuestas a preguntas sobre el grupo A debería ser similar a la distribución sobre respuestas sobre el grupo B.

**Detección:**
Para detectar sesgo en dimensión X (ej. género):
1. Se generan N respuestas del modelo a prompts sobre el grupo A (ej. mujeres en posiciones de liderazgo).
2. Se generan N respuestas a los mismos prompts sobre el grupo B (ej. hombres en posiciones de liderazgo).
3. Se mide la KL-divergence entre las dos distribuciones de respuestas (sobre atributos como sentimiento, temas, roles mencionados).
4. Si la KL-divergence es alta, hay sesgo.

**Mitigación:**
Se añade un término de regularización durante el fine-tuning que minimiza la KL-divergence entre la distribución del modelo sobre el grupo A y la distribución "deseada" (equidad = distribuciones iguales entre grupos). Las capas del transformer se actualizan con este objetivo combinado (task loss + KL fairness term).

---

## Datasets utilizados

- **WinoBias**: evaluación de sesgo de género en ocupaciones.
- **StereoSet**: sesgo general.
- **BBQ**: múltiples dimensiones demográficas.
- Datos de fine-tuning: pares de oraciones sobre diferentes grupos demográficos.
- Evaluado en BERT, RoBERTa, y GPT-2.

---

## Ejemplo ilustrativo

Se mide la distribución de sentimiento en respuestas del modelo a "Las enfermeras son..." vs "Los enfermeros son...". Si la distribución de sentimiento para "enfermeras" concentra palabras como "cuidadosas", "amables", "pacientes" mientras que "enfermeros" concentra "innovadores", "eficientes", "técnicos" — hay sesgo. La KL-divergence entre estas distribuciones cuantifica el sesgo. La regularización entrena al modelo para que ambas distribuciones se asemejen más.

---

## Resultados principales

- La detección basada en KL-divergence correlaciona mejor con evaluaciones humanas de sesgo que métodos basados en scores de tokens individuales.
- La mitigación con regularización KL reduce el sesgo en BBQ en un 18% con <2% degradación en downstream tasks.
- El framework unifica detección y mitigación en un pipeline coherente.
- La "distribución deseada" puede configurarse según distintos conceptos de fairness (equidad demográfica, equidad de oportunidad, etc.).

---

## Ventajas respecto a trabajos anteriores

- El enfoque distribucional es más robusto que métodos basados en ejemplos individuales.
- La KL-divergence como métrica de sesgo es más principled que scores ad-hoc.
- La flexibilidad en definir la "distribución deseada" permite adaptar el método a diferentes conceptos de fairness.

---

## Trabajos previos relacionados

El artículo organiza los trabajos previos en dos perspectivas: métodos de cuantificación de sesgo (igualdad de asociaciones, métricas de disparidad demográfica) y técnicas de mitigación en-procesamiento (modificación de arquitectura, restricción de parámetros, modificación de la función de pérdida).

- **Meade et al. (2021) — An empirical survey of debiasing techniques**: encuesta de referencia que proporciona el marco para categorizar los métodos de mitigación frente a los que se contrasta la propuesta de pérdida KL adaptativa; ver [2021_meade_debiasing-survey.md](2021_meade_debiasing-survey.html).
- **Nadeem et al. (2021) — StereoSet: Measuring stereotypical bias in pretrained language models**: benchmark de referencia para medir sesgo estereotipado, mencionado como método de evaluación base en el contexto de métodos de embedding estático; ver [2021_nadeem_stereoset.md](2021_nadeem_stereoset.html).
- **Gallegos et al. (2024) — Self-debiasing large language models**: método de zero-shot debiasing comparado como alternativa sin modificar parámetros; ver [2024_gallegos_self-debiasing.md](2024_gallegos_self-debiasing.html).
- **Gira et al. (2022) — Debiasing pre-trained language models via efficient fine-tuning**: método PEFT de debiasing por restricción de parámetros específicos (capas de atención, adaptadores), comparado en la categoría de mitigación en-procesamiento; ver [2022_gira_debiasing-efficient-finetuning.md](2022_gira_debiasing-efficient-finetuning.html).
- **Yang et al. (2023) — Bias neurons in transformers**: poda de neuronas de sesgo, ejemplo del enfoque de restricción de parámetros discutido en la sección de trabajos previos de mitigación; ver [2023_yang_bias-neurons.md](2023_yang_bias-neurons.html).
- **Xu et al. (2025) — BiasEdit: Debiasing stereotyped language models via model editing**: uso de adaptadores y edición de modelos para debiasing paramétrico, antecedente directo del enfoque de modificación de arquitectura evaluado en el artículo; ver [2025_xu_biasedit.md](2025_xu_biasedit.html).
- **He et al. (2022) — MABEL: Attenuating gender bias using textual entailment data**: método de fine-tuning contrastivo para sesgo de género con restricción de parámetros, referente del paradigma de mitigación con datos de entailment; ver [2022_he_mabel.md](2022_he_mabel.html).

## Tags

`debiasing` `distribuciones` `KL-divergence` `fairness` `detección-sesgo`
