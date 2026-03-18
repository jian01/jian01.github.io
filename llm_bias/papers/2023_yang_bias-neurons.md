---
layout: paper
title: "Mitigating Biases for Instruction-following Language Models via Bias Neurons Elimination"
year: 2023
date_published: "2023-11-16"
authors: "Nakyeong Yang, Taegwan Kang, Stanley Jungkyu Choi, Honglak Lee, Kyomin Jung"
published: "ACL, 2023"
tags:
  - "debiasing"
  - "neuronas-de-sesgo"
  - "FFN-layers"
  - "interpretabilidad"
  - "edición-quirúrgica"
pdf: "/llm_bias/pdfs/2023_yang_bias-neurons.pdf"
method_type: "Edición de pesos / neuronas"
datasets:
  - "WinoBias"
  - "StereoSet"
  - "BBQ"
  - "TruthfulQA"
measures_general_quality: "Sí"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2023_yang_bias-neurons.png"
image_caption: "Diagrama de la arquitectura propuesta: (a) visión general del encoder-decoder con el módulo Guidance que conduce al decoder con pérdidas de oración y tipo de error; (b) detalle del decoder guiado, con dos mecanismos de atención cruzada (GCA) y un identificador de género (GID) para corregir el sesgo de forma controlada."
opinion: "<WIP>"
---

## Qué hace

Identifica **neuronas de sesgo** — neuronas individuales en las capas FFN de LLMs de instrucción (como InstructGPT) que son las principales responsables de generar outputs sesgados — y las elimina/neutraliza selectivamente para reducir el sesgo sin afectar otras capacidades.


---

## Metodología

**Identificación de neuronas de sesgo:**
Para cada neurona en las capas FFN del transformer, se mide su "bias score": cuánto difiere su activación promedio cuando el modelo procesa texto sobre el grupo A (ej. hombres) vs. el grupo B (ej. mujeres) para el mismo contexto. Las neuronas con mayor diferencia de activación entre grupos son candidatas a ser "neuronas de sesgo".

**Validación causal:**
Para confirmar que estas neuronas causan el sesgo (no sólo que están correlacionadas), se hace activation patching: se interviene específicamente esas neuronas y se mide si el sesgo en el output cambia. Si intervenir la neurona X cambia el sesgo en el output, X es causalmente responsable.

**Eliminación:**
Las neuronas de sesgo identificadas se **anulan** (sus pesos se ponen a cero o se escalan hacia abajo). Esto modifica quirúrgicamente las matrices de peso FFN en las capas donde se encuentran, sin tocar otras neuronas.

**Specificidad:**
Los autores verifican que las neuronas de sesgo identificadas son distintas para diferentes tipos de sesgo (sesgo de género vs. racial vs. religioso), validando que el método es específico.

---

## Datasets utilizados

- **WinoBias**: evaluación de sesgo de género en ocupaciones.
- **StereoSet**: sesgo general en completaciones.
- **BBQ**: preguntas con contexto ambiguo.
- **TruthfulQA**: para verificar que el modelo no pierde veracidad.
- **Downstream NLP tasks**: evaluación de retención de capacidades de instrucción.

---

## Ejemplo ilustrativo

En InstructGPT, la neurona 847 de la capa FFN-16 se activa fuertemente cuando hay pronombres femeninos en contextos de roles de baja autoridad ("asistente", "secretaria") y débilmente para roles de alta autoridad. Esta neurona contribuye directamente a que el modelo use "ella" para referirse a asistentes. Al poner en cero los pesos asociados a esta neurona, el modelo reduce esta asociación sin perder su capacidad de seguir instrucciones generales.

---

## Resultados principales

- Se identifican ~0.1-0.5% de neuronas como "neuronas de sesgo" — un número muy pequeño del total.
- Eliminar estas neuronas reduce el sesgo en WinoBias en un 20-30%.
- La degradación en tareas de instrucción es mínima (<1% en benchmarks de instrucción).
- Las neuronas de sesgo son en su mayoría distintas de las "neuronas de conocimiento" identificadas en trabajos de interpretabilidad.

---

## Ventajas respecto a trabajos anteriores

- Más preciso que el fine-tuning: sólo modifica un subconjunto minúsculo de parámetros.
- La validación causal con activation patching da fundamento interpretabilístico al método.
- Específico por tipo de sesgo: puede eliminar sesgo de género sin afectar el de raza, y viceversa.

---

## Trabajos previos relacionados

El paper combina dos líneas: interpretabilidad mecanística de transformers (localización de conocimiento en neuronas FFN) y mitigación de sesgo en LLMs de instrucción. Los trabajos previos más relevantes son los de edición de neuronas y los benchmarks de sesgo.

- **Meade et al. (2022) — An empirical survey of the effectiveness of debiasing techniques**: encuesta de referencia sobre técnicas de debiasing que motiva la necesidad de métodos más precisos; [2021_meade_debiasing-survey.md](2021_meade_debiasing-survey.html)
- **Nadeem et al. (2021) — StereoSet**: benchmark empleado para evaluar el sesgo estereotípico tras la eliminación de neuronas; [2021_nadeem_stereoset.md](2021_nadeem_stereoset.html)
- **Parrish et al. (2021) — BBQ**: benchmark de preguntas sesgadas con contexto ambiguo utilizado en la evaluación; [2021_parrish_bbq.md](2021_parrish_bbq.html)
- **Lin et al. (2021) — TruthfulQA**: benchmark de veracidad usado para verificar que la eliminación de neuronas no degrada la honestidad del modelo; [2021_lin_truthfulqa.md](2021_lin_truthfulqa.html)
- **Vig et al. (2020) — Investigating gender bias in language models using causal mediation analysis**: trabajo seminal que analiza causalmente qué componentes del transformer median el sesgo de género, metodología que inspira la validación causal de este paper; [2020_vig_gender-bias-causal.md](2020_vig_gender-bias-causal.html)
- **Geva et al. (2021) — Transformer feed-forward layers are key-value memories**: muestra que las capas FFN almacenan conocimiento factual, fundamento para buscar neuronas de sesgo en las FFN.
- **Meng et al. (2022) — ROME (Locating and editing factual associations in GPT)**: método de edición de conocimiento que localiza y edita hechos en neuronas específicas, paradigma del que se inspira la "cirugía" de neuronas de sesgo.
- **Gira et al. (2022) — Debiasing pre-trained language models via efficient fine-tuning**: método alternativo de debiasing eficiente, con el que se compara la precisión del enfoque basado en neuronas; [2022_gira_debiasing-efficient-finetuning.md](2022_gira_debiasing-efficient-finetuning.html)
- **Lauscher et al. (2021) — Sustainable modular debiasing**: aplica adapters modulares para debiasing, contrastando con la edición directa de parámetros específicos propuesta aquí.
- **Zhao et al. (2018) — WinoBias**: dataset de resolución de correferencias con sesgo de género que sirve como evaluación principal del método.

## Tags

`debiasing` `neuronas-de-sesgo` `FFN-layers` `interpretabilidad` `edición-quirúrgica`
