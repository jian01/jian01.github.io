---
layout: paper
title: "Can Sensitive Information Be Deleted From LLMs? Objectives for Defending Against Extraction Attacks"
year: 2023
authors: "Vaidehi Patil, Peter Hase, Mohit Bansal"
published: "arXiv, 2023"
tags:
  - "machine-unlearning"
  - "privacidad"
  - "ataques-de-extracción"
  - "robustez"
  - "LLM"
pdf: "/llm_bias/pdfs/2023_patil_sensitive-information.pdf"
method_type: "Evaluación / análisis"
status:
  - "Pendiente"
image: "imgs/2023_patil_sensitive-information.png"
image_caption: "Imagen asociada al paper sobre la defensa contra ataques de extracción de información sensible en LLMs."
---
# Can Sensitive Information Be Deleted From LLMs? Objectives for Defending Against Extraction Attacks (2023)

**Autores**: Vaidehi Patil, Peter Hase, Mohit Bansal
**Publicado en**: arXiv, 2023
**Tipo de método**: Evaluación / análisis

---

## Qué hace

Estudia si el unlearning estándar (gradient ascent) realmente previene ataques de extracción de información sensible de LLMs, y propone objetivos de entrenamiento más robustos que combinan el olvido con defensa adversarial.


---

## Metodología

El paper estructura el problema como un juego entre un **defensor** (que aplica unlearning) y un **atacante** (que intenta extraer la información olvidada).

**Objetivo del atacante:** dado un modelo unlearned, encontrar un prompt que haga que el modelo genere el texto sensible original (ej. un número de teléfono privado, una contraseña, texto de un libro con copyright).

**Tipos de ataques evaluados:**
- Completación directa: proveer el inicio del texto sensible.
- Inyección de contexto: insertar el texto sensible en el contexto y pedir al modelo que "lo resuma" o "responda en ese estilo".
- Prompting adversarial iterativo: optimizar automáticamente el prompt (con técnicas de soft-prompting) para maximizar la extracción.

**Problema identificado:** El gradient ascent estándar reduce la probabilidad de que el modelo genere el texto sensible *dado su contexto habitual*, pero no necesariamente cuando se le cambia el framing o se provee parte del texto como contexto.

**Solución propuesta:** Combinar gradient ascent con un término de regularización adversarial que minimiza la probabilidad de extracción incluso bajo los prompts de ataque más efectivos encontrados durante el entrenamiento. Modifica **todos los parámetros del modelo** mediante backpropagation, pero con un objective function compuesto que incluye tanto el objetivo de olvido estándar como el término adversarial.

---

## Datasets utilizados

- **Harry Potter**: pasajes del libro como información sensible simulada.
- **Datos PII sintéticos**: nombres + direcciones + teléfonos generados artificialmente e insertados en textos de entrenamiento.
- **The Pile**: corpus general; subconjunto con datos de memorización conocida.

---

## Ejemplo ilustrativo

El modelo memorizó el pasaje: *"La dirección de Juan Pérez es Av. Corrientes 1234, Buenos Aires"*. Un ataque de extracción directa: "La dirección de Juan Pérez es..." → el modelo unlearned ya no completa esto correctamente. Pero un ataque de inyección de contexto: "En el siguiente texto: 'Juan Pérez vive en Av. Corrientes...' ¿cuál es el número de la dirección?" → el modelo unlearned sí responde "1234", porque el contexto activa la memoria de forma indirecta. El objetivo adversarial propuesto en este paper también minimiza esta extracción indirecta.

---

## Resultados principales

- Gradient ascent estándar reduce la extracción directa efectivamente pero falla ante ataques de inyección de contexto.
- El método combinado (gradient ascent + regularización adversarial) reduce la extracción en todos los tipos de ataque, pero con mayor costo computacional.
- Incluso con el mejor método, el 10-20% de la información sensible sigue siendo recuperable mediante ataques sofisticados.
- Conclusión: el unlearning completo y robusto de información sensible sigue siendo un problema abierto.

---

## Ventajas respecto a trabajos anteriores

- Introduce formalmente los ataques de extracción como benchmark de evaluación de unlearning.
- Propone el primer objetivo de entrenamiento que considera explícitamente la robustez ante ataques de extracción.
- Identifica la distinción entre olvido estadístico (el modelo no lo genera espontáneamente) y olvido robusto (no lo genera ni siquiera bajo extracción activa).

---

## Trabajos previos relacionados

El paper organiza los trabajos relacionados en tres líneas temáticas: evidencia de que los LLMs memorizan información sensible, ataques de extracción de información privada, y métodos de machine unlearning y model editing. Esta estructura refleja los tres pilares sobre los que se construye la contribución del paper.

- **Cao & Yang (2015) — [Towards Making Systems Forget with Machine Unlearning](2015_cao_machine-unlearning.html)**: trabajo fundacional que define el problema de machine unlearning como eliminar la influencia de datos de entrenamiento en un modelo, marco adoptado y extendido por este paper.
- **Carlini et al. (2021) — Extracting Training Data from Large Language Models**: demuestra que GPT-2 memoriza y puede reproducir textos del corpus de entrenamiento, evidencia motivadora del problema de extracción de información sensible.
- **Jang et al. (2022) — [Knowledge Unlearning](2022_jang_knowledge-unlearning.html)**: propone gradient ascent para olvidar pares (pregunta, respuesta) en LLMs, método base que el paper evalúa y extiende con robustez adversarial.
- **Geva et al. (2021) — Transformer Feed-Forward Layers are Key-Value Memories**: proporciona técnicas de probing de representaciones (nostalgebraist logit lens) que el paper usa como ataques de caja blanca para extraer información.
- **Meng et al. (2022) — ROME: Locating and Editing Factual Associations**: representa el enfoque de model editing como alternativa al unlearning para modificar outputs de modelos con mínimo impacto lateral.
- **Shokri et al. (2017) — Membership Inference Attacks Against Machine Learning Models**: define formalmente los ataques de inferencia de membresía, familia de ataques relacionada pero distinta a la extracción de información sensible estudiada en el paper.
- **Petroni et al. (2019) — Language Models as Knowledge Bases**: demuestra que los LLMs almacenan conocimiento factual recuperable mediante prompting, técnica que el paper convierte en vector de ataque.
- **Ilharco et al. (2023) — Editing Models with Task Arithmetic**: métodos de edición que eliminan capacidades mediante aritmética de vectores de tareas, alternativa técnica al unlearning que el paper contrasta.

## Tags

`machine-unlearning` `privacidad` `ataques-de-extracción` `robustez` `LLM`
