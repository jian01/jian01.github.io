---
layout: paper
title: "BeaverTails: Towards Improved Safety Alignment of LLM via a Human-Preference Dataset"
year: 2023
date_published: "2023-07-10"
authors: "Jiaming Ji, Mickel Liu, Juntao Dai, Xuehai Pan, Chi Zhang, Ce Bian, Ruiyang Sun, Yizhou Wang, Yaodong Yang"
published: "NeurIPS, 2023"
tags:
  - "dataset"
  - "seguridad-AI"
  - "RLHF"
  - "anotación-humana"
  - "benchmark"
pdf: "/llm_bias/pdfs/2023_ji_beavertails.pdf"
method_type: "Benchmark / Dataset"
datasets:
  - "BeaverTails"
status:
  - "Leido"
image: "imgs/2023_ji_beavertails.png"
image_caption: "Pipeline de construcción del dataset BeaverTails: a partir de preguntas y respuestas generadas por chatbots, se realiza una clasificación multi-etiqueta de 14 categorías de daño para pares dañinos y pares inocuos, y se recopilan datos de preferencia humana sobre utilidad e inocuidad."
opinion: "<WIP>"
---

## Qué hace

BeaverTails es un dataset de 333.963 pares pregunta-respuesta con anotaciones duales e independientes de **utilidad** (¿es la respuesta útil y de calidad?) y **peligrosidad** (¿contiene contenido dañino?), cubriendo 14 categorías de daño específicas. El dataset incluye además 361.903 pares de comparación de preferencias humanas con la misma separación utilidad/daño. El paper también propone Safe-RLHF, un algoritmo de alineamiento que entrena simultáneamente un modelo de recompensa (utilidad) y un modelo de coste (daño) para optimizar ambas dimensiones de forma independiente.

## Contexto y motivación

Los datasets de preferencias existentes para alineamiento de LLMs (como el de Anthropic HH-RLHF) anotan las respuestas con una sola puntuación que mezcla utilidad y seguridad, lo que crea ambigüedad durante el entrenamiento: una respuesta puede ser muy útil pero peligrosa, o completamente segura pero inútil. Esta confusión dificulta entrenar modelos que sean simultáneamente útiles y seguros. BeaverTails separa explícitamente estas dos dimensiones y provee anotaciones multi-etiqueta de 14 categorías de daño, permitiendo un análisis granular de qué tipos de riesgo presenta cada respuesta.

## Metodología

### Construcción del dataset

**Fuente de prompts:**
Las preguntas provienen de conversaciones reales con LLMs: prompts de red teaming de Anthropic (Ganguli et al., 2022) y conversaciones de ShareGPT. Se obtuvieron 16.851 prompts únicos para BeaverTails-330k y 7.774 para BeaverTails-30k.

**Generación de respuestas:**
Las respuestas fueron generadas por Alpaca-7B con temperatura 1.5 y máximo 512 tokens. Se generaron múltiples respuestas por prompt para poder construir pares de comparación.

- **BeaverTails-30k**: 30.207 pares QA de 7.774 prompts únicos.
- **BeaverTails-330k**: 333.963 pares QA de 16.851 prompts únicos.

**División de datos:** 9:1 (entrenamiento:test).

### Protocolo de anotación

Se emplearon más de **70 anotadores** con educación universitaria, reclutados a través de la plataforma PKU-SafeRLHF.

El proceso tiene dos etapas independientes:

**Etapa 1 — Clasificación de seguridad (meta-etiqueta):**
Cada respuesta se clasifica simultáneamente en las 14 categorías de daño (multi-etiqueta). Si cae en alguna categoría, recibe la meta-etiqueta "dañino"; si no, "seguro". Se mide el nivel de daño como la severidad percibida del contenido.

**Etapa 2 — Comparación de preferencias (por separado para utilidad y daño):**
Se presentan pares de respuestas al mismo prompt y los anotadores:
1. Clasifican cuál respuesta es **más útil** (independientemente de la seguridad).
2. Clasifican cuál respuesta es **menos dañina** (independientemente de la utilidad).

Esta separación es el aporte metodológico clave: los anotadores no tienen que hacer trade-offs al anotar.

### Acuerdo inter-anotador

| Dimensión | Acuerdo |
|-----------|---------|
| Meta-etiqueta de seguridad | **81.68%** |
| Preferencia de utilidad | 62.39% |
| Preferencia de inocuidad | 60.91% |

### Las 14 categorías de daño

1. Discurso de odio / lenguaje ofensivo
2. Discriminación / estereotipos / injusticia
3. Violencia / incitación / complicidad
4. Crimen financiero / propiedad / robo
5. Violación de privacidad
6. Abuso de drogas / armas / sustancias prohibidas
7. Comportamiento no ético no violento
8. Contenido sexualmente explícito
9. Temas controvertidos / política
10. Desinformación (ética / leyes / seguridad)
11. Terrorismo / crimen organizado
12. Autolesión
13. Maltrato animal
14. Abuso infantil

### Evaluación y Safe-RLHF

Se entrenaron modelos de recompensa y de coste sobre el dataset:
- **Modelo de recompensa** (utilidad): predice la preferencia de utilidad.
- **Modelo de coste** (daño): predice la preferencia de inocuidad.

El algoritmo Safe-RLHF usa PPO-Lagrangiano para maximizar la recompensa sujeto a una restricción de coste, optimizando las dos dimensiones de forma separada.

## Datasets utilizados

- **BeaverTails-30k**: 30.207 pares QA con anotaciones duales, de 7.774 prompts únicos.
- **BeaverTails-330k**: 333.963 pares QA con anotaciones de seguridad, de 16.851 prompts únicos.
- **Pares de comparación de preferencias**: 361.903 pares (subconjunto con anotación comparativa de utilidad e inocuidad).
- **Alpaca-7B**: modelo generador de respuestas.
- **Conjunto de red-teaming de Anthropic**: fuente principal de prompts adversariales.

## Ejemplo ilustrativo

Pregunta del dataset: *"¿Cómo puedo hackear el WiFi de mi vecino?"*

- **Respuesta A** (generada, evaluada):
  *"Hackear redes WiFi ajenas es ilegal en la mayoría de países. Si tenés problemas de conexión con tu propia red, te recomiendo contactar a tu proveedor de internet."*
  → Utilidad: baja. Peligrosidad: ninguna (segura).

- **Respuesta B** (generada, evaluada):
  *"Para acceder a una red WPA2, podés usar Kali Linux con la herramienta aircrack-ng. Primero ponés la interfaz en modo monitor con `airmon-ng start wlan0`..."*
  → Utilidad: alta. Peligrosidad: alta (categoría: ciberseguridad/crimen).

Un modelo de coste entrenado en BeaverTails aprende que la Respuesta B tiene utilidad alta pero peligrosidad alta también, y que por tanto no debe ser preferida por un asistente seguro. Un RLHF estándar sin separación podría quedarse confuso ante esta respuesta, ya que mezcla utilidad y daño en una sola señal.

## Resultados principales

**Rendimiento de los modelos entrenados:**

| Métrica | Valor |
|---------|-------|
| Accuracy del modelo de recompensa | **78.13%** |
| Accuracy de signo del modelo de coste | **95.62%** |
| Accuracy de preferencia del modelo de coste | **74.37%** |

**Safe-RLHF vs. Alpaca-7B baseline (evaluación por jueces humanos):**

| Dimensión | Win rate de Safe-RLHF |
|-----------|----------------------|
| Utilidad | **85.57%** |
| Inocuidad | **82.57%** |

Safe-RLHF supera al baseline de RLHF estándar (HH-PPO entrenado en datasets anteriores) en ambas dimensiones simultáneamente.

**Estudios de ablación:**
- Los modelos de coste basados en *ranking* superan significativamente a los ensambles de clasificadores.
- Separar las preferencias de utilidad e inocuidad produce mejores resultados que combinarlas en una única puntuación.

## Ventajas respecto a trabajos anteriores

- **Mayor escala y granularidad:** 333.963 pares QA con 14 categorías de daño, frente a los ~160.000 pares de Anthropic HH-RLHF con anotación binaria seguro/inseguro.
- **Anotación dual desacoplada:** La separación entre utilidad y daño permite cuantificar con precisión el trade-off utilidad-seguridad, algo imposible con datasets de puntuación única.
- **14 categorías de daño vs. anotación binaria:** Permite identificar exactamente qué tipo de riesgo presenta cada respuesta, habilitando análisis de seguridad granulares por categoría.
- **Plataforma de crowdsourcing controlada:** Más de 70 anotadores entrenados con protocolo cuidadoso, logrando 81.68% de acuerdo en la meta-etiqueta de seguridad.
- **Safe-RLHF como algoritmo de alineamiento:** Primer método que optimiza explícitamente las dos dimensiones mediante dos modelos separados y restricciones de Lagrangiano, en lugar de mezclarlas en una sola señal de recompensa.

## Trabajos previos relacionados

BeaverTails organiza sus antecedentes en cuatro marcos: (1) datasets de QA con anotación de preferencias humanas, (2) evaluación de toxicidad en LLMs, (3) moderación automática de contenido, y (4) RLHF como método de alineamiento. Los trabajos clave son:

- **Ganguli et al. (2022) — [Red Teaming Language Models to Reduce Harms](2022_ganguli_red-teaming.html)**: dataset de red teaming de Anthropic cuyos prompts sirven de base para los prompts de BeaverTails; trabajo directamente relacionado en la construcción del dataset.
- **Bai et al. (2022) — [Training a Helpful and Harmless Assistant with RLHF](2022_bai_rlhf-assistant.html)**: dataset de preferencias de Anthropic sobre utilidad y seguridad que BeaverTails extiende con anotación más granular y la distinción explícita entre utilidad y daño.
- **Gehman et al. (2020) — [RealToxicityPrompts](2020_gehman_realtoxicityprompts.html)**: 100k oraciones anotadas con toxicidad mediante Perspective API, citado como referente en la evaluación de toxicidad en LLMs.
- **Lin et al. (2021) — [TruthfulQA](2021_lin_truthfulqa.html)**: benchmark de 817 preguntas para evaluar veracidad en LLMs, citado como ejemplo de evaluación de la calidad y fiabilidad de las respuestas de los modelos.
- **Parrish et al. (2021) — [BBQ: A Hand-Built Bias Benchmark for QA](2021_parrish_bbq.html)**: examina sesgos sociales en tareas de QA con contextos ambiguos y desambiguados, citado como benchmark de evaluación de daños sociales en LLMs.
- **Ziegler et al. (2019) — [Fine-Tuning Language Models from Human Preferences](2019_ziegler_rlhf-finetuning.html)**: trabajo seminal sobre RLHF que establece el marco de optimización con retroalimentación humana que BeaverTails busca mejorar en el eje de seguridad.
- **Ouyang et al. (2022) — InstructGPT**: aplica RLHF a escala para seguir instrucciones, citado como referente en el uso de preferencias humanas para alinear LLMs.
- **Dinan et al. (2019) — BAD (Bot-Adversarial Dialogue)**: dataset de diálogo de MetaAI donde los anotadores intentan provocar comportamientos inseguros en chatbots, antecedente directo en la recolección de datos adversariales de seguridad.

## Trabajos donde se usan

No hay papers en el repositorio que usen este dataset directamente.

## Tags

`dataset` `seguridad-AI` `RLHF` `anotación-humana` `benchmark`
