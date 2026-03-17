---
layout: paper
title: "Localizing Model Behavior with Path Patching"
year: 2023
date_published: "2023-04-12"
authors: "Nicholas W. Goldowsky-Dill, Chris MacLeod, Lucas Sato, Aryaman Arora"
published: "arXiv, 2023"
tags:
  - "interpretabilidad-mecanística"
  - "circuitos"
  - "path-patching"
  - "residual-stream"
  - "causalidad"
pdf: "/llm_bias/pdfs/2023_goldowskydill_path-patching.pdf"
status:
  - "Pendiente"
image: "imgs/2023_goldowskydill_path-patching.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---## Qué hace

Introduce **path patching**, una extensión del activation patching que permite trazar rutas causales específicas a través del grafo computacional del transformer, identificando no sólo qué componentes importan sino exactamente cómo se comunican entre sí.


---

## Metodología

**Limitación del activation patching:** El activation patching estándar mide si parchear un nodo X afecta el output, pero no revela *a través de qué camino* X afecta el output. Un nodo X podría afectar el output directamente, o podría hacerlo a través de un nodo intermedio Y. Esto es importante para entender el mecanismo completo.

**Path Patching:**
En lugar de parchear un nodo individual, se parcha un "camino" específico: la conexión de la salida del nodo A hacia el nodo B, mientras se mantienen todas las demás conexiones intactas.

Técnicamente: en el residual stream, cada cabeza/MLP escribe su output sumándolo. Path patching permite reemplazar sólo la contribución de A en la entrada de B, sin afectar cómo A contribuye a todos los demás nodos downstream.

**Lo que revela:**
- No sólo "la cabeza 9-6 importa" sino "la cabeza 9-6 importa porque alimenta a la cabeza 10-1, que es la que realmente genera el output".
- Permite mapear el grafo causal completo del circuito, no sólo los nodos aislados.

---

## Datasets utilizados

- **IOI**: principal, para comparar con Wang et al.
- **Factual associations**: "The capital of France is ___" → "Paris".
- Modelos evaluados: GPT-2 small y medium.

---

## Ejemplo ilustrativo

Activation patching revela que tanto la cabeza A como la cabeza B son importantes para la tarea IOI. Pero ¿se comunican entre sí o trabajan en paralelo? Path patching responde esto: se parcha el camino A→B (la contribución de A a la entrada de B) y se ve si el output cambia. Si sí cambia, A y B están en serie (A alimenta a B). Si no cambia (pero parchear A sí afecta el output), entonces A y B trabajan en paralelo. Esto permite reconstruir el grafo de comunicación dentro del circuito.

---

## Resultados principales

- En IOI, el path patching revela que las Name Mover Heads no reciben directamente la información de los Duplicate Token Heads, sino a través de las S-Inhibition Heads como intermediarias.
- Esta cadena causal era invisible para el activation patching estándar.
- Para asociaciones factuales, identifica que las cabezas de atención en capas medias consultan las capas MLP de capas anteriores (que almacenan los "hechos"), no al input directamente.

---

## Ventajas respecto a trabajos anteriores

- Más informativo que activation patching: revela la estructura de comunicación entre componentes.
- Permite construir diagramas causales completos del circuito, no sólo listas de componentes importantes.
- La granularidad de los caminos es clave para entender el mecanismo completo.

---

## Trabajos previos relacionados

- **Wang et al. (2022) — [Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 Small](2022_wang_ioi-circuit.html)**: combina ablación por media con una forma simple de path patching para identificar el circuito IOI, trabajo cuyo enfoque ad-hoc path patching formaliza y generaliza este paper.
- **Vig et al. (2020) — Investigating Gender Bias in Language Models Using Causal Mediation Analysis**: aplica análisis de mediación causal de Pearl a LLMs, midiendo efectos directos e indirectos de cabezas de atención, trabajo que inspira el enfoque de efectos sobre caminos específicos del path patching.
- **Pearl (2009, 2013) — Causality: Models, Reasoning and Inference / Path-specific Effects**: marco teórico causal del cual se deriva el path-specific effect que el path patching implementa de forma determinista para redes neuronales.
- **Geiger et al. (2020) — Neural Natural Language Inference Models Partially Embed Theories of Lexical Entailment**: aplica interchange interventions a BERT especificando significado semántico para cada nodo, trabajo que opera sobre nodos (como activation patching) pero con interpretación semántica, antecedente del enfoque causal.
- **Geiger et al. (2021) — [Causal Abstractions of Neural Networks](2021_geiger_causal-abstractions.html)**: formaliza intervenciones de intercambio para verificar abstracciones causales, marco teórico del que path patching es una instancia más granular enfocada en aristas del grafo.
- **Chan et al. (2022) — Causal Scrubbing: A Method for Rigorously Testing Interpretability Hypotheses**: propone causal scrubbing como generalización del patching que incluye clases de equivalencia en nodos, trabajo más general del que path patching es un caso especial más eficiente.
- **Meng et al. (2022) — Locating and Editing Factual Associations in GPT (ROME)**: usa causal tracing (una forma de activation patching) para localizar conocimiento factual en capas FFN, trabajo que usa la misma primitiva de intervención que path patching pero sin analizar aristas entre componentes.
- **Conmy et al. (2023) — [Towards Automated Circuit Discovery for Mechanistic Interpretability](2023_conmy_automated-circuit-discovery.html)**: automatiza el proceso de descubrimiento de circuitos usando patching sistemático sobre aristas, trabajo que extiende el path patching de este paper a una búsqueda automática.
- **Finlayson et al. (2021) — Causal Analysis of Syntactic Agreement Mechanisms in Neural Language Models**: aplica activation patching para estudiar acuerdo sujeto-verbo en GPT-2, ejemplo de análisis causal de componentes que path patching hace más preciso al considerar caminos entre ellos.

## Tags

`interpretabilidad-mecanística` `circuitos` `path-patching` `residual-stream` `causalidad`
