---
layout: paper
title: "Language Models Can Explain Neurons in Language Models"
year: 2023
date_published: "2023-05-09"
authors: "Steven Bills, Nick Cammarata, Dan Mossing, Henk Tillman, Leo Gao, Gabriel Goh, Ilya Sutskever, Jan Leike, Jeff Wu, William Saunders"
published: "OpenAI Technical Report, 2023"
tags:
  - "interpretabilidad-mecanística"
  - "neuronas"
  - "explicaciones-automáticas"
  - "GPT-4"
  - "GPT-2"
status:
  - "Pendiente"
image: "imgs/2023_bills_neuron-explanation.png"
image_caption: "Pipeline de tres pasos: (1) GPT-4 observa los tokens que activan la neurona y genera una explicación, (2) GPT-4 simula las activaciones predichas, (3) se calcula la correlación entre activaciones reales y simuladas como puntuación de la explicación."
opinion: "<WIP>"
---
# Language Models Can Explain Neurons in Language Models (2023)

**Autores**: Steven Bills, Nick Cammarata, Dan Mossing, Henk Tillman, Leo Gao, Gabriel Goh, Ilya Sutskever, Jan Leike, Jeff Wu, William Saunders (OpenAI)
**Publicado en**: OpenAI Technical Report, 2023

---

## Qué hace

Propone el **primer sistema automatizado para generar explicaciones en lenguaje natural de neuronas individuales en modelos de lenguaje**, usando GPT-4 como "explicador". El sistema examina los tokens que más activan cada neurona de GPT-2 (el modelo objetivo), genera una hipótesis en lenguaje natural sobre qué concepto representa esa neurona, y luego verifica la hipótesis usando GPT-4 como simulador de las activaciones.

El resultado es un pipeline escalable que puede generar explicaciones para todas las ~300,000 neuronas de GPT-2, convirtiendo la interpretación manual de neuronas (que tarda horas por neurona) en un proceso automático.


---

## Metodología

El pipeline tiene tres etapas:

**1. Recolección de ejemplos de activación**:
Para cada neurona n de GPT-2, se recopilan los tokens del dataset que producen las activaciones más altas (top-k activations). Se incluyen los tokens con activación máxima y también el contexto en que aparecen.

**2. Generación de explicación (GPT-4 como explicador)**:
Se le muestra a GPT-4 los top tokens y sus contextos con un prompt del tipo: *"Aquí están los tokens que más activan una neurona. ¿Qué concepto o patrón crees que representa esta neurona?"*. GPT-4 genera una hipótesis en lenguaje natural, por ejemplo: *"Esta neurona se activa ante tokens relacionados con deportes acuáticos"*.

**3. Verificación y puntuación (GPT-4 como simulador)**:
Para evaluar la calidad de la explicación, se le pide a GPT-4 que, dado el texto de la explicación, simule qué tokens activarían la neurona. Se calcula la correlación entre las activaciones simuladas y las activaciones reales del modelo como *explanation score*.

Las explicaciones con score alto son candidatas a ser correctas; las con score bajo o negativo indican que la explicación no captura bien el comportamiento de la neurona.

---

## Datasets utilizados

- **GPT-2 XL** (1.5B parámetros): modelo objetivo cuyas neuronas se analizan.
- **GPT-4**: modelo usado como explicador y simulador.
- **WebText**: corpus de preentrenamiento de GPT-2, usado para recopilar activaciones.
- Se generan explicaciones para ~300,000 neuronas en las capas FFN de GPT-2 XL.

---

## Ejemplo ilustrativo

Neurona #4840 de GPT-2 XL: sus top tokens incluyen *"swimming", "diving", "surfing", "kayaking", "paddling"*. GPT-4 genera la explicación: *"Esta neurona se activa ante palabras relacionadas con deportes acuáticos"*. Para verificar, GPT-4 predice que la neurona debería activarse ante *"rowing"*, *"snorkeling"* y *"wakeboarding"* pero no ante *"running"* o *"cycling"*. La correlación entre estas predicciones y las activaciones reales de la neurona es 0.82 — una explicación de alta calidad.

Neurona #12043: top tokens son *"the", "a", "an", "this"*. GPT-4 genera: *"artículos determinantes e indeterminantes"*. Pero al verificar, la correlación es 0.21 — la explicación es superficialmente correcta pero no captura el verdadero patrón funcional de la neurona.

---

## Resultados principales

- El **score promedio de explicación** sobre todas las neuronas de GPT-2 XL es ~0.1 (en una escala de -1 a 1), lo que sugiere que la mayoría de las explicaciones actuales son poco informativas.
- Aproximadamente el 1-2% de las neuronas tienen scores >0.5, indicando que solo una minoría son bien explicables con el método actual.
- Las neuronas más explicables tienden a estar en las primeras capas y a responder a patrones sintácticos simples.
- Las neuronas de capas medias y profundas son mucho más difíciles de explicar, sugiriendo que representan conceptos más abstractos o policémicos.
- El sistema puede escalar a modelos más grandes en principio, aunque el costo computacional de GPT-4 lo limita.

---

## Ventajas respecto a trabajos anteriores

- La interpretación manual de neuronas (Olah et al. 2020 para visión) no escala: cada neurona requiere horas de trabajo humano. Este sistema reduce el costo a segundos por neurona.
- A diferencia de los métodos de probing (que entrenan clasificadores externos), este método no requiere datos etiquetados ni diseño de sondas — la explicación emerge directamente del LLM.
- El uso de GPT-4 como "simulador" para verificar hipótesis es una contribución metodológica: en lugar de tests empíricos costosos, se usa el LLM para predecir activaciones.
- Es el punto de partida para la línea de **interpretabilidad automática** (*automated interpretability*) que prolifera en 2023-2025.

---

## Trabajos previos relacionados

- **Olah et al. (2020) — [Zoom In: An Introduction to Circuits](2020_olah_zoom-in-circuits.html)**: análisis manual de circuitos en redes de visión; Bills et al. automatizan el equivalente para LMs.
- **Elhage et al. (2021) — [A Mathematical Framework for Transformer Circuits](2021_elhage_transformer-circuits.html)**: provee el formalismo para entender qué hacen las neuronas FFN como memorias clave-valor.
- **Conmy et al. (2023) — [ACDC](2023_conmy_automated-circuit-discovery.html)**: automatiza el descubrimiento de circuitos; Bills et al. automatizan la interpretación de componentes individuales dentro de esos circuitos.
- **Geva et al. (2021) — Transformer Feed-Forward Layers as Key-Value Memories**: interpreta las neuronas FFN como memorias factuales; Bills et al. generalizan esta interpretación a cualquier tipo de neurona.

## Tags

`interpretabilidad-mecanística` `neuronas` `explicaciones-automáticas` `GPT-4` `GPT-2` `automated-interpretability`
