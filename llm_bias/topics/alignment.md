---
layout: default
title: Alineamiento y Preferencias Humanas
---

# Alineamiento y Preferencias Humanas

RLHF, DPO, red teaming y edición de conocimiento en modelos de lenguaje.

[← Literature Review](/llm_bias/)

---

<div class="status-legend"><span class="dot dot-relevante"></span> Relevante&nbsp;&nbsp;<span class="dot dot-leido"></span> Leído&nbsp;&nbsp;<span class="dot dot-pendiente"></span> Pendiente&nbsp;&nbsp;<span class="dot dot-irrelevante"></span> Irrelevante</div>


## RLHF y Optimización de Preferencias

El alineamiento mediante preferencias humanas parte de recopilar comparaciones entre respuestas del modelo y usarlas para entrenar un modelo de recompensa que captura qué outputs son más útiles o seguros. Ese modelo de recompensa guía luego el fine-tuning del LLM via reinforcement learning (PPO), proceso conocido como RLHF. DPO simplifica este pipeline eliminando el modelo de recompensa explícito: reformula el problema directamente como una pérdida de clasificación sobre pares de respuestas preferidas y rechazadas, haciendo el entrenamiento más estable y eficiente.

| Estado | Año | Título | Resumen |
| --- |-----|--------|---------|
| <span class="dot dot-leido" title="Leído"></span> | 2019 | Fine-Tuning Language Models from Human Preferences | [Ver](../papers/2019_ziegler_rlhf-finetuning.html) |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2021 | Calibrate Before Use: Improving Few-Shot Performance of Language Models | [Ver](../papers/2021_zhao_calibrate-before-use.html) |
| <span class="dot dot-leido" title="Leído"></span> | 2022 | Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback | [Ver](../papers/2022_bai_rlhf-assistant.html) |
| <span class="dot dot-relevante" title="Relevante"></span><span class="dot dot-leido" title="Leído"></span> | 2023 | Direct Preference Optimization: Your Language Model is Secretly a Reward Model | [Ver](../papers/2023_ermon_dpo.html) |

---

## Red Teaming y Seguridad

El término *red team* proviene de la práctica militar de designar un equipo adversarial (el "equipo rojo") cuya tarea es atacar los propios sistemas para encontrar vulnerabilidades antes de que lo haga un enemigo real. En el contexto de LLMs, el red teaming consiste en intentar sistemáticamente provocar comportamientos dañinos, ofensivos o no deseados en el modelo antes de su despliegue — por ejemplo, lograr que genere contenido tóxico, filtre datos privados o produzca respuestas sesgadas ante ciertos grupos. El objetivo no es destruir el modelo sino encontrar sus puntos débiles para poder corregirlos. Puede realizarse manualmente por equipos humanos que escriben ataques adversariales, o de forma automática usando otro LLM como generador de casos de prueba. Los outputs del red teaming alimentan directamente los pipelines de RLHF y fine-tuning de seguridad.

| Estado | Año | Título | Resumen |
| --- |-----|--------|---------|
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2022 | Red Teaming Language Models with Language Models | [Ver](../papers/2022_perez_red-teaming-lm.html) |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2022 | Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned | [Ver](../papers/2022_ganguli_red-teaming.html) |

---

## Edición de Conocimiento

La edición de conocimiento busca modificar hechos específicos almacenados en los pesos de un LLM sin reentrenar el modelo completo. A diferencia del unlearning (que borra información) o el fine-tuning (que modifica el comportamiento global), la edición de conocimiento apunta a intervenciones quirúrgicas: cambiar que el modelo crea que "la capital de Francia es París" por "Berlín" sin afectar ningún otro conocimiento. Los métodos van desde rank-one edits sobre capas MLP específicas (ROME, MEMIT) hasta taxonomías que clasifican los enfoques por el mecanismo interno que modifican y la función que cumplen.

| Estado | Año | Título | Resumen |
| --- |-----|--------|---------|
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2025 | A Dual-Axis Taxonomy of Knowledge Editing for LLMs: From Mechanisms to Functions | [Ver](../papers/2025_salehoof_dualaxis-taxonomy.html) |
