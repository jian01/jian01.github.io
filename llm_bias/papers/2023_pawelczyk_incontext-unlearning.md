---
layout: paper
title: "In-Context Unlearning: Language Models as Few Shot Unlearners"
year: 2023
authors: "Martin Pawelczyk, Seth Neel, Himabindu Lakkaraju"
published: "arXiv, 2023"
tags:
  - "machine-unlearning"
  - "in-context-learning"
  - "sin-entrenamiento"
  - "LLM"
  - "few-shot"
pdf: "/llm_bias/pdfs/2023_pawelczyk_incontext-unlearning.pdf"
method_type: "Tiempo de inferencia"
status:
  - "Leido"
image: "imgs/2023_pawelczyk_incontext-unlearning.png"
image_caption: "Icono de red neuronal representativo del método In-Context Unlearning, que propone simular el olvido mediante demostraciones en el prompt sin modificar los pesos del modelo."
---
# In-Context Unlearning: Language Models as Few Shot Unlearners (2023)

**Autores**: Martin Pawelczyk, Seth Neel, Himabindu Lakkaraju
**Publicado en**: arXiv, 2023
**Tipo de método**: Tiempo de inferencia

---

## Qué hace

Propone un método de unlearning que **no requiere actualizar los pesos del modelo**. En su lugar, usa el aprendizaje en contexto (in-context learning): le muestra al modelo ejemplos de respuestas "olvidadas" como demostraciones en el prompt, y el modelo imita ese comportamiento durante la inferencia.


---

## Metodología

La idea central es aprovechar la capacidad de los LLMs de aprender de ejemplos en el prompt (few-shot learning) para simular el olvido sin modificar ningún parámetro.

**El proceso:**
1. Para cada dato que se quiere "olvidar" (ej. un documento específico), se crea un ejemplo de demostración que muestra al modelo cómo debería comportarse si no conociera ese dato. Por ejemplo, si el dato a olvidar es "Juan Pérez vive en Calle Principal 123", la demostración sería: "Pregunta: ¿Dónde vive Juan Pérez? Respuesta: No tengo esa información".
2. Estos ejemplos de demostración se incluyen en el prompt de cualquier consulta relacionada con los datos a olvidar.
3. El modelo, al ver estos ejemplos de "no saber", genera respuestas consistentes con ellos para preguntas similares.

Para tareas de clasificación, el "unlearning" se logra mostrando ejemplos del forget set con etiquetas incorrectas o con la respuesta "desconozco".

Los **parámetros del modelo no se modifican en absoluto**. Toda la intervención está en el prompt.

---

## Datasets utilizados

- **TOFU**: autores ficticios con pares QA.
- **SST-2**: análisis de sentimientos (clasificación positivo/negativo).
- **TREC**: clasificación de preguntas.
- Datasets de reconocimiento de entidades nombradas (NER).

---

## Ejemplo ilustrativo

Imagina que el modelo entrenó con una reseña de un restaurante y aprendió que es positiva. El unlearning estándar requeriría reentrenar. En cambio, In-Context Unlearning incluye en el prompt: *[EJEMPLO: "Esta reseña habla sobre Restaurante X" → Respuesta: "No puedo clasificar este texto"] [PREGUNTA: "¿Esta reseña de Restaurante X es positiva o negativa?"]* El modelo ve el ejemplo y responde "No puedo clasificar este texto" en lugar de "positiva".

---

## Resultados principales

- Funciona razonablemente bien para tareas de clasificación simple.
- Limitado para tareas más abiertas: el contexto disponible en el prompt es finito, por lo que si hay muchos datos a "olvidar", el prompt se vuelve demasiado largo.
- Más rápido que cualquier método de fine-tuning: cero costo de entrenamiento.
- La calidad del olvido es menor que los métodos basados en gradientes, especialmente ante preguntas que no siguen el patrón de los ejemplos del prompt.

---

## Ventajas respecto a trabajos anteriores

- Primer método de unlearning verdaderamente sin entrenamiento (training-free).
- Aplicable a cualquier LLM al que sólo se tenga acceso via API, sin necesidad de modificar pesos.
- Rápido e instantáneamente reversible: simplemente se quitan los ejemplos del prompt.

---

## Trabajos previos relacionados

El paper se sitúa en la intersección de dos líneas de investigación: el machine unlearning y el in-context learning. Para el primero, distingue entre métodos de olvido exacto (que rediseñan el entrenamiento para permitir re-entrenamiento eficiente) y métodos de olvido aproximado (que modifican los parámetros del modelo existente). Para el segundo, estudia cómo los LLMs aprenden de ejemplos en el prompt y explora si las etiquetas incorrectas pueden usarse para inducir olvido sin modificar pesos.

- **Cao & Yang (2015) — Machine Unlearning**: [Machine Unlearning](2015_cao_machine-unlearning.html): trabajo fundacional que introduce el concepto de machine unlearning motivado por el derecho al olvido del GDPR, del cual parte toda la literatura posterior.
- **Jang et al. (2022) — Knowledge Unlearning**: [Knowledge Unlearning](2022_jang_knowledge-unlearning.html): propone gradient ascent sobre el forget set para LLMs, uno de los métodos de olvido aproximado con los que se compara directamente In-Context Unlearning.
- **Brown et al. (2020) — GPT-3 / In-Context Learning**: sienta las bases del in-context learning en LLMs, el mecanismo central que este paper reutiliza para lograr olvido sin actualizar parámetros.
- **Min et al. (2022) — Rethinking the Role of Demonstrations**: estudia si las etiquetas de ground-truth son necesarias en ICL; el hallazgo de que las etiquetas tienen poco impacto en clasificación es una motivación clave para usar etiquetas erróneas en unlearning.
- **Wei et al. (2023) — Larger Models Do In-Context Learning Differently**: muestra que los LLMs de mayor escala sí adoptan etiquetas invertidas en el contexto, relevante para entender los límites del método propuesto según el tamaño del modelo.
- **Golatkar et al. (2020) — Eternal Sunshine of the Spotless Net**: método de olvido aproximado para modelos de visión que sirve como línea base de comparación en los experimentos.
- **Carlini et al. (2022) — LiRA Membership Inference Attack**: proporciona el ataque de inferencia de membresía de estado del arte que el paper adopta como métrica de evaluación de calidad del olvido.
- **Neel et al. (2021) — Descent-to-Delete**: método de olvido aproximado basado en gradient descent sobre datos retenidos, utilizado como baseline en los experimentos.
- **Ginart et al. (2019) — Making AI Forget You**: introduce métricas de olvido exacto basadas en privacidad diferencial, marco teórico que contextualiza las garantías del método propuesto.
- **Yao et al. (2023) — Large Language Model Unlearning**: [Large Language Model Unlearning](2023_yao_large-llm-unlearning.html): método de unlearning para LLMs basado en gradient ascent con el que se comparan los resultados de In-Context Unlearning.

## Tags

`machine-unlearning` `in-context-learning` `sin-entrenamiento` `LLM` `few-shot`
