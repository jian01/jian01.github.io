---
layout: paper
title: "KnowBias: Mitigating Social Bias in LLMs via Know-Bias Neuron Enhancement"
year: 2026
date_published: "2026-01-29"
authors: "J. J. Pan, Chahat Raj, Anjishnu Mukherjee, Sina Mansouri, Bowen Wei, Shloka Yada, Ziwei Zhu"
published: "arXiv, 2026"
tags:
  - "debiasing"
  - "neuronas-equitativas"
  - "FFN-layers"
  - "amplificación"
  - "interpretabilidad"
pdf: "/llm_bias/pdfs/2026_pan_knowbias.pdf"
method_type: "Edición de pesos / neuronas"
datasets:
  - "StereoSet"
  - "BBQ"
  - "WinoBias"
  - "CrowS-Pairs"
measures_general_quality: "Sí"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2026_pan_knowbias.png"
image_caption: "Diagrama ilustrativo del método KnowBias: (a) el LLM exhibe sesgo racial al responder una pregunta, con neuronas de sesgo en rojo; (b) el modelo reconoce el sesgo activando neuronas conoce-sesgo en verde; (c) al amplificar dichas neuronas, el modelo produce una respuesta imparcial."
opinion: "<WIP>"
---
# KnowBias: Mitigating Social Bias in LLMs via Know-Bias Neuron Enhancement (2026)

**Autores**: J. J. Pan, Chahat Raj, Anjishnu Mukherjee, Sina Mansouri, Bowen Wei, Shloka Yada, Ziwei Zhu
**Publicado en**: arXiv, 2026
**Tipo de método**: Edición de pesos / neuronas

---

## Qué hace

Propone KnowBias, un método de debiasing que identifica "neuronas conoce-sesgo" — neuronas en las capas FFN que, cuando se activan, producen respuestas más equitativas — y las **amplifica** en lugar de suprimir neuronas sesgadas. Enfoque opuesto al de Yang et al. (2023).


---

## Metodología

**La distinción conceptual clave:**
Trabajos anteriores (Yang et al.) identifican neuronas que *causan* sesgo y las eliminan. KnowBias busca neuronas que *previenen* el sesgo (las "conoce-sesgo") y las potencia. La lógica: el modelo ya tiene mecanismos internos de equidad — simplemente están siendo suprimidos por otros.

**Identificación de neuronas conoce-sesgo:**
1. Se seleccionan pares de oraciones con diferentes géneros/razas sobre el mismo contexto.
2. Para cada neurona FFN, se mide si su activación es consistentemente mayor cuando el modelo genera respuestas más equitativas (que asignan probabilidades similares a ambos grupos).
3. Las neuronas con mayor correlación entre alta activación y respuestas equitativas son las "conoce-sesgo".

**Amplificación:**
En lugar de poner en cero neuronas sesgadas, se multiplican los pesos de las neuronas conoce-sesgo por un factor > 1 (ej. 1.5-2x). Esto amplifica su influencia en el output del modelo.

Sólo se modifican las **matrices de peso FFN** en las capas donde se encuentran las neuronas conoce-sesgo — una modificación quirúrgica de muy pocos parámetros.

---

## Datasets utilizados

- **StereoSet**: evaluación principal.
- **BBQ**: preguntas con contexto ambiguo.
- **WinoBias**: correferencias de género.
- **CrowS-Pairs**: pares sesgados.
- **Downstream tasks**: GLUE para medir retención de capacidades.

---

## Ejemplo ilustrativo

Cuando el modelo procesa "La persona que lideró el equipo de ingeniería era muy competente" (neutro en género), las neuronas conoce-sesgo de la capa FFN-15 se activan fuertemente. Estas neuronas contribuyen a que el modelo genere el pronombre de forma neutra o balanceada. KnowBias amplifica estas neuronas × 1.8, haciendo que su influencia "neutral" sea más fuerte que la de las neuronas que tirarían hacia un género específico.

---

## Resultados principales

- KnowBias reduce el bias score en StereoSet de 63% a 51% (50% es ideal) en Llama-2-7B.
- La degradación en GLUE es menor al 1% — comparable a los mejores métodos de debiasing.
- La amplificación de neuronas conoce-sesgo es complementaria a la eliminación de neuronas sesgadas: combinarlos produce mejores resultados.
- Las neuronas conoce-sesgo representan ~0.3% de todas las neuronas — son raras pero muy influyentes.

---

## Ventajas respecto a trabajos anteriores

- Perspectiva novedosa: amplificar lo bueno en lugar de suprimir lo malo.
- Las neuronas conoce-sesgo son una nueva clase de componentes del transformer con rol funcional específico.
- La modificación es mínima y quirúrgica: pocos pesos cambian.

---

## Trabajos previos relacionados

El apéndice organiza los trabajos previos en dos bloques: métodos de mitigación de sesgo social en LLMs (categorías: prompts, fine-tuning, edición, steering, intervención en neuronas) e identificación de neuronas de conocimiento.

- **Gallegos et al. (2025) — Self-debiasing large language models**: método de steering por prompts de contexto sin modificar parámetros, contrastado con KnowBias en la categoría de métodos de prompt-based; ver [2024_gallegos_self-debiasing.md](2024_gallegos_self-debiasing.html).
- **Yang et al. (2023) — Bias neurons in transformers**: identifica y suprime neuronas asociadas al sesgo, antecedente directo del concepto de "know-bias neurons" de KnowBias que en cambio amplifica en lugar de suprimir; ver [2023_yang_bias-neurons.md](2023_yang_bias-neurons.html).
- **Xu et al. (2025) — BiasEdit: Debiasing stereotyped language models via model editing**: método de edición paramétrica para debiasing, comparado como alternativa de edición frente al enfoque de amplificación de KnowBias; ver [2025_xu_biasedit.md](2025_xu_biasedit.html).
- **Li et al. (2025) — FairSteer**: método de activation steering con clasificador lineal para detección y corrección de activaciones sesgadas, comparado en la categoría de métodos de steering; ver [2025_li_fairsteer.md](2025_li_fairsteer.html).
- **Nadeem et al. (2021) — StereoSet: Measuring stereotypical bias in pretrained language models**: benchmark de sesgo estereotipado utilizado como uno de los datasets de evaluación principales de KnowBias; ver [2021_nadeem_stereoset.md](2021_nadeem_stereoset.html).
- **Parrish et al. (2021) — BBQ: A hand-built bias benchmark for question answering**: benchmark de sesgo en QA empleado para evaluar KnowBias en ambiguedad y desambiguación de contextos sesgados; ver [2021_parrish_bbq.md](2021_parrish_bbq.html).
- **Wang et al. (2022) — Finding skill neurons in pre-trained transformer-based LMs**: localización de neuronas de habilidad en FFN de transformers, base metodológica para la identificación de know-bias neurons; ver [2022_wang_skill-neurons.md](2022_wang_skill-neurons.html).
- **Cheng et al. (2025) — BiasFilter**: método de debiasing mediante recompensa implícita en inferencia, incluido en la categoría de fine-tuning/alignment y contrastado con KnowBias en tiempo de inferencia; ver [2025_cheng_biasfilter.md](2025_cheng_biasfilter.html).
- **Meade et al. (2021) — An empirical survey of debiasing techniques**: encuesta que clasifica los enfoques de debiasing, marco de referencia para la taxonomía de cuatro paradigmas del apéndice A.1; ver [2021_meade_debiasing-survey.md](2021_meade_debiasing-survey.html).
- **Zhao et al. (2025) — Debiasing with PEFT**: método PEFT para clasificación fina, representante del paradigma de fine-tuning comparado con la amplificación de neuronas de KnowBias; ver [2025_zhao_debiasing-peft.md](2025_zhao_debiasing-peft.html).

## Tags

`debiasing` `neuronas-equitativas` `FFN-layers` `amplificación` `interpretabilidad`
