"""Build CNTT20261_N01 MS Project file from WBS + budget."""
from __future__ import annotations

import os
import time
from datetime import datetime
from pathlib import Path

import pythoncom
import win32com.client

OUT = Path(
    r"C:\Dev\Learning\VIII.HUST\Quản trị dự án\Nhóm 1\ke-hoach-du-an.mpp"
)
START = datetime(2026, 9, 1, 8, 0)
DEADLINE = datetime(2027, 3, 31, 17, 0)
PJ_DO_NOT_SAVE = 0
PJ_SNET = 4
PJ_FNLT = 7
PJ_FIXED_DURATION = 1
PJ_COST_RESOURCE = 2
PJ_ACCRUE_START = 1

# Daily rates from CongLaoDong (luong co so 2.530.000 * he so)
RATES = {
    "Bùi Tuấn Anh": 1_897_500,
    "Bùi Quốc Luýt": 1_138_500,
    "Vũ Quang Minh": 1_138_500,
    "Bạch Minh Quang": 1_138_500,
    "Phạm Đoàn Bảo Thiên": 1_138_500,
}
ROLES = {
    "Bùi Tuấn Anh": "Chủ nhiệm / Giám đốc dự án",
    "Bùi Quốc Luýt": "Trưởng nhóm kỹ thuật / Back-end",
    "Vũ Quang Minh": "Thành viên chính / Back-end",
    "Bạch Minh Quang": "Thành viên chính / UI-UX, Front-end",
    "Phạm Đoàn Bảo Thiên": "Thành viên chính / CSDL, Kiểm thử",
}
INITIALS = {
    "Bùi Tuấn Anh": "BTA",
    "Bùi Quốc Luýt": "BQL",
    "Vũ Quang Minh": "VQM",
    "Bạch Minh Quang": "BMQ",
    "Phạm Đoàn Bảo Thiên": "PDBT",
}

# (code, name, start, tbvt, chikhac, notes)
PHASES = [
    (
        "A",
        "A. Khảo sát & yêu cầu",
        datetime(2026, 9, 1, 8, 0),
        4_000_000,
        5_500_000,
        "WBS: 01/09/2026–25/09/2026. TBVT 4.000.000 + chi khác 5.500.000.",
    ),
    (
        "B",
        "B. Phân tích & thiết kế hệ thống",
        datetime(2026, 9, 26, 8, 0),
        15_000_000,
        4_500_000,
        "WBS: 26/09/2026–20/11/2026. TBVT 15.000.000 + chi khác 4.500.000.",
    ),
    (
        "C",
        "C. Thiết kế CSDL & giao diện",
        datetime(2026, 11, 21, 8, 0),
        9_100_000,
        8_000_000,
        "WBS: 21/11/2026–25/12/2026. TBVT 9.100.000 + chi khác 8.000.000.",
    ),
    (
        "D",
        "D. Xây dựng chương trình",
        datetime(2026, 12, 26, 8, 0),
        21_000_000,
        11_000_000,
        "WBS: 26/12/2026–15/02/2027. TBVT 21.000.000 + chi khác 11.000.000.",
    ),
    (
        "E",
        "E. Tích hợp & kiểm thử",
        datetime(2027, 2, 16, 8, 0),
        11_600_000,
        11_000_000,
        "WBS: 16/02/2027–15/03/2027. TBVT 11.600.000 + chi khác 11.000.000.",
    ),
    (
        "F",
        "F. Triển khai & bàn giao",
        datetime(2027, 3, 16, 8, 0),
        13_100_000,
        9_000_000,
        "WBS: 16/03/2027–31/03/2027. TBVT 13.100.000 + chi khác 9.000.000.",
    ),
]

# stt, name, est_days, preds, people, deliverable, notes
TASKS = [
    (1, "Khảo sát quy trình nhập hàng và đổi trả", 3.4833, [], ["Bùi Tuấn Anh"],
     "Báo cáo khảo sát & đặc tả yêu cầu",
     "Khảo sát cách kho nhận hàng từ NCC, kiểm tra mẫu mã/màu/size, đối chiếu hóa đơn; tiếp nhận và phân loại hàng khách trả lại."),
    (2, "Khảo sát quy trình xuất hàng, chuyển kho, hủy hàng", 3.4833, [], ["Bùi Quốc Luýt"],
     "Báo cáo khảo sát & đặc tả yêu cầu",
     "Khảo sát yêu cầu xuất từ bán hàng, soạn hàng, chuyển kho tổng–cửa hàng, xử lý hàng lỗi hỏng."),
    (3, "Khảo sát kiểm kê và thu thập biểu mẫu", 4.4000, [], ["Phạm Đoàn Bảo Thiên"],
     "Báo cáo khảo sát & đặc tả yêu cầu",
     "Khảo sát kiểm kê, đối chiếu sổ sách; thu thập 13 biểu mẫu (7 phiếu chứng từ, 6 mẫu báo cáo)."),
    (4, "Khảo sát thông tin hàng hóa và biến thể", 2.3833, [], ["Bạch Minh Quang"],
     "Báo cáo khảo sát & đặc tả yêu cầu",
     "Khảo sát ghi nhận sản phẩm, loại, màu, size, giá nhập/bán, vị trí; cấp quản lý sản phẩm hay biến thể."),
    (5, "Tổng hợp hiện trạng", 3.3000, [1, 2, 3, 4], ["Bùi Tuấn Anh"],
     "Báo cáo khảo sát & đặc tả yêu cầu",
     "Tổng hợp khảo sát, mô tả 4 quy trình cốt lõi, hạn chế sổ sách/Excel, đối chiếu nhu cầu hệ thống."),
    (6, "Xác định mục tiêu, phạm vi và quy tắc nghiệp vụ", 3.3000, [5], ["Bùi Tuấn Anh"],
     "Báo cáo khảo sát & đặc tả yêu cầu",
     "Mục tiêu đo được, in/out-scope, tác nhân, quy tắc QT-01 đến QT-06."),
    (7, "Phân tích yêu cầu chức năng và phi chức năng", 4.5833, [6], ["Bùi Quốc Luýt"],
     "Báo cáo khảo sát & đặc tả yêu cầu",
     "19 FR và 11 NFR kèm tiêu chí đo hiệu năng, toàn vẹn dữ liệu, bảo mật."),
    (8, "Xác nhận/chỉnh sửa yêu cầu", 2.2000, [7], ["Bùi Tuấn Anh"],
     "Báo cáo khảo sát & đặc tả yêu cầu",
     "Trao đổi với quản lý kho và bộ phận bán hàng, chốt đặc tả yêu cầu."),
    (9, "Xác định tác nhân và ma trận phân quyền", 2.2000, [8], ["Bùi Tuấn Anh"],
     "Báo cáo phân tích thiết kế (UML)",
     "Tác nhân Người dùng, Quản lý, NV kho, NV bán hàng; ma trận vai trò–use case (RBAC)."),
    (10, "Xây dựng biểu đồ use case", 3.3000, [9], ["Bùi Tuấn Anh"],
     "Báo cáo phân tích thiết kế (UML)",
     "Use case tổng quát và 4 gói: Quản trị, Danh mục, Nghiệp vụ kho, Tồn kho & báo cáo."),
    (11, "Đặc tả use case", 6.6000, [10], ["Phạm Đoàn Bảo Thiên"],
     "Báo cáo phân tích thiết kế (UML)",
     "19 use case; chi tiết Nhập kho, Xuất kho, Duyệt điều chỉnh tồn, Đổi trả."),
    (12, "Mô hình lĩnh vực và biểu đồ lớp phân tích", 5.5000, [11], ["Bùi Tuấn Anh"],
     "Báo cáo phân tích thiết kế (UML)",
     "Mô hình lĩnh vực (sản phẩm, biến thể, kho, tồn, phiếu, thẻ kho) và lớp phân tích BCE."),
    (13, "Thiết kế biểu đồ tuần tự", 5.5000, [12], ["Vũ Quang Minh"],
     "Báo cáo phân tích thiết kế (UML)",
     "4 sequence: Nhập kho, Xuất kho, Duyệt điều chỉnh tồn, Xử lý đổi trả."),
    (14, "Thiết kế biểu đồ hoạt động và trạng thái", 4.5833, [11], ["Bạch Minh Quang"],
     "Báo cáo phân tích thiết kế (UML)",
     "4 activity (nghiệp vụ, xuất kho, kiểm kê, đổi trả) và 2 state (PhieuKho, PhieuKiemKe)."),
    (15, "Thiết kế kiến trúc hệ thống", 4.5833, [12], ["Bùi Quốc Luýt"],
     "Báo cáo phân tích thiết kế (UML)",
     "Web 3 tầng React–Spring Boot–PostgreSQL, 6 hệ thống con, gói BCE."),
    (16, "Thiết kế biểu đồ thành phần và triển khai", 3.3000, [15], ["Vũ Quang Minh"],
     "Báo cáo phân tích thiết kế (UML)",
     "Thành phần phần mềm, REST API; máy chủ app, CSDL, sao lưu, máy tính bảng tại kho."),
    (17, "Thiết kế lớp chi tiết", 5.5000, [13, 15], ["Bùi Quốc Luýt"],
     "Báo cáo phân tích thiết kế (UML)",
     "Kiểu dữ liệu, tầm vực, phương thức: chứng từ kho, tồn/kiểm kê, danh mục, quản trị."),
    (18, "Thiết kế lược đồ CSDL", 4.5833, [17], ["Phạm Đoàn Bảo Thiên"],
     "Lược đồ CSDL & từ điển dữ liệu",
     "Ánh xạ 15 bảng, PK/FK, quan hệ sản phẩm–biến thể–kho–tồn–phiếu–thẻ kho."),
    (19, "Xây dựng từ điển dữ liệu, ràng buộc và chỉ mục", 4.2167, [18], ["Phạm Đoàn Bảo Thiên"],
     "Lược đồ CSDL & từ điển dữ liệu",
     "Cột chi tiết; CHECK tồn ≥ 0; UNIQUE (kho, biến thể); chỉ mục thẻ kho (biến thể, kho, thời gian)."),
    (20, "Tạo script CSDL PostgreSQL và dữ liệu mẫu", 3.4833, [19], ["Vũ Quang Minh"],
     "Lược đồ CSDL & từ điển dữ liệu",
     "Migration PostgreSQL 16 và dữ liệu mẫu nhiều màu/size, nhiều kho."),
    (21, "Thiết kế luồng màn hình và bố cục chung", 3.3000, [17], ["Bạch Minh Quang"],
     "Thiết kế UI/UX hệ thống",
     "10 màn hình, menu theo quyền, ô tìm SKU quét mã vạch, tablet 10 inch."),
    (22, "Thiết kế giao diện đăng nhập và tổng quan", 2.2000, [21], ["Bạch Minh Quang"],
     "Thiết kế UI/UX hệ thống",
     "MH-01 Đăng nhập, MH-02 Tổng quan (cảnh báo hết/sắp hết, phiếu chờ)."),
    (23, "Thiết kế giao diện sản phẩm và biến thể", 3.3000, [21], ["Bạch Minh Quang"],
     "Thiết kế UI/UX hệ thống",
     "MH-03 mẫu sản phẩm, ma trận màu × size, giá nhập/bán, tồn tối thiểu."),
    (24, "Thiết kế giao diện phiếu nhập, xuất, đổi trả", 4.5833, [21], ["Bạch Minh Quang"],
     "Thiết kế UI/UX hệ thống",
     "MH-04 nhập, MH-05 xuất, MH-08 đổi trả; quét hàng, tồn khả dụng, thông báo lỗi."),
    (25, "Thiết kế giao diện kiểm kê, tra cứu, báo cáo", 4.2167, [21], ["Bùi Tuấn Anh"],
     "Thiết kế UI/UX hệ thống",
     "MH-06 kiểm kê, MH-07 duyệt, MH-09 tra cứu tồn/thẻ kho, MH-10 báo cáo + Excel."),
    (26, "Dựng khung dự án và môi trường phát triển", 3.3000, [20], ["Bùi Quốc Luýt"],
     "Mã nguồn & module chạy được",
     "Spring Boot 3 + ReactJS/TypeScript, Docker, kho mã, quy ước code, pipeline."),
    (27, "Đăng nhập & quản lý tài khoản", 4.5833, [26], ["Bùi Quốc Luýt"],
     "Mã nguồn & module chạy được",
     "JWT, đổi mật khẩu, khóa sau 5 lần sai; vai trò và kho phụ trách (UC-1.1, UC-1.2)."),
    (28, "Quản lý danh mục loại, màu, size, NCC, kho", 4.5833, [26], ["Vũ Quang Minh"],
     "Mã nguồn & module chạy được",
     "CRUD loại, màu, kích thước, NCC, kho, vị trí (UC-2.3, UC-2.4, UC-2.5)."),
    (29, "Quản lý sản phẩm và biến thể", 5.5000, [28], ["Vũ Quang Minh"],
     "Mã nguồn & module chạy được",
     "Sản phẩm, biến thể màu × size, sinh SKU, tìm/lọc (UC-2.1, UC-2.2)."),
    (30, "Dịch vụ tồn kho và thẻ kho", 5.8667, [29], ["Bùi Quốc Luýt"],
     "Mã nguồn & module chạy được",
     "Tăng/trừ/điều chỉnh có khóa dòng FOR UPDATE; thẻ kho chỉ thêm, dùng chung mọi nghiệp vụ."),
    (31, "Nhập kho", 4.5833, [30], ["Vũ Quang Minh"],
     "Mã nguồn & module chạy được",
     "Phiếu nhập theo NCC, quét SKU, giao dịch nguyên tử cộng tồn + thẻ kho (UC-3.1)."),
    (32, "Yêu cầu xuất kho và xuất kho", 5.6833, [30], ["Bùi Quốc Luýt"],
     "Mã nguồn & module chạy được",
     "Yêu cầu xuất kèm mã đơn; không cho tồn âm (UC-3.2, UC-3.3)."),
    (33, "Chuyển kho", 3.4833, [32], ["Vũ Quang Minh"],
     "Mã nguồn & module chạy được",
     "Hai bước xuất đi và xác nhận nhận tại kho đích (UC-3.4)."),
    (34, "Kiểm kê và duyệt điều chỉnh tồn kho", 5.6833, [30], ["Phạm Đoàn Bảo Thiên"],
     "Mã nguồn & module chạy được",
     "Phiếu kiểm kê, chênh lệch = thực tế − hệ thống; duyệt mới sinh phiếu điều chỉnh (UC-3.5, UC-3.6)."),
    (35, "Xử lý đổi trả hàng", 4.5833, [32], ["Phạm Đoàn Bảo Thiên"],
     "Mã nguồn & module chạy được",
     "Nhập lại hàng tốt, tách hàng lỗi, xuất hàng đổi, tiền chênh lệch (UC-3.7)."),
    (36, "Hủy hàng", 2.2000, [35], ["Phạm Đoàn Bảo Thiên"],
     "Mã nguồn & module chạy được",
     "Phiếu hủy hàng lỗi/hỏng; chỉ trừ tồn sau khi Quản lý duyệt (UC-3.8)."),
    (37, "Tra cứu tồn, cảnh báo tồn thấp, thẻ kho", 4.5833, [30], ["Bạch Minh Quang"],
     "Mã nguồn & module chạy được",
     "Tra cứu theo kho/SP/màu/size/vị trí; cảnh báo hết/sắp hết; lịch sử biến động (UC-4.1, 4.2, 4.4)."),
    (38, "Báo cáo kho và xuất Excel", 5.6833, [31, 32, 34], ["Bùi Tuấn Anh"],
     "Mã nguồn & module chạy được",
     "6 báo cáo: tồn, nhập, xuất, NXT, kiểm kê, tồn lâu; xuất .xlsx Apache POI (UC-4.3)."),
    (39, "Lập trình giao diện web", 8.9833, [25, 27], ["Bạch Minh Quang"],
     "Mã nguồn & module chạy được",
     "10 màn hình ReactJS, menu theo quyền, máy quét mã vạch, REST API."),
    (40, "Tích hợp các module", 4.5833, [39], ["Bùi Quốc Luýt"],
     "Báo cáo kiểm thử",
     "Kết nối UI–dịch vụ; kho/kiểm kê/báo cáo đều đổi tồn qua dịch vụ Tồn kho và thẻ kho."),
    (41, "Kiểm thử đăng nhập, phân quyền, danh mục", 3.3000, [40], ["Bạch Minh Quang"],
     "Báo cáo kiểm thử",
     "Đăng nhập, khóa tài khoản, RBAC; CRUD danh mục, sinh SKU không trùng."),
    (42, "Kiểm thử nhập, xuất, chuyển kho", 4.5833, [40], ["Phạm Đoàn Bảo Thiên"],
     "Báo cáo kiểm thử",
     "Cộng/trừ tồn, thẻ kho; hai phiếu xuất đồng thời không làm tồn âm (NFR-04)."),
    (43, "Kiểm thử kiểm kê, đổi trả, hủy hàng", 3.4833, [40], ["Vũ Quang Minh"],
     "Báo cáo kiểm thử",
     "Chênh lệch, duyệt điều chỉnh, phân loại hàng trả, hủy hàng chỉ sau duyệt."),
    (44, "Kiểm thử tra cứu và báo cáo", 3.3000, [40], ["Bùi Tuấn Anh"],
     "Báo cáo kiểm thử",
     "Tồn cuối = tồn đầu + nhập − xuất ± điều chỉnh; cảnh báo tồn thấp; file Excel."),
    (45, "Kiểm thử hiệu năng và bảo mật", 3.4833, [40], ["Phạm Đoàn Bảo Thiên"],
     "Báo cáo kiểm thử",
     "Tra cứu < 2s / 50.000 biến thể / 100 user; NXT tháng < 10s; HTTPS, hết phiên, bcrypt."),
    (46, "Kiểm thử toàn hệ thống (UAT)", 4.5833, [41, 42, 43, 44, 45], ["Bùi Tuấn Anh"],
     "Báo cáo kiểm thử",
     "User doanh nghiệp chạy nhập–xuất–kiểm kê–báo cáo; ghi nhận lỗi và góp ý."),
    (47, "Sửa lỗi & hoàn thiện", 4.5833, [46],
     ["Bùi Quốc Luýt", "Vũ Quang Minh", "Bạch Minh Quang"],
     "Báo cáo kiểm thử",
     "3 thành viên song song (mỗi người 4,583 manday): sửa lỗi kiểm thử, hoàn thiện trước nghiệm thu."),
    (48, "Chuẩn bị môi trường triển khai", 2.2000, [47], ["Bùi Quốc Luýt"],
     "Tài liệu cấu hình hệ thống",
     "Máy chủ app, CSDL, Nginx HTTPS, sao lưu hằng ngày giữ 30 bản."),
    (49, "Chuyển đổi dữ liệu và triển khai hệ thống", 3.4833, [48], ["Vũ Quang Minh"],
     "Biên bản nghiệm thu",
     "Chuyển danh mục và tồn đầu kỳ từ Excel; triển khai kho tổng và cửa hàng."),
    (50, "Viết tài liệu hướng dẫn", 3.3000, [48], ["Phạm Đoàn Bảo Thiên"],
     "Tài liệu hướng dẫn",
     "Hướng dẫn theo vai trò Quản lý, NV kho, NV bán hàng và tài liệu vận hành."),
    (51, "Báo cáo nghiệm thu", 2.2000, [49, 50], ["Bùi Tuấn Anh"],
     "Báo cáo nghiệm thu",
     "Tổng hợp kết quả, kiểm thử, đối chiếu mục tiêu, hồ sơ nghiệm thu."),
    (52, "Đào tạo người dùng", 2.2000, [51], ["Bạch Minh Quang"],
     "Xác nhận bàn giao",
     "Hướng dẫn NV kho/cửa hàng, máy quét mã vạch; hỗ trợ vận hành ban đầu."),
]

PHASE_OF = {}
for stt, *_ in TASKS:
    if stt <= 8:
        PHASE_OF[stt] = "A"
    elif stt <= 17:
        PHASE_OF[stt] = "B"
    elif stt <= 25:
        PHASE_OF[stt] = "C"
    elif stt <= 39:
        PHASE_OF[stt] = "D"
    elif stt <= 47:
        PHASE_OF[stt] = "E"
    else:
        PHASE_OF[stt] = "F"


def kill_project() -> None:
    os.system("taskkill /IM WINPROJ.EXE /F >NUL 2>&1")
    time.sleep(2)


def com_set(obj, attr, value) -> None:
    try:
        setattr(obj, attr, value)
    except Exception as exc:
        print(f"  warn set {attr}={value!r}: {exc}")


def build() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        try:
            OUT.unlink()
        except PermissionError:
            kill_project()
            time.sleep(1)
            OUT.unlink()

    pythoncom.CoInitialize()
    kill_project()
    try:
        app = win32com.client.gencache.EnsureDispatch("MSProject.Application")
    except Exception:
        app = win32com.client.Dispatch("MSProject.Application")
    app.Visible = True
    app.DisplayAlerts = False
    try:
        app.FileClose(PJ_DO_NOT_SAVE)
    except Exception:
        pass

    try:
        app.FileNew()
        time.sleep(0.8)
        proj = app.ActiveProject
        try:
            app.NewTasksCreatedAsScheduled = True
        except Exception:
            pass

        try:
            app.ProjectSummaryInfo(
                Title="CNTT20261_N01 - Ke hoach du an",
                Subject="Xay dung he thong quan ly hang hoa va kho bai san pham thoi trang",
                Author="Nhom 1 - Bui Tuan Anh",
                Company="HUST SOICT",
                Manager="Bui Tuan Anh",
                Comments=(
                    "Nhom 1 | CNTT20261_N01 | 01/09/2026-31/03/2027 | "
                    "Ngan sach 408.196.650 VND (lao dong 285.396.650 + TBVT 73.800.000 + chi khac 49.000.000). "
                    "WBS 52 task, 6 giai doan, 5 thanh vien. Nguon: ton-chi-DA-va-phan-ra-cong-viec.xlsx, kinh-phi-du-an.xlsx."
                ),
                Start=START,
                Calendar="Standard",
            )
        except Exception as exc:
            print("ProjectSummaryInfo warn:", exc)

        com_set(proj, "CurrencyCode", "VND")
        com_set(proj, "CurrencySymbol", "₫")
        com_set(proj, "CurrencyDigits", 0)
        try:
            proj.CurrencySymbolPosition = 3
        except Exception:
            pass
        com_set(proj, "HoursPerDay", 8)
        com_set(proj, "HoursPerWeek", 40)
        com_set(proj, "DaysPerMonth", 20)

        # Resources
        work_res = {}
        for name, rate in RATES.items():
            r = proj.Resources.Add(name)
            com_set(r, "Initials", INITIALS[name])
            com_set(r, "Group", "Nhóm 1")
            com_set(r, "Code", INITIALS[name])
            com_set(r, "StandardRate", f"{rate}/d")
            com_set(r, "OvertimeRate", "0/d")
            com_set(r, "MaxUnits", 1.0)
            com_set(r, "Notes", f"{ROLES[name]}\nĐịnh mức {rate:,} VND/ngày công (lương cơ sở 2.530.000).".replace(",", "."))
            work_res[name] = r
            print("resource", name, rate)

        # Clear any default task
        for i in range(proj.Tasks.Count, 0, -1):
            t = proj.Tasks(i)
            if t is not None:
                try:
                    t.Delete()
                except Exception:
                    pass

        phase_tasks = {}
        leaf_by_stt = {}
        indent_targets = []

        for code, pname, pstart, p_tbvt, p_khac, pnotes in PHASES:
            pt = proj.Tasks.Add(pname)
            com_set(pt, "Manual", False)
            com_set(pt, "Notes", pnotes)
            phase_tasks[code] = pt
            print(f"phase {code} ID={pt.ID}")

            for stt, name, est, preds, people, deliverable, notes in TASKS:
                if PHASE_OF[stt] != code:
                    continue
                t = proj.Tasks.Add(f"{stt}. {name}")
                com_set(t, "Manual", False)
                com_set(t, "Type", PJ_FIXED_DURATION)
                try:
                    t.EffortDriven = False
                except Exception:
                    pass
                t.Duration = f"{est:.2f}d".replace(".", ",")
                com_set(t, "Notes", f"Sản phẩm: {deliverable}\n{notes}")
                if stt == 52:
                    try:
                        t.Deadline = DEADLINE
                    except Exception:
                        pass
                leaf_by_stt[stt] = t
                indent_targets.append(t)
                print(f"  task {stt} ID={t.ID} {est:.4f}d {people}")

            com_set(pt, "FixedCost", p_tbvt + p_khac)
            com_set(pt, "FixedCostAccrual", PJ_ACCRUE_START)
            try:
                pt.Cost1 = p_tbvt
                pt.Cost2 = p_khac
            except Exception:
                pass
            print(f"  fixed cost TBVT {p_tbvt} + CK {p_khac} = {p_tbvt + p_khac}")

        # Indent leaves + cost tasks under their preceding summary
        for t in indent_targets:
            try:
                t.OutlineIndent()
            except Exception as exc:
                print("  indent warn", t.Name, exc)

        # Predecessors: đúng cột "Thứ tự thực hiện" trên WBS, không thêm link
        for stt, name, est, preds, people, deliverable, notes in TASKS:
            t = leaf_by_stt[stt]
            for p in preds:
                try:
                    t.TaskDependencies.Add(leaf_by_stt[p])
                except Exception as exc:
                    print("  pred warn", stt, "<-", p, exc)

        # Cửa sổ thời gian từng giai đoạn trên WBS (cột Thời gian)
        entry_snet = {
            9: datetime(2026, 9, 26, 8, 0),
            18: datetime(2026, 11, 21, 8, 0),
            21: datetime(2026, 11, 21, 8, 0),
            26: datetime(2026, 12, 26, 8, 0),
            40: datetime(2027, 2, 16, 8, 0),
            48: datetime(2027, 3, 16, 8, 0),
        }
        for stt, when in entry_snet.items():
            t = leaf_by_stt[stt]
            try:
                t.ConstraintType = PJ_SNET
                t.ConstraintDate = when
                print(f"  SNET task {stt} {when.date()}")
            except Exception as exc:
                print("  SNET warn", stt, exc)

        # Resource assignments
        for stt, name, est, preds, people, deliverable, notes in TASKS:
            t = leaf_by_stt[stt]
            for person in people:
                try:
                    asn = t.Assignments.Add(ResourceID=work_res[person].ID)
                    asn.Units = 1.0
                    minutes = int(round(est * 8 * 60))
                    asn.Work = f"{minutes}m"
                except Exception as exc:
                    print("  assign warn", stt, person, exc)

        try:
            app.DisplayProjectSummaryTask = True
        except Exception:
            try:
                late = win32com.client.dynamic.Dispatch(app)
                late.DisplayProjectSummaryTask = True
            except Exception as exc:
                print("summary display warn", exc)
        try:
            pst = proj.ProjectSummaryTask
            pst.Name = "CNTT20261_N01 — QL hàng hóa & kho thời trang"
            com_set(pst, "Notes",
                    "Dự án phần mềm quy mô vừa. Chủ đầu tư: DN thời trang được khảo sát. "
                    "Ngân sách 408.196.650 VND. 5 thành viên, 07 tháng.")
            try:
                pst.Deadline = DEADLINE
            except Exception:
                pass
        except Exception as exc:
            print("summary warn", exc)

        try:
            app.HighlightCriticalTasks = True
        except Exception:
            pass
        try:
            app.ViewApply("Gantt Chart")
        except Exception:
            pass
        try:
            app.TableApply("Entry")
        except Exception:
            pass
        for col in ("Task Mode", "Chế độ tác vụ", "Task mode"):
            try:
                app.SelectTaskColumn(Column=col)
                app.ColumnDelete()
                break
            except Exception:
                continue
        try:
            app.SelectTaskColumn(Column="Cost")
        except Exception:
            try:
                app.SelectTaskColumn(Column="Finish")
                app.ColumnInsert(Column="Cost")
            except Exception as exc:
                print("  cost column warn", exc)
        try:
            app.ZoomTimescale(Start=START, Finish=DEADLINE)
        except Exception as exc:
            print("  zoom warn", exc)
            try:
                app.ZoomTimescale(Entire=True)
            except Exception:
                pass

        # Recalculate
        try:
            app.CalculateProject()
        except Exception:
            try:
                proj.Application.CalculateProject()
            except Exception:
                pass
        time.sleep(0.5)

        app.FileSaveAs(str(OUT))
        time.sleep(0.4)

        # Report
        pst = proj.ProjectSummaryTask
        print("==== RESULT ====")
        print("file", OUT, "size", OUT.stat().st_size)
        print("start", pst.Start)
        print("finish", pst.Finish)
        print("duration", pst.Duration)
        print("work", pst.Work)
        print("cost", pst.Cost)
        print("tasks", proj.Tasks.Count)
        print("resources", proj.Resources.Count)
    finally:
        try:
            app.FileClose(PJ_DO_NOT_SAVE)
        except Exception:
            pass
        try:
            app.Quit(PJ_DO_NOT_SAVE)
        except Exception:
            pass
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    build()
    print("DONE")
