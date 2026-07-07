# Tài liệu yêu cầu dự án: Phân tích và thiết kế hệ thống quản lý kho hàng

> Tài liệu này tổng hợp yêu cầu cho đề tài **Phân tích và thiết kế hệ thống quản lý kho hàng**, dựa trên yêu cầu môn học Phân tích và thiết kế hệ thống (IT3120) và các tài liệu tham khảo trong thư mục `request`.

---

## 1. Tên đề tài

**Phân tích và thiết kế hệ thống quản lý kho hàng**

---

## 2. Bối cảnh và lý do chọn đề tài

Trong hoạt động kinh doanh và sản xuất, quản lý kho hàng là khâu trung tâm ảnh hưởng đến chi phí vận hành, khả năng đáp ứng đơn hàng và hiệu quả sử dụng vốn. Nhiều doanh nghiệp hiện nay vẫn quản lý kho bằng Excel/sổ sách, gây ra các vấn đề:

- Dữ liệu phân tán, khó tổng hợp và đối chiếu.
- Sai sót trong quá trình nhập/xuất, khó truy vết.
- Không cập nhật tồn kho theo thời gian thực.
- Báo cáo thủ công, chậm và thiếu chính xác.
- Khó kiểm soát hàng hết, hàng tồn lâu ngày, hàng hết hạn sử dụng.

Do đó, việc xây dựng một hệ thống thông tin quản lý kho hàng là cần thiết để số hóa quy trình, tăng tính minh bạch và hỗ trợ ra quyết định.

---

## 3. Mục tiêu đề tài

- Số hóa quy trình nhập kho, xuất kho, kiểm kê và điều chuyển kho.
- Quản lý tập trung thông tin hàng hóa, nhà cung cấp, khách hàng và kho.
- Cập nhật tồn kho tự động theo thời gian thực khi có phiếu nhập/xuất.
- Cảnh báo tồn kho thấp, tồn kho cao và hàng sắp hết hạn.
- Hỗ trợ báo cáo nhập xuất tồn, hàng bán chạy, hàng tồn lâu ngày.
- Phân quyền người dùng và ghi log thao tác để đảm bảo an toàn dữ liệu.

---

## 4. Phạm vi nghiên cứu

### 4.1. Phạm vi nghiệp vụ

Hệ thống tập trung vào các nghiệp vụ cốt lõi:

1. Quản lý danh mục hàng hóa, nhóm hàng, đơn vị tính.
2. Quản lý nhà cung cấp và khách hàng.
3. Quản lý phiếu nhập kho và chi tiết nhập kho.
4. Quản lý phiếu xuất kho và chi tiết xuất kho.
5. Quản lý điều chuyển hàng giữa các kho.
6. Quản lý tồn kho, kiểm kê định kỳ và điều chỉnh chênh lệch.
7. Quản lý người dùng, phân quyền và theo dõi lịch sử thao tác.
8. Báo cáo thống kê nhập xuất tồn.

### 4.2. Phạm vi đối tượng sử dụng

| Tác nhân | Vai trò chính |
|----------|---------------|
| Quản trị viên | Quản lý tài khoản, cấu hình hệ thống, sao lưu dữ liệu, phân quyền. |
| Quản lý kho | Giám sát tồn kho, phê duyệt phiếu nhập/xuất, xem báo cáo. |
| Nhân viên kho | Lập phiếu nhập/xuất, kiểm kê, cập nhật trạng thái hàng hóa. |
| Khách hàng | Tra cứu đơn hàng, lịch sử giao dịch (nếu được cấp quyền). |
| Nhà cung cấp | Theo dõi trạng thái đơn hàng nhập (nếu được cấp quyền). |

---

## 5. Các use case chính

### 5.1. Module Quản lý hàng hóa

- Thêm hàng hóa mới.
- Cập nhật thông tin hàng hóa.
- Xóa hàng hóa (logic hoặc vật lý).
- Tìm kiếm và lọc hàng hóa.
- Quản lý nhóm hàng và đơn vị tính.

### 5.2. Module Quản lý nhập kho

- Lập phiếu nhập kho.
- Duyệt phiếu nhập kho.
- Nhập hàng vào kho (cập nhật tồn).
- In phiếu nhập kho.
- Tra cứu lịch sử nhập kho.

### 5.3. Module Quản lý xuất kho

- Lập phiếu xuất kho.
- Duyệt phiếu xuất kho.
- Xuất hàng khỏi kho (giảm tồn).
- In phiếu xuất kho.
- Tra cứu lịch sử xuất kho.

### 5.4. Module Quản lý tồn kho

- Xem tồn kho theo kho và theo hàng hóa.
- Kiểm kê định kỳ.
- Điều chỉnh tồn kho sau kiểm kê.
- Cảnh báo tồn kho thấp/cao.
- Theo dõi hàng sắp hết hạn.

### 5.5. Module Quản lý người dùng

- Đăng nhập / đăng xuất.
- Quản lý tài khoản.
- Phân quyền theo vai trò.
- Ghi log thao tác.

### 5.6. Module Báo cáo

- Báo cáo nhập xuất tồn theo thời gian.
- Báo cáo hàng hóa tồn kho.
- Báo cáo hàng bán chạy / hàng tồn lâu ngày.
- Báo cáo giá trị tồn kho.

---

## 6. Yêu cầu phi chức năng

| STT | Yêu cầu | Mô tả |
|-----|---------|-------|
| 1 | Hiệu năng | Phản hồi các thao tác thường dưới 3 giây. |
| 2 | Bảo mật | Mã hóa mật khẩu, phân quyền rõ ràng, ghi log. |
| 3 | Khả dụng | Hệ thống hoạt động ổn định, sao lưu định kỳ. |
| 4 | Khả mở rộng | Dễ dàng bổ sung kho, chi nhánh, loại hàng hóa. |
| 5 | Giao diện | Thân thiện, hỗ trợ tiếng Việt, responsive. |
| 6 | Tính nhất quán | Dữ liệu nhập/xuất được cập nhật đồng bộ tồn kho. |

---

## 7. Các sơ đồ UML cần thiết kế

Theo yêu cầu môn học, báo cáo cần bao gồm các sơ đồ sau:

1. **Sơ đồ use case tổng quát** và sơ đồ use case phân rã.
2. **Đặc tả use case** cho các use case chính: Đăng nhập, Nhập kho, Xuất kho, Kiểm kê.
3. **Sơ đồ hoạt động (Activity Diagram)** cho quy trình nhập kho và xuất kho.
4. **Sơ đồ lớp (Class Diagram)** mô tả các lớp và quan hệ.
5. **Sơ đồ trình tự (Sequence Diagram)** cho các luồng nhập kho, xuất kho.
6. **Sơ đồ quan hệ thực thể (ERD)** / thiết kế cơ sở dữ liệu.

---

## 8. Công nghệ đề xuất

| Thành phần | Đề xuất |
|------------|---------|
| Kiến trúc | Web Application / Cloud-based |
| Ngôn ngữ lập trình | Python / Java / C# |
| Framework | Django / Spring Boot / ASP.NET Core |
| Cơ sở dữ liệu | PostgreSQL / MySQL / SQL Server |
| Giao diện | HTML5, CSS3, JavaScript |
| Công cụ vẽ UML | TikZ + pgf-umlcd + pgf-umlsd trên LaTeX |

---

## 9. Cấu trúc báo cáo LaTeX dự kiến

```
BaoCao/
├── main.tex              # File chính, điều phối các chương
├── YeuCauDuAn.md         # Tài liệu yêu cầu dự án (file này)
├── chapters/
│   ├── chapter1.tex      # Tổng quan đề tài
│   ├── chapter2.tex      # Phân tích hệ thống
│   └── chapter3.tex      # Thiết kế hệ thống
└── diagrams/
    ├── usecase.tex       # Sơ đồ use case tổng quát
    ├── activity.tex      # Sơ đồ hoạt động
    ├── classdiagram.tex  # Sơ đồ lớp
    ├── sequence_nhapkho.tex
    └── sequence_xuatkho.tex
```

---

## 10. Tham khảo

- `request/PTTKHT.docx` – Bài tập lớn mẫu về quản lý du lịch.
- `request/Bai Tap Lon/IT3120-Phan-Tich-Thiet-Ke-He-Thong.xlsx` – Danh sách nhóm và đề tài.
- `request/TaiLieuMau/phanTichYeuCau_IT4421_V3.docx` – Mẫu tài liệu phân tích yêu cầu.
- `request/TaiLieuMau/moTaThietKePhanMem_IT4421_V2.docx` – Mẫu tài liệu mô tả thiết kế phần mềm.
- Các bài tập lớn của các nhóm khác trong thư mục `request/Bai Tap Lon/`.
