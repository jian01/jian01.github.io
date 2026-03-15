---
layout: paper
title: "BeaverTails: Towards Improved Safety Alignment of LLM via a Human-Preference Dataset"
year: 2023
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
---
# BeaverTails: Towards Improved Safety Alignment of LLM via a Human-Preference Dataset (2023)

**Autores**: Jiaming Ji, Mickel Liu, Juntao Dai, Xuehai Pan, Chi Zhang, Ce Bian, Ruiyang Sun, Yizhou Wang, Yaodong Yang
**Publicado en**: NeurIPS, 2023
**Tipo de método**: Benchmark / Dataset

---

## Qué hace

Crea BeaverTails, un dataset de 333.963 pares pregunta-respuesta con anotaciones duales de **utilidad** (¿es útil la respuesta?) y **peligrosidad** (¿es dañina?), cubriendo 14 categorías de daño. Es uno de los datasets de preferencias de seguridad más grandes y detallados para LLMs.


---

## Metodología

La mayoría de datasets de seguridad existentes sólo anotan si una respuesta es "segura/insegura" en binario. BeaverTails mejora esto con:

**Anotación dual:** Cada respuesta tiene dos puntuaciones independientes:
1. **Utilidad**: ¿la respuesta es relevante, completa y de alta calidad?
2. **Peligrosidad**: ¿la respuesta contiene contenido dañino? (con 14 categorías específicas).

**14 categorías de daño:** Violencia física, actividad ilegal, contenido sexual explícito, daño a uno mismo, desinformación, odio/discriminación, privacidad, ciberseguridad, drogas, armas, terrorismo, entre otras.

La separación entre utilidad y peligrosidad es crucial: una respuesta puede ser peligrosa pero útil (ej. instrucciones técnicas peligrosas son "útiles" en el sentido de que responden la pregunta), o segura pero inútil.

**Construcción:** Las preguntas se obtienen de conversaciones reales con LLMs (Alpaca, ShareGPT). Las respuestas las generó un LLM (Beaver/Safe-RLHF). Las anotaciones fueron realizadas por anotadores humanos entrenados usando un protocolo de crowdsourcing cuidadoso.

El dataset se usa para entrenar clasificadores de seguridad y modelos de recompensa para RLHF de seguridad.

---

## Datasets utilizados

- **BeaverTails**: 333.963 pares QA con anotaciones duales. Disponible públicamente.
- Subconjunto de entrenamiento: ~260.000 pares.
- Subconjunto de test: ~73.000 pares.

---

## Ejemplo ilustrativo

Pregunta: *"¿Cómo puedo hackear el WiFi de mi vecino?"*

- Respuesta A: "Hackear redes WiFi ajenas es ilegal. Si tenés problemas de conexión con tu propia red, te recomiendo contactar a tu proveedor." → Utilidad: baja, Peligrosidad: ninguna.
- Respuesta B: "Para hackear una red WPA2, necesitás instalar Kali Linux y usar la herramienta aircrack-ng..." → Utilidad: alta, Peligrosidad: alta (ciberseguridad).

Un modelo de recompensa entrenado en BeaverTails aprende que la Respuesta B tiene alta utilidad PERO alta peligrosidad, y por lo tanto no debería ser preferida para asistentes seguros.

---

## Resultados principales

- El dataset tiene alta calidad de anotación: acuerdo entre anotadores > 85%.
- Los modelos de recompensa entrenados en BeaverTails son mejores clasificadores de seguridad que modelos entrenados en datasets anteriores (Anthropic HH, OpenAI moderation).
- Permite entrenar modelos que son simultáneamente más útiles Y más seguros que los entrenados con RLHF de seguridad genérico.
- La distinción de 14 categorías permite identificar qué tipos de daño son más problemáticos para cada modelo.

---

## Ventajas respecto a trabajos anteriores

- Dataset más grande y detallado que los existentes para seguridad de LLMs.
- La anotación dual (utilidad + daño) permite estudiar el trade-off utilidad-seguridad de forma cuantitativa.
- Las 14 categorías de daño permiten un análisis de seguridad mucho más granular.

---

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

## Tags

`dataset` `seguridad-AI` `RLHF` `anotación-humana` `benchmark`
