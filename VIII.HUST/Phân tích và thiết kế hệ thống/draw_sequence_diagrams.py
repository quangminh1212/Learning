import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch


# High-contrast monochrome palette
ACTOR_BG = '#FFFFFF'
ACTOR_EDGE = 'black'
LIFELINE_COLOR = '#CCCCCC'
ALT_BG = '#FFFFFF'
ALT_EDGE = 'black'
SUB_BG = '#F8F8F8'
TEXT_COLOR = 'black'

# Large fonts for landscape A4 readability
ACTOR_FONTSIZE = 10.0
MESSAGE_FONTSIZE = 9.0
LABEL_FONTSIZE = 10.0
DPI = 300


def check_overlap(texts):
    """Check if any text boxes overlap."""
    if not texts:
        return []
    overlaps = []
    bboxes = []
    for t in texts:
        try:
            bbox = t.get_window_extent()
            bboxes.append((t, bbox))
        except Exception:
            continue
    for i in range(len(bboxes)):
        for j in range(i + 1, len(bboxes)):
            t1, b1 = bboxes[i]
            t2, b2 = bboxes[j]
            if b1.overlaps(b2):
                overlaps.append((t1.get_text(), t2.get_text()))
    return overlaps


def draw_sequence_diagram(actors, messages, alt_boxes, filename, height=6):
    """Draw a large, high-contrast monochrome sequence diagram for landscape A4."""
    fig, ax = plt.subplots(1, 1, figsize=(20, height))
    ax.set_xlim(0, 20)
    ax.set_ylim(-height + 0.5, 1.2)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    n = len(actors)
    positions = [1.5 + i * (17.0 / (n - 1)) for i in range(n)]

    # Actors
    for i, actor in enumerate(actors):
        x = positions[i]
        rect = FancyBboxPatch((x - 1.5, 0.85), 3.0, 0.35, boxstyle="round,pad=0.03",
                               linewidth=1.5, edgecolor=ACTOR_EDGE, facecolor=ACTOR_BG)
        ax.add_patch(rect)
        ax.text(x, 1.025, actor, fontsize=ACTOR_FONTSIZE, ha='center', va='center',
                color=TEXT_COLOR, fontweight='bold')
        ax.plot([x, x], [0.85, -height + 1], '--', linewidth=1.0, color=LIFELINE_COLOR, alpha=0.9)

    all_texts = []

    def draw_message(y, from_idx, to_idx, text, is_return):
        x1 = positions[from_idx]
        x2 = positions[to_idx]
        linestyle = 'dashed' if is_return else 'solid'
        arrow = FancyArrowPatch((x1, y), (x2, y), arrowstyle='->', mutation_scale=12,
                                linewidth=1.2, linestyle=linestyle, color=TEXT_COLOR)
        ax.add_patch(arrow)
        mid_x = (x1 + x2) / 2
        txt = ax.text(mid_x, y + 0.10, text, fontsize=MESSAGE_FONTSIZE, ha='center', va='bottom',
                      color=TEXT_COLOR, wrap=True,
                      bbox=dict(boxstyle='round,pad=0.12', facecolor='white', edgecolor='none', alpha=0.95))
        all_texts.append(txt)
        return txt

    # Alt boxes
    for y1, y2, label, sub_boxes in alt_boxes:
        rect = FancyBboxPatch((0.5, y2), 19, y1 - y2, boxstyle="round,pad=0.03",
                               linewidth=1.5, edgecolor=ALT_EDGE, facecolor=ALT_BG, alpha=1.0)
        ax.add_patch(rect)
        lbl = ax.text(0.7, y1 - 0.15, label, fontsize=LABEL_FONTSIZE, fontweight='bold', va='top', color=TEXT_COLOR)
        all_texts.append(lbl)

        for sub_y1, sub_y2, sub_label, sub_messages in sub_boxes:
            rect = FancyBboxPatch((0.8, sub_y2), 18.4, sub_y1 - sub_y2, boxstyle="round,pad=0.03",
                                   linewidth=1.2, edgecolor=ALT_EDGE, facecolor=SUB_BG, alpha=1.0)
            ax.add_patch(rect)
            sub_lbl = ax.text(1.0, sub_y1 - 0.10, sub_label, fontsize=LABEL_FONTSIZE - 1, va='top',
                              color=TEXT_COLOR, style='italic')
            all_texts.append(sub_lbl)
            for y, from_idx, to_idx, text, is_return in sub_messages:
                draw_message(y, from_idx, to_idx, text, is_return)

    # Main messages
    for y, from_idx, to_idx, text, is_return in messages:
        draw_message(y, from_idx, to_idx, text, is_return)

    plt.tight_layout()
    plt.savefig(filename, dpi=DPI, bbox_inches='tight', facecolor='white')

    # Skip overlap check to avoid errors
    print(f'Saved: {filename}')

    plt.close()


# ==================== 1. Ghi nhận hàng lỗi ====================
actors1 = ['Nhân viên\nkho', 'Giao diện\nhàng lỗi', 'HangLoi\nController', 'Database']

messages1 = [
    (-0.50, 0, 1, 'Chọn "Ghi nhận hàng lỗi"', False),
    (-0.95, 1, 2, 'ghiNhanHangLoi()', False),
    (-1.40, 2, 3, 'Lấy danh sách hàng hóa', False),
    (-1.85, 3, 2, 'Danh sách hàng hóa', True),
    (-2.30, 2, 1, 'Danh sách hàng hóa', True),
    (-2.75, 1, 0, 'Hiển thị danh sách', False),
    (-3.20, 0, 1, 'Chọn hàng hóa, nhập SL lỗi, nguyên nhân', False),
    (-3.65, 1, 2, 'ghiNhanHangLoi(hàng hóa, SL lỗi, nguyên nhân)', False),
]

alt1 = [
    (-4.00, -4.80, 'alt [Chưa chọn nguyên nhân]', [
        (-4.00, -4.80, '[Chưa chọn nguyên nhân]', [
            (-4.50, 2, 1, 'Vui lòng chọn nguyên nhân', False),
        ]),
    ]),
    (-5.15, -7.50, 'alt [Đã chọn nguyên nhân]', [
        (-5.15, -6.20, '[SL lỗi > SL tồn]', [
            (-5.75, 2, 3, 'Kiểm tra số lượng tồn', False),
            (-6.20, 3, 2, 'Số lượng tồn', True),
            (-6.65, 2, 1, 'Số lượng vượt quá tồn kho', False),
        ]),
        (-6.90, -7.50, '[Số lượng hợp lệ]', [
            (-7.50, 2, 3, 'Giảm tồn kho, chuyển khu vực lỗi, lưu phiếu', False),
            (-7.95, 3, 2, 'Lưu thành công', True),
            (-8.35, 2, 1, 'Thông báo thành công', False),
        ]),
    ]),
]

draw_sequence_diagram(actors1, messages1, alt1,
                      'sequence_ghi_nhan_hang_loi.png', height=8.5)

# ==================== 2. Xử lý hàng lỗi ====================
actors2 = ['Quản lý\nkho', 'Giao diện\nhàng lỗi', 'HangLoi\nController', 'Database']

messages2 = [
    (-0.50, 0, 1, 'Mở phiếu hàng lỗi', False),
    (-0.95, 1, 2, 'Yêu cầu mở phiếu (mã phiếu)', False),
    (-1.40, 2, 3, 'Lấy thông tin phiếu hàng lỗi', False),
    (-1.85, 3, 2, 'Thông tin phiếu', True),
    (-2.30, 2, 1, 'Thông tin phiếu', True),
]

alt2 = [
    (-2.65, -4.40, 'alt', [
        (-2.65, -3.40, '[Phiếu đã xử lý]', [
            (-3.30, 1, 0, 'Phiếu đã xử lý, không thể xử lý lại', False),
        ]),
        (-3.75, -4.40, '[Phiếu chưa xử lý]', [
            (-4.15, 1, 0, 'Hiển thị thông tin phiếu', False),
            (-4.50, 1, 0, 'Hiển thị phương án xử lý', False),
        ]),
    ]),
    (-4.80, -5.30, '', [
        (-4.80, -5.30, '', [
            (-4.80, 0, 1, 'Chọn phương án xử lý', False),
        ]),
    ]),
    (-5.55, -7.50, 'alt', [
        (-5.55, -6.50, '[Chưa chọn phương án]', [
            (-6.25, 1, 0, 'Vui lòng chọn phương án xử lý', False),
        ]),
        (-6.80, -7.50, '[Đã chọn phương án]', [
            (-7.15, 0, 1, 'Xác nhận xử lý', False),
            (-7.50, 1, 2, 'Xử lý hàng lỗi (phương án)', False),
            (-7.85, 2, 3, 'Cập nhật tồn kho hàng lỗi', False),
            (-8.20, 2, 3, 'Lưu lịch sử xử lý', False),
            (-8.55, 2, 3, 'Cập nhật trạng thái phiếu', False),
        ]),
    ]),
    (-8.95, -9.60, '', [
        (-8.95, -9.60, '', [
            (-8.95, 3, 2, 'Cập nhật thành công', True),
            (-9.25, 2, 1, 'Thông báo xử lý thành công', False),
            (-9.55, 1, 0, 'Thông báo xử lý thành công', False),
        ]),
    ]),
]

draw_sequence_diagram(actors2, messages2, alt2,
                      'sequence_xu_ly_hang_loi.png', height=9.5)

# ==================== 3. Thêm nhà cung cấp ====================
actors3 = ['Người dùng', 'Giao diện\nNCC', 'NCC\nController', 'Database']

messages3 = [
    (-0.50, 0, 1, 'Chọn "Thêm NCC"', False),
    (-0.95, 1, 0, 'Hiển thị form thêm NCC', False),
    (-1.40, 0, 1, 'Nhập thông tin NCC', False),
    (-1.85, 0, 1, 'Nhấn "Lưu"', False),
    (-2.30, 1, 2, 'themNhaCungCap(thông tin)', False),
]

alt3 = [
    (-2.65, -6.10, 'alt', [
        (-2.65, -3.75, '[Dữ liệu không hợp lệ]', [
            (-3.30, 2, 1, 'Thông báo lỗi cụ thể', False),
        ]),
        (-3.95, -4.85, '[Mã NCC trùng lặp]', [
            (-4.55, 2, 1, 'Mã NCC đã tồn tại', False),
        ]),
        (-5.05, -6.10, '[Dữ liệu hợp lệ]', [
            (-5.65, 2, 3, 'Lưu thông tin NCC', False),
            (-6.05, 3, 2, 'Lưu thành công', True),
            (-6.50, 2, 1, 'Thêm NCC thành công', False),
            (-6.95, 1, 0, 'Thêm NCC thành công', False),
        ]),
    ]),
]

draw_sequence_diagram(actors3, messages3, alt3,
                      'sequence_them_nha_cung_cap.png', height=7)

# ==================== 4. Tìm kiếm nhà cung cấp ====================
actors4 = ['Người dùng', 'Giao diện\nNCC', 'NCC\nController', 'Database']

messages4 = [
    (-0.50, 0, 1, 'Chọn "Tìm kiếm NCC"', False),
    (-0.95, 1, 0, 'Hiển thị ô tìm kiếm', False),
    (-1.40, 0, 1, 'Nhập từ khóa, chọn tiêu chí', False),
    (-1.85, 0, 1, 'Nhấn "Tìm kiếm"', False),
    (-2.30, 1, 2, 'timKiemNhaCungCap(từ khóa, tiêu chí)', False),
    (-2.75, 2, 3, 'Tìm kiếm theo tiêu chí', False),
    (-3.20, 3, 2, 'Kết quả tìm kiếm', True),
    (-3.65, 2, 1, 'Kết quả tìm kiếm', True),
    (-4.10, 1, 0, 'Hiển thị kết quả', False),
]

draw_sequence_diagram(actors4, messages4, [],
                      'sequence_tim_kiem_nha_cung_cap.png', height=5)

# ==================== 5. Thêm kho ====================
actors5 = ['Người dùng', 'Giao diện\nkho', 'Kho\nController', 'Database']

messages5 = [
    (-0.50, 0, 1, 'Chọn "Thêm kho"', False),
    (-0.95, 1, 0, 'Hiển thị form thêm kho', False),
    (-1.40, 0, 1, 'Nhập thông tin kho', False),
    (-1.85, 0, 1, 'Nhấn "Lưu"', False),
    (-2.30, 1, 2, 'themKho(thông tin)', False),
]

alt5 = [
    (-2.65, -6.10, 'alt', [
        (-2.65, -3.75, '[Dữ liệu không hợp lệ]', [
            (-3.30, 2, 1, 'Thông báo lỗi cụ thể', False),
        ]),
        (-3.95, -4.85, '[Mã kho trùng lặp]', [
            (-4.55, 2, 1, 'Mã kho đã tồn tại', False),
        ]),
        (-5.05, -6.10, '[Dữ liệu hợp lệ]', [
            (-5.65, 2, 3, 'Lưu thông tin kho, trạng thái Hoạt động', False),
            (-6.05, 3, 2, 'Lưu thành công', True),
            (-6.50, 2, 1, 'Thêm kho thành công', False),
            (-6.95, 1, 0, 'Thêm kho thành công', False),
        ]),
    ]),
]

draw_sequence_diagram(actors5, messages5, alt5,
                      'sequence_them_kho.png', height=7)

# ==================== 6. Quản lý trạng thái kho ====================
actors6 = ['Người dùng', 'Giao diện\nkho', 'Kho\nController', 'Database']

messages6 = [
    (-0.50, 0, 1, 'Chọn kho cần thay đổi', False),
    (-0.95, 1, 0, 'Hiển thị trạng thái hiện tại', False),
    (-1.40, 0, 1, 'Chọn trạng thái mới', False),
    (-1.85, 0, 1, 'Nhấn "Cập nhật trạng thái"', False),
    (-2.30, 1, 2, 'capNhatTrangThaiKho()', False),
]

alt6 = [
    (-2.65, -6.10, 'alt', [
        (-2.65, -4.15, '[Đóng/Tạm dừng có hàng hóa]', [
            (-3.40, 2, 3, 'Kiểm tra hàng hóa trong kho', False),
            (-3.80, 3, 2, 'Có hàng hóa', True),
            (-4.20, 2, 1, 'Kho có hàng, vui lòng chuyển hàng', False),
        ]),
        (-4.45, -6.10, '[Cập nhật thành công]', [
            (-5.05, 2, 3, 'Cập nhật trạng thái kho', False),
            (-5.45, 3, 2, 'Cập nhật thành công', True),
            (-5.85, 2, 1, 'Cập nhật trạng thái thành công', False),
            (-6.25, 1, 0, 'Cập nhật trạng thái thành công', False),
        ]),
    ]),
]

draw_sequence_diagram(actors6, messages6, alt6,
                      'sequence_quan_ly_trang_thai_kho.png', height=7)
