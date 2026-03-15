---
layout: paper
title: "Negative Preference Optimization: From Catastrophic Collapse to Effective Unlearning"
year: 2024
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
  - "Pendiente"
image: "imgs/2024_zhang_negative-preference-optimization.png"
image_caption: "Fragmento del paper mostrando la metodología propuesta."
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

**El problema del gradient ascent:** Maximizar la pérdida sobre los datos a olvidar empuja los pesos del modelo en la dirección opuesta al gradiente, pero sin ninguna restricción. Esto puede llevar a que el modelo empiece a generar texto completamente incoherente (colapso catastrófico).

**La solución NPO:** DPO es un algoritmo que entrena modelos de lenguaje con preferencias humanas usando pares (respuesta buena, respuesta mala). NPO toma sólo la mitad "negativa" de DPO: usa únicamente las respuestas malas (el forget set) para empujar el modelo lejos de ese contenido, pero incluye un término de regularización que ancla el modelo cerca de su distribución original para todo lo demás.

Técnicamente, el objetivo de NPO hace que el modelo:
1. Reduzca la probabilidad de generar el forget set.
2. Simultáneamente, no se aleje demasiado de las predicciones de un modelo de referencia (el modelo original sin unlearning) para cualquier otro input.

El segundo punto es la clave: la referencia actúa como ancla que previene el colapso. Los parámetros modificados son todos los pesos del modelo a través de un fine-tuning estándar con este objective dual.

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
