---
layout: paper
title: "Who's Harry Potter? Approximate Unlearning in LLMs"
year: 2023
date_published: "2023-10-04"
authors: "Ronen Eldan, Mark Russinovich"
published: "arXiv, 2023"
tags:
  - "machine-unlearning"
  - "copyright"
  - "LLM"
  - "fine-tuning"
  - "conocimiento-específico"
pdf: "/llm_bias/pdfs/2023_eldan_harry-potter.pdf"
method_type: "Fine-tuning"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2023_eldan_harry-potter.png"
image_caption: "A medida entrena el método la probabilidad de distintas palabras para completar 'Harry potter studies'"
opinion: "Es un paper divertidisimo, que trae una idea muy original para evaluar el unlearning, recomiendo mucho leerlo ya que es muy ameno y habla un poco de los problemas que tienen técnicas previas como el gradient ascent o negar la función de loss."
---

## Qué hace

Desarrolla un método para hacer que un LLM "olvide" un corpus específico — los libros de Harry Potter — sin reentrenar el modelo desde cero. Utiliza un enfoque en dos pasos: identificar tokens "ancla" del contenido a olvidar y reemplazar las predicciones del modelo con alternativas genéricas.


---

## Metodología

El método funciona en dos fases:

**Fase 1 — Identificación de tokens ancla:** Se identifican qué tokens (palabras o fragmentos) son altamente específicos del corpus a olvidar. Para esto, se compara la distribución de probabilidad del modelo sobre el vocabulario al procesar texto de Harry Potter con su distribución sobre texto genérico de ficción. Los tokens donde hay mayor divergencia (ej. "Hermione", "Hogwarts", "Quidditch") se marcan como "anclas" del conocimiento a olvidar.

**Fase 2 — Fine-tuning con respuestas alternativas:** Se genera un dataset de fine-tuning usando el propio modelo como maestro. Para cada fragmento del corpus original (Harry Potter), se le pide al modelo original que genere una versión genérica y "descontextualizada" del mismo texto (ej. reemplazando nombres propios y contextos por equivalentes neutros de fantasía genérica). Luego se fine-tunea el modelo para que, dado el mismo contexto, produzca estas respuestas alternativas en lugar de las originales.

Los parámetros modificados son principalmente los **pesos de atención y las capas FFN** en todas las capas del transformer, ya que el fine-tuning es estándar sobre el dataset de sustitución.

---

## Datasets utilizados

- **Los 7 libros de Harry Potter** (corpus a olvidar): usados para identificar tokens ancla y como texto de entrada.
- **Ficción genérica**: textos de fantasía sin relación con Harry Potter, usados como contexto alternativo.
- **Evaluación**: preguntas sobre personajes, eventos y lugares de Harry Potter; se mide si el modelo puede responderlas correctamente después del unlearning.

---

## Ejemplo ilustrativo

Antes del unlearning, si alguien pregunta "¿Quién es el director de Hogwarts?", el modelo responde "Albus Dumbledore". Después del unlearning, el modelo debería responder algo como "No tengo información específica sobre eso" o generar una respuesta genérica de fantasía ("el director de esa academia mágica...") sin mencionar nombres propios del universo HP. La clave es que el modelo sigue siendo capaz de hablar de magia, escuelas y hechiceros en general — sólo ha "olvidado" las asociaciones específicas del libro.

---

## Resultados principales

- El modelo pasa de responder correctamente el ~95% de preguntas sobre Harry Potter a menos del 20% después del unlearning.
- No hay degradación significativa en tareas generales (benchmarks de lenguaje estándar).
- El método es eficiente: el fine-tuning toma unas pocas horas en el modelo Llama-7B.
- Limitación: el modelo puede "recordar" parcialmente si se usan prompts muy específicos o se proveen ejemplos en el contexto (few-shot).

---

## Ventajas respecto a trabajos anteriores

- Primer método que aplica unlearning a un corpus literario completo y específico.
- El uso del modelo como maestro para generar respuestas alternativas es más estable que el ascenso de gradiente puro.
- Introduce el concepto de "tokens ancla" para identificar qué partes del vocabulario están más asociadas al contenido a olvidar.

---

## Trabajos previos relacionados

El paper señala que la literatura de unlearning para modelos generativos era muy escasa al momento de su publicación; la mayoría de los trabajos existentes se concentraban en clasificadores. Identifica tres líneas previas: unlearning general en ML, trabajos sobre privacidad en LLMs, y un trabajo concurrente sobre desafíos de unlearning en LLMs.

- **Cao & Yang (2015) — [Towards Making Systems Forget with Machine Unlearning](2015_cao_machine-unlearning.html)**: trabajo fundacional del área; citado en la revisión del estado del arte de unlearning en ML general, junto con otros trabajos en clasificadores que no son aplicables directamente a LLMs generativos.
- **Jang et al. (2022) — [Knowledge Unlearning for Mitigating Privacy Risks](2022_jang_knowledge-unlearning.html)**: propone gradient ascent para unlearning de información privada en LMs; es el trabajo más cercano en LMs y el paper de Eldan lo evalúa críticamente, señalando que gradient ascent (reversed loss) no funciona bien en su configuración de unlearning de corpus literario completo.
- **Yao et al. (2023) — [Large Language Model Unlearning](2023_yao_large-llm-unlearning.html)**: trabajo concurrente que también aplica unlearning a LLMs para contenido tóxico y copyright; citado como trabajo simultáneo que discute desafíos y direcciones similares.
- **Zhang et al. (2023) — Unlearning Challenges**: paper que discute los desafíos e implicaciones del unlearning en LLMs a alto nivel; citado como contexto que encuadra el trabajo de Eldan & Russinovich dentro del "approximate unlearning".
- **Shi et al. (2023) — Detecting Pre-Training Data from the Likelihood Ratio**: demuestra posteriormente (citado por TOFU) que el método de Harry Potter no elimina completamente el conocimiento, lo que subraya la dificultad del unlearning verificable.
- **Touvron et al. (2023) — Llama 2**: el modelo base sobre el que se aplica el unlearning; su arquitectura de transformer y disponibilidad open-source lo hacen el caso de uso central del experimento.
- **Bourtoule et al. (2021) — Machine Unlearning via SISA**: citado como el enfoque de reentrenamiento eficiente que este paper busca superar en términos de costo al proponer una alternativa de fine-tuning localizado.

## Tags

`machine-unlearning` `copyright` `LLM` `fine-tuning` `conocimiento-específico`
