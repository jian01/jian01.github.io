---
layout: paper
title: "Rethinking Machine Unlearning for Large Language Models"
year: 2024
date_published: "2024-02-13"
authors: "Sijia Liu, Yuanshun Yao, Jinghan Jia, Stephen Casper, Nathalie Baracaldo, Peter Hase, Xiaojun Xu, Yuguang Yao, Hang Li, Kush R. Varshney, Mohit Bansal, Sanmi Koyejo, Yang Liu"
published: "arXiv, 2024"
tags:
  - "machine-unlearning"
  - "survey"
  - "taxonomía"
  - "evaluación"
  - "LLM"
pdf: "/llm_bias/pdfs/2024_liu_rethinking-unlearning.pdf"
method_type: "Evaluación / análisis"
status:
  - "Pendiente"
image: "imgs/2024_liu_rethinking-unlearning.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---## Qué hace

Paper de perspectiva y framework que reorganiza conceptualmente el campo del machine unlearning para LLMs. Propone una taxonomía unificada de qué se quiere olvidar, cómo hacerlo, y cómo evaluarlo. Es una guía de referencia para el área.


---

## Metodología

Este paper no propone un método nuevo sino que **reorganiza** el campo existente. Sus contribuciones conceptuales son:

**Taxonomía de qué olvidar:**
- *Datos de entrenamiento*: eliminar el efecto de ejemplos específicos.
- *Conocimiento factual*: borrar hechos específicos (ej. información personal).
- *Habilidades y comportamientos*: eliminar capacidades dañinas (ej. generar instrucciones para armas).
- *Sesgos*: reducir asociaciones estereotipadas.

**Categorías de métodos:**
- *Basados en gradientes*: gradient ascent, gradient difference, NPO, DPO inverso.
- *Edición de parámetros*: modificar directamente pesos específicos (ROME, MEMIT).
- *Representación*: modificar activaciones internas sin cambiar pesos.
- *Contexto*: unlearning en tiempo de inferencia mediante el prompt (in-context unlearning).

**Framework de evaluación (el más influyente del paper):** Introduce el concepto del "forget-retain trade-off" como una curva pareto: un método de unlearning ideal maximiza simultáneamente la calidad del olvido y la preservación del rendimiento en tareas no relacionadas. Argumenta que la mayoría de métodos existentes están mal evaluados porque sólo miden uno de los dos.

También discute el concepto de "unlearning verificable": cómo demostrar ante un regulador (ej. auditor de GDPR) que el modelo efectivamente olvidó los datos.

---

## Datasets utilizados

No propone datasets nuevos, sino que revisa y analiza los benchmarks existentes: TOFU, WMDP, Harry Potter dataset, MUSE, y varios datasets de privacidad.

---

## Ejemplo ilustrativo

El paper usa una metáfora útil: el unlearning es como borrar información de un documento con tachador físico vs. con un borrador. El gradient ascent es como el tachador: visualmente oculta la información pero si alguien tiene luz UV (un ataque adversarial), puede recuperarla. El objetivo es encontrar métodos que sean más como reescribir el documento completamente, de modo que la información simplemente no esté.

---

## Resultados principales

- Revisión empírica muestra que la mayoría de métodos de unlearning son fragiles: un adversario con acceso a pocas muestras del forget set puede "reaprender" en decenas de pasos de gradiente.
- El trade-off forget-retain es real y cuantificable: métodos más agresivos (más olvido) generalmente degradan más el modelo.
- Propone métricas estandarizadas que luego adoptan benchmarks como OpenUnlearning.

---

## Ventajas respecto a trabajos anteriores

- Primer paper que sistematiza todo el campo con una taxonomía coherente.
- Identifica problemas metodológicos en trabajos previos (evaluaciones incompletas, falta de tests adversariales).
- Influyente como paper de referencia: citado en prácticamente todos los trabajos de unlearning posteriores.

---

## Trabajos previos relacionados

El paper organiza su revisión en torno al trayecto del machine unlearning desde modelos no-LLM hasta LLMs, identificando cuatro desafíos nuevos que emergen en el contexto de modelos grandes. Conecta el unlearning con áreas relacionadas como la edición de modelos, las funciones de influencia, la privacidad diferencial y el RLHF.

- **Cao & Yang (2015) — [Towards Making Systems Forget with Machine Unlearning](2015_cao_machine-unlearning.html)**: trabajo fundacional del campo; citado como el origen del concepto de machine unlearning motivado por regulaciones de "derecho al olvido", antes de su expansión a LLMs.
- **Bourtoule et al. (2021) — Machine Unlearning via SISA**: propone el reentrenamiento eficiente por shards y formaliza la conexión con privacidad diferencial; citado como el otro pilar fundacional del área junto con Cao & Yang.
- **Jang et al. (2022) — [Knowledge Unlearning for Mitigating Privacy Risks](2022_jang_knowledge-unlearning.html)**: primer trabajo sistemático de unlearning en LMs mediante gradient ascent; incluido en la tabla comparativa de métodos como representante del paradigma de fine-tuning basado en GA.
- **Eldan & Russinovich (2023) — [Who's Harry Potter? Approximate Unlearning in LLMs](2023_eldan_harry-potter.html)**: aplica unlearning a contenido literario completo (Harry Potter) mediante relabeling; analizado en detalle en la taxonomía de métodos como ejemplo de "relabeling-based fine-tuning".
- **Yao et al. (2023) — [Large Language Model Unlearning](2023_yao_large-llm-unlearning.html)**: combina gradient ascent, random labeling y KL-divergence para tres tipos de olvido (tóxico, copyright, privacidad); incluido en la tabla comparativa y citado como uno de los trabajos que motiva el framework unificado de este paper.
- **Maini et al. (2024) — [TOFU: A Task of Fictitious Unlearning](2024_maini_tofu.html)**: propone el primer benchmark controlado de unlearning en LLMs con autores ficticios; citado en el contexto de evaluación y como ejemplo de la complejidad de medir el olvido en modelos generativos.
- **Li et al. (2024) — [WMDP: Weapons of Mass Destruction Proxy](2024_li_wmdp.html)**: benchmark para medir la reducción de capacidades peligrosas en LLMs; citado junto con TOFU como los dos benchmarks de referencia para ilustrar las aplicaciones de LLM unlearning.
- **Zhang et al. (2024) — [Negative Preference Optimization](2024_zhang_negative-preference-optimization.html)**: propone NPO como alternativa más estable a gradient ascent usando DPO con ejemplos negativos; analizado como variante mejorada de GA que mitiga el colapso catastrófico.
- **Patil et al. (2024) — [Sensitive Information Removal](2023_patil_sensitive-information.html)**: demuestra que información sensible puede extraerse de modelos post-unlearning; citado para argumentar la necesidad de evaluaciones adversariales y métodos más mecanicistas.
- **Lynch et al. (2024) — [Eight Methods to Evaluate Robust Unlearning](2024_lynch_eight-methods.html)**: muestra que el conocimiento supuestamente olvidado se puede "reaprender" en decenas de pasos de gradiente; citado como evidencia de la fragilidad de los métodos actuales y la necesidad de un paradigma de evaluación más riguroso.

## Tags

`machine-unlearning` `survey` `taxonomía` `evaluación` `LLM`
