"""
add_citation_counts.py
-----------------------
Adds a "Citas" column to every paper row in the topic tables
(unlearning.md, bias.md, alignment.md, interpretability.md).

Reads cited_by_count from data/internal_citations.json.
"""

import json
import re
from pathlib import Path

ROOT       = Path(__file__).parent
DATA_DIR   = ROOT / "data"
TOPICS_DIR = ROOT / "topics"
CITATIONS  = DATA_DIR / "internal_citations.json"

TOPIC_FILES = [
    TOPICS_DIR / "unlearning.md",
    TOPICS_DIR / "bias.md",
    TOPICS_DIR / "alignment.md",
    TOPICS_DIR / "interpretability.md",
]

# Matches [Ver](../papers/STEM.html) or [Ver](STEM.html)
VER_RE = re.compile(r'\[Ver\]\((?:\.\./papers/)?([^)]+)\.html\)')

# Matches a markdown table separator row like | --- | --- | :---: |
SEP_RE = re.compile(r'^\|\s*[-:]+\s*\|')


def add_col(line: str, content: str) -> str:
    """Insert a new column before the trailing | of a table row."""
    line = line.rstrip()
    if line.endswith("|"):
        return line[:-1] + "| " + content + " |"
    return line + " | " + content + " |"


def process_file(path: Path, citations: dict) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    new_lines = []
    in_paper_table = False   # True while inside a table that has [Ver] links

    for i, line in enumerate(lines):
        stripped = line.strip()

        if not stripped.startswith("|"):
            in_paper_table = False
            new_lines.append(line)
            continue

        # --- inside a | row ---

        # Separator row?
        if SEP_RE.match(stripped):
            if in_paper_table:
                line = add_col(line, ":---:")
            new_lines.append(line)
            continue

        # Header row: contains "Resumen" column and is the header we care about
        if "| Resumen |" in line or line.rstrip().endswith("| Resumen |"):
            in_paper_table = True
            line = add_col(line, "Citas")
            new_lines.append(line)
            continue

        # Data row inside a paper table: add count
        if in_paper_table:
            m = VER_RE.search(line)
            if m:
                stem = m.group(1)
                count = citations.get(stem, {}).get("cited_by_count", 0)
                line = add_col(line, str(count))
            # else: table row without [Ver] — leave as is
            new_lines.append(line)
            continue

        # Any other | row (stats tables, etc.) — leave unchanged
        new_lines.append(line)

    new_text = "\n".join(new_lines)
    if text.endswith("\n"):
        new_text += "\n"
    path.write_text(new_text, encoding="utf-8")

    # Count how many paper rows were updated
    n = sum(1 for l in new_lines if VER_RE.search(l))
    print(f"  {path.name}: {n} paper rows updated")


def main():
    citations = json.loads(CITATIONS.read_text(encoding="utf-8"))
    for f in TOPIC_FILES:
        process_file(f, citations)
    print("Done.")


if __name__ == "__main__":
    main()
