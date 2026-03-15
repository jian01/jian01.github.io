---
layout: default
title: Interpretabilidad Mecanística
---

# Interpretabilidad Mecanística

Circuitos, neuronas y análisis causal para entender el comportamiento interno de los transformers.

[← Literature Review](/llm_bias/)

---

<div class="status-legend"><span class="dot dot-relevante"></span> Relevante&nbsp;&nbsp;<span class="dot dot-leido"></span> Leído&nbsp;&nbsp;<span class="dot dot-pendiente"></span> Pendiente&nbsp;&nbsp;<span class="dot dot-irrelevante"></span> Irrelevante</div>


## Fundamentos

La interpretabilidad mecanística parte de la hipótesis de que las redes neuronales no son cajas negras irreducibles sino que implementan algoritmos comprensibles que pueden ser reverse-engineered. Los trabajos fundacionales establecen el vocabulario y el formalismo del campo: el paradigma de circuitos (subgrafos del modelo que implementan comportamientos concretos), el formalismo del residual stream (cada capa del transformer lee y escribe en un stream compartido, lo que permite analizar sus contribuciones de forma aditiva), y el marco de abstracciones causales (que permite verificar formalmente si un circuito hipotético explica el comportamiento observado mediante intervenciones controladas).

| Estado | Año | Título | Resumen |
| --- |-----|--------|---------|
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2020 | Zoom In: An Introduction to Circuits | [Ver](../papers/2020_olah_zoom-in-circuits.html) |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2021 | A Mathematical Framework for Transformer Circuits | [Ver](../papers/2021_elhage_transformer-circuits.html) |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2021 | Causal Abstractions of Neural Networks | [Ver](../papers/2021_geiger_causal-abstractions.html) |

---

## Circuitos y Patching

El análisis de circuitos en transformers consiste en identificar qué cabezas de atención y capas FFN colaboran para producir un comportamiento específico. La técnica principal es el **activation patching**: se corrompe la activación de un componente con la de una entrada diferente y se mide cuánto cae el rendimiento del modelo — si cae mucho, ese componente es causalmente relevante. El path patching extiende esta idea trazando el flujo de información a través de rutas específicas del residual stream. ACDC automatiza el proceso de descubrimiento de circuitos usando estas intervenciones de forma sistemática, mientras que attribution patching aproxima el patching mediante gradientes para hacerlo escalar a modelos grandes.

| Estado | Año | Título | Resumen |
| --- |-----|--------|---------|
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2020 | Investigating Gender Bias in Language Models Using Causal Mediation Analysis | [Ver](../papers/2020_vig_gender-bias-causal.html) |
| <span class="dot dot-leido" title="Leído"></span> | 2022 | Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small | [Ver](../papers/2022_wang_ioi-circuit.html) |
| <span class="dot dot-relevante" title="Relevante"></span><span class="dot dot-leido" title="Leído"></span> | 2023 | Towards Automated Circuit Discovery for Mechanistic Interpretability | [Ver](../papers/2023_conmy_automated-circuit-discovery.html) |
| <span class="dot dot-relevante" title="Relevante"></span><span class="dot dot-leido" title="Leído"></span> | 2023 | How does GPT-2 compute greater-than? | [Ver](../papers/2023_hanna_gpt2-greater-than.html) |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2023 | Localizing Model Behavior with Path Patching | [Ver](../papers/2023_goldowskydill_path-patching.html) |
| <span class="dot dot-leido" title="Leído"></span> | 2023 | A circuit for Python docstrings in a 4-layer attention-only transformer | [Ver](../papers/2023_heimersheim_python-docstrings.html) |
| <span class="dot dot-leido" title="Leído"></span> | 2024 | Attribution Patching Outperforms Automated Circuit Discovery | [Ver](../papers/2024_syed_attribution-patching.html) |

---

## Neuronas y Localización de Conocimiento

En paralelo al análisis de circuitos, otra línea estudia qué neuronas individuales o grupos de neuronas almacenan tipos específicos de conocimiento o habilidades. Las capas FFN de los transformers funcionan como memorias clave-valor: ciertas neuronas se activan selectivamente ante conceptos factuales, habilidades lingüísticas o sesgos sociales. Identificar estas neuronas permite intervenciones más quirúrgicas que modificar circuitos completos: se puede suprimir, amplificar o reescribir el conocimiento asociado a neuronas específicas. La interpretabilidad automática lleva esta idea más lejos usando un LLM para generar y verificar hipótesis sobre qué representa cada neurona, haciendo el proceso escalable a modelos con cientos de miles de neuronas.

| Estado | Año | Título | Resumen |
| --- |-----|--------|---------|
| <span class="dot dot-leido" title="Leído"></span> | 2022 | Finding Skill Neurons in Pre-trained Transformer-based Language Models | [Ver](../papers/2022_wang_skill-neurons.html) |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2022 | Task-specific Compression for Multi-task Language Models using Attribution-based Pruning | [Ver](../papers/2022_yang_task-specific-compression.html) |
| <span class="dot dot-leido" title="Leído"></span> | 2023 | Task-Specific Skill Localization in Fine-tuned Language Models | [Ver](../papers/2023_panigrahi_skill-localization.html) |
| <span class="dot dot-leido" title="Leído"></span> | 2023 | Large language models show human-like content biases in transmission chain experiments | [Ver](../papers/2023_acerbi_human-like-biases.html) |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2023 | Language Models Can Explain Neurons in Language Models | [Ver](../papers/2023_bills_neuron-explanation.html) |
| <span class="dot dot-relevante" title="Relevante"></span><span class="dot dot-leido" title="Leído"></span> | 2025 | Dissecting Bias in LLMs: A Mechanistic Interpretability Perspective | [Ver](../papers/2025_chandna_dissecting-bias.html) |
