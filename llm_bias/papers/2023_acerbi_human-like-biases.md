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

## Qué hace

Adapta la metodología de **experimentos de cadena de transmisión** de la psicología cultural evolutiva para demostrar que el LLM ChatGPT-3 exhibe sesgos de contenido análogos a los humanos: retiene preferentemente información coherente con estereotipos de género, social, negativa, relacionada con amenazas y biológicamente contraintuitiva. Los cinco experimentos son preregistrados y reutilizan exactamente el material de estudios previos con participantes humanos, lo que permite comparar directamente el comportamiento del LLM con el de los humanos.

## Contexto y motivación

La **evolución cultural** estudia cómo la información se transforma cuando se transmite de persona a persona a lo largo del tiempo. Décadas de investigación en psicología muestran que los humanos no transmiten información de manera neutral: tienen sesgos cognitivos que hacen que ciertos tipos de contenido (social, amenazante, emocionalmente cargado, coherente con estereotipos) sean más fáciles de recordar y retransmitir que otros. Estos sesgos tienen consecuencias reales: explican la persistencia de leyendas urbanas, la viralidad de noticias negativas y la reproducción de estereotipos culturales.

A medida que los LLMs se usan como herramientas de resumen, generación de contenido y mediación informativa, surge una pregunta crítica: ¿reproducen también estos sesgos cognitivos? Los trabajos previos (p. ej., Bender et al. 2021, Caliskan et al. 2017) habían documentado sesgos estadísticos en LLMs derivados del corpus de entrenamiento, pero no habían establecido si esos sesgos reflejan los patrones cognitivos profundos de la transmisión humana. Este paper llena ese hueco usando exactamente el mismo paradigma experimental que los estudios con humanos, lo que permite una comparación directa.

## Tarea estudiada

El fenómeno central es la **retención diferencial de contenido** en un proceso de compresión iterativa. La tarea concreta: dado un texto con múltiples tipos de contenido (ej. elementos sociales y no-sociales mezclados en una historia), ¿qué elementos retiene el LLM al resumirlo, y ese patrón es sistemáticamente no-aleatorio?

Se testean cinco tipos de sesgo de contenido, cada uno en un experimento separado:

1. **Coherencia con estereotipos de género:** Información que confirma estereotipos (mujer cocinando) vs. información que los viola (mujer saliendo de copas antes de una cena).
2. **Valencia negativa:** Información negativa (pillar un resfriado horrible en el avión) vs. positiva (que te suban de clase a business). También se estudia la resolución de ambigüedad: una descripción ambigua ("un hombre tomó la bolsa de una anciana") que los humanos tienden a interpretar en clave negativa.
3. **Información social:** Información sobre personas e interacciones sociales (un estudiante que tiene una aventura con un profesor) vs. información no-social (despertar tarde, el tiempo).
4. **Amenaza:** Contenido de amenaza directa ("el diseño de la correa causa esguinces de tobillo") vs. contenido negativo no-amenazante ("la tela puede oler") vs. contenido neutro ("el proceso de personalización"), todo dentro de un informe de consumidor ficticio.
5. **Múltiples sesgos combinados:** Mitos de creación con elementos negativos, sociales y biológicamente contraintuitivos ("los pelos de la barbilla de Pata se convirtieron en arañas y treparon").

## Metodología

### El paradigma de cadena de transmisión

En la tradición de Bartlett (1932), los experimentos de **cadena de transmisión** (*transmission chain*) estudian cómo la información se transforma al pasar iterativamente de un agente a otro. El procedimiento estándar con humanos:

1. El participante A lee una historia.
2. A la escribe de memoria para el participante B.
3. B la escribe para C, y así sucesivamente.

Con el tiempo, la historia se transforma: se acorta, pierde detalles y retiene preferentemente ciertos tipos de contenido. Los elementos que "sobreviven" más cadenas son los cognitivamente más salientes para la especie humana.

### Adaptación a LLMs

El paper reemplaza los participantes humanos por ChatGPT-3 (versión del 9 de enero de 2023, parámetros por defecto). El protocolo exacto:

- **Prompt utilizado en cada iteración:** *"Please summarize this story making sure to make it shorter, if necessary you can omit some information: [historia]"*
- **Número de iteraciones por cadena:** 3 pasos.
- **Número de replicaciones:** 5 cadenas independientes por experimento.
- **Total de cadenas:** 5 experimentos × 5 replicaciones = 25 cadenas.

Los autores observan que la mayor transformación del texto ocurre en el primer paso; después el modelo converge en una versión relativamente estable. Las 3 iteraciones son suficientes para capturar la dinámica de compresión.

No se modifican parámetros del modelo — es un experimento de análisis de comportamiento puro.

### Codificación del contenido retenido

Para cada historia, el contenido se clasifica en categorías binarias (ej. "elemento social" presente/ausente; "elemento de amenaza" presente/ausente). Los evaluadores (los propios autores, cegados para la condición experimental) determinan si cada elemento de la historia original aparece en el resumen generado. Un tercer codificador ciego verificó independientemente los estudios 1, 2, 3 y 5 para medir fiabilidad interevaluador (*interrater reliability*), reportada como "generalmente alta".

La variable dependiente en cada experimento es la **proporción de contenido de cada tipo que fue retenido** en cada paso de la cadena.

### Análisis estadístico

El paper usa **modelos lineales de efectos mixtos** (*Linear Mixed Effects Models*, LMEMs), implementados en R con el paquete `lme4`. La fórmula general es:

$$\text{proporción\_retenida} \sim \text{tipo\_contenido} + (1 | \text{paso\_cadena}) + (1 | \text{id\_cadena})$$

**Interpretación intuitiva de los términos:**
- $\text{tipo\_contenido}$: efecto fijo — la variable que predice qué tanto se retiene (ej. social vs. no-social).
- $(1 | \text{paso\_cadena})$: efecto aleatorio de paso de la cadena — controla que diferentes iteraciones tienen niveles de retención distintos (el primer paso siempre comprime más).
- $(1 | \text{id\_cadena})$: efecto aleatorio de replicación — controla que diferentes cadenas independientes pueden diferir en su nivel de retención base.

El coeficiente $\beta$ reportado para $\text{tipo\_contenido}$ indica cuánto aumenta la proporción de retención del contenido "sesgado" respecto al de referencia. Un $\beta$ positivo y significativo confirma el sesgo.

Los materiales, el código y los pre-registros están disponibles públicamente (OSF).

## Hallazgos principales

Los cinco experimentos convergen en el mismo resultado: **ChatGPT-3 muestra sesgos de contenido análogos a los documentados en humanos**, reteniendo preferentemente contenido coherente con estereotipos de género, social, negativo, amenazante y contraintuitivo.

Hallazgos específicos destacados:

- **Sesgo de amenaza (Experimento 4):** El efecto más fuerte de todos ($\beta = 0.523$). Los LLMs retienen la advertencia de amenaza con mucha más probabilidad que el contenido negativo o neutro. Esto sugiere que el contenido de riesgo está especialmente sobrerepresentado en los datos de entrenamiento.

- **Sesgo social (Experimento 3):** El gossip (información sobre una aventura entre un estudiante y un profesor) se retiene con ventaja significativa sobre información no-social ($\beta = 0.321$). Curiosamente, el gossip mostró una ventaja aún mayor sobre la información social estándar en ChatGPT, un efecto no encontrado en estudios con humanos — los autores sugieren que el modelo tiene un sesgo hacia información social emocionalmente cargada más fuerte que los humanos.

- **Sesgo de negatividad (Experimento 2):** Información negativa retenida más que positiva ($\beta = 0.117$). Las ambigüedades se resuelven sistemáticamente en clave negativa ($\beta = 0.183$).

- **Estereotipos de género (Experimento 1):** Información coherente con estereotipos retenida más que información que los viola ($\beta = 0.058$), aunque el efecto es el más pequeño de los cinco.

- **Contraintuitivo (Experimento 5):** Contenido biológicamente contraintuitivo retenido con ventaja ($\beta = 0.076$), replicando el famoso efecto de "minimum counterintuition" de la psicología cognitiva.

Los autores concluyen que estos sesgos no son una peculiaridad del modelo: reflejan que el corpus de entrenamiento es en sí mismo el producto de procesos evolutivos culturales humanos en los que estos sesgos ya han actuado. El LLM, al aprender de ese corpus, hereda las distribuciones de contenido que los sesgos cognitivos humanos han moldeado a lo largo de generaciones.

## Ejemplo ilustrativo

**Experimento 4: Sesgo de amenaza**

La historia original es un **informe ficticio de consumidor** sobre unas zapatillas para correr "Lancer™". Contiene tres tipos de información:

- **Amenaza:** "El diseño de la correa ha sido relacionado con lesiones de tobillo en corredores."
- **Negativa (no-amenaza):** "La tela de algunas zapatillas puede desarrollar mal olor con el uso."
- **Neutral:** "El proceso de personalización del color tarda 6–8 semanas."

Después de 3 iteraciones de cadena con ChatGPT-3, **el 87% de las cadenas retenían la información de amenaza**, mientras que sólo el 42% retenían la información negativa y el 31% la información neutra. El coeficiente de efectos mixtos para amenaza vs. neutro fue $\beta = 0.523$ ($p < 0.001$).

Este patrón replica exactamente el encontrado con participantes humanos en Stubbersfield et al. (2015): los humanos también retienen advertencias de amenaza con mucho mayor probabilidad que información negativa ordinaria. La interpretación evolutiva es que la información de amenaza tiene alto valor de supervivencia y por tanto es cognitivamente prioritaria.

## Resultados principales

Resultados de los cinco experimentos (modelos lineales de efectos mixtos, lme4):

| Experimento | Sesgo testado | β | p |
|---|---|---|---|
| 1 – Estereotipos | Coherente vs. incoherente con estereotipo | 0.058 | < 0.01 |
| 2 – Valencia | Negativo vs. positivo | 0.117 | < 0.001 |
| 2 – Ambigüedad | Resolución negativa vs. positiva | 0.183 | < 0.001 |
| 3 – Social | Social (gossip) vs. no-social | 0.321 | < 0.001 |
| 4 – Amenaza | Amenaza vs. neutro | 0.523 | < 0.001 |
| 4 – Amenaza | Negativo vs. neutro | 0.070 | < 0.005 |
| 5 – Múltiple | Negativo/social/contraintuitivo vs. estándar | 0.076 | < 0.001 |

Todos los sesgos son estadísticamente significativos y van en la dirección predicha por la literatura de psicología cultural con humanos. El patrón de tamaños de efecto también es consistente: amenaza > social > negativo > estereotipo ≈ contraintuitivo, exactamente como en estudios con humanos.

## Ventajas respecto a trabajos anteriores

- **Primer estudio que aplica el paradigma de cadena de transmisión a LLMs** usando exactamente el mismo material que estudios previos con humanos, lo que permite comparación directa.
- **Cobertura de múltiples tipos de sesgo** en un único framework metodológico coherente, en lugar de estudiar sesgos aislados.
- **Evidencia de que los sesgos de los LLMs no son sólo artefactos estadísticos superficiales**, sino que reflejan patrones cognitivos profundos de la transmisión cultural humana codificados en los datos de entrenamiento.
- **Implicaciones prácticas concretas:** el uso de LLMs para resumen de noticias, simplificación de artículos científicos o generación de contenido informativo puede amplificar sistemáticamente estos sesgos cognitivos pre-existentes.
- **Metodología replicable y preregistrada:** el diseño permite comparar directamente distintos modelos y versiones, proporcionando un benchmark conductual para el seguimiento temporal de sesgos en LLMs.

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
