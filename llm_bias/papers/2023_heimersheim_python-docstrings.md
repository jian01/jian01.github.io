---
layout: paper
title: "A circuit for Python docstrings in a 4-layer attention-only transformer"
year: 2023
date_published: "2023-02-20"
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

## Qué hace

Mapea completamente el circuito responsable de predecir el nombre correcto de argumento en docstrings de funciones Python en un transformer attention-only de 4 capas (sin capas MLP). El circuito identificado consta de 8 cabezas de atención principales (0.2, 0.4, 0.5, 1.4, 2.0, 3.0, 3.6, más 1.2 como cabeza de soporte) que componen a través de tres niveles de composición. Además de ser un resultado de interpretabilidad novedoso, el trabajo sirve como tutorial pedagógico de referencia para aprender circuit analysis paso a paso en un modelo lo suficientemente simple para ser analizado exhaustivamente.

## Contexto y motivación

Tras el trabajo de Wang et al. (2022) sobre el circuito IOI en GPT-2 small, quedó establecida la metodología de circuit analysis para LLMs, pero GPT-2 small con sus 12 capas, 12 cabezas por capa y capas MLP sigue siendo complejo para aprender la metodología desde cero. Había necesidad de un caso de estudio más simple y pedagógico que permitiera: (a) mapear el circuito completo sin ambigüedad, (b) entender las composiciones entre cabezas paso a paso, y (c) verificar los resultados con experimentos concluyentes.

Un transformer attention-only (sin MLPs) en el que la tarea se puede describir algorítmicamente de forma precisa es ideal para este propósito. Al no haber capas FFN, todo el cómputo relevante para la tarea pasa por las cabezas de atención, haciendo el análisis más limpio. El trabajo fue producido como parte del programa SERI ML Alignment Theory Scholars bajo la supervisión de Neel Nanda.

Adicionalmente, el trabajo responde a una pregunta científica de interés: ¿los mecanismos de copia de tokens (como las induction heads) se generalizan a tareas más complejas en código? La respuesta es sí, pero con una jerarquía de composición que va más allá del par Previous Token Head + Induction Head clásico.

## Tarea estudiada

El modelo estudiado es un transformer attention-only de 4 capas con 8 cabezas por capa, entrenado en texto en lenguaje natural y código Python (principalmente de GitHub). La tarea específica es predecir correctamente el nombre de argumento en una línea de docstring:

```python
def f(self, files, obj, state, size, shape, option):
    """document string example
    :param state: performance analysis
    :param size: pattern design
    :param
```

El modelo debe completar con ` shape` (el siguiente argumento en la firma de la función). La tarea requiere que el modelo:

1. Identifique los argumentos listados en la firma de la función (`files`, `obj`, `state`, `size`, `shape`, `option`).
2. Reconozca cuáles de esos argumentos ya han aparecido en el docstring (`:param state:`, `:param size:`).
3. Prediga el siguiente argumento en orden (`shape`), que es el que aparece en la firma después de los ya listados.

La métrica utilizada es la **diferencia de logits** entre el argumento correcto y el argumento alternativo más probable. El dataset usado proviene del notebook de Colab de los autores y usa una función específica `random_random` como distribución corrupta (aleatoriza tanto los nombres de variables en la definición de la función como en el docstring).

La tarea es lingüísticamente significativa: en código Python real, los docstrings suelen listar los parámetros en el mismo orden que la firma de la función. El modelo ha aprendido esta convención de su entrenamiento en código GitHub.

Otro ejemplo más simple de la misma clase de comportamiento:

```python
def calcular_descuento(precio, porcentaje):
    """calcular_
```

Aquí el modelo debe completar con `descuento`, reconociendo que `calcular_` ya apareció en la definición y que `descuento` es el token que le siguió.

## Metodología

### El modelo y sus propiedades

El transformer estudiado tiene 4 capas, 8 cabezas por capa (32 cabezas en total), y es **attention-only** (sin capas MLP). Esto significa que el residual stream sólo es modificado por las cabezas de atención. Para una capa $i$:

$$x_{i+1} = x_i + \sum_{j=1}^{8} h_{i,j}(x_i)$$

La ausencia de MLPs simplifica enormemente el análisis: no hay neuronas FFN que actúen como "memorias" clave-valor (Geva et al. 2021), y todo el cómputo trazable pasa por composiciones de cabezas de atención.

### Activation patching para identificar cabezas importantes

El proceso comienza con activation patching: dado el prompt de docstring original $x_\text{orig}$ y un prompt corrupto $x_\text{new}$ (con nombres de variables aleatorizados), para cada cabeza $h_{i,j}$:

1. Ejecutar forward pass en $x_\text{orig}$.
2. Reemplazar las activaciones de $h_{i,j}$ con las del forward pass en $x_\text{new}$.
3. Medir el cambio en la diferencia de logits $\Delta[\text{logit}(\text{correcto}) - \text{logit}(\text{incorrecto})]$.

Las cabezas con mayor impacto negativo son las que forman parte del circuito. Este proceso identifica un conjunto inicial de cabezas candidatas en capas 1-3.

### Path patching para desambiguar composiciones

Una vez identificadas las cabezas candidatas, se usa path patching para determinar qué cabezas de capas anteriores las alimentan. Para una cabeza $h$ y un conjunto de cabezas objetivo $R$ (las identificadas en el paso anterior):

1. Parchear las activaciones de $h$ con las del input corrupto.
2. Restringir el efecto al camino directo $h \to R$ (sin que la corrupción se propague a través de otras cabezas).
3. Medir el efecto en la diferencia de logits.

Este proceso revela las composiciones de valor, clave y query entre cabezas de diferentes capas, permitiendo construir el grafo del circuito.

### Análisis de patrones de atención

Para cada cabeza importante, se visualiza a qué tokens atiende en los ejemplos de docstring. Este análisis revela los tipos funcionales:

- ¿Atiende al token anterior en la secuencia? → Previous Token Head.
- ¿Atiende al token que siguió a la última aparición del token actual? → Induction Head.
- ¿Atiende al nombre de función en la línea `def`? → Function Name Head.
- ¿Atiende a los argumentos ya usados en el docstring? → Argument tracking head.

### Composición entre cabezas: K-composition, Q-composition, V-composition

Siguiendo la notación de Elhage et al. (2021), las cabezas pueden componerse de tres formas:

- **V-composition**: La cabeza $B$ lee los valores escritos por la cabeza $A$ al residual stream. El output de $A$ pasa por la matriz OV de $B$.
- **K-composition**: La cabeza $B$ usa el output de $A$ para calcular sus claves: dónde atender depende de lo que $A$ ha escrito.
- **Q-composition**: La cabeza $B$ usa el output de $A$ para calcular sus queries: qué busca $B$ depende de lo que $A$ ha escrito.

El circuito de docstrings hace uso principalmente de K-composition entre las cabezas de capa 0 y las de capas superiores.

## El circuito / Los componentes

El circuito final consta de 8 cabezas principales con 37 aristas en el grafo de composición:

### Previous Token Heads — capas 0 y 1: cabezas 0.2, 0.4, 0.5
Estas cabezas atienden al token inmediatamente anterior en la secuencia. Su función es copiar información sobre el token $t-1$ al residual stream del token $t$, creando así una "representación del contexto inmediato" en cada posición. Son análogas a las Previous Token Heads del circuito IOI.

En el contexto de docstrings: al estar en la posición del segundo token de un nombre de argumento (por ejemplo, `_descuento` en `calcular_descuento`), estas cabezas copian el token anterior (`calcular_`), preparando la clave para que las Induction Heads detecten el patrón de repetición.

La cabeza **0.5** es la más importante de este grupo y es recuperada consistentemente por ACDC como parte del circuito mínimo.

### Induction Head — capa 1: cabeza 1.4
Esta es la cabeza más crítica del circuito. Implementa el mecanismo de inducción clásico (Olsson et al. 2022): reconoce el patrón $[A][B]\ldots[A]$ y contribuye a predecir $[B]$ como siguiente token.

En el contexto de docstrings: si la firma contiene `calcular_descuento` y el docstring contiene `calcular_`, la cabeza 1.4 atiende a la posición inmediatamente siguiente a la última aparición de `calcular_` en el contexto (es decir, al token `descuento` en la definición de la función) y escribe en el residual stream de la posición actual la representación de `descuento`. La composición de clave con las Previous Token Heads es lo que permite esta atención: la cabeza 1.4 busca posiciones cuya "representación del token anterior" coincide con el token actual.

Importante: la cabeza 1.4 puede operar en dos posiciones distintas con funciones ligeramente diferentes:
- En la posición del token `:param` dentro del docstring: atiende a otras apariciones previas de `:param` para establecer el patrón de repetición.
- En la posición del argumento a predecir: atiende al argumento correspondiente en la firma para copiarlo.

Esta dualidad de funciones de una misma cabeza según la posición es una limitación que el propio trabajo reconoce: herramientas como ACDC, que no distinguen posiciones de token, no pueden capturar este comportamiento a su nivel de abstracción.

### Argument Mover Heads — capa 2 y 3: cabezas 2.0, 3.0
Estas cabezas, activas en la posición de predicción final, atienden a los argumentos de la firma de la función y "mueven" la información del argumento correcto a la posición de predicción. Son análogas a las Name Mover Heads del circuito IOI: leen el residual stream enriquecido por las Induction Heads y copian el token relevante al output.

La cabeza **2.0** actúa como mover primario: con alta probabilidad de atención al argumento correcto, escribe su representación en la posición de predicción via su matriz OV.

### Output Head — capa 3: cabeza 3.6
Cabeza principal de output. Activa en la posición de predicción, consolida las señales de las capas anteriores y proyecta la predicción final hacia el espacio de logits. Tiene alta importancia en el path patching directo hacia los logits.

### Supporting Heads — cabeza 1.2
Cabeza de soporte no siempre incluida en el circuito mínimo (no recuperada por ACDC con threshold $\tau = 0.095$, pero sí con $\tau = 0.005$). Los autores la consideran una cabeza de apoyo que refuerza el comportamiento pero no es esencial. ACDC la recupera en circuitos más grandes.

### Cabezas no relevantes bajo la distribución docstring — 0.2, 0.4
Aunque los autores las incluyen manualmente en su circuito "de 8 cabezas", el análisis de ACDC (Conmy et al. 2023) muestra que estas cabezas no son relevantes bajo la distribución docstring específica. Se añadieron manualmente por error o por generalidad, pero no contribuyen al comportamiento bajo el dataset de evaluación.

### Por qué cada componente es necesario

El algoritmo que el modelo implementa es: "dado el nombre de función que aparece en `def`, encuéntralo en el texto del docstring y predice el siguiente subtoken que le siguió en la definición". Esto requiere:

1. **Previous Token Heads (0.5, 1.2-via-0.5)**: Sin éstas, las Induction Heads no pueden hacer K-composition para detectar que el token actual ya aparecía antes seguido de un token específico.
2. **Induction Head (1.4)**: Sin ella, no hay mecanismo para "recordar" qué token siguió a la ocurrencia anterior del token actual en la firma de la función.
3. **Argument Movers (2.0, 3.0) y Output Head (3.6)**: Sin ellas, la información sobre el argumento correcto no llega al residual stream en la posición de predicción con suficiente magnitud para dominar los logits.

## Ejemplo ilustrativo

Consideremos:

```python
def f(self, files, obj, state, size, shape, option):
    """document string example
    :param state: performance analysis
    :param size: pattern design
    :param
```

El modelo debe predecir ` shape`.

**Token target**: la posición del último `:param` en el docstring, que debe ser completado con ` shape`.

**Paso 1 — Previous Token Heads (capa 0, cabeza 0.5):**
Para cada posición en la secuencia, la cabeza 0.5 copia el token anterior al residual stream de la posición actual. En particular, en la posición del token `shape` dentro de `def f(...)`, 0.5 copia `size` (el token anterior). Esto significa que en la posición de `shape`, el residual stream contiene información de que el token anterior era `size`.

**Paso 2 — Induction Head (capa 1, cabeza 1.4):**
En la posición de predicción (la última `:param`), la cabeza 1.4 busca en el contexto previo dónde apareció `:param` antes. Cuando encuentra `:param size:`, y dado que ya sabe (del residual stream de la posición de predicción) que el token actual es `:param`, atiende a `:param size:` y detecta que el argumento que siguió a `:param` después de `state` y `size` en la secuencia de firma es `shape`. Escribe la representación de `shape` en el residual stream de la posición de predicción.

Más precisamente, la cabeza 1.4 implementa: "el `:param` que viene a continuación en el docstring debe listar el argumento que aparece en la firma de la función justo después de los ya listados". Esto lo hace reconociendo el patrón de repetición entre la firma y el docstring.

**Paso 3 — Argument Movers (capas 2-3):**
Las cabezas 2.0, 3.0 y 3.6 leen el residual stream enriquecido por 1.4 y copian la representación de `shape` hacia el espacio de logits con suficiente magnitud para que sea la predicción dominante.

**Resultado:** El modelo predice ` shape` con alta diferencia de logits respecto a cualquier otro argumento (como ` option`, que sería el siguiente candidato).

**Ablación confirmatoria:** Si se knockoutea la cabeza 1.4 (sustituyendo por activaciones medias), la diferencia de logits para `shape` colapsa. El modelo deja de poder identificar qué argumento viene a continuación en el orden de la firma, demostrando que 1.4 es la cabeza central del mecanismo.

## Resultados principales

- El circuito de 8 cabezas (37 aristas) reproduce el comportamiento de docstring del modelo con buena fidelidad. En la métrica de diferencia de logits, el circuito manual logra $-0.62$ vs. el modelo completo con $0.48$ (la métrica negativa refleja la convención usada: KL divergence 0.83 vs. 0 del modelo completo).
- El circuito opera en tres niveles de composición: capa 0 → capa 1 (K-composition para induction) → capas 2-3 (V-composition para argument moving).
- **Validación con ACDC** (Conmy et al. 2023): ACDC recupera automáticamente las cabezas 0.5, 1.4, 2.0, 3.0 y 3.6 del circuito manual con alta concordancia. Con threshold $\tau = 0.095$, ACDC produce un circuito de 34 aristas con KL divergence 1.2 respecto al modelo (vs. 1.1 del circuito manual de 37 aristas). El circuito ACDC con el threshold $\tau = 0.067$ (optimizando diferencia de logits en lugar de KL) es incluso más específico: 93% menos aristas que el modelo completo, 79% menos que el circuito manual de cabezas, con mejor rendimiento en todas las métricas.
- Las cabezas 0.2 y 0.4 incluidas en el circuito manual no son relevantes bajo la distribución docstring según los experimentos de ACDC.
- La cabeza 1.4 opera de forma distinta según la posición de token, ilustrando la limitación de analizar circuitos sin distinguir posiciones.
- El mismo mecanismo de induction (Previous Token Head + Induction Head) aparece aquí igual que en el análisis de Olsson et al. (2022) para transformers más pequeños, pero ahora dentro de un circuito más complejo con capas de moving adicionales.

## Ventajas respecto a trabajos anteriores

- **Modelo más simple para pedagogía**: Al ser attention-only de 4 capas, el circuito es completamente analizable sin ambigüedades. No hay que lidiar con capas MLP que complican la interpretación, haciendo el tutorial accesible.
- **Primera demostración en código Python**: Extiende el análisis de circuitos a un dominio de código fuente, mostrando que los mismos mecanismos (induction heads) se aplican en dominios más técnicos que el lenguaje natural.
- **Composición en tres niveles verificada**: Demuestra explícitamente cómo K-composition, V-composition y Q-composition entre cabezas de diferentes capas implementan conjuntamente un comportamiento complejo.
- **Referencia pedagógica estándar**: Se convierte en el tutorial canónico para aprender circuit analysis en la comunidad de interpretabilidad mecanística, citado por trabajos posteriores como punto de entrada al área.
- **Circuito más pequeño que IOI**: Con 8 cabezas frente a las 26 de Wang et al. (2022), el circuito es más manejable para entender cada componente en detalle.
- **Dualidad funcional de cabezas**: La observación de que la cabeza 1.4 realiza dos funciones distintas en diferentes posiciones de token motiva herramientas más granulares (como el análisis por posición que desarrollan trabajos posteriores).

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
