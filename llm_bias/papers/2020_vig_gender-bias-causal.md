---
layout: paper
title: "Investigating Gender Bias in Language Models Using Causal Mediation Analysis"
year: 2020
date_published: "2020-04-26"
authors: "Jesse Vig, Sebastian Gehrmann, Yonatan Belinkov, Sharon Qian, Daniel Nevo, Yaron Singer, Stuart Shieber"
published: "NeurIPS, 2020"
tags:
  - "interpretabilidad"
  - "sesgo-de-género"
  - "causal-mediation"
  - "attention-heads"
  - "GPT-2"
pdf: "/llm_bias/pdfs/2020_vig_gender-bias-causal.pdf"
status:
  - "Pendiente"
image: "imgs/2020_vig_gender-bias-causal.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---

## Qué hace

Usa **análisis de mediación causal** para identificar qué componentes específicos del transformer (cabezas de atención, neuronas FFN) son causalmente responsables del sesgo de género en modelos de lenguaje como GPT-2.


---

## Metodología

El análisis de mediación causal es una técnica estadística que permite aislar el efecto de intervenir en un componente específico de la red.

**El setup del experimento:**
Se crean pares de oraciones que difieren sólo en el género: "The doctor said that she..." vs. "The doctor said that he...". Se mide la diferencia en las probabilidades de la siguiente palabra (¿el modelo asocia más "doctor" con un género que con otro?).

**Mediación causal:**
Para identificar qué componentes del transformer median este efecto de género, se hace lo siguiente:
1. **Efecto total**: se mide la diferencia de activación entre las dos versiones de la oración a la salida del modelo.
2. **Indirect effect a través de un componente X**: se "parcha" (patch) el componente X (ej. la cabeza de atención 3-5) con los valores que tendría para la versión masculina de la oración, pero manteniendo todo lo demás de la versión femenina. Si el output cambia al valor de la versión masculina, entonces X media el efecto de género.
3. Se computa esto para todas las cabezas de atención y neuronas FFN.

Las cabezas de atención y FFN no se modifican permanentemente — el patching es sólo para medir causalidad, no para desbiasificar.

---

## Datasets utilizados

- **WinoBias**: frases con profesiones de alta y baja representación femenina.
- **Winogender**: frases con pronombres de género en contextos ocupacionales.
- Templates propios: pares mínimos "The [PROFESSION] said that [he/she]..."
- Modelos evaluados: GPT-2 (small, medium, large, XL), BERT, DistilBERT.

---

## Ejemplo ilustrativo

Oración: "El médico dijo que **ella** vendría mañana."

El análisis de mediación revela que la cabeza de atención 9-6 (capa 9, cabeza 6) de GPT-2 es la que más media el efecto de género: cuando se parcha esta cabeza con los valores de la versión masculina, la probabilidad de "médico" referido a un hombre sube drásticamente. Esto identifica 9-6 como una "cabeza de género" — responsable de transferir información de género entre tokens.

---

## Resultados principales

- El sesgo de género está mediado principalmente por 3-5 cabezas de atención específicas en las capas medias del transformer.
- Las capas FFN también median parte del efecto, pero en menor medida que las cabezas de atención.
- Los modelos más grandes tienen más cabezas que median el sesgo, pero el efecto por cabeza es más distribuido.
- Identifica que el sesgo no está en los embeddings iniciales sino en cómo la atención propaga información de género a través de las capas.

---

## Ventajas respecto a trabajos anteriores

- Primer uso de análisis de mediación causal para localizar sesgo en transformers.
- Proporciona evidencia causal (no sólo correlacional) de qué componentes causan el sesgo.
- Metodología aplicable a cualquier tipo de sesgo o comportamiento en cualquier modelo de transformer.

---

## Trabajos previos relacionados

El paper organiza los trabajos previos en dos ejes principales: (1) métodos de análisis estructural y conductual de modelos de NLP, y (2) trabajos sobre sesgo de género y desbiasificación.

- **Bolukbasi et al. (2016) — Man is to Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings**: trabajo fundacional que identificó y mitigó sesgos de género en word embeddings estáticos, precursor directo del análisis de sesgo en representaciones contextualizadas.
- **Radford et al. (2019) — Language Models are Unsupervised Multitask Learners (GPT-2)**: introduce GPT-2, el modelo principal sobre el que se aplica el análisis de mediación causal de este paper.
- **Zhao et al. (2018) — Gender Bias in Coreference Resolution: Evaluation and Debiasing Methods (WinoBias)**: propone el dataset WinoBias, uno de los tres conjuntos de datos usados en los experimentos de este paper para medir sesgo de género.
- **Rudinger et al. (2018) — Gender Bias in Coreference Resolution (Winogender)**: introduce el dataset Winogender, también utilizado directamente en los experimentos de atención.
- **Pearl (2001) — Direct and Indirect Effects**: la base teórica del análisis de mediación causal, de cuyo formalismo (efectos directos e indirectos naturales) depende toda la metodología propuesta.
- **Belinkov & Glass (2019) — Analysis Methods in Neural NLP**: revisión de métodos de análisis en NLP que motiva la necesidad de combinar análisis estructural y conductual, limitación que este paper aborda.
- **Conneau et al. (2018) — What you can cram into a single vector: Probing sentence embeddings**: ejemplo representativo del paradigma de probing classifiers que este paper critica por no ser causal.
- **Elhage et al. (2021) — A Mathematical Framework for Transformer Circuits**: aunque posterior, el framework de residual stream de Elhage es conceptualmente afín; Vig et al. pueden considerarse precursores de esta corriente.
- **Caliskan et al. (2017) — Semantics derived automatically from language corpora contain human-like biases**: documenta sesgos implícitos en corpora de texto que los modelos absorben, motivando el estudio del sesgo de género en LLMs.

## Tags

`interpretabilidad` `sesgo-de-género` `causal-mediation` `attention-heads` `GPT-2`
