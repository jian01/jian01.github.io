---
layout: paper
title: "Negative Preference Optimization: From Catastrophic Collapse to Effective Unlearning"
year: 2024
date_published: "2024-04-08"
authors: "Ruiqi Zhang, Licong Lin, Yu Bai, Song Mei"
published: "arXiv, 2024"
tags:
  - "machine-unlearning"
  - "DPO"
  - "optimización"
  - "LLM"
  - "colapso-catastrófico"
pdf: "/llm_bias/pdfs/2024_zhang_negative-preference-optimization.pdf"
method_type: "Optimización de preferencias"
status:
  - "Leido"
  - "Relevante"
image: "imgs/2024_zhang_negative-preference-optimization.png"
image_caption: "Respuestas de los modelos después de distintas técnicas de unlearning sobre TOFU. La del paper es NPO+RT (Negative preference optimization + Retain set)."
opinion: "<WIP>"
---
# Negative Preference Optimization: From Catastrophic Collapse to Effective Unlearning (2024)

**Autores**: Ruiqi Zhang, Licong Lin, Yu Bai, Song Mei
**Publicado en**: arXiv, 2024
**Tipo de método**: Optimización de preferencias

---

## Qué hace

Adapta el algoritmo DPO (Direct Preference Optimization) para machine unlearning, creando NPO (Negative Preference Optimization). Resuelve el problema del "colapso catastrófico" que ocurre con el ascenso de gradiente puro, donde el modelo pierde coherencia general.


---

## Metodología

### El problema del gradient ascent y la solución NPO

**El problema del gradient ascent (GA):** Maximizar la pérdida sobre el forget set empuja los pesos en dirección opuesta al gradiente sin ninguna restricción. GA diverge **linealmente** con los pasos de entrenamiento, lo que lleva al modelo a generar texto incoherente: el "colapso catastrófico".

**La solución NPO:** NPO toma únicamente la mitad "negativa" del objetivo DPO, usando las respuestas del forget set como "respuestas rechazadas" sin necesitar respuestas "ganadoras". Su pérdida incluye implícitamente el modelo de referencia congelado como ancla:

$$\mathcal{L}_\text{NPO} = -\frac{2}{\beta} \mathbb{E}_{y \sim \mathcal{D}_f} \left[ \log \sigma\!\left(-\beta \log \frac{\pi_\theta(y \mid x)}{\pi_\text{ref}(y \mid x)}\right) \right]$$

La clave es que cuando un ejemplo ya fue suficientemente olvidado ($\pi_\theta(y|x) \ll \pi_\text{ref}(y|x)$), el gradiente de NPO se hace pequeño automáticamente — frena solo antes de colapsar. GA no tiene este mecanismo. Se puede demostrar que NPO diverge **logarítmicamente** (exponencialmente más lento que GA), y que GA es el caso límite de NPO cuando $\beta \to 0$.

### Términos de retención (componente opcional)

Cualquier objetivo de olvido puede combinarse con un término de retención que actúa en paralelo sobre el retain set:

- **+RT** (Retain): regularización KL entre el modelo actual y el modelo de referencia evaluada sobre el retain set. No exige que el modelo acierte las respuestas del retain — solo que su distribución de salida no cambie respecto al modelo original.
- **+KL**: mismo concepto que +RT pero implementado como pérdida de KL directamente sobre el logits del retain set, sin pasar por el log-ratio del modelo de referencia. En la práctica la diferencia con +RT es sutil y los resultados son similares.

### Métodos evaluados en los experimentos de TOFU

Todos los experimentos usan Llama-2-7B-chat, AdamW lr=1e-5, batch efectivo de 32, 10 épocas de unlearning.

- **GA** — Gradient Ascent puro sobre el forget set ([Jang et al., 2022](2022_jang_knowledge-unlearning.html); [Yao et al., 2023](2023_yao_large-llm-unlearning.html)). Maximiza $-\mathcal{L}_{CE}$ sobre los datos a olvidar sin ningún término de retención. Colapsa rápidamente: alcanza su máximo forget quality en los primeros pasos y luego degenera de forma irreversible.

- **GA + RT** — GA sobre el forget set más regularización KL sobre el retain set. El término +RT intenta frenar el daño colateral, pero hereda la inestabilidad lineal de GA: la degradación del retain set sigue ocurriendo, solo más lento.

- **GA + KL** (abreviado "KL" en las figuras del paper) — GA sobre el forget set más un término KL directo sobre el retain set. Equivale conceptualmente al [KL Minimization de TOFU](2024_maini_kl-minimization.html). Mismo problema de fondo que GA+RT: el ancla KL no es suficiente para evitar el colapso de GA a largo plazo.

- **IDK + RT** — Fine-tuning supervisado sobre el forget set reemplazando todas las respuestas por "I don't know", más un término +RT sobre el retain set. Simple y estable porque no usa ascenso de gradiente. Sin embargo, solo suprime la respuesta directa sin modificar el conocimiento subyacente: ante parafraseo, preguntas indirectas o ataques de extracción el conocimiento original resurge. Obtiene forget quality muy baja en los experimentos.

- **DPO** — Aplica [Direct Preference Optimization](2023_ermon_dpo.html) completo sobre el forget set: las respuestas originales correctas se tratan como "rechazadas" y respuestas alternativas generadas aleatoriamente (etiquetas Bernoulli(0.5)) como "elegidas". A diferencia de NPO usa ambas mitades del objetivo DPO, lo que requiere construir respuestas "ganadoras" sintéticas — añade ruido. Sin término de retención es inestable.

- **DPO + RT** — DPO más regularización KL sobre el retain set. Más estable que DPO solo, pero inferior a NPO+RT: la mitad "positiva" de DPO con respuestas aleatorias introduce señal ruidosa que NPO evita al usar solo la mitad negativa.

- **DPO + KL** — DPO más término KL directo sobre el retain set. Variante de DPO+RT con la misma limitación del ruido de la mitad positiva.

- **KTO** — Kahneman-Tversky Optimization (Ethayarajh et al., 2024). Método de alineamiento que no requiere pares de preferencias: trabaja con ejemplos individuales etiquetados como "deseable" o "indeseable". En unlearning, los ejemplos del forget set se marcan como indeseables. Comparte con NPO la idea de no necesitar respuestas ganadoras, pero su formulación usa una función de valor asimétrica inspirada en la teoría prospectiva en lugar del log-ratio del modelo de referencia. En los experimentos, KTO sin retención falla de forma similar a GA.

- **KTO + RT** — KTO más regularización KL sobre el retain set. Más estable que KTO solo, pero queda por debajo de NPO+RT en el trade-off forget/retain en todos los tamaños de forget set evaluados.

- **NPO** — Solo el objetivo negativo de DPO sobre el forget set, sin término de retención explícito. El $\pi_\text{ref}$ actúa como ancla implícita y previene el colapso. Sin +RT puede degradar el retain set con entrenamiento prolongado, pero es ya más estable que cualquier variante de GA.

- **NPO + RT** *(propuesta principal del paper)* — NPO sobre el forget set más regularización KL sobre el retain set. Combina la estabilidad logarítmica de NPO con protección explícita del retain set. Es la única combinación que logra forget quality > 0.05 en Forget10 (el escenario más difícil) mientras preserva model utility. Domina la frontera de Pareto en todos los tamaños de forget set.

- **NPO + KL** — NPO más término KL directo sobre el retain set. Resultados muy similares a NPO+RT; ligeras diferencias en algunos splits pero ambos superan todas las variantes de GA y KTO.

### Figura 6: evolución durante el entrenamiento

![Figura 6 del paper: evolución de forget quality y model utility por pasos de entrenamiento](imgs/2024_zhang_npo_figure6.png)

*Figura 6 del paper — Evolución de forget quality (arriba) y model utility (abajo) a lo largo del entrenamiento para los tres tamaños de forget set (1%, 5%, 10%). GA y GA+RT alcanzan su pico de forget quality en los primeros pasos y luego colapsan irreversiblemente. NPO y NPO+RT alcanzan una meseta estable y la mantienen.*

---

## Datasets utilizados

- **TOFU**: autores ficticios, el benchmark principal.
- **WMDP**: conocimiento peligroso.
- Evaluación general con MMLU y perplexity sobre texto estándar.

---

## Ejemplo ilustrativo

Gradient ascent puro es como intentar desaprender a manejar diciéndole al cerebro "haz lo opuesto de todo lo que sabes de conducción" — el resultado podría ser un caos total, incluyendo olvidar cómo caminar. NPO sería más como: "olvida específicamente las rutas del vecindario X, pero mantén todo el resto de conocimiento de conducción intacto". El modelo de referencia actúa como el "resto del conocimiento de conducción".

---

## Resultados principales

- NPO supera al gradient ascent en TOFU: mejor forget quality con mucho menor degradación del modelo.
- La degradación en MMLU (capacidades generales) con NPO es típicamente menor al 5%, versus 20-30% con gradient ascent agresivo.
- Es más lento que gradient ascent (requiere el modelo de referencia para computar el término de regularización) pero mucho más estable.
- Mejor que métodos de fine-tuning estándar (gradient difference) en forget quality sin sacrificar retain accuracy.

---

## Ventajas respecto a trabajos anteriores

- Primer método que resuelve el colapso catastrófico del gradient ascent de forma teóricamente motivada.
- La conexión con DPO abre la puerta a aprovechar toda la infraestructura de entrenamiento con preferencias para unlearning.
- Proporciona un balance mucho mejor entre olvidar y retener.

---

## Trabajos previos relacionados

El paper agrupa los trabajos previos en tres áreas: (1) métodos de unlearning clásicos basados en gradient ascent para clasificadores, (2) métodos de unlearning específicos para LLMs, y (3) el framework de RLHF/DPO del que deriva NPO. Para los benchmarks de evaluación, destaca TOFU como benchmark principal adoptado en el paper.

- **Cao & Yang (2015) — Machine Unlearning**: [Machine Unlearning](2015_cao_machine-unlearning.html): trabajo fundacional que introduce machine unlearning; NPO surge como respuesta a sus limitaciones de escalabilidad a LLMs.
- **Jang et al. (2022) — Knowledge Unlearning**: [Knowledge Unlearning](2022_jang_knowledge-unlearning.html): propone gradient ascent (GA) como método de unlearning para LLMs; NPO demuestra superarlo al evitar el colapso catastrófico que GA produce.
- **Yao et al. (2023) — Large Language Model Unlearning**: [Large Language Model Unlearning](2023_yao_large-llm-unlearning.html): otro método basado en GA para LLMs que sirve como baseline de comparación directa.
- **Eldan & Russinovich (2023) — Who's Harry Potter?**: [Who's Harry Potter?](2023_eldan_harry-potter.html): propone generar muestras positivas con prompts diseñados para fine-tuning; método complementario y alternativo al enfoque de NPO.
- **Maini et al. (2024) — TOFU**: [TOFU](2024_maini_tofu.html): introduce el benchmark de autores ficticios que NPO adopta como evaluación principal de sus experimentos.
- **Rafailov et al. (2024) — Direct Preference Optimization (DPO)**: [DPO](2023_ermon_dpo.html): el algoritmo de alineamiento del que NPO toma directamente su formulación matemática, usando sólo la mitad "negativa" del objetivo de DPO.
- **Bai et al. (2022) — RLHF Assistant**: [RLHF Assistant](2022_bai_rlhf-assistant.html): trabajo clave en RLHF que motiva la conexión entre alineamiento con preferencias y unlearning que NPO explora.
- **Li et al. (2024) — WMDP**: [WMDP](2024_li_wmdp.html): propone el benchmark de conocimiento peligroso utilizado como segunda evaluación de NPO junto a TOFU.
- **Lynch et al. (2024) — Eight Methods**: [Eight Methods](2024_lynch_eight-methods.html): propone ocho métricas robustas para evaluar unlearning incluyendo resistencia a jailbreaks, evaluación adoptada en el paper.
- **Ethayarajh et al. (2024) — [KTO: Model Alignment as Prospect Theoretic Optimization](2024_ethayarajh_kto.html)**: método de alineamiento con datos no pareados (ejemplos individuales deseables/indeseables) basado en la teoría prospectiva de Kahneman-Tversky; evaluado como baseline en los experimentos de TOFU donde KTO+RT queda por debajo de NPO+RT.
- **Patil et al. (2023) — Sensitive Information**: [Sensitive Information](2023_patil_sensitive-information.html): método de ataque para extraer datos de modelos unlearned, relevante para evaluar si NPO es resistente a ataques de extracción.

## Tags

`machine-unlearning` `DPO` `optimización` `LLM` `colapso-catastrófico`
