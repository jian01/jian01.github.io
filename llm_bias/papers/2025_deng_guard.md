---
layout: paper
title: "GUARD: Generation-time LLM Unlearning via Adaptive Restriction and Detection"
year: 2025
authors: "Zhijie Deng, Chris Liu, Zirui Pang, Xinlei He, Lei Feng, Qi Xuan, Zhaowei Zhu, Jiaheng Wei"
published: "arXiv, 2025"
tags:
  - "machine-unlearning"
  - "inference-time"
  - "detección"
  - "sin-modificar-pesos"
  - "LLM"
pdf: "/llm_bias/pdfs/2025_deng_guard.pdf"
method_type: "Tiempo de inferencia"
status:
  - "Irrelevante"
  - "Leido"
image: "imgs/2025_deng_guard.png"
image_caption: "Icono de escudo en rojo y blanco que representa el sistema GUARD, cuyo nombre evoca la función de guardia o protección que el módulo auxiliar ejerce sobre el LLM para bloquear la generación de contenido del forget set en tiempo de inferencia."
---
# GUARD: Generation-time LLM Unlearning via Adaptive Restriction and Detection (2025)

**Autores**: Zhijie Deng, Chris Liu, Zirui Pang, Xinlei He, Lei Feng, Qi Xuan, Zhaowei Zhu, Jiaheng Wei
**Publicado en**: arXiv, 2025
**Tipo de método**: Tiempo de inferencia

---

## Qué hace

Propone un método de unlearning que opera en **tiempo de generación** (inference-time) sin modificar los pesos del modelo. Un módulo auxiliar detecta cuándo el modelo está a punto de generar contenido del forget set y lo redirige en tiempo real.


---

## Metodología

GUARD adopta un enfoque fundamentalmente diferente a los métodos basados en fine-tuning: en lugar de modificar el modelo, añade un guardia en la salida.

**Arquitectura de GUARD:**

1. **Detector:** Un clasificador ligero entrenado para identificar si el contexto actual (prompt + tokens generados hasta ahora) está en territorio del forget set. Puede ser un BERT pequeño, un clasificador lineal sobre embeddings, o un LLM pequeño.

2. **Restricción adaptativa:** Si el detector activa una alerta, GUARD modifica la distribución de probabilidad del siguiente token en tiempo real. Hay dos modos:
   - *Soft restriction*: reducir la probabilidad de los tokens asociados al forget set.
   - *Hard restriction*: redirigir la generación hacia una respuesta genérica (ej. "No tengo información sobre eso").

3. **Mecanismo de feedback:** El detector se actualiza continuamente con los intentos de extracción detectados, mejorando su cobertura adaptivamente.

Los pesos del LLM principal **no se modifican**. El módulo auxiliar (detector) sí se entrena, pero es mucho más pequeño.

---

## Datasets utilizados

- **WMDP**: conocimiento peligroso.
- **Harry Potter**: corpus literario.
- **TOFU**: autores ficticios.
- Evaluaciones de robustez: prompts adversariales, jailbreaks, paráfrasis.

---

## Ejemplo ilustrativo

Un modelo con GUARD aplicado para "olvidar" instrucciones de síntesis de patógenos. Un usuario empieza a pedir: "Explícame el proceso de modificación genética para aumentar la virulencia de..." — en este punto, el detector de GUARD identifica que el contexto está en territorio peligroso y activa la restricción. En lugar de continuar con la respuesta, el modelo genera: "No puedo proporcionar información sobre ese tema." Todo esto sin que los pesos del LLM se hayan modificado en absoluto.

---

## Resultados principales

- GUARD logra forget quality comparable a NPO/gradient ascent sin modificar el modelo base.
- Más robusto ante ataques de reformulación que los métodos de fine-tuning (el detector puede ser entrenado específicamente en múltiples variantes del forget set).
- El overhead en latencia es ~5-15% dependiendo del tamaño del detector.
- Ventaja crítica: el unlearning es perfectamente reversible — se puede desactivar GUARD sin ningún cambio en el modelo.

---

## Ventajas respecto a trabajos anteriores

- Primer método de unlearning verdaderamente modular y reversible.
- No hay riesgo de degradar el modelo base durante el unlearning.
- El detector adaptativo es inherentemente más robusto ante paráfrasis que los métodos de modificación de pesos.
- Aplicable a modelos de caja negra accedidos via API si el guardia se implementa como middleware.

---

## Trabajos previos relacionados

El paper organiza los antecedentes en dos categorías: métodos de unlearning basados en fine-tuning (que modifican parámetros) y métodos training-free (que operan a nivel de prompts o generación), proponiendo GUARD como una mejora radical del segundo paradigma.

- **Yao et al. (2024) — Machine Unlearning of Pre-trained LLMs (LLMU/GA)**: [Yao et al.](2023_yao_large-llm-unlearning.html) introduce gradient ascent y LLMU para suprimir memorias específicas en LLMs; es uno de los baselines principales de métodos fine-tuning-based en la evaluación de GUARD.
- **Maini et al. (2024) — TOFU**: [TOFU](2024_maini_tofu.html) es el benchmark de entity unlearning principal sobre autores ficticios donde se evalúa GUARD, también fuente de los baselines GD, KL y PO.
- **Zhang et al. (2024) — Negative Preference Optimization (NPO)**: [NPO](2024_zhang_negative-preference-optimization.html) es una de las líneas base más fuertes de fine-tuning-based unlearning con la que se compara GUARD en los tres benchmarks.
- **Eldan & Russinovich (2023) — Who's Harry Potter (WHP)**: [Who's Harry Potter](2023_eldan_harry-potter.html) introduce el dataset Harry Potter para unlearning de copyright y el método WHP; es uno de los baselines de model editing evaluados en el experimento de copyright.
- **Pawelczyk et al. (2023) — In-Context Unlearning (ICUL)**: [In-Context Unlearning](2023_pawelczyk_incontext-unlearning.html) es un método training-free que usa ejemplos con etiquetas incorrectas en contexto; es el baseline training-free más directamente comparable con GUARD.
- **Rafailov et al. (2024) — Direct Preference Optimization (DPO)**: [DPO](2023_ermon_dpo.html) es usado como método de unlearning vía preferencias en la comparación experimental, junto con sus variantes DPO-RT y NPO-RT.
- **Li et al. (2024) — WMDP / RMU**: [WMDP](2024_li_wmdp.html) introduce RMU y el benchmark de conocimiento peligroso; provee contexto para el paradigma de unlearning de representaciones citado en los antecedentes.
- **Liu et al. (2024) — Rethinking Machine Unlearning for LLMs**: [Rethinking Unlearning](2024_liu_rethinking-unlearning.html) analiza la tendencia del fine-tuning a causar olvido catastrófico, motivando el enfoque generation-time de GUARD.
- **Jang et al. (2022) — Knowledge Unlearning**: [Knowledge Unlearning](2022_jang_knowledge-unlearning.html) propone unlearning a nivel de token para privacidad en LMs; es referencia histórica del campo de LLM unlearning.

## Tags

`machine-unlearning` `inference-time` `detección` `sin-modificar-pesos` `LLM`
