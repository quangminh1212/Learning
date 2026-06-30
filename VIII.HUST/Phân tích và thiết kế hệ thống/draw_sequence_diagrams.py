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

# Very compact fonts
ACTOR_FONTSIZE = 5.0
MESSAGE_FONTSIZE = 4.5
LABEL_FONTSIZE = 5.0
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


def draw_sequence_diagram(title, actors, messages, alt_boxes, filename, height=3.5):
    """Draw a very compact, high-contrast monochrome sequence diagram."""
    fig, ax = plt.subplots(1, 1, figsize=(12, height))
    ax.set_xlim(0, 12)
    ax.set_ylim(-height + 0.5, 1.5)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    n = len(actors)
    positions = [1.5 + i * (9.0 / (n - 1)) for i in range(n)]

    # Actors
    for i, actor in enumerate(actors):
        x = positions[i]
        rect = FancyBboxPatch((x - 1.1, 0.8), 2.2, 0.4, boxstyle="round,pad=0.03",
                               linewidth=1.0, edgecolor=ACTOR_EDGE, facecolor=ACTOR_BG)
        ax.add_patch(rect)
        ax.text(x, 1.0, actor, fontsize=ACTOR_FONTSIZE, ha='center', va='center',
                color=TEXT_COLOR, fontweight='bold')
        ax.plot([x, x], [0.8, -height + 1], '--', linewidth=0.6, color=LIFELINE_COLOR, alpha=0.9)

    all_texts = []

    def draw_message(y, from_idx, to_idx, text, is_return):
        x1 = positions[from_idx]
        x2 = positions[to_idx]
        linestyle = 'dashed' if is_return else 'solid'
        arrow = FancyArrowPatch((x1, y), (x2, y), arrowstyle='->', mutation_scale=8,
                                linewidth=0.8, linestyle=linestyle, color=TEXT_COLOR)
        ax.add_patch(arrow)
        mid_x = (x1 + x2) / 2
        txt = ax.text(mid_x, y + 0.06, text, fontsize=MESSAGE_FONTSIZE, ha='center', va='bottom',
                      color=TEXT_COLOR, wrap=True,
                      bbox=dict(boxstyle='round,pad=0.08', facecolor='white', edgecolor='none', alpha=0.95))
        all_texts.append(txt)
        return txt

    # Alt boxes
    for y1, y2, label, sub_boxes in alt_boxes:
        rect = FancyBboxPatch((0.5, y2), 11, y1 - y2, boxstyle="round,pad=0.03",
                               linewidth=1.0, edgecolor=ALT_EDGE, facecolor=ALT_BG, alpha=1.0)
        ax.add_patch(rect)
        lbl = ax.text(0.7, y1 - 0.10, label, fontsize=LABEL_FONTSIZE, fontweight='bold', va='top', color=TEXT_COLOR)
        all_texts.append(lbl)

        for sub_y1, sub_y2, sub_label, sub_messages in sub_boxes:
            rect = FancyBboxPatch((0.8, sub_y2), 10.4, sub_y1 - sub_y2, boxstyle="round,pad=0.03",
                                   linewidth=0.8, edgecolor=ALT_EDGE, facecolor=SUB_BG, alpha=1.0)
            ax.add_patch(rect)
            sub_lbl = ax.text(1.0, sub_y1 - 0.08, sub_label, fontsize=LABEL_FONTSIZE - 0.5, va='top',
                              color=TEXT_COLOR, style='italic')
            all_texts.append(sub_lbl)
            for y, from_idx, to_idx, text, is_return in sub_messages:
                draw_message(y, from_idx, to_idx, text, is_return)

    # Main messages
    for y, from_idx, to_idx, text, is_return in messages:
        draw_message(y, from_idx, to_idx, text, is_return)

    ax.set_title(title, fontsize=7, fontweight='bold', pad=3, color=TEXT_COLOR)
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
    (-0.30, 0, 1, 'Chọn "Ghi nhận hàng lỗi"', False),
    (-0.50, 1, 2, 'ghiNhanHangLoi()', False),
    (-0.70, 2, 3, 'Lấy danh sách hàng hóa', False),
    (-0.90, 3, 2, 'Danh sách hàng hóa', True),
    (-1.10, 2, 1, 'Danh sách hàng hóa', True),
    (-1.30, 1, 0, 'Hiển thị danh sách', False),
    (-1.50, 0, 1, 'Chọn hàng hóa, nhập SL lỗi, nguyên nhân', False),
    (-1.70, 1, 2, 'ghiNhanHangLoi(hàng hóa, SL lỗi, nguyên nhân)', False),
]

alt1 = [
    (-1.90, -2.40, 'alt [Chưa chọn nguyên nhân]', [
        (-1.90, -2.40, '[Chưa chọn nguyên nhân]', [
            (-2.15, 2, 1, 'Vui lòng chọn nguyên nhân', False),
        ]),
    ]),
    (-2.45, -3.70, 'alt [Đã chọn nguyên nhân]', [
        (-2.45, -3.10, '[SL lỗi > SL tồn]', [
            (-2.80, 2, 3, 'Kiểm tra số lượng tồn', False),
            (-3.00, 3, 2, 'Số lượng tồn', True),
            (-3.20, 2, 1, 'Số lượng vượt quá tồn kho', False),
        ]),
        (-3.30, -3.70, '[Số lượng hợp lệ]', [
            (-3.60, 2, 3, 'Giảm tồn kho, chuyển khu vực lỗi, lưu phiếu', False),
            (-3.80, 3, 2, 'Lưu thành công', True),
            (-3.90, 2, 1, 'Thông báo thành công', False),
        ]),
    ]),
]

draw_sequence_diagram('Sequence Diagram: Ghi nhận hàng lỗi', actors1, messages1, alt1,
                      'sequence_ghi_nhan_hang_loi.png', height=4.5)

# ==================== 2. Xử lý hàng lỗi ====================
actors2 = ['Quản lý\nkho', 'Giao diện\nhàng lỗi', 'HangLoi\nController', 'Database']

messages2 = [
    (-0.30, 0, 1, 'Mở phiếu hàng lỗi', False),
    (-0.50, 1, 2, 'Yêu cầu mở phiếu (mã phiếu)', False),
    (-0.70, 2, 3, 'Lấy thông tin phiếu hàng lỗi', False),
    (-0.90, 3, 2, 'Thông tin phiếu', True),
    (-1.10, 2, 1, 'Thông tin phiếu', True),
]

alt2 = [
    (-1.25, -2.20, 'alt', [
        (-1.25, -1.75, '[Phiếu đã xử lý]', [
            (-1.65, 1, 0, 'Phiếu đã xử lý, không thể xử lý lại', False),
        ]),
        (-1.85, -2.20, '[Phiếu chưa xử lý]', [
            (-2.05, 1, 0, 'Hiển thị thông tin phiếu', False),
            (-2.20, 1, 0, 'Hiển thị phương án xử lý', False),
        ]),
    ]),
    (-2.35, -2.55, '', [
        (-2.35, -2.55, '', [
            (-2.35, 0, 1, 'Chọn phương án xử lý', False),
        ]),
    ]),
    (-2.60, -3.55, 'alt', [
        (-2.60, -3.05, '[Chưa chọn phương án]', [
            (-2.95, 1, 0, 'Vui lòng chọn phương án xử lý', False),
        ]),
        (-3.10, -3.55, '[Đã chọn phương án]', [
            (-3.30, 0, 1, 'Xác nhận xử lý', False),
            (-3.45, 1, 2, 'Xử lý hàng lỗi (phương án)', False),
            (-3.60, 2, 3, 'Cập nhật tồn kho hàng lỗi', False),
            (-3.75, 2, 3, 'Lưu lịch sử xử lý', False),
            (-3.90, 2, 3, 'Cập nhật trạng thái phiếu', False),
        ]),
    ]),
    (-4.05, -4.25, '', [
        (-4.05, -4.25, '', [
            (-4.05, 3, 2, 'Cập nhật thành công', True),
            (-4.20, 2, 1, 'Thông báo xử lý thành công', False),
            (-4.30, 1, 0, 'Thông báo xử lý thành công', False),
        ]),
    ]),
]

draw_sequence_diagram('Sequence Diagram: Xử lý hàng lỗi', actors2, messages2, alt2,
                      'sequence_xu_ly_hang_loi.png', height=4.5)

# ==================== 3. Thêm nhà cung cấp ====================
actors3 = ['Người dùng', 'Giao diện\nNCC', 'NCC\nController', 'Database']

messages3 = [
    (-0.30, 0, 1, 'Chọn "Thêm NCC"', False),
    (-0.50, 1, 0, 'Hiển thị form thêm NCC', False),
    (-0.70, 0, 1, 'Nhập thông tin NCC', False),
    (-0.90, 0, 1, 'Nhấn "Lưu"', False),
    (-1.10, 1, 2, 'themNhaCungCap(thông tin)', False),
]

alt3 = [
    (-1.25, -2.85, 'alt', [
        (-1.25, -2.00, '[Dữ liệu không hợp lệ]', [
            (-1.75, 2, 1, 'Thông báo lỗi cụ thể', False),
        ]),
        (-2.05, -2.45, '[Mã NCC trùng lặp]', [
            (-2.35, 2, 1, 'Mã NCC đã tồn tại', False),
        ]),
        (-2.55, -2.85, '[Dữ liệu hợp lệ]', [
            (-2.85, 2, 3, 'Lưu thông tin NCC', False),
            (-3.05, 3, 2, 'Lưu thành công', True),
            (-3.25, 2, 1, 'Thêm NCC thành công', False),
            (-3.40, 1, 0, 'Thêm NCC thành công', False),
        ]),
    ]),
]

draw_sequence_diagram('Sequence Diagram: Thêm nhà cung cấp', actors3, messages3, alt3,
                      'sequence_them_nha_cung_cap.png', height=3.8)

# ==================== 4. Tìm kiếm nhà cung cấp ====================
actors4 = ['Người dùng', 'Giao diện\nNCC', 'NCC\nController', 'Database']

messages4 = [
    (-0.30, 0, 1, 'Chọn "Tìm kiếm NCC"', False),
    (-0.50, 1, 0, 'Hiển thị ô tìm kiếm', False),
    (-0.70, 0, 1, 'Nhập từ khóa, chọn tiêu chí', False),
    (-0.90, 0, 1, 'Nhấn "Tìm kiếm"', False),
    (-1.10, 1, 2, 'timKiemNhaCungCap(từ khóa, tiêu chí)', False),
    (-1.30, 2, 3, 'Tìm kiếm theo tiêu chí', False),
    (-1.50, 3, 2, 'Kết quả tìm kiếm', True),
    (-1.70, 2, 1, 'Kết quả tìm kiếm', True),
    (-1.90, 1, 0, 'Hiển thị kết quả', False),
]

draw_sequence_diagram('Sequence Diagram: Tìm kiếm nhà cung cấp', actors4, messages4, [],
                      'sequence_tim_kiem_nha_cung_cap.png', height=2.8)

# ==================== 5. Thêm kho ====================
actors5 = ['Người dùng', 'Giao diện\nkho', 'Kho\nController', 'Database']

messages5 = [
    (-0.30, 0, 1, 'Chọn "Thêm kho"', False),
    (-0.50, 1, 0, 'Hiển thị form thêm kho', False),
    (-0.70, 0, 1, 'Nhập thông tin kho', False),
    (-0.90, 0, 1, 'Nhấn "Lưu"', False),
    (-1.10, 1, 2, 'themKho(thông tin)', False),
]

alt5 = [
    (-1.25, -2.85, 'alt', [
        (-1.25, -2.00, '[Dữ liệu không hợp lệ]', [
            (-1.75, 2, 1, 'Thông báo lỗi cụ thể', False),
        ]),
        (-2.05, -2.45, '[Mã kho trùng lặp]', [
            (-2.35, 2, 1, 'Mã kho đã tồn tại', False),
        ]),
        (-2.55, -2.85, '[Dữ liệu hợp lệ]', [
            (-2.85, 2, 3, 'Lưu thông tin kho, trạng thái Hoạt động', False),
            (-3.05, 3, 2, 'Lưu thành công', True),
            (-3.25, 2, 1, 'Thêm kho thành công', False),
            (-3.40, 1, 0, 'Thêm kho thành công', False),
        ]),
    ]),
]

draw_sequence_diagram('Sequence Diagram: Thêm kho', actors5, messages5, alt5,
                      'sequence_them_kho.png', height=3.8)

# ==================== 6. Quản lý trạng thái kho ====================
actors6 = ['Người dùng', 'Giao diện\nkho', 'Kho\nController', 'Database']

messages6 = [
    (-0.30, 0, 1, 'Chọn kho cần thay đổi', False),
    (-0.50, 1, 0, 'Hiển thị trạng thái hiện tại', False),
    (-0.70, 0, 1, 'Chọn trạng thái mới', False),
    (-0.90, 0, 1, 'Nhấn "Cập nhật trạng thái"', False),
    (-1.10, 1, 2, 'capNhatTrangThaiKho()', False),
]

alt6 = [
    (-1.25, -2.85, 'alt', [
        (-1.25, -2.05, '[Đóng/Tạm dừng có hàng hóa]', [
            (-1.85, 2, 3, 'Kiểm tra hàng hóa trong kho', False),
            (-2.05, 3, 2, 'Có hàng hóa', True),
            (-2.25, 2, 1, 'Kho có hàng, vui lòng chuyển hàng', False),
        ]),
        (-2.15, -2.85, '[Cập nhật thành công]', [
            (-2.45, 2, 3, 'Cập nhật trạng thái kho', False),
            (-2.65, 3, 2, 'Cập nhật thành công', True),
            (-2.85, 2, 1, 'Cập nhật trạng thái thành công', False),
            (-3.05, 1, 0, 'Cập nhật trạng thái thành công', False),
        ]),
    ]),
]

draw_sequence_diagram('Sequence Diagram: Quản lý trạng thái kho', actors6, messages6, alt6,
                      'sequence_quan_ly_trang_thai_kho.png', height=3.8)
