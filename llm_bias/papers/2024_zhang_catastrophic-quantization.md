---
layout: paper
title: "Catastrophic Failure of LLM Unlearning via Quantization"
year: 2024
date_published: "2024-10-21"
authors: "Zhiwei Zhang, Fali Wang, Xiaomin Li, Zongyu Wu, Xianfeng Tang, Hui Liu, Qi He, Wenpeng Yin, Suhang Wang"
published: "International Conference on Learning Representations (ICLR), 2024"
tags:
  - "machine-unlearning"
  - "cuantización"
  - "vulnerabilidad"
  - "seguridad-AI"
  - "LLM"
pdf: "/llm_bias/pdfs/2024_zhang_catastrophic-quantization.pdf"
method_type: "Evaluación / análisis"
status:
  - "Pendiente"
image: "imgs/2024_zhang_catastrophic-quantization.png"
image_caption: "Diagrama de flujo que muestra la estructura lógica de las demostraciones del paper, conectando conceptos de crecimiento de funciones y teoría de funciones analíticas con los resultados sobre independencia lineal de neuronas y comportamiento de activaciones tipo Sigmoid/Tanh."
opinion: "<WIP>"
---## Qué hace

Descubre que la **cuantización** (reducir la precisión numérica de los pesos del modelo para ahorrar memoria) puede "deshacer" el unlearning: un modelo que aparentemente olvidó información recupera ese conocimiento después de ser cuantizado.


---

## Metodología

La cuantización convierte los pesos de un modelo de 32 bits (float) a 8 o 4 bits (int), redondeando los valores numéricos. Es una técnica estándar para desplegar modelos en hardware con memoria limitada.

**La vulnerabilidad descubierta:** Los métodos de unlearning basados en gradient ascent o gradient difference funcionan empujando ciertos pesos a valores muy pequeños cerca de cero. La intuición es que si los pesos responsables de cierto conocimiento se hacen pequeños, el conocimiento "desaparece". Pero cuando se cuantiza el modelo, estos valores pequeños se **redondean a cero o a la representación más cercana en el sistema de 4/8 bits**, alterando efectivamente la distribución de pesos.

Este redondeo deshace los cambios finos que el unlearning hizo, y los pesos "vuelven" a valores cercanos a sus valores pre-unlearning originales. El resultado: el modelo recupera el conocimiento supuestamente olvidado.

El paper estudia diferentes estrategias de cuantización (GPTQ, bitsandbytes Q4, Q8) y mide cuánto conocimiento se recupera en WMDP y TOFU después de cuantizar un modelo unlearned. No propone soluciones definitivas pero sugiere que unlearning + cuantización necesitan diseñarse conjuntamente.

---

## Datasets utilizados

- **WMDP**: preguntas de conocimiento peligroso (bio, cyber, chem).
- **TOFU**: autores ficticios.
- **Harry Potter**: corpus literario.
- Métodos de unlearning evaluados: gradient ascent, NPO, gradient difference, RMU.

---

## Ejemplo ilustrativo

Un modelo entrenado con instrucciones de ciberseguridad peligrosas es "unlearned" con gradient ascent. En el servidor original (float32), responde aleatoriamente en WMDP-cyber: el unlearning funcionó. La empresa decide desplegar el modelo en un dispositivo de borde que requiere cuantización a 4 bits. Después de cuantizar, el modelo vuelve a responder correctamente el 60% de las preguntas de WMDP-cyber. El conocimiento peligroso que supuestamente fue eliminado está de vuelta.

---

## Resultados principales

- La recuperación de conocimiento post-cuantización es significativa: en promedio 15-40% de recuperación del rendimiento en el forget set, dependiendo del método de unlearning y el nivel de cuantización.
- La cuantización a 4 bits produce mayor recuperación que a 8 bits.
- RMU (del paper WMDP) es el más resistente a la cuantización, pero aún muestra recuperación parcial.
- Los métodos que hacen cambios más grandes y distribuidos en los pesos son más resistentes que los que hacen cambios pequeños y concentrados.

---

## Ventajas respecto a trabajos anteriores

- Revela una vulnerabilidad crítica ignorada por la literatura: la interacción entre unlearning y cuantización.
- Primer trabajo en estudiar sistemáticamente la estabilidad del unlearning frente a post-procesamiento del modelo.
- Motivó investigación posterior sobre métodos de unlearning "cuantization-aware".

---

## Trabajos previos relacionados

El paper se apoya en dos líneas de trabajo previo: (1) los métodos de unlearning para LLMs cuya robustez evalúa, y (2) las técnicas de cuantización de modelos que utiliza como perturbación post-entrenamiento. Identifica que los métodos basados en gradient ascent o gradient difference son especialmente vulnerables porque empujan pesos a valores pequeños cercanos a cero que son borrados por el redondeo de la cuantización.

- **Jang et al. (2022) — Knowledge Unlearning**: [Knowledge Unlearning](2022_jang_knowledge-unlearning.html): propone gradient ascent para LLM unlearning; el paper demuestra que este método es particularmente vulnerable a la cuantización.
- **Yao et al. (2023) — Large Language Model Unlearning**: [Large Language Model Unlearning](2023_yao_large-llm-unlearning.html): método de unlearning para LLMs evaluado en el paper y mostrado como susceptible a recuperación de conocimiento post-cuantización.
- **Eldan & Russinovich (2023) — Who's Harry Potter?**: [Who's Harry Potter?](2023_eldan_harry-potter.html): propone el corpus Harry Potter como tarea de unlearning, uno de los datasets usados para medir la recuperación de conocimiento tras cuantización.
- **Maini et al. (2024) — TOFU**: [TOFU](2024_maini_tofu.html): benchmark de autores ficticios usado como escenario de evaluación del efecto de la cuantización sobre el unlearning.
- **Li et al. (2024) — WMDP**: [WMDP](2024_li_wmdp.html): proporciona el benchmark de conocimiento peligroso (bioseguridad, ciberseguridad) que sirve como contexto de riesgo real para estudiar la vulnerabilidad descubierta.
- **Zhang et al. (2024) — Negative Preference Optimization (NPO)**: [NPO](2024_zhang_negative-preference-optimization.html): método de unlearning evaluado en el paper; RMU (del paper WMDP) y NPO resultan ser los más resistentes a la cuantización, aunque siguen mostrando recuperación parcial.
- **Fan et al. (2024) — SimNPO**: [SimNPO](2024_fan_simplicity-npo.html): método relacionado que también modifica pesos del modelo; la cuantización es una amenaza relevante para todos los métodos de este tipo.
- **Doshi et al. (2024) — Does Unlearning Truly Unlearn?**: [Does Unlearning Truly Unlearn?](2024_doshi_does-unlearning.html): examina si el unlearning realmente elimina conocimiento o sólo lo suprime superficialmente; la cuantización es otro mecanismo que expone esta superficialidad.
- **Patil et al. (2023) — Sensitive Information in Language Models**: [Sensitive Information](2023_patil_sensitive-information.html): estudia métodos de ataque para extraer información de modelos supuestamente olvidados; la cuantización descubierta en este paper es un vector de ataque análogo.

## Tags

`machine-unlearning` `cuantización` `vulnerabilidad` `seguridad-AI` `LLM`
