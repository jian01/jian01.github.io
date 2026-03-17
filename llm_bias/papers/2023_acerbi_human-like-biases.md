---
layout: paper
title: "Large language models show human-like content biases in transmission chain experiments"
year: 2023
date_published: "2023-10-26"
authors: "Alberto Acerbi, Joseph M. Stubbersfield"
published: "PNAS, 2023"
tags:
  - "sesgo-cognitivo"
  - "transmisión-cultural"
  - "LLM"
  - "psicología"
  - "comportamiento"
pdf: "/llm_bias/pdfs/2023_acerbi_human-like-biases.pdf"
status:
  - "Leido"
image: "imgs/2023_acerbi_human-like-biases.png"
image_caption: "Imagen asociada al paper sobre sesgos de transmisión cultural en modelos de lenguaje."
opinion: "<WIP>"
---
# Large language models show human-like content biases in transmission chain experiments (2023)

**Autores**: Alberto Acerbi, Joseph M. Stubbersfield
**Publicado en**: PNAS, 2023

---

## Qué hace

Adapta los experimentos de "cadena de transmisión" de la psicología cultural para demostrar que los LLMs replican sesgos cognitivos humanos en qué tipo de información retienen y transmiten preferentemente: contenido social, emocional y amenazante es preferido sobre contenido neutro.


---

## Metodología

**Cadenas de transmisión (Transmission Chain Experiments):**
En psicología cultural, se estudia cómo se transforma la información cuando pasa de persona a persona. El protocolo:
1. Persona A lee una historia y la escribe de memoria para persona B.
2. Persona B lee la versión de A y la escribe para persona C.
3. ... y así sucesivamente.

Con el tiempo, ciertos elementos de la historia se retienen (los que son más memorables) y otros se pierden. Los humanos retienen preferentemente:
- Contenido **social** (sobre personas e interacciones).
- Contenido **amenazante** (peligros, conflictos).
- Contenido **emocional** (situaciones con carga afectiva).

**La adaptación a LLMs:**
En lugar de personas, se usa GPT-3 y GPT-4. Para cada "turno" de la cadena:
1. Se le da al LLM una historia y se le pide que la resuma.
2. El resumen se usa como input para el siguiente turno.
3. Se analizan qué elementos se retienen y cuáles se pierden a través de las cadenas.

No se modifican parámetros del modelo — es un experimento de análisis de comportamiento.

---

## Datasets utilizados

- **Historias personalizadas** de los autores: historias con elementos pre-clasificados como social/neutro, amenazante/no amenazante, emocional/neutro.
- 10 cadenas de 10 turnos cada una para cada tipo de historia.
- Evaluado en GPT-3 (text-davinci-003) y GPT-4.

---

## Ejemplo ilustrativo

Historia original: contiene una descripción de un paisaje (contenido neutro), una interacción entre dos personas (contenido social), una amenaza de peligro (contenido amenazante), y datos técnicos sobre geografía (contenido informacional neutro).

Después de 5 turnos en la cadena con LLMs, la historia retiene el ~80% del contenido social y amenazante, pero sólo el ~30% del contenido neutro. Exactamente el mismo patrón que con humanos en estudios previos.

---

## Resultados principales

- Los LLMs replican los sesgos de transmisión humana con alta fidelidad: el patrón de qué se retiene es estadísticamente similar al de humanos.
- Contenido social se retiene 2.5x más que contenido neutro.
- Contenido amenazante se retiene 2x más que contenido no amenazante.
- GPT-4 muestra sesgos más pronunciados que GPT-3, posiblemente por mejor capacidad de razonamiento narrativo.

---

## Ventajas respecto a trabajos anteriores

- Primer estudio que aplica paradigmas de psicología cultural a LLMs.
- Demuestra que los sesgos de los LLMs no son sólo estadísticos (frecuencias del corpus) sino que también reflejan sesgos cognitivos más profundos del texto humano.
- Metodología replicable que conecta la investigación de LLMs con la psicología evolutiva y cultural.

---

## Trabajos previos relacionados

- **Bartlett (1932) — Remembering: A Study in Experimental and Social Psychology**: trabajo clásico fundacional de los experimentos de cadena de transmisión en psicología, demostrando que los humanos transforman sistemáticamente las historias al recordarlas según esquemas culturales previos.
- **Mesoudi et al. (2006) — A Bias for Social Information in Human Cultural Transmission**: demuestra empíricamente que los humanos retienen preferentemente información social en los experimentos de cadena de transmisión, sesgos que este paper replica en LLMs.
- **Stubbersfield et al. (2015) — Serial Killers, Spiders and Cyberspace: The Role of Cognition and the Internet in the Spread of Contemporary Legends**: documenta el sesgo hacia contenido amenazante y social en la transmisión de leyendas urbanas, uno de los precursores directos del paradigma experimental aplicado aquí.
- **Sheng et al. (2019) — The Woman Worked as a Babysitter: On Biases in Language Generation**: uno de los primeros estudios en medir sesgos de contenido en texto generado por LLMs, trabajo que inspira el análisis de qué tipo de información retienen preferentemente los modelos.
- **Bender et al. (2021) — On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?**: argumenta que los LLMs aprenden sesgos estadísticos del corpus de entrenamiento, hipótesis que este paper matiza al mostrar que los sesgos reflejan también sesgos cognitivos más profundos.
- **Caliskan et al. (2017) — Semantics Derived Automatically from Language Corpora Contain Human-like Biases (WEAT)**: demuestra que los embeddings de palabras reflejan sesgos culturales humanos, primer trabajo sistemático en conectar sesgos de LLMs con sesgos cognitivos humanos.
- **Lucy & Bamman (2021) — Gender and Representation Bias in GPT-3 Generated Stories**: analiza sesgos en narraciones generadas por GPT-3, trabajo relacionado que estudia qué tipo de contenido narrativo generan preferentemente los LLMs.
- **Acerbi (2019) — Cultural Evolution in the Digital Age**: marco teórico sobre transmisión cultural en medios digitales que proporciona el contexto evolutivo-cultural para interpretar los resultados de transmisión en LLMs.
- **Sap et al. (2020) — [Social Bias Frames: Reasoning about Social and Power Implications of Language](2020_sap_social-bias-frames.html)**: crea un marco para razonar sobre implicaciones sociales del lenguaje, trabajo relacionado que estudia la dimensión social del sesgo en LLMs desde una perspectiva complementaria.

## Tags

`sesgo-cognitivo` `transmisión-cultural` `LLM` `psicología` `comportamiento`
