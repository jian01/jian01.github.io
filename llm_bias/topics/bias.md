---
layout: default
title: Sesgo en LLMs
---

# Sesgo en LLMs

Benchmarks, datasets y métodos de mitigación de sesgo en modelos de lenguaje.

[← Literature Review](/llm_bias/)

---

<div class="status-legend"><span class="dot dot-relevante"></span> Relevante&nbsp;&nbsp;<span class="dot dot-leido"></span> Leído&nbsp;&nbsp;<span class="dot dot-pendiente"></span> Pendiente&nbsp;&nbsp;<span class="dot dot-irrelevante"></span> Irrelevante</div>


## Benchmarks y Datasets

| Estado | Año | Título | Tipo de método | Resumen | Citas* |
| --- |-----|--------|----------------|---------| :---: |
| <span class="dot dot-leido" title="Leído"></span> | 2020 | Social Bias Frames: Reasoning about Social and Power Implications of Language | Benchmark / Dataset | [Ver](../papers/2020_sap_social-bias-frames.html) | 4 |
| <span class="dot dot-leido" title="Leído"></span> | 2021 | StereoSet: Measuring stereotypical bias in pretrained language models | Benchmark / Dataset | [Ver](../papers/2021_nadeem_stereoset.html) | 19 |
| <span class="dot dot-leido" title="Leído"></span> | 2020 | RealToxicityPrompts: Evaluating Neural Toxic Degeneration in Language Models | Benchmark / Dataset | [Ver](../papers/2020_gehman_realtoxicityprompts.html) | 7 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2021 | Bot-Adversarial Dialogue for Safe Conversational Agents | Benchmark / Dataset | [Ver](../papers/2021_xu_bot-adversarial.html) | 2 |
| <span class="dot dot-leido" title="Leído"></span> | 2021 | TruthfulQA: Measuring How Models Mimic Human Falsehoods | Benchmark / Dataset | [Ver](../papers/2021_lin_truthfulqa.html) | 6 |
| <span class="dot dot-leido" title="Leído"></span> | 2021 | BBQ: A hand-built bias benchmark for question answering | Benchmark / Dataset | [Ver](../papers/2021_parrish_bbq.html) | 12 |
| <span class="dot dot-leido" title="Leído"></span> | 2022 | ToxiGen: A Large-Scale Machine-Generated Dataset for Adversarial and Implicit Hate Speech Detection | Benchmark / Dataset | [Ver](../papers/2022_hartvigsen_toxigen.html) | 0 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2022 | "I'm sorry to hear that": Finding New Biases in Language Models with a Holistic Descriptor Dataset | Benchmark / Dataset | [Ver](../papers/2022_smith_holistic-descriptor.html) | 3 |
| <span class="dot dot-leido" title="Leído"></span> | 2023 | Nationality Bias in Text Generation | Benchmark / Dataset | [Ver](../papers/2023_venkit_nationality-bias.html) | 1 |
| <span class="dot dot-leido" title="Leído"></span> | 2023 | HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models | Benchmark / Dataset | [Ver](../papers/2023_li_halueval.html) | 0 |
| <span class="dot dot-leido" title="Leído"></span> | 2023 | BeaverTails: Towards Improved Safety Alignment of LLM via a Human-Preference Dataset | Benchmark / Dataset | [Ver](../papers/2023_ji_beavertails.html) | 0 |
| <span class="dot dot-leido" title="Leído"></span><span class="dot dot-irrelevante" title="Irrelevante"></span> | 2025 | Do Bias Benchmarks Generalise? Evidence from Voice-based Evaluation of Gender Bias in SpeechLLMs | Benchmark / Dataset | [Ver](../papers/2025_satish_bias-benchmarks-speech.html) | 0 |
| <span class="dot dot-relevante" title="Relevante"></span><span class="dot dot-leido" title="Leído"></span> | 2025 | BiasFreeBench: a Benchmark for Mitigating Bias in Large Language Model Responses | Benchmark / Dataset | [Ver](../papers/2025_xu_biasfreebench.html) | 0 |

*Solo citas entre papers del repositorio.

---

## Métodos de Mitigación

| Estado | Año | Título | Tipo de método | Resumen | Citas* |
| --- |-----|--------|----------------|---------| :---: |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2021 | FairFil: Contrastive Neural Debiasing Method for Pretrained Text Encoders | Fine-tuning / data augmentation | [Ver](../papers/2021_cheng_fairfil.html) | 0 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2021 | Sustainable Modular Debiasing of Language Models | Adapters / PEFT | [Ver](../papers/2021_lauscher_modular-debiasing.html) | 1 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2021 | An Empirical Survey of the Effectiveness of Debiasing Techniques for Pre-trained Language Models | Evaluación / análisis | [Ver](../papers/2021_meade_debiasing-survey.html) | 18 |
| <span class="dot dot-leido" title="Leído"></span> | 2022 | Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback | Fine-tuning / data augmentation | [Ver](../papers/2022_bai_rlhf-assistant.html) | 8 |
| <span class="dot dot-leido" title="Leído"></span> | 2022 | Debiasing Pre-Trained Language Models via Efficient Fine-Tuning | Fine-tuning / data augmentation | [Ver](../papers/2022_gira_debiasing-efficient-finetuning.html) | 8 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2022 | Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned | Evaluación / análisis | [Ver](../papers/2022_ganguli_red-teaming.html) | 3 |
| <span class="dot dot-relevante" title="Relevante"></span><span class="dot dot-leido" title="Leído"></span> | 2022 | MABEL: Attenuating Gender Bias using Textual Entailment Data | Fine-tuning / data augmentation | [Ver](../papers/2022_he_mabel.html) | 10 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2023 | D-CALM: A Dynamic Clustering-based Active Learning Approach for Mitigating Bias | Fine-tuning / data augmentation | [Ver](../papers/2023_hassan_dcalm.html) | 1 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2023 | An Empirical Analysis of Parameter-Efficient Methods for Debiasing Pre-Trained Language Models | Adapters / PEFT | [Ver](../papers/2023_xie_parameter-efficient-debiasing.html) | 5 |
| <span class="dot dot-leido" title="Leído"></span> | 2023 | Language Models Get a Gender Makeover: Mitigating Gender Bias with Few-Shot Data Interventions | Fine-tuning / data augmentation | [Ver](../papers/2023_thakur_gender-makeover.html) | 1 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2023 | Causal-Debias: Unifying Debiasing in Pretrained Language Models via Causal Invariant Learning | Causal / invariante | [Ver](../papers/2023_zhou_causal-debias.html) | 2 |
| <span class="dot dot-relevante" title="Relevante"></span><span class="dot dot-leido" title="Leído"></span> | 2023 | Mitigating Biases for Instruction-following Language Models via Bias Neurons Elimination | Edición de pesos / neuronas | [Ver](../papers/2023_yang_bias-neurons.html) | 8 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2024 | Self-Debiasing Large Language Models: Zero-Shot Recognition and Reduction of Stereotypes | Tiempo de inferencia | [Ver](../papers/2024_gallegos_self-debiasing.html) | 10 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2024 | ChatGPT Based Data Augmentation for Improved Parameter-Efficient Debiasing of LLMs | Fine-tuning / data augmentation | [Ver](../papers/2024_han_chatgpt-data-augmentation.html) | 0 |
| <span class="dot dot-leido" title="Leído"></span><span class="dot dot-irrelevante" title="Irrelevante"></span> | 2025 | Aligned but Stereotypical? The Hidden Influence of System Prompts on Social Bias | Evaluación / análisis | [Ver](../papers/2025_park_aligned-stereotypical.html) | 0 |
| <span class="dot dot-relevante" title="Relevante"></span><span class="dot dot-leido" title="Leído"></span> | 2025 | BiasEdit: Debiasing Stereotyped Language Models via Model Editing | Edición de pesos / neuronas | [Ver](../papers/2025_xu_biasedit.html) | 6 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2025 | FairSteer: Inference Time Debiasing for LLMs with Dynamic Activation Steering | Tiempo de inferencia | [Ver](../papers/2025_li_fairsteer.html) | 2 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2025 | BiasFilter: An Inference-Time Debiasing Framework for Large Language Models | Tiempo de inferencia | [Ver](../papers/2025_cheng_biasfilter.html) | 1 |
| <span class="dot dot-relevante" title="Relevante"></span><span class="dot dot-leido" title="Leído"></span> | 2025 | Dissecting Bias in LLMs: A Mechanistic Interpretability Perspective | Evaluación / análisis | [Ver](../papers/2025_chandna_dissecting-bias.html) | 1 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2025 | Debiasing the Fine-Grained Classification Task in LLMs with Bias-Aware PEFT | Adapters / PEFT | [Ver](../papers/2025_zhao_debiasing-peft.html) | 2 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2025 | BiasGym: Fantastic LLM Biases and How to Find (and Remove) Them | Evaluación / análisis | [Ver](../papers/2025_islam_biasgym.html) | 0 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2025 | LLM Bias Detection and Mitigation through the Lens of Desired Distributions | Fine-tuning / data augmentation | [Ver](../papers/2025_shrestha_llm-bias-detection.html) | 0 |
| <span class="dot dot-pendiente" title="Pendiente"></span> | 2026 | No Free Lunch in Language Model Bias Mitigation? | Evaluación / análisis | [Ver](../papers/2026_chand_no-free-lunch.html) | 0 |
| <span class="dot dot-relevante" title="Relevante"></span><span class="dot dot-leido" title="Leído"></span> | 2026 | KnowBias: Mitigating Social Bias in LLMs via Know-Bias Neuron Enhancement | Edición de pesos / neuronas | [Ver](../papers/2026_pan_knowbias.html) | 0 |

*Solo citas entre papers del repositorio.

---

## Estadísticas

### Por tipo de método

| Tipo de método | N° de papers |
|----------------|:------------:|
| Benchmark / Dataset | 13 |
| Fine-tuning / data augmentation | 8 |
| Evaluación / análisis | 6 |
| Adapters / PEFT | 3 |
| Edición de pesos / neuronas | 3 |
| Tiempo de inferencia | 3 |
| Causal / invariante | 1 |
| **Total** | **37** |

---

### Frecuencia de datasets en papers de métodos

Número de papers de mitigación (sobre 24) que utilizan cada dataset.

| Dataset | Papers que lo usan |
|---------|:-----------------:|
| StereoSet | 18 |
| WinoBias | 15 |
| BBQ | 11 |
| CrowS-Pairs | 10 |
| GLUE | 8 |
| SEAT | 5 |
| BOLD | 3 |
| MMLU | 2 |
| BiasFreeBench, STS-B, WNC, SentiBias, SNLI/MultiNLI, TruthfulQA, WEAT, HH-RLHF, FairFace, CUB-200, Stanford Cars, Food-101 | 1 cada uno |

---

### Métodos que miden calidad general del modelo

De los 18 papers que proponen un método de mitigación activo (excluidos los 6 de evaluación/análisis pura).

| Mide calidad general | N° de papers | Papers |
|----------------------|:------------:|--------|
| Sí | 11 | FairFil, Gira, MABEL, RLHF-Asst., Lauscher, Xie, Yang, Causal-Debias, BiasEdit, Zhao, KnowBias |
| No | 7 | Thakur, D-CALM, Gallegos, Han, BiasFilter, FairSteer, Shrestha |
