"""Render selected pages of main.pdf to PNG images in output/."""
import os
import sys

import fitz

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
PDF_PATH = os.path.join(BASE_DIR, "main.pdf")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def render_pages(pages, dpi=200):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    doc = fitz.open(PDF_PATH)
    for p in pages:
        if p < 0 or p >= len(doc):
            print(f"Page {p + 1} out of range")
            continue
        page = doc.load_page(p)
        pix = page.get_pixmap(dpi=dpi)
        out_path = os.path.join(OUTPUT_DIR, f"page_{p + 1}.png")
        pix.save(out_path)
        print(f"Rendered {out_path}")
    doc.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python render_pages.py 1,2,3 [dpi]")
        sys.exit(1)
    pages = [int(x) - 1 for x in sys.argv[1].split(",")]
    dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    render_pages(pages, dpi=dpi)
