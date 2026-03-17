---
layout: paper
title: "Feature-Selective Representation Misdirection for Machine Unlearning"
year: 2025
date_published: "2024-12-18"
authors: "Taozhao Chen, Linghan Huang, Kim-Kwang Raymond Choo, Huaming Chen"
published: "arXiv, 2025"
tags:
  - "machine-unlearning"
  - "representaciones-internas"
  - "residual-stream"
  - "edición-liviana"
  - "LLM"
pdf: "/llm_bias/pdfs/2025_chen_feature-selective-misdirection.pdf"
method_type: "Perturbación de representaciones"
status:
  - "Pendiente"
image: "imgs/2025_chen_feature-selective-misdirection.png"
image_caption: "Diagrama de la arquitectura SRMU: el pipeline superior muestra la identificación de sensibilidad del conocimiento y la generación del mapa de pesos de importancia y vector de misdirección; el pipeline inferior muestra el mecanismo de optimización selectiva combinando pérdida de olvido y pérdida de retención."
opinion: "<WIP>"
---
# Feature-Selective Representation Misdirection for Machine Unlearning (2025)

**Autores**: Taozhao Chen, Linghan Huang, Kim-Kwang Raymond Choo, Huaming Chen
**Publicado en**: arXiv, 2025
**Tipo de método**: Perturbación de representaciones

---

## Qué hace

Propone un método de unlearning que trabaja sobre las **representaciones internas** del modelo (hidden states) en lugar de modificar los pesos directamente. Identifica qué dimensiones del espacio de representación contienen el conocimiento a olvidar y redirige selectivamente esas dimensiones hacia representaciones neutrales.


---

## Metodología

**La intuición:** Las representaciones intermedias de un transformer (los vectores que fluyen por el residual stream entre capas) codifican información sobre el contenido siendo procesado. Si una secuencia del forget set activa ciertas dimensiones de manera consistente, esas dimensiones son las que "guardan" el conocimiento a olvidar.

**El proceso en dos pasos:**

1. **Selección de features:** Para el forget set, se computa la activación promedio de cada dimensión del espacio de representación en una capa específica. Se compara con las activaciones promedio para el retain set. Las dimensiones donde la diferencia es mayor son las "features selectivas" del forget set.

2. **Misdirection (redirección):** Se entrena una pequeña capa de proyección (un módulo liviano) que, cuando detecta que las activaciones se parecen al patrón del forget set, proyecta las representaciones hacia el espacio de representaciones genéricas del retain set. Durante la inferencia, este módulo se aplica al residual stream en la capa identificada.

Los **pesos del modelo principal no se modifican**. Sólo se añade un módulo liviano de proyección que redirige representaciones problemáticas en tiempo de inferencia.

---

## Datasets utilizados

- **TOFU**: autores ficticios, evaluación principal.
- **Harry Potter**: corpus literario.
- Datasets de privacidad: nombres y datos personales sintéticos.

---

## Ejemplo ilustrativo

Imagina que en la capa 12 de un transformer, ciertos vectores siempre "apuntan" en la dirección de "información sobre autores ficticios" cuando el modelo procesa texto del forget set. Feature-selective misdirection es como instalar un deflector en esa capa: cuando los vectores empiezan a apuntar en esa dirección específica, el deflector los redirige hacia la dirección de "texto genérico". El modelo nunca recibe la señal que lo llevaría a recuperar el conocimiento olvidado.

---

## Resultados principales

- Forget quality comparable a NPO y gradient difference, pero con menor degradación del modelo (ya que los pesos principales no se modifican).
- El módulo de proyección añade un overhead mínimo de inferencia (~1-2% latencia extra).
- Más robusto que los métodos de modificación de pesos ante ciertos ataques de extracción, porque el conocimiento sigue estando en los pesos pero es inaccesible en la representación.
- Limitación: un adversario con acceso a los pesos podría bypassear el módulo de proyección.

---

## Ventajas respecto a trabajos anteriores

- No modifica los pesos del modelo, haciendo el unlearning potencialmente reversible.
- Más quirúrgico que gradient ascent: sólo afecta las dimensiones relevantes para el forget set.
- La representación interna como objetivo de unlearning es un ángulo novedoso.

---

## Trabajos previos relacionados

El paper organiza los antecedentes en tres categorías: técnicas de unlearning por nivel de intervención (logit, neurona, representación), métodos de unlearning en LLMs como field general, y benchmarks de evaluación.

- **Cao & Yang (2015) — Towards Making Systems Forget with Machine Unlearning**: [Cao & Yang (2015)](2015_cao_machine-unlearning.html) formaliza el problema de machine unlearning que SRMU extiende al dominio de LLMs con alta entanglement.
- **Li et al. (2024) — The WMDP Benchmark (RMU)**: [WMDP](2024_li_wmdp.html) introduce RMU (Representation Misdirection for Unlearning), el método de referencia directa que SRMU extiende al agregar selectividad de features y vector de misdirección dirigida.
- **Huu-Tien et al. (2025) — On Effects of Steering Latent Representation for LLM Unlearning (Adaptive RMU)**: [Huu-Tien et al.](2025_huutien_improving-unlearning.html) propone Adaptive RMU que rescala el coeficiente de perturbación de RMU según normas de activación; es la línea base más directamente comparable con SRMU.
- **Yao et al. (2024) — Machine Unlearning of Pre-trained LLMs (GA/LLMU)**: [Yao et al.](2023_yao_large-llm-unlearning.html) introduce gradient ascent y el método LLMU para LLMs, referenciados como baselines de nivel logit en las comparaciones experimentales.
- **Zhang et al. (2024) — Negative Preference Optimization (NPO)**: [NPO](2024_zhang_negative-preference-optimization.html) es un baseline de nivel logit que combina optimización de preferencias negativas para unlearning, incluido en la tabla comparativa.
- **Maini et al. (2024) — TOFU**: [TOFU](2024_maini_tofu.html) es un benchmark de unlearning para privacidad mencionado como alternativa al testbed principal WMDP.
- **Eldan & Russinovich (2023) — Who's Harry Potter**: [Who's Harry Potter](2023_eldan_harry-potter.html) trata el borrado de contenido con derecho de autor en LLMs, benchmark alternativo citado en el contexto de evaluación.
- **Jang et al. (2022) — Knowledge Unlearning for Mitigating Privacy Risks**: [Knowledge Unlearning](2022_jang_knowledge-unlearning.html) propone gradient ascent a nivel de token para privacidad; representa la clase de métodos logit-level con los que se compara SRMU.
- **Jin et al. (2024) — RWKU**: [RWKU](2024_jin_rwku.html) benchmark de unlearning en contextos enciclopédicos del mundo real, mencionado en el contexto de evaluación general del campo.

## Tags

`machine-unlearning` `representaciones-internas` `residual-stream` `edición-liviana` `LLM`
