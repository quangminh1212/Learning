# Audit — Báo cáo tổng hợp Nhóm 1 vs. mẫu Nhóm 2 (read-only)

**Artifact (Group 1):** `01. Bài tập nhóm/Nhóm 1/Bài làm/bao_cao_tong_hop_latex/output/docx/bao_cao_tong_hop_nhom_1.docx` + `output/pdf/bao_cao_tong_hop_nhom_1.pdf`
**Reference (Group 2 template):** `02. Mẫu/Nhóm 2/0.BaoCaoTongHop-HRMS-QTDA.docx`
**Method:** OOXML package inspection (python-docx + raw `document.xml`), `pdftotext -layout` page-by-page diff. No files edited.

## Baseline facts

| | Group 1 | Group 2 (mẫu) |
|---|---|---|
| Paragraphs / Tables / Drawings | 154 / 22 / 4 | 169 / 15 / 0 |
| TOC | literal text, no field, no page nos. | `TOC \o "1-2" \h \z \u` + 29 `PAGEREF` |
| `fldChar` begin/sep/end | 0 / 0 / 0 | 30 / 30 / 30 |
| `bookmarkStart` / `hyperlink` | 0 / 0 | 28 / 29 |
| `sectPr` (sections) | 1 | 1 |
| Page breaks (`w:br type=page`) | 2 | 1 |
| PDF pages | 20 | (n/a, docx only) |
| Bảng / Hình | 19 / 3 | 13 / 0 |

Section 1–12 structure matches the template 1:1, and Group 1 legitimately adds §12.1.
No paragraph carries `keep_with_next`. Trailing empty page 21 in the PDF.

---

## S1 — TOC has no page numbers and no navigation (Severity: HIGH)

Group 1's TOC is hand-typed `[Normal]` text, not a field. The `document.xml` contains
`fldChar begin=0 separate=0 end=0`, `instrText` count 0, `bookmarkStart` 0, `hyperlink` 0.
The template has `TOC \o "1-2" \h \z \u` + 29 `PAGEREF` + 29 `hyperlink` + 28 bookmarks.

Consequence, visible in the PDF: page 2 renders only the right-hand dot leaders for the
longer headings — the page digit is pushed off the printable width. Measured on PDF p.2,
the entries **missing their page number entirely** are:

- `1. TÊN DỰ ÁN VÀ NHÓM THỰC HIỆN` (nested-dot row 5)
- `2.1. Bối cảnh`, `2.2. Mục tiêu và ý nghĩa`, `2.3. Yêu cầu và phạm vi`, `2.4. Các bên liên quan`
- `3. TÍNH KHẢ THI CỦA DỰ ÁN`, `4. CÁC CHỨC NĂNG CỦA DỰ ÁN`, `4.1. Các luồng nghiệp vụ trọng tâm`
- `5. NGUỒN NHÂN LỰC CỦA DỰ ÁN`, `7. KINH PHÍ DỰ ÁN`
- `8. QUẢN LÝ CHẤT LƯỢNG VÀ RỦI RO`, `8.1. Quản lý chất lượng`, `8.2. Quản lý rủi ro`
- `9.6. Bảng thuật ngữ`
- `10. KẾT QUẢ THỰC HIỆN DỰ ÁN`
- `11.1. Khó khăn gặp phải`, `11.2. Tự đánh giá kết quả`, `11.3. Bài học kinh nghiệm`
- `12. KẾT LUẬN`

Only some entries (`9.1`–`9.5`, `6.`, `11.`, `12.1.`, `TÀI LIỆU THAM KHẢO`, `DANH MỤC…`) happen
to keep a digit. This is a subset of 22 of 30 entries — the defect is layout-driven, not
content-driven.

Additionally: because there are no bookmarks, **reviewers cannot ctrl-click the TOC**, and any
edit reflows page numbers silently with no way to refresh them.

---

## S2 — Every table caption sits ABOVE its table (contradicts template + own convention) (Severity: HIGH)

Body-order inspection shows all 19 captions precede the table they label. Verified cases
(`PREV` = element immediately before the table):

```
TABLE 9x2  'Nội dung'    PREV: Table Caption 'Bảng 1. Thông tin chung của dự án'
TABLE 6x3  'Thành viên'  PREV: Table Caption 'Bảng 2. Thành viên và trách nhiệm chính'
TABLE 6x2  'Trong phạm vi' PREV: Table Caption 'Bảng 3. Phạm vi trong và ngoài dự án'
TABLE 5x3  'Danh mục'    PREV: Table Caption 'Bảng 13. Cơ cấu kinh phí dự án'
```

The template places captions **below**: `Bảng 1. Thông tin chung (PL1)` follows its table,
`Bảng 4. Các module…`, `Bảng 5…`, `Bảng 8…`, `Bảng 12…` all follow theirs. Group 1's own
`Bảng 1`/`Bảng 2` are the exception that proves the rule is broken inconsistently within the
document. In the PDF this is visible on p.3, p.10, p.11: caption line, then table.

---

## S3 — Figure captions use the wrong style, size and alignment; figures are unnumbered in flow (Severity: HIGH)

`Bảng` captions are `[Table Caption]`, CENTER, 11 pt italic. `Hình` captions are:

```
77 [Normal] align=JUSTIFY :: 'Hình 1. Mô hình lĩnh vực của hệ thống'  runs italic sz=13.0
79 [Normal] align=JUSTIFY :: 'Hình 2. Lược đồ cơ sở dữ liệu'          runs italic sz=13.0
116 [Normal] align=JUSTIFY :: 'Hình 3. Thiết kế triển khai đề xuất'    runs italic sz=13.0
```

Three distinct faults: wrong style (`Normal`, not `Caption`/`Table Caption`), wrong size
(13 pt vs 11 pt — a visible 18 % mismatch), and wrong alignment (`JUSTIFY` left-aligns a
centered figure; the template centers all captions).

There is also **no numbered figure list**. The template's TOC covers `1-2`; Group 1's TOC
covers `1-2` too but the document uses `Heading 1`/`Heading 2` only, so figures can never
enter the TOC even if the field were generated. Combined with S1, a reader has no way to
locate Hình 1–3 other than scrolling.

---

## S4 — Figure/heading collisions on PDF pages 9 and 17 (Severity: HIGH)

`Hình 1` and `Hình 2` both render on **page 9, whose body is otherwise empty** — just the two
caption lines and the page footer:

```
p9: 16 lines -> 'Hình 1. Mô hình lĩnh vực của hệ thống'
                 'Hình 2. Lược đồ cơ sở dữ liệu'
                 9
```

From p.10 onward the header regains `Nhóm 1`; on **p.2 and p.9 the header is truncated**
(`…kho bãi - Nhóm` / `Nhóm 1`) — a field-width overflow in `header1.xml`.

Worse, on **page 17** `Hình 3` is injected *inside* §9.6's glossary table flow:

```
Thẻ kho
Baseline  Lịch sử biến động số lượng của biến thể tại từng
          kho.
          Đường cơ sở đã được duyệt để so sánh và kiểm soát
          thay đổi.
   Hình 3. Thiết kế triển khai đề xuất      <-- collides, then
10. KẾT QUẢ THỰC HIỆN DỰ ÁN                   <-- Heading 1
```

The glossary's right-hand column continues *below* the figure caption, so `Hình 3` is not a
caption for a figure — it is interleaved into the table. This is a missing page break plus a
missing `keep_with_next` on the glossary table, and it orphans §10's heading against the
figure caption.

---

## S5 — Glossary table is badly broken across the page 16→17 boundary (Severity: HIGH)

The §9.6 glossary (`Bảng 12`, 11×2) splits so that **terms and definitions are separated by a
full page turn**. PDF p.16 ends with:

```
Thẻ kho
Baseline  Lịch sử biến động...
```

and p.17 restarts the header row `Thuật ngữ | Ý nghĩa`, then renders:

```
  Thẻ kho
Baseline  Lịch sử biến động số lượng của biến thể tại tầng
          kho.
```

`Thẻ kho` is emitted with **no definition** on both pages, while `Baseline`'s definition is
split. The term/definition pairing that exists in the DOCX (row 9 `Thẻ kho` → "Lịch sử biến
động số lượng của biến thể tại từng kho.", row 10 `Baseline` → "Đường cơ sở đã được duyệt…")
is destroyed in the PDF. Compare the template: `Bảng 12` glossary renders as a 4-column
`Từ viết tắt | Nghĩa đơn giản | Từ viết tắt | Nghĩa đơn giản` layout specifically to avoid
this tall-thin-table split.

---

## S6 — `Bảng 12. Các mốc kiểm soát` is destroyed by a page break (Severity: HIGH)

PDF **page 12** shows the trailing rows of `Bảng 11` (Khối lượng chốt) colliding with the
header of `Bảng 12`:

```
        Giai đoạn     Manday chốt     Diễn giải
            Tổng
                 221,83       Tổng khối lượng trong bảng tổng
        Mốc                   hợp WBS.
M1 - Chốt yêu cầu
M2 - Chốt phân tích  Bảng 12. Các mốc kiểm soát
        thiết kế     Thời điểm     Điều kiện đạt    Người phê duyệt
M3 - Chốt CSDL và
                     25/09/2026    Đặc tả yêu cầu được xác Bùi Tuấn Anh và đại
        giao diện                   nhận.                    diện doanh nghiệp.
```

The first column of `Bảng 12` (`M1`–`M3` milestone names) is **transposed out of its column
and interleaved with `Bảng 11`'s `Tổng` row**, so the "Người phê duyệt" cell of M1
(`Bùi Tuấn Anh và đại diện doanh nghiệp`) is orphaned onto its own visual band. The DOCX has
this table correct (6 milestones, 4 columns); the PDF layout is unreadable for the first three
milestones. Root cause is again the absent `keep_with_next`/`cantSplit` on caption + header row.

---

## S7 — `Bảng 10` overflows the page width (Severity: MEDIUM)

On PDF **p.11** the 5th column of `Bảng 10. Lịch biểu, sản phẩm và cột mốc theo giai đoạn`
(7×5) is clipped — the header prints as `Sản phẩm và ni` (truncated `…nội dung`) and the
header row's remaining cells are emitted as **whitespace-only runs**:

```
   Mã Giai đoạn Thời gian Task Sản phẩm và ni
                                       <-- header cells run off
   A Kho sát và yêu 01/09/2026 - 1-8   Báo cáo khảo sát, …
```

The `Thời gian` column also wraps onto a second line (`-` / `25/09/2026`) for giai đoạn A,
indicating the column widths are wrong for A4 portrait. Note this is the table whose content
was flagged in §6; the rendering defect is independent of content.

---

## S8 — Conflicting page-number reporting in the TOC (Severity: MEDIUM)

The TOC digits that *are* present disagree with the actual PDF pages:

| TOC entry | TOC says | actual PDF page |
|---|---|---|
| `1. TÊN DỰ ÁN…` | 3 | 3 ✓ |
| `2. MỤC TIÊU…` | 4 | 3 ✗ |
| `2.1 Bối cảnh` | 4 | 3 ✗ |
| `4.1. Các luồng…` | 8 | 8 ✓ |
| `6. THỜI GIAN…` | 10 | 10 ✓ |
| `7. KINH PHÍ` | 12 | 12 ✓ |
| `8. QUẢN LÝ CHẤT LƯỢNG…` | 13 | 13 ✓ |
| `9.6. Bảng thuật ngữ` | 16 | 16 ✓ |
| `12.1 Hạn chế` | 20 | 20 ✓ |
| `TÀI LIỆU THAM KHẢO` | 20 | 20 ✓ |

`§2` and `§2.1` are off by one (+1). Because there is no TOC field (S1), these numbers are
frozen text and were never re-derived after the §2.1 page break moved. Mixed correct/incorrect
entries are the tell-tale of a hand-copied TOC.

---

## S9 — Section 9.6 heading has no body text in the DOCX (Severity: LOW)

`114 [Heading 2] 9.6. Bảng thuật ngữ` is followed immediately by the glossary table with no
introductory sentence, whereas every other sub-section (§8.1, §8.2, §9.1–§9.5) opens with a
paragraph. The template has one (`'Bảng dưới giải thích ngắn gọn các từ viết tắt đã dùng
trong báo cáo.'`). Minor, but it makes §9.6 read as an abandoned stub.

---

## S10 — Page-1 title block: table without header row rendering (Severity: MEDIUM)

PDF p.1 shows the cover table emitting its header row (`Vai trò | Họ và tên - MSSV`) and then
five member rows. There is **no `Giảng viên hướng dẫn` / `Hà Nội` separation** from the table,
and the §"Mã số đề tài" line sits above the table while `Hà Nội, tháng 9 năm 2026` sits below
it, straddling the table. The template separates these with `----- ◆ & ◆ -----` and a distinct
title block. Cosmetic but visible on the first page a grader sees.

---

## Summary by severity

| ID | Defect | Severity | Evidence |
|---|---|---|---|
| S1 | TOC is not a field; no page nos. (22/30 entries), no bookmarks/hyperlinks | HIGH | `fldChar=0`, `pdftotext` p.2 |
| S2 | All 19 captions ABOVE tables; template and own convention = below | HIGH | body-order dump |
| S3 | `Hình` captions `Normal`/13 pt/JUSTIFY vs `Bảng` `Table Caption`/11 pt/CENTER | HIGH | run-level dump |
| S4 | Figure/heading collision; `Hình 3` inside §9.6 table | HIGH | PDF p.9, p.17 |
| S5 | Glossary split across p.16→17; `Thẻ kho` orphaned, `Baseline` definition severed | HIGH | PDF p.16–17 |
| S6 | `Bảng 12` header transposed into `Bảng 11`'s trailing row | HIGH | PDF p.12 |
| S7 | `Bảng 10` column 5 clipped, header cells empty | MEDIUM | PDF p.11 |
| S8 | TOC page digits wrong for §2/§2.1 (+1) | MEDIUM | PDF p.2 vs p.3 |
| S9 | §9.6 heading with no introductory paragraph | LOW | paragraph dump |
| S10 | Cover block header/date straddle the member table | MEDIUM | PDF p.1 |

**Root cause grouping:** S1/S2/S3/S9 are authoring-style defects in the DOCX (conversion from
LaTeX/HTML left a literal TOC and inconsistent caption styles). S4/S5/S6/S7/S8/S10 are pagination
defects that manifest only in the PDF — all traceable to the total absence of
`keep_with_next` and `w:cantSplit`, plus one missing page break before §9.6's table.
Fixing S1 and adding `keep_with_next` to caption paragraphs + `cantSplit` to table rows would
resolve or reduce S2, S4, S5, S6, and S8 at once.

**Style-consistency note:** Group 1's caption formatting is internally inconsistent — this is
the single highest-leverage fix, because it is what a grader sees on every page.
