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

## 5. Các use case chính (theo mục lục tham khảo)

| Mã | Tên use case | Mô tả ngắn |
|----|--------------|------------|
| UC01 | Quản lý tài khoản người dùng | Tạo, chỉnh sửa, khóa/mở tài khoản và phân quyền. |
| UC02 | Đăng nhập / Đăng xuất | Xác thực người dùng vào hệ thống. |
| UC03 | Quản lý nhà cung cấp | Thêm, sửa, xóa, tìm kiếm nhà cung cấp. |
| UC04 | Quản lý khách hàng | Thêm, sửa, xóa, tìm kiếm khách hàng. |
| UC05 | Quản lý hàng hóa | Thêm, cập nhật, tìm kiếm, phân loại hàng hóa. |
| UC06 | Tìm kiếm hàng hóa | Tra cứu hàng hóa theo nhiều tiêu chí. |
| UC07 | Quản lý kho | Tạo, cập nhật, tìm kiếm kho/thông tin kho. |
| UC08 | Tìm kiếm kho | Tra cứu thông tin kho. |
| UC09 | Lập phiếu nhập kho | Tạo phiếu nhập và cập nhật tồn kho. |
| UC10 | Lập phiếu xuất kho | Tạo phiếu xuất và giảm tồn kho. |
| UC11 | Quản lý đơn đặt hàng | Tạo, duyệt, theo dõi đơn đặt hàng từ khách hàng. |
| UC12 | Quản lý thanh toán | Ghi nhận, cập nhật chi phí/thanh toán liên quan. |
| UC13 | Xem báo cáo thống kê | Xem các báo cáo nhập xuất tồn, hàng bán chạy, tồn lâu. |

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

Theo yêu cầu môn học và mục lục tham khảo, báo cáo cần bao gồm các sơ đồ sau:

1. **Sơ đồ use case tổng quát** và sơ đồ use case phân rã.
2. **Đặc tả use case** cho các use case chính (UC01–UC13).
3. **Sơ đồ hoạt động (Activity Diagram)** cho các quy trình nhập kho, xuất kho, kiểm kê.
4. **Sơ đồ lớp (Class Diagram)** tổng thể và biểu đồ lớp trong ca sử dụng cho các UC chính.
5. **Sơ đồ trình tự (Sequence Diagram)** cho các luồng nhập kho, xuất kho, tìm kiếm hàng, quản lý tài khoản, ...
6. **Sơ đồ quan hệ thực thể (ERD)** / thiết kế cơ sở dữ liệu.
7. **Thiết kế giao diện (UI mockup)** cho các màn hình chính.

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

## 9. Mục lục báo cáo LaTeX theo ảnh tham khảo

| Chương | Nội dung |
|--------|----------|
| **Chương 1** | Khảo sát hiện trạng: Giới thiệu doanh nghiệp; Thực trạng quy trình quản lý hiện tại và các hạn chế; Mục tiêu của hệ thống. |
| **Chương 2** | Mô tả nghiệp vụ: Các nghiệp vụ nhập kho, xuất kho, kiểm kê, điều chuyển, quản lý hàng hóa, nhà cung cấp, khách hàng, báo cáo. |
| **Chương 3** | Phân tích chức năng: Use case tổng quát, use case phân rã, đặc tả use case. |
| **Chương 4** | Phân tích hành vi: Biểu đồ lớp tổng thể và biểu đồ lớp trong ca sử dụng cho các UC chính. |
| **Chương 5** | Phân tích tương tác: Biểu đồ trình tự (sequence) cho các ca sử dụng chính. |
| **Chương 6** | Thiết kế các lớp chi tiết: Bảng mô tả các lớp; Bảng mô tả quan hệ. |
| **Chương 7** | Thiết kế cơ sở dữ liệu: Mô hình quan hệ tổng thể; Đặc tả các bảng; Thiết kế giao diện. |

---

## 10. Cấu trúc thư mục LaTeX dự kiến

```
BaoCao/
├── main.tex                # File chính, điều phối các chương
├── YeuCauDuAn.md           # Tài liệu yêu cầu dự án (file này)
├── chapters/
│   ├── chapter1_khao_sat_hien_trang.tex          # Khảo sát hiện trạng
│   ├── chapter2_mo_ta_nghiep_vu.tex              # Mô tả nghiệp vụ
│   ├── chapter3_phan_tich_chuc_nang.tex         # Phân tích chức năng
│   ├── chapter4_phan_tich_hanh_vi.tex            # Phân tích hành vi (class diagrams)
│   ├── chapter5_phan_tich_tuong_tac.tex           # Phân tích tương tác (sequence diagrams)
│   ├── chapter6_thiet_ke_lop_chi_tiet.tex         # Thiết kế các lớp chi tiết
│   └── chapter7_thiet_ke_csdl_va_giao_dien.tex  # Thiết kế CSDL và giao diện
└── diagrams/
    ├── bfd.tex                 # Sơ đồ phân cấp chức năng (BFD)
    ├── dfd_context.tex         # DFD cấp 0 (Context Diagram)
    ├── dfd_level1.tex          # DFD cấp 1
    ├── usecase.tex             # Use case tổng quát
    ├── activity_nhapkho.tex
    ├── activity_xuatkho.tex
    ├── activity_kiemke.tex
    ├── classdiagram.tex        # Class diagram tổng thể
    ├── class_uc05.tex          # Class diagram trong ca sử dụng UC05
    ├── class_uc09.tex          # Class diagram trong ca sử dụng UC09
    ├── class_uc10.tex          # Class diagram trong ca sử dụng UC10
    ├── sequence_uc05.tex       # Sequence quản lý hàng hóa
    ├── sequence_uc09.tex       # Sequence nhập kho
    ├── sequence_uc10.tex       # Sequence xuất kho
    ├── sequence_uc06.tex       # Sequence tìm kiếm hàng hóa
    ├── state_phieu_nhap.tex      # State Machine phiếu nhập kho
    ├── state_phieu_xuat.tex      # State Machine phiếu xuất kho
    ├── component.tex            # Component Diagram
    └── erd.tex                  # Sơ đồ ERD
```

---

## 11. Xuất file Word

Báo cáo được xuất sang định dạng Word để nộp và chỉnh sửa thuận tiện:

- `BaoCao_QuanLyKhoHang_Editable.docx` – File Word từ nội dung LaTeX, văn bản rõ ràng, dễ chỉnh sửa (chưa bao gồm các hình vẽ TikZ).
- `BaoCao_QuanLyKhoHang_Full.docx` – File Word chuyển từ PDF, đầy đủ văn bản và hình ảnh/biểu đồ (do chuyển từ PDF nên văn bản có thể bị dính ký tự, phù hợp để xem và in).

---

## 12. Tham khảo

- Các ảnh mục lục trong `request/image/` – mục lục báo cáo tham khảo từ đề tài tương tự.
- `request/PTTKHT.docx` – Bài tập lớn mẫu về quản lý du lịch.
- `request/Bai Tap Lon/IT3120-Phan-Tich-Thiet-Ke-He-Thong.xlsx` – Danh sách nhóm và đề tài.
- `request/TaiLieuMau/phanTichYeuCau_IT4421_V3.docx` – Mẫu tài liệu phân tích yêu cầu.
- `request/TaiLieuMau/moTaThietKePhanMem_IT4421_V2.docx` – Mẫu tài liệu mô tả thiết kế phần mềm.
- Các bài tập lớn của các nhóm khác trong thư mục `request/Bai Tap Lon/`.
