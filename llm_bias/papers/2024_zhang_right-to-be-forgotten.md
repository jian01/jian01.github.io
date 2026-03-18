---
layout: paper
title: "Right to be Forgotten in the Era of Large Language Models: Implications, Challenges, and Solutions"
year: 2024
date_published: "2023-07-08"
authors: "Dawen Zhang, Pamela Finckenberg-Broman, Thong Hoang, Shidong Pan, Zhenchang Xing, Mark Staples, Xiwei Xu"
published: "AI and Ethics, 2024"
tags:
  - "machine-unlearning"
  - "privacidad"
  - "GDPR"
  - "derecho-al-olvido"
  - "regulación"
pdf: "/llm_bias/pdfs/2024_zhang_right-to-be-forgotten.pdf"
method_type: "Evaluación / análisis"
status:
  - "Pendiente"
image: "imgs/2024_zhang_right-to-be-forgotten.png"
image_caption: "Ejemplo de interfaz conversacional donde un asistente rechaza responder preguntas sobre personas cuya información fue aprobada para eliminación bajo el GDPR."
opinion: "<WIP>"
---

## Qué hace

Analiza las implicaciones legales del **derecho al olvido** (GDPR Art. 17 y regulaciones similares) aplicado a los LLMs. Propone una taxonomía de qué necesita ser olvidado, identifica los desafíos técnicos y legales únicos de los LLMs, y revisa las soluciones existentes desde una perspectiva de cumplimiento regulatorio.


---

## Metodología

Este es principalmente un paper de análisis y posicionamiento (no propone un método nuevo), pero su contribución es sistematizar el problema desde la perspectiva de la intersección entre derecho e IA.

**Taxonomía de lo que debe olvidarse:**
- *Datos personales directos*: nombres, emails, información de salud que el modelo memorizó del corpus de entrenamiento.
- *Contenido generado*: el modelo puede generar texto nuevo que exponga información privada de personas (no sólo reproducir texto memorizado).
- *Inferencias implícitas*: el modelo puede inferir información privada a partir de datos no directamente privados.

**Por qué los LLMs son especialmente difíciles:**
- A diferencia de bases de datos estructuradas, no se puede "borrar un registro" de un LLM: el conocimiento está distribuido en millones de parámetros.
- Los LLMs generan texto nuevo, por lo que incluso si se elimina el dato original, el modelo puede "reconstituir" información privada a partir de patrones aprendidos.
- La verificación del olvido es casi imposible: no hay forma determinista de probar ante un regulador que la información fue eliminada.

**Revisión de soluciones técnicas:** Evalúa machine unlearning, differential privacy, data minimization, y model editing desde la perspectiva de si son legalmente suficientes para cumplir con el GDPR.

---

## Datasets utilizados

No propone datasets nuevos; revisa casos de uso y regulaciones existentes (GDPR europeo, CCPA californiano, PDPA australiano).

---

## Ejemplo ilustrativo

Una persona descubre que cuando le pregunta a un LLM comercial "¿Qué sabes sobre María García, periodista de Buenos Aires?", el modelo genera detalles correctos sobre su domicilio, historial laboral y familia, información que estaba en artículos de internet que fueron parte del corpus de entrenamiento. María ejerce su derecho al olvido ante la empresa. El paper analiza qué debe hacer técnicamente la empresa y si los métodos de unlearning existentes son suficientes para cumplir legalmente.

---

## Resultados principales

- Los métodos de unlearning existentes no ofrecen garantías de olvido verificables que satisfagan los estándares legales del GDPR.
- La verificación post-unlearning (demostrar que la información fue eliminada) es el mayor desafío abierto.
- Differential privacy durante el preentrenamiento es la única solución con garantías formales, pero requiere decidirse antes de entrenar el modelo.
- Propone una agenda de investigación para cerrar la brecha entre los requerimientos legales y las capacidades técnicas actuales.

---

## Ventajas respecto a trabajos anteriores

- Primer análisis sistemático desde la perspectiva legal de lo que significa "cumplir" el derecho al olvido en LLMs.
- Identifica que el problema de verificación del olvido es tan importante como el problema técnico de olvidar.
- Puente entre la comunidad de ML y la comunidad legal/regulatoria.

---

## Trabajos previos relacionados

Este paper de análisis legal-técnico no tiene una sección formal de trabajos relacionados, pero su revisión de soluciones técnicas cubre los trabajos relevantes organizados por tipo de solución: privacidad diferencial, machine unlearning exacto, machine unlearning aproximado, model editing y guardrails.

- **Cao & Yang (2015) — [Towards Making Systems Forget with Machine Unlearning](2015_cao_machine-unlearning.html)**: trabajo fundacional del campo de machine unlearning que motiva toda la discusión técnica del paper sobre cómo implementar el derecho al olvido en modelos de ML.
- **Bourtoule et al. (2021) — Machine Unlearning (SISA)**: propone el unlearning exacto mediante particionamiento del conjunto de entrenamiento y reentrenamiento selectivo; el paper lo presenta como la solución de unlearning exacto de referencia, con sus limitaciones de equidad.
- **Golatkar et al. (2020) — Eternal Sunshine of the Spotless Net**: método de unlearning aproximado que ajusta los pesos del modelo para eliminar la influencia de datos específicos, representante del enfoque de unlearning aproximado revisado.
- **Meng et al. (2022) — ROME: Locating and Editing Factual Associations**: representa el enfoque de model editing como alternativa al unlearning para modificar las salidas del modelo sin reentrenamiento completo.
- **Carlini et al. (2021) — Extracting Training Data from Large Language Models**: demuestra que los LLMs memorizan y pueden reproducir textos del corpus de entrenamiento, evidencia fundamental que hace urgente el problema de RTBF en LLMs.
- **Brown et al. (2020) — Language Models are Few-Shot Learners (GPT-3)**: representa la generación de LLMs de gran escala que el paper identifica como especialmente problemáticos para el RTBF por su capacidad de generar información privada derivada.
- **Yue et al. (2023) — Synthetic Text Generation with Differential Privacy**: propone entrenamiento con privacidad diferencial para datos sintéticos, representando la categoría de privacidad diferencial como solución al RTBF.
- **Patil et al. (2023) — [Can Sensitive Information Be Deleted?](2023_patil_sensitive-information.html)**: estudia directamente si la información sensible puede eliminarse de LLMs con unlearning, trabajo técnico complementario al análisis legal del paper.

## Tags

`machine-unlearning` `privacidad` `GDPR` `derecho-al-olvido` `regulación`
