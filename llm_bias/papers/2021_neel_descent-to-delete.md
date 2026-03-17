---
layout: paper
title: "Descent-to-Delete: Gradient-Based Methods for Machine Unlearning"
year: 2021
date_published: "2020-07-06"
authors: "Seth Neel, Aaron Roth, Saeed Sharifi-Malvajerdi"
published: "Algorithmic Learning Theory (ALT), 2021"
tags:
  - "machine-unlearning"
  - "unlearning-aproximado"
  - "gradiente"
  - "privacidad"
  - "modelos-convexos"
pdf: "/llm_bias/pdfs/2021_neel_descent-to-delete.pdf"
method_type: "Reentrenamiento exacto"
status:
  - "Pendiente"
image: "imgs/2021_neel_descent-to-delete.png"
image_caption: "Esquema del proceso de unlearning mediante descenso de gradiente perturbado: el modelo se actualiza con ruido calibrado para garantizar indistinguibilidad estadística tras el borrado."
opinion: "<WIP>"
---## Qué hace

Propone el primer framework de **unlearning aproximado basado en gradientes** para modelos convexos que puede manejar una secuencia arbitrariamente larga de solicitudes de borrado adversariales. El objetivo es que, tras borrar un punto, el estado interno del optimizador (no solo las predicciones del modelo) sea estadísticamente indistinguible del estado que habría resultado de nunca haber entrenado con ese punto.

El paper distingue dos nociones de garantía: **full-state indistinguishability** (el estado completo del optimizador es indistinguible) y **output indistinguishability** (solo las predicciones son indistinguibles). La segunda es más débil pero permite algoritmos más eficientes.


---

## Metodología

El método central es el **Perturbed Gradient Descent (PGD)**: cuando se solicita borrar un punto de entrenamiento, en lugar de reentrenar desde cero, se continúa el descenso de gradiente añadiendo ruido gaussiano calibrado para "enmascarar" la influencia del punto borrado.

La intuición es que el descenso de gradiente con ruido suficiente converge a una distribución sobre parámetros que es indistinguible de la distribución que habría resultado de entrenar sin ese punto. El ruido necesario se calibra en función de la *sensibilidad* de la función de pérdida (cuánto cambia el óptimo al añadir/quitar un punto).

Para manejar secuencias largas de borrados, el paper introduce **Perturbed Distributed Descent**: mantiene múltiples copias del modelo (basado en reservoir sampling) para garantizar que el costo por borrado no crezca con el número de borrados previos.

Las garantías se establecen bajo condiciones de convexidad fuerte de la función de pérdida, como en modelos de regresión logística o SVM.

---

## Datasets utilizados

El paper es fundamentalmente teórico. Los experimentos de validación empírica utilizan:
- Datasets sintéticos de regresión logística.
- MNIST para clasificación binaria con modelos convexos.

---

## Ejemplo ilustrativo

Un banco entrena un modelo de regresión logística con 100,000 solicitudes de crédito. El cliente #5,000 ejerce su derecho al olvido. El reentrenamiento desde cero tarda 30 minutos. Con Descent-to-Delete: se calcula el gradiente del punto borrado, se aplica una actualización de gradiente en dirección contraria al punto borrado, y se añade ruido gaussiano calibrado. El proceso tarda segundos y produce un modelo estadísticamente indistinguible del que habría resultado de nunca haber entrenado con ese cliente.

---

## Resultados principales

- Los algoritmos propuestos son los primeros que garantizan tanto **tiempo de borrado** como **error en estado estacionario** que no crecen con la longitud de la secuencia de borrados.
- Bajo la condición de fuerte convexidad, el costo computacional por borrado es O(d) donde d es la dimensión del modelo, comparado con O(nd) del reentrenamiento.
- La versión de output-only indistinguishability requiere un factor de ruido significativamente menor que la versión full-state.

---

## Ventajas respecto a trabajos anteriores

- Es el primer trabajo en garantizar que el costo por borrado no se degrada con secuencias largas de borrados (problema de "no amortización" de métodos anteriores).
- Distingue formalmente entre dos niveles de garantía (full-state vs. output), permitiendo elegir el nivel de privacidad apropiado para cada aplicación.
- A diferencia de [SISA (Bourtoule et al., 2021)](2021_bourtoule_sisa.html), no requiere modificar el proceso de entrenamiento original ni mantener múltiples modelos por defecto.

---

## Trabajos previos relacionados

- **Cao & Yang (2015) — [Towards Making Systems Forget with Machine Unlearning](2015_cao_machine-unlearning.html)**: trabajo fundacional del unlearning; Descent-to-Delete extiende sus garantías a modelos entrenados con SGD.
- **Bourtoule et al. (2021) — [Machine Unlearning via SISA](2021_bourtoule_sisa.html)**: el enfoque complementario de exact unlearning mediante particionamiento; Descent-to-Delete es la alternativa post-hoc basada en gradientes.
- **Dwork et al. (2006) — Differential Privacy**: el ruido gaussiano utilizado en PGD es directamente análogo al mecanismo gaussiano de la privacidad diferencial.
- **Guo et al. (2020) — Certified Data Removal from Machine Learning Models**: trabajo contemporáneo de unlearning certificado; Descent-to-Delete proporciona garantías más fuertes sobre el estado completo del optimizador.

## Tags

`machine-unlearning` `unlearning-aproximado` `gradiente` `privacidad` `modelos-convexos` `garantías-formales`
