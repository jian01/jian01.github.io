"""
Add YAML front matter to all paper markdown files in papers/.
Extracts: title, year, authors, published_in, tags, and sets pdf path.
Skips files that already have front matter.
"""
import re
import os
from pathlib import Path

PAPERS_DIR = Path("/mnt/d/Escritorio/resumen papers/papers")
PDFS_DIR = Path("/mnt/d/Escritorio/resumen papers/pdfs")


def extract_frontmatter_data(content: str, stem: str) -> dict:
    lines = content.splitlines()

    # Title: first line starting with "# "
    title = ""
    year = ""
    for line in lines:
        m = re.match(r'^#\s+(.+?)(?:\s+\((\d{4})\))?\s*$', line)
        if m:
            title = m.group(1).strip()
            year = m.group(2) or stem[:4]
            break

    # Authors
    authors = ""
    for line in lines:
        m = re.match(r'^\*\*Autores\*\*:\s*(.+)', line)
        if m:
            authors = m.group(1).strip()
            break

    # Published in
    published = ""
    for line in lines:
        m = re.match(r'^\*\*Publicado en\*\*:\s*(.+)', line)
        if m:
            published = m.group(1).strip()
            break

    # Tags: last occurrence of backtick-quoted tags after "## Tags"
    tags = []
    in_tags = False
    for line in lines:
        if line.strip() == "## Tags":
            in_tags = True
            continue
        if in_tags:
            found = re.findall(r'`([^`]+)`', line)
            if found:
                tags = found
            if line.startswith("##") and "Tags" not in line:
                break

    # PDF path
    pdf_path = ""
    pdf_file = PDFS_DIR / f"{stem}.pdf"
    if pdf_file.exists():
        pdf_path = f"/pdfs/{stem}.pdf"

    return {
        "title": title,
        "year": year,
        "authors": authors,
        "published": published,
        "tags": tags,
        "pdf": pdf_path,
    }


def make_frontmatter(data: dict) -> str:
    lines = ["---"]
    lines.append(f"layout: paper")

    # Escape quotes in title
    title = data["title"].replace('"', '\\"')
    lines.append(f'title: "{title}"')

    if data["year"]:
        lines.append(f'year: {data["year"]}')

    if data["authors"]:
        authors = data["authors"].replace('"', '\\"')
        lines.append(f'authors: "{authors}"')

    if data["published"]:
        published = data["published"].replace('"', '\\"')
        lines.append(f'published: "{published}"')

    if data["tags"]:
        lines.append("tags:")
        for tag in data["tags"]:
            lines.append(f'  - "{tag}"')

    if data["pdf"]:
        lines.append(f'pdf: "{data["pdf"]}"')

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def process_file(md_path: Path) -> bool:
    content = md_path.read_text(encoding="utf-8")

    # Skip if already has front matter
    if content.startswith("---"):
        print(f"  SKIP (has front matter): {md_path.name}")
        return False

    data = extract_frontmatter_data(content, md_path.stem)
    fm = make_frontmatter(data)
    new_content = fm + content
    md_path.write_text(new_content, encoding="utf-8")
    print(f"  OK: {md_path.name} | {data['year']} | tags={data['tags'][:2]}")
    return True


def main():
    md_files = sorted(PAPERS_DIR.glob("*.md"))
    updated = 0
    skipped = 0
    for md_path in md_files:
        if process_file(md_path):
            updated += 1
        else:
            skipped += 1
    print(f"\nDone: {updated} updated, {skipped} skipped.")


if __name__ == "__main__":
    main()
