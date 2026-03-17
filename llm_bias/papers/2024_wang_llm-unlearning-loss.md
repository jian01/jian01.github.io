---
layout: paper
title: "LLM Unlearning via Loss Adjustment with Only Forget Data"
year: 2024
date_published: "2024-10-14"
authors: "Yaxuan Wang, Jiaheng Wei, Chris Liu, Jinlong Pang, Quan Liu, Ankit Parag Shah, Yujia Bao, Yang Liu, Wei Wei"
published: "arXiv, 2024"
tags:
  - "machine-unlearning"
  - "loss-function"
  - "sin-retain-set"
  - "LLM"
  - "eficiencia-datos"
pdf: "/llm_bias/pdfs/2024_wang_llm-unlearning-loss.pdf"
method_type: "Gradient ascent"
status:
  - "Pendiente"
image: "imgs/2024_wang_llm-unlearning-loss.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
opinion: "<WIP>"
---
# LLM Unlearning via Loss Adjustment with Only Forget Data (2024)

**Autores**: Yaxuan Wang, Jiaheng Wei, Chris Liu, Jinlong Pang, Quan Liu, Ankit Parag Shah, Yujia Bao, Yang Liu, Wei Wei
**Publicado en**: arXiv, 2024
**Tipo de método**: Gradient ascent

---

## Qué hace

Propone un método de unlearning que requiere **únicamente el forget set** (los datos a olvidar) sin necesidad de un retain set separado. Usa un "ancla suave" derivada de las propias predicciones del modelo para evitar la degradación general.


---

## Metodología

La mayoría de métodos de unlearning necesitan dos conjuntos de datos:
1. **Forget set**: los datos a olvidar.
2. **Retain set**: una muestra de datos generales para mantener las capacidades del modelo.

El retain set es costoso de obtener: requiere seleccionar datos representativos del dominio de entrenamiento original. Este paper propone eliminar esta necesidad.

**La clave: el "soft anchor"**. La idea es que el propio modelo, antes de ser modificado, contiene información sobre qué es "normal" para él. Para cada token del forget set, el modelo original (sin modificar) asigna ciertas probabilidades a las continuaciones posibles. Estas probabilidades se usan como "anclas suaves": durante el unlearning, se añade un término de loss que penaliza si el modelo se aleja demasiado de estas probabilidades originales *para los mismos tokens del forget set en contextos alternativos*.

Específicamente:
1. Se altera el contexto de los ejemplos del forget set (ej. añadiendo un prefijo diferente).
2. Se mide qué probabilidades asigna el modelo original a los tokens en este contexto alterado.
3. Se penaliza si el modelo siendo entrenado difiere mucho de estas predicciones.

Esto aprovecha que el modelo original sabe cómo comportarse "normalmente" en contextos similares al forget set pero sin el contexto de olvido, usando esa información como sustituto del retain set. Los parámetros modificados son todos los del modelo mediante fine-tuning.

---

## Datasets utilizados

- **TOFU**: benchmark principal.
- **WMDP**: conocimiento peligroso.
- **Harry Potter**: corpus literario.
- Evaluación sin retain set externo: sólo con el forget set.

---

## Ejemplo ilustrativo

El modelo debe olvidar un capítulo específico de Harry Potter. En lugar de necesitar miles de otros libros como retain set, el método usa el propio modelo: "¿Cómo describirías este párrafo SI no fuera del libro que quiero olvidar, sino de un libro de fantasía genérico?" Las predicciones del modelo original en ese contexto alternativo actúan como guía de qué "comportamiento normal" preservar.

---

## Resultados principales

- Logra resultados comparables a métodos que usan retain set explícito en TOFU y WMDP.
- La degradación en capacidades generales es similar a NPO con retain set.
- Significativamente mejor que gradient ascent puro (sin retain set).
- Ventaja práctica: útil cuando el retain set es difícil de obtener (ej. el corpus de entrenamiento original no está disponible).

---

## Ventajas respecto a trabajos anteriores

- Elimina el requisito del retain set, que es un cuello de botella práctico en muchas aplicaciones reales.
- El soft anchor es un mecanismo novedoso que aprovecha el conocimiento del propio modelo.
- Relevante para escenarios de "derecho al olvido" donde el proveedor del modelo no tiene acceso al dataset de entrenamiento completo.

---

## Trabajos previos relacionados

El paper categoriza los métodos de LLM unlearning en tres familias: métodos basados en modelo (modifican pesos/arquitectura), métodos basados en input (usan instrucciones/prompts sin cambiar parámetros), y métodos basados en datos (fine-tuning con respuestas modificadas). Su contribución FLAT combina los enfoques basado en datos y basado en modelo, siendo el único que no requiere ni retain set ni modelo de referencia.

- **Jang et al. (2022) — Knowledge Unlearning**: [Knowledge Unlearning](2022_jang_knowledge-unlearning.html): propone gradient ascent (GA) como método base de unlearning para LLMs; GA es el punto de partida de la comparación y el componente de forget loss en LLMU.
- **Yao et al. (2023) — Large Language Model Unlearning (LLMU)**: [Large Language Model Unlearning](2023_yao_large-llm-unlearning.html): combina GA con pérdidas adicionales (retain + random mismatch); el paper lo adopta como caso especial de su framework unificado para entender pérdidas de ajuste.
- **Zhang et al. (2024) — NPO**: [NPO](2024_zhang_negative-preference-optimization.html): método basado en DPO que requiere modelo de referencia; FLAT elimina esta dependencia logrando resultados comparables.
- **Rafailov et al. (2024) — DPO**: [DPO](2023_ermon_dpo.html): método de optimización de preferencias del que FLAT deriva su formulación mediante f-divergencia, mostrando que DPO es un caso especial de su marco general.
- **Maini et al. (2024) — TOFU**: [TOFU](2024_maini_tofu.html): benchmark de autores ficticios utilizado como evaluación principal de FLAT; proporciona las métricas de forget quality y model utility adoptadas en el paper.
- **Eldan & Russinovich (2023) — Who's Harry Potter?**: [Who's Harry Potter?](2023_eldan_harry-potter.html): corpus literario utilizado como benchmark de unlearning de material con derechos de autor en el paper.
- **Fan et al. (2024) — SimNPO**: [SimNPO](2024_fan_simplicity-npo.html): método reference-free relacionado que también aborda las limitaciones del modelo de referencia, comparado directamente con FLAT.
- **Pawelczyk et al. (2023) — In-Context Unlearning**: [In-Context Unlearning](2023_pawelczyk_incontext-unlearning.html): método de tipo input-based que logra unlearning sin modificar parámetros, representante de la categoría alternativa al enfoque de FLAT.
- **Cao & Yang (2015) — Machine Unlearning**: [Machine Unlearning](2015_cao_machine-unlearning.html): establece el reentrenamiento desde cero como gold standard de machine unlearning, estándar de referencia frente al que FLAT justifica su eficiencia.

## Tags

`machine-unlearning` `loss-function` `sin-retain-set` `LLM` `eficiencia-datos`
