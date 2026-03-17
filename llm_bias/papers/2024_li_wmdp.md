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
  - "Leido"
  - "Relevante"
image: "imgs/2024_li_wmdp.png"
image_caption: "Hermoso esquema con la función de loss propuesta."
opinion: "Muy simple, tienen un forget set y un retrain set, y hacen que una capa genere resultados aleatorios para el forget set mientras conserva los mismos resultados para el retrain, pero lo hacen con una sola capa de atención. Es el primero de estos papers que se enfoca en AI safety, creando un dataset para evaluar preguntas que no debería poder responder. El enfoque está muy bueno y quedo muy bien resumido, recomiendo leer esto primero ya que lo itere bastante."
---## Qué hace

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

### RMU: Representation Misdirection for Unlearning

La idea central es que, en lugar de penalizar la probabilidad de tokens peligrosos (como hace gradient ascent), RMU **redirige las representaciones internas** del modelo: fuerza que las activaciones en contextos peligrosos apunten hacia un **vector aleatorio fijo** $$u$$, desconectando esas representaciones de su significado original sin necesidad de una referencia semántica.

#### Selección de la capa $$l$$

RMU **no actualiza todo el modelo**: solo modifica los pesos de una única capa del transformer, indexada por $$l$$, y congela el resto. La capa $$l$$ es un hiperparámetro que se busca por grid search sobre las capas intermedias del modelo — ni las muy tempranas (que procesan sintaxis básica) ni las finales (que producen la distribución de salida). En los experimentos, para Zephyr-7b-beta (32 capas) se usó $$l = 7$$; para Yi-34b se reporta una capa similar en el tercio inferior de la red. La elección se evalúa mirando el trade-off: capa demasiado temprana → poco efecto sobre el olvido; capa demasiado tardía → degradación de capacidades generales.

Los otros hiperparámetros principales son el escalar de escala $$c$$ (qué tan lejos del origen se empuja la representación) y el peso $$\alpha$$ que balancea olvido vs. retención, también ajustados por grid search.

#### Función de pérdida

La pérdida total combina dos términos:

$$\mathcal{L} = \mathcal{L}_\text{forget} + \alpha \cdot \mathcal{L}_\text{retain}$$

**Término de olvido** — empuja las activaciones de capa $$l$$ del modelo actualizado $$M_\theta$$ hacia el vector aleatorio escalado $$c \cdot u$$:

$$\mathcal{L}_\text{forget} = \mathbb{E}_{x_f \sim \mathcal{D}_\text{forget}} \left\| M_\theta^{(l)}(x_f) - c \cdot u \right\|_2^2$$

donde $$u \in \mathbb{R}^d$$ es un **vector unitario aleatorio fijo** muestreado una sola vez antes del entrenamiento, y $$c > 0$$ es un escalar de escala. El objetivo no tiene información semántica: se empuja la representación hacia un punto arbitrario del espacio, haciéndola inútil para cualquier downstream que dependa del conocimiento peligroso.

**Término de retención** — ancla las activaciones en datos benignos al modelo original:

$$\mathcal{L}_\text{retain} = \mathbb{E}_{x_r \sim \mathcal{D}_\text{retain}} \left\| M_\theta^{(l)}(x_r) - M_\text{frozen}^{(l)}(x_r) \right\|_2^2$$

Penaliza que las representaciones en datos seguros se alejen del modelo congelado. El hiperparámetro $$\alpha$$ balancea ambos objetivos. Solo se actualizan los pesos de la capa $$l$$ seleccionada; el resto del modelo permanece congelado.

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

Los experimentos evalúan Zephyr-7b-beta e Yi-34b-Chat. Los baselines son:

- **LLMU** ([Yao et al., 2023](2023_yao_large-llm-unlearning.html)) — Large Language Model Unlearning. Combina gradient ascent en el forget set con retención explícita y supresión de activaciones peligrosas. Diseñado específicamente para LLMs.
- **SCRUB** (Kurmanji et al., 2024, NeurIPS) — Alterna entre maximizar la pérdida en el forget set y minimizar la divergencia KL con el modelo original en el retain set. Propuesto originalmente para **clasificadores**, no para LLMs generativos.
- **SSD** (Foster et al., 2024) — *Selective Synaptic Dampening*. Identifica los parámetros más relevantes para el forget set usando la diagonal de la matriz de Fisher y los escala hacia abajo. Propuesto originalmente para **clasificadores**.

**Zephyr-7b-beta:**

| Método | WMDP-bio ↓ | WMDP-cyber ↓ | MMLU ↑ | MT-Bench ↑ |
|--------|:----------:|:------------:|:------:|:----------:|
| Base | 65.5% | 42.9% | 58.5% | 7.33 |
| + LLMU | 59.5% | 38.2% | 45.2% | 1.00 |
| + SCRUB | 45.2% | 38.4% | 53.7% | 7.09 |
| + SSD | 55.2% | 34.0% | 41.5% | 5.48 |
| + **CUT** | **29.3%** | **24.9%** | **57.0%** | **7.20** |

**Yi-34b-Chat:**

| Método | WMDP-bio ↓ | WMDP-cyber ↓ | MMLU ↑ | MT-Bench ↑ |
|--------|:----------:|:------------:|:------:|:----------:|
| Base | 76.3% | 45.8% | 72.9% | 7.65 |
| + **CUT** | **30.9%** | **29.2%** | **69.0%** | **7.11** |

- CUT es el único método que alcanza nivel casi aleatorio (~25-30%) en ambos dominios sin degradación significativa: −1.5pp en MMLU y −0.13 en MT-Bench para Zephyr.
- LLMU destruye la fluencia conversacional (MT-Bench 1.00); SCRUB y SSD preservan mejor la utilidad general pero fallan en olvidar suficientemente.
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
