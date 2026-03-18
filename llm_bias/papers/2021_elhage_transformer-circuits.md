---
layout: paper
title: "A Mathematical Framework for Transformer Circuits"
year: 2021
date_published: "2021-12-22"
authors: "Nelson Elhage, Neel Nanda, Catherine Olsson, Tom Henighan, Nicholas Joseph, Ben Mann, Amanda Askell, Yuntao Bai, Anna Chen, Tom Conerly, Nova DasSarma, Dawn Drain, Deep Ganguli, Zac Hatfield-Dodds, Danny Hernandez, Andy Jones, Jackson Kernion, Liane Lovitt, Kamal Ndousse, Dario Amodei, Tom Brown, Jack Clark, Jared Kaplan, Sam McCandlish, Chris Olah"
published: "Transformer Circuits Thread, Anthropic, 2021"
tags:
  - "interpretabilidad-mecanística"
  - "circuitos"
  - "transformers"
  - "residual-stream"
  - "composición-de-cabezas"
status:
  - "Pendiente"
image: "imgs/2021_elhage_transformer-circuits.png"
image_caption: "El residual stream (arriba) y cómo cada capa de atención lee del stream y escribe de vuelta en él. Las flechas muestran los circuitos de composición entre capas."
opinion: "<WIP>"
---

## Qué hace

Establece el **formalismo matemático del residual stream** para analizar transformers de forma mecanística: cada capa del transformer escribe en un stream residual compartido, y las distintas capas (atención y FFN) pueden analizarse como operaciones independientes que leen y escriben en ese stream. Este framework convierte el análisis de transformers en un ejercicio de álgebra lineal sobre el espacio de activaciones, eliminando la necesidad de "abrir la caja negra" de forma empírica.

El paper introduce conceptos que se convierten en estándar del campo: **circuitos**, **composición de cabezas** (Q-K composition, Q-V composition, K-V composition), **cabezas de atención de cero capa**, y la noción de que las cabezas de atención pueden analizarse como productos de matrices OV (Output-Value) y QK (Query-Key) independientes del embedding.


---

## Metodología

El insight central es la **decomposición del residual stream**: en un transformer, cada capa suma su output al residual stream en lugar de reemplazarlo. Esto significa que la salida final es literalmente la suma de las contribuciones de todas las capas. Formalmente:

- El residual stream x se actualiza como: x ← x + attn(x) + ffn(x) en cada capa.
- Cada cabeza de atención puede escribirse como (OV)(QK): una matriz OV que transforma qué información se copia de posiciones fuente, y una matriz QK que determina de qué posiciones se copia.

Esto permite analizar **circuitos**: subgrafos del modelo donde ciertas cabezas de atención componen sus matrices con las de otras cabezas en capas posteriores para implementar comportamientos concretos.

El paper demuestra este framework analizando transformers de 0, 1 y 2 capas, derivando analíticamente qué función implementan y verificándolo empíricamente. Para 2 capas, descubre los **induction heads**: cabezas que implementan copia de contexto (si la secuencia [A][B] apareció antes, predicen [B] después de ver [A] nuevamente).

---

## Datasets utilizados

- Transformers de lenguaje pequeños entrenados desde cero (0-2 capas) sobre texto de internet.
- El análisis es principalmente analítico/matemático, con verificación empírica sobre modelos entrenados.

---

## Ejemplo ilustrativo

En un transformer de 2 capas, una *induction head* implementa el siguiente circuito: la cabeza H1 en la capa 1 copia el token anterior al token actual en el residual stream (cabeza de "previous token"). La cabeza H2 en la capa 2 usa esa información para buscar en el contexto el mismo patrón. Resultado: si la secuencia *"Harry Potter"* apareció en el contexto, el modelo predice correctamente *"Potter"* cuando ve *"Harry"* por segunda vez. El framework permite derivar esto matemáticamente de las matrices QK y OV sin necesidad de experimentos de activación patching.

---

## Resultados principales

- El formalismo del residual stream permite analizar transformers de forma exacta en modelos pequeños.
- Se descubren los **induction heads** como mecanismo universal del aprendizaje en contexto (in-context learning) — resultado que Olsson et al. (2022) luego verifican a gran escala.
- La descomposición QK/OV permite identificar qué información "fluye" entre capas sin necesidad de experimentos de intervención.
- El paper establece el vocabulario estándar (circuito, cabeza de composición, residual stream, logit lens) que toda la interpretabilidad mecanística posterior adopta.

---

## Ventajas respecto a trabajos anteriores

- Antes de este trabajo, el análisis interno de transformers dependía de sondas (*probing*) o de experimentos de ablación empíricos. Este paper provee un formalismo matemático exacto que permite derivar el comportamiento del modelo a priori.
- La decomposición en circuitos permite analizar modelos grandes enfocándose en subsistemas relevantes, en lugar de tener que entender todos los pesos.
- El paper provee las herramientas para que toda la línea de trabajo de interpretabilidad mecanística (IOI, ACDC, Greater-Than, path patching) exista.

---

## Trabajos previos relacionados

El paper conecta dos tradiciones: el análisis de circuitos en redes de visión y la interpretación de transformers mediante análisis de representaciones.

- **Olah et al. (2020) — [Zoom In: An Introduction to Circuits](2020_olah_zoom-in-circuits.html)**: introduce el paradigma de circuitos para redes de visión; Elhage et al. trasladan este paradigma a transformers.
- **Wang et al. (2022) — [IOI Circuit](2022_wang_ioi-circuit.html)**: primer paper que aplica el framework de Elhage et al. para reverse-engineer un circuito complejo en GPT-2.
- **Conmy et al. (2023) — [ACDC](2023_conmy_automated-circuit-discovery.html)**: automatiza el descubrimiento de circuitos usando el formalismo de Elhage et al.
- **Meng et al. (2022) — ROME**: usa el mismo formalismo para localizar y editar conocimiento factual en las capas FFN.

## Tags

`interpretabilidad-mecanística` `circuitos` `transformers` `residual-stream` `composición-de-cabezas` `induction-heads`
