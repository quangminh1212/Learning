"""Build Word report for KTTH Buoi 5 / De 1.1 then convert to .doc."""
from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor, Emu
from PIL import Image

ROOT = Path(
    r"C:\Dev\Learning\VIII.HUST\Quản trị dự án\BachMinhQuang_202490077\KTTH_Buoi5"
)
SHOT = ROOT / "screenshots"
STEM = "202490077-BachMinhQuang-K6901-Buoi5-De1.1"
DOCX = ROOT / f"{STEM}.docx"
DOC = ROOT / f"{STEM}.doc"
NAVY = RGBColor(0x1F, 0x4E, 0x79)
RED = RGBColor(0xC0, 0x10, 0x28)
GRAY = RGBColor(0x55, 0x55, 0x55)
HEADER_FILL = "1F4E79"
ROW_ALT = "F5F8FB"
CRIT_FILL = "FDECEC"


def crop_whitespace(src: Path, dest: Path, header_keep: int = 72) -> tuple[int, int]:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    px = im.load()
    last = header_keep
    for y in range(h - 1, header_keep, -1):
        if any(px[x, y][0] < 248 or px[x, y][1] < 248 or px[x, y][2] < 248 for x in range(0, w, 3)):
            last = y
            break
    bottom = min(h, last + 24)
    cropped = im.crop((0, 0, w, bottom))
    cropped.save(dest, "PNG")
    return cropped.size


def set_run_font(run, name="Times New Roman", size=12, bold=False, color=None, italic=False):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color


def shade_cell(cell, fill: str) -> None:
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def set_cell_border(cell) -> None:
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "B0B8C1")
        tcBorders.append(el)
    tcPr.append(tcBorders)


def cell_text(cell, text, size=10, bold=False, color=None, align="left", fill=None):
    cell.text = ""
    p = cell.paragraphs[0]
    if align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif align == "right":
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, color=color)
    set_cell_border(cell)
    if fill:
        shade_cell(cell, fill)
    for m in ("top", "bottom", "left", "right"):
        cell.margin_top = Cm(0.05) if m in ("top", "bottom") else Cm(0.08)


def add_heading(doc, text, size=14):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    set_run_font(run, size=size, bold=True, color=NAVY)
    return p


def add_body(doc, text, size=12, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    set_run_font(run, size=size)
    return p


def add_table(doc, headers, rows, col_widths, header_fill=HEADER_FILL, crit_rows=None):
    table = doc.add_table(rows=1, cols=len(headers))
    table.autofit = False
    table.allow_autofit = False
    total = sum(col_widths)
    table.width = Cm(total)
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].width = Cm(col_widths[i])
        cell_text(hdr[i], h, size=10, bold=True, color=RGBColor(255, 255, 255), align="center", fill=header_fill)
    crit_rows = crit_rows or set()
    for r_i, row in enumerate(rows):
        cells = table.add_row().cells
        fill = CRIT_FILL if r_i in crit_rows else (ROW_ALT if r_i % 2 else "FFFFFF")
        for i, val in enumerate(row):
            cells[i].width = Cm(col_widths[i])
            align = "center" if i != 0 else "left"
            cell_text(cells[i], str(val), size=10, align=align, fill=fill)
    return table


def add_picture(doc, path: Path, caption: str) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    section = doc.sections[-1]
    usable_w = section.page_width - section.left_margin - section.right_margin
    usable_h = section.page_height - section.top_margin - section.bottom_margin - Cm(2.4)
    with Image.open(path) as im:
        w_px, h_px = im.size
    aspect = h_px / w_px
    width = usable_w
    height = int(width * aspect)
    if height > usable_h:
        height = usable_h
        width = int(height / aspect)
    run = p.add_run()
    run.add_picture(str(path), width=width)
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(8)
    r = cap.add_run(caption)
    set_run_font(r, size=10, italic=True, color=GRAY)


def set_cell_widths(table, widths_cm):
    for row in table.rows:
        for i, w in enumerate(widths_cm):
            row.cells[i].width = Cm(w)


def main() -> None:
    cropped = SHOT / "cropped"
    cropped.mkdir(exist_ok=True)
    shots = {}
    for name in ("gantt", "schedule", "network", "resources", "assign", "cost", "resource_cost"):
        src = SHOT / f"{name}.png"
        dest = cropped / f"{name}.png"
        size = crop_whitespace(src, dest)
        shots[name] = dest
        print("crop", name, size)

    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(1.8)
    section.right_margin = Cm(1.8)
    section.top_margin = Cm(1.6)
    section.bottom_margin = Cm(1.6)

    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = header.add_run("202490077 — Bạch Minh Quang")
    set_run_font(r, size=10, bold=True, color=NAVY)
    r2 = header.add_run("\tKTTH Buổi 5 — Đề 1.1")
    set_run_font(r2, size=10, bold=True, color=NAVY)
    header.paragraph_format.tab_stops.add_tab_stop(Cm(17.0), alignment=2)

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr = footer.add_run("Quản trị dự án — Microsoft Project — lịch 7 ngày/tuần")
    set_run_font(fr, size=9, color=GRAY)

    # Cover
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Cm(1.4)
    run = p.add_run("ĐẠI HỌC BÁCH KHOA HÀ NỘI")
    set_run_font(run, size=16, bold=True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Trường Công nghệ Thông tin và Truyền thông")
    set_run_font(run, size=13, bold=True)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Cm(1.2)
    run = p.add_run("BÁO CÁO KIỂM TRA THỰC HÀNH")
    set_run_font(run, size=20, bold=True, color=NAVY)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("QUẢN TRỊ DỰ ÁN — MICROSOFT PROJECT")
    set_run_font(run, size=14, bold=True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    run = p.add_run("Buổi 5 — Đề 1.1  |  Lịch làm việc 7 ngày/tuần")
    set_run_font(run, size=13, color=NAVY)

    info = [
        ("Họ và tên", "Bạch Minh Quang"),
        ("MSSV", "202490077"),
        ("Lớp", "K6901"),
        ("Nhóm", "1"),
        ("Buổi / Đề", "Buổi 5 / Đề 1.1"),
        ("File MPP", f"{STEM}.mpp"),
        ("File báo cáo", f"{STEM}.doc"),
        ("Ngày bắt đầu", "15/09/2026 (08:00)"),
        ("Ngày kết thúc", "16/12/2026 (17:00)"),
        ("Thời gian dự án", "93 ngày (tuần 7 ngày)"),
        ("Đường găng", "A → B → D → G"),
        ("Tổng chi phí", "932.370.000 ₫"),
    ]
    table = doc.add_table(rows=len(info), cols=2)
    table.width = Cm(12)
    for i, (k, v) in enumerate(info):
        fill = ROW_ALT if i % 2 else "FFFFFF"
        cell_text(table.rows[i].cells[0], k, size=11, bold=True, fill=fill)
        cell_text(table.rows[i].cells[1], v, size=11, fill=fill)
        table.rows[i].cells[0].width = Cm(4.5)
        table.rows[i].cells[1].width = Cm(7.5)
    # center the info table by adding it after a spacer paragraph
    for p in table.rows[0].cells[0].paragraphs:
        pass

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Cm(1.2)
    run = p.add_run("Hà Nội, tháng 09 năm 2026")
    set_run_font(run, size=12)

    # 1. De bai
    add_heading(doc, "1. Yêu cầu đề bài")
    add_body(
        doc,
        "Dùng Microsoft Project, lịch một tuần làm việc 7 ngày, lập biểu đồ Gantt, "
        "xác định công việc găng và đường găng; nhập nguồn lực và gán nguồn lực theo bảng đề bài. "
        "Tên công việc theo mẫu A_MSSV_hovaten.",
    )

    add_heading(doc, "2. Dữ liệu công việc")
    add_body(doc, "Tên công việc trong file: {ký hiệu}_202490077_BachMinhQuang. Ngày bắt đầu dự án: 15/09/2026.")
    add_table(
        doc,
        ["CV", "Số ngày", "Trình tự", "Nguồn lực Work", "Material / Cost"],
        [
            ["A", "25", "Từ đầu", "CN 0,3; TV 0,4; KTV 0,3", "Giấy A3 ×5; Máy in màu ×2"],
            ["B", "20", "Sau A", "CN 0,2; TV 0,4; KTV 0,4", "Công tác phí; Đăng bài ×3"],
            ["C", "18", "Từ đầu", "CN 0,3; TV 0,4; KTV 0,3", "Hội thảo"],
            ["D", "23", "Sau B, C", "CN 0,3; TV 0,4; KTV 0,3", "Đăng bài ×4; Hội thảo"],
            ["E", "19", "Từ đầu", "CN 0,3; TV 0,4; KTV 0,3", "Công tác phí"],
            ["G", "25", "Sau E, D", "CN 0,3; TV 0,4; KTV 0,3", "Hội thảo; Nghiệm thu; Giấy A3 ×1"],
        ],
        [1.6, 2.0, 2.4, 5.2, 6.2],
        crit_rows={0, 1, 3, 5},
    )
    add_body(doc, "Hàng tô hồng là công việc găng (Total Slack = 0). CN = Chủ nhiệm, TV = Thành viên, KTV = Kỹ thuật viên. Hệ số 0,3 / 0,4 là Units trên MS Project (30% / 40%).", size=11)

    add_heading(doc, "3. Lịch 7 ngày/tuần và mạng công việc")
    add_body(
        doc,
        "Tạo lịch cơ sở “7 Days” từ Standard, bật Thứ Bảy và Chủ nhật thành ngày làm việc "
        "(ca 08:00–17:00, 8 giờ/ngày). HoursPerDay = 8, HoursPerWeek = 56. "
        "Mọi công việc kiểu Fixed Duration, Effort driven tắt, để gán Units không làm đổi số ngày.",
    )
    add_body(
        doc,
        "Ba đường đi từ đầu đến kết thúc:",
    )
    add_table(
        doc,
        ["Đường", "Chuỗi công việc", "Độ dài (ngày)"],
        [
            ["1 (găng)", "A → B → D → G", "25 + 20 + 23 + 25 = 93"],
            ["2", "C → D → G", "18 + 23 + 25 = 66"],
            ["3", "E → G", "19 + 25 = 44"],
        ],
        [3.2, 7.5, 6.7],
        crit_rows={0},
    )
    add_body(
        doc,
        "Thời gian dự án T = max = 93 ngày. Công việc găng: A, B, D, G. "
        "Dự trữ C = 93 − 66 = 27 ngày; dự trữ E = 93 − 44 = 49 ngày. "
        "MS Project cho cùng kết quả (Total Slack A/B/D/G = 0; C = 27d; E = 49d). "
        "Start 15/09/2026, Finish 16/12/2026.",
    )

    add_heading(doc, "4. Biểu đồ Gantt")
    add_body(doc, "Cột thời gian theo tuần. Nhãn trên thanh là nguồn lực đã gán. Quan hệ FS: B←A, D←B+C, G←E+D.")
    add_picture(doc, shots["gantt"], "Hình 1. Biểu đồ Gantt — lịch 7 ngày/tuần")

    add_heading(doc, "5. Đường găng (Critical Path)")
    add_body(doc, "Bảng Schedule: Total Slack = 0 là găng. Network Diagram: hộp đỏ = găng, hộp xanh = không găng.")
    add_picture(doc, shots["schedule"], "Hình 2. Bảng Schedule — Total Slack")
    add_picture(doc, shots["network"], "Hình 3. Network Diagram — đường găng A-B-D-G (hộp đỏ)")

    add_heading(doc, "6. Nguồn lực")
    add_table(
        doc,
        ["Nguồn lực", "Loại", "Đơn vị", "Đơn giá"],
        [
            ["Chủ nhiệm", "Work", "Giờ", "180.000 ₫/h"],
            ["Thành viên", "Work", "Giờ", "155.000 ₫/h"],
            ["Kỹ thuật viên", "Work", "Giờ", "100.000 ₫/h"],
            ["Giấy A3", "Material", "Ram", "135.000 ₫"],
            ["Máy in màu", "Material", "Cái", "5.500.000 ₫"],
            ["Công tác phí", "Cost", "Lần", "45.000.000 ₫"],
            ["Đăng bài", "Material", "Bài", "35.000.000 ₫"],
            ["Hội thảo", "Cost", "Lần", "95.000.000 ₫"],
            ["Nghiệm thu", "Cost", "Lần", "150.000.000 ₫"],
        ],
        [4.4, 2.6, 2.6, 7.8],
    )
    add_body(doc, "Work: Std. Rate theo giờ. Material: Standard Rate + Material Label. Cost: gán Cost trên Assignment bằng đúng đơn giá mỗi lần xuất hiện trên công việc.", size=11)
    add_picture(doc, shots["resources"], "Hình 4. Resource Sheet — loại và đơn giá")

    add_heading(doc, "7. Gán nguồn lực")
    add_body(
        doc,
        "Work: Units = 0,3 / 0,4 / 0,2 (hiển thị 30% / 40% / 20%). "
        "Material: Units = số lượng (5 Ram, 2 Cái, 3 Bài, …). "
        "Cost: mỗi lần xuất hiện gán đủ đơn giá (Công tác phí 45.000.000 trên B và trên E; Hội thảo 95.000.000 trên C, D, G).",
    )
    add_picture(doc, shots["assign"], "Hình 5. Gán nguồn lực và cột Critical / Total Slack")

    add_heading(doc, "8. Chi phí")
    add_body(doc, "Công thức Work: Chi phí = Số ngày × 8 giờ/ngày × Units × Đơn giá/giờ. Material = số lượng × đơn giá. Cost = đơn giá mỗi lần gán.")
    add_table(
        doc,
        ["CV", "Nhân công", "Vật tư / chi phí", "Tổng (₫)"],
        [
            ["A", "10.800.000 + 12.400.000 + 6.000.000", "Giấy 675.000; Máy in 11.000.000", "40.875.000"],
            ["B", "5.760.000 + 9.920.000 + 6.400.000", "Công tác 45.000.000; 3 bài 105.000.000", "172.080.000"],
            ["C", "7.776.000 + 8.928.000 + 4.320.000", "Hội thảo 95.000.000", "116.024.000"],
            ["D", "9.936.000 + 11.408.000 + 5.520.000", "4 bài 140.000.000; Hội thảo 95.000.000", "261.864.000"],
            ["E", "8.208.000 + 9.424.000 + 4.560.000", "Công tác 45.000.000", "67.192.000"],
            ["G", "10.800.000 + 12.400.000 + 6.000.000", "Hội thảo 95tr; NT 150tr; Giấy 135.000", "274.335.000"],
            ["Cộng", "", "", "932.370.000"],
        ],
        [1.6, 6.4, 6.6, 2.8],
        crit_rows={0, 1, 3, 5},
    )
    add_picture(doc, shots["cost"], "Hình 6. Task Sheet — Cost (trùng tay tính)")
    add_picture(doc, shots["resource_cost"], "Hình 7. Tổng chi phí theo nguồn lực")

    add_heading(doc, "9. Kết luận")
    add_body(
        doc,
        "File MS Project dùng lịch 7 Days, 6 công việc đúng quan hệ đề bài, 9 nguồn lực đúng loại/đơn giá và đã gán. "
        "Đường găng A-B-D-G, thời gian 93 ngày (15/09/2026–16/12/2026), tổng chi phí 932.370.000 ₫. "
        "C có 27 ngày dự trữ, E có 49 ngày dự trữ.",
    )
    add_table(
        doc,
        ["Hạng mục", "Kết quả"],
        [
            ["Lịch", "7 Days (cả thứ Bảy, Chủ nhật)"],
            ["Công việc găng", "A, B, D, G"],
            ["Đường găng", "A → B → D → G"],
            ["Thời gian", "93 ngày"],
            ["Tổng chi phí", "932.370.000 ₫"],
            ["File MPP", f"{STEM}.mpp"],
        ],
        [5.0, 12.4],
    )

    doc.save(str(DOCX))
    print("docx", DOCX, DOCX.stat().st_size)

    # May nay khong co Word.Application; xuat RTF (Word mo duoc khi doi ten .doc).
    import pypandoc

    if DOC.exists():
        DOC.unlink()
    pypandoc.convert_file(str(DOCX), "rtf", outputfile=str(DOC))
    print("doc", DOC, DOC.stat().st_size)


if __name__ == "__main__":
    main()
