---
layout: paper
title: "Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small"
year: 2022
date_published: "2022-11-01"
authors: "Kevin Wang, Alexandre Variengien, Arthur Conmy, Buck Shlegeris, Jacob Steinhardt"
published: "arXiv, 2022"
tags:
  - "interpretabilidad-mecanística"
  - "circuitos"
  - "GPT-2"
  - "attention-heads"
  - "IOI"
pdf: "/llm_bias/pdfs/2022_wang_ioi-circuit.pdf"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2022_wang_ioi-circuit.png"
image_caption: "Visualización de las activaciones del circuito en GPT-2 small para la tarea IOI, mostrando la estructura de cabezas de atención involucradas en la identificación del objeto indirecto."
opinion: "<WIP>"
---

## Qué hace

Identifica manualmente el circuito completo en GPT-2 small responsable de la tarea IOI (Indirect Object Identification): dado "John and Mary went to the store. John gave a bag to ___", el modelo debe completar con "Mary". Mapea 26 cabezas de atención con roles funcionales específicos.


---

## Metodología

Este paper es un hito de la interpretabilidad mecanística: el primer análisis completo de un circuito no trivial en un LLM.

**La tarea IOI:** Dado un texto con dos personajes (A y B) donde A aparece dos veces y B una, y una frase como "[A] le dio algo a ___", el modelo debe completar con B (el objeto indirecto).

**Metodología de activation patching:**
Para cada cabeza de atención del modelo, se realiza un "patch": se reemplaza la activación de esa cabeza con los valores que tendría en una versión "corrupted" de la misma oración (donde se intercambian los nombres). Si el output correcto del modelo se destruye al parchear la cabeza X, entonces X es parte del circuito.

**Los grupos funcionales descubiertos:**
- **Duplicate Token Heads** (capas 0-3): identifican qué tokens aparecen dos veces.
- **Induction Heads** (capas 5-6): detectan patrones de repetición.
- **S-Inhibition Heads** (capas 7-8): suprimen el primer sujeto (para evitar que el modelo complete con el nombre repetido).
- **Name Mover Heads** (capas 9-10): copian el nombre del objeto indirecto al output.
- **Backup Name Mover Heads** (capas 10-11): cabezas secundarias que toman el relevo si las principales fallan.

---

## Datasets utilizados

- **Dataset IOI**: ~500 templates con nombres propios ingleses variados.
  Ej: "When Mary and John went to the store, John gave a bag to ___" → "Mary"
  Ej: "Then, Alice and Bob had a meeting. Bob told the manager about ___" → "Alice"
- Evaluado únicamente en GPT-2 small (117M parámetros).

---

## Ejemplo ilustrativo

El circuito funciona así paso a paso:
1. Las Duplicate Token Heads en capa 2 detectan que "John" aparece dos veces en la secuencia.
2. Las S-Inhibition Heads en capas 7-8 "marcan" a John como el sujeto repetido que NO debe completar el espacio en blanco.
3. Las Name Mover Heads en capa 9 leen el residual stream, ven que Mary no está marcada como repetida, y la copian al output.

Si se parcha (desactiva) cualquier Name Mover Head, el modelo deja de completar con "Mary". Si se parcha las S-Inhibition Heads, el modelo puede completar con "John" (el nombre incorrecto/repetido).

---

## Resultados principales

- El circuito de 26 cabezas preserva el 90% del rendimiento IOI del modelo completo.
- Cada grupo funcional tiene una función interpretable y verificable experimentalmente.
- El circuito es suficientemente preciso como para predecir el comportamiento en variantes de la tarea no vistas durante el análisis.
- Las cabezas "backup" (respaldo) son un descubrimiento inesperado: el modelo tiene redundancia incorporada.

---

## Ventajas respecto a trabajos anteriores

- Primer análisis completo de un circuito no trivial en un LLM real.
- Introduce el vocabulario y metodología de "grupos funcionales" dentro de un circuito.
- Las herramientas desarrolladas (TransformerLens) se convierten en la librería estándar del área.

---

## Trabajos previos relacionados

- **Elhage et al. (2021) — A Mathematical Framework for Transformer Circuits**: establece el marco teórico del residual stream y las composiciones de cabezas de atención en transformers, base conceptual sobre la que se construye el análisis del circuito IOI.
- **Olah et al. (2020) — Zoom In: An Introduction to Circuits**: introduce el paradigma de "circuitos" en redes neuronales convolucionales, terminología y metodología que este paper traslada por primera vez a un LLM de tamaño real.
- **Meng et al. (2022) — Locating and Editing Factual Associations in GPT (ROME)**: localiza dónde se almacena conocimiento factual en GPT-J mediante causal tracing, técnica de localización causal que inspira el uso de activation patching para descubrir el circuito IOI.
- **Olsson et al. (2022) — In-context Learning and Induction Heads**: descubre y caracteriza las induction heads en transformers, trabajo que define el rol de las induction heads que el paper IOI integra en el circuito más complejo.
- **Geiger et al. (2021) — [Causal Abstractions of Neural Networks](2021_geiger_causal-abstractions.html)**: formaliza las intervenciones de intercambio como herramienta para verificar abstracciones causales, marco teórico causal en el que se inscribe el método de activation patching del paper IOI.
- **Nanda & Lieberum (2022) — A Mechanistic Interpretability Analysis of Grokking**: aplica análisis mecanístico a un fenómeno de generalización repentina usando metodología similar, y motiva las ablaciones por media que el paper IOI adopta.
- **Vig et al. (2020) — Investigating Gender Bias in Language Models Using Causal Mediation Analysis**: uno de los primeros trabajos en usar intervenciones causales sobre cabezas de atención en LLMs para estudiar efectos directos e indirectos.
- **Goldowsky-Dill et al. (2023) — [Localizing Model Behavior with Path Patching](2023_goldowskydill_path-patching.html)**: formaliza el path patching como extensión del activation patching para analizar caminos de información entre componentes, metodología desarrollada en paralelo e integrada en los experimentos del paper.
- **Conmy et al. (2023) — [Towards Automated Circuit Discovery for Mechanistic Interpretability](2023_conmy_automated-circuit-discovery.html)**: automatiza el proceso de descubrimiento de circuitos que el paper IOI realiza manualmente, tomando el circuito IOI como caso de referencia.

## Tags

`interpretabilidad-mecanística` `circuitos` `GPT-2` `attention-heads` `IOI`
