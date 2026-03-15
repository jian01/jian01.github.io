---
layout: paper
title: "Precise In-Parameter Concept Erasure in Large Language Models"
year: 2025
authors: "Fazl Barez, Mor Geva, Yoav Gur-Arieh, Yihuai Hong, Haya Clara Suslik"
published: "Association for Computational Linguistics, 2025"
tags:
  - "machine-unlearning"
  - "edición-de-modelos"
  - "interpretabilidad"
  - "FFN-layers"
  - "borrado-conceptos"
pdf: "/llm_bias/pdfs/2025_barez_precise-concept-erasure.pdf"
method_type: "Enmascarado / edición de pesos"
status:
  - "Pendiente"
image: "imgs/2025_barez_precise-concept-erasure.png"
image_caption: "Gráficos de violín que muestran la distribución del delta en escala Likert (cambio percibido en el concepto) para cuatro condiciones de evaluación: arg-hum, arg-llm, simple y mixed."
---
# Precise In-Parameter Concept Erasure in Large Language Models (2025)

**Autores**: Fazl Barez, Mor Geva, Yoav Gur-Arieh, Yihuai Hong, Haya Clara Suslik
**Publicado en**: Association for Computational Linguistics, 2025
**Tipo de método**: Enmascarado / edición de pesos

---

## Qué hace

Propone un método para borrar conceptos específicos de los parámetros de un LLM de forma quirúrgica, identificando primero exactamente qué neuronas y matrices de pesos almacenan el concepto, y luego modificando sólo esos parámetros.


---

## Metodología

Este método combina interpretabilidad mecanística con edición de modelos para lograr un borrado más preciso que los métodos de fine-tuning indiscriminados.

**Paso 1 — Localización del concepto:**
Se usan dos técnicas para identificar dónde está almacenado el concepto:
- **Probing classifiers**: se entrena un clasificador lineal simple que toma las activaciones de cada capa del transformer y predice si el contexto actual está relacionado con el concepto a borrar. La capa donde el clasificador tiene más accuracy es donde el concepto está representado con más fuerza.
- **Activation patching**: se hacen intervenciones causales (patching) para verificar qué capas, cuando se intervienen, causan cambios en el comportamiento relacionado con el concepto.

**Paso 2 — Borrado quirúrgico:**
Una vez identificadas las capas y dimensiones relevantes, se aplica una edición directa a esas matrices de pesos (principalmente FFN layers del transformer). La edición consiste en proyectar las componentes del espacio de activaciones asociadas al concepto hacia el subespacio ortogonal — eliminando la dirección que representaba el concepto sin afectar las demás direcciones.

Esto modifica directamente los **pesos de las capas FFN** en las capas identificadas, pero sólo las dimensiones relevantes para el concepto.

---

## Datasets utilizados

- **Datasets de género/ocupación**: asociaciones estereotipadas (médico-hombre, enfermera-mujer).
- **Datasets de conocimiento factual**: capital de países, fechas históricas.
- Evaluación: accuracy en el concepto borrado vs. otros conceptos relacionados y no relacionados.

---

## Ejemplo ilustrativo

El concepto a borrar: la asociación entre "abogado" y el género masculino. El método primero hace probing: entrena un clasificador que, dado los vectores de activación de la capa 16, predice el género implícito cuando el modelo procesa la palabra "abogado". Si el clasificador tiene 90% de accuracy en la capa 16, ahí está el concepto. Luego, el método identifica exactamente qué neuronas de la FFN de la capa 16 forman la dirección "abogado=masculino" en el espacio vectorial y la borra quirúrgicamente. Después del borrado, el modelo ya no asocia "abogado" con ningún género específico.

---

## Resultados principales

- El método borra el 80-90% de la información del concepto objetivo medida por probing accuracy.
- La degradación en conceptos no relacionados es menor del 2%.
- Más preciso que métodos de fine-tuning completo: estos últimos suelen afectar conceptos adyacentes.
- Funciona mejor en conceptos con localización clara (alta accuracy de probing en pocas capas).

---

## Ventajas respecto a trabajos anteriores

- Primer método de borrado de conceptos con fundamento en interpretabilidad mecanística.
- La precisión quirúrgica es significativamente mayor que la de fine-tuning o gradient ascent.
- La localización previa del concepto garantiza que sólo se modifican los parámetros necesarios.

---

## Trabajos previos relacionados

El paper combina dos líneas de trabajo: machine unlearning/edición de modelos para borrar conocimiento, e interpretabilidad mecanística para localizar conceptos dentro de las representaciones de LLMs.

- **Cao & Yang (2015) — Towards Making Systems Forget with Machine Unlearning**: [Cao & Yang (2015)](2015_cao_machine-unlearning.html) establece el marco formal del machine unlearning; este paper extiende esa noción al borrado quirúrgico de conceptos específicos en lugar de datos de entrenamiento.
- **Yao et al. (2023) — Large Language Model Unlearning**: [Yao et al.](2023_yao_large-llm-unlearning.html) representa los métodos de unlearning mediante gradient ascent indiscriminado; este paper mejora su precisión usando localización mecanística previa.
- **Li et al. (2024) — The WMDP Benchmark**: [WMDP](2024_li_wmdp.html) introduce RMU y el benchmark de conocimiento peligroso; el paper de Barez apunta a mayor precisión que RMU al no perturbar representaciones indiscriminadamente.
- **Lynch et al. (2024) — Eight Methods to Evaluate Robust Unlearning**: [Lynch et al.](2024_lynch_eight-methods.html) demuestra la fragilidad de los métodos de unlearning actuales ante reaprendizaje, motivando la necesidad de borrado más preciso e internamente fundamentado.
- **Łucki et al. (2024) — Adversarial Unlearning**: [Łucki et al.](2024_ucki_adversarial-unlearning.html) muestra que los métodos estándar solo "bypasean" los conceptos sin eliminarlos de los pesos, motivando el enfoque de borrado genuino en parámetros de este paper.
- **Ravfogel et al. (2020) — Null-it-Out**: propone proyección ortogonal sobre representaciones de activaciones para eliminar conceptos en inferencia; es antecedente directo del enfoque de borrado en espacio de activaciones, aunque Barez et al. lo aplica directamente a pesos FFN.
- **Meng et al. (2022) — Locating and Editing Factual Associations in GPT (ROME)**: localiza y edita información factual en capas FFN del transformer; es referencia clave para el componente de edición quirúrgica de pesos que el paper adopta.
- **Cloud et al. (2024) — Gradient Routing**: [Gradient Routing](2024_cloud_gradient-routing.html) localiza capacidades en sub-redes mediante enrutamiento de gradientes durante el entrenamiento; trabajo estrechamente relacionado en el objetivo de borrado preciso de capacidades en LLMs.
- **Fan et al. (2025) — Unlearning and Relearning**: [Fan et al.](2025_fan_unlearning-relearning.html) estudia la robustez del unlearning ante ataques de reaprendizaje; el borrado preciso en parámetros propuesto por Barez et al. es relevante para esa misma robustez.

## Tags

`machine-unlearning` `edición-de-modelos` `interpretabilidad` `FFN-layers` `borrado-conceptos`
