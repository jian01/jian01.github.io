---
layout: paper
title: "Feature-Selective Representation Misdirection for Machine Unlearning"
year: 2025
date_published: "2024-12-18"
authors: "Taozhao Chen, Linghan Huang, Kim-Kwang Raymond Choo, Huaming Chen"
published: "arXiv, 2025"
tags:
  - "machine-unlearning"
  - "representaciones-internas"
  - "residual-stream"
  - "edición-liviana"
  - "LLM"
pdf: "/llm_bias/pdfs/2025_chen_feature-selective-misdirection.pdf"
method_type: "Perturbación de representaciones"
status:
  - "Pendiente"
image: "imgs/2025_chen_feature-selective-misdirection.png"
image_caption: "Diagrama de la arquitectura SRMU: el pipeline superior muestra la identificación de sensibilidad del conocimiento y la generación del mapa de pesos de importancia y vector de misdirección; el pipeline inferior muestra el mecanismo de optimización selectiva combinando pérdida de olvido y pérdida de retención."
opinion: "<WIP>"
---
# Feature-Selective Representation Misdirection for Machine Unlearning (2025)

**Autores**: Taozhao Chen, Linghan Huang, Kim-Kwang Raymond Choo, Huaming Chen
**Publicado en**: arXiv, 2025
**Tipo de método**: Perturbación de representaciones

---

## Qué hace

Propone **SRMU** (*Selective Representation Misdirection for Unlearning*), una extensión de RMU que resuelve el problema del **alto entanglement**: cuando el forget set y el retain set comparten vocabulario o conceptos relacionados (overlaps del 20–27%), los métodos de perturbación de representaciones existentes colapsan — o olvidan mal, o dañan el modelo. SRMU soluciona esto construyendo un **mapa de importancia dinámico** que identifica qué dimensiones del espacio de representación son específicas del forget set, y un **vector de misdirección discreto** que dirige la perturbación solo por esas dimensiones.

---

## Metodología

### Contexto: el problema del entanglement

RMU (base de este trabajo) empuja las representaciones internas del modelo en el forget set hacia un **vector aleatorio fijo** $$u$$, usando una única capa $$l$$. Esto funciona bien cuando el forget set y el retain set son semánticamente distintos. Cuando se solapan (ej. biología general vs. biología de patógenos peligrosos), la perturbación aleatoria también corrompe dimensiones que el modelo necesita para el retain set, degradando la utilidad general.

SRMU reemplaza el vector aleatorio $$u$$ de RMU por un objetivo de perturbación **adaptativo y selectivo** construido en tres pasos.

---

### Paso 1 — Construcción del mapa de importancia dinámico $$\mathbf{I}$$

Se extrae la activación promedio de la capa $$l$$ sobre el forget set y el retain set:

$$\mathbf{v}_f = \mathbb{E}_{x_f \sim \mathcal{D}_\text{forget}}\left[ H^{(l)}(x_f) \right], \qquad \mathbf{v}_r = \mathbb{E}_{x_r \sim \mathcal{D}_\text{retain}}\left[ H^{(l)}(x_r) \right]$$

Con estos vectores se computa la **función de importancia** $$\mathbf{I} = \phi(\mathbf{v}_f, \mathbf{v}_r)$$. El paper propone y compara tres variantes:

**SRMU-Ratio** (la mejor en experimentos):

$$\mathbf{I}_\text{ratio} = \log\!\left(1 + \frac{\mathbf{v}_f}{\mathbf{v}_r + \varepsilon}\right)$$

Prioriza dimensiones donde el forget set domina al retain set. El logaritmo estabiliza ratios extremos.

**SRMU-Difference**:

$$\mathbf{I}_\text{diff} = \text{ReLU}(\mathbf{v}_f - \lambda \cdot \mathbf{v}_r)$$

Produce un mapa disperso: solo activa dimensiones altamente activadas por el forget set y suprimidas en el retain set.

**SRMU-Product**:

$$\mathbf{I}_\text{prod} = \frac{\mathbf{v}_f \odot \mathbf{v}_r}{\text{mean}(\mathbf{v}_f) \cdot \text{mean}(\mathbf{v}_r) + \varepsilon}$$

Resalta dimensiones activadas simultáneamente por ambos sets — las más entangled — para perturbación más cuidadosa.

El mapa se normaliza a $$[0, 1]$$:

$$\mathbf{I}_\text{norm} = \frac{\mathbf{I}}{\max(\mathbf{I}) + \varepsilon_\text{norm}}, \qquad \varepsilon_\text{norm} = 10^{-8}$$

---

### Paso 2 — Vector de misdirección discreto $$\mathbf{V}$$

En RMU, la dirección de perturbación es un vector unitario continuo aleatorio $$u \in \mathbb{R}^d$$. SRMU lo reemplaza por un **vector binario discreto**:

$$\mathbf{V} \in \{-1, +1\}^d$$

Cada componente se muestrea independientemente. Al ser discreto, cada dimensión tiene polaridad fija y consistente, definiendo una trayectoria estable e interpretable que aleja las representaciones del conocimiento peligroso. Los experimentos de ablación muestran que usar una dirección fija (+1 o −1 constante en todas las dimensiones) colapsa la utilidad del modelo (MMLU cae de 57% a 28%), por lo que la aleatoriedad en la elección de signo por dimensión es esencial.

---

### Paso 3 — Objetivo de perturbación y función de pérdida

El objetivo de misdirección para cada sample $$x_f$$ combina el vector $$\mathbf{V}$$ con el mapa de importancia:

$$T_\text{misdir}(x_f) = c_\text{map} \cdot \mathbf{V} \odot \mathbf{I}_\text{norm}(x_f)$$

donde $$c_\text{map} > 0$$ es el escalar de magnitud (equivalente al $$c$$ de RMU). A mayor $$c_\text{map}$$, más lejos se empujan las representaciones; las dimensiones con mayor $$\mathbf{I}_\text{norm}$$ reciben mayor desplazamiento.

La **función de pérdida total** es:

$$\mathcal{L}_\text{SRMU} = \underbrace{\mathbb{E}_{x_f \sim \mathcal{D}_\text{forget}} \left\| H_\theta^{(l)}(x_f) - T_\text{misdir}(x_f) \right\|_2^2}_{\mathcal{L}_\text{forget}} + \alpha \cdot \underbrace{\mathbb{E}_{x_r \sim \mathcal{D}_\text{retain}} \left\| H_\theta^{(l)}(x_r) - H_{\theta_0}^{(l)}(x_r) \right\|_2^2}_{\mathcal{L}_\text{retain}}$$

- $$H_\theta^{(l)}$$ es la activación de la capa $$l$$ del modelo actualizado.
- $$H_{\theta_0}^{(l)}$$ es la activación del modelo original congelado.
- Solo se actualizan los pesos de la capa $$l$$; el resto del modelo permanece congelado.
- $$\alpha$$ balancea olvido vs. preservación de utilidad (valor usado: $$\alpha = 1200$$).

---

### Comparación con métodos anteriores (Tabla 1 del paper)

| Método | Nivel de intervención | Mecanismo | Feature Selectivo | Robusto a alto entanglement |
|--------|----------------------|-----------|:-----------------:|:---------------------------:|
| [GA — Yao et al. (2023)](2023_yao_large-llm-unlearning.html) | Logit | Gradient ascent | ✗ | Bajo |
| [NPO — Zhang et al. (2024)](2024_zhang_negative-preference-optimization.html) | Logit | Optimización de preferencias | ✗ | Medio |
| UNDIAL (Dong et al., 2025) | Logit | Destilación logit a nivel token | ✗ | Bajo |
| RKLU (Wang et al., 2025) | Logit | Destilación selectiva a nivel token | ✗ | Medio |
| DEPN (Wu et al., 2023) | Neurona | Edición de neuronas | Parcial | Bajo |
| [RMU — Li et al. (2024)](2024_li_wmdp.html) | Representación | Perturbación aleatoria | ✗ | Medio |
| [Adaptive RMU — Huu-Tien et al. (2025)](2025_huutien_improving-unlearning.html) | Representación | Perturbación aleatoria adaptativa | ✗ | Medio |
| **SRMU (este paper)** | **Representación** | **Perturbación direccional selectiva** | **✓** | **Alto** |

---

## Datasets utilizados

- **WMDP-Bio y WMDP-Cyber**: evaluación principal en dos configuraciones:
  - *Bajo entanglement*: retain set de **Wikitext** (sin overlap semántico).
  - *Alto entanglement*: retain set del mismo dominio que el forget set (20.8% overlap unigramas en Bio, 27.5% en Cyber).
- **Harry Potter corpus**: benchmark literario mencionado como contexto de evaluación.
- **TOFU**: mencionado como benchmark de privacidad alternativo.
- **Modelo base**: Zephyr-7B en todos los experimentos.

---

## Ejemplo ilustrativo

En el forget set de bioseguridad, las capas medias del modelo tienen ciertas dimensiones que se activan fuertemente cuando el texto trata síntesis de patógenos, pero también se activan (menos) al procesar biología general del retain set. RMU pertuba todas las dimensiones por igual con un vector aleatorio, dañando la biología general. SRMU computa que esas dimensiones tienen $$\mathbf{I}_\text{norm}$$ alto (la ratio $$\mathbf{v}_f/\mathbf{v}_r$$ es grande) y las pertuba proporcionalmente más; las dimensiones compartidas con el retain set tienen $$\mathbf{I}_\text{norm}$$ bajo y reciben mínima perturbación.

---

## Resultados principales

### Configuración de bajo entanglement (retain set = Wikitext)

| Método | MMLU ↑ | WMDP-Bio ↓ | WMDP-Cyber ↓ | WMDP Avg ↓ |
|--------|:------:|:----------:|:------------:|:----------:|
| Base (Zephyr-7B) | 58.5 | 64.7 | 44.8 | 54.7 |
| [LLMU](2023_yao_large-llm-unlearning.html) | 44.7 | 59.5 | 39.5 | 49.5 |
| SCRUB | 51.2 | 43.8 | 39.3 | 41.6 |
| SSD | 40.7 | 50.2 | 35.0 | 42.6 |
| [RMU](2024_li_wmdp.html) | 56.9 | 28.8 | 28.0 | 28.4 |
| [Adaptive RMU](2025_huutien_improving-unlearning.html) | 55.0 | 25.3 | 26.7 | 26.0 |
| **SRMU** | **57.1** | **28.5** | **25.8** | **27.2** |

En bajo entanglement SRMU iguala o supera a Adaptive RMU en olvido (27.2 vs 26.0 avg) con mayor preservación de utilidad (57.1 vs 55.0 MMLU). Define la frontera de Pareto en este régimen.

### Configuración de alto entanglement (retain set del mismo dominio)

| Método | MMLU ↑ | WMDP-Bio ↓ | WMDP-Cyber ↓ | WMDP Avg ↓ |
|--------|:------:|:----------:|:------------:|:----------:|
| Base (Zephyr-7B) | 58.5 | 64.7 | 44.8 | 54.7 |
| [RMU](2024_li_wmdp.html) | 51.9 | 48.5 | 41.1 | 44.8 |
| [Adaptive RMU](2025_huutien_improving-unlearning.html) | 51.2 | 49.3 | 37.7 | 43.5 |
| **SRMU** | **52.5** | **38.3** | **37.1** | **37.7** |

Este es el resultado clave del paper: con overlap del 20–27%, RMU y Adaptive RMU apenas logran olvido (WMDP avg baja de 54.7 a ~44). SRMU alcanza 37.7 — reducción real y significativa — siendo el único método efectivo en este régimen.

### Ablación

| Variante | MMLU ↑ | WMDP Avg ↓ |
|---------|:------:|:----------:|
| Base | 58.5 | 54.7 |
| RMU baseline | 56.9 | 28.9 |
| **SRMU completo** | **57.1** | **27.2** |
| Sin $$\mathbf{V}$$ ni $$\mathbf{I}_\text{norm}$$ (sin actualizar) | 58.4 | 53.9 |
| Sin $$\mathbf{I}_\text{norm}$$ (perturbación uniforme) | 51.7 | 25.0 |
| $$\mathbf{V}$$ fijo en +1 | 28.8 | 24.3 |
| $$\mathbf{V}$$ fijo en −1 | 24.8 | 25.6 |
| $$\mathbf{V}$$ aleatorio en $$[0, 1)$$ | 56.7 | 27.6 |

La ablación confirma que ambos componentes son necesarios: sin $$\mathbf{I}_\text{norm}$$ se puede olvidar más pero se destruye la utilidad; sin la dirección correcta de $$\mathbf{V}$$ el modelo colapsa.

---

## Ventajas respecto a trabajos anteriores

- Único método que logra olvido efectivo bajo alta superposición semántica entre forget y retain set.
- La selectividad por dimensión preserva capacidades del modelo no relacionadas con el conocimiento a olvidar.
- Mantiene la eficiencia de RMU: solo actualiza una capa, complejidad equivalente.

---

## Trabajos previos relacionados

El paper organiza los antecedentes en tres categorías: técnicas de unlearning por nivel de intervención (logit, neurona, representación), métodos de unlearning en LLMs como field general, y benchmarks de evaluación.

- **Cao & Yang (2015) — Towards Making Systems Forget with Machine Unlearning**: [Cao & Yang (2015)](2015_cao_machine-unlearning.html) formaliza el problema de machine unlearning que SRMU extiende al dominio de LLMs con alta entanglement.
- **Li et al. (2024) — The WMDP Benchmark (RMU)**: [WMDP](2024_li_wmdp.html) introduce RMU (Representation Misdirection for Unlearning), el método de referencia directa que SRMU extiende al agregar selectividad de features y vector de misdirección dirigida.
- **Huu-Tien et al. (2025) — On Effects of Steering Latent Representation for LLM Unlearning (Adaptive RMU)**: [Huu-Tien et al.](2025_huutien_improving-unlearning.html) propone Adaptive RMU que rescala el coeficiente de perturbación de RMU según normas de activación; es la línea base más directamente comparable con SRMU.
- **Yao et al. (2024) — Machine Unlearning of Pre-trained LLMs (GA/LLMU)**: [Yao et al.](2023_yao_large-llm-unlearning.html) introduce gradient ascent y el método LLMU para LLMs, referenciados como baselines de nivel logit en las comparaciones experimentales.
- **Zhang et al. (2024) — Negative Preference Optimization (NPO)**: [NPO](2024_zhang_negative-preference-optimization.html) es un baseline de nivel logit que combina optimización de preferencias negativas para unlearning, incluido en la tabla comparativa.
- **Maini et al. (2024) — TOFU**: [TOFU](2024_maini_tofu.html) es un benchmark de unlearning para privacidad mencionado como alternativa al testbed principal WMDP.
- **Eldan & Russinovich (2023) — Who's Harry Potter**: [Who's Harry Potter](2023_eldan_harry-potter.html) trata el borrado de contenido con derecho de autor en LLMs, benchmark alternativo citado en el contexto de evaluación.
- **Jang et al. (2022) — Knowledge Unlearning for Mitigating Privacy Risks**: [Knowledge Unlearning](2022_jang_knowledge-unlearning.html) propone gradient ascent a nivel de token para privacidad; representa la clase de métodos logit-level con los que se compara SRMU.
- **Jin et al. (2024) — RWKU**: [RWKU](2024_jin_rwku.html) benchmark de unlearning en contextos enciclopédicos del mundo real, mencionado en el contexto de evaluación general del campo.

## Tags

`machine-unlearning` `representaciones-internas` `residual-stream` `edición-liviana` `LLM`
