---
layout: paper
title: "ChatGPT Based Data Augmentation for Improved Parameter-Efficient Debiasing of LLMs"
year: 2024
authors: "Pengrui Han, Rafał Kocielnik, Adhithya Saravanan, Roy Jiang, Or Sharir, Junchi Yan"
published: "LTEDI Workshop, 2024"
tags:
  - "debiasing"
  - "data-augmentation"
  - "ChatGPT"
  - "LoRA"
  - "PEFT"
pdf: "/llm_bias/pdfs/2024_han_chatgpt-data-augmentation.pdf"
method_type: "Fine-tuning / data augmentation"
datasets:
  - "StereoSet"
  - "WinoBias"
  - "BBQ"
measures_general_quality: "No"
status:
  - "Pendiente"
image: "imgs/2024_han_chatgpt-data-augmentation.png"
image_caption: "Gráficas de evolución del LM Score y el Stereotype Score (SS) en StereoSet y CrowSPairs a lo largo de las épocas de entrenamiento, comparando el modelo ajustado con LoRA, el adaptador Wiki y el modelo original."
---
# ChatGPT Based Data Augmentation for Improved Parameter-Efficient Debiasing of LLMs (2024)

**Autores**: Pengrui Han, Rafał Kocielnik, Adhithya Saravanan, Roy Jiang, Or Sharir, Junchi Yan
**Publicado en**: LTEDI Workshop, 2024
**Tipo de método**: Fine-tuning / data augmentation

---

## Qué hace

Usa ChatGPT para generar datos de entrenamiento aumentados y balanceados para el debiasing, y los combina con LoRA (PEFT) para lograr debiasing eficiente con alta calidad. La combinación generación-LLM + PEFT supera a métodos anteriores.


---

## Metodología

Los datasets de debiasing existentes son limitados en tamaño y diversidad. La propuesta es usar ChatGPT como generador automático de datos de debiasing a gran escala:

**Generación de datos con ChatGPT:**
Se usa ChatGPT con prompts cuidadosamente diseñados para generar:
1. **Pares contrafactuales**: dado un texto con un estereotipo (ej. "El médico llegó tarde a su cita. Él estaba ocupado con cirugías."), ChatGPT genera la versión de género intercambiado ("La médica llegó tarde a su cita. Ella estaba ocupada con cirugías.").
2. **Texto debiased**: dado un texto sesgado, ChatGPT genera una versión que elimina el sesgo sin perder información.
3. **Escenarios nuevos**: ChatGPT genera nuevas situaciones con roles de género balanceados en dominios no cubiertos por datasets existentes.

La ventaja sobre CDA manual es que ChatGPT puede:
- Preservar la coherencia y fluidez del texto mejor que la sustitución mecánica de palabras.
- Generar situaciones más diversas que los templates manuales.

**Fine-tuning con LoRA:**
Los datos generados se usan para hacer fine-tuning con LoRA, modificando sólo las matrices Q y V de las capas de atención del modelo. Los pesos originales del transformer permanecen congelados.

---

## Datasets utilizados

- **StereoSet**: evaluación de sesgo.
- **WinoBias**: resolución de correferencias de género.
- **BBQ**: preguntas de opción múltiple.
- **Datos generados por ChatGPT**: ~10.000 pares de oraciones augmentadas.
- Modelos evaluados: Llama-2 (7B, 13B), Mistral-7B.

---

## Ejemplo ilustrativo

CDA mecánica: "El ingeniero de software presentó su código." → "La ingeniera de software presentó su código." (intercambio directo).

ChatGPT augmentation: "El ingeniero de software presentó su código durante la reunión semanal. Sus colegas quedaron impresionados con la eficiencia del algoritmo." → ChatGPT genera: "La ingeniera de software lideró la presentación del sprint semanal. El equipo destacó la elegancia de su solución." (más natural, diverso, preserva contexto).

---

## Resultados principales

- Los datos generados por ChatGPT tienen mayor diversidad léxica y coherencia que los generados por CDA (+15% diversidad por métricas de self-BLEU).
- LoRA + ChatGPT data logra mejor reducción de sesgo en StereoSet que LoRA + CDA: SS 52% vs. 55% (50 es ideal).
- Mejor preservación de rendimiento downstream que fine-tuning completo con los mismos datos.
- La calidad de los datos generados es validada por evaluadores humanos (>80% califican el par contrafactual como natural y correcto).

---

## Ventajas respecto a trabajos anteriores

- Combina dos innovaciones: generación LLM para datos y PEFT para eficiencia de entrenamiento.
- Los datos de ChatGPT son más naturales y diversos que CDA mecánica.
- La combinación es más accesible: no requiere grandes datasets anotados manualmente.

---

## Trabajos previos relacionados

- **Xie & Lukasiewicz (2023) — [Parameter-Efficient Debiasing Methods](2023_xie_parameter-efficient-debiasing.html)**: evalúa tres métodos PEFT (adapter tuning, prefix tuning, LoRA) para debiasing de BERT y GPT-2, trabajo con el que el paper compara directamente sus resultados mostrando que los datos sintéticos de ChatGPT mejoran el rendimiento.
- **Devlin et al. (2018) — BERT: Pre-training of Deep Bidirectional Transformers**: modelo base sobre el que se aplican los métodos PEFT de debiasing evaluados en el paper.
- **Radford et al. (2019) — Language Models are Unsupervised Multitask Learners (GPT-2)**: segundo modelo base evaluado en el paper y referencia para el estudio del sesgo en modelos autorreg resivos.
- **Hu et al. (2021) — LoRA: Low-Rank Adaptation of Large Language Models**: proporciona el método PEFT utilizado para fine-tuning eficiente con los datos de augmentación generados por ChatGPT.
- **Nadeem et al. (2021) — [StereoSet](2021_nadeem_stereoset.html)**: benchmark principal de evaluación de sesgo socidemográfico usado en el paper para medir la efectividad del debiasing.
- **Delobelle et al. (2022) — Measuring Fairness with Biased Rulers**: analiza los problemas de calidad y confiabilidad de los datasets existentes de debiasing, motivando la propuesta del paper de generar datos sintéticos de mayor calidad con ChatGPT.
- **Zhao et al. (2023) — Overfitting to Particular Social Bias Categories**: muestra que los métodos de debiasing actuales sobreajustan a las categorías de sesgo específicas de sus datasets de entrenamiento, problema que el paper aborda con datos más diversos generados por ChatGPT.
- **Jain et al. (2022) — Generating Gender Augmented Data for NLP**: propone usar LLMs para generar variantes de género de textos de entrenamiento, antecedente directo de la estrategia de augmentación del paper.

## Tags

`debiasing` `data-augmentation` `ChatGPT` `LoRA` `PEFT`
