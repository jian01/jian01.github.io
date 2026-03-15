---
layout: paper
title: "A circuit for Python docstrings in a 4-layer attention-only transformer"
year: 2023
authors: "Stefan Heimersheim, Jett Janiak"
published: "Alignment Forum / distill.pub blog, 2023"
tags:
  - "interpretabilidad-mecanística"
  - "circuitos"
  - "induction-heads"
  - "transformer-pequeño"
  - "tutorial"
status:
  - "Leido"
opinion: "<WIP>"
---
# A circuit for Python docstrings in a 4-layer attention-only transformer (2023)

**Autores**: Stefan Heimersheim, Jett Janiak
**Publicado en**: Alignment Forum / distill.pub blog, 2023

---

## Qué hace

Mapea completamente el circuito responsable de completar docstrings de funciones Python en un transformer pequeño (4 capas, sólo atención, sin MLP). Es un paper pedagógico que sirve como tutorial de cómo hacer circuit analysis paso a paso.

---

## Metodología

**El modelo:** Un transformer attention-only de 4 capas entrenado en código Python. La tarea: dado el nombre de una función y su apertura de docstring, completar con el nombre de la función repetido. Ej: `def calcular_suma(a, b):\n\t"""calcular_` → `suma`.

**El valor pedagógico:** Al ser attention-only (sin capas MLP), el modelo es más simple de analizar. Todo el cómputo se hace en las cabezas de atención, sin la complejidad adicional de las capas FFN.

**La metodología completa de descubrimiento de circuitos:**

1. **Identificar el comportamiento:** El modelo debe copiar el nombre de la función al docstring. Esto requiere encontrar el token del nombre de la función y copiarlo.

2. **Activation patching para identificar cabezas importantes:** Se corrompe el input (cambiando el nombre de la función) y se parcha cada cabeza para ver cuáles son importantes.

3. **Analizar los attention patterns:** Se visualiza a qué tokens atiende cada cabeza importante. Se descubre que hay dos tipos de cabezas:
   - **"Previous Token Heads"** (capas 0-1): atienden al token anterior en la secuencia.
   - **"Induction Heads"** (capas 2-3): implementan el patrón "si viste [A][B] antes, después de ver [A] de nuevo, predice [B]". Esta es la clave para copiar el nombre.

4. **Verificar con intervenciones:** Se confirma que las induction heads son las responsables del comportamiento insertando nombres artificiales y verificando que el modelo los copia correctamente.

---

## Datasets utilizados

- **The Pile (código Python)**: el transformer fue pre-entrenado en código Python de GitHub.
- **Dataset de docstrings**: funciones Python con docstrings para evaluar el comportamiento específico.
- El modelo tiene 4 capas y 8 cabezas por capa (modelo pequeño, ~1M parámetros).

---

## Ejemplo ilustrativo

```python
def calcular_descuento(precio, porcentaje):
    """calcular_
```

El modelo debe completar con "descuento". El circuito:
1. Las previous token heads en la capa 0 atienden al token anterior, creando representaciones contextuales.
2. Las induction heads en la capa 2 identifican el patrón: "def calcular_descuento" apareció antes, y ahora veo "calcular_" de nuevo. Por lo tanto, el siguiente token debe ser "descuento".
3. La induction head copia "descuento" al output.

---

## Resultados principales

- El circuito completo se puede mapear con sólo 4 tipos de cabezas (previous token + induction).
- Las induction heads son las responsables principales del comportamiento de copiado.
- El circuito es generalizable: el mismo mecanismo de induction heads aparece en modelos más grandes (GPT-2, GPT-3) para tareas de copiado similares.

---

## Ventajas respecto a trabajos anteriores

- El modelo attention-only simplifica enormemente el análisis, haciéndolo ideal para enseñar interpretabilidad.
- Demuestra que los mismos mecanismos (induction heads) descubiertos en modelos grandes aparecen también en modelos pequeños entrenados desde cero.
- Referencia pedagógica fundamental para aprender circuit analysis.

---

## Trabajos previos relacionados

Este blog post de LessWrong (sin sección formal de trabajos relacionados) se enmarca explícitamente en la tradición de interpretabilidad mecanística de circuitos en transformers, citando y extendiendo trabajos previos sobre componentes específicos del transformer.

- **Elhage et al. (2021) — A Mathematical Framework for Transformer Circuits**: proporciona el marco residual stream y la noción de composición entre cabezas de atención que estructura todo el análisis del circuito de docstrings.
- **Olah et al. (2020) — Zoom In: An Introduction to Circuits**: trabajo fundacional de Anthropic que define el concepto de circuito como subgrafo interpretable, marco que este paper aplica a un transformer de código.
- **Wang et al. (2022) — [Interpretability in the Wild: IOI Circuit](2022_wang_ioi-circuit.html)**: el circuito IOI en GPT-2 small es la referencia metodológica directa; los "Argument Mover Heads" del paper son equivalentes a los "Name Mover Heads" de Wang et al.
- **Conmy et al. (2023) — [Automated Circuit Discovery (ACDC)](2023_conmy_automated-circuit-discovery.html)**: herramienta de descubrimiento automático de circuitos que se menciona como método complementario para ampliar el análisis.
- **Syed et al. (2024) — [Attribution Patching](2024_syed_attribution-patching.html)**: el paper usa una variante de puntuaciones de composición basadas en patching puntual que anticipa el attribution patching formalizado posteriormente por Syed et al.
- **Hanna et al. (2023) — [How does GPT-2 compute greater-than?](2023_hanna_gpt2-greater-than.html)**: trabajo paralelo que aplica la misma metodología de circuitos a una tarea de razonamiento numérico en GPT-2 small, constituyendo un análogo directo en diferente dominio.
- **Nanda et al. — Neel Nanda's toy language models**: los modelos de transformer pequeño entrenados en código Python usados como base experimental son herramientas abiertas de Neel Nanda, cuya metodología pedagógica orienta todo el trabajo.
- **Bahdanau et al. (2015) — Neural Machine Translation with Attention**: antecedente remoto del mecanismo de atención que las "Induction Heads" explotan para implementar copia de tokens.

## Tags

`interpretabilidad-mecanística` `circuitos` `induction-heads` `transformer-pequeño` `tutorial`
