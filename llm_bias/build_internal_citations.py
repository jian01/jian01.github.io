"""
build_internal_citations.py
----------------------------
Lee la sección "## Trabajos previos relacionados" de cada paper en papers/
y extrae todos los links a otros papers del repo (patrón: ../papers/STEM.html
o simplemente STEM.html dentro de esa sección).

Genera data/internal_citations.json con:
{
  "paper_id": {
    "title": "...",
    "cites": ["id1", "id2", ...],        # papers que este paper cita
    "cited_by": ["id3", "id4", ...],     # papers que citan a este paper
    "cites_count": 5,
    "cited_by_count": 3
  },
  ...
}

IMPORTANTE: regenerar este archivo cada vez que se modifique la sección
"## Trabajos previos relacionados" de cualquier paper.

Uso:
  python build_internal_citations.py
"""

import json
import re
from pathlib import Path

PAPERS_DIR   = Path(__file__).parent / "papers"
DATA_DIR     = Path(__file__).parent / "data"
PAPERS_JSON  = DATA_DIR / "papers.json"
OUTPUT_JSON  = DATA_DIR / "internal_citations.json"

# Regex: cualquier link markdown cuyo href termine en .html y sea un stem de paper
# Acepta: [text](STEM.html) o [text](../papers/STEM.html) o [text](./STEM.html)
LINK_RE = re.compile(r'\[.*?\]\((?:\.\.\/papers\/|\.\/)?([^/)]+)\.html\)')


def extract_related_work_section(text: str) -> str:
    """Devuelve solo el contenido de '## Trabajos previos relacionados'."""
    # Busca el encabezado y toma todo hasta el próximo ## o fin de archivo
    m = re.search(r'##\s+Trabajos previos relacionados\s*\n(.*?)(?=\n##|\Z)',
                  text, re.DOTALL)
    return m.group(1) if m else ""


def main():
    # Cargar lista de papers para tener título y validar stems
    papers_meta = json.loads(PAPERS_JSON.read_text(encoding="utf-8"))
    valid_ids   = {p["id"] for p in papers_meta}
    id_to_title = {p["id"]: p["title"] for p in papers_meta}

    # Para cada paper, extraer los ids que cita en su sección de related work
    cites: dict[str, list[str]] = {}   # paper_id -> [cited_id, ...]

    for md_file in sorted(PAPERS_DIR.glob("*.md")):
        pid  = md_file.stem
        text = md_file.read_text(encoding="utf-8")
        section = extract_related_work_section(text)

        cited = []
        for stem in LINK_RE.findall(section):
            if stem in valid_ids and stem != pid:
                if stem not in cited:
                    cited.append(stem)

        cites[pid] = cited

    # Construir cited_by (inverso de cites)
    cited_by: dict[str, list[str]] = {pid: [] for pid in valid_ids}
    for pid, cited_list in cites.items():
        for target in cited_list:
            if pid not in cited_by[target]:
                cited_by[target].append(pid)

    # Ensamblar resultado final
    result = {}
    for p in papers_meta:
        pid = p["id"]
        c   = cites.get(pid, [])
        cb  = cited_by.get(pid, [])
        result[pid] = {
            "title":         p["title"],
            "cites":         c,
            "cited_by":      cb,
            "cites_count":   len(c),
            "cited_by_count": len(cb),
        }

    OUTPUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2),
                           encoding="utf-8")

    # Resumen en consola
    total_links = sum(v["cites_count"] for v in result.values())
    print(f"Procesados {len(result)} papers, {total_links} links internos totales.\n")

    print("Top 15 más citados dentro del repo:")
    top = sorted(result.items(), key=lambda x: x[1]["cited_by_count"], reverse=True)[:15]
    for pid, data in top:
        print(f"  {data['cited_by_count']:3d}  {pid}")

    print(f"\nGuardado en {OUTPUT_JSON}")


if __name__ == "__main__":
    main()
