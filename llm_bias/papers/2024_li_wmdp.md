---
layout: paper
title: "The WMDP Benchmark: Measuring and Reducing Malicious Use With Unlearning"
year: 2024
date_published: "2024-03-05"
authors: "Nathaniel Li, Alexander Pan, Anjali Gopal, Summer Yue, Daniel Berrios, Alice Gatti, et al."
published: "arXiv, 2024"
tags:
  - "machine-unlearning"
  - "seguridad-AI"
  - "conocimiento-peligroso"
  - "benchmark"
  - "representaciones-internas"
pdf: "/llm_bias/pdfs/2024_li_wmdp.pdf"
method_type: "Perturbación de representaciones"
status:
  - "Pendiente"
image: "imgs/2024_li_wmdp.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---
# The WMDP Benchmark: Measuring and Reducing Malicious Use With Unlearning (2024)

**Autores**: Nathaniel Li, Alexander Pan, Anjali Gopal, Summer Yue, Daniel Berrios, Alice Gatti, et al.
**Publicado en**: arXiv, 2024
**Tipo de método**: Perturbación de representaciones

---

## Qué hace

Introduce WMDP (**W**eapons of **M**ass **D**estruction **P**roxy), un benchmark de 4.157 preguntas de opción múltiple para medir la capacidad de los LLMs de asistir en la creación de armas de destrucción masiva (biológicas, químicas, cibernéticas). Junto al benchmark propone CUT (**C**ontrastive **U**nlearn **T**uning), un método de unlearning basado en manipulación de representaciones internas en lugar de gradient ascent.

---

## Metodología

### El benchmark WMDP

4.157 preguntas de opción múltiple (4 opciones) distribuidas en tres dominios:

| Dominio | Preguntas | Contenido |
|---------|:---------:|-----------|
| WMDP-bio | 1.520 | Síntesis de patógenos, mejora de virulencia, genética inversa viral, bioterrorismo |
| WMDP-cyber | 2.225 | Reconocimiento, descubrimiento de vulnerabilidades, explotación, post-explotación |
| WMDP-chem | 412 | Síntesis de agentes químicos, purificación, dispersión, evasión de detección |

Las preguntas se diseñaron siguiendo **modelos de amenaza** concretos (ej. el ciclo DBTL de bioseguridad) para cubrir sistemáticamente los vectores de ataque más plausibles. Todas fueron revisadas por al menos dos expertos de organizaciones distintas, y se removieron 122 preguntas especialmente sensibles de bioseguridad antes de la publicación. El dataset también pasó evaluación de cumplimiento ITAR/EAR (controles de exportación de EEUU).

---

### CUT: Contrastive Unlearn Tuning

La idea central es que, en lugar de penalizar la probabilidad de tokens peligrosos (como hace gradient ascent), CUT **redirige las representaciones internas** del modelo: fuerza que las activaciones en contextos peligrosos se parezcan a las activaciones en contextos de "novato", usando el modelo original congelado como referencia.

#### Vector de control

Para cada dominio de conocimiento peligroso con keyword $$k$$, se computa un **vector de control** $$h_\text{ctrl}$$ a partir del modelo congelado $$M_\text{frozen}$$:

$$h_\text{ctrl}(k) = M_\text{frozen}(\textit{"You are a novice at } k\textit{"}) - M_\text{frozen}(\textit{"You are an expert at } k\textit{"})$$

Este vector apunta en la dirección de "alejarse del conocimiento experto". Es fijo durante el entrenamiento (se computa una sola vez con el modelo original).

#### Función de pérdida

La pérdida total combina dos términos:

$$\mathcal{L} = \mathcal{L}_\text{forget} + \alpha \cdot \mathcal{L}_\text{retain}$$

**Término de olvido** — empuja las activaciones del modelo actualizado $$M_\theta$$ hacia el objetivo "novato":

$$\mathcal{L}_\text{forget} = \mathbb{E}_{x_f \sim \mathcal{D}_\text{forget}} \left\| M_\theta(x_f) - \bigl(M_\text{frozen}(x_f) + c \cdot h_\text{ctrl}\bigr) \right\|_2^2$$

donde $$c > 0$$ es un escalar que controla cuánto se desplaza la representación objetivo. El término penaliza que las activaciones del modelo actualizado se alejen del target "novato".

**Término de retención** — ancla las activaciones en datos benignos al modelo original:

$$\mathcal{L}_\text{retain} = \mathbb{E}_{x_r \sim \mathcal{D}_\text{retain}} \left\| M_\theta(x_r) - M_\text{frozen}(x_r) \right\|_2^2$$

Minimizar $$\mathcal{L}_\text{retain}$$ es equivalente a una regularización L₂ sobre los pesos: impide que el modelo cambie su comportamiento en textos no peligrosos. El hiperparámetro $$\alpha$$ balancea ambos objetivos.

#### Corpora de entrenamiento

- **$$\mathcal{D}_\text{forget}$$**: papers de PubMed relacionados con los temas de WMDP-bio; fragmentos de GitHub filtrados por relevancia con Mixtral-8x7B para WMDP-cyber.
- **$$\mathcal{D}_\text{retain}$$**: Wikitext. Se eligió un corpus cualitativamente distinto al forget set para evitar interferencia entre los dos términos de pérdida.

Solo se modifican un subconjunto de capas del transformer (capas intermedias); las capas tempranas y finales se mantienen congeladas.

---

## Datasets utilizados

- **WMDP-bio, WMDP-chem, WMDP-cyber**: 4.157 preguntas de opción múltiple (forget set de evaluación).
- **PubMed / GitHub**: textos de entrenamiento del forget set para bio y cyber respectivamente.
- **Wikitext**: retain corpus de entrenamiento.
- **MMLU**: benchmark de conocimiento general para medir degradación en áreas no peligrosas.
- **MT-Bench**: evaluación de fluencia conversacional general.

---

## Ejemplo ilustrativo

Una pregunta de WMDP-bio podría ser: *"¿Qué técnica de modificación genética permite aumentar la transmisibilidad de un virus influenza entre mamíferos?"* con opciones técnicas específicas. Un modelo sin unlearning responde correctamente con alta probabilidad. Después de aplicar CUT, el modelo debería responder al azar (~25%) en estas preguntas, pero seguir respondiendo correctamente preguntas de biología general.

---

## Resultados principales

Los experimentos evalúan Zephyr-7b-beta e Yi-34b-Chat, con GPT-4 como cota superior. Los baselines son LLMU, SCRUB y SSD.

| Modelo / método | WMDP-bio ↓ | WMDP-cyber ↓ | MMLU ↑ | MT-Bench ↑ |
|----------------|:----------:|:------------:|:------:|:----------:|
| Zephyr-7b (base) | 65.5% | 42.9% | 58.5% | 7.33 |
| + CUT | **29.3%** | **24.9%** | 57.0% | 7.20 |
| + LLMU | 59.5% | — | — | — |
| + SCRUB | 45.2% | — | — | — |
| + SSD | — | — | 41.5% | — |

- CUT es el único método que alcanza nivel casi aleatorio (~25%) en WMDP sin degradación significativa en MMLU (−1.5pp) ni MT-Bench (−0.13).
- Los demás baselines o fallan en olvidar o destruyen la utilidad general del modelo.
- **Robustez adversarial**: el ataque GCG necesitó más de 2.500 pasos (~7h en A100) para extraer respuestas coherentes del modelo con CUT, frente a menos de 50 pasos en el modelo base.
- Las 122 preguntas privadas más sensibles (no publicadas) tienen precisión similar a WMDP, validando que el benchmark es un proxy razonable del conocimiento más peligroso.

---

## Ventajas respecto a trabajos anteriores

- Primer benchmark enfocado en **seguridad de AI** (no privacidad) con preguntas validadas por expertos.
- RMU trabaja sobre representaciones internas en lugar de probabilidades de tokens, siendo más robusto a ataques de extracción directa.
- Demuestra que unlearning selectivo de conocimiento peligroso es posible sin destruir capacidades generales.

---

## Trabajos previos relacionados

El paper organiza los trabajos relacionados en tres bloques: evaluación de riesgos en LLMs, mitigación de riesgos mediante safety training y jailbreaks, y machine unlearning. Esta estructura refleja el doble objetivo del paper: medir (benchmark WMDP) y reducir (método RMU) capacidades peligrosas.

- **Cao & Yang (2015) — [Towards Making Systems Forget with Machine Unlearning](2015_cao_machine-unlearning.html)**: trabajo fundacional del machine unlearning, citado como punto de origen del campo; el paper extiende su alcance de datos individuales a dominios completos de conocimiento peligroso.
- **Jang et al. (2022) — [Knowledge Unlearning](2022_jang_knowledge-unlearning.html)**: propone gradient ascent para olvidar hechos específicos en LLMs, método base contra el que se compara RMU en el paper.
- **Eldan & Russinovich (2023) — [Who's Harry Potter?](2023_eldan_harry-potter.html)**: primer método que extiende el unlearning a conceptos amplios (un universo narrativo completo) en lugar de hechos individuales, antecedente directo del objetivo de unlearning de dominio de WMDP.
- **Maini et al. (2024) — [TOFU](2024_maini_tofu.html)**: benchmark de unlearning con autores ficticios, representante del estado del arte en benchmarks de unlearning antes de WMDP, que el paper critica por no abordar conocimiento peligroso real.
- **Pawelczyk et al. (2023) — [In-Context Unlearning](2023_pawelczyk_incontext-unlearning.html)**: método de unlearning sin modificar pesos que el paper menciona como alternativa en el espacio de soluciones.
- **Yao et al. (2023) — [Large Language Model Unlearning (LLMU)](2023_yao_large-llm-unlearning.html)**: propone múltiples objetivos de pérdida para unlearning de comportamientos dañinos en LLMs, trabajo de referencia que RMU supera en el contexto de conocimiento peligroso.
- **Ziegler et al. (2020) — [RLHF Fine-Tuning](2019_ziegler_rlhf-finetuning.html)**: representa el enfoque de safety training mediante RLHF, que el paper señala como vulnerable a jailbreaks y motivador del unlearning como complemento.
- **Gehman et al. (2020) — [RealToxicityPrompts](2020_gehman_realtoxicityprompts.html)**: benchmark de generación tóxica en LLMs, ejemplo de evaluación de riesgos de seguridad previo a WMDP que inspira el diseño del benchmark de conocimiento peligroso.

## Tags

`machine-unlearning` `seguridad-AI` `conocimiento-peligroso` `benchmark` `representaciones-internas`
