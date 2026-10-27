from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(r"C:\Dev\Learning\IX.Interview")
OUT = ROOT / "Cam_nang_phong_van_Chargecore_Product_Solution_Engineer_02-10-2026.pdf"
FONT_DIR = Path(r"C:\Windows\Fonts")

pdfmetrics.registerFont(TTFont("Arial", str(FONT_DIR / "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_DIR / "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", str(FONT_DIR / "ariali.ttf")))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic", boldItalic="Arial-Bold")

NAVY = colors.HexColor("#132A4A")
BLUE = colors.HexColor("#1E5B91")
TEAL = colors.HexColor("#079A91")
PALE = colors.HexColor("#EAF4F4")
PALE_BLUE = colors.HexColor("#EEF3F8")
INK = colors.HexColor("#263442")
MUTED = colors.HexColor("#647382")
GOLD = colors.HexColor("#E6A13A")
LINE = colors.HexColor("#D6E0E8")
WHITE = colors.white

PAGE_W, PAGE_H = A4
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle", fontName="Arial-Bold", fontSize=25, leading=30,
    textColor=NAVY, alignment=TA_LEFT, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="CoverSub", fontName="Arial", fontSize=12, leading=17,
    textColor=BLUE, alignment=TA_LEFT, spaceAfter=10,
))
styles.add(ParagraphStyle(
    name="H1x", fontName="Arial-Bold", fontSize=17, leading=21,
    textColor=NAVY, spaceBefore=1, spaceAfter=7, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="H2x", fontName="Arial-Bold", fontSize=11.3, leading=14,
    textColor=BLUE, spaceBefore=7, spaceAfter=3, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="Bodyx", fontName="Arial", fontSize=8.8, leading=12.2,
    textColor=INK, spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="Smallx", fontName="Arial", fontSize=7.5, leading=10,
    textColor=MUTED, spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="Bulletx", fontName="Arial", fontSize=8.55, leading=11.6,
    textColor=INK, leftIndent=10, firstLineIndent=-8, spaceAfter=2.2,
))
styles.add(ParagraphStyle(
    name="Cellx", fontName="Arial", fontSize=7.75, leading=10.1,
    textColor=INK, spaceAfter=1,
))
styles.add(ParagraphStyle(
    name="CellHeadx", fontName="Arial-Bold", fontSize=7.9, leading=10.2,
    textColor=WHITE, spaceAfter=0,
))
styles.add(ParagraphStyle(
    name="CardTitlex", fontName="Arial-Bold", fontSize=8.2, leading=10.2,
    textColor=TEAL, spaceAfter=2,
))
styles.add(ParagraphStyle(
    name="QuoteX", fontName="Arial-Italic", fontSize=8.5, leading=12,
    textColor=NAVY, leftIndent=8, rightIndent=8, spaceAfter=1,
))
styles.add(ParagraphStyle(
    name="Centerx", fontName="Arial-Bold", fontSize=8.2, leading=10.5,
    textColor=NAVY, alignment=TA_CENTER,
))
styles.add(ParagraphStyle(
    name="Rightx", fontName="Arial", fontSize=8, leading=10.5,
    textColor=MUTED, alignment=TA_RIGHT,
))


def P(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def bullet(text):
    return P(f'<font color="{TEAL.hexval()}">●</font>&nbsp; {text}', "Bulletx")


def h1(text, kicker=None):
    items = []
    if kicker:
        items.append(P(f'<font color="{TEAL.hexval()}"><b>{escape(kicker.upper())}</b></font>', "Smallx"))
    items.append(P(text, "H1x"))
    return KeepTogether(items)


def h2(text):
    return P(text, "H2x")


def make_table(rows, widths, header=True, backgrounds=None, repeatRows=1, padd=5):
    converted = []
    for ri, row in enumerate(rows):
        converted.append([
            cell if isinstance(cell, (Paragraph, Table)) else P(str(cell), "CellHeadx" if header and ri == 0 else "Cellx")
            for cell in row
        ])
    t = Table(converted, colWidths=widths, repeatRows=repeatRows if header else 0, hAlign="LEFT")
    rules = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), padd),
        ("RIGHTPADDING", (0, 0), (-1, -1), padd),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
    ]
    if header:
        rules.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
        if len(rows) > 1:
            rules.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE_BLUE]))
    elif backgrounds:
        for row_i, color in enumerate(backgrounds):
            rules.append(("BACKGROUND", (0, row_i), (-1, row_i), color))
    t.setStyle(TableStyle(rules))
    return t


def info_card(title, body, color=PALE):
    t = Table([[P(title, "CardTitlex")], [P(body, "Bodyx")]], colWidths=[166 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
        ("LINEBEFORE", (0, 0), (0, -1), 3, TEAL),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def source_link(label, url):
    return f'<link href="{url}" color="{BLUE.hexval()}"><u>{escape(label)}</u></link>'


def on_page(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(18 * mm, PAGE_H - 14 * mm, PAGE_W - 18 * mm, PAGE_H - 14 * mm)
        canvas.setFont("Arial-Bold", 7)
        canvas.setFillColor(MUTED)
        canvas.drawString(18 * mm, PAGE_H - 10.8 * mm, "CHARGECORE  /  PRODUCT SOLUTION ENGINEER")
    canvas.setStrokeColor(LINE)
    canvas.line(18 * mm, 13 * mm, PAGE_W - 18 * mm, 13 * mm)
    canvas.setFont("Arial", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, 8.5 * mm, "Tài liệu ôn tập cá nhân • cập nhật 01/10/2026")
    canvas.drawRightString(PAGE_W - 18 * mm, 8.5 * mm, f"{doc.page}")
    canvas.restoreState()


class GuideDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(18 * mm, 18 * mm, PAGE_W - 36 * mm, PAGE_H - 37 * mm,
                      leftPadding=0, rightPadding=0, topPadding=2 * mm, bottomPadding=0, id="normal")
        self.addPageTemplates([PageTemplate(id="all", frames=frame, onPage=on_page)])


story = []

# PAGE 1 — quick orientation
story += [Spacer(1, 7 * mm)]
story.append(P("SỔ TAY ÔN PHỎNG VẤN", "CoverSub"))
story.append(P("Product Solution Engineer<br/>Chargecore Vietnam", "CoverTitle"))
story.append(P("Học nhanh theo đúng buổi hẹn • Trọng tâm: sản phẩm, kiểm thử và giải quyết vấn đề", "CoverSub"))
story.append(Spacer(1, 2 * mm))
story.append(info_card(
    "THÔNG TIN BUỔI PHỎNG VẤN",
    "<b>Thời gian:</b> 17:00, thứ Sáu, ngày 02/10/2026<br/>"
    "<b>Địa điểm:</b> Tầng 6, tòa nhà Silk Path, số 04 Lý Sơn, phường Việt Hưng, Hà Nội<br/>"
    "<b>Vị trí:</b> Product Solution Engineer<br/>"
    "<b>Việc cần làm:</b> trả lời email mời để xác nhận tham dự.",
    PALE,
))
story.append(Spacer(1, 3 * mm))
story.append(h2("Một câu để nhớ về vai trò"))
story.append(info_card(
    "CẦU NỐI GIỮA NHU CẦU VÀ SẢN PHẨM ĐÃ ĐƯỢC KIỂM CHỨNG",
    "Hiểu vấn đề của khách hàng → viết yêu cầu có thể đo được → phối hợp R&D → kiểm thử bộ sạc, xe và backend → xác nhận/hỗ trợ sau bán → đưa phản hồi quay lại cải tiến sản phẩm.",
    PALE_BLUE,
))
story.append(Spacer(1, 2 * mm))
story.append(h2("Nếu chỉ còn 15 phút, ôn 5 ý này"))
for s in [
    "Phân biệt <b>AC/DC</b>: bộ sạc AC cấp AC và xe thường đổi sang DC bằng bộ sạc trên xe; bộ sạc DC thực hiện chuyển đổi công suất bên ngoài xe.",
    "Phân biệt giao tiếp: <b>OCPP</b> nối trạm sạc với hệ thống quản lý; <b>ISO 15118 / DIN 70121</b> liên quan giao tiếp giữa xe và EVSE.",
    "Khi test tương thích, ghi rõ <b>mẫu xe, phiên bản xe, model/firmware trạm, đầu cắm, backend, mạng và kết quả mong đợi</b>.",
    "Khi có lỗi: tái hiện → khoanh lớp lỗi → lưu log/thời điểm/mã lỗi → đánh giá an toàn và ảnh hưởng → phối hợp xử lý → kiểm thử hồi quy → báo khách hàng.",
    "Trả lời bằng ví dụ thật theo <b>Tình huống – Mục tiêu – Hành động của bạn – Kết quả – Bài học</b>. Không tự nhận kinh nghiệm mình chưa có.",
]: story.append(bullet(s))
story.append(Spacer(1, 2 * mm))
story.append(P("Dựa trên email mời bạn cung cấp và bản mô tả công việc công khai tìm được cho vị trí gần trùng tên. Bản mô tả trên CVWork là nguồn bên thứ ba; hãy hỏi lại phạm vi ưu tiên của đội ngũ trong buổi gặp. [1]", "Smallx"))
story.append(PageBreak())

# PAGE 2 — company and role
story.append(h1("Chargecore và công việc này", "01 · Hiểu trước khi trả lời"))
story.append(P("Chargecore hoạt động trong hệ sinh thái sạc xe điện. Website toàn cầu giới thiệu sản phẩm sạc AC/DC, công nghệ điều khiển và nền tảng quản lý; một trang sản phẩm Coremini 60 kW nêu hỗ trợ OCPP 1.6J, chức năng cân bằng tải động và khả năng nâng cấp giao thức. Đây là thông tin do hãng công bố, áp dụng cho trang/model được nêu; không nên suy rộng thành thông số của mọi bộ sạc. [2][3]"))
story.append(h2("Mô tả công việc công khai cho vị trí gần trùng tên"))
rows = [
    ["Nhóm việc", "Đầu ra bạn cần tạo", "Bạn phối hợp với"],
    ["Phát triển sản phẩm", "Yêu cầu khách hàng; mô tả giải pháp; đặc tả, use case và test case.", "Khách hàng, kinh doanh/presales, R&D tại Trung Quốc."],
    ["Kiểm thử và xác nhận", "Kiểm tra theo đặc tả; tương thích nhiều mẫu xe; kết nối và tích hợp OCPP/backend; hỗ trợ khách hàng phê duyệt/chứng nhận.", "R&D, QA, đội dịch vụ sau bán hàng, khách hàng."],
    ["Cải tiến sản phẩm", "Tổng hợp phản hồi sau bán hàng; đề xuất cải thiện độ ổn định, dễ sử dụng và giảm lỗi.", "Dịch vụ, sản phẩm, R&D và đội thị trường."],
    ["Hỗ trợ kỹ thuật cấp 2", "Điều tra sự cố sản phẩm phức tạp; hướng dẫn/đào tạo kỹ thuật cho đội dịch vụ sau bán hàng.", "Đội dịch vụ, khách hàng và R&D Trung Quốc."],
]
story.append(make_table(rows, [30 * mm, 79 * mm, 57 * mm]))
story.append(Spacer(1, 2 * mm))
story.append(h2("Yêu cầu ứng viên trong tin đăng công khai"))
for s in [
    "Nền tảng điện, điện tử–viễn thông, tự động hóa hoặc ngành liên quan; có trải nghiệm thực hành với lập trình nhúng và thiết bị điện là lợi thế trực tiếp.",
    "Hiểu quy trình phát triển và kiểm thử sản phẩm; hiểu OCPP và ISO 15118 là điểm cộng mạnh.",
    "Tiếng Anh ở mức làm việc; tiếng Trung được ưu tiên. Tin đăng cũng nhấn mạnh phân tích, xử lý vấn đề và trao đổi kỹ thuật với khách hàng.",
]: story.append(bullet(s))
story.append(h2("Cách hiểu đúng về vai trò"))
story.append(P("Đây là vị trí thiên về giải pháp sản phẩm và kiểm chứng thực tế. Người làm tốt không chỉ nói sản phẩm có tính năng gì; họ chứng minh tính năng đáp ứng trường hợp sử dụng nào, với cấu hình nào, bằng kết quả nào và xử lý ra sao khi xe, trạm hoặc backend không tương thích."))
story.append(info_card(
    "ĐIỂM MẠNH NÊN THỂ HIỆN",
    "Tư duy hệ thống • đặt câu hỏi làm rõ • viết yêu cầu kiểm thử được • phân tích có bằng chứng • giao tiếp rõ với khách hàng và R&D • theo lỗi tới khi đóng • ưu tiên an toàn và trải nghiệm người dùng.",
    PALE,
))
story.append(h2("Giới thiệu về Chargecore trong 20 giây"))
story.append(P("“Theo tìm hiểu của em, Chargecore phát triển giải pháp sạc xe điện gồm thiết bị AC/DC và phần mềm/kết nối quản lý. Em quan tâm vị trí này vì nó kết hợp hiểu nhu cầu khách hàng với đặc tả, kiểm thử tương thích xe và backend, rồi phản hồi lại cho đội phát triển để cải thiện sản phẩm. Em muốn tìm hiểu thêm đội đang ưu tiên dòng sản phẩm và thị trường nào.”", "QuoteX"))
story.append(Spacer(1, 2 * mm))
story.append(P("Lưu ý: trách nhiệm trên lấy từ tin tuyển dụng bên thứ ba [1], không phải JD đính kèm email. Hãy xác nhận tại phỏng vấn: sản phẩm cụ thể, OCPP/firmware đang dùng, tỷ lệ công việc giữa văn phòng và hiện trường, và tiêu chí thành công 3–6 tháng đầu." , "Smallx"))
story.append(PageBreak())

# PAGE 3 — charging basics
story.append(h1("Nền tảng sạc xe điện trong 5 phút", "02 · Thiết bị và công suất"))
story.append(P("Hãy nhìn cả chuỗi thay vì chỉ nhìn “cục sạc”. Mỗi phiên sạc phụ thuộc vào nguồn điện, EVSE, cáp/đầu nối, khả năng nhận sạc của xe, xác thực và backend."))
flow = [[P("LƯỚI ĐIỆN / TỦ ĐIỆN", "Centerx"), P("EVSE / TRỤ SẠC", "Centerx"), P("XE ĐIỆN", "Centerx"), P("CSMS / BACKEND", "Centerx")],
        [P("Nguồn, bảo vệ, giới hạn công suất", "Cellx"), P("Chuyển đổi, điều khiển, đo lường, kết nối", "Cellx"), P("Bộ sạc trên xe hoặc pin nhận công suất", "Cellx"), P("Xác thực, theo dõi phiên, lệnh và dữ liệu", "Cellx")]]
t = Table(flow, colWidths=[41.5 * mm, 41.5 * mm, 41.5 * mm, 41.5 * mm], hAlign="LEFT")
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (0, 0), PALE_BLUE), ("BACKGROUND", (1, 0), (1, 0), PALE),
    ("BACKGROUND", (2, 0), (2, 0), PALE_BLUE), ("BACKGROUND", (3, 0), (3, 0), PALE),
    ("GRID", (0, 0), (-1, -1), 0.45, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(Spacer(1, 2 * mm))
story.append(h2("AC và DC khác nhau ở đâu?"))
rows = [
    ["", "Sạc AC", "Sạc DC"],
    ["Chuyển đổi điện", "Bộ sạc trên xe thường đổi AC thành DC cho pin.", "Bộ sạc ngoài xe đổi điện lưới thành DC trước khi cấp cho xe."],
    ["Điều quyết định công suất", "Giới hạn của trạm, bộ sạc trên xe, nguồn điện và cài đặt.", "Giới hạn của trạm, xe/pin, nguồn điện, nhiệt độ và chia công suất."],
    ["Câu hỏi tương thích", "Xe nhận được bao nhiêu pha/dòng AC? Đầu nối và bảo vệ phù hợp không?", "Xe hỗ trợ chuẩn/cấu hình DC nào? Điện áp, dòng và giao tiếp có giao nhau không?"],
]
story.append(make_table(rows, [28 * mm, 82 * mm, 56 * mm]))
story.append(Spacer(1, 2 * mm))
story.append(h2("Công suất và năng lượng"))
story.append(P("<b>kW</b> là tốc độ truyền năng lượng; <b>kWh</b> là lượng năng lượng theo thời gian. Với DC, ước lượng cơ bản: P (W) = V (V) × I (A). Với AC ba pha cân bằng: P ≈ √3 × V<sub>dây-dây</sub> × I × hệ số công suất. Công suất thực tế còn bị giới hạn bởi xe, trạm, nguồn điện, nhiệt và cơ chế chia tải; thông số định mức không đảm bảo xe luôn nhận đúng mức đó."))
story.append(info_card("CÂU TRẢ LỜI AN TOÀN", "“Em sẽ không kết luận chỉ từ công suất ghi trên trụ. Em sẽ xác minh cấu hình điện, model xe, giới hạn bộ sạc trên xe/pin, cài đặt chia tải và dữ liệu đo trong phiên.”", PALE_BLUE))
story.append(PageBreak())

# PAGE 4 — protocol and OCPP
story.append(h1("Giao thức: phân biệt đúng lớp", "03 · Trạm – xe – backend"))
rows = [
    ["Giao tiếp", "Kết nối", "Nó giúp làm gì?"],
    ["OCPP", "Trạm sạc ↔ hệ thống quản lý trung tâm (CSMS/backend)", "Theo dõi trạng thái trạm, xác thực/điều khiển phiên, đo lường và trao đổi dữ liệu vận hành. OCA định nghĩa OCPP như giao thức giữa charge point và central system. [4]"],
    ["ISO 15118 / DIN 70121", "Xe điện ↔ EVSE", "Trao đổi thông tin để thiết lập và điều khiển phiên sạc; hỗ trợ các luồng giao tiếp xe–trạm. ISO 15118-2 mô tả giao tiếp giữa EV và EVSE. [3][5]"],
    ["Kết nối mạng", "Trạm ↔ router/SIM/LAN ↔ Internet", "Cho phép trạm tới backend; cần kiểm tra DNS, IP, cổng, TLS/chứng chỉ, WebSocket và firewall theo cấu hình thực tế."],
]
story.append(make_table(rows, [34 * mm, 47 * mm, 85 * mm]))
story.append(Spacer(1, 2 * mm))
story.append(h2("Mô hình OCPP cần nhớ"))
story.append(P("Trạm là thiết bị đầu cuối. CSMS là hệ thống giám sát/quản lý. OCPP là giao thức ứng dụng giữa hai bên; nó không thay thế giao tiếp xe–trạm, đầu cắm, an toàn điện hay logic nội bộ của xe."))
flow2 = [[P("TRẠM", "Centerx"), P("OCPP qua mạng", "Centerx"), P("CSMS / BACKEND", "Centerx")],
         [P("Boot / trạng thái / dữ liệu phiên", "Cellx"), P("Kết nối, xác thực, thông điệp hai chiều", "Cellx"), P("Nhận dữ liệu, gửi cấu hình/lệnh theo hỗ trợ", "Cellx")]]
t = Table(flow2, colWidths=[55 * mm, 55 * mm, 56 * mm])
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), PALE), ("GRID", (0, 0), (-1, -1), 0.45, LINE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
]))
story.append(t)
story.append(h2("OCPP 1.6 và 2.0.1: điều cần nói chính xác"))
for s in [
    "OCPP 1.6 vẫn phổ biến; 2.0.1 bổ sung quản lý thiết bị, xử lý giao dịch và bảo mật nâng cao. OCA nói 2.0.1 không tương thích ngược với 1.6; 2.1 là phiên bản mới hơn và tương thích với 2.0.1. [6]",
    "Trang sản phẩm Chargecore Coremini 60 kW nêu OCPP 1.6J và nâng cấp 2.0.1 cho model/trang đó. Hãy hỏi đúng SKU, firmware, profile được hỗ trợ và backend mục tiêu. [3]",
    "Tên lệnh và trình tự giao dịch thay đổi theo phiên bản. Trong buổi phỏng vấn, nói về luồng và cách kiểm chứng trước khi khẳng định tên message cụ thể.",
]: story.append(bullet(s))
story.append(info_card("CÂU NHỚ", "OCPP = trạm–backend. ISO 15118/DIN 70121 = xe–trạm. Đầu cắm, điện lực và bảo vệ = các lớp khác cần xác nhận riêng.", PALE_BLUE))
story.append(PageBreak())

# PAGE 5 — requirements and test approach
story.append(h1("Từ yêu cầu đến bài kiểm thử", "04 · Làm việc có bằng chứng"))
story.append(P("Một yêu cầu tốt mô tả ai cần gì, trong điều kiện nào và làm sao biết đã đạt. Tránh yêu cầu mơ hồ như “sạc nhanh hơn” hoặc “tương thích tốt hơn” nếu chưa có chỉ số và phạm vi."))
rows = [
    ["Bước", "Đầu ra / câu hỏi kiểm tra"],
    ["1. Làm rõ", "Ai là người dùng? Vấn đề hiện tại là gì? Xe/trạm/backend/địa điểm nào? Mức ưu tiên và tác động nếu lỗi?"],
    ["2. Đặc tả", "Luồng chính và trường hợp biên; điều kiện trước; dữ liệu đầu vào; trạng thái mong đợi; giới hạn/ngoại lệ; phiên bản phần cứng và firmware."],
    ["3. Tiêu chí chấp nhận", "Có thể quan sát/đo được, lặp lại được, có ngưỡng hoặc trạng thái rõ; gắn với một yêu cầu cụ thể."],
    ["4. Kiểm thử", "Kiểm thử trên thiết bị, xe và backend; lưu cấu hình, thời điểm, log, mã lỗi, kết quả thực tế và expected/actual."],
    ["5. Phê duyệt", "Đưa bằng chứng cho khách hàng; ghi nhận sai khác; theo dõi lỗi tới khi sửa, xác nhận và đóng."],
]
story.append(make_table(rows, [37 * mm, 145 * mm]))
story.append(h2("Ví dụ: yêu cầu kết nối backend"))
story.append(info_card(
    "YÊU CẦU CÓ THỂ KIỂM THỬ",
    "Khi trạm có nguồn và cấu hình endpoint hợp lệ, sau khi khởi động lại, trạm kết nối tới CSMS đã chỉ định và xuất hiện online trong thời hạn hai bên thống nhất; mất mạng thì trạm phục hồi kết nối sau khi mạng trở lại, không tạo phiên sạc trùng. Ghi lại model, firmware, giao thức, thời gian, trạng thái và log.",
    PALE,
))
story.append(h2("Bảng kiểm tối thiểu cho xác nhận tương thích"))
rows = [
    ["Lớp", "Ghi lại / kiểm tra"],
    ["Xe", "Hãng, model/phiên bản, năm hoặc trim nếu quan trọng, phiên bản phần mềm, giới hạn AC/DC."],
    ["Trạm", "SKU/model, đầu cắm, firmware, công suất định mức, cấu hình và mã lỗi."],
    ["Điện và cài đặt", "Điện áp/pha/dòng; giới hạn tại site; chia tải; thời điểm; điều kiện môi trường."],
    ["Backend/mạng", "CSMS, phiên bản OCPP, endpoint, TLS/chứng chỉ, kết quả online, xác thực, sự kiện phiên."],
    ["Kết quả", "Có bắt đầu/dừng được không; công suất đo; thông báo lỗi; log; expected vs actual; có tái hiện không."],
]
story.append(make_table(rows, [33 * mm, 149 * mm]))
story.append(P("Đừng coi một lần thử thành công là đủ. Lặp lại với cùng cấu hình, kiểm tra trường hợp lỗi, lưu phiên bản và chạy hồi quy sau khi có bản sửa.", "Smallx"))
story.append(PageBreak())

# PAGE 6 — troubleshooting case
story.append(h1("Tình huống kỹ thuật mẫu", "05 · Nói theo quy trình"))
story.append(info_card("TÌNH HUỐNG", "Trạm hiện online trên backend nhưng một mẫu xe không bắt đầu sạc. Khách hàng cần câu trả lời nhanh.", PALE_BLUE))
story.append(h2("Cách xử lý có thứ tự"))
rows = [
    ["Bước", "Việc làm", "Bằng chứng cần có"],
    ["1. An toàn và ảnh hưởng", "Xác nhận không có nguy cơ điện/nhiệt/hư hỏng; dừng thử nếu có dấu hiệu nguy hiểm. Xác định một xe hay nhiều xe, một trạm hay cả site.", "Khách hàng bị ảnh hưởng, thời điểm, hiện trường, lỗi hiển thị."],
    ["2. Tái hiện", "Ghi đúng model xe, cổng, trạm, firmware, backend, xác thực, trạng thái cáp và các bước thao tác.", "Video/ảnh nếu được phép, timestamp, log trạm/CSMS, mã lỗi."],
    ["3. Khoanh lớp lỗi", "Tách xe–EVSE, trạm–backend, mạng/xác thực, nguồn điện và cấu hình site. So sánh với xe/trạm đã biết hoạt động tốt.", "Ma trận xe × trạm × firmware × backend; trạng thái từng điểm."],
    ["4. Tạo giả thuyết và kiểm tra", "Thay từng biến một; kiểm tra phiên bản giao thức và trình tự xác thực; kiểm tra giới hạn dòng/điện áp, cấu hình và lỗi trong log.", "Kết quả từng phép thử và giả thuyết được loại trừ/xác nhận."],
    ["5. Khắc phục và xác nhận", "Chuyển R&D gói lỗi có expected/actual và bằng chứng; thống nhất workaround an toàn; kiểm thử bản sửa, xe khác và hồi quy.", "Bản phần mềm/cấu hình, test report, khách hàng xác nhận."],
]
story.append(make_table(rows, [29 * mm, 87 * mm, 66 * mm]))
story.append(h2("Mẫu câu trả lời phỏng vấn"))
story.append(P("“Đầu tiên em xác định phạm vi ảnh hưởng và kiểm tra an toàn. Sau đó em tái hiện lỗi với cấu hình được ghi rõ, chia hệ thống thành xe–trạm, trạm–backend, mạng/xác thực và nguồn điện. Em lấy log với timestamp, mã lỗi và expected/actual; nếu cần em so sánh một xe/trạm đã biết tốt và chỉ đổi một biến mỗi lần. Khi có giả thuyết, em phối hợp R&D với gói bằng chứng đủ để tái hiện, kiểm tra bản sửa cùng khách hàng và chạy hồi quy trước khi kết luận. Em sẽ cập nhật tiến độ và tác động cho khách hàng trong lúc điều tra.”", "QuoteX"))
story.append(h2("Một phiếu lỗi tốt cần có"))
for s in [
    "Tiêu đề ngắn + mức độ ảnh hưởng + môi trường tái hiện.",
    "Các bước tái hiện, kết quả mong đợi, kết quả thực tế, tần suất và phạm vi.",
    "Model/SKU, serial nếu được phép, firmware, phiên bản backend/OCPP, mạng và cấu hình.",
    "Timestamp và múi giờ, log liên quan, mã lỗi, ảnh/video đã che dữ liệu nhạy cảm.",
    "Workaround an toàn, người phụ trách, bản sửa, test hồi quy và xác nhận khách hàng.",
]: story.append(bullet(s))
story.append(info_card("TRÁNH NÓI", "“Chắc do xe” / “trạm vẫn online nên backend không lỗi” / “em sẽ thử bypass bảo vệ”. Thay bằng giả thuyết có thể kiểm tra và bằng chứng cần thu.", PALE))
story.append(PageBreak())

# PAGE 7 — interview answers
story.append(h1("Câu hỏi thường gặp và cách trả lời", "06 · Dùng ví dụ thật của bạn"))
story.append(P("Tin tuyển dụng công khai nhấn mạnh yêu cầu khách hàng, test case, kiểm thử xe, OCPP/backend, cải tiến sản phẩm và hỗ trợ kỹ thuật cấp 2. Các câu hỏi dưới đây là khả năng chuẩn bị, không phải lịch phỏng vấn đã xác nhận. [1]"))
story.append(h2("1. Hãy giới thiệu về bạn"))
story.append(P("Khung 45–60 giây: <b>nền tảng hiện tại</b> → <b>2 kỹ năng liên quan</b> → <b>một ví dụ có kết quả</b> → <b>vì sao vị trí này</b>. Nói ngắn gọn và chọn ví dụ gần với giải quyết vấn đề, kiểm thử, khách hàng hoặc phối hợp nhóm."))
story.append(P("“Em là [ngành/vai trò hiện tại], có kinh nghiệm/thực hành về [kỹ năng liên quan]. Trong [ví dụ thật], em [hành động cụ thể] và đạt [kết quả đo được]. Em thích biến nhu cầu thành giải pháp có thể kiểm chứng; vì vậy em quan tâm vị trí Product Solution Engineer, nơi cần phối hợp giữa khách hàng, kiểm thử và R&D.”", "QuoteX"))
story.append(h2("2. Bạn chưa làm EV charging, vì sao phù hợp?"))
story.append(P("Đừng giấu khoảng trống. Hãy chỉ ra transferable skills và kế hoạch học: “Em chưa làm trực tiếp với [phần chưa biết]. Em đã làm [ví dụ gần nhất] theo cách [quy trình]; kỹ năng đó áp dụng được vào làm rõ yêu cầu và điều tra lỗi. Em đang học AC/DC, lớp EV–trạm và OCPP–backend. Khi gặp nội dung mới, em sẽ kiểm chứng bằng tài liệu, log và test có kiểm soát.”"))
story.append(h2("3. Bạn chuyển yêu cầu mơ hồ thành đặc tả thế nào?"))
story.append(P("Nêu câu hỏi làm rõ người dùng, luồng hiện tại, ngoại lệ, môi trường, ràng buộc và mức ưu tiên. Sau đó viết use case, tiêu chí chấp nhận đo được, test case và người phê duyệt. Đưa một ví dụ thật bạn từng làm."))
story.append(h2("4. Bạn xử lý bất đồng với R&D / khách hàng ra sao?"))
story.append(P("Tách ý kiến khỏi dữ liệu. Ghi rõ vấn đề, tác động, cấu hình, expected/actual, bằng chứng, quyết định cần xin và thời hạn. Với R&D, gửi bước tái hiện ngắn; với khách hàng, giải thích ảnh hưởng và nhịp cập nhật. Nếu chưa biết nguyên nhân, nói rõ điều đã xác nhận và bước kế tiếp."))
story.append(h2("5. Bạn đánh giá bản sửa đã sẵn sàng chưa?"))
story.append(P("Kiểm tra test case gốc đã đạt; các case biên và hồi quy không tạo lỗi mới; model/firmware/backend mục tiêu được ghi rõ; log và kết quả có thể truy xuất; rủi ro còn lại được thông báo; khách hàng/QA phê duyệt theo quy trình."))
story.append(h2("6. Hãy kể về một lỗi khó bạn đã giải quyết"))
story.append(P("Dùng STAR ngắn: <b>S</b> tình huống và tác động; <b>T</b> nhiệm vụ của bạn; <b>A</b> các bước và quyết định của chính bạn; <b>R</b> kết quả bằng số/trạng thái; sau đó thêm một câu bài học. Chọn ví dụ thật, không nhất thiết phải thuộc ngành xe điện."))
story.append(info_card("MẸO", "Đừng chỉ nói “chúng em đã giải quyết”. Nêu rõ phần việc của bạn, dữ liệu bạn dùng, cách bạn phối hợp và kết quả kiểm chứng được.", PALE_BLUE))
story.append(PageBreak())

# PAGE 8 — English and questions
story.append(h1("Câu hỏi nên hỏi và tiếng Anh hữu ích", "07 · Thể hiện tư duy sản phẩm"))
story.append(h2("Nên hỏi nhà tuyển dụng 3–5 câu"))
for s in [
    "Trong 3 tháng đầu, kết quả nào cho thấy người ở vị trí này đang làm tốt?",
    "Nhóm đang tập trung vào model AC/DC, khách hàng và thị trường nào?",
    "Các phiên bản OCPP, firmware và backend/CSMS nào đang là phạm vi kiểm thử chính?",
    "Đội có xe thử nghiệm, test bench, log và quy trình tái hiện lỗi như thế nào?",
    "Quy trình phối hợp với R&D ở Trung Quốc: ngôn ngữ, ticket, múi giờ, SLA và quyền quyết định ra sao?",
    "Tỷ lệ giữa làm sản phẩm/kiểm thử, hỗ trợ khách hàng và đi hiện trường thường như thế nào?",
    "Khó khăn tương thích hoặc phản hồi sau bán hàng nào đội muốn vị trí này xử lý trước?",
]: story.append(bullet(s))
story.append(h2("Tiếng Anh dùng khi cần làm rõ"))
rows = [
    ["Mục đích", "Câu ngắn, tự nhiên"],
    ["Làm rõ phạm vi", "Could you clarify the target vehicle models, charger firmware, and backend version?"],
    ["Nói về giả thuyết", "My current hypothesis is that the issue is in the authorization flow, but I would verify it with the station and backend logs."],
    ["Nói về kiểm thử", "I would reproduce the issue, change one variable at a time, and compare the expected and actual results."],
    ["Nói khi chưa biết", "I haven't worked with this exact protocol version yet. I would check the specification and validate the behavior on a controlled test setup."],
    ["Cập nhật khách hàng", "We have confirmed the issue affects [scope]. We are collecting [evidence], and I will share the next update by [time]."],
    ["Xác nhận thành công", "The fix passed the original test case and the regression checks on [models / firmware]."],
]
story.append(make_table(rows, [35 * mm, 147 * mm]))
story.append(h2("Từ vựng cần nhận ra"))
rows = [
    ["Thuật ngữ", "Nghĩa nhanh"],
    ["EVSE", "Electric Vehicle Supply Equipment — thiết bị cấp điện cho xe điện."],
    ["CSMS", "Charging Station Management System — hệ thống quản lý trạm sạc; thường được gọi là backend."],
    ["Use case / test case", "Trường hợp sử dụng / các bước kiểm thử với dữ liệu và kết quả mong đợi."],
    ["Interoperability", "Khả năng các xe, trạm, backend và cấu hình khác nhau hoạt động cùng nhau."],
    ["Regression test", "Kiểm tra lại luồng cũ sau thay đổi để phát hiện lỗi phát sinh."],
]
story.append(make_table(rows, [38 * mm, 144 * mm]))
story.append(PageBreak())

# PAGE 9 — study plan, logistics and sources
story.append(h1("Ôn trong tối nay và chuẩn bị đi", "08 · Kế hoạch và nguồn"))
story.append(h2("Kế hoạch ôn 60 phút"))
rows = [
    ["Thời gian", "Việc ôn"],
    ["0–10 phút", "Đọc trang 1–2; nói to vai trò bằng một câu; nhớ 3 nhóm việc: yêu cầu, validation, cải tiến."],
    ["10–25 phút", "Đọc trang 3–4; tự giải thích AC/DC, kW/kWh, OCPP và ISO 15118 mà không nhìn tài liệu."],
    ["25–40 phút", "Ôn tình huống lỗi trang 6; tập trình bày quy trình trong 90 giây."],
    ["40–55 phút", "Chuẩn bị 3 chuyện thật theo STAR: xử lý lỗi, phối hợp bất đồng, cải thiện quy trình/sản phẩm."],
    ["55–60 phút", "Chọn 3 câu hỏi cho nhà tuyển dụng; gửi email xác nhận; kiểm tra đường đi và giấy tờ."],
]
story.append(make_table(rows, [31 * mm, 151 * mm]))
story.append(h2("Checklist trước khi rời nhà"))
for s in [
    "Đã gửi email xác nhận; lưu địa chỉ và số điện thoại liên hệ nếu có.",
    "Tính thời gian đi đến số 04 Lý Sơn, phường Việt Hưng; cố gắng đến trước 10–15 phút.",
    "Mang CV bản mới nhất, giấy tờ tùy thân, sổ ghi chép và bút; chuẩn bị ví dụ dự án có thể nói trong 1–2 phút.",
    "Không chia sẻ tài liệu mật của công ty cũ; mô tả bằng dữ liệu đã được phép công bố.",
    "Đến nơi hỏi lễ tân/bảo vệ tòa nhà Silk Path để lên tầng 6; nếu thay đổi lịch/địa điểm, xác minh qua email mời.",
]: story.append(bullet(s))
story.append(h2("Email xác nhận tham dự"))
story.append(info_card(
    "MẪU ĐỂ GỬI TRẢ LỜI EMAIL MỜI",
    "<b>Tiêu đề:</b> Xác nhận tham dự phỏng vấn – Product Solution Engineer – Quang<br/><br/>"
    "Kính gửi Chargecore,<br/>"
    "Em xác nhận sẽ tham dự buổi phỏng vấn vào 17h00, thứ Sáu ngày 02/10/2026 tại Tầng 6, tòa nhà Silk Path, số 04 Lý Sơn, phường Việt Hưng, Hà Nội.<br/>"
    "Em cảm ơn Quý công ty và hẹn gặp anh/chị.<br/><br/>"
    "Trân trọng,<br/>Quang",
    PALE,
))
story.append(h2("Nguồn để đọc thêm"))
sources = [
    ("[1] Tin tuyển dụng Product Solution Engineer – EV Charger trên CVWork (nguồn bên thứ ba; dùng để suy ra nhóm trách nhiệm).", "https://cvwork.vn/viec-lam/viec/product-solution-engineer-ev-charger-303586"),
    ("[2] Chargecore Global – trang giới thiệu công ty và giải pháp.", "https://www.chargecoreglobal.com/"),
    ("[3] Chargecore Coremini 60 kW – trang sản phẩm; xem thông số riêng của model và xác nhận lại firmware/SKU.", "https://www.chargecoreglobal.com/coremini-60kw-fast-dc-charging-stations-for-commercial"),
    ("[4] Open Charge Alliance – tổng quan OCPP.", "https://openchargealliance.org/protocols/ocpp-protocols/"),
    ("[5] ISO 15118-2 – mô tả giao tiếp EV–EVSE.", "https://www.iso.org/standard/55366.html"),
    ("[6] Open Charge Alliance FAQ – khác biệt phiên bản OCPP.", "https://openchargealliance.org/faq/"),
]
for label, url in sources:
    story.append(P(f'• {source_link(label, url)}', "Smallx"))
story.append(Spacer(1, 2 * mm))
story.append(P("Đây là tài liệu ôn tập, không phải đề cương phỏng vấn chính thức. Vai trò và tiêu chí có thể thay đổi theo nhóm tuyển dụng; hãy ưu tiên thông tin nhà tuyển dụng xác nhận trực tiếp.", "Smallx"))


doc = GuideDocTemplate(
    str(OUT), pagesize=A4,
    leftMargin=18 * mm, rightMargin=18 * mm,
    topMargin=17 * mm, bottomMargin=17 * mm,
    title="Cẩm nang phỏng vấn Chargecore Product Solution Engineer",
    author="OpenAI",
    subject="Tài liệu ôn phỏng vấn ngày 02/10/2026",
)
doc.build(story)
print(OUT.as_posix())
