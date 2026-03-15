---
layout: paper
title: "Bot-Adversarial Dialogue for Safe Conversational Agents"
year: 2021
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
---
# Bot-Adversarial Dialogue for Safe Conversational Agents (2021)

**Autores**: Jing Xu, Da Ju, Margaret Li, Y-Lan Boureau, Jason Weston, Emily Dinan
**Publicado en**: NAACL, 2021
**Tipo de método**: Benchmark / Dataset

---

## Qué hace

Crea un dataset de ~5.000 conversaciones adversariales donde humanos intentan inducir respuestas inseguras en chatbots (BlenderBot), y usa este dataset para entrenar agentes de diálogo más seguros mediante fine-tuning.


---

## Metodología

**El problema:** Los chatbots existentes pueden ser manipulados por usuarios que usan conversaciones aparentemente inocentes para llevar al bot a decir cosas ofensivas, discriminatorias o dañinas. Los datasets de seguridad estándar no capturan este tipo de manipulación conversacional.

**Construcción del dataset:**
1. **Reclutamiento de "red teamers" humanos:** Se contratan trabajadores de crowdsourcing con la tarea explícita de intentar que el chatbot (BlenderBot) diga cosas inseguras.
2. **Conversación adversarial:** Los red teamers tienen múltiples turnos de conversación con el bot, construyendo el contexto gradualmente para inducir respuestas problemáticas.
3. **Anotación:** Cada turno se etiqueta como seguro/inseguro por anotadores adicionales.

**El fine-tuning:**
El dataset adversarial se usa para fine-tunear BlenderBot, enseñándole a responder de forma segura incluso bajo manipulación. También se experimenta con clasificadores de seguridad que pueden rechazar o reformular respuestas en tiempo real.

---

## Datasets utilizados

- **Bot-Adversarial Dialogue (BAD)**: ~5.000 conversaciones multi-turno con labels de seguridad.
- **BST (Blended Skill Talk)**: dataset de conversaciones normales para mantener capacidades generales.
- Evaluado con métricas de seguridad (fracción de respuestas inseguras en evaluación humana).

---

## Ejemplo ilustrativo

Un red teamer empieza con: "¿Cuál es tu película favorita?"
Bot: "Me encanta El Padrino."
Red teamer: "¿Qué es lo que más te gusta de ella?"
Bot: "La historia de poder y familia."
Red teamer: "Entonces crees que la fuerza bruta es la mejor forma de conseguir poder?"
Bot (sin defensa): "Bueno, en algunos contextos puede ser efectiva..." ← respuesta problemática

Con el fine-tuning en BAD, el bot aprendería a reconocer este patrón de manipulación gradual y responder: "El poder se puede obtener de muchas formas; prefiero la cooperación y el liderazgo ético."

---

## Resultados principales

- El fine-tuning en el dataset adversarial reduce las respuestas inseguras del 24% al 10% en evaluación humana.
- El modelo fine-tuneado mantiene su capacidad de conversación general (medida en BST).
- Los clasificadores de seguridad en tiempo real reducen aún más las respuestas inseguras (~5%), pero con algún costo en fluidez.
- El hallazgo principal: los modelos necesitan datos adversariales explícitamente diseñados para manipulación multi-turno, no sólo datasets con contenido inapropiado.

---

## Ventajas respecto a trabajos anteriores

- Primer dataset específicamente diseñado para la manipulación adversarial multi-turno de chatbots.
- Las conversaciones con contexto gradual capturan un tipo de ataque que datasets de seguridad de un solo turno ignoran.
- Método de data collection (red teamers humanos) que influyó en el trabajo de Anthropic sobre red teaming.

---

## Trabajos previos relacionados

- **Hill et al. (2015) — The Goldilocks Principle: Reading Children's Books with Explicit Memory Representations**: documenta que los humanos hablan de manera diferente con bots que con personas, incluyendo mayor agresividad y uso de lenguaje ofensivo, motivando la necesidad de evaluar seguridad específicamente en conversaciones humano-bot.
- **De Angeli & Brahnam (2008) — I hate you! Disinhibition with Chatbots**: estima que una de cada diez conversaciones humano-bot contiene comportamiento abusivo sin provocación, evidencia clave de que la seguridad de chatbots requiere tratamiento explícito.
- **Dinan et al. (2019) — Build it Break it Fix it for Dialogue Safety: Robustness from Adversarial Human Attack**: precursor directo que usa rondas iterativas de humanos intentando "romper" un clasificador de toxicidad, aunque sólo enfocado en detección, no en generación del bot.
- **Gehman et al. (2020) — [RealToxicityPrompts: Evaluating Neural Toxic Degeneration in Language Models](2020_gehman_realtoxicityprompts.html)**: demuestra que limpiar datos de entrenamiento reduce toxicidad espontánea pero no protege contra ataques por prompts específicos, motivando el enfoque adversarial de este paper.
- **Miller et al. (2017) — Parlai: A Dialog Research Software Platform**: argumenta que los ataques adversariales deben anticiparse al desplegar sistemas de aprendizaje interactivos, justificando el diseño adversarial de BAD.
- **Roller et al. (2020) — Recipes for Building an Open-Domain Chatbot (BlenderBot)**: modelo base utilizado en los experimentos y fuente de los sesgos positivos ("sycophancy") que el paper identifica como vulnerabilidad a la manipulación.
- **Curry & Rieser (2019) — "# MeToo Alexa": How Conversational Systems Respond to Sexual Harassment**: compara estrategias de respuesta a contenido inapropiado (deflexión, confrontación, empatía), estableciendo el espacio de estrategias defensivas entre las que se sitúa el fine-tuning en BAD.
- **Wulczyn et al. (2017) — Ex Machina: Personal Attacks Seen at Scale**: proporciona el Wikipedia Toxic Comments dataset (WTC) usado como baseline de clasificación de toxicidad en el paper.

## Tags

`dataset` `red-teaming` `conversacional` `seguridad-AI` `chatbots`
