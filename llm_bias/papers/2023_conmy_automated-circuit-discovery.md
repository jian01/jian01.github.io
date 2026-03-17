---
layout: paper
title: "Towards Automated Circuit Discovery for Mechanistic Interpretability"
year: 2023
date_published: "2023-04-28"
authors: "Arthur Conmy, Adrià Garriga-Alonso, Stefan Heimersheim, Aengus Lynch, Augustine N. Mavor-Parker"
published: "NeurIPS, 2023"
tags:
  - "interpretabilidad-mecanística"
  - "circuitos"
  - "activation-patching"
  - "automatización"
  - "transformer"
pdf: "/llm_bias/pdfs/2023_conmy_automated-circuit-discovery.pdf"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2023_conmy_automated-circuit-discovery.png"
image_caption: "Visualización del circuito descubierto por ACDC en un transformer: los nodos y aristas en rojo representan los componentes causalmente relevantes identificados automáticamente, destacados sobre el grafo completo del modelo en gris."
opinion: "<WIP>"
---
# Towards Automated Circuit Discovery for Mechanistic Interpretability (2023)

**Autores**: Arthur Conmy, Adrià Garriga-Alonso, Stefan Heimersheim, Aengus Lynch, Augustine N. Mavor-Parker
**Publicado en**: NeurIPS, 2023

---

## Qué hace

Propone ACDC (**A**utomated **C**ircuit **D**iscovery for Mechanistic Interpretability), un algoritmo que automatiza el descubrimiento de "circuitos" — subgrafos de cabezas de atención y MLPs responsables de comportamientos específicos — eliminando la necesidad de encontrarlos manualmente.


---

## Metodología

**¿Qué es un circuito?** Un circuito es el conjunto mínimo de componentes del transformer (cabezas de atención, neuronas FFN) que, cuando se remueven del modelo, destruyen el comportamiento estudiado. Por ejemplo, el circuito para la tarea IOI (Indirect Object Identification) incluye ~26 cabezas específicas.

**El problema del descubrimiento manual:** Identificar circuitos manualmente (como en Wang et al. 2022) requiere meses de trabajo de investigadores. ACDC automatiza este proceso.

**El algoritmo ACDC:**
El transformer puede verse como un grafo donde los nodos son (cabezas de atención y MLPs) y los ejes son conexiones entre ellos a través del residual stream. ACDC trabaja en este grafo:

1. Comenzar con el grafo completo (todos los nodos y ejes).
2. Para cada eje del grafo: hacer patching del eje con sus valores de una "baseline" (corrupted input que no produce el comportamiento de interés) y medir cuánto cambia el output del modelo.
3. Si el cambio en el output es menor a un umbral, el eje no es necesario para el comportamiento → se elimina del circuito.
4. Repetir iterativamente hasta que sólo queden los ejes causalmente importantes.

El patching se hace sobre el **residual stream** entre componentes, lo que permite analizar la causalidad a nivel de conexiones individuales.

---

## Datasets utilizados

- **IOI (Indirect Object Identification)**: "John and Mary went to the store. John gave a bag to ___" → "Mary".
- **Docstring completion**: completar el nombre de función en docstrings Python.
- **Greater-than task**: "The war lasted from 1945 to 19__" → años > 45.
- **Factual recall**: "The Eiffel Tower is in ___" → "Paris".

---

## Ejemplo ilustrativo

Para la tarea IOI, ACDC recibe el grafo completo con ~1.500 ejes posibles y, después de pocas horas de cómputo, identifica automáticamente los ~100 ejes más importantes. El circuito resultante coincide en un 80% con el circuito descubierto manualmente por Wang et al. en 3 meses de investigación. ACDC tardó 3 horas en una GPU donde el trabajo manual tardó 3 meses.

---

## Resultados principales

- ACDC descubre circuitos similares a los manuales en IOI y docstring con alta concordancia (~80%).
- El circuito descubierto automáticamente preserva el 90% del rendimiento en la tarea con sólo el 5-15% de todos los componentes del modelo.
- Velocidad: horas vs. meses para el descubrimiento manual.
- Limitación: ACDC puede perder conexiones de largo rango que son difíciles de detectar con patching individual.

---

## Ventajas respecto a trabajos anteriores

- Escala el descubrimiento de circuitos de proyectos de investigación de meses a cómputo de horas.
- El algoritmo es principled (basado en intervenciones causales) y no heurístico.
- Aplicable a cualquier comportamiento medible en cualquier modelo de transformer.

---

## Trabajos previos relacionados

El paper organiza los trabajos previos en tres áreas: (1) interpretabilidad mecanística y circuitos, (2) poda de redes neuronales, y (3) interpretación causal de redes neuronales.

- **Wang et al. (2022) — [Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 Small](2022_wang_ioi-circuit.html)**: descubre manualmente el circuito IOI que ACDC después reproduce automáticamente, siendo el caso de referencia principal para evaluar ACDC.
- **Hanna et al. (2023) — [How does GPT-2 compute greater-than?](2023_hanna_gpt2-greater-than.html)**: identifica manualmente el circuito para la tarea Greater-Than, otro caso de referencia usado para evaluar ACDC.
- **Goldowsky-Dill et al. (2023) — [Localizing Model Behavior with Path Patching](2023_goldowskydill_path-patching.html)**: formaliza el path patching que ACDC utiliza como primitiva de intervención causal para evaluar la importancia de aristas en el grafo computacional.
- **Geiger et al. (2021) — [Causal Abstractions of Neural Networks](2021_geiger_causal-abstractions.html)**: proporciona el marco teórico de las abstracciones causales y las intervenciones de intercambio en las que se basa la metodología de patching causal de ACDC.
- **Elhage et al. (2021) — A Mathematical Framework for Transformer Circuits**: establece el marco teórico del residual stream y las composiciones entre cabezas de atención, base conceptual de la representación como grafo computacional que usa ACDC.
- **Olah et al. (2020) — Zoom In: An Introduction to Circuits**: introduce el paradigma de circuitos para redes neuronales de visión artificial, terminología y metodología que ACDC extiende y automatiza para transformers.
- **Bills et al. (2023) — Language Models Can Explain Neurons in Language Models**: único trabajo anterior de automatización de interpretabilidad, que usa LLMs para etiquetar neuronas, siendo el único antecedente en automatización que ACDC cita explícitamente.
- **Chan et al. (2022) — Causal Scrubbing: A Method for Rigorously Testing Interpretability Hypotheses**: propone el causal scrubbing como método más general que el patching individual de ACDC pero más computacionalmente costoso, trabajo con el que ACDC se compara directamente.
- **Meng et al. (2022) — Locating and Editing Factual Associations in GPT (ROME)**: localiza conocimiento factual en capas FFN mediante causal tracing, ejemplo de uso de intervenciones causales para localizar comportamientos que motiva la automatización de ACDC.

## Tags

`interpretabilidad-mecanística` `circuitos` `activation-patching` `automatización` `transformer`
