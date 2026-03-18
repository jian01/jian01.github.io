---
layout: paper
title: "KL Minimization for Machine Unlearning in LLMs"
year: 2024
date_published: "2024-01-11"
authors: "Pratyush Maini, Zhili Feng, Avi Schwarzschild, Zachary Chase Lipton, J. Zico Kolter"
published: "Introducido como baseline en TOFU (arXiv, 2024)"
tags:
  - "machine-unlearning"
  - "gradient-ascent"
  - "regularización"
  - "LLM"
  - "KL-divergencia"
pdf: "/llm_bias/pdfs/2024_maini_tofu.pdf"
method_type: "Gradient ascent"
status:
  - "Pendiente"
image: "imgs/2024_maini_tofu.png"
image_caption: "KL Minimization es uno de los métodos de unlearning evaluados en el benchmark TOFU. Combina ascenso de gradiente sobre el forget set con regularización KL para preservar el comportamiento del modelo en el retain set."
opinion: "<WIP>"
---

## Qué hace

Propone un método de unlearning que combina **ascenso de gradiente sobre el forget set** con un **término de regularización basado en divergencia KL** para mantener la distribución de salida del modelo sobre el retain set cercana al modelo original. Es una variante del Gradient Difference que reemplaza el descenso de gradiente explícito sobre el retain set por una penalización KL más suave.

Este método es introducido y evaluado como baseline en el benchmark [TOFU](2024_maini_tofu.html).

---

## Metodología

La función de pérdida combina dos términos:

1. **Gradient Ascent sobre el forget set**: maximiza la pérdida del modelo sobre los datos que se quieren olvidar, igual que en [Jang et al. (2022)](2022_jang_knowledge-unlearning.html) y [Yao et al. (2023)](2023_yao_large-llm-unlearning.html).

2. **Regularización KL sobre el retain set**: en lugar de aplicar gradient descent directo sobre el retain set (como hace [Gradient Difference](2023_yao_large-llm-unlearning.html)), minimiza la divergencia KL entre la distribución del modelo actualizado y la del modelo original sobre el retain set:

   $$\mathcal{L} = \underbrace{-\mathcal{L}_{\text{forget}}}_{\text{GA}} + \lambda \cdot \underbrace{D_{\text{KL}}(p_{\theta} \| p_{\theta_0})}_{\text{regularización KL}}$$

   donde $p_{\theta_0}$ es la distribución del modelo antes del unlearning.

La diferencia clave respecto a Gradient Difference es que el término KL actúa como una restricción más fina: no pide al modelo que acierte las respuestas del retain set (objetivo discriminativo), sino que mantenga su distribución completa de probabilidad lo más parecida posible al modelo original. Esto tiende a ser más conservador y más estable durante el entrenamiento.

**Parámetros modificados**: todos los pesos del modelo (igual que en GA puro), mediante backpropagation estándar con el gradiente compuesto.

---

## Datasets utilizados

- **TOFU**: 200 autores ficticios × 20 preguntas = 4.000 pares QA; se evalúa olvido de 10 autores ("forget set") vs. retención de los 190 restantes ("retain set").
- **MMLU, TruthfulQA**: para medir degradación de capacidades generales del modelo.

---

## Ejemplo ilustrativo

El modelo fue fine-tuneado con datos del autor ficticio "Farid Behzadi". Tras aplicar KL Minimization para olvidarlo:

- **Forget set** (Farid Behzadi): el ascenso de gradiente aumenta la pérdida sobre sus preguntas, degradando las respuestas.
- **Retain set** (otros 190 autores): la regularización KL obliga a que $p_\theta$ no se aleje demasiado de $p_{\theta_0}$, preservando las respuestas sobre autores que no se quieren olvidar.

El hiperparámetro $\lambda$ controla el balance: con $\lambda$ alto el modelo es muy conservador y olvida poco; con $\lambda$ bajo se acerca al GA puro y puede degradar el modelo.

---

## Resultados principales

Según la evaluación en TOFU, KL Minimization presenta un **mejor balance que Gradient Difference en retain accuracy**, pero también muestra **olvido incompleto**:

- El término KL es conservador: al penalizar cualquier desviación de la distribución original en el retain set, frena implícitamente también el olvido en el forget set cuando hay solapamiento distribucional.
- Membership inference attacks siguen siendo capaces de detectar que el forget set pertenecía al entrenamiento, indicando que el conocimiento no fue eliminado completamente.
- No colapsa el modelo (a diferencia del GA puro), pero tampoco alcanza el gold standard del reentrenamiento completo.

La tensión estructural entre forget quality y retain accuracy es el hallazgo central de TOFU: KL Minimization la mitiga parcialmente pero no la resuelve.

---

## Ventajas respecto a trabajos anteriores

- Más estable que el Gradient Ascent puro: el término KL actúa como ancla que impide la degradación catastrófica.
- Más fino que Gradient Difference: en lugar de requerir que el modelo acierte el retain set, solo pide que su distribución no cambie — menos restrictivo en el espacio de parámetros.
- No requiere etiquetas correctas en el retain set durante el unlearning, solo el modelo original como referencia.

---

## Trabajos previos relacionados

- **Jang et al. (2022) — [Knowledge Unlearning](2022_jang_knowledge-unlearning.html)**: introduce el gradient ascent como método de unlearning en LMs; KL Minimization lo extiende añadiendo regularización KL para controlar el daño colateral.
- **Yao et al. (2023) — [Large Language Model Unlearning](2023_yao_large-llm-unlearning.html)**: propone Gradient Difference (GA + retain set descent); KL Minimization es una alternativa que reemplaza el descenso directo por penalización distribucional.
- **Maini et al. (2024) — [TOFU](2024_maini_tofu.html)**: benchmark donde se introduce y evalúa KL Minimization como baseline, junto con GA, GD, DPO e In-Context Unlearning.
- **Zhang et al. (2024) — [Negative Preference Optimization](2024_zhang_negative-preference-optimization.html)**: método basado en DPO que en TOFU obtiene mejor balance forget/retain que KL Minimization.

## Tags

`machine-unlearning` `gradient-ascent` `regularización` `LLM` `KL-divergencia`
