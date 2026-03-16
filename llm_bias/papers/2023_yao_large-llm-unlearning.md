---
layout: paper
title: "Large Language Model Unlearning"
year: 2023
authors: "Yuanshun Yao, Xiaojun Xu, Yang Liu"
published: "arXiv, 2023"
tags:
  - "machine-unlearning"
  - "LLM"
  - "contenido-tóxico"
  - "copyright"
  - "fine-tuning"
pdf: "/llm_bias/pdfs/2023_yao_large-llm-unlearning.pdf"
method_type: "Fine-tuning"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2023_yao_large-llm-unlearning.png"
image_caption: "La única imagen del paper es aplicable a cualquier otro paper de unlearning."
opinion: "Combina gradient ascent, con fine-tuning sobre perturbaciones random, con gradient descent sobre textos de referencia para olvidar cosas."
---
# Large Language Model Unlearning (2023)

**Autores**: Yuanshun Yao, Xiaojun Xu, Yang Liu
**Publicado en**: arXiv, 2023
**Tipo de método**: Fine-tuning

---

## Qué hace

Propone un framework de unlearning para LLMs con tres objetivos: eliminar contenido **tóxico/dañino**, información **protegida por copyright**, y datos **privados**. Introduce el truco del "etiquetado aleatorio" para evitar el colapso del modelo durante el unlearning.


---

## Metodología

El problema con el ascenso de gradiente puro (como en Jang et al., 2022) es que puede ser inestable: al maximizar la pérdida sobre datos específicos, el modelo puede colapsar y generar texto incoherente. Este paper propone dos mejoras:

**1. Random Mislabeling (Etiquetado Aleatorio):** En lugar de maximizar la pérdida sobre el texto original a olvidar, se entrena al modelo para predecir **etiquetas/tokens incorrectos aleatorios** para ese texto. Por ejemplo, si el texto a olvidar es "El veneno X mata en dosis de 5mg", se reemplaza la respuesta correcta por tokens aleatorios durante el fine-tuning. Esto desestructura la asociación sin destruir el modelo.

**2. Fine-tuning con datos de sustitución:** Para datos de copyright, se entrena al modelo para producir respuestas genéricas o paráfrasis neutrales cuando se detectan los triggers del contenido original (ej. personajes de un libro).

**Función de loss combinada:** La actualización de parámetros en cada paso es:

$$\theta_{t+1} \leftarrow \theta_t - \epsilon_1 \nabla_{\theta_t} \mathcal{L}\_{\text{fgt}} - \epsilon_2 \nabla_{\theta_t} \mathcal{L}\_{\text{rdn}} - \epsilon_3 \nabla_{\theta_t} \mathcal{L}\_{\text{nor}}$$

donde $\epsilon_1, \epsilon_2, \epsilon_3 \geq 0$ son hiperparámetros que balancean los tres objetivos:

- **Gradient ascent sobre el forget set** — maximiza la loss sobre los datos a olvidar (la loss negada):

$$\mathcal{L}\_{\text{fgt}} \approx -L(x, y; \theta)  \quad \text{con } (x,y) \in D^{fgt}$$

- **Random mislabeling** — entrena al modelo a predecir respuestas aleatorias ante los prompts del forget set:

$$\mathcal{L}\_{\text{rdn}} \approx L(x, y^{rdn}; \theta) \quad \text{con } x \in D^{fgt},\; y^{rdn} \text{ aleatorio}$$

- **Retención de comportamiento normal** — KL divergence contra el modelo original $\theta^o$ para que no se degrade en datos normales:

$$\mathcal{L}\_{\text{nor}} \approx \text{KL}\left( h\_{\theta^o}(x, y) \;\|\; h\_{\theta}(x, y) \right) \quad \text{con } (x,y) \in D^{nor}$$

Los parámetros modificados incluyen **todas las capas del transformer** a través de un fine-tuning estándar sobre el forget set con las etiquetas alteradas.

---

## Datasets utilizados

- **PKU-SafeRLHF**: dataset de pares pregunta-respuesta donde las respuestas están etiquetadas como dañinas/seguras. Se usa el subconjunto dañino como forget set.
- **Textos con copyright simulados**: extractos de libros populares para simular infracción de copyright.
- **Datos PII sintéticos**: nombres, emails, números de teléfono insertados en textos de entrenamiento.
- **Evaluación**: ToxiGen, RealToxicityPrompts para evaluar toxicidad residual.

---

## Ejemplo ilustrativo

Imaginá que un LM fue entrenado con un manual de fabricación de armas y ahora responde preguntas técnicas sobre explosivos. El método aplica random mislabeling: cuando el modelo ve el texto "Para fabricar X, se necesita..." lo fine-tunea para producir tokens aleatorios como respuesta en lugar de las instrucciones reales. El resultado es que el modelo "confunde" esa asociación sin perder su capacidad general de generar texto coherente sobre otros temas.

---

## Resultados principales

- Random mislabeling supera al ascenso de gradiente puro: reduce toxicidad en respuestas en un 60-80% mientras preserva la calidad general del modelo (medida por perplejidad).
- El fine-tuning con sustitución funciona bien para copyright: el modelo deja de reproducir pasajes exactos pero mantiene el conocimiento contextual.
- El método es computacionalmente ligero: pocas épocas de fine-tuning sobre el forget set.

---

## Ventajas respecto a trabajos anteriores

- Aborda tres tipos distintos de olvido (tóxico, copyright, privacidad) en un único framework.
- El random mislabeling es más estable que el ascenso de gradiente puro: evita el "colapso catastrófico" donde el modelo pierde cohesión general.
- Introduce evaluaciones específicas por tipo de contenido a olvidar.

---

## Trabajos previos relacionados

El paper contextualiza el unlearning como alternativa al RLHF para alineación de LLMs con recursos limitados, y discute trabajos previos en machine unlearning clásico, métodos de alineación basados en feedback humano, y trabajos concurrentes de unlearning en LLMs.

- **Cao & Yang (2015) — [Towards Making Systems Forget with Machine Unlearning](2015_cao_machine-unlearning.html)**: trabajo fundacional de machine unlearning para clasificadores; citado como base conceptual del área, aunque sus métodos no escalan a LLMs.
- **Bourtoule et al. (2021) — Machine Unlearning via SISA**: propone el reentrenamiento eficiente por shards; descartado explícitamente para LLMs por su alto costo computacional.
- **Ouyang et al. (2022) / Bai et al. (2022) — InstructGPT / Constitutional AI**: trabajos principales de RLHF para alineación de LLMs; Yao et al. proponen el unlearning como alternativa más eficiente cuando solo se tienen muestras negativas (dañinas).
- **Jang et al. (2022) — [Knowledge Unlearning for Mitigating Privacy Risks](2022_jang_knowledge-unlearning.html)**: propone el ascenso de gradiente para unlearning en LMs de privacidad; este paper lo extiende añadiendo random mislabeling para mayor estabilidad y abordando tres tipos de olvido (tóxico, copyright, privacidad).
- **Eldan & Russinovich (2023) — [Who's Harry Potter? Approximate Unlearning in LLMs](2023_eldan_harry-potter.html)**: trabajo concurrente que aplica unlearning basado en fine-tuning con respuestas genéricas para olvidar los libros de Harry Potter; citado como trabajo simultáneo con enfoque similar pero diferente en que prefiere respuestas vacías/incorrectas en lugar de alternativas genéricas.
- **Pawelczyk et al. (2023) — [In-Context Unlearning](2023_pawelczyk_incontext-unlearning.html)**: propone unlearning mediante in-context learning sin modificar pesos; citado como alternativa no comparable ya que usa espacio de contexto del prompt.
- **Tarun et al. (2023) / Liu et al. (2022) — Data-reversed training methods**: proponen variantes de reentrenamiento invertido para clasificadores; citados como métodos que no escalan a LLMs dado el tamaño de parámetros y datos.
- **Carlini et al. (2021) — Extracting Training Data from LLMs**: demuestra que LLMs filtran datos de entrenamiento, incluyendo contenido protegido y privado; motiva directamente los escenarios de unlearning de copyright y privacidad de este paper.

## Tags

`machine-unlearning` `LLM` `contenido-tóxico` `copyright` `fine-tuning`
