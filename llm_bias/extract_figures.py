"""
Extract the best representative figure from each paper PDF and save to papers/imgs/.
Prefers figures from early pages (architecture/overview diagrams tend to be early).
Skips images that are too small (logos, icons) or too narrow (likely text artifacts).
"""
import fitz  # PyMuPDF
import os
import sys
from pathlib import Path

PDF_DIR = Path("/mnt/d/Escritorio/resumen papers/pdfs")
IMG_DIR = Path("/mnt/d/Escritorio/resumen papers/papers/imgs")
IMG_DIR.mkdir(exist_ok=True)

# Minimum dimensions to consider an image worth keeping
MIN_WIDTH = 200
MIN_HEIGHT = 150
MIN_PIXELS = 60_000  # width * height

def score_image(img_info, page_num, total_pages):
    """Score an image: higher = better candidate for the summary figure."""
    w, h = img_info["width"], img_info["height"]
    pixels = w * h
    aspect = w / h if h > 0 else 0

    if w < MIN_WIDTH or h < MIN_HEIGHT or pixels < MIN_PIXELS:
        return -1  # too small

    # Prefer images that are roughly landscape/square (diagrams, not decorations)
    if aspect < 0.3 or aspect > 5:
        return -1  # too tall or too wide (likely a banner or sidebar)

    score = pixels  # base: bigger is better

    # Prefer early pages (first 40% of paper)
    relative_pos = page_num / max(total_pages, 1)
    if relative_pos < 0.4:
        score *= 1.5
    elif relative_pos < 0.6:
        score *= 1.0
    else:
        score *= 0.7

    return score

def extract_best_image(pdf_path, out_path):
    """Extract the best figure from pdf_path and save as PNG to out_path."""
    try:
        doc = fitz.open(str(pdf_path))
    except Exception as e:
        print(f"  ERROR opening {pdf_path.name}: {e}")
        return False

    total_pages = len(doc)
    best_score = -1
    best_xref = None
    best_ext = None

    for page_num in range(min(total_pages, 20)):  # look at first 20 pages max
        page = doc[page_num]
        for img in page.get_images(full=True):
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
            except Exception:
                continue
            w = base_image.get("width", 0)
            h = base_image.get("height", 0)
            ext = base_image.get("ext", "png")
            info = {"width": w, "height": h}
            score = score_image(info, page_num, total_pages)
            if score > best_score:
                best_score = score
                best_xref = xref
                best_ext = ext

    if best_xref is None:
        print(f"  No suitable image found in {pdf_path.name}")
        doc.close()
        return False

    try:
        base_image = doc.extract_image(best_xref)
        img_bytes = base_image["image"]
        # Save as PNG via PIL for format normalization
        try:
            from PIL import Image
            import io
            img = Image.open(io.BytesIO(img_bytes))
            img.save(str(out_path), "PNG")
        except Exception:
            # Fallback: save raw bytes with original extension
            raw_path = out_path.with_suffix("." + best_ext)
            raw_path.write_bytes(img_bytes)
            if raw_path != out_path:
                raw_path.rename(out_path)
        print(f"  Saved: {out_path.name} ({base_image['width']}x{base_image['height']})")
        doc.close()
        return True
    except Exception as e:
        print(f"  ERROR extracting image from {pdf_path.name}: {e}")
        doc.close()
        return False


def main(only_missing=True):
    papers_dir = Path("/mnt/d/Escritorio/resumen papers/papers")
    pdf_files = sorted(PDF_DIR.glob("*.pdf"))

    success = []
    failed = []

    for pdf_path in pdf_files:
        stem = pdf_path.stem
        out_path = IMG_DIR / f"{stem}.png"
        md_path = papers_dir / f"{stem}.md"

        if not md_path.exists():
            continue  # no corresponding summary

        if only_missing and out_path.exists():
            print(f"  SKIP (exists): {stem}")
            continue

        print(f"Processing: {stem}")
        ok = extract_best_image(pdf_path, out_path)
        if ok:
            success.append(stem)
        else:
            failed.append(stem)

    print(f"\nDone: {len(success)} extracted, {len(failed)} failed.")
    if failed:
        print("Failed:", failed)
    return success, failed


if __name__ == "__main__":
    only_missing = "--all" not in sys.argv
    main(only_missing)
