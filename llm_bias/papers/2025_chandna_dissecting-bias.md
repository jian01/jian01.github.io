---
layout: paper
title: "Dissecting Bias in LLMs: A Mechanistic Interpretability Perspective"
year: 2025
authors: "Bhavik Chandna, Zubair Bashir, Procheta Sen"
published: "arXiv, 2025"
tags:
  - "interpretabilidad-mecanística"
  - "sesgo-de-género"
  - "circuitos"
  - "activation-patching"
  - "probing"
pdf: "/llm_bias/pdfs/2025_chandna_dissecting-bias.pdf"
method_type: "Evaluación / análisis"
datasets:
  - "WinoBias"
  - "StereoSet"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2025_chandna_dissecting-bias.png"
image_caption: "Gráfico de barras que muestra la cantidad de conexiones (aristas) importantes identificadas en cada capa del transformer (capas 0 a 31), revelando concentraciones de procesamiento de sesgo en las capas iniciales y finales del modelo."
opinion: "<WIP>"
---
# Dissecting Bias in LLMs: A Mechanistic Interpretability Perspective (2025)

**Autores**: Bhavik Chandna, Zubair Bashir, Procheta Sen
**Publicado en**: arXiv, 2025
**Tipo de método**: Evaluación / análisis

---

## Qué hace

Aplica herramientas de interpretabilidad mecanística (activation patching, probing de cabezas de atención, análisis de FFN) para localizar exactamente dónde y cómo se codifica el sesgo de género y racial en LLMs, trazando el flujo de información sesgada a través de las capas del transformer.


---

## Metodología

Este paper aplica las metodologías de circuit analysis al problema del sesgo, en lugar de a tareas de razonamiento como IOI o greater-than.

**Paso 1 — Probing de representaciones:**
Para cada capa del transformer, se entrena un clasificador lineal que predice el género implícito del sujeto de una oración (ej. ¿el modelo está procesando esto como "hombre" o "mujer"?). La accuracy del clasificador en cada capa indica dónde se representa esta información.

**Paso 2 — Activation patching para causalidad:**
Se intercambian las activaciones de capas específicas entre la versión masculina y femenina de la misma oración, midiendo cuánto cambia el output sesgado. Las capas donde el patch produce mayor cambio son causalmente responsables del sesgo.

**Paso 3 — Análisis de cabezas de atención:**
Se identifican qué cabezas de atención específicas atienden a tokens de género y cómo propagan esa información al residual stream.

**Paso 4 — Análisis de FFN:**
Se estudia qué neuronas FFN se activan más para tokens con carga de género y cómo sus activaciones contribuyen a los logits del token sesgado en el output.

---

## Datasets utilizados

- **WinoBias**: resolución de correferencias de género en ocupaciones.
- **StereoSet**: completación de oraciones estereotipadas.
- Plantillas custom de profesiones con variaciones de género.
- Evaluado en GPT-2 (medium, large) y Llama-2-7B.

---

## Ejemplo ilustrativo

El paper traza el procesamiento de: "El enfermero atiende a sus pacientes con cuidado. Él es..." vs "La enfermera atiende a sus pacientes con cuidado. Ella es..."

El análisis muestra:
- Capas 1-4: la información de género del pronombre ("él/ella") es representada pero con baja influencia en las predicciones.
- Capa 6-8: la cabeza de atención 7-4 atiende fuertemente al token "enfermero/a" y propaga la asociación de género al residual stream.
- Capas 10-12: las neuronas FFN amplifican la predicción sesgada (ej. "enfermera" → mayor probabilidad de atributos de cuidado).

---

## Resultados principales

- El sesgo de género no está distribuido uniformemente — está concentrado en 5-8 cabezas de atención específicas.
- Las cabezas sesgadas están principalmente en capas medias (capas 6-10 para modelos de 12 capas).
- Las capas FFN amplifican el sesgo inicialmente introducido por las cabezas de atención.
- El mapa del sesgo es consistente entre GPT-2 y Llama-2, sugiriendo mecanismos similares en arquitecturas distintas.

---

## Ventajas respecto a trabajos anteriores

- Primer análisis completo de circuitos de sesgo en LLMs usando la metodología de mechanistic interpretability.
- Identifica la jerarquía de procesamiento del sesgo: cabezas de atención lo introducen, FFN lo amplifica.
- El mapa detallado orienta qué componentes deben modificarse en el debiasing para máxima efectividad.

---

## Trabajos previos relacionados

El paper organiza los trabajos relacionados en tres bloques: sesgo en LLMs en general, interpretabilidad mecanística como campo, e interpretabilidad mecanística aplicada al análisis de sesgo. Este encuadre refleja la novedad del paper: aplicar herramientas de MI al problema específico del sesgo.

- **Vig et al. (2020) — [Investigating Gender Bias with Causal Mediation Analysis](2020_vig_gender-bias-causal.html)**: trabajo pionero en el uso de análisis de mediación causal (forma temprana de activation patching) para localizar neuronas y cabezas responsables del sesgo de género en GPT-2; el paper de Chandna et al. extiende este análisis a modelos más grandes y a sesgo racial.
- **Syed et al. (2024) — [Attribution Patching](2024_syed_attribution-patching.html)**: la técnica EAP (Edge Attribution Patching) que el paper usa como método principal para asignar puntuaciones de importancia a las aristas del grafo computacional del transformer.
- **Wang et al. (2022) — [IOI Circuit](2022_wang_ioi-circuit.html)**: establece el marco de circuitos en GPT-2 small y el análisis de cabezas de atención y MLP como nodos del grafo computacional, metodología que el paper adapta para estudiar sesgo.
- **Conmy et al. (2023) — [ACDC](2023_conmy_automated-circuit-discovery.html)**: introduce el descubrimiento automático de circuitos relevantes para tareas específicas, mencionado como método alternativo al EAP para el descubrimiento de los circuitos de sesgo.
- **Geiger et al. (2021) — [Causal Abstractions](2021_geiger_causal-abstractions.html)**: proporciona el marco de intervenciones causales para determinar si un componente implementa un mecanismo específico, base teórica de las intervenciones causales del paper.
- **Goldowsky-Dill et al. (2023) — [Path Patching](2023_goldowskydill_path-patching.html)**: refina la comprensión de los induction heads y el flujo de información en transformers, trabajo metodológico relacionado con el análisis de aristas del paper.
- **Meng et al. (2022) — ROME: Locating and Editing Factual Associations**: demuestra que el conocimiento factual se almacena en capas FFN específicas; el paper extiende este principio al estudio de cómo el sesgo se codifica en FFN y lo amplifica.
- **Hanna et al. (2023) — [GPT-2 Greater-Than](2023_hanna_gpt2-greater-than.html)**: ejemplo representativo de análisis de circuitos en GPT-2 que el paper cita como trabajo relacionado en MI, cuyo método de identification de circuitos se adapta al problema del sesgo.

## Tags

`interpretabilidad-mecanística` `sesgo-de-género` `circuitos` `activation-patching` `probing`
