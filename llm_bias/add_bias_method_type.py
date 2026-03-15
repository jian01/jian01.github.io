"""
Add method_type to front matter and body of all bias papers.
"""
from pathlib import Path
import re

PAPERS_DIR = Path("/mnt/d/Escritorio/resumen papers/papers")

METHOD_TYPES = {
    # Benchmarks
    "2020_gehman_realtoxicityprompts":       "Benchmark / Dataset",
    "2020_sap_social-bias-frames":           "Benchmark / Dataset",
    "2021_lin_truthfulqa":                   "Benchmark / Dataset",
    "2021_xu_bot-adversarial":               "Benchmark / Dataset",
    "2021_nadeem_stereoset":                 "Benchmark / Dataset",
    "2021_parrish_bbq":                      "Benchmark / Dataset",
    "2022_hartvigsen_toxigen":               "Benchmark / Dataset",
    "2022_ethayarajh_v-usable-information":  "Benchmark / Dataset",
    "2022_smith_holistic-descriptor":        "Benchmark / Dataset",
    "2023_ji_beavertails":                   "Benchmark / Dataset",
    "2023_li_halueval":                      "Benchmark / Dataset",
    "2023_venkit_nationality-bias":          "Benchmark / Dataset",
    "2025_xu_biasfreebench":                 "Benchmark / Dataset",
    "2025_satish_bias-benchmarks-speech":    "Benchmark / Dataset",
    # Fine-tuning / data augmentation
    "2021_cheng_fairfil":                    "Fine-tuning / data augmentation",
    "2022_gira_debiasing-efficient-finetuning": "Fine-tuning / data augmentation",
    "2022_he_mabel":                         "Fine-tuning / data augmentation",
    "2022_bai_rlhf-assistant":               "Fine-tuning / data augmentation",
    "2023_thakur_gender-makeover":           "Fine-tuning / data augmentation",
    "2023_hassan_dcalm":                     "Fine-tuning / data augmentation",
    "2024_han_chatgpt-data-augmentation":    "Fine-tuning / data augmentation",
    "2025_shrestha_llm-bias-detection":      "Fine-tuning / data augmentation",
    # Adapters / PEFT
    "2021_lauscher_modular-debiasing":       "Adapters / PEFT",
    "2023_xie_parameter-efficient-debiasing": "Adapters / PEFT",
    "2025_zhao_debiasing-peft":              "Adapters / PEFT",
    # Edición de pesos / neuronas
    "2023_yang_bias-neurons":                "Edición de pesos / neuronas",
    "2025_xu_biasedit":                      "Edición de pesos / neuronas",
    "2026_pan_knowbias":                     "Edición de pesos / neuronas",
    # Causal / invariante
    "2023_zhou_causal-debias":               "Causal / invariante",
    # Tiempo de inferencia
    "2024_gallegos_self-debiasing":          "Tiempo de inferencia",
    "2025_cheng_biasfilter":                 "Tiempo de inferencia",
    "2025_li_fairsteer":                     "Tiempo de inferencia",
    # Evaluación / análisis
    "2021_meade_debiasing-survey":           "Evaluación / análisis",
    "2022_ganguli_red-teaming":              "Evaluación / análisis",
    "2025_islam_biasgym":                    "Evaluación / análisis",
    "2025_chandna_dissecting-bias":          "Evaluación / análisis",
    "2025_park_aligned-stereotypical":       "Evaluación / análisis",
    "2026_chand_no-free-lunch":              "Evaluación / análisis",
}


def update_paper(stem, method_type):
    path = PAPERS_DIR / f"{stem}.md"
    if not path.exists():
        print(f"  MISSING: {stem}.md")
        return False
    content = path.read_text(encoding="utf-8")

    # Skip if already has method_type
    if "method_type:" in content:
        content = re.sub(r'method_type:.*', f'method_type: "{method_type}"', content)
    else:
        fm_end = content.find("\n---\n", 3)
        if fm_end == -1:
            return False
        content = content[:fm_end] + f'\nmethod_type: "{method_type}"' + content[fm_end:]

    tipo_line = f"**Tipo de método**: {method_type}"
    if "**Tipo de método**" in content:
        content = re.sub(r'\*\*Tipo de método\*\*:.*', tipo_line, content)
    else:
        content = re.sub(r'(\*\*Publicado en\*\*:.*)', r'\1\n' + tipo_line, content, count=1)

    path.write_text(content, encoding="utf-8")
    print(f"  OK: {stem} → {method_type}")
    return True


for stem, mtype in METHOD_TYPES.items():
    update_paper(stem, mtype)
print(f"\nDone: {len(METHOD_TYPES)} papers.")
