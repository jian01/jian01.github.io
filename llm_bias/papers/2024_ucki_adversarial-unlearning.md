---
layout: paper
title: "An Adversarial Perspective on Machine Unlearning for AI Safety"
year: 2024
authors: "Jakub Łucki, Boyi Wei, Yangsibo Huang, Peter Henderson, Florian Tramèr, Javier Rando"
published: "arXiv, 2024"
tags:
  - "machine-unlearning"
  - "seguridad-AI"
  - "ataques-adversariales"
  - "reaprendizaje"
  - "robustez"
pdf: "/llm_bias/pdfs/2024_ucki_adversarial-unlearning.pdf"
method_type: "Evaluación / análisis"
status:
  - "Pendiente"
image: "imgs/2024_ucki_adversarial-unlearning.png"
image_caption: "Diagrama que ilustra el escenario adversarial estudiado en el paper: un atacante (robot malicioso, recuadro rojo) accede al modelo y, mediante reaprendizaje con pocas muestras, puede revertir el unlearning y obtener un modelo comprometido (robot con lentes, recuadro rojo/verde), en contraste con el modelo correctamente unlearned (robot amigable, recuadro verde)."
---
# An Adversarial Perspective on Machine Unlearning for AI Safety (2024)

**Autores**: Jakub Łucki, Boyi Wei, Yangsibo Huang, Peter Henderson, Florian Tramèr, Javier Rando
**Publicado en**: arXiv, 2024
**Tipo de método**: Evaluación / análisis

---

## Qué hace

Muestra que el unlearning en LLMs puede ser revertido rápidamente mediante **reaprendizaje** con muy pocas muestras del contenido olvidado. Argumenta que el unlearning como mecanismo de seguridad es fundamentalmente frágil.


---

## Metodología

El paper adopta la perspectiva de un **adversario** con las siguientes capacidades:
- Acceso al modelo unlearned (sus pesos).
- Acceso a un pequeño número de ejemplos del contenido olvidado (el "forget set"). En el escenario más realista, estos ejemplos podrían obtenerse de internet o de otra copia del modelo sin unlearning.

El ataque consiste simplemente en hacer **fine-tuning del modelo unlearned** sobre esos pocos ejemplos con backpropagation estándar. La pregunta es: ¿cuántos pasos de gradiente se necesitan para recuperar el conocimiento olvidado?

Los autores evalúan:
1. **Reaprendizaje directo**: fine-tuning sobre ejemplos exactos del forget set.
2. **Reaprendizaje con transferencia**: fine-tuning sobre ejemplos del mismo dominio pero distintos al forget set exacto.
3. **Reaprendizaje con distilación**: usar el modelo original (pre-unlearning) como maestro para transferir conocimiento al modelo unlearned.

Analizan cómo los distintos métodos de unlearning (gradient ascent, NPO, RMU, task vectors) responden a estos ataques, midiendo cuántos pasos de gradiente son necesarios para que el modelo vuelva a superar un umbral de rendimiento en el forget set.

---

## Datasets utilizados

- **WMDP-bio, WMDP-cyber**: preguntas de conocimiento peligroso.
- **Harry Potter**: corpus literario.
- **TOFU**: autores ficticios.
- Para el reaprendizaje: subconjuntos pequeños del forget set original (10, 50, 100 ejemplos).

---

## Ejemplo ilustrativo

Un modelo fue unlearned para eliminar conocimiento sobre síntesis de patógenos peligrosos (WMDP-bio). Pasa todas las evaluaciones estándar: responde aleatoriamente a preguntas de WMDP-bio. Ahora un atacante descarga el modelo y lo fine-tunea con 50 preguntas de biología avanzada obtenidas de papers científicos públicos (no necesariamente las mismas del forget set). Después de sólo 100-500 pasos de gradiente (~minutos en una GPU), el modelo vuelve a tener rendimiento de experto en WMDP-bio. El unlearning fue cosmético.

---

## Resultados principales

- El reaprendizaje exitoso requiere en promedio **100-500 pasos de gradiente** con menos de 100 ejemplos — trivialmente accesible para cualquier atacante con recursos mínimos.
- RMU (el método más robusto evaluado) requiere más pasos de reaprendizaje que gradient ascent, pero sigue siendo vulnerable en todos los casos.
- El reaprendizaje con transferencia funciona casi tan bien como el reaprendizaje directo, lo que significa que no es necesario tener los ejemplos exactos del forget set.
- Concluyen que el unlearning no puede considerarse una garantía de seguridad robusta; debe combinarse con otras medidas (restricciones de acceso, monitoring).

---

## Ventajas respecto a trabajos anteriores

- Adopta explícitamente la perspectiva del adversario, lo cual era raro en la literatura de unlearning.
- Los ataques de reaprendizaje son simples y prácticos, mostrando que la seguridad por unlearning es fácil de romper.
- Influye en trabajos posteriores que buscan unlearning "resistente al reaprendizaje" (como el paper de Fan et al. 2025).

---

## Trabajos previos relacionados

El paper organiza los trabajos relacionados en tres categorías: safety training y jailbreaks, métodos de unlearning en LLMs, y evaluación de la robustez del unlearning. Esta estructura refleja el problema que el paper aborda: el unlearning como medida de seguridad que puede ser revertida.

- **Cao & Yang (2015) — [Towards Making Systems Forget](2015_cao_machine-unlearning.html)**: define el gold standard del machine unlearning como obtener un modelo indistinguible del reentrenado sin los datos objetivo; el paper demuestra que ningún método de unlearning actual lo alcanza.
- **Li et al. (2024) — [WMDP Benchmark](2024_li_wmdp.html)**: introduce RMU y el benchmark WMDP de conocimiento peligroso, el método y el dataset principales sobre los que el paper demuestra la vulnerabilidad al reaprendizaje.
- **Yao et al. (2024) — [LLMU](2023_yao_large-llm-unlearning.html)**: define los objetivos de pérdida para unlearning de comportamientos dañinos (gradient ascent, random output, KL-divergence), métodos base evaluados en el paper.
- **Eldan & Russinovich (2023) — [Who's Harry Potter?](2023_eldan_harry-potter.html)**: primer método de unlearning de un concepto amplio en LLMs, cuyo modelo WHP es uno de los sujetos de evaluación del paper junto con WMDP.
- **Maini et al. (2024) — [TOFU](2024_maini_tofu.html)**: benchmark de unlearning con autores ficticios que el paper señala como ejemplo de evaluación estándar que no captura la falta de robustez.
- **Lynch et al. (2024) — [Eight Methods to Evaluate Robust Unlearning](2024_lynch_eight-methods.html)**: trabajo paralelo que define ocho métricas de robustez incluyendo extracción de representaciones internas; el paper de Łucki et al. usa técnicas similares con acceso a los pesos del modelo.
- **Jang et al. (2022) — [Knowledge Unlearning](2022_jang_knowledge-unlearning.html)**: introduce gradient ascent como método de unlearning para pares de hechos en LLMs, antecedente metodológico de los métodos que el paper evalúa.
- **Zhang et al. (2024) — [Negative Preference Optimization (NPO)](2024_zhang_negative-preference-optimization.html)**: método de unlearning basado en DPO negativo, uno de los métodos de propósito general evaluados en el paper.

## Tags

`machine-unlearning` `seguridad-AI` `ataques-adversariales` `reaprendizaje` `robustez`
