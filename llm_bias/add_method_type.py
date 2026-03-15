"""
Add method_type to front matter and body of all unlearning paper summaries,
then regenerate topics/unlearning.md with a Tipo de método column.
"""
from pathlib import Path
import re

PAPERS_DIR = Path("/mnt/d/Escritorio/resumen papers/papers")

METHOD_TYPES = {
    # Reentrenamiento exacto
    "2015_cao_machine-unlearning":          "Reentrenamiento exacto",
    "2019_ginart_data-deletion":            "Reentrenamiento exacto",
    "2021_bourtoule_sisa":                  "Reentrenamiento exacto",
    "2021_neel_descent-to-delete":          "Reentrenamiento exacto",
    # Gradient ascent / ajuste de loss
    "2022_jang_knowledge-unlearning":       "Gradient ascent",
    "2023_yao_large-llm-unlearning":        "Gradient ascent",
    "2024_wang_llm-unlearning-loss":        "Gradient ascent",
    "2024_li_wmdp":                         "Gradient ascent",
    "2025_fan_unlearning-relearning":       "Gradient ascent",
    # Optimización de preferencias (DPO / NPO)
    "2023_eldan_harry-potter":              "Optimización de preferencias",
    "2024_zhang_negative-preference-optimization": "Optimización de preferencias",
    "2024_fan_simplicity-npo":              "Optimización de preferencias",
    # Enmascarado / edición de pesos
    "2023_yu_pcgu":                         "Enmascarado / edición de pesos",
    "2024_cloud_gradient-routing":          "Enmascarado / edición de pesos",
    "2025_barez_precise-concept-erasure":   "Enmascarado / edición de pesos",
    "2026_cai_per-parameter-task-arithmetic": "Enmascarado / edición de pesos",
    # Perturbación de representaciones
    "2025_huutien_improving-unlearning":    "Perturbación de representaciones",
    "2025_chen_feature-selective-misdirection": "Perturbación de representaciones",
    # Tiempo de inferencia
    "2023_pawelczyk_incontext-unlearning":  "Tiempo de inferencia",
    "2025_deng_guard":                      "Tiempo de inferencia",
    # Evaluación / análisis
    "2023_patil_sensitive-information":     "Evaluación / análisis",
    "2024_maini_tofu":                      "Evaluación / análisis",
    "2024_yao_muse":                        "Evaluación / análisis",
    "2024_jin_rwku":                        "Evaluación / análisis",
    "2024_liu_rethinking-unlearning":       "Evaluación / análisis",
    "2024_lynch_eight-methods":             "Evaluación / análisis",
    "2024_doshi_does-unlearning":           "Evaluación / análisis",
    "2024_ucki_adversarial-unlearning":     "Evaluación / análisis",
    "2024_zhang_right-to-be-forgotten":     "Evaluación / análisis",
    "2024_zhang_catastrophic-quantization": "Evaluación / análisis",
    "2024_dige_machine-unlearning-bias":    "Evaluación / análisis",
    "2025_dorna_openunlearning":            "Evaluación / análisis",
    "2025_qiu_survey-unlearning":           "Evaluación / análisis",
    "2026_dang_beyond-forgetting":          "Evaluación / análisis",
}


def update_paper(stem: str, method_type: str) -> bool:
    path = PAPERS_DIR / f"{stem}.md"
    if not path.exists():
        print(f"  MISSING: {stem}.md")
        return False
    content = path.read_text(encoding="utf-8")

    # 1. Add method_type to front matter (after 'published:' line if present, else before closing ---)
    if "method_type:" in content:
        # Update existing
        content = re.sub(r'method_type:.*', f'method_type: "{method_type}"', content)
    else:
        # Insert before closing --- of front matter
        # Find the second ---
        fm_end = content.find("\n---\n", 3)
        if fm_end == -1:
            print(f"  NO FRONT MATTER: {stem}.md")
            return False
        insert_pos = fm_end
        content = content[:insert_pos] + f'\nmethod_type: "{method_type}"' + content[insert_pos:]

    # 2. Add/update **Tipo de método** line in body (after **Publicado en** line)
    tipo_line = f"**Tipo de método**: {method_type}"
    if "**Tipo de método**" in content:
        content = re.sub(r'\*\*Tipo de método\*\*:.*', tipo_line, content)
    else:
        # Insert after **Publicado en**: line
        content = re.sub(
            r'(\*\*Publicado en\*\*:.*)',
            r'\1\n' + tipo_line,
            content,
            count=1
        )

    path.write_text(content, encoding="utf-8")
    print(f"  OK: {stem} → {method_type}")
    return True


def main():
    updated = 0
    for stem, mtype in METHOD_TYPES.items():
        if update_paper(stem, mtype):
            updated += 1
    print(f"\nDone: {updated}/{len(METHOD_TYPES)} papers updated.")


if __name__ == "__main__":
    main()
