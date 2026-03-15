---
layout: paper
title: "Causal Abstractions of Neural Networks"
year: 2021
authors: "Atticus Geiger, Hanson Lu, Thomas Icard, Christopher Potts"
published: "NeurIPS, 2021"
tags:
  - "interpretabilidad"
  - "causalidad"
  - "intervenciones"
  - "redes-neuronales"
  - "razonamiento"
pdf: "/llm_bias/pdfs/2021_geiger_causal-abstractions.pdf"
status:
  - "Pendiente"
image: "imgs/2021_geiger_causal-abstractions.png"
image_caption: "Gráfico de box-plot comparando la atribución media en condiciones \"Different\" y \"Matched\", ilustrando la diferencia de efecto causal entre componentes del modelo según el análisis de intervenciones de intercambio propuesto en el paper."
---
# Causal Abstractions of Neural Networks (2021)

**Autores**: Atticus Geiger, Hanson Lu, Thomas Icard, Christopher Potts
**Publicado en**: NeurIPS, 2021

---

## Qué hace

Formaliza la relación entre los componentes de una red neuronal y modelos causales simbólicos usando el concepto de **abstracción causal**. Introduce las "interchange interventions" como herramienta para verificar si una red neuronal implementa un modelo causal específico.


---

## Metodología

**El problema:** Queremos saber si una red neuronal "realmente" implementa un cierto proceso de razonamiento (ej. "el modelo hace inferencia lógica como si aplicara la regla: si A entonces B"). Pero las redes neuronales son cajas negras — no podemos leer directamente qué está computando cada neurona.

**Abstracción causal:** Se define formalmente cuándo una red neuronal N es una implementación de un modelo causal abstracto M. La intuición es: si intervenimos en N de la manera que M prescribiría, el output de N debería cambiar de la manera que M predice.

**Interchange Interventions (intervenciones de intercambio):**
Dado dos inputs X y X', se "intercambia" la representación interna de X en una capa específica del modelo con la representación de X'. Si el output cambia de la manera predicha por el modelo causal M, entonces esa capa implementa el nodo correspondiente en M.

Ejemplo: Si M predice que "el modelo determina si A→B en la capa 5, y luego usa eso para determinar la conclusión en la capa 8", se puede verificar haciendo interchange interventions en estas capas específicas y viendo si los outputs concuerdan con las predicciones de M.

---

## Datasets utilizados

- **Synthetic logical reasoning**: datasets artificiales de inferencias modus ponens (si A entonces B, A → B).
- **HANS (Heuristic Analysis for NLI Systems)**: para modelos de inferencia textual.
- **Arithmetic tasks**: sumas y comparaciones simples.
- Evaluado en BERT, transformers pequeños entrenados en tareas específicas.

---

## Ejemplo ilustrativo

Modelo causal M: "Para resolver A and (B or C), el modelo primero evalúa (B or C) en la capa 3, y luego combina ese resultado con A en la capa 6."

Interchange intervention: se toma un input donde B=True, C=False (entonces B or C=True), y se intercambia la representación de la capa 3 con la de un input donde B=False, C=True (también B or C=True). Si el output final no cambia (porque en ambos casos B or C=True), entonces el modelo efectivamente está computando (B or C) en la capa 3 según lo predice M.

---

## Resultados principales

- Los modelos de transformer entrenados en razonamiento lógico implementan estructuras causales alineadas con el modelo causal esperado en el 80-90% de los casos.
- Las interchange interventions exitosas confirman que el modelo "realmente" implementa los pasos intermedios del razonamiento, no sólo memoriza input-output.
- Las capas más profundas tienden a implementar operaciones más abstractas/finales del razonamiento.

---

## Ventajas respecto a trabajos anteriores

- Formaliza por primera vez la noción de "implementar un proceso causal" en una red neuronal.
- Las interchange interventions son un método más preciso que el probing (que sólo mide correlación, no causalidad).
- Sienta las bases teóricas para toda la literatura posterior de interpretabilidad causal e intervenciones.

---

## Trabajos previos relacionados

El paper organiza los trabajos previos en tres categorías: (1) sondas (probes), que miden correlación pero no causalidad; (2) métodos de atribución, que cuantifican la contribución de representaciones al output; y (3) métodos de intervención, que son los más directamente relacionados con el enfoque causal propuesto.

- **Alain & Bengio (2016) — Understanding Intermediate Layers Using Linear Classifier Probes**: trabajo representativo del enfoque de probing, que el paper critica por medir correlación en lugar de causalidad y por poder identificar información "irrelevante" causalmente.
- **Hewitt & Manning (2019) — A Structural Probe for Finding Syntax in Word Representations**: ejemplo de probing para propiedades lingüísticas en representaciones de transformers, cuyas limitaciones causales motivan el enfoque de este paper.
- **Sundararajan et al. (2017) — Axiomatic Attribution for Deep Networks (Integrated Gradients)**: método de atribución con interpretación causal bien definida, discutido como el antecedente más riguroso antes de las interchange interventions.
- **Ravichander et al. (2021) — Probing the Probing Paradigm: Does Probing Accuracy Entail Task Relevance?**: critica directamente las limitaciones del probing como método para inferir propiedades causales, trabajo que refuerza la motivación de este paper.
- **Pearl (2009) — Causality: Models, Reasoning and Inference**: marco teórico fundamental de inferencia causal del cual se derivan los modelos causales simbólicos usados como referencia en las abstracciones causales.
- **Woodward (2003) — Making Things Happen: A Theory of Causal Explanation**: fundamento filosófico de la teoría intervencionalista de la causalidad en la que se basa el formalismo de interchange interventions.
- **Vig et al. (2020) — Investigating Gender Bias in Language Models Using Causal Mediation Analysis**: aplica análisis de mediación causal (basado en Pearl) para estudiar el sesgo de género en LLMs, trabajo concreto de aplicación de intervenciones causales a transformers que precede a este enfoque más general.
- **Elazar et al. (2020) — Amnesic Probing: Behavioral Explanation with Amnesic Counterfactuals**: propone intervenciones de borrado de información para estudiar el impacto causal de representaciones, alternativa al probing con mayor rigor causal.
- **Geiger et al. (2020) — Neural Natural Language Inference Models Partially Embed Theories of Lexical Entailment**: trabajo previo de los mismos autores que aplica intervenciones de intercambio a BERT en tareas de inferencia léxica, siendo el precursor directo de esta formalización.

## Tags

`interpretabilidad` `causalidad` `intervenciones` `redes-neuronales` `razonamiento`
