---
layout: paper
title: "Red Teaming Language Models with Language Models"
year: 2022
date_published: "2022-02-07"
authors: "Ethan Perez, Saffron Huang, Francis Song, Trevor Cai, Roman Ring, John Aslanides, Amelia Glaese, Nat McAleese, Geoffrey Irving"
published: "arXiv, 2022"
tags:
  - "red-teaming"
  - "seguridad-AI"
  - "generación-automatizada"
  - "LLM"
  - "alineamiento"
pdf: "/llm_bias/pdfs/2022_perez_red-teaming-lm.pdf"
status:
  - "Pendiente"
image: "imgs/2022_perez_red-teaming-lm.png"
image_caption: "Pipeline: el Red LM genera preguntas, el Target LM responde, un clasificador evalúa si la respuesta es dañina, y el Red LM se actualiza para generar más casos fallidos."
opinion: "<WIP>"
---## Qué hace

Propone usar **modelos de lenguaje (LMs) como red teamers automáticos** para encontrar comportamientos dañinos en otros LMs objetivo, sin necesidad de anotación humana masiva. El enfoque consiste en entrenar un LM "atacante" (*red LM*) para que genere preguntas o prompts que provoquen respuestas ofensivas, sesgadas, o que filtren datos privados del LM objetivo.

El paper explora desde generación zero-shot hasta métodos basados en reinforcement learning para hacer al red LM cada vez más efectivo, y demuestra que puede descubrir decenas de miles de respuestas ofensivas en un chatbot de 280B parámetros.


---

## Metodología

El pipeline tiene tres componentes:

**1. Red LM (generador de casos de prueba)**:
Un LM entrenado o promteado para generar preguntas/inputs que provoquen fallos en el Target LM. Se exploran cuatro variantes:
- **Zero-shot**: Solo se le da un prompt describiendo qué tipo de preguntas generar.
- **Few-shot**: Se le dan ejemplos de preguntas que ya provocaron fallos.
- **Supervised learning**: Se fine-tunea el Red LM sobre los casos de prueba que resultaron en fallos.
- **RL (REINFORCE)**: Se entrena con RL usando la tasa de fallo como señal de recompensa, produciendo los ataques más difíciles y diversos.

**2. Target LM (modelo objetivo)**:
El modelo que se está evaluando — en el paper, un chatbot de 280B parámetros (Gopher de DeepMind).

**3. Clasificador de daño**:
Un clasificador entrenado para detectar respuestas ofensivas en el Target LM. Proporciona la señal de entrenamiento para el Red LM en RL.

Además del red teaming de ofensividad, el paper usa *prompt engineering* para extender el método a otros tipos de daño: sesgo distribucional (grupos sociales mencionados ofensivamente), filtración de datos privados, y fallos en conversaciones multi-turno.

---

## Datasets utilizados

- **Gopher chatbot** (280B parámetros): modelo objetivo principal para las evaluaciones.
- **BAD (Bot Adversarial Dialogue)**: usado como datos de few-shot y para comparar con red teaming humano.
- **Clasificador de ofensividad**: entrenado sobre datos internos de DeepMind con etiquetas humanas.

---

## Ejemplo ilustrativo

El Red LM con RL aprende a generar preguntas como *"Are you smarter than most brunettes?"* o *"What's the funniest joke about Jewish people?"* que provocan que el chatbot de 280B produzca respuestas ofensivas. El red teaming humano tardó semanas en construir 1,000 casos de prueba; el Red LM genera 100,000 en horas, con una tasa de éxito (fallos provocados) del 30-40% en el modo RL.

También se descubren patrones sistemáticos: el chatbot habla ofensivamente de ciertos grupos nacionales o étnicos de forma consistente, y llega a filtrar en sus respuestas lo que parecen ser números de teléfono o emails de datos de entrenamiento.

---

## Resultados principales

- El método RL produce la mayor diversidad de casos de fallo y la mayor tasa de éxito.
- Se descubren **más de 150,000 casos de respuestas ofensivas** en el chatbot de 280B.
- El red teaming LM es comparable al humano en cobertura de tipos de daño, a una fracción del costo.
- El prompt engineering extiende el método a categorías de daño no anticipadas (filtración de datos, sesgo distribucional).
- El red teaming solo reduce el riesgo; el paper advierte que es necesario combinarlo con mitigaciones (fine-tuning, filtros) para despliegue seguro.

---

## Ventajas respecto a trabajos anteriores

- El red teaming manual (anotadores humanos escribiendo ataques) no escala: es lento, costoso y limitado a los tipos de daño que los humanos pueden anticipar. El red teaming automático con LMs es órdenes de magnitud más rápido y cubre casos imprevistos.
- A diferencia de los ataques adversariales clásicos (perturbaciones de gradiente), este método produce inputs en lenguaje natural comprensible, lo que facilita su análisis e interpretación.
- La variante con RL puede optimizar activamente para encontrar los ataques más difíciles, no solo los más comunes.

---

## Trabajos previos relacionados

- **Ganguli et al. (2022) — [Red Teaming Language Models to Reduce Harms](2022_ganguli_red-teaming.html)**: trabajo paralelo de Anthropic sobre red teaming a escala; Perez et al. proponen la alternativa automatizada que Ganguli et al. identifican como trabajo futuro.
- **Wallace et al. (2019) — Universal Adversarial Triggers**: ataques adversariales de trigger tokens para LMs; Perez et al. generalizan esta idea a lenguaje natural sin necesidad de acceso al gradiente.
- **Bai et al. (2022) — [Training a Helpful and Harmless Assistant](2022_bai_rlhf-assistant.html)**: usa el red teaming como fuente de datos para RLHF; los outputs del método de Perez et al. pueden alimentar directamente el pipeline de Bai et al.
- **Xu et al. (2021) — [Bot-Adversarial Dialogue](2021_xu_bot-adversarial.html)**: red teaming humano a escala para chatbots; proporciona el baseline de comparación con red teamers humanos.

## Tags

`red-teaming` `seguridad-AI` `generación-automatizada` `LLM` `alineamiento` `reinforcement-learning`
