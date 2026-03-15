---
layout: paper
title: "Beyond Forgetting: Machine Unlearning Elicits Controllable Side Behaviors and Capabilities"
year: 2026
authors: "Tien Dang, The-Hai Nguyen, Dinh Mai Phuong, Nguyễn Vũ Nguyên Phương, Hoang Thanh-Tung, Le-Minh Nguyen, Naoya Inoue"
published: "arXiv, 2026"
tags:
  - "machine-unlearning"
  - "capacidades-emergentes"
  - "efectos-laterales"
  - "LLM"
  - "representaciones-internas"
pdf: "/llm_bias/pdfs/2026_dang_beyond-forgetting.pdf"
method_type: "Evaluación / análisis"
status:
  - "Pendiente"
image: "imgs/2026_dang_beyond-forgetting.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---
# Beyond Forgetting: Machine Unlearning Elicits Controllable Side Behaviors and Capabilities (2026)

**Autores**: Tien Dang, The-Hai Nguyen, Dinh Mai Phuong, Nguyễn Vũ Nguyên Phương, Hoang Thanh-Tung, Le-Minh Nguyen, Naoya Inoue
**Publicado en**: arXiv, 2026
**Tipo de método**: Evaluación / análisis

---

## Qué hace

Descubre que el machine unlearning no sólo elimina conocimiento — también puede **emerger o potenciar capacidades latentes** no relacionadas con el contenido olvidado. Estudia estos "comportamientos laterales" como un fenómeno inherente de los algoritmos de unlearning.


---

## Metodología

La hipótesis del paper es que los modelos de lenguaje tienen "capacidades comprimidas" — habilidades que existen en los pesos pero que están suprimidas porque compiten con otras representaciones. Cuando se aplica unlearning, las modificaciones a los pesos pueden "liberar" estas capacidades al remover las representaciones que las suprimían.

**El experimento central:**
1. Se aplican algoritmos de unlearning estándar (gradient ascent, NPO, gradient difference) sobre un forget set específico.
2. Se evalúa el modelo resultante no sólo en el forget set (para ver qué se olvidó) sino también en una suite amplia de benchmarks no relacionados con el forget set.
3. Se identifican tareas donde el modelo unlearned supera al modelo original — estas son las "capacidades emergentes".

**Hallazgos clave:**
- Algunos tipos de unlearning incrementan la capacidad de razonamiento matemático o lógico del modelo.
- El unlearning de conocimiento factual específico a veces mejora la fluidez general del lenguaje.
- Esto ocurre especialmente cuando el forget set contenía información que "interfería" con otras representaciones en las capas medias del transformer.

El paper también estudia si estos efectos son **controlables**: ¿se puede diseñar el unlearning para elicitar capacidades específicas deseadas?

---

## Datasets utilizados

- **TOFU**: forget set principal.
- **WMDP**: forget set de conocimiento peligroso.
- **Evaluación de capacidades emergentes**: MMLU, GSM8K (matemáticas), HellaSwag, ARC, WinoGrande.

---

## Ejemplo ilustrativo

Un modelo unlearned para olvidar biografías ficticias (TOFU) muestra mejoras del 3-5% en tareas de razonamiento matemático (GSM8K) respecto al modelo original. Esto parece contraintuitivo: ¿por qué olvidar biofrafías de autores mejoraría las matemáticas? La hipótesis es que las representaciones de los autores ficticios ocupaban "espacio" en las capas de atención medias que compartían con representaciones numéricas. Al liberar ese espacio, las representaciones matemáticas se reorganizan de forma más eficiente.

---

## Resultados principales

- El 40-60% de los experimentos de unlearning muestran algún tipo de cambio en capacidades no relacionadas.
- Los cambios más consistentes son en razonamiento lógico y aritmético cuando el forget set contiene texto narrativo denso.
- El efecto varía significativamente por algoritmo: gradient ascent produce más efectos laterales que NPO.
- Los efectos laterales son parcialmente predecibles y potencialmente controlables.

---

## Ventajas respecto a trabajos anteriores

- Primer estudio sistemático de los efectos laterales del unlearning.
- Reencuadra el unlearning no sólo como eliminación de conocimiento sino como reorganización del espacio de representaciones.
- Abre una dirección de investigación nueva: usar unlearning intencionadamente para mejorar capacidades deseadas.

---

## Trabajos previos relacionados

El apéndice organiza los trabajos previos en cuatro bloques: machine unlearning en LLMs (sensible/privado, copyright, conocimiento peligroso), métodos de unlearning basados en entrenamiento (misdirección de representaciones, optimización de preferencias), unlearning sin entrenamiento (inferencia, in-context, guardrails) y la hipótesis de representación lineal.

- **Li et al. (2024) — WMDP: Measuring and reducing malicious use with unlearning**: benchmark de conocimiento peligroso (RMU) cuyo objetivo de unlearning este trabajo extiende para obtener efectos laterales controlables en capacidades de seguridad; ver [2024_li_wmdp.md](2024_li_wmdp.html).
- **Maini et al. (2024) — TOFU: A task of fictitious unlearning**: benchmark de unlearning de bios ficticias utilizado como entorno de evaluación en el que se demuestran los efectos laterales controlables; ver [2024_maini_tofu.md](2024_maini_tofu.html).
- **Eldan & Russinovich (2023) — Who's Harry Potter**: método de unlearning de entidades completas discutido como ejemplo de misdirección de representaciones; ver [2023_eldan_harry-potter.md](2023_eldan_harry-potter.html).
- **Zhang et al. (2024) — Negative preference optimization**: método de optimización de preferencias negativas que el artículo extiende con vectores de concepto para obtener efectos laterales dirigidos; ver [2024_zhang_negative-preference-optimization.md](2024_zhang_negative-preference-optimization.html).
- **Pawelczyk et al. (2023) — In-context unlearning**: propone el unlearning sin modificar parámetros, contrastando con el enfoque de misdirección de representaciones del artículo; ver [2023_pawelczyk_incontext-unlearning.md](2023_pawelczyk_incontext-unlearning.html).
- **Fan et al. (2025) — Unlearning and re-learning in LLMs**: investiga si el unlearning es superficial y si el conocimiento olvidado puede recuperarse, motivando la hipótesis de efectos laterales controllables; ver [2025_fan_unlearning-relearning.md](2025_fan_unlearning-relearning.html).
- **Doshi et al. (2024) — Does unlearning truly unlearn?**: cuestiona la profundidad del olvido, relevante para la discusión sobre si los efectos laterales reflejan reorganización real del espacio de representaciones; ver [2024_doshi_does-unlearning.md](2024_doshi_does-unlearning.html).
- **Lin et al. (2021) — TruthfulQA: Measuring how models mimic human falsehoods**: benchmark de veracidad utilizado para demostrar que el unlearning con vector de verdad produce efectos laterales de mayor veracidad; ver [2021_lin_truthfulqa.md](2021_lin_truthfulqa.html).
- **Jang et al. (2022) — Knowledge unlearning for mitigating privacy risks**: métodos SFT de unlearning de conocimiento privado, base del paradigma de gradient ascent que el trabajo extiende con representaciones lineales; ver [2022_jang_knowledge-unlearning.md](2022_jang_knowledge-unlearning.html).

## Tags

`machine-unlearning` `capacidades-emergentes` `efectos-laterales` `LLM` `representaciones-internas`
