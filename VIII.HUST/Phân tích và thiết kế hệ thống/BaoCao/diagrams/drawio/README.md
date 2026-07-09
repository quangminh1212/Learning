# Draw.io diagrams — Báo cáo Quản lý kho hàng

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
