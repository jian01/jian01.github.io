---
layout: paper
title: "Attribution Patching Outperforms Automated Circuit Discovery"
year: 2024
authors: "Aaquib Syed, Can Rager, Arthur Conmy"
published: "BlackboxNLP Workshop, 2024"
tags:
  - "interpretabilidad-mecanística"
  - "circuitos"
  - "attribution-patching"
  - "gradientes"
  - "eficiencia"
pdf: "/llm_bias/pdfs/2024_syed_attribution-patching.pdf"
status:
  - "Leido"
image: "imgs/2024_syed_attribution-patching.png"
image_caption: "Curvas ROC para tres tareas de descubrimiento de circuitos (Greaterthan, IOI y Docstring), comparando EAP, Activation Patching y ACDC con distintas métricas; el área bajo la curva (AUC) indica la capacidad de cada método para identificar correctamente los componentes relevantes del circuito."
opinion: "<WIP>"
---
# Attribution Patching Outperforms Automated Circuit Discovery (2024)

**Autores**: Aaquib Syed, Can Rager, Arthur Conmy
**Publicado en**: BlackboxNLP Workshop, 2024

---

## Qué hace

Demuestra que el **attribution patching** — usar gradientes para estimar el impacto de cada componente — es más rápido y más preciso que ACDC (intervenciones causales completas) para descubrir circuitos en transformers.


---

## Metodología

**El problema con ACDC:** Para cada eje del grafo del transformer, ACDC hace un forward pass completo con patching, lo que requiere miles de forward passes en total. Esto es costoso.

**Attribution Patching:** En lugar de hacer intervenciones reales (costosas), se usa el **gradiente** como proxy del impacto. La idea:
- Para medir cuánto importa el eje A→B para el output final, se computa el gradiente del output con respecto a la activación en A cuando "llega" a B.
- Un gradiente grande indica que cambiar esa conexión cambiaría mucho el output.
- Un gradiente pequeño indica que la conexión es irrelevante.

Esta aproximación es analítica (un solo backward pass calcula el gradiente de todos los ejes simultáneamente) en lugar de empírica (un forward pass por eje en ACDC).

**Attribution Patching más preciso:** El paper también propone "Integrated Gradients Attribution Patching" que integra gradientes a lo largo de un camino entre la activación limpia y la corrupted, dando estimaciones más precisas del impacto real.

Las partes del modelo estudiadas son las mismas que en ACDC: **cabezas de atención y salidas FFN** en el residual stream.

---

## Datasets utilizados

- **IOI**: tarea de Indirect Object Identification (mismo que Wang et al. 2022).
- **Greater-than**: "The war lasted from 1945 to 19__".
- **Docstring**: completación de docstrings Python.
- **Factual recall**: capital de países.

---

## Ejemplo ilustrativo

Para descubrir el circuito IOI:
- ACDC necesita parchear cada uno de los ~1.500 ejes del grafo individualmente → ~1.500 forward passes → 3 horas de cómputo.
- Attribution Patching hace UN backward pass y calcula simultáneamente el gradiente de todos los ~1.500 ejes → 3 minutos de cómputo.

El circuito resultante es 85% similar al de ACDC y 80% similar al circuito manual de Wang et al. La velocidad es 60x mayor.

---

## Resultados principales

- Attribution Patching es 10-100x más rápido que ACDC para descubrir circuitos.
- El circuito descubierto es tan bueno o mejor que ACDC en la mayoría de tareas.
- Integrated Gradients Attribution Patching supera a attribution patching simple en precisión.
- Conclusión: gradientes son mejores proxies para causalidad de lo que se pensaba en el contexto del descubrimiento de circuitos.

---

## Ventajas respecto a trabajos anteriores

- Mejora dramáticamente la velocidad de ACDC sin sacrificar precisión.
- La base teórica en gradientes hace el método más interpretable que ACDC (que es empírico).
- Hace el descubrimiento de circuitos accesible para investigadores con recursos computacionales limitados.

---

## Trabajos previos relacionados

El paper se ubica dentro de la literatura de descubrimiento automático de circuitos en transformers, mejorando la eficiencia computacional de ACDC mediante aproximaciones por gradiente.

- **Conmy et al. (2023) — [Automated Circuit Discovery (ACDC)](2023_conmy_automated-circuit-discovery.html)**: el método ACDC es el punto de partida explícito del paper; attribution patching se propone como alternativa más rápida y precisa a ACDC para el mismo problema de descubrimiento de circuitos.
- **Wang et al. (2022) — [Interpretability in the Wild: IOI Circuit](2022_wang_ioi-circuit.html)**: el circuito IOI es uno de los benchmarks de evaluación del paper, y la referencia metodológica principal para entender qué debe descubrir el algoritmo de búsqueda de circuitos.
- **Elhage et al. (2021) — A Mathematical Framework for Transformer Circuits**: proporciona el marco conceptual de nodos y aristas en el grafo computacional del transformer sobre el que opera el attribution patching.
- **Goldowsky-Dill et al. (2023) — [Localizing Model Behavior with Path Patching](2023_goldowskydill_path-patching.html)**: introduce el path patching como método de atribución causal en transformers; el attribution patching es una aproximación por gradiente del mismo concepto.
- **Vig et al. (2020) — [Causal Mediation Analysis](2020_vig_gender-bias-causal.html)**: trabajo anterior de activation patching bajo otro nombre, citado como antecedente de la técnica de intervención causal sobre componentes del transformer.
- **Geiger et al. (2021) — [Causal Abstractions](2021_geiger_causal-abstractions.html)**: los "interchange interventions" son la versión más formal de las intervenciones causales que el attribution patching aproxima; se cita como fundamento teórico.
- **Hanna et al. (2023) — [GPT-2 Greater-Than](2023_hanna_gpt2-greater-than.html)**: el circuito greater-than es uno de los benchmarks de evaluación del paper, y el trabajo de Hanna et al. proporciona el circuito de referencia manual contra el que comparar los resultados del attribution patching.
- **Heimersheim & Janiak (2023) — [Python Docstrings Circuit](2023_heimersheim_python-docstrings.html)**: el circuito de docstrings es el tercer benchmark de evaluación del paper; citado como trabajo relacionado en el uso del grafo de composición entre cabezas.

## Tags

`interpretabilidad-mecanística` `circuitos` `attribution-patching` `gradientes` `eficiencia`
