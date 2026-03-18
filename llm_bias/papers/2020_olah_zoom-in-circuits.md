---
layout: paper
title: "Zoom In: An Introduction to Circuits"
year: 2020
date_published: "2020-03-10"
authors: "Chris Olah, Nick Cammarata, Ludwig Schubert, Gabriel Goh, Michael Petrov, Shan Carter"
published: "Distill, 2020"
tags:
  - "interpretabilidad-mecanística"
  - "circuitos"
  - "redes-de-visión"
  - "features"
  - "composición"
status:
  - "Pendiente"
image: "imgs/2020_olah_zoom-in-circuits.png"
image_caption: "Ejemplos de features interpretables en InceptionV1: neuronas que responden a curvas, ojos, textos, y composición de esas features en circuitos de detección de objetos."
opinion: "<WIP>"
---

## Qué hace

Introduce el **paradigma de circuitos** para la interpretabilidad de redes neuronales, aplicado a redes de visión (InceptionV1/AlexNet). El paper propone que las redes neuronales no son cajas negras ininteligibles sino que pueden entenderse a nivel mecanístico: las neuronas individuales representan **features** interpretables (curvas, formas, texturas, conceptos), y esas features se conectan en **circuitos** — subgrafos del modelo que implementan comportamientos concretos y comprensibles.

Aunque el paper trabaja con modelos de visión, sus conceptos y metodología son los que toda la interpretabilidad mecanística de transformers (IOI, Greater-Than, ACDC) adopta directamente. Es el paper fundacional que define el vocabulario y la filosofía del campo.


---

## Metodología

El paper propone tres "claims" sobre redes neuronales que juntos constituyen la hipótesis de los circuitos:

**Claim 1 — Features**: Las neuronas de redes neuronales representan features significativas y comprensibles. Cada neurona puede interpretarse como un detector de un concepto específico: una neurona detecta "curvas hacia la derecha", otra detecta "textura de pelo", otra detecta "ojos de perro". Las features se visualizan mediante *feature visualization* (optimización de inputs para maximizar la activación) y se validan mostrando que los activadores naturales del dataset coinciden con la visualización.

**Claim 2 — Circuits**: Las conexiones entre neuronas forman circuitos que implementan algoritmos comprensibles. Por ejemplo, un circuito de detección de cabezas de perro: neuronas de ojos → neuronas de oreja → neurona de cara → neurona de perro. Cada conexión puede leerse directamente de los pesos de la red.

**Claim 3 — Universality**: Los mismos circuitos y features emergen de forma independiente en distintas redes entrenadas en los mismos datos, e incluso en redes entrenadas en datos distintos.

La metodología usa: feature visualization, análisis de pesos directos (lectura de matrices de pesos entre capas), y dataset examples (mostrar las imágenes del dataset que más activan cada neurona).

---

## Datasets utilizados

- **InceptionV1** (GoogLeNet): red de visión entrenada en ImageNet, modelo principal de análisis.
- **AlexNet**: para verificar la universalidad de los circuitos.
- **ImageNet**: dataset de imágenes sobre el que están entrenadas las redes analizadas.

---

## Ejemplo ilustrativo

El paper analiza en detalle el **curve detector circuit** en InceptionV1: hay neuronas que detectan segmentos de línea en distintas orientaciones (0°, 45°, 90°, 135°). En la siguiente capa, una neurona "curve detector" combina detectores de segmentos adyacentes: si una neurona de 45° y una de 90° se activan en posiciones contiguas, la neurona de curva se activa. Los pesos entre estas neuronas se pueden leer directamente y tienen el patrón esperado: peso positivo entre detector de 45° en posición izquierda y detector de 90° en posición derecha para la neurona de curva que gira de izquierda a derecha.

---

## Resultados principales

- Se identifican docenas de features interpretables en InceptionV1: detectores de curvas, texturas, partes de animales, conceptos de alto nivel como "perro" o "edificio".
- Se reverse-engineering completo de 5 circuitos: curve detector, high-low frequency detector, multimodal neurons, curve circuit, y dog head circuit.
- Se verifica la universalidad: los mismos detectores de curvas y sus circuitos emergen en InceptionV1, AlexNet y modelos entrenados en distintos datos.
- Las neuronas "multimodales" (que responden a múltiples conceptos distintos, como gatos y coches) sugieren que el espacio de features es más complejo de lo que el paradigma de features discretas sugiere.

---

## Ventajas respecto a trabajos anteriores

- La interpretabilidad anterior usaba sondas (*probing*) que entrenan clasificadores sobre activaciones para detectar si el modelo "sabe" algo, pero no explican el mecanismo. Los circuitos explican **cómo** el modelo computa su salida, no solo **qué** representa.
- La combinación de feature visualization + análisis de pesos + dataset examples crea una metodología triangulada que produce interpretaciones más robustas.
- El concepto de circuitos como subgrafos interpretables es directamente trasladable a transformers (donde Elhage et al. 2021 lo formalizan matemáticamente).

---

## Trabajos previos relacionados

- **Zeiler & Fergus (2013) — Visualizing and Understanding Convolutional Networks**: primeros intentos de visualizar qué aprenden las capas de CNNs mediante deconvolución; Olah et al. extienden esto al nivel de circuitos completos.
- **Elhage et al. (2021) — [A Mathematical Framework for Transformer Circuits](2021_elhage_transformer-circuits.html)**: traslada el paradigma de Olah et al. a transformers, con el formalismo del residual stream.
- **Wang et al. (2022) — [IOI Circuit](2022_wang_ioi-circuit.html)**: primer paper que aplica la metodología de circuitos a un comportamiento concreto de GPT-2.
- **Conmy et al. (2023) — [ACDC](2023_conmy_automated-circuit-discovery.html)**: automatiza el descubrimiento de circuitos en transformers usando el paradigma de Olah et al.

## Tags

`interpretabilidad-mecanística` `circuitos` `redes-de-visión` `features` `composición` `universalidad`
