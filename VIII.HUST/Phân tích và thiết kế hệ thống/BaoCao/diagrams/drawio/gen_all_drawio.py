# -*- coding: utf-8 -*-
"""Generate editable .drawio files for all report diagrams."""
from __future__ import annotations

import html
import uuid
from pathlib import Path

OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

# Styles
S_ACTOR = "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;fillColor=#FFFFFF;strokeColor=#000000;"
S_UC = "ellipse;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=11;align=center;"
S_SYS = "rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=8 8;fillColor=none;strokeColor=#666666;verticalAlign=top;fontStyle=1;fontSize=13;align=center;spacingTop=8;"
S_RECT = "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=11;align=center;"
S_ROUNDED = "rounded=1;whiteSpace=wrap;html=1;fillColor=#F5F5F5;strokeColor=#000000;fontSize=11;align=center;fontStyle=1;"
S_PROCESS = "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=11;align=center;"
S_DECISION = "rhombus;whiteSpace=wrap;html=1;fillColor=#F0F0F0;strokeColor=#000000;fontSize=10;align=center;"
S_CLASS = "swimlane;fontStyle=1;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;startSize=26;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;"
S_CLASS_ATTR = "text;strokeColor=none;fillColor=none;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;fontSize=10;"
S_EDGE = "endArrow=block;html=1;rounded=0;endFill=1;strokeColor=#000000;"
S_EDGE_OPEN = "endArrow=open;html=1;rounded=0;endFill=0;strokeColor=#000000;"
S_EDGE_NONE = "endArrow=none;html=1;rounded=0;strokeColor=#000000;"
S_LIFELINE = "shape=umlLifeline;perimeter=lifelinePerimeter;whiteSpace=wrap;html=1;container=1;collapsible=0;recursiveResize=0;outlineConnect=0;size=30;fillColor=#FFFFFF;strokeColor=#000000;"
S_MSG = "html=1;verticalAlign=bottom;endArrow=block;endFill=1;rounded=0;strokeColor=#000000;fontSize=10;"
S_STATE = "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=12;align=center;arcSize=40;"
S_COMPONENT = "shape=component;align=left;spacingLeft=28;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontSize=11;"
S_CYL = "shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=12;fillColor=#F0F0F0;strokeColor=#000000;fontSize=10;align=center;"
S_NOTE = "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=12;fontStyle=1;"


class D:
    def __init__(self, name: str, w: int = 1200, h: int = 900):
        self.name = name
        self.w = w
        self.h = h
        self.cells: list[str] = []
        self._n = 2

    def _id(self) -> str:
        i = str(self._n)
        self._n += 1
        return i

    def node(self, value: str, x: float, y: float, w: float, h: float, style: str, parent: str = "1") -> str:
        cid = self._id()
        v = html.escape(value).replace("\n", "&#xa;")
        self.cells.append(
            f'<mxCell id="{cid}" value="{v}" style="{style}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )
        return cid

    def edge(self, src: str, tgt: str, label: str = "", style: str = S_EDGE, exitX=None, exitY=None, entryX=None, entryY=None) -> str:
        cid = self._id()
        v = html.escape(label) if label else ""
        extra = ""
        if exitX is not None:
            extra += f"exitX={exitX};exitY={exitY};exitDx=0;exitDy=0;"
        if entryX is not None:
            extra += f"entryX={entryX};entryY={entryY};entryDx=0;entryDy=0;"
        self.cells.append(
            f'<mxCell id="{cid}" value="{v}" style="{style}{extra}" edge="1" parent="1" source="{src}" target="{tgt}">'
            f'<mxGeometry relative="1" as="geometry"/></mxCell>'
        )
        return cid

    def class_box(self, title: str, attrs: list[str], x: float, y: float, w: float = 180) -> str:
        """UML-like class: title + attributes stacked (draw.io swimlane)."""
        h_row = 18
        h = 26 + h_row * max(len(attrs), 1) + 4
        cid = self._id()
        t = html.escape(title)
        self.cells.append(
            f'<mxCell id="{cid}" value="{t}" style="{S_CLASS}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )
        for a in attrs:
            aid = self._id()
            self.cells.append(
                f'<mxCell id="{aid}" value="{html.escape(a)}" style="{S_CLASS_ATTR}" vertex="1" parent="{cid}">'
                f'<mxGeometry width="{w}" height="{h_row}" as="geometry"/></mxCell>'
            )
        return cid

    def save(self, filename: str):
        body = "\n".join(self.cells)
        xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" agent="Grok-BaoCao-QLKH" version="24.0.0">
  <diagram id="{uuid.uuid4().hex[:8]}" name="{html.escape(self.name)}">
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.w}" pageHeight="{self.h}" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''
        path = OUT / filename
        path.write_text(xml, encoding="utf-8")
        print("wrote", path.name)
        return path


# ───────────────────────── 2.x Activity ─────────────────────────

def activity_flow(name: str, filename: str, steps: list[str], decisions: list[tuple], branches: list):
    """
    steps: main vertical process labels
    decisions: list of (step_index_after_which_decision, label)
    branches: list of (dec_idx, err_label, back_to_step_idx)
    Simplified: build linear activity like report.
    """
    d = D(name, 900, 1100)
    y = 40
    ids = []
    start = d.node("Bắt đầu", 300, y, 140, 40, S_ROUNDED)
    y += 70
    ids.append(start)
    main = []
    for s in steps:
        style = S_DECISION if s.startswith("?") else S_PROCESS
        w, h = (140, 70) if s.startswith("?") else (280, 44)
        x = 300 + (140 - w) / 2 + 70  # center-ish
        x = 230 if not s.startswith("?") else 300
        n = d.node(s.lstrip("?"), x, y, w, h, style)
        main.append(n)
        d.edge(ids[-1], n)
        ids.append(n)
        y += 80 if not s.startswith("?") else 100

    end = d.node("Kết thúc", 300, y, 140, 40, S_ROUNDED)
    d.edge(ids[-1], end)
    # error branches for decisions
    for i, s in enumerate(steps):
        if s.startswith("?"):
            err = d.node("Thông báo lỗi / từ chối", 560, 40 + 70 + i * 90, 200, 44, S_PROCESS)
            d.edge(main[i], err, "Không")
            # reconnect roughly to previous process
            if i > 0:
                d.edge(err, main[max(0, i - 2)], "")
    d.save(filename)


def gen_activity_nhap():
    d = D("Activity UC23 Lập phiếu nhập", 800, 1100)
    y, x = 30, 260
    nodes = []
    labels = [
        ("Bắt đầu", S_ROUNDED, 140, 40),
        ("NV lập phiếu nhập kho", S_PROCESS, 260, 44),
        ("Nhập NCC, kho, ngày nhập", S_PROCESS, 260, 44),
        ("Thêm chi tiết hàng hóa nhập", S_PROCESS, 260, 44),
        ("Dữ liệu hợp lệ?", S_DECISION, 140, 70),
        ("Gửi phiếu nhập để duyệt", S_PROCESS, 260, 44),
        ("Quản lý duyệt?", S_DECISION, 140, 70),
        ("Cập nhật tồn kho (tăng)", S_PROCESS, 260, 44),
        ("In / lưu phiếu nhập", S_PROCESS, 260, 44),
        ("Kết thúc", S_ROUNDED, 140, 40),
    ]
    for text, style, w, h in labels:
        n = d.node(text, x + (260 - w) / 2, y, w, h, style)
        if nodes:
            lab = ""
            if "hợp lệ" in labels[len(nodes) - 1][0] or "duyệt" in labels[len(nodes) - 1][0]:
                if "Gửi" in text or "Cập nhật" in text:
                    lab = "Có"
            d.edge(nodes[-1], n, lab)
        nodes.append(n)
        y += h + 28
    err1 = d.node("Báo lỗi, nhập lại", 560, 280, 180, 44, S_PROCESS)
    err2 = d.node("Từ chối, trả NV", 560, 520, 180, 44, S_PROCESS)
    d.edge(nodes[4], err1, "Không")
    d.edge(err1, nodes[2])
    d.edge(nodes[6], err2, "Không")
    d.edge(err2, nodes[1])
    d.save("2.1_activity_nhapkho.drawio")


def gen_activity_xuat():
    d = D("Activity UC28 Lập phiếu xuất", 800, 1100)
    y, x = 30, 260
    nodes = []
    labels = [
        ("Bắt đầu", S_ROUNDED, 140, 40),
        ("NV lập phiếu xuất kho", S_PROCESS, 260, 44),
        ("Nhập kho, ngày, lý do/ghi chú", S_PROCESS, 260, 44),
        ("Thêm chi tiết hàng xuất", S_PROCESS, 260, 44),
        ("Tồn kho đủ?", S_DECISION, 140, 70),
        ("Gửi phiếu xuất để duyệt", S_PROCESS, 260, 44),
        ("Quản lý duyệt?", S_DECISION, 140, 70),
        ("Giảm tồn kho", S_PROCESS, 260, 44),
        ("In phiếu xuất", S_PROCESS, 260, 44),
        ("Kết thúc", S_ROUNDED, 140, 40),
    ]
    for text, style, w, h in labels:
        n = d.node(text, x + (260 - w) / 2, y, w, h, style)
        if nodes:
            lab = "Có" if ("đủ" in labels[len(nodes)-1][0] or "duyệt" in labels[len(nodes)-1][0]) and ("Gửi" in text or "Giảm" in text) else ""
            d.edge(nodes[-1], n, lab)
        nodes.append(n)
        y += h + 28
    err1 = d.node("Báo lỗi tồn không đủ", 560, 280, 190, 44, S_PROCESS)
    err2 = d.node("Từ chối, trả NV", 560, 520, 180, 44, S_PROCESS)
    d.edge(nodes[4], err1, "Không")
    d.edge(err1, nodes[3])
    d.edge(nodes[6], err2, "Không")
    d.edge(err2, nodes[1])
    d.save("2.2_activity_xuatkho.drawio")


def gen_activity_kiemke():
    d = D("Activity UC33 Lập phiếu kiểm kê", 700, 900)
    y = 30
    nodes = []
    labels = [
        ("Bắt đầu", S_ROUNDED),
        ("Tạo phiếu kiểm kê theo kho", S_PROCESS),
        ("Hệ thống nạp SL theo sổ (TonKho)", S_PROCESS),
        ("NV nhập SL thực tế", S_PROCESS),
        ("Tính chênh lệch", S_PROCESS),
        ("Gửi duyệt", S_PROCESS),
        ("QL duyệt điều chỉnh?", S_DECISION),
        ("Cập nhật TonKho = thực tế", S_PROCESS),
        ("Kết thúc", S_ROUNDED),
    ]
    for text, style in labels:
        w, h = (140, 70) if style == S_DECISION else (280, 44)
        if style == S_ROUNDED:
            w, h = 140, 40
        n = d.node(text, 210, y, w, h, style)
        if nodes:
            d.edge(nodes[-1], n, "Có" if "Cập nhật" in text else "")
        nodes.append(n)
        y += h + 30
    err = d.node("Yêu cầu kiểm lại", 520, 520, 170, 44, S_PROCESS)
    d.edge(nodes[6], err, "Không")
    d.edge(err, nodes[3])
    d.save("2.3_activity_kiemke.drawio")


# ───────────────────────── 3.x Use case ─────────────────────────

def gen_uc_tongquat():
    d = D("Use case tổng quát", 1100, 800)
    # system box
    d.node("Hệ thống quản lý kho hàng\n(use case tổng quát — không có KH)", 200, 40, 700, 620, S_SYS)
    # left ovals
    left = [
        (280, 100, "Đăng nhập / Đăng xuất"),
        (280, 190, "Quản lý tài khoản"),
        (280, 280, "Quản lý nhà cung cấp"),
        (280, 370, "Quản lý hàng hóa"),
        (280, 460, "Quản lý kho"),
    ]
    right = [
        (620, 100, "Nhập kho"),
        (620, 190, "Xuất kho"),
        (620, 280, "Kiểm kê"),
        (620, 370, "Báo cáo tồn kho"),
    ]
    lids, rids = [], []
    for x, y, t in left:
        lids.append(d.node(t, x, y, 200, 50, S_UC))
    for x, y, t in right:
        rids.append(d.node(t, x, y, 200, 50, S_UC))
    admin = d.node("Quản trị viên", 40, 220, 70, 90, S_ACTOR)
    qlk = d.node("Quản lý kho", 960, 220, 70, 90, S_ACTOR)
    nvk = d.node("Nhân viên kho", 500, 700, 70, 90, S_ACTOR)
    # QTV only g1 g2
    d.edge(admin, lids[0], style=S_EDGE_NONE)
    d.edge(admin, lids[1], style=S_EDGE_NONE)
    # QL: all except account
    for i in [0, 2, 3, 4]:
        d.edge(qlk, lids[i], style=S_EDGE_NONE)
    for r in rids:
        d.edge(qlk, r, style=S_EDGE_NONE)
    # NV
    for i in [0, 2, 3]:
        d.edge(nvk, lids[i], style=S_EDGE_NONE)
    for r in rids[:3]:
        d.edge(nvk, r, style=S_EDGE_NONE)
    d.save("3.4_usecase_tongquat.drawio")


def gen_uc_account():
    d = D("UC phân rã Tài khoản", 1000, 750)
    d.node("Phân rã: Xác thực & quản lý tài khoản", 150, 30, 700, 620, S_SYS)
    left = [
        (200, 100, "UC03: Thêm tài khoản"),
        (200, 180, "UC04: Sửa tài khoản"),
        (200, 260, "UC05: Xóa tài khoản"),
        (200, 340, "UC06: Tìm kiếm tài khoản"),
        (200, 420, "UC07: Xem danh sách TK"),
    ]
    right = [
        (560, 160, "UC01: Đăng nhập"),
        (560, 260, "UC02: Đăng xuất"),
    ]
    ids = []
    for x, y, t in left + right:
        ids.append(d.node(t, x, y, 220, 48, S_UC))
    admin = d.node("Quản trị viên", 30, 250, 70, 90, S_ACTOR)
    user = d.node("Người dùng", 880, 200, 70, 90, S_ACTOR)
    for i in range(7):
        d.edge(admin, ids[i], style=S_EDGE_NONE)
    d.edge(user, ids[5], style=S_EDGE_NONE)
    d.edge(user, ids[6], style=S_EDGE_NONE)
    d.save("3.5_usecase_taikhoan.drawio")


def gen_uc_ncc():
    d = D("UC phân rã NCC", 900, 700)
    d.node("Phân rã: Quản lý nhà cung cấp", 180, 30, 540, 560, S_SYS)
    items = [
        "UC08: Thêm NCC",
        "UC09: Sửa NCC",
        "UC10: Xóa NCC",
        "UC11: Tìm kiếm NCC",
        "UC12: Xem danh sách NCC",
    ]
    ids = []
    y = 90
    for t in items:
        ids.append(d.node(t, 300, y, 220, 48, S_UC))
        y += 80
    nv = d.node("Nhân viên kho", 40, 250, 70, 90, S_ACTOR)
    ql = d.node("Quản lý kho", 780, 250, 70, 90, S_ACTOR)
    for i in ids:
        d.edge(nv, i, style=S_EDGE_NONE)
        d.edge(ql, i, style=S_EDGE_NONE)
    d.save("3.6_usecase_ncc.drawio")


def gen_uc_hang_kho():
    d = D("UC phân rã Hàng hóa & Kho", 1100, 750)
    d.node("Phân rã: Hàng hóa & Kho", 120, 20, 860, 620, S_SYS)
    d.node("Hàng hóa", 220, 60, 100, 24, S_NOTE)
    d.node("Kho", 640, 60, 60, 24, S_NOTE)
    h = ["UC13: Thêm hàng", "UC14: Sửa hàng", "UC15: Xóa hàng", "UC16: Tìm hàng", "UC17: Xem DS hàng"]
    k = ["UC18: Thêm kho", "UC19: Sửa kho", "UC20: Xóa kho", "UC21: Tìm kho", "UC22: Xem DS kho"]
    hids, kids = [], []
    y = 100
    for t in h:
        hids.append(d.node(t, 180, y, 200, 46, S_UC))
        y += 80
    y = 100
    for t in k:
        kids.append(d.node(t, 580, y, 200, 46, S_UC))
        y += 80
    nv = d.node("Nhân viên kho", 30, 280, 70, 90, S_ACTOR)
    ql = d.node("Quản lý kho", 980, 280, 70, 90, S_ACTOR)
    for i in hids:
        d.edge(nv, i, style=S_EDGE_NONE)
        d.edge(ql, i, style=S_EDGE_NONE)
    for i in kids:
        d.edge(ql, i, style=S_EDGE_NONE)
    d.save("3.7_usecase_hang_kho.drawio")


def gen_uc_phieu():
    d = D("UC phân rã Phiếu nhập/xuất", 1200, 850)
    d.node("Phân rã: Phiếu nhập / xuất / kiểm kê / báo cáo", 100, 15, 1000, 720, S_SYS)
    d.node("Phiếu nhập", 220, 50, 100, 22, S_NOTE)
    d.node("Phiếu xuất", 720, 50, 100, 22, S_NOTE)
    pn = ["UC23: Lập PN", "UC24: Sửa PN", "UC25: Xóa PN", "UC26: Tìm PN", "UC27: Xem DS PN"]
    px = ["UC28: Lập PX", "UC29: Sửa PX", "UC30: Xóa PX", "UC31: Tìm PX", "UC32: Xem DS PX"]
    pids, xids = [], []
    y = 90
    for t in pn:
        pids.append(d.node(t, 180, y, 190, 44, S_UC))
        y += 70
    y = 90
    for t in px:
        xids.append(d.node(t, 680, y, 190, 44, S_UC))
        y += 70
    kk = d.node("UC33: Lập kiểm kê", 180, 460, 190, 44, S_UC)
    bc = d.node("UC34: Xem BC tồn", 680, 460, 190, 44, S_UC)
    nv = d.node("NV kho", 30, 250, 70, 90, S_ACTOR)
    ql = d.node("QL kho", 1080, 250, 70, 90, S_ACTOR)
    for i in pids + xids + [kk]:
        d.edge(nv, i, style=S_EDGE_NONE)
        d.edge(ql, i, style=S_EDGE_NONE)
    d.edge(ql, bc, style=S_EDGE_NONE)
    d.save("3.8_usecase_phieu_bc.drawio")


# ───────────────────────── 4.x Class ─────────────────────────

def gen_class_master():
    d = D("Class Master Data", 1100, 800)
    d.node("Sơ đồ lớp danh mục (Master Data)", 350, 10, 350, 30, S_NOTE)
    c1 = d.class_box("NhomHangHoa", ["+ MaNhomHang", "+ TenNhomHang", "+ MoTa"], 40, 60, 170)
    c2 = d.class_box("HangHoa", ["+ MaHangHoa", "+ TenHangHoa", "+ MaNhom", "+ MaDVT", "+ GiaNhap", "+ GiaXuat", "+ TrangThai", "+ CapNhatThongTin()"], 280, 60, 200)
    c3 = d.class_box("DonViTinh", ["+ MaDonViTinh", "+ TenDonViTinh"], 560, 60, 170)
    c4 = d.class_box("Kho", ["+ MaKho", "+ TenKho", "+ DiaChi", "+ NguoiPhuTrach", "+ TrangThai"], 40, 320, 180)
    c5 = d.class_box("NguoiDung", ["+ MaNguoiDung", "+ TenDangNhap", "+ MatKhau", "+ HoTen", "+ VaiTro", "+ TrangThai", "+ DangNhap()", "+ DangXuat()"], 280, 320, 200)
    c6 = d.class_box("NhaCungCap", ["+ MaNCC", "+ Ten", "+ DiaChi", "+ SDT", "+ Email", "+ NguoiLienHe"], 560, 320, 190)
    c7 = d.class_box("TonKho", ["+ MaKho", "+ MaHangHoa", "+ SoLuongTon", "+ NgayCapNhat", "+ CapNhatTonKho()"], 800, 200, 190)
    d.edge(c1, c2, "1..*", S_EDGE_OPEN)
    d.edge(c3, c2, "1..*", S_EDGE_OPEN)
    d.edge(c2, c7, "1..*", S_EDGE_OPEN)
    d.edge(c4, c7, "1..*", S_EDGE_OPEN)
    d.save("4.1_class_master.drawio")


def gen_class_nhapxuat():
    d = D("Class Nhập Xuất", 1000, 700)
    pn = d.class_box("PhieuNhapKho", ["+ MaPhieuNhap", "+ MaNCC", "+ MaKho", "+ MaNguoiDung", "+ NgayNhap", "+ TongTien", "+ TrangThai", "+ LapPhieuNhap()", "+ DuyetPhieuNhap()"], 40, 40, 210)
    ctn = d.class_box("ChiTietPhieuNhap", ["+ MaChiTiet", "+ MaPhieuNhap", "+ MaHangHoa", "+ SoLuong", "+ DonGia", "+ ThanhTien"], 400, 40, 200)
    px = d.class_box("PhieuXuatKho", ["+ MaPhieuXuat", "+ MaKho", "+ MaNguoiDung", "+ NgayXuat", "+ LyDoXuat", "+ GhiChu", "+ TongTien", "+ TrangThai", "+ LapPhieuXuat()", "+ DuyetPhieuXuat()"], 40, 320, 210)
    ctx = d.class_box("ChiTietPhieuXuat", ["+ MaChiTiet", "+ MaPhieuXuat", "+ MaHangHoa", "+ SoLuong", "+ DonGia", "+ ThanhTien"], 400, 320, 200)
    d.edge(pn, ctn, "1..*", S_EDGE_OPEN)
    d.edge(px, ctx, "1..*", S_EDGE_OPEN)
    d.node("Không có lớp KhachHang", 700, 360, 200, 40, S_NOTE)
    d.save("4.2_class_nhapxuat.drawio")


def gen_class_kiemke():
    d = D("Class Kiểm kê & Log", 900, 550)
    pk = d.class_box("PhieuKiemKe", ["+ MaPhieuKiemKe", "+ MaKho", "+ MaNguoiDung", "+ NgayKiemKe", "+ TrangThai"], 40, 40, 200)
    ct = d.class_box("ChiTietKiemKe", ["+ MaChiTiet", "+ MaPhieuKiemKe", "+ MaHangHoa", "+ SLThucTe", "+ SLSoSach", "+ ChenhLech"], 380, 40, 210)
    log = d.class_box("LichSuThaoTac", ["+ MaLog", "+ MaNguoiDung", "+ HanhDong", "+ ThoiGian", "+ DoiTuong", "+ MoTa"], 200, 300, 220)
    d.edge(pk, ct, "1..*", S_EDGE_OPEN)
    d.save("4.3_class_kiemke.drawio")


def gen_class_uc_hang():
    d = D("Class UC13 Thêm hàng hóa", 1000, 600)
    hh = d.class_box("HangHoa", ["+ MaHangHoa", "+ TenHangHoa", "...", "+ ThemHangHoa()", "+ TimKiem()"], 350, 200, 180)
    nh = d.class_box("NhomHangHoa", ["+ MaNhom", "+ TenNhom"], 40, 80, 160)
    dvt = d.class_box("DonViTinh", ["+ MaDVT", "+ TenDVT"], 40, 280, 160)
    tk = d.class_box("TonKho", ["+ MaKho", "+ MaHang", "+ SoLuongTon", "+ KhoiTaoTon()"], 700, 200, 180)
    nd = d.class_box("NguoiDung", ["+ MaNguoiDung", "+ VaiTro"], 350, 40, 160)
    d.edge(nh, hh, "1", S_EDGE_OPEN)
    d.edge(dvt, hh, "1", S_EDGE_OPEN)
    d.edge(hh, tk, "1..*", S_EDGE_OPEN)
    d.edge(nd, hh, "", S_EDGE_OPEN)
    d.save("4.4_class_uc13_themhang.drawio")


def gen_class_uc_pn():
    d = D("Class UC23 Lập phiếu nhập", 1100, 650)
    pn = d.class_box("PhieuNhapKho", ["+ LapPhieuNhap()", "+ DuyetPhieuNhap()"], 400, 200, 180)
    ct = d.class_box("ChiTietPhieuNhap", ["+ SoLuong", "+ DonGia"], 700, 200, 170)
    ncc = d.class_box("NhaCungCap", ["+ MaNCC", "+ Ten"], 40, 80, 160)
    kho = d.class_box("Kho", ["+ MaKho"], 40, 280, 140)
    hh = d.class_box("HangHoa", ["+ MaHang"], 700, 40, 140)
    ton = d.class_box("TonKho", ["+ TangTon()"], 700, 400, 150)
    nd = d.class_box("NguoiDung", ["+ VaiTro"], 400, 40, 150)
    d.edge(pn, ct, "1..*", S_EDGE_OPEN)
    d.edge(pn, ncc, "n..1", S_EDGE_OPEN)
    d.edge(pn, kho, "n..1", S_EDGE_OPEN)
    d.edge(ct, hh, "n..1", S_EDGE_OPEN)
    d.edge(pn, nd, "", S_EDGE_OPEN)
    d.edge(kho, ton, "", S_EDGE_OPEN)
    d.edge(hh, ton, "", S_EDGE_OPEN)
    d.save("4.5_class_uc23_phieunhap.drawio")


def gen_class_uc_px():
    d = D("Class UC28 Lập phiếu xuất", 1100, 650)
    px = d.class_box("PhieuXuatKho", ["+ LyDoXuat", "+ GhiChu", "+ LapPhieuXuat()", "+ DuyetPhieuXuat()"], 400, 200, 200)
    ct = d.class_box("ChiTietPhieuXuat", ["+ SoLuong", "+ DonGia"], 720, 200, 170)
    kho = d.class_box("Kho", ["+ MaKho"], 40, 200, 140)
    hh = d.class_box("HangHoa", ["+ MaHang"], 720, 40, 140)
    ton = d.class_box("TonKho", ["+ KiemTraDu()", "+ GiamTon()"], 720, 400, 160)
    nd = d.class_box("NguoiDung", ["+ VaiTro"], 400, 40, 150)
    d.node("Không gắn KhachHang", 40, 40, 180, 30, S_NOTE)
    d.edge(px, ct, "1..*", S_EDGE_OPEN)
    d.edge(px, kho, "n..1", S_EDGE_OPEN)
    d.edge(ct, hh, "n..1", S_EDGE_OPEN)
    d.edge(px, nd, "", S_EDGE_OPEN)
    d.edge(kho, ton, "", S_EDGE_OPEN)
    d.edge(hh, ton, "", S_EDGE_OPEN)
    d.save("4.6_class_uc28_phieuxuat.drawio")


def gen_class_uc_tk():
    d = D("Class UC03-07 Tài khoản", 700, 450)
    nd = d.class_box("NguoiDung", ["+ TenDangNhap", "+ MatKhau", "+ VaiTro", "+ ThemTaiKhoan()", "+ SuaTaiKhoan()", "+ Xoa/Khoa()", "+ TimKiem()", "+ LayDanhSach()", "+ DangNhap()", "+ DangXuat()"], 80, 80, 240)
    log = d.class_box("LichSuThaoTac", ["+ GhiLog()"], 420, 120, 180)
    d.edge(nd, log, "1..*", S_EDGE_OPEN)
    d.save("6.2_class_uc03_taikhoan.drawio")


# ───────────────────────── 5.x Sequence / State ─────────────────────────

def gen_sequence(name, filename, actors, messages):
    """actors: list of names; messages: list of (from_idx, to_idx, text)"""
    d = D(name, 200 + 160 * len(actors), 200 + 50 * len(messages))
    heads = []
    for i, a in enumerate(actors):
        x = 80 + i * 160
        heads.append(d.node(a, x, 40, 120, 50, S_RECT))
        # lifeline line as thin tall rect
        d.node("", x + 55, 90, 2, 40 + 45 * len(messages), "endArrow=none;html=1;strokeColor=#999999;fillColor=#999999;")
    y = 120
    for fr, to, text in messages:
        d.edge(heads[fr], heads[to], text, S_MSG)
        # fake spacing by notes
        y += 40
    # Better: place message labels as text along
    d.save(filename)


def gen_sequences():
    # Simpler sequence representation with vertical steps
    def seq(name, fn, cols, steps):
        d = D(name, 120 + 150 * len(cols), 100 + 55 * len(steps))
        heads = []
        for i, c in enumerate(cols):
            heads.append(d.node(c, 40 + i * 150, 30, 130, 44, S_RECT))
        y = 100
        for i, (fr, to, msg) in enumerate(steps):
            # message bar between columns
            x1 = 40 + fr * 150 + 65
            x2 = 40 + to * 150 + 65
            left, right = min(x1, x2), max(x1, x2)
            mid = d.node(msg, left, y, max(right - left, 120), 28, "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFDE7;strokeColor=#000000;fontSize=10;align=center;")
            y += 48
        d.save(fn)

    seq(
        "Sequence UC01 Đăng nhập",
        "5.7_sequence_uc01.drawio",
        ["Người dùng", "Giao diện", "Hệ thống", "CSDL"],
        [
            (0, 1, "1. Mở trang đăng nhập"),
            (0, 1, "2. Nhập tên / mật khẩu"),
            (1, 2, "3. Gửi thông tin"),
            (2, 3, "4. Kiểm tra tài khoản"),
            (2, 1, "5. Tạo phiên / báo lỗi"),
            (1, 0, "6. Trang chủ hoặc lỗi"),
        ],
    )
    seq(
        "Sequence UC13 Thêm hàng",
        "5.1_sequence_uc13_themhang.drawio",
        ["NV kho", "Giao diện HH", "Hệ thống", "CSDL"],
        [
            (0, 1, "1. Chọn thêm hàng"),
            (0, 1, "2. Nhập thông tin"),
            (1, 2, "3. Gửi dữ liệu"),
            (2, 3, "4. Lưu HangHoa"),
            (2, 3, "5. KhoiTaoTon = 0"),
            (2, 1, "6. Thông báo thành công"),
        ],
    )
    seq(
        "Sequence UC16 Tìm hàng",
        "5.2_sequence_uc16_timhang.drawio",
        ["User", "Giao diện", "Hệ thống", "CSDL"],
        [
            (0, 1, "1. Nhập điều kiện tìm"),
            (1, 2, "2. Gửi truy vấn"),
            (2, 3, "3. Query HangHoa + TonKho"),
            (2, 1, "4. Trả danh sách"),
            (1, 0, "5. Hiển thị kết quả"),
        ],
    )
    seq(
        "Sequence UC23 Lập phiếu nhập",
        "5.3_sequence_uc23_phieunhap.drawio",
        ["NV", "QL", "Hệ thống", "CSDL"],
        [
            (0, 2, "1. Lập phiếu + chi tiết"),
            (2, 3, "2. Lưu Chờ duyệt"),
            (1, 2, "3. Duyệt / Từ chối"),
            (2, 3, "4. Nếu duyệt: TangTon"),
            (2, 3, "5. Ghi log"),
        ],
    )
    seq(
        "Sequence UC28 Lập phiếu xuất",
        "5.4_sequence_uc28_phieuxuat.drawio",
        ["NV", "QL", "Hệ thống", "CSDL"],
        [
            (0, 2, "1. Lập phiếu xuất"),
            (2, 3, "2. KiemTraDu tồn"),
            (2, 3, "3. Lưu Chờ duyệt"),
            (1, 2, "4. Duyệt"),
            (2, 3, "5. GiamTon + log"),
        ],
    )


def gen_states():
    d = D("State phiếu nhập", 1100, 500)
    s1 = d.node("Mới tạo", 40, 120, 140, 60, S_STATE)
    s2 = d.node("Chờ duyệt", 260, 120, 140, 60, S_STATE)
    s3 = d.node("Đã duyệt", 480, 120, 140, 60, S_STATE)
    s4 = d.node("Đã nhập kho", 700, 120, 150, 60, S_STATE)
    s5 = d.node("Hủy / Từ chối", 480, 300, 160, 60, S_STATE)
    d.edge(s1, s2, "Gửi duyệt")
    d.edge(s2, s3, "QL duyệt")
    d.edge(s3, s4, "Cập nhật tồn")
    d.edge(s2, s5, "Từ chối")
    d.edge(s3, s5, "Hủy phiếu")
    d.save("5.5_state_phieu_nhap.drawio")

    d2 = D("State phiếu xuất", 1100, 500)
    a = d2.node("Mới tạo", 40, 120, 140, 60, S_STATE)
    b = d2.node("Chờ duyệt", 260, 120, 140, 60, S_STATE)
    c = d2.node("Đã duyệt", 480, 120, 140, 60, S_STATE)
    e = d2.node("Đã xuất kho", 700, 120, 150, 60, S_STATE)
    f = d2.node("Hủy / Từ chối", 480, 300, 160, 60, S_STATE)
    d2.edge(a, b, "Gửi duyệt")
    d2.edge(b, c, "QL duyệt")
    d2.edge(c, e, "Giảm tồn")
    d2.edge(b, f, "Từ chối")
    d2.edge(c, f, "Hủy phiếu")
    d2.save("5.6_state_phieu_xuat.drawio")


def gen_component():
    d = D("Component kiến trúc", 900, 750)
    layers = [
        (300, 40, "Giao diện người dùng\n(UI / Web Browser)"),
        (300, 140, "Controller Layer\n(API / Routing)"),
        (300, 240, "Service Layer\n(Business Logic)"),
        (300, 340, "Repository Layer\n(Data Access)"),
    ]
    ids = []
    for x, y, t in layers:
        ids.append(d.node(t, x, y, 240, 60, S_COMPONENT if False else S_RECT))
    db = d.node("Cơ sở dữ liệu", 350, 460, 140, 80, S_CYL)
    for i in range(len(ids) - 1):
        labs = ["HTTP/HTTPS", "Gọi dịch vụ", "Truy vấn"]
        d.edge(ids[i], ids[i + 1], labs[i] if i < len(labs) else "")
    d.edge(ids[-1], db, "SQL")
    auth = d.node("Authentication\nService", 620, 140, 160, 55, S_RECT)
    inv = d.node("Inventory Service\n(Tồn kho)", 620, 280, 160, 55, S_RECT)
    ntf = d.node("Notification\nService", 620, 360, 160, 55, S_RECT)
    d.edge(ids[1], auth, "Xác thực")
    d.edge(ids[2], inv, "Tính tồn")
    d.edge(ids[2], ntf, "Cảnh báo")
    d.save("6.1_component.drawio")


def gen_ui_nav():
    d = D("UI Navigation", 1100, 600)
    login = d.node("Đăng nhập\nUC01", 460, 30, 120, 50, S_ROUNDED)
    home = d.node("Trang chủ", 460, 120, 120, 45, S_RECT)
    d.edge(login, home)
    menus = [
        (40, 240, "Hàng hóa\nUC13–17"),
        (180, 240, "NCC\nUC08–12"),
        (320, 240, "Kho\nUC18–22"),
        (460, 240, "Tài khoản\nUC03–07"),
        (600, 240, "Báo cáo\nUC34"),
        (180, 380, "Phiếu nhập\nUC23–27"),
        (360, 380, "Phiếu xuất\nUC28–32"),
        (540, 380, "Kiểm kê\nUC33"),
    ]
    for x, y, t in menus:
        m = d.node(t, x, y, 120, 55, S_RECT)
        d.edge(home, m)
    d.node("Menu theo vai trò: QTV chủ yếu Tài khoản", 300, 500, 380, 30, S_NOTE)
    d.save("7.3_ui_navigation.drawio")


def gen_readme():
    text = """# Draw.io diagrams — Báo cáo Quản lý kho hàng

Mở file bằng:
- https://app.diagrams.net (File → Open from → Device)
- VS Code extension **Draw.io Integration**
- Desktop draw.io

## Danh sách file

| File | Nội dung |
|------|----------|
| 2.1_activity_nhapkho.drawio | Activity lập phiếu nhập (UC23) |
| 2.2_activity_xuatkho.drawio | Activity lập phiếu xuất (UC28) |
| 2.3_activity_kiemke.drawio | Activity kiểm kê (UC33) |
| 3.4_usecase_tongquat.drawio | Use case tổng quát (QTV chỉ TK) |
| 3.5_usecase_taikhoan.drawio | UC01–07 Xác thực + tài khoản |
| 3.6_usecase_ncc.drawio | UC08–12 NCC |
| 3.7_usecase_hang_kho.drawio | UC13–22 Hàng + Kho |
| 3.8_usecase_phieu_bc.drawio | UC23–34 Phiếu + KK + BC |
| 4.1_class_master.drawio | Class danh mục |
| 4.2_class_nhapxuat.drawio | Class nhập/xuất |
| 4.3_class_kiemke.drawio | Class kiểm kê + log |
| 4.4_class_uc13_themhang.drawio | Class cắt lát thêm hàng |
| 4.5_class_uc23_phieunhap.drawio | Class cắt lát phiếu nhập |
| 4.6_class_uc28_phieuxuat.drawio | Class cắt lát phiếu xuất |
| 5.1–5.4, 5.7 sequence_*.drawio | Sequence diagrams |
| 5.5–5.6 state_*.drawio | State phiếu nhập/xuất |
| 6.1_component.drawio | Component kiến trúc |
| 6.2_class_uc03_taikhoan.drawio | Class tài khoản |
| 7.3_ui_navigation.drawio | Điều hướng UI |

## MCP Draw.io (khuyến nghị cho lần sau)

Hiện session **chưa** kết nối MCP Draw.io. Có thể cài:

### 1) Official `@drawio/mcp` (mở diagram trên draw.io)

Trong `~/.grok/config.toml`:

```toml
[mcp_servers.drawio]
command = "npx"
args = ["-y", "@drawio/mcp"]
enabled = true
startup_timeout_sec = 60
```

Hoặc HTTP hosted (MCP Apps): `https://mcp.draw.io/mcp` — xem https://www.draw.io/docs/manual/generate/drawio-mcp-server/

### 2) Community `drawio-mcp-server` (lgazo) — control editor trực tiếp

```toml
[mcp_servers.drawio-lgazo]
command = "npx"
args = ["-y", "drawio-mcp-server"]
enabled = true
startup_timeout_sec = 90
```

Repo: https://github.com/lgazo/drawio-mcp-server

Sau khi thêm, **restart Grok** rồi nhờ gen/sửa sơ đồ qua MCP sẽ mượt hơn (preview, edit live).

## Gen lại

```bash
python gen_all_drawio.py
```
"""
    (OUT / "README.md").write_text(text, encoding="utf-8")
    print("wrote README.md")


def main():
    gen_activity_nhap()
    gen_activity_xuat()
    gen_activity_kiemke()
    gen_uc_tongquat()
    gen_uc_account()
    gen_uc_ncc()
    gen_uc_hang_kho()
    gen_uc_phieu()
    gen_class_master()
    gen_class_nhapxuat()
    gen_class_kiemke()
    gen_class_uc_hang()
    gen_class_uc_pn()
    gen_class_uc_px()
    gen_class_uc_tk()
    gen_sequences()
    gen_states()
    gen_component()
    gen_ui_nav()
    gen_readme()
    files = sorted(OUT.glob("*.drawio"))
    print(f"\nTotal: {len(files)} drawio files in {OUT}")


if __name__ == "__main__":
    main()
