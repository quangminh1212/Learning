import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Ellipse, FancyBboxPatch, FancyArrowPatch

# Create figure
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# System boundary
system_box = FancyBboxPatch((4.5, 0.5), 9, 9, boxstyle="round,pad=0.1", 
                             linewidth=2, edgecolor='black', facecolor='none', linestyle='--')
ax.add_patch(system_box)
ax.text(9, 9.7, 'Hệ thống Quản lý Kho', fontsize=14, fontweight='bold', ha='center')

# Actor positions
actors = {
    'Quản trị viên': (1.5, 7.5),
    'Quản lý kho': (1.5, 4.5),
    'Nhân viên kho': (1.5, 1.5)
}

# Draw actors as stick figures
for name, (x, y) in actors.items():
    # Head
    head = plt.Circle((x, y + 1.2), 0.3, color='white', ec='black', linewidth=1.5)
    ax.add_patch(head)
    # Body
    ax.plot([x, x], [y + 0.9, y + 0.2], 'k-', linewidth=1.5)
    # Arms
    ax.plot([x - 0.3, x + 0.3], [y + 0.6, y + 0.6], 'k-', linewidth=1.5)
    # Legs
    ax.plot([x, x - 0.3], [y + 0.2, y - 0.2], 'k-', linewidth=1.5)
    ax.plot([x, x + 0.3], [y + 0.2, y - 0.2], 'k-', linewidth=1.5)
    # Label
    ax.text(x, y - 0.6, name, fontsize=10, ha='center', fontweight='bold')

# Use cases for Supplier Management
supplier_uses = [
    'Thêm nhà cung cấp',
    'Sửa nhà cung cấp',
    'Tìm kiếm nhà cung cấp',
    'Xóa nhà cung cấp'
]

# Use cases for Warehouse Management
warehouse_uses = [
    'Thêm kho',
    'Sửa thông tin kho',
    'Quản lý trạng thái kho',
    'Xóa kho',
    'Xem chi tiết kho'
]

# Draw use cases
use_case_positions = {}
start_y = 8.2
for i, uc in enumerate(supplier_uses):
    y = start_y - i * 1.1
    x = 7.5
    ellipse = Ellipse((x, y), 3.5, 0.7, color='#90EE90', ec='black', linewidth=1.5)
    ax.add_patch(ellipse)
    ax.text(x, y, uc, fontsize=9, ha='center', va='center')
    use_case_positions[uc] = (x, y)

start_y = 4.5
for i, uc in enumerate(warehouse_uses):
    y = start_y - i * 1.0
    x = 11.5
    ellipse = Ellipse((x, y), 3.5, 0.7, color='#90EE90', ec='black', linewidth=1.5)
    ax.add_patch(ellipse)
    ax.text(x, y, uc, fontsize=9, ha='center', va='center')
    use_case_positions[uc] = (x, y)

# Connections
admin_pos = actors['Quản trị viên']
manager_pos = actors['Quản lý kho']
staff_pos = actors['Nhân viên kho']

# Admin connections
for uc in supplier_uses + warehouse_uses:
    x1, y1 = admin_pos
    x2, y2 = use_case_positions[uc]
    ax.plot([x1 + 0.3, x2 - 1.75], [y1 + 1.2, y2], 'k-', linewidth=1)

# Manager connections
for uc in ['Tìm kiếm nhà cung cấp', 'Sửa thông tin kho', 'Quản lý trạng thái kho', 'Xem chi tiết kho']:
    x1, y1 = manager_pos
    x2, y2 = use_case_positions[uc]
    ax.plot([x1 + 0.3, x2 - 1.75], [y1 + 1.2, y2], 'k-', linewidth=1)

# Staff connections
for uc in ['Tìm kiếm nhà cung cấp', 'Xem chi tiết kho']:
    x1, y1 = staff_pos
    x2, y2 = use_case_positions[uc]
    ax.plot([x1 + 0.3, x2 - 1.75], [y1 + 1.2, y2], 'k-', linewidth=1)

# Include relationships (dashed)
ax.plot([use_case_positions['Sửa nhà cung cấp'][0], use_case_positions['Tìm kiếm nhà cung cấp'][0]],
        [use_case_positions['Sửa nhà cung cấp'][1], use_case_positions['Tìm kiếm nhà cung cấp'][1]],
        'k--', linewidth=1)
ax.text((use_case_positions['Sửa nhà cung cấp'][0] + use_case_positions['Tìm kiếm nhà cung cấp'][0]) / 2,
        (use_case_positions['Sửa nhà cung cấp'][1] + use_case_positions['Tìm kiếm nhà cung cấp'][1]) / 2 + 0.15,
        '<<include>>', fontsize=7, ha='center', style='italic')

ax.plot([use_case_positions['Sửa thông tin kho'][0], use_case_positions['Xem chi tiết kho'][0]],
        [use_case_positions['Sửa thông tin kho'][1], use_case_positions['Xem chi tiết kho'][1]],
        'k--', linewidth=1)
ax.text((use_case_positions['Sửa thông tin kho'][0] + use_case_positions['Xem chi tiết kho'][0]) / 2,
        (use_case_positions['Sửa thông tin kho'][1] + use_case_positions['Xem chi tiết kho'][1]) / 2 + 0.15,
        '<<include>>', fontsize=7, ha='center', style='italic')

plt.tight_layout()
plt.savefig('use_case_diagram.png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()
print('Diagram saved as use_case_diagram.png')
