import math
import os

import fitz
from PIL import Image, ImageDraw


PDF = r"C:\Dev\Learning\tmp\group1_editable_tables_render15\group1_editable_tables.pdf"
OUT = r"C:\Dev\Learning\tmp\group1_editable_tables_render15\png"
CONTACT = r"C:\Dev\Learning\tmp\group1_editable_tables_render15\contact-1.png"

os.makedirs(OUT, exist_ok=True)
doc = fitz.open(PDF)
print(f"pages={len(doc)}")
scale = 1.3
matrix = fitz.Matrix(scale, scale)
thumb_w, thumb_h, gap, cols = 220, 310, 8, 4
rows = math.ceil(len(doc) / cols)
sheet = Image.new("RGB", (cols * thumb_w + (cols + 1) * gap, rows * thumb_h + (rows + 1) * gap), "white")
draw = ImageDraw.Draw(sheet)

for index, page in enumerate(doc):
    pixmap = page.get_pixmap(matrix=matrix, alpha=False)
    path = os.path.join(OUT, f"page-{index + 1:03d}.png")
    pixmap.save(path)
    thumb = Image.open(path).convert("RGB")
    thumb.thumbnail((thumb_w - 10, thumb_h - 25))
    x = gap + (index % cols) * thumb_w
    y = gap + (index // cols) * thumb_h
    sheet.paste(thumb, (x + (thumb_w - thumb.width) // 2, y + 20))
    draw.text((x + 5, y + 3), str(index + 1), fill="black")

sheet.save(CONTACT)
