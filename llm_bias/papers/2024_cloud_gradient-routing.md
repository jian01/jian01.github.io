---
layout: paper
title: "Gradient Routing: Masking Gradients to Localize Computation in Neural Networks"
year: 2024
date_published: "2024-10-06"
authors: "Alex Cloud, Jacob Goldman-Wetzler, Evžen Wybitul, Joseph Miller, Alexander Turner"
published: "arXiv, 2024"
tags:
  - "machine-unlearning"
  - "gradient-masking"
  - "localización-conocimiento"
  - "entrenamiento"
  - "interpretabilidad"
pdf: "/llm_bias/pdfs/2024_cloud_gradient-routing.pdf"
method_type: "Enmascarado / edición de pesos"
status:
  - "Pendiente"
image: "imgs/2024_cloud_gradient-routing.png"
image_caption: "Imagen asociada al paper sobre Gradient Routing, técnica que aplica máscaras binarias a los gradientes durante el entrenamiento para localizar el conocimiento en subredes identificables."
opinion: "<WIP>"
---
# Gradient Routing: Masking Gradients to Localize Computation in Neural Networks (2024)

**Autores**: Alex Cloud, Jacob Goldman-Wetzler, Evžen Wybitul, Joseph Miller, Alexander Turner
**Publicado en**: arXiv, 2024
**Tipo de método**: Enmascarado / edición de pesos

---

## Qué hace

Propone **Gradient Routing**, una técnica de entrenamiento que aplica máscaras binarias a los gradientes para que las actualizaciones de ciertos datos sólo fluyan a partes específicas de la red, localizando el conocimiento en subredes identificables que luego pueden modificarse o eliminarse.


---

## Metodología

La idea central es modificar el proceso de backpropagation durante el entrenamiento:

**Entrenamiento estándar:** todos los gradientes de todos los datos fluyen hacia todos los parámetros del modelo.

**Gradient Routing:** para cada ejemplo de entrenamiento, se especifica un "subconjunto de parámetros objetivo" y los gradientes de ese ejemplo sólo actualizan esos parámetros. Los demás parámetros no ven ese ejemplo durante el entrenamiento.

**Aplicación al unlearning:**
1. Durante el entrenamiento inicial, se clasifica cada dato como "normal" o "potencialmente olvide-able".
2. Los datos normales actualizan todos los parámetros.
3. Los datos del forget set sólo actualizan un subconjunto específico de parámetros (ej. las cabezas de atención en las capas 8-12).
4. Cuando se quiere olvidar esos datos, simplemente se resetean o modifican ese subconjunto de parámetros, sabiendo que el forget set está localizado allí.

La implementación técnica usa máscaras binarias multiplicadas con los gradientes antes de la actualización. Funciona en capas específicas del transformer (attention heads, MLP, etc.).

---

## Datasets utilizados

- **Datasets sintéticos**: experimentos controlados con información localizable artificialmente.
- **MNIST**: para demostrar localización de clases específicas.
- Algunos experimentos en NLP con clasificación de texto.

---

## Ejemplo ilustrativo

Imagina una biblioteca donde los libros de medicina están en el ala norte y los de historia en el ala sur. Si construyes la biblioteca con Gradient Routing, cada libro se coloca en un ala específica desde el principio. Cuando alguien pide "elimina todos los libros de medicina", simplemente vaciás el ala norte sin tocar el resto. Sin Gradient Routing, todos los libros estarían mezclados y tendrías que revisar cada uno.

---

## Resultados principales

- En experimentos con datos sintéticos, los datos enrutados a subredes específicas son eliminables con ~95% de forget quality y <2% de degradación en el resto.
- En MNIST, se puede eliminar el conocimiento de dígitos específicos modificando sólo las cabezas de atención designadas.
- El overhead de entrenamiento es mínimo (~5-10% más tiempo por la computación de máscaras).
- Limitación: requiere que el forget set sea identificado *antes* del entrenamiento, lo que no siempre es posible.

---

## Ventajas respecto a trabajos anteriores

- Aborda el problema de unlearning desde el diseño del entrenamiento en lugar de post-hoc.
- La localización garantizada del conocimiento hace el unlearning mucho más preciso.
- Técnicamente elegante: una modificación mínima al proceso de backpropagation.

---

## Trabajos previos relacionados

El paper organiza los antecedentes en cuatro líneas: entrenamiento para localizar capacidades pre-especificadas (arquitecturas modulares), erasure adversarial de representaciones y conceptos, unlearning robusto post-entrenamiento, y los límites del filtrado de datos para eliminar capacidades indeseadas.

- **Cao & Yang (2015) — Towards Making Systems Forget with Machine Unlearning**: [Cao & Yang (2015)](2015_cao_machine-unlearning.html) es la referencia fundacional del machine unlearning; el paper contrasta su enfoque post-hoc con gradient routing, que localiza el conocimiento durante el entrenamiento.
- **Li et al. (2024) — The WMDP Benchmark (RMU)**: [WMDP/RMU](2024_li_wmdp.html) introduce RMU como método convencional de unlearning post-hoc; es la línea base de unlearning más directamente comparable con ERA en los experimentos de LLMs.
- **Lynch et al. (2024) — Eight Methods to Evaluate Robust Unlearning**: [Lynch et al.](2024_lynch_eight-methods.html) documenta que el unlearning estándar es frágil —el conocimiento se recupera con pocas actualizaciones— motivando la propuesta de localización pre-entrenamiento de gradient routing.
- **Sheshadri et al. (2024) — TAR (Tampering Attack Resistance)**: propone meta-aprendizaje MAML para resistir ataques de manipulación en LLMs; gradient routing ofrece otra solución al mismo problema de robustez mediante localización explícita en lugar de entrenamiento adversarial.
- **Gehman et al. (2020) — RealToxicityPrompts**: [RealToxicityPrompts](2020_gehman_realtoxicityprompts.html) ilustra los límites de los clasificadores de toxicidad para filtrar datos dañinos; en el paper, la inadecuación del filtrado de datos motiva gradient routing como alternativa con el efecto de absorción.
- **Gururangan et al. (2021) — DEMix Layers**: introduce capas de expertos por dominio entrenadas con provenance labels; es la alternativa de localización más directamente comparable (DEMix + ablation) en los experimentos controlados de unlearning robusto.
- **Eldan & Russinovich (2023) — Who's Harry Potter**: [Who's Harry Potter](2023_eldan_harry-potter.html) aplica unlearning de copyright en LLMs; el paper de Cloud et al. escala su método a modelos de 0.7B con el dominio de virología, abordando el mismo tipo de capacidades duales.
- **Patil et al. (2023) — Sensitive Information in LLM Unlearning**: [Patil et al.](2023_patil_sensitive-information.html) analiza la recuperación de información sensible tras el unlearning; junto con Lynch et al. motiva la necesidad de robustez que gradient routing aborda desde el diseño del entrenamiento.
- **Geiger et al. (2021) — Causal Abstractions of Neural Networks (IIT)**: [Geiger et al.](2021_geiger_causal-abstractions.html) entrena redes para respetar estructura causal mediante intervenciones en el forward pass; es el antecedente más cercano a gradient routing en términos de imponer estructura en los internals del modelo, aunque con diferencias de especificación y costo.

## Tags

`machine-unlearning` `gradient-masking` `localización-conocimiento` `entrenamiento` `interpretabilidad`
