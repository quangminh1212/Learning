from pathlib import Path
import re
from xml.sax.saxutils import escape, quoteattr

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    CondPageBreak,
    LongTable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "danh-sach-repo-tiet-kiem-token-llm.md"
OUTPUT = ROOT / "danh-sach-repo-tiet-kiem-token-llm.pdf"

FONT = Path(r"C:\Windows\Fonts\DejaVuSans.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\DejaVuSans-Bold.ttf")
pdfmetrics.registerFont(TTFont("DejaVu", str(FONT)))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(FONT_BOLD)))
pdfmetrics.registerFontFamily(
    "DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu", boldItalic="DejaVu-Bold"
)

NAVY = colors.HexColor("#17365D")
BLUE = colors.HexColor("#24527A")
PALE_BLUE = colors.HexColor("#EAF2F8")
GRID = colors.HexColor("#C8D2DC")
INK = colors.HexColor("#202A34")
MUTED = colors.HexColor("#596775")

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="TitleVN",
        parent=styles["Title"],
        fontName="DejaVu-Bold",
        fontSize=21,
        leading=27,
        alignment=TA_CENTER,
        textColor=NAVY,
        spaceAfter=9,
    )
)
styles.add(
    ParagraphStyle(
        name="H2VN",
        parent=styles["Heading2"],
        fontName="DejaVu-Bold",
        fontSize=14,
        leading=18,
        textColor=NAVY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="H3VN",
        parent=styles["Heading3"],
        fontName="DejaVu-Bold",
        fontSize=11,
        leading=14,
        textColor=BLUE,
        spaceBefore=9,
        spaceAfter=5,
        keepWithNext=True,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyVN",
        parent=styles["BodyText"],
        fontName="DejaVu",
        fontSize=8.6,
        leading=12,
        textColor=INK,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="TableCellVN",
        parent=styles["BodyText"],
        fontName="DejaVu",
        fontSize=7.4,
        leading=9.5,
        textColor=INK,
        spaceAfter=0,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="TableHeadVN",
        parent=styles["BodyText"],
        fontName="DejaVu-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        spaceAfter=0,
    )
)
styles.add(
    ParagraphStyle(
        name="ListVN",
        parent=styles["BodyText"],
        fontName="DejaVu",
        fontSize=8.5,
        leading=11.5,
        leftIndent=13,
        firstLineIndent=-8,
        textColor=INK,
        spaceAfter=4,
    )
)


def inline_markup(text: str) -> str:
    """Convert the small Markdown inline subset used in this report safely."""
    token_pattern = re.compile(r"(\[[^\]]+\]\([^\)]+\)|\*\*.*?\*\*|`[^`]*`)")
    pieces = []
    cursor = 0
    for match in token_pattern.finditer(text):
        pieces.append(escape(text[cursor : match.start()]))
        token = match.group(0)
        if token.startswith("["):
            link = re.fullmatch(r"\[([^\]]+)\]\(([^\)]+)\)", token)
            label, url = link.groups()
            pieces.append(
                f'<link href={quoteattr(url)} color="#1155CC">{escape(label)}</link>'
            )
        elif token.startswith("**"):
            pieces.append(f"<b>{escape(token[2:-2])}</b>")
        else:
            pieces.append(f'<font name="DejaVu-Bold">{escape(token[1:-1])}</font>')
        cursor = match.end()
    pieces.append(escape(text[cursor:]))
    return "".join(pieces)


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_table_separator(line: str) -> bool:
    cells = table_cells(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c.replace(" ", "")) for c in cells)


def build_table(rows: list[list[str]]) -> LongTable:
    if not rows:
        raise ValueError("Markdown table has no rows")
    col_count = len(rows[0])
    if any(len(row) != col_count for row in rows):
        raise ValueError("Markdown table rows have inconsistent column counts")

    cells = []
    for row_index, row in enumerate(rows):
        cell_style = styles["TableHeadVN"] if row_index == 0 else styles["TableCellVN"]
        cells.append([Paragraph(inline_markup(cell), cell_style) for cell in row])

    page_width, _ = landscape(A4)
    available = page_width - 1.6 * cm
    if col_count == 4:
        proportions = [0.20, 0.22, 0.18, 0.40]
    elif col_count == 3:
        proportions = [0.24, 0.31, 0.45]
    else:
        proportions = [1 / col_count] * col_count
    table = LongTable(
        cells,
        colWidths=[available * value for value in proportions],
        repeatRows=1,
        splitByRow=1,
        hAlign="LEFT",
    )
    commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.35, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for row_index in range(2, len(rows), 2):
        commands.append(("BACKGROUND", (0, row_index), (-1, row_index), PALE_BLUE))
    table.setStyle(TableStyle(commands))
    return table


def draw_page(canvas, doc):
    canvas.saveState()
    width, _ = landscape(A4)
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.5)
    canvas.line(0.8 * cm, 0.72 * cm, width - 0.8 * cm, 0.72 * cm)
    canvas.setFont("DejaVu", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.8 * cm, 0.43 * cm, "Repo và benchmark: liên kết bấm được trong tài liệu")
    canvas.drawRightString(width - 0.8 * cm, 0.43 * cm, f"Trang {doc.page}")
    canvas.restoreState()


def build_story(markdown: str):
    lines = markdown.splitlines()
    story = []
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line.startswith("|"):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_line = lines[index].strip()
                if not is_table_separator(table_line):
                    rows.append(table_cells(table_line))
                index += 1
            story.append(build_table(rows))
            story.append(Spacer(1, 6))
            continue
        if line.startswith("# "):
            story.append(Paragraph(inline_markup(line[2:]), styles["TitleVN"]))
        elif line.startswith("## "):
            story.append(CondPageBreak(52))
            story.append(Paragraph(inline_markup(line[3:]), styles["H2VN"]))
        elif line.startswith("### "):
            story.append(CondPageBreak(42))
            story.append(Paragraph(inline_markup(line[4:]), styles["H3VN"]))
        elif line.startswith("- "):
            story.append(Paragraph("• " + inline_markup(line[2:]), styles["ListVN"]))
        elif line.startswith("> "):
            story.append(Paragraph(inline_markup(line[2:]), styles["BodyVN"]))
        elif line == "---":
            story.append(Spacer(1, 5))
        else:
            story.append(Paragraph(inline_markup(line), styles["BodyVN"]))
        index += 1
    return story


def main():
    if not FONT.is_file() or not FONT_BOLD.is_file():
        raise FileNotFoundError("DejaVuSans fonts were not found in C:\\Windows\\Fonts")
    markdown = SOURCE.read_text(encoding="utf-8")
    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=landscape(A4),
        rightMargin=0.8 * cm,
        leftMargin=0.8 * cm,
        topMargin=0.85 * cm,
        bottomMargin=1.05 * cm,
        title="Danh sách GitHub repo hỗ trợ tiết kiệm token cho LLM",
        author="",
        subject="Repo, phương pháp, mức tiết kiệm token và benchmark tham khảo",
    )
    document.build(build_story(markdown), onFirstPage=draw_page, onLaterPages=draw_page)
    print(f"Đã tạo: {OUTPUT}")


if __name__ == "__main__":
    main()
