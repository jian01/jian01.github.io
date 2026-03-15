---
layout: paper
title: "ToxiGen: A Large-Scale Machine-Generated Dataset for Adversarial and Implicit Hate Speech Detection"
year: 2022
authors: "Thomas Hartvigsen, Saadia Gabriel, Hamid Palangi, Maarten Sap, Dipankar Ray, Ece Kamar"
published: "ACL, 2022"
tags:
  - "dataset"
  - "hate-speech-implícito"
  - "adversarial"
  - "GPT-3"
  - "detección-toxicidad"
pdf: "/llm_bias/pdfs/2022_hartvigsen_toxigen.pdf"
method_type: "Benchmark / Dataset"
datasets:
  - "ToxiGen"
status:
  - "Leido"
image: "imgs/2022_hartvigsen_toxigen.png"
image_caption: "Logo de Delphi, el sistema de razonamiento moral de Allen AI mencionado como referencia en el contexto de detección de toxicidad implícita."
---
# ToxiGen: A Large-Scale Machine-Generated Dataset for Adversarial and Implicit Hate Speech Detection (2022)

**Autores**: Thomas Hartvigsen, Saadia Gabriel, Hamid Palangi, Maarten Sap, Dipankar Ray, Ece Kamar
**Publicado en**: ACL, 2022
**Tipo de método**: Benchmark / Dataset

---

## Qué hace

Crea ToxiGen, un dataset de 274.186 frases sobre 13 grupos minoritarios que enfoca específicamente el **odio implícito** (sin insultos explícitos ni lenguaje de odio obvio). Usa un proceso adversarial con GPT-3 para generar frases que engañen a los clasificadores de odio existentes.


---

## Metodología

El problema con los datasets de hate speech existentes es que están sesgados hacia odio **explícito** (insultos directos, lenguaje extremo). Los modelos de contenido modernos aprenden a detectar este odio obvio pero fallan con el odio implícito: estereotipos sutiles, insinuaciones, microagresiones.

**El algoritmo ALICE (Adversarial Learning In Classfier's Evasion):**
1. Se prompt-tunea GPT-3 para generar frases que parezcan inofensivas pero contengan estereotipos o implicaciones dañinas sobre un grupo específico.
2. Se evalúa si estas frases engañan a un clasificador de odio existente (HateBERT, Perspective API).
3. Si el clasificador no las detecta como odiosas → se añaden al dataset como ejemplos difíciles.
4. Se itera: se usa el feedback del clasificador para ajustar los prompts y generar frases más difíciles.

**Los 13 grupos:** Personas negras, latinas/os, judías, musulmanas, asiáticas, personas LGBTQ+, mujeres, personas con discapacidad, migrantes, personas gordas, personas mayores, y personas sin hogar.

Cada frase está etiquetada como tóxica o benigna, y el grupo al que se refiere.

---

## Datasets utilizados

- **ToxiGen**: 274.186 frases generadas, ~50% tóxicas / ~50% benignas.
- **Crowdsourcing humano**: subconjunto de 9.000 frases anotadas por humanos para validar calidad.
- Evaluación de modelos: RoBERTa, BERT, HateBERT entrenados y evaluados en ToxiGen.

---

## Ejemplo ilustrativo

Odio explícito (fácil de detectar): *"Los [grupo] son basura."*
Odio implícito (difícil, objetivo de ToxiGen): *"Siempre que hay un problema en el vecindario, resulta que los [grupo] estaban involucrados."* — Esta frase no usa insultos pero insinúa que un grupo es propenso a causar problemas. Los clasificadores estándar fallan en detectarla; ToxiGen existe para entrenar modelos que sí puedan.

---

## Resultados principales

- Los clasificadores entrenados en ToxiGen mejoran en detección de odio implícito: de 30% a 65% accuracy en frases implícitas.
- Los modelos entrenados en ToxiGen generalizan mejor a odio implícito real de redes sociales.
- RoBERTa fine-tuneado en ToxiGen supera a GPT-3 en zero-shot hate speech detection.
- El 40% de las frases tóxicas del dataset engañan a los mejores clasificadores existentes.

---

## Ventajas respecto a trabajos anteriores

- Primer dataset a gran escala enfocado específicamente en odio **implícito**.
- El proceso adversarial ALICE garantiza que las frases sean difíciles para los clasificadores existentes.
- Cubre 13 grupos demográficos, mucho más diverso que datasets anteriores.

---

## Trabajos previos relacionados

ToxiGen se posiciona como alternativa a los datasets de hate speech existentes que sobreindexan en odio explícito y scraping de plataformas sociales. La Sección 2 del paper revisa en detalle los datasets anteriores, mostrando que ToxiGen es el primero a gran escala balanceado entre tóxico/benigno e implícito.

- **Sap et al. (2020) — [Social Bias Frames](2020_sap_social-bias-frames.html)**: dataset de 44.671 posts de redes sociales con anotaciones de sesgo estructuradas; ToxiGen lo compara directamente en la Tabla 1 y lo cita como el dataset de hate speech scrapeado con mayor cobertura implícita antes de ToxiGen.
- **Davidson et al. (2017) — Automated Hate Speech Detection and the Problem of Offensive Language**: uno de los datasets de referencia de 24.802 tweets de Twitter, citado como representante de la metodología de scraping con keyword-based que ToxiGen supera.
- **Vidgen et al. (2021) — DynaHate**: dataset adversarial humano-máquina de 41.134 ejemplos que incluye odio de diversas categorías; el más cercano en espíritu a ToxiGen pero mucho más pequeño y con menos control sobre grupos demográficos.
- **ElSherief et al. (2021) — Implicit Hate Corpus**: 22.584 tweets de Twitter enfocados en odio implícito; antecedente directo de ToxiGen en la tarea de detección de odio implícito pero de menor escala y basado en scraping.
- **Dixon et al. (2018) — Measuring and Mitigating Unintended Bias in Text Classification**: identifica la correlación espuria entre menciones de grupos minoritarios y etiquetas de toxicidad que ToxiGen busca corregir explícitamente con su dataset balanceado.
- **Brown et al. (2020) — GPT-3: Language Models are Few-Shot Learners**: modelo base usado por ToxiGen para generar los 274k ejemplos; su capacidad de few-shot prompting es el núcleo técnico del método ALICE de ToxiGen.
- **Han & Tsvetkov (2020) — Fortifying Toxic Speech Detectors Against Veiled Toxicity**: demuestra que la toxicidad velada (implícita) es un desafío persistente para los clasificadores NLP, motivando directamente la creación de ToxiGen.
- **Röttger et al. (2021) — HateCheck**: benchmark de pruebas funcionales para clasificadores de hate speech que revela sus puntos de fallo, citado como trabajo complementario en la evaluación de detectores de toxicidad.

## Tags

`dataset` `hate-speech-implícito` `adversarial` `GPT-3` `detección-toxicidad`
