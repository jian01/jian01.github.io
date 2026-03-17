---
layout: paper
title: "Negative Preference Optimization: From Catastrophic Collapse to Effective Unlearning"
year: 2024
date_published: "2024-04-08"
authors: "Ruiqi Zhang, Licong Lin, Yu Bai, Song Mei"
published: "arXiv, 2024"
tags:
  - "machine-unlearning"
  - "DPO"
  - "optimización"
  - "LLM"
  - "colapso-catastrófico"
pdf: "/llm_bias/pdfs/2024_zhang_negative-preference-optimization.pdf"
method_type: "Optimización de preferencias"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2024_zhang_negative-preference-optimization.png"
image_caption: "Respuestas de los modelos después de distintas técnicas de unlearning sobre TOFU. La del paper es NPO+RT (Negative preference optimization + Retain set)."
opinion: "<WIP>"
---
# Negative Preference Optimization: From Catastrophic Collapse to Effective Unlearning (2024)

**Autores**: Ruiqi Zhang, Licong Lin, Yu Bai, Song Mei
**Publicado en**: arXiv, 2024
**Tipo de método**: Optimización de preferencias

---

## Qué hace

Adapta el algoritmo DPO (Direct Preference Optimization) para machine unlearning, creando NPO (Negative Preference Optimization). Resuelve el problema del "colapso catastrófico" que ocurre con el ascenso de gradiente puro, donde el modelo pierde coherencia general.


---

## Metodología

### El problema del gradient ascent y la solución NPO

**El problema del gradient ascent (GA):** Maximizar la pérdida sobre el forget set empuja los pesos en la dirección opuesta al gradiente sin ninguna restricción. Esto puede llevar al modelo a generar texto completamente incoherente: el "colapso catastrófico".

**La solución NPO:** DPO entrena LLMs con pares (respuesta buena, respuesta mala). NPO toma únicamente la mitad "negativa" de ese objetivo: usa solo las respuestas del forget set como "respuestas rechazadas", sin necesitar ninguna respuesta "ganadora". Matemáticamente, el objetivo NPO sobre el forget set es:

$$\mathcal{L}_\text{NPO} = -\frac{2}{\beta} \mathbb{E}_{y \sim \mathcal{D}_f} \left[ \log \sigma\!\left(-\beta \log \frac{\pi_\theta(y \mid x)}{\pi_\text{ref}(y \mid x)}\right) \right]$$

El término $\pi_\text{ref}$ (el modelo original congelado) actúa como ancla implícita: el modelo no puede alejarse arbitrariamente de la distribución original, lo que previene el colapso.

### Combinaciones de métodos evaluadas

El paper organiza todos los métodos como una combinación de dos componentes independientes:

**Componente 1 — Objetivo de olvido** (qué se aplica sobre el forget set):

| Nombre | Descripción |
|--------|-------------|
| **GA** | Gradient Ascent puro: maximiza la pérdida $\mathcal{L}_{CE}$ sobre el forget set. No tiene restricción interna → propenso al colapso catastrófico. |
| **NPO** | Negative Preference Optimization: aplica el objetivo DPO negativo sobre el forget set usando el modelo de referencia como ancla implícita. Estable por construcción. |

**Componente 2 — Término de retención** (qué se aplica sobre el retain set, opcional):

| Nombre | Descripción |
|--------|-------------|
| *(ninguno)* | Solo se actúa sobre el forget set. Más riesgo de degradación. |
| **+ GD** (Gradient Difference) | Añade gradient descent normal sobre el retain set: $-\mathcal{L}_{CE}$ sobre datos del retain set. Penaliza directamente que el modelo olvide lo que debe retener. |
| **+ RT** (Retain) | Añade una regularización KL entre el modelo actual y el modelo de referencia evaluada sobre el retain set, forzando que la distribución de salida no cambie en ese subconjunto. Es más conservador que GD: no pide que el modelo acierte las respuestas del retain, sino que su distribución no cambie. |

**Combinaciones completas evaluadas (grilla 2 × 3):**

| | Sin retención | + GD | + RT |
|---|:---:|:---:|:---:|
| **GA** | GA | GA + GD | GA + RT |
| **NPO** | NPO | NPO + GD | **NPO + RT** ← propuesta principal |

Cada combinación se evalúa en las tres métricas de TOFU (Forget Quality, Retain Accuracy, Model Utility) y en WMDP + MMLU para el dominio de conocimiento peligroso.

**La propuesta central del paper es NPO + RT**: combina el objetivo de olvido estable de NPO con la regularización sobre el retain set, y es la combinación que domina consistentemente el trade-off forget/retain en los experimentos.

---

## Datasets utilizados

- **TOFU**: autores ficticios, el benchmark principal.
- **WMDP**: conocimiento peligroso.
- Evaluación general con MMLU y perplexity sobre texto estándar.

---

## Ejemplo ilustrativo

Gradient ascent puro es como intentar desaprender a manejar diciéndole al cerebro "haz lo opuesto de todo lo que sabes de conducción" — el resultado podría ser un caos total, incluyendo olvidar cómo caminar. NPO sería más como: "olvida específicamente las rutas del vecindario X, pero mantén todo el resto de conocimiento de conducción intacto". El modelo de referencia actúa como el "resto del conocimiento de conducción".

---

## Resultados principales

- NPO supera al gradient ascent en TOFU: mejor forget quality con mucho menor degradación del modelo.
- La degradación en MMLU (capacidades generales) con NPO es típicamente menor al 5%, versus 20-30% con gradient ascent agresivo.
- Es más lento que gradient ascent (requiere el modelo de referencia para computar el término de regularización) pero mucho más estable.
- Mejor que métodos de fine-tuning estándar (gradient difference) en forget quality sin sacrificar retain accuracy.

---

## Ventajas respecto a trabajos anteriores

- Primer método que resuelve el colapso catastrófico del gradient ascent de forma teóricamente motivada.
- La conexión con DPO abre la puerta a aprovechar toda la infraestructura de entrenamiento con preferencias para unlearning.
- Proporciona un balance mucho mejor entre olvidar y retener.

---

## Trabajos previos relacionados

El paper agrupa los trabajos previos en tres áreas: (1) métodos de unlearning clásicos basados en gradient ascent para clasificadores, (2) métodos de unlearning específicos para LLMs, y (3) el framework de RLHF/DPO del que deriva NPO. Para los benchmarks de evaluación, destaca TOFU como benchmark principal adoptado en el paper.

- **Cao & Yang (2015) — Machine Unlearning**: [Machine Unlearning](2015_cao_machine-unlearning.html): trabajo fundacional que introduce machine unlearning; NPO surge como respuesta a sus limitaciones de escalabilidad a LLMs.
- **Jang et al. (2022) — Knowledge Unlearning**: [Knowledge Unlearning](2022_jang_knowledge-unlearning.html): propone gradient ascent (GA) como método de unlearning para LLMs; NPO demuestra superarlo al evitar el colapso catastrófico que GA produce.
- **Yao et al. (2023) — Large Language Model Unlearning**: [Large Language Model Unlearning](2023_yao_large-llm-unlearning.html): otro método basado en GA para LLMs que sirve como baseline de comparación directa.
- **Eldan & Russinovich (2023) — Who's Harry Potter?**: [Who's Harry Potter?](2023_eldan_harry-potter.html): propone generar muestras positivas con prompts diseñados para fine-tuning; método complementario y alternativo al enfoque de NPO.
- **Maini et al. (2024) — TOFU**: [TOFU](2024_maini_tofu.html): introduce el benchmark de autores ficticios que NPO adopta como evaluación principal de sus experimentos.
- **Rafailov et al. (2024) — Direct Preference Optimization (DPO)**: [DPO](2023_ermon_dpo.html): el algoritmo de alineamiento del que NPO toma directamente su formulación matemática, usando sólo la mitad "negativa" del objetivo de DPO.
- **Bai et al. (2022) — RLHF Assistant**: [RLHF Assistant](2022_bai_rlhf-assistant.html): trabajo clave en RLHF que motiva la conexión entre alineamiento con preferencias y unlearning que NPO explora.
- **Li et al. (2024) — WMDP**: [WMDP](2024_li_wmdp.html): propone el benchmark de conocimiento peligroso utilizado como segunda evaluación de NPO junto a TOFU.
- **Lynch et al. (2024) — Eight Methods**: [Eight Methods](2024_lynch_eight-methods.html): propone ocho métricas robustas para evaluar unlearning incluyendo resistencia a jailbreaks, evaluación adoptada en el paper.
- **Ethayarajh et al. (2024) — KTO**: [V-Usable Information / KTO](2022_ethayarajh_v-usable-information.html): método de alineamiento con datos no pareados que comparte formulación similar a NPO; los autores comparan NPO vs KTO en simulaciones.
- **Patil et al. (2023) — Sensitive Information**: [Sensitive Information](2023_patil_sensitive-information.html): método de ataque para extraer datos de modelos unlearned, relevante para evaluar si NPO es resistente a ataques de extracción.

## Tags

`machine-unlearning` `DPO` `optimización` `LLM` `colapso-catastrófico`
