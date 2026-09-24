# Checklist cấu trúc & định dạng — Báo cáo tổng hợp Nhóm 1

**Đối tượng kiểm:** `bao_cao_tong_hop_nhom_1.docx`
**Mốc tham chiếu:** `C:\Users\GHC\Downloads\Báo cáo tổng hợp.docx`
**Phương pháp:** trích xuất read-only bằng `python-docx` + đọc raw OOXML (`word/document.xml`, `numbering.xml`, `styles.xml`). Không sửa/tạo/xóa file, không chạy lệnh Git.

> **Phát hiện nền tảng, quan trọng nhất:** Hai file **trùng khớp 100% về nội dung văn bản** (294 paragraph, 29 bảng, 8 ảnh, cùng 13 H1 / 37 H2 / 8 H3, cùng 4 section-property, cùng toàn bộ chú thích Bảng/Hình, cùng danh sách nguồn tài liệu). Khác biệt **duy nhất** nằm ở ba nhóm: (1) khối bìa/front-matter, (2) cơ chế mục lục, (3) cơ chế đánh số danh sách. Vì vậy checklist dưới đây **không phải** là "Nhóm 1 thiếu nội dung" — mà là **các lỗi hình thức/kỹ thuật cục bộ** trong file của Nhóm 1.

---

## A. Mục lục / Chương / Mục

| # | Hạng mục | Tham chiếu | Nhóm 1 | Đánh giá |
|---|---|---|---|---|
| A1 | Có mục "Mục lục" (H1) | ✅ | ✅ | **Đạt** |
| A2 | Số chương & thứ tự chương | 13 H1 | 13 H1 | **Đạt — giống hệt** |
| A3 | Số mục cấp 2 | 37 H2 | 37 H2 | **Đạt — giống hệt** |
| A4 | Số mục cấp 3 | 8 H3 | 8 H3 | **Đạt — giống hệt** |
| A5 | Thụt lề phân cấp trong mục lục | cấp 1 `indL=0`, cấp 2 `indL=215900` | giống hệt | **Đạt** |
| A6 | **Thụt dòng đầu mục lục** | `firstLineIndent = 360045` (≈0.63cm) trên **mọi** dòng mục lục | **`None` — không có** | ⚠️ **LỖI HÌNH THỨC — cần sửa** |
| A7 | **Mục lục là trường tự động (field code)** | ❌ không có TOC field | ❌ không có TOC field | **Cả hai đều tĩnh — xem ghi chú** |
| A8 | "Danh sách bảng" / "Danh sách hình" | ✅ H2, 26 bảng + 7 hình | ✅ giống hệt | **Đạt** |
| A9 | **Liên kết chéo trong thân bài** | `"…thành bốn gói như Bảng ."` — **số hiệu rỗng** | **y hệt lỗi** | ⚠️ **LỖI NỘI DUNG ở cả hai — cần sửa** |

**Ghi chú A7:** Cả hai file đều **không** dùng Word TOC field (`w:instrText` = rỗng). Mục lục là văn bản chép tay, **không có số trang**, không tự cập nhật. Nếu mốc tham chiếu được chấp nhận thì đây là **hợp lệ**; nhưng đây là **điểm yếu thật**: mục lục sẽ sai ngay khi nội dung co giãn. → **Khuyến nghị: bắt buộc về mặt kỹ thuật**, dùng `References ▸ Table of Contents` tự động.

**Ghi chú A9 — bắt buộc, không phải hình thức:** câu "Các yêu cầu được tổ chức thành bốn gói như **Bảng .**" bị mất số hiệu. Đúng phải là **Bảng 3.1**. Lỗi này có ở **cả hai** file → nếu chỉ sao chép mốc tham chiếu thì lỗi vẫn còn.

---

## B. Bảng biểu / Hình

| # | Hạng mục | Tham chiếu | Nhóm 1 | Đánh giá |
|---|---|---|---|---|
| B1 | Tổng số bảng | 29 | 29 | **Đạt** |
| B2 | Kích thước từng bảng (rows×cols) | 29/29 khớp | 29/29 khớp | **Đạt — giống hệt** |
| B3 | Tổng số hình nhúng | 8 | 8 | **Đạt** |
| B4 | Chú thích "Bảng x.y." đặt **trên** bảng | ✅ | ✅ | **Đạt** |
| B5 | Chú thích "Hình x.y." đặt **dưới** hình | ✅ | ✅ | **Đạt** |
| B6 | Số hiệu chú thích đúng chuỗi chương (1.1→9.1) | ✅ | ✅ | **Đạt** |
| B7 | Không nhảy số / không trùng số | ✅ | ✅ | **Đạt** |
| B8 | Đường viền bảng (`tblBorders`) | 29/29 | 29/29 | **Đạt** |
| B9 | Bố cục bảng cố định (`fixed`) | ✅ | ✅ | **Đạt** |
| B10 | Độ rộng bảng | `7086 dxa` | `7086 dxa` | **Đạt** |
| B11 | **Bảng dùng style có tên** | `tblStyle = Table1` (định danh) | **`tblStyle` rỗng** — không gán style | ⚠️ **LỖI KỸ THUẬT — nên sửa** (dùng `Table Grid`) |
| B12 | Định dạng chữ trong ô bảng | Times New Roman 14pt | Times New Roman 14pt | **Đạt** |
| B13 | Không dùng style `Caption` cho chú thích | dùng `normal` | dùng `Normal` | **Đạt (tương đương)** |

**Ghi chú B11:** Nhóm 1 mất thuộc tính `tblStyle`, chỉ còn viền trực tiếp. Về **hiển thị** hai file giống nhau, nên đây là **hình thức/kỹ thuật**; nhưng nếu Nhóm 2 yêu cầu "bảng phải áp style", đây là điểm trừ. **Không bắt buộc về nội dung.**

---

## C. Phụ lục

| # | Hạng mục | Tham chiếu | Nhóm 1 | Đánh giá |
|---|---|---|---|---|
| C1 | Có chương "Phụ lục" | ❌ | ❌ | **Nhất quán** |
| C2 | Có chương "Thuật ngữ chính" (thay phụ lục) | ✅ H1 | ✅ H1 | **Đạt** |
| C3 | Bảng thuật ngữ | Bảng 9.1 | Bảng 9.1 | **Đạt** |

**Ghi chú C1 — cân nhắc nội dung, không phải hình thức:** **Không** file nào có phụ lục. Nếu rubric của Nhóm 2 **bắt buộc** phụ lục (biểu mẫu gốc, WBS đầy đủ 52 task, từ điển dữ liệu 15 bảng), thì đây là **thiếu sót bắt buộc** mà mốc tham chiếu **cũng đang thiếu** — không thể "đối chiếu theo mẫu" để phát hiện, phải đọc rubric. Đây là **lỗ hổng lớn nhất** trong checklist này.

---

## D. Mở đầu — Kết luận — Tài liệu tham khảo

| # | Hạng mục | Tham chiếu | Nhóm 1 | Đánh giá |
|---|---|---|---|---|
| D1 | Chương "Tóm tắt" | ✅ H1, 3 đoạn | ✅ 3 đoạn giống hệt | **Đạt** |
| D2 | Chương "Phạm vi tổng hợp" | ✅ | ✅ | **Đạt** |
| D3 | Chương "Kết luận và giới hạn" | ✅ | ✅ | **Đạt** |
| D4 | 3 tiểu mục kết luận (Kết quả / Hạn chế / Hướng phát triển) | ✅ | ✅ | **Đạt** |
| D5 | "Nguồn tài liệu" (H1) | ✅ | ✅ | **Đạt** |
| D6 | Số nguồn liệt kê | 5 | 5 | **Đạt** |
| D7 | **Nguồn tài liệu liệt kê thô, thiếu chuẩn** | `1. Nhóm 1 - Báo cáo khảo sát.docx.` | y hệt | ⚠️ **LỖI HÌNH THỨC ở cả hai** |

**Ghi chú D7 — bắt buộc theo quy tắc học thuật:** danh mục hiện chỉ là tên file, **không có tác giả, năm, nhà xuất bản, URL**. Chuẩn phải là (ví dụ): *Nhóm 1. (2026). Báo cáo khảo sát hiện trạng. HUST.* Đây là lỗi **ở cả hai file** → phải sửa theo rubric, không thể copy.

---

## E. Quy tắc bố cục / định dạng (Nhóm 2)

| # | Hạng mục | Tham chiếu | Nhóm 1 | Đánh giá |
|---|---|---|---|---|
| E1 | Khổ giấy | A4 `11906×16838` portrait | **giống hệt** | **Đạt** |
| E2 | Lề trang chẵn (section 2 — thân bài) | L1701 R1247 T1417 B1417 | **giống hệt** | **Đạt** |
| E3 | **Lề trang bìa (section 1)** | L`425.1969` R`260.0787` (lề hẹp tùy biến) | L`1020` R`1020` | ⚠️ **KHÁC BIỆT HÌNH THỨC** |
| E4 | **Đánh số trang bắt đầu từ 1** | `w:pgNumType start="1"` **có khai báo** | **không khai báo** | ⚠️ **LỖI KỸ THUẬT — cần sửa** |
| E5 | Footer chứa trường PAGE | ✅ | ✅ | **Đạt** |
| E6 | Header | rỗng (cả hai) | rỗng | **Đạt** |
| E7 | Font chữ | Times New Roman toàn bộ | Times New Roman toàn bộ | **Đạt** |
| E8 | Cỡ chữ H1 / H2 / H3 | 19 / 16 / 14 pt, **đậm** | 19 / 16 / 14 pt, **đậm** | **Đạt** |
| E9 | Màu chữ tiêu đề | `#000000` | `#000000` | **Đạt** |
| E10 | Cỡ chữ thân bài | 14pt (qua run) | 14pt (**qua style Normal**) | **Đạt (tương đương)** |
| E11 | Thụt dòng đầu đoạn thân bài | `firstLine = 360045` | `firstLine = 360045` | **Đạt** |
| E12 | Giãn dòng | single (1.0) | single (1.0) | **Đạt** |
| E13 | Khoảng cách sau đoạn | 50800 / 25400 | giống hệt | **Đạt** |
| E14 | Khối bìa — 4 dòng, canh giữa | 20/16/24/16pt đậm | giống hệt | **Đạt** |
| E15 | **Tên style thân bài** | `normal` (viết thường) | `Normal` | ⚠️ **Rủi ro tương thích** |
| E16 | **Quy tắc đánh số danh sách** | **`numPr` thật** (`numId=1`, `ilvl=0`) trên 19 đoạn | **`List Bullet` — 0 đoạn có `numPr`** | ⚠️ **LỖI NỘI DUNG/KỸ THUẬT** |
| E17 | Số `abstractNum` trong `numbering.xml` | 1 (sạch) | 9 (thừa, kế thừa template) | ⚠️ **Rác kỹ thuật** |
| E18 | `stylesWithEffects.xml` | ❌ không có | ✅ **có (thừa)** | ⚠️ **Rác kỹ thuật** |
| E19 | `latentStyles` trong styles.xml | không có | **có** | ⚠️ **Rác kỹ thuật** |

**Ghi chú E3:** Lề bìa khác nhau (425/260 so với 1020/1020). Bìa vẫn canh giữa đúng ở cả hai → **thuần hình thức, ưu tiên thấp**. Chỉ cần đồng bộ nếu Nhóm 2 chấm khắt khe về "cùng template".

**Ghi chú E4 — cần sửa:** Tham chiếu khai báo tường minh `start="1"` cho section bìa để số trang được reset. Nhóm 1 **không khai báo** → nếu bìa dài hơn 1 trang, số trang ở thân bài **lệch** so với mốc. **Bắt buộc về kỹ thuật.**

**Ghi chú E16 — quan trọng nhất trong nhóm E:** Hai file **hiển thị giống nhau** nhưng **cơ chế khác nhau hoàn toàn**. Tham chiếu dùng **danh sách đánh số tự động thật** (`numPr`/`numId=1`) → 19 đoạn được Word tự đánh số, tự cập nhật. Nhóm 1 chỉ gán **style `List Bullet`** mà **không có `numPr`** → nhiều khả năng **hiển thị không có bullet**, phụ thuộc hoàn toàn vào định nghĩa style trong template. Nếu template Nhóm 2 định nghĩa `List Bullet` khác, kết quả sẽ **sai**. Đây là lỗi **kỹ thuật/nội dung**, không phải hình thức — **bắt buộc sửa**: dùng `numPr` tường minh hoặc `Bullets` chuẩn của Word.

**Ghi chú E15:** `normal` vs `Normal` — hai style id khác nhau trong hai template. Về hiển thị **không khác biệt**, nhưng là **rủi ro tương thích** khi trộn template. Ưu tiên thấp.

**Ghi chú E17–E19:** `numbering.xml` 9 abstractNum thay vì 1, cộng thêm `stylesWithEffects.xml` và `latentStyles` — đây là **rác kỹ thuật** do LaTeX→DOCX converter sinh ra, không ảnh hưởng hiển thị. **Thuần hình thức, ưu tiên thấp nhất.**

---

## Tổng hợp — Phân loại ưu tiên

### 🔴 BẮT BUỘC VỀ NỘI DUNG (phải sửa, không thể bỏ qua)
1. **C1 — Thiếu phụ lục.** Kiểm tra rubric Nhóm 2: nếu bắt buộc phụ lục (52 task, 15 bảng dữ liệu, biểu mẫu gốc) thì **cả hai file đều vi phạm**. Không thể phát hiện bằng đối chiếu mẫu.
2. **E16 — Danh sách 19 mục không có `numPr`.** Tham chiếu dùng đánh số tự động thật; Nhóm 1 chỉ gán style `List Bullet` → rủi ro hiển thị sai/không có bullet. **Sửa bằng `numPr` tường minh.**
3. **A9 — Tham chiếu chéo hỏng:** `"như Bảng ."` → phải là **Bảng 3.1**. Lỗi ở **cả hai** file.
4. **D7 — Nguồn tài liệu thiếu chuẩn trích dẫn** (thiếu tác giả/năm/NXB). Lỗi ở **cả hai** file.

### 🟡 BẮT BUỘC VỀ KỸ THUẬT (gây sai kết quả khi in/xuất)
5. **E4 — Thiếu `pgNumType start="1"`** → số trang có thể lệch mốc.
6. **A6 — Mục lục thiếu `firstLineIndent = 360045`.**
7. **A7 — Mục lục không có số trang & không tự cập nhật.** Mốc tham chiếu cũng vậy, nhưng nên nâng cấp lên TOC field.

### 🟢 CHỈ LÀ HÌNH THỨC (ưu tiên thấp, không ảnh hưởng nội dung)
8. **B11 — Bảng thiếu `tblStyle`** (mất tên style, vẫn còn viền).
9. **E3 — Lề bìa khác** (425/260 so với 1020/1020); bìa vẫn canh giữa đúng.
10. **E15 — `normal` vs `Normal`** (khác id style, hiển thị giống nhau).
11. **E17–E19 — Rác kỹ thuật từ converter:** 9 abstractNum thay vì 1, `stylesWithEffects.xml`, `latentStyles`.

### ✅ ĐÃ ĐẠT — giống hệt mốc tham chiếu
Toàn bộ **13 H1 / 37 H2 / 8 H3**, **29 bảng** (đúng kích thước từng bảng), **8 hình**, **26 chú thích bảng + 7 chú thích hình** (đúng số hiệu, đúng vị trí trên/dưới), khổ A4, lề thân bài, font Times New Roman 19/16/14pt đậm cho tiêu đề, 14pt thân bài, thụt dòng đầu 360045, giãn dòng single, và **toàn bộ văn bản** (Tóm tắt → Kết luận → Thuật ngữ → Nguồn tài liệu).

---

## Kết luận (3 câu)

Nhóm 1 **không thiếu nội dung**: văn bản, 13 chương, 37 mục, 29 bảng và 8 hình trùng khớp 100% với mốc tham chiếu. Bốn điểm **bắt buộc về nội dung** cần xử lý (phụ lục, `numPr` cho danh sách, tham chiếu `Bảng 3.1`, chuẩn hoá trích dẫn) — trong đó **hai điểm (tham chiếu hỏng, trích dẫn thô) tồn tại ở cả file mốc**, nên đối chiếu mẫu đơn thuần sẽ bỏ sót. Ba điểm **kỹ thuật** (thiếu `start="1"`, thụt dòng mục lục, mục lục không tự động) và bốn điểm **thuần hình thức** (tblStyle, lề bìa, id style, rác converter) xếp sau.
