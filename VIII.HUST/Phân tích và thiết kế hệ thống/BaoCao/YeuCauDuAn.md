# Tài liệu yêu cầu dự án: Phân tích và thiết kế hệ thống quản lý kho hàng

> Đề tài **Phân tích và thiết kế hệ thống quản lý kho hàng** (IT3120).

---

## 1. Tên đề tài

**Phân tích và thiết kế hệ thống quản lý kho hàng**

---

## 2. Mục tiêu

- Số hóa nhập kho, xuất kho, kiểm kê.
- Quản lý hàng hóa, NCC, khách hàng, kho.
- Cập nhật tồn kho khi duyệt phiếu nhập/xuất.
- Phân quyền người dùng, ghi log.

---

## 3. Phạm vi

Xác thực, tài khoản, đối tác, hàng hóa, kho, phiếu nhập/xuất.

---

## 4. Tác nhân

| Tác nhân | Vai trò |
|----------|---------|
| Quản trị viên | Thêm tài khoản, phân quyền |
| Quản lý kho | Duyệt phiếu, quản lý kho/hàng/đối tác |
| Nhân viên kho | Lập phiếu, thêm/tìm hàng, đối tác |

---

## 5. Use case (10 UC -- mỗi UC = một mục tiêu)

| Mã | Tên | Tác nhân |
|----|-----|----------|
| UC01 | Đăng nhập | Tất cả |
| UC02 | Đăng xuất | Tất cả |
| UC03 | Thêm tài khoản | QTV |
| UC04 | Thêm nhà cung cấp | NV, QL |
| UC05 | Thêm khách hàng | NV, QL |
| UC06 | Thêm hàng hóa | NV, QL |
| UC07 | Tìm kiếm hàng hóa | Có quyền |
| UC08 | Thêm kho | QL, QTV |
| UC09 | Lập phiếu nhập kho | NV (lập), QL (duyệt) |
| UC10 | Lập phiếu xuất kho | NV (lập), QL (duyệt) |

---

## 6. File Word

`BaoCao/BaoCao_QuanLyKhoHang.docx` -- file chính.
