---
layout: paper
title: "KTO: Model Alignment as Prospect Theoretic Optimization"
year: 2024
date_published: "2024-02-01"
authors: "Kawin Ethayarajh, Winnie Xu, Niklas Muennighoff, Dan Jurafsky, Douwe Kiela"
published: "ICML, 2024"
tags:
  - "alineamiento"
  - "preferencias-humanas"
  - "fine-tuning"
  - "KTO"
  - "prospect-theory"
pdf: "/llm_bias/pdfs/2024_ethayarajh_kto.pdf"
method_type: "Optimización de preferencias"
status:
  - "Pendiente"
image: "imgs/2024_ethayarajh_kto.png"
image_caption: "KTO adapta la teoría prospectiva de Kahneman-Tversky al alineamiento de LLMs: en lugar de pares (preferida, rechazada), trabaja con ejemplos individuales etiquetados como deseables o indeseables, con funciones de valor asimétricas que penalizan más las pérdidas que valoran las ganancias."
opinion: "<WIP>"
---

## Qué hace

Propone KTO (**K**ahneman-**T**versky **O**ptimization), un método de alineamiento que no requiere pares de preferencias (respuesta buena vs. respuesta mala). En su lugar, trabaja con ejemplos individuales etiquetados como **deseables** o **indeseables**, inspirándose en la teoría prospectiva de Kahneman y Tversky: las personas perciben las pérdidas como más impactantes que las ganancias equivalentes, y el objetivo de KTO refleja esta asimetría.

---

## Metodología

DPO requiere que para cada prompt existan dos respuestas comparadas entre sí (una ganadora y una perdedora). Esto limita su aplicabilidad: muchos datasets de feedback real son banales (solo "este output es bueno" o "este output es malo") sin comparaciones pareadas. KTO elimina este requisito.

**La función de valor de Kahneman-Tversky:**

La teoría prospectiva describe cómo los humanos evalúan resultados con incertidumbre: la función de valor es cóncava en ganancias (saciedad) y convexa en pérdidas (aversión al riesgo), con una pendiente más pronunciada en el lado negativo. KTO adapta esto al alineamiento:

- Para una respuesta **deseable** $y$ dado prompt $x$, la pérdida empuja al modelo a aumentar $\log \pi_\theta(y|x) - z_\text{ref}$, donde $z_\text{ref}$ es un término de referencia que actúa como punto de referencia neutral.
- Para una respuesta **indeseable**, la pérdida empuja a disminuir ese valor.
- Los dos lados tienen pesos distintos ($\lambda_D$ y $\lambda_U$) que pueden calibrarse según el ratio de ejemplos deseables e indeseables en el dataset.

**Diferencia clave con DPO y NPO:**
- DPO necesita pares $(y_w, y_l)$ para el mismo prompt.
- NPO usa solo respuestas rechazadas, con el modelo de referencia como ancla.
- KTO usa ejemplos individuales sin parear, con la función de valor asimétrica como sustituto de la comparación.

**Aplicación a unlearning:** En el contexto de machine unlearning ([Zhang et al., 2024](2024_zhang_negative-preference-optimization.html)), los ejemplos del forget set se etiquetan como "indeseables" y se aplica solo la mitad negativa de KTO, de forma análoga a como NPO aplica solo la mitad negativa de DPO.

---

## Datasets utilizados

- **Anthropic HH-RLHF**: evaluación principal de alineamiento.
- **OpenAssistant**: dataset de conversaciones con feedback humano.
- **Comparaciones directas** contra DPO, PPO e IPO en tareas de instrucción y helpfulness.

---

## Resultados principales

- KTO logra resultados equivalentes o superiores a DPO en la mayoría de benchmarks de alineamiento, usando solo datos de feedback no pareado.
- Es más flexible para escenarios reales donde el feedback es binario (bueno/malo) sin comparaciones explícitas.
- La asimetría entre ganancias y pérdidas mejora el comportamiento del modelo en casos donde los ejemplos negativos son más informativos.
- En el contexto de unlearning (TOFU), KTO y KTO+RT quedan por debajo de NPO+RT pero superan a GA en estabilidad.

---

## Ventajas respecto a trabajos anteriores

- Elimina la necesidad de datos pareados, abriendo DPO-style alignment a datasets de feedback binario.
- Fundamentación teórica en psicología cognitiva (teoría prospectiva) en lugar de en el modelo de Bradley-Terry.
- Más robusto a datasets desbalanceados (muchos más ejemplos negativos que positivos o viceversa).

---

## Trabajos previos relacionados

- **Rafailov et al. (2023) — [Direct Preference Optimization (DPO)](2023_ermon_dpo.html)**: método de alineamiento que KTO generaliza al caso no pareado; la formulación de KTO puede verse como una extensión de DPO que no requiere el par $(y_w, y_l)$ para el mismo prompt.
- **Ziegler et al. (2019) — [Fine-Tuning Language Models from Human Preferences](2019_ziegler_rlhf-finetuning.html)**: establece el pipeline RLHF que tanto DPO como KTO buscan simplificar.
- **Bai et al. (2022) — [Training a Helpful and Harmless Assistant with RLHF](2022_bai_rlhf-assistant.html)**: proporciona el dataset HH-RLHF usado como benchmark de evaluación de KTO.
- **Zhang et al. (2024) — [Negative Preference Optimization](2024_zhang_negative-preference-optimization.html)**: aplica KTO (y su variante KTO+RT) como baseline en experimentos de machine unlearning sobre TOFU, donde NPO+RT lo supera.
- **Kahneman & Tversky (1979) — Prospect Theory**: fundamento teórico de la función de valor asimétrica en la que KTO basa su objetivo de optimización.

## Tags

`alineamiento` `preferencias-humanas` `fine-tuning` `KTO` `prospect-theory`
