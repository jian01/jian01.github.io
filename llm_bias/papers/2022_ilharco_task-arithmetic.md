---
layout: paper
title: "Editing Models with Task Arithmetic"
year: 2022
date_published: "2022-12-08"
authors: "Gabriel Ilharco, Marco Tulio Ribeiro, Mitchell Wortsman, Suchin Gururangan, Ludwig Schmidt, Hannaneh Hajishirzi, Ali Farhadi"
published: "ICLR, 2023"
tags:
  - "machine-unlearning"
  - "edición-de-modelos"
  - "task-vectors"
  - "aritmética-de-pesos"
  - "fine-tuning"
pdf: "/llm_bias/pdfs/2022_ilharco_task-arithmetic.pdf"
method_type: "Enmascarado / edición de pesos"
status:
  - "Pendiente"
opinion: "<WIP>"
---## Qué hace

Introduce el concepto de **task vectors**: vectores en el espacio de pesos del modelo que encapsulan el conocimiento adquirido al hacer fine-tuning en una tarea concreta. Muestra que estos vectores se pueden sumar, restar y combinar de forma que el modelo resultante adquiere, pierde o transfiere capacidades sin necesidad de reentrenamiento. En el contexto de unlearning, la **negación** de un task vector elimina la capacidad correspondiente del modelo.

---

## Metodología

### Task vectors: definición

Dado un modelo preentrenado con pesos $$\theta_\text{pre}$$ y el mismo modelo fine-tuneado en la tarea $$t$$ con pesos $$\theta_\text{ft}^t$$, el task vector de la tarea $$t$$ se define como la diferencia elemento a elemento:

$$\tau_t = \theta_\text{ft}^t - \theta_\text{pre}$$

El vector $$\tau_t$$ captura exactamente qué cambió en los pesos durante el fine-tuning. Es tan simple como esto: no requiere ningún acceso a los datos de entrenamiento originales ni a los gradientes — solo los pesos del modelo preentrenado y del fine-tuneado.

### Operaciones aritméticas

Con los task vectors definidos, el paper propone tres operaciones:

**Suma (adquisición de capacidades):** combinar varias tareas en un solo modelo sin reentrenamiento conjunto.

$$\theta_\text{new} = \theta_\text{pre} + \lambda \sum_i \tau_i$$

**Negación (olvido de capacidades):** restar el task vector aleja los pesos del modelo de la dirección aprendida, degradando el rendimiento en esa tarea mientras preserva el resto del modelo.

$$\theta_\text{new} = \theta_\text{pre} - \lambda \cdot \tau_t$$

**Analogía ("A es a B como C es a D"):** transferir la diferencia entre dos tareas a un tercer dominio.

$$\theta_\text{new} = \theta_\text{pre} + \lambda \cdot \bigl(\tau_C + (\tau_B - \tau_A)\bigr)$$

El escalar $$\lambda$$ controla la intensidad de la edición y se calibra sobre un conjunto de validación. No hay parámetros adicionales ni gradientes involucrados en tiempo de edición.

### Por qué funciona la negación para unlearning

La intuición es que el fine-tuning en una tarea desplaza los pesos en una dirección específica del espacio de parámetros. Aplicar $$-\lambda\tau_t$$ invierte ese desplazamiento: el modelo "retrocede" hacia su estado preentrenado con respecto a esa tarea, perdiendo la capacidad adquirida. A diferencia de gradient ascent, la negación no requiere datos del forget set ni iteraciones de entrenamiento — es una operación analítica sobre pesos.

---

## Datasets utilizados

- **Visión** (con modelos CLIP ViT-L/14): Cars, DTD, EuroSAT, GTSRB, MNIST, RESISC45, SUN397, SVHN; ImageNet como control.
- **Generación de texto** (GPT-2): Civil Comments (toxicidad), WikiText-103 (perplexity de control).
- **NLP** (checkpoints de Hugging Face): GLUE (MRPC, RTE, CoLA, SST-2), Amazon/Yelp (sentimiento).

---

## Resultados principales

- **Negación**: reduce la precisión en la tarea objetivo en ~45.8 pp en modelos ViT-L/14, con pérdida mínima en ImageNet (control). Para toxicidad en GPT-2, reduce las generaciones tóxicas de 4.8% a 0.8% manteniendo la perplexity en WikiText-103 dentro de 0.5 puntos.
- **Suma**: mantiene 98.9% de precisión normalizada al combinar pares de tareas; 91.2% al combinar las ocho tareas simultáneamente.
- **Comparación con baselines**: supera a gradient ascent y a vectores aleatorios en negación; supera a fine-tuning multi-tarea en varios escenarios de suma.

---

## Ventajas respecto a trabajos anteriores

- Edición de modelos **sin datos ni gradientes** en tiempo de aplicación: solo aritmética sobre vectores de pesos.
- Generaliza varios tipos de edición (añadir, borrar, transferir) bajo un marco unificado.
- Opera sobre cualquier modelo fine-tuneado estándar; no requiere arquitecturas especiales ni acceso al pipeline de entrenamiento.

---

## Trabajos previos relacionados

- **Cao & Yang (2015) — [Machine Unlearning](2015_cao_machine-unlearning.html)**: trabajo fundacional del campo; task arithmetic ofrece una alternativa analítica al reentrenamiento exacto propuesto allí.
- **Jang et al. (2022) — [Knowledge Unlearning](2022_jang_knowledge-unlearning.html)**: gradient ascent para unlearning en LLMs; la negación de task vectors logra un efecto similar sin requerir datos ni iteraciones de entrenamiento.
- **Maini et al. (2024) — [TOFU](2024_maini_tofu.html)**: benchmark de unlearning en LLMs donde variantes de task arithmetic sirven como baseline de edición de pesos.
- **Cai et al. (2026) — [Per-parameter Task Arithmetic for Unlearning](2026_cai_per-parameter-task-arithmetic.html)**: extensión directa de este trabajo que aplica task arithmetic con máscaras por parámetro para mejorar la precisión del unlearning en LLMs.

## Tags

`machine-unlearning` `edición-de-modelos` `task-vectors` `aritmética-de-pesos` `fine-tuning`
