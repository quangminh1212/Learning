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
    fig, ax = plt.subplots(1, 1, figsize=(18, height))
    ax.set_xlim(0, 18)
    ax.set_ylim(-height + 0.5, 1.2)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    n = len(actors)
    positions = [1.5 + i * (15.0 / (n - 1)) for i in range(n)]

    # Actors
    for i, actor in enumerate(actors):
        x = positions[i]
        rect = FancyBboxPatch((x - 1.5, 0.8), 3.0, 0.4, boxstyle="round,pad=0.03",
                               linewidth=1.5, edgecolor=ACTOR_EDGE, facecolor=ACTOR_BG)
        ax.add_patch(rect)
        ax.text(x, 1.0, actor, fontsize=ACTOR_FONTSIZE, ha='center', va='center',
                color=TEXT_COLOR, fontweight='bold')
        ax.plot([x, x], [0.8, -height + 1], '--', linewidth=1.0, color=LIFELINE_COLOR, alpha=0.9)

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
        rect = FancyBboxPatch((0.5, y2), 17, y1 - y2, boxstyle="round,pad=0.03",
                               linewidth=1.5, edgecolor=ALT_EDGE, facecolor=ALT_BG, alpha=1.0)
        ax.add_patch(rect)
        lbl = ax.text(0.7, y1 - 0.12, label, fontsize=LABEL_FONTSIZE, fontweight='bold', va='top', color=TEXT_COLOR)
        all_texts.append(lbl)

        for sub_y1, sub_y2, sub_label, sub_messages in sub_boxes:
            rect = FancyBboxPatch((0.8, sub_y2), 16.4, sub_y1 - sub_y2, boxstyle="round,pad=0.03",
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

    # Check for overlaps after rendering
    fig.canvas.draw()
    overlaps = check_overlap(all_texts)
    if overlaps:
        print(f'WARNING: Overlap detected in {filename}:')
        for pair in overlaps:
            print(f'  - "{pair[0]}" overlaps "{pair[1]}"')
    else:
        print(f'No text overlap detected in {filename}')

    plt.close()
    print(f'Saved: {filename}')


# ==================== 1. Ghi nhận hàng lỗi ====================
actors1 = ['Nhân viên\nkho', 'Giao diện\nhàng lỗi', 'HangLoi\nController', 'Database']

messages1 = [
    (-0.45, 0, 1, 'Chọn "Ghi nhận hàng lỗi"', False),
    (-0.80, 1, 2, 'ghiNhanHangLoi()', False),
    (-1.15, 2, 3, 'Lấy danh sách hàng hóa', False),
    (-1.50, 3, 2, 'Danh sách hàng hóa', True),
    (-1.85, 2, 1, 'Danh sách hàng hóa', True),
    (-2.20, 1, 0, 'Hiển thị danh sách', False),
    (-2.55, 0, 1, 'Chọn hàng hóa, nhập SL lỗi, nguyên nhân', False),
    (-2.90, 1, 2, 'ghiNhanHangLoi(hàng hóa, SL lỗi, nguyên nhân)', False),
]

alt1 = [
    (-3.25, -4.25, 'alt [Chưa chọn nguyên nhân]', [
        (-3.25, -4.25, '[Chưa chọn nguyên nhân]', [
            (-3.75, 2, 1, 'Vui lòng chọn nguyên nhân', False),
        ]),
    ]),
    (-4.45, -6.80, 'alt [Đã chọn nguyên nhân]', [
        (-4.45, -5.75, '[SL lỗi > SL tồn]', [
            (-5.05, 2, 3, 'Kiểm tra số lượng tồn', False),
            (-5.45, 3, 2, 'Số lượng tồn', True),
            (-5.85, 2, 1, 'Số lượng vượt quá tồn kho', False),
        ]),
        (-6.00, -6.80, '[Số lượng hợp lệ]', [
            (-6.55, 2, 3, 'Giảm tồn kho, chuyển khu vực lỗi, lưu phiếu', False),
            (-6.95, 3, 2, 'Lưu thành công', True),
            (-7.25, 2, 1, 'Thông báo thành công', False),
        ]),
    ]),
]

draw_sequence_diagram(actors1, messages1, alt1,
                      'sequence_ghi_nhan_hang_loi.png', height=7.5)

# ==================== 2. Xử lý hàng lỗi ====================
actors2 = ['Quản lý\nkho', 'Giao diện\nhàng lỗi', 'HangLoi\nController', 'Database']

messages2 = [
    (-0.45, 0, 1, 'Mở phiếu hàng lỗi', False),
    (-0.80, 1, 2, 'Yêu cầu mở phiếu (mã phiếu)', False),
    (-1.15, 2, 3, 'Lấy thông tin phiếu hàng lỗi', False),
    (-1.50, 3, 2, 'Thông tin phiếu', True),
    (-1.85, 2, 1, 'Thông tin phiếu', True),
]

alt2 = [
    (-2.15, -3.80, 'alt', [
        (-2.15, -2.95, '[Phiếu đã xử lý]', [
            (-2.80, 1, 0, 'Phiếu đã xử lý, không thể xử lý lại', False),
        ]),
        (-3.15, -3.80, '[Phiếu chưa xử lý]', [
            (-3.50, 1, 0, 'Hiển thị thông tin phiếu', False),
            (-3.80, 1, 0, 'Hiển thị phương án xử lý', False),
        ]),
    ]),
    (-4.05, -4.45, '', [
        (-4.05, -4.45, '', [
            (-4.05, 0, 1, 'Chọn phương án xử lý', False),
        ]),
    ]),
    (-4.70, -6.50, 'alt', [
        (-4.70, -5.60, '[Chưa chọn phương án]', [
            (-5.35, 1, 0, 'Vui lòng chọn phương án xử lý', False),
        ]),
        (-5.85, -6.50, '[Đã chọn phương án]', [
            (-6.20, 0, 1, 'Xác nhận xử lý', False),
            (-6.55, 1, 2, 'Xử lý hàng lỗi (phương án)', False),
            (-6.90, 2, 3, 'Cập nhật tồn kho hàng lỗi', False),
            (-7.25, 2, 3, 'Lưu lịch sử xử lý', False),
            (-7.60, 2, 3, 'Cập nhật trạng thái phiếu', False),
        ]),
    ]),
    (-7.95, -8.55, '', [
        (-7.95, -8.55, '', [
            (-7.95, 3, 2, 'Cập nhật thành công', True),
            (-8.25, 2, 1, 'Thông báo xử lý thành công', False),
            (-8.50, 1, 0, 'Thông báo xử lý thành công', False),
        ]),
    ]),
]

draw_sequence_diagram(actors2, messages2, alt2,
                      'sequence_xu_ly_hang_loi.png', height=8.5)

# ==================== 3. Thêm nhà cung cấp ====================
actors3 = ['Người dùng', 'Giao diện\nNCC', 'NCC\nController', 'Database']

messages3 = [
    (-0.45, 0, 1, 'Chọn "Thêm NCC"', False),
    (-0.80, 1, 0, 'Hiển thị form thêm NCC', False),
    (-1.15, 0, 1, 'Nhập thông tin NCC', False),
    (-1.50, 0, 1, 'Nhấn "Lưu"', False),
    (-1.85, 1, 2, 'themNhaCungCap(thông tin)', False),
]

alt3 = [
    (-2.15, -5.10, 'alt', [
        (-2.15, -3.15, '[Dữ liệu không hợp lệ]', [
            (-2.75, 2, 1, 'Thông báo lỗi cụ thể', False),
        ]),
        (-3.30, -4.10, '[Mã NCC trùng lặp]', [
            (-3.85, 2, 1, 'Mã NCC đã tồn tại', False),
        ]),
        (-4.35, -5.10, '[Dữ liệu hợp lệ]', [
            (-4.95, 2, 3, 'Lưu thông tin NCC', False),
            (-5.35, 3, 2, 'Lưu thành công', True),
            (-5.75, 2, 1, 'Thêm NCC thành công', False),
            (-6.10, 1, 0, 'Thêm NCC thành công', False),
        ]),
    ]),
]

draw_sequence_diagram(actors3, messages3, alt3,
                      'sequence_them_nha_cung_cap.png', height=6)

# ==================== 4. Tìm kiếm nhà cung cấp ====================
actors4 = ['Người dùng', 'Giao diện\nNCC', 'NCC\nController', 'Database']

messages4 = [
    (-0.45, 0, 1, 'Chọn "Tìm kiếm NCC"', False),
    (-0.80, 1, 0, 'Hiển thị ô tìm kiếm', False),
    (-1.15, 0, 1, 'Nhập từ khóa, chọn tiêu chí', False),
    (-1.50, 0, 1, 'Nhấn "Tìm kiếm"', False),
    (-1.85, 1, 2, 'timKiemNhaCungCap(từ khóa, tiêu chí)', False),
    (-2.20, 2, 3, 'Tìm kiếm theo tiêu chí', False),
    (-2.55, 3, 2, 'Kết quả tìm kiếm', True),
    (-2.90, 2, 1, 'Kết quả tìm kiếm', True),
    (-3.25, 1, 0, 'Hiển thị kết quả', False),
]

draw_sequence_diagram(actors4, messages4, [],
                      'sequence_tim_kiem_nha_cung_cap.png', height=4)

# ==================== 5. Thêm kho ====================
actors5 = ['Người dùng', 'Giao diện\nkho', 'Kho\nController', 'Database']

messages5 = [
    (-0.45, 0, 1, 'Chọn "Thêm kho"', False),
    (-0.80, 1, 0, 'Hiển thị form thêm kho', False),
    (-1.15, 0, 1, 'Nhập thông tin kho', False),
    (-1.50, 0, 1, 'Nhấn "Lưu"', False),
    (-1.85, 1, 2, 'themKho(thông tin)', False),
]

alt5 = [
    (-2.15, -5.10, 'alt', [
        (-2.15, -3.15, '[Dữ liệu không hợp lệ]', [
            (-2.75, 2, 1, 'Thông báo lỗi cụ thể', False),
        ]),
        (-3.30, -4.10, '[Mã kho trùng lặp]', [
            (-3.85, 2, 1, 'Mã kho đã tồn tại', False),
        ]),
        (-4.35, -5.10, '[Dữ liệu hợp lệ]', [
            (-4.95, 2, 3, 'Lưu thông tin kho, trạng thái Hoạt động', False),
            (-5.35, 3, 2, 'Lưu thành công', True),
            (-5.75, 2, 1, 'Thêm kho thành công', False),
            (-6.10, 1, 0, 'Thêm kho thành công', False),
        ]),
    ]),
]

draw_sequence_diagram(actors5, messages5, alt5,
                      'sequence_them_kho.png', height=6)

# ==================== 6. Quản lý trạng thái kho ====================
actors6 = ['Người dùng', 'Giao diện\nkho', 'Kho\nController', 'Database']

messages6 = [
    (-0.45, 0, 1, 'Chọn kho cần thay đổi', False),
    (-0.80, 1, 0, 'Hiển thị trạng thái hiện tại', False),
    (-1.15, 0, 1, 'Chọn trạng thái mới', False),
    (-1.50, 0, 1, 'Nhấn "Cập nhật trạng thái"', False),
    (-1.85, 1, 2, 'capNhatTrangThaiKho()', False),
]

alt6 = [
    (-2.15, -5.10, 'alt', [
        (-2.15, -3.55, '[Đóng/Tạm dừng có hàng hóa]', [
            (-2.90, 2, 3, 'Kiểm tra hàng hóa trong kho', False),
            (-3.30, 3, 2, 'Có hàng hóa', True),
            (-3.70, 2, 1, 'Kho có hàng, vui lòng chuyển hàng', False),
        ]),
        (-3.85, -5.10, '[Cập nhật thành công]', [
            (-4.45, 2, 3, 'Cập nhật trạng thái kho', False),
            (-4.85, 3, 2, 'Cập nhật thành công', True),
            (-5.25, 2, 1, 'Cập nhật trạng thái thành công', False),
            (-5.65, 1, 0, 'Cập nhật trạng thái thành công', False),
        ]),
    ]),
]

draw_sequence_diagram(actors6, messages6, alt6,
                      'sequence_quan_ly_trang_thai_kho.png', height=6)
