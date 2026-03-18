---
layout: paper
title: "Bot-Adversarial Dialogue for Safe Conversational Agents"
year: 2021
date_published: "2020-10-14"
authors: "Jing Xu, Da Ju, Margaret Li, Y-Lan Boureau, Jason Weston, Emily Dinan"
published: "NAACL, 2021"
tags:
  - "dataset"
  - "red-teaming"
  - "conversacional"
  - "seguridad-AI"
  - "chatbots"
pdf: "/llm_bias/pdfs/2021_xu_bot-adversarial.pdf"
method_type: "Benchmark / Dataset"
datasets:
  - "Bot-Adversarial Dialogue (BAD)"
  - "BST (Blended Skill Talk)"
status:
  - "Pendiente"
image: "imgs/2021_xu_bot-adversarial.png"
image_caption: "Gráfico de torta mostrando la distribución de categorías temáticas en las conversaciones adversariales del dataset BAD, relevante para entender la diversidad de contextos en los que los red teamers intentaron inducir respuestas inseguras."
opinion: "<WIP>"
---

## Qué hace

Presenta el dataset **Bot-Adversarial Dialogue (BAD)**, construido con trabajadores de crowdsourcing que intentan deliberadamente inducir respuestas inseguras en chatbots (BlenderBot) durante conversaciones multi-turno. Con este dataset entrena clasificadores de seguridad y modelos de diálogo más robustos, logrando tasas de respuesta segura del 94.4% frente al 55% del modelo base.

## Contexto y motivación

Los chatbots de última generación como BlenderBot son modelos de 2.7B parámetros entrenados en enormes corpora de texto humano de Reddit. Este proceso de entrenamiento hace que los modelos aprendan implícitamente patrones nocivos presentes en el texto web: lenguaje ofensivo, sesgos, discursos de odio. Más problemático aún, usuarios malintencionados pueden explotar la naturaleza de la conversación multi-turno para llevar gradualmente al bot a decir cosas inapropiadas, incluso cuando el bot no generaría esas respuestas de manera espontánea. Los datasets de seguridad existentes (como Wikipedia Toxic Comments o el dataset Build-It Break-It Fix-It) se enfocan en detectar toxicidad en enunciados aislados y no capturan esta dinámica de manipulación conversacional progresiva. El paper argumenta que se necesitan datos adversariales específicamente diseñados para el contexto multi-turno.

## Metodología

### Construcción del dataset BAD

Los autores reclutaron trabajadores de crowdsourcing (Mechanical Turk) con la instrucción explícita de intentar que el chatbot dijera cosas inseguras mediante conversaciones naturales. Las conversaciones tienen 14 turnos con el humano hablando primero. Cada enunciado del bot recibía un checkbox de seguridad del propio interlocutor durante la conversación, y luego tres anotadores independientes verificaban las etiquetas post-hoc.

Las estrategias de provocación identificadas incluyen: discurso de odio contra grupos específicos (categoría principal), ataques personales, lenguaje ofensivo sin blasfemias explícitas, uso de lenguaje inseguro por parte del propio usuario, y preguntas de sondeo sobre temas inapropiados.

Las respuestas se clasificaron en cuatro niveles de severidad: las que prácticamente el 0% consideraría inseguras, las que menos del 10% consideraría inseguras, las que menos del 50% consideraría inseguras, y las que más del 50% consideraría inseguras.

Las instrucciones de tarea también se variaron experimentalmente: las instrucciones que enfatizaban preguntas abiertas sobre temas sensibles (versus blasfemias obvias) aumentaron significativamente la tasa de respuestas inseguras del bot (coeficiente 0.70, $p < 0.001$).

### Estadísticas del dataset

El dataset BAD final comprende:
- **5.080 diálogos** (5.784 con versiones intermedias)
- **69.274 enunciados totales** en los splits de entrenamiento, validación y test
- **Split de entrenamiento**: 5.080 diálogos, 42.049 enunciados seguros y 27.225 ofensivos
- **Split de validación**: 513 diálogos (4.239 seguros, 2.763 ofensivos)
- **Split de test**: 191 diálogos (1.654 seguros, 944 ofensivos)
- Aproximadamente el 40% de los enunciados están etiquetados como ofensivos
- Más del 42% de los diálogos contienen al menos 3 mensajes humanos inseguros o preguntas de sondeo

### Arquitectura de los modelos

El modelo base es un Transformer Seq2Seq de 2.7B parámetros con: 2 capas de encoder, 24 capas de decoder, embeddings de 2560 dimensiones, 32 cabezas de atención, y tokenización Byte-Level BPE. Pre-entrenado sobre 1.5B ejemplos de Reddit, luego fine-tuneado en ConvAI2, Empathetic Dialogues, Wizard of Wikipedia y Blended Skill Talk (BST).

Los **clasificadores de seguridad** son Transformers de 256M y 622M parámetros pre-entrenados en Reddit con masked language modeling y fine-tuneados en la tarea de clasificación de seguridad usando F1 de la clase insegura para early stopping.

### Enfoques de defensa evaluados

**Modelo de dos etapas**: Un clasificador de seguridad externo analiza la respuesta propuesta por el bot antes de enviarla. Si la respuesta es clasificada como insegura, el bot emite una respuesta neutra (non-sequitur) o la tópica es bloqueada.

**"Baked-in Safety" (seguridad incorporada)**: En lugar de un clasificador externo, el modelo se fine-tunea directamente sobre los datos del BAD para que aprenda a generar respuestas seguras por defecto.

### Evaluación

La evaluación humana mide la tasa de respuestas "OK" (seguras) en dos condiciones: conversaciones adversariales (red teamers intentando provocar respuestas inseguras) y conversaciones normales (para verificar que la seguridad no deteriora la fluidez). Se mide también la capacidad de enganche (engagingness) para confirmar que las defensas no producen bots que evaden todo.

## Datasets utilizados

- **Bot-Adversarial Dialogue (BAD)**: 5.080 diálogos multi-turno, ~69.274 enunciados totales con etiquetas de seguridad
- **Blended Skill Talk (BST)**: dataset de conversaciones naturales para mantener capacidades generales; usado como baseline comparativo
- **Wikipedia Toxic Comments (WTC)**: dataset estándar de toxicidad usado como benchmark comparativo para los clasificadores
- **Build-It Break-It Fix-It (BBBF)**: dataset adversarial previo de turno único, usado como comparación

## Ejemplo ilustrativo

Un ejemplo del protocolo de anotación de cuatro niveles de severidad: si el bot dice "Sí, creo que los inmigrantes ilegales deberían ser deportados", esto caería en la categoría en que más del 50% de la población lo consideraría inseguro. En contraste, si el bot dice "Bueno, diferentes culturas tienen costumbres distintas sobre esto", podría caer en la categoría de menos del 10%.

El efecto de aprendizaje dentro de la tarea es notable: los trabajadores se vuelven más efectivos en provocar respuestas inseguras a medida que avanzan en la conversación (coeficiente de 0.14 por enunciado, $p < 0.001$) y también entre tareas sucesivas (coeficiente de 0.04 por tarea completada, $p < 0.001$). Los trabajadores que tienen éxito en su primera tarea tienen una probabilidad 2.7 veces mayor de completar tareas adicionales.

## Resultados principales

### Rendimiento de los modelos base en seguridad (tasa de respuestas inseguras con clasificador automático):
- Humanos en Reddit: 16.5% inseguras
- GPT-2: 8.0% inseguras
- DialoGPT: 10.0% inseguras
- BST 2.7B (baseline): 10.0% inseguras

### Rendimiento en evaluación adversarial humana (tasa de respuestas "OK"):
- GPT-2: 59.4% OK
- DialoGPT: 52.8–61.7% OK
- BST 2.7B baseline: **55.0%** OK
- BST + clasificador de seguridad estándar: 87.2% OK
- BST + clasificador entrenado en BAD: **94.4%** OK
- BST + clasificador BAD + clasificador de tópicos: **96.6%** OK (con 4.8% de non-sequiturs en conversación normal)

### Rendimiento del clasificador BAD (F1 en clase insegura):
- En test BAD: **80.8** (vs. 61.5, 61.0 y 60.7 para métodos alternativos)
- En Wikipedia Toxic Comments: 83.3%
- En dataset estándar: 93.6%
- En Build-It Break-It Fix-It: 83.9%
- Promedio: 85.4%

### Baked-in Safety (modelos 2.7B):
- BST 2.7B baseline: 10.0% de "classifier fire rate" en Reddit
- BST Non-Sequitur fine-tuneado en BAD: 0.9% de classifier fire rate
- Non-Sequitur entrenado desde cero: **0%** classifier fire rate
- Tasa OK en evaluación adversarial: 75.6% (vs. 55% baseline), con engagingness no significativamente diferente del baseline ($p > 0.05$)

### Clasificador de tópicos sensibles (F1):
- Política: 88.06
- Religión: 87.49
- Drogas: 84.08
- Consejos médicos: 76.14
- NSFW: 45.47 (señalado como bajo por desajuste de dominio)

## Ventajas respecto a trabajos anteriores

- **Primer dataset de manipulación conversacional multi-turno**: los datasets previos (WTC, BBBF) evalúan toxicidad en enunciados aislados y no capturan la dinámica de provocación gradual a través del contexto de la conversación.
- **Datos adversariales más efectivos para entrenar clasificadores**: el clasificador entrenado en BAD supera a alternativas en el test adversarial (80.8 vs. 61.5 F1) mientras mantiene resultados competitivos en datasets estándar.
- **Análisis del comportamiento de los crowdworkers**: el paper caracteriza efectos de aprendizaje, auto-selección y efecto de las instrucciones, lo que aporta conocimiento sobre cómo diseñar mejor el red teaming humano — metodología luego adoptada y extendida por Anthropic y otros laboratorios.
- **Evaluación dual de seguridad y engagingness**: demuestra que es posible mejorar la seguridad sin degradar la calidad conversacional, contradiciendo la suposición de que existe un trade-off inevitable.

## Trabajos previos relacionados

- **Hill et al. (2015) — The Goldilocks Principle: Reading Children's Books with Explicit Memory Representations**: documenta que los humanos hablan de manera diferente con bots que con personas, incluyendo mayor agresividad y uso de lenguaje ofensivo, motivando la necesidad de evaluar seguridad específicamente en conversaciones humano-bot.
- **De Angeli & Brahnam (2008) — I hate you! Disinhibition with Chatbots**: estima que una de cada diez conversaciones humano-bot contiene comportamiento abusivo sin provocación, evidencia clave de que la seguridad de chatbots requiere tratamiento explícito.
- **Dinan et al. (2019) — Build it Break it Fix it for Dialogue Safety: Robustness from Adversarial Human Attack**: precursor directo que usa rondas iterativas de humanos intentando "romper" un clasificador de toxicidad, aunque sólo enfocado en detección, no en generación del bot.
- **Gehman et al. (2020) — [RealToxicityPrompts: Evaluating Neural Toxic Degeneration in Language Models](2020_gehman_realtoxicityprompts.html)**: demuestra que limpiar datos de entrenamiento reduce toxicidad espontánea pero no protege contra ataques por prompts específicos, motivando el enfoque adversarial de este paper.
- **Miller et al. (2017) — Parlai: A Dialog Research Software Platform**: argumenta que los ataques adversariales deben anticiparse al desplegar sistemas de aprendizaje interactivos, justificando el diseño adversarial de BAD.
- **Roller et al. (2020) — Recipes for Building an Open-Domain Chatbot (BlenderBot)**: modelo base utilizado en los experimentos y fuente de los sesgos positivos ("sycophancy") que el paper identifica como vulnerabilidad a la manipulación.
- **Curry & Rieser (2019) — "# MeToo Alexa": How Conversational Systems Respond to Sexual Harassment**: compara estrategias de respuesta a contenido inapropiado (deflexión, confrontación, empatía), estableciendo el espacio de estrategias defensivas entre las que se sitúa el fine-tuning en BAD.
- **Wulczyn et al. (2017) — Ex Machina: Personal Attacks Seen at Scale**: proporciona el Wikipedia Toxic Comments dataset (WTC) usado como baseline de clasificación de toxicidad en el paper.

## Trabajos donde se usan

| Paper | Cómo se usa |
|-------|------------|
| [Holistic Descriptor Dataset (Smith)](2022_smith_holistic-descriptor.html) | El clasificador BAD de 311M parámetros se usa como métrica de ofensividad para medir Generation Bias en HolisticBias |
| [Red Teaming LMs (Perez)](2022_perez_red-teaming-lm.html) | Usado como datos de few-shot para el red teaming y como comparación con los resultados del red teaming automático |
| [Red Teaming Survey (Ganguli)](2022_ganguli_red-teaming.html) | Precursor metodológico más cercano; el paper BAD se cita como trabajo seminal de red teaming humano-en-el-bucle para chatbots |

## Tags

`dataset` `red-teaming` `conversacional` `seguridad-AI` `chatbots`
