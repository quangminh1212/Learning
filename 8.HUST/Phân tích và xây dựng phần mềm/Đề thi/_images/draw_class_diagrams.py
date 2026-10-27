from pathlib import Path

from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


OUT = Path(__file__).resolve().parent
PAGE_W, PAGE_H = 560, 390
FONT_DIR = Path("C:/Windows/Fonts")
pdfmetrics.registerFont(TTFont("Arial", str(FONT_DIR / "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_DIR / "arialbd.ttf")))

COLORS = {
    "boundary": colors.HexColor("#E6F2FA"),
    "control": colors.HexColor("#FFF1D6"),
    "interface": colors.HexColor("#FFF8CC"),
    "entity": colors.HexColor("#E8F4E8"),
}


def class_box(c, x, y, w, h, name, attrs, kind="entity", stereotype=None):
    c.setFillColor(COLORS[kind])
    c.setStrokeColor(colors.HexColor("#283747"))
    c.setLineWidth(0.8)
    c.roundRect(x, y, w, h, 3, stroke=1, fill=1)
    c.setFillColor(colors.HexColor("#455A64"))
    c.setFont("Arial", 6.2)
    c.drawCentredString(x + w / 2, y + h - 9, stereotype or f"<<{kind}>>")
    c.setFillColor(colors.HexColor("#17202A"))
    c.setFont("Arial-Bold", 8.4)
    c.drawCentredString(x + w / 2, y + h - 20, name)
    divider = y + h - 25
    c.setStrokeColor(colors.HexColor("#667782"))
    c.line(x, divider, x + w, divider)
    c.setFillColor(colors.HexColor("#17202A"))
    c.setFont("Arial", 6.6)
    line_y = divider - 9
    for attr in attrs:
        if line_y < y + 4:
            break
        c.drawString(x + 5, line_y, attr)
        line_y -= 8


def arrow(c, points, dashed=False, color="#536878"):
    c.saveState()
    c.setStrokeColor(colors.HexColor(color))
    c.setFillColor(colors.HexColor(color))
    c.setLineWidth(0.75)
    if dashed:
        c.setDash(3, 2)
    path = c.beginPath()
    path.moveTo(points[0][0], points[0][1])
    for x, y in points[1:]:
        path.lineTo(x, y)
    c.drawPath(path, stroke=1, fill=0)
    if len(points) > 1:
        x0, y0 = points[-2]
        x1, y1 = points[-1]
        dx, dy = x1 - x0, y1 - y0
        length = max((dx * dx + dy * dy) ** 0.5, 1)
        ux, uy = dx / length, dy / length
        px, py = -uy, ux
        size = 4.5
        c.setDash()
        head = c.beginPath()
        head.moveTo(x1, y1)
        head.lineTo(x1 - size * ux + 2.5 * px, y1 - size * uy + 2.5 * py)
        head.lineTo(x1 - size * ux - 2.5 * px, y1 - size * uy - 2.5 * py)
        head.close()
        c.drawPath(head, stroke=0, fill=1)
    c.restoreState()


def label(c, x, y, text):
    c.setFillColor(colors.HexColor("#34495E"))
    c.setFont("Arial", 6.2)
    c.drawString(x, y, text)


def draw(path, exam, lang):
    c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle(f"{exam} - class diagram")
    c.setFillColor(colors.HexColor("#17202A"))
    c.setFont("Arial-Bold", 11)
    c.drawString(18, 373, f"{exam} - So do lop thiet ke")
    c.setFont("Arial", 6.7)
    c.setFillColor(colors.HexColor("#52616B"))
    c.drawString(18, 360, "Dashed: service dependency; solid: domain association and multiplicity. Payment internals excluded.")

    # Boundary, control, and service dependencies.
    arrow(c, [(166, 322), (200, 322)], dashed=True)
    arrow(c, [(353, 322), (390, 322)], dashed=True)
    arrow(c, [(276, 295), (276, 272)], dashed=True)

    # Domain associations. Lines are drawn before boxes so labels remain legible.
    arrow(c, [(136, 236), (170, 236)])
    label(c, 137, 243, "1")
    label(c, 157, 243, "0..*")
    arrow(c, [(310, 236), (355, 236)])
    label(c, 311, 243, "1")
    label(c, 333, 243, "1..*")
    arrow(c, [(136, 129), (170, 129)])
    label(c, 137, 136, "1")
    label(c, 151, 136, "1..*")
    arrow(c, [(310, 129), (355, 129)])
    label(c, 311, 136, "1")
    label(c, 333, 136, "0..*")
    arrow(c, [(240, 98), (240, 70)])
    label(c, 244, 83, "1..*")
    arrow(c, [(448, 190), (448, 174)])
    label(c, 453, 178, "1")
    arrow(c, [(385, 98), (385, 70)])
    label(c, 368, 80, "1")
    arrow(c, [(495, 98), (495, 70)])
    label(c, 499, 80, "1")
    # A ticket belongs to one seat; route around the booking and room boxes.
    arrow(c, [(355, 202), (319, 202), (319, 49), (310, 49)])
    label(c, 321, 184, "0..*")
    label(c, 293, 54, "1")

    # User interface and service layer.
    if lang == "en":
        class_box(c, 18, 295, 148, 54, "BookingPage",
                  ["search(), showSeats()", "confirmBooking()"], "boundary")
        class_box(c, 200, 295, 153, 54, "BookingController",
                  ["search / reserve / confirm", "orchestrate use case"], "control")
        class_box(c, 390, 286, 152, 72, "Service interfaces",
                  ["ScreeningSearchService", "SeatAvailabilityService", "PricingService",
                   "NotificationService", "PaymentService*"], "interface")
        customer, booking, ticket = "Customer", "Booking", "BookingItem / Ticket"
        complex_name, room_name, show_name = "CinemaComplex", "ScreeningRoom", "Screening"
        seat_name, movie_name, operator_name = "Seat", "Movie", "Operator"
        customer_attrs = ["customerId, name", "phone, email"]
        booking_attrs = ["bookingId, createdAt", "status, totalAmount"]
        ticket_attrs = ["screening: Screening", "seat: Seat, unitPrice", "seatType, status"]
        complex_attrs = ["complexId, city"]
        room_attrs = ["roomId, roomNumber", "roomType, capacity"]
        show_attrs = ["start/end, breakTime", "type, screeningRoom", "movie, operator"]
        seat_attrs = ["seatId, row, number", "area, seatType"]
        movie_attrs = ["title", "duration"]
        operator_attrs = ["employeeId", "name"]
        note = "* Payment internals are excluded; only the interface is shown."
    else:
        class_box(c, 18, 295, 148, 54, "ManHinhDatVe",
                  ["timSuat(), hienThiGhe()", "xacNhanDatVe()"], "boundary")
        class_box(c, 200, 295, 153, 54, "DatVeController",
                  ["tim / giu ghe / xac nhan", "dieu phoi use case"], "control")
        class_box(c, 390, 286, 152, 72, "Service interfaces",
                  ["ISuatChieuService", "IGheService", "IDinhGia", "IThongBao",
                   "IThanhToanTrucTuyen*"], "interface")
        customer, booking, ticket = "KhachHang", "DonDatVe", "DatVe"
        complex_name, room_name, show_name = "CumRap", "PhongChieu", "SuatChieu"
        seat_name, movie_name, operator_name = "Ghe", "Phim", "NhanVienVanHanh"
        customer_attrs = ["maKH, hoTen", "dienThoai, email"]
        booking_attrs = ["maDatCho, thoiDiemDat", "phuongThuc, trangThai"]
        ticket_attrs = ["gioSuatChieu: LocalDateTime, tongTien: double",
                        "daThanhToanTruoc, khachDaDenQuay: boolean",
                        "ghe: Ghe, trangThai: TrangThai", "huyDatVe(now): double"]
        complex_attrs = ["maCum, thanhPho"]
        room_attrs = ["maPhong, soHieuCumRap", "loaiPhong, sucChua"]
        show_attrs = ["gioBatDau, gioKetThuc", "loaiSuatChieu", "phong, phim, nhanVien"]
        seat_attrs = ["maGhe, hang, khuVuc", "daDat, giaiPhong()"]
        movie_attrs = ["tenPhim", "thoiLuong"]
        operator_attrs = ["maNV", "hoTen"]
        note = "TrangThai = {DA_DAT, DA_HUY}; payment use case internals are excluded."

    class_box(c, 18, 204, 118, 65, customer, customer_attrs)
    class_box(c, 170, 204, 140, 65, booking, booking_attrs)
    class_box(c, 355, 190, 187, 84, ticket, ticket_attrs)
    class_box(c, 18, 98, 118, 62, complex_name, complex_attrs)
    class_box(c, 170, 98, 140, 70, room_name, room_attrs)
    class_box(c, 355, 98, 187, 76, show_name, show_attrs)
    class_box(c, 170, 10, 140, 60, seat_name, seat_attrs)
    class_box(c, 350, 10, 88, 60, movie_name, movie_attrs)
    class_box(c, 448, 10, 94, 60, operator_name, operator_attrs)

    c.showPage()
    c.save()


draw(OUT / "de1_class_diagram.pdf", "De 1", "en")
draw(OUT / "de2_class_diagram.pdf", "De 2", "vi")
print("Generated de1_class_diagram.pdf and de2_class_diagram.pdf")
