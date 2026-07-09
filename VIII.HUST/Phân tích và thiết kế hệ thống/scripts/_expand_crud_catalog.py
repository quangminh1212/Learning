# -*- coding: utf-8 -*-
"""Expand HangHoa/Kho/PhieuNhap/PhieuXuat to full CRUD+search+list; remove KhachHang."""
from pathlib import Path

BASE = Path(r"C:\Dev\Learning\VIII.HUST\Phân tích và thiết kế hệ thống\BaoCao")
CH = BASE / "chapters"
DG = BASE / "diagrams" / "tex"


def crud_ops(prefix, codes, entity, actors="NV, QL", notes=None):
    """codes = (them, sua, xoa, tim, xem)"""
    t, s, x, f, v = codes
    note_xoa = (notes or {}).get("xoa", "Nếu đã có phiếu liên quan thì không xóa cứng, chỉ ngừng/khóa.")
    note_sua = (notes or {}).get("sua", "")
    blocks = []

    blocks.append(rf"""
\subsection{{{t} -- Thêm {entity}}}

\begin{{itemize}}[leftmargin=1.5cm]
    \item \textbf{{Tên use case}}: Thêm {entity}.
    \item \textbf{{Mã}}: {t}.
    \item \textbf{{Tác nhân chính}}: {actors}.
    \item \textbf{{Mô tả tóm tắt}}: Bổ sung bản ghi {entity} mới vào hệ thống.
    \item \textbf{{Mục tiêu}}: Lưu được bản ghi mới, dùng được ở các chức năng liên quan.
    \item \textbf{{Điều kiện trước}}: Actor đã đăng nhập với quyền phù hợp.
    \item \textbf{{Điều kiện sau}}: Có bản ghi mới trong CSDL; xuất hiện trên danh sách.
    \item \textbf{{Luồng sự kiện chính}}:
    \begin{{enumerate}}
        \item Actor mở màn hình quản lý (từ {v} xem danh sách).
        \item Chọn ``Thêm mới'', nhập thông tin bắt buộc, nhấn ``Lưu''.
        \item Hệ thống kiểm tra hợp lệ / không trùng khóa.
        \item Lưu CSDL, thông báo thành công, làm mới danh sách.
    \end{{enumerate}}
    \item \textbf{{Luồng thay thế}}: Trùng mã / thiếu trường $\rightarrow$ báo lỗi, không lưu.
\end{{itemize}}
""")

    blocks.append(rf"""
\subsection{{{s} -- Sửa {entity}}}

\begin{{itemize}}[leftmargin=1.5cm]
    \item \textbf{{Tên use case}}: Sửa {entity}.
    \item \textbf{{Mã}}: {s}.
    \item \textbf{{Tác nhân chính}}: {actors}.
    \item \textbf{{Mô tả tóm tắt}}: Cập nhật thông tin bản ghi đã có.
    \item \textbf{{Mục tiêu}}: Dữ liệu phản ánh đúng thông tin mới nhất.
    \item \textbf{{Điều kiện trước}}: Đã có bản ghi (chọn từ {v} hoặc {f}). {note_sua}
    \item \textbf{{Điều kiện sau}}: Bản ghi được cập nhật; khóa định danh thường không đổi.
    \item \textbf{{Luồng sự kiện chính}}:
    \begin{{enumerate}}
        \item Chọn bản ghi $\rightarrow$ ``Sửa'' $\rightarrow$ nạp form.
        \item Chỉnh các trường cho phép $\rightarrow$ ``Lưu''.
        \item Hệ thống validate và cập nhật CSDL.
    \end{{enumerate}}
    \item \textbf{{Luồng thay thế}}: Hủy / dữ liệu không hợp lệ $\rightarrow$ không lưu.
\end{{itemize}}
""")

    blocks.append(rf"""
\subsection{{{x} -- Xóa {entity}}}

\begin{{itemize}}[leftmargin=1.5cm]
    \item \textbf{{Tên use case}}: Xóa {entity}.
    \item \textbf{{Mã}}: {x}.
    \item \textbf{{Tác nhân chính}}: {actors}.
    \item \textbf{{Mô tả tóm tắt}}: Gỡ bản ghi khỏi danh mục đang dùng.
    \item \textbf{{Mục tiêu}}: Bản ghi không còn dùng cho thao tác mới (đã xóa hoặc đã ngừng).
    \item \textbf{{Điều kiện trước}}: Đã chọn một bản ghi.
    \item \textbf{{Điều kiện sau}}: Xóa cứng \textbf{{hoặc}} chuyển trạng thái ngừng/khóa.
    \item \textbf{{Luồng sự kiện chính}}:
    \begin{{enumerate}}
        \item Chọn bản ghi $\rightarrow$ ``Xóa'' $\rightarrow$ xác nhận.
        \item Hệ thống kiểm tra ràng buộc tham chiếu.
        \item {note_xoa}
    \end{{enumerate}}
    \item \textbf{{Luồng thay thế}}: Hủy xác nhận $\rightarrow$ không đổi dữ liệu.
\end{{itemize}}
""")

    blocks.append(rf"""
\subsection{{{f} -- Tìm kiếm {entity}}}

\begin{{itemize}}[leftmargin=1.5cm]
    \item \textbf{{Tên use case}}: Tìm kiếm {entity}.
    \item \textbf{{Mã}}: {f}.
    \item \textbf{{Tác nhân chính}}: {actors}.
    \item \textbf{{Mô tả tóm tắt}}: Lọc nhanh theo mã/tên (hoặc điều kiện liên quan).
    \item \textbf{{Mục tiêu}}: Nhận danh sách khớp điều kiện.
    \item \textbf{{Điều kiện trước}}: Actor đã đăng nhập.
    \item \textbf{{Điều kiện sau}}: Hiển thị kết quả; không bắt buộc đổi dữ liệu.
    \item \textbf{{Luồng sự kiện chính}}:
    \begin{{enumerate}}
        \item Nhập từ khóa / bộ lọc $\rightarrow$ ``Tìm kiếm''.
        \item Hệ thống truy vấn và hiển thị kết quả.
        \item Có thể chọn dòng để sửa ({s}) / xóa ({x}).
    \end{{enumerate}}
    \item \textbf{{Luồng thay thế}}: Không có kết quả $\rightarrow$ thông báo trống.
\end{{itemize}}
""")

    blocks.append(rf"""
\subsection{{{v} -- Xem danh sách {entity}}}

\begin{{itemize}}[leftmargin=1.5cm]
    \item \textbf{{Tên use case}}: Xem danh sách {entity}.
    \item \textbf{{Mã}}: {v}.
    \item \textbf{{Tác nhân chính}}: {actors}.
    \item \textbf{{Mô tả tóm tắt}}: Mở màn hình quản lý và xem toàn bộ (hoặc phân trang) danh sách -- điểm vào trước khi thêm/sửa/xóa/tìm.
    \item \textbf{{Mục tiêu}}: Nhìn được danh mục hiện tại.
    \item \textbf{{Điều kiện trước}}: Actor đã đăng nhập.
    \item \textbf{{Điều kiện sau}}: Danh sách hiển thị; có thể sang {t}/{s}/{x}/{f}.
    \item \textbf{{Luồng sự kiện chính}}:
    \begin{{enumerate}}
        \item Chọn menu quản lý $\rightarrow$ hệ thống tải danh sách.
        \item Hiển thị bảng (phân trang nếu nhiều).
        \item Từ danh sách chọn Thêm / Sửa / Xóa / Tìm.
    \end{{enumerate}}
    \item \textbf{{Ghi chú}}: Xem danh sách $\neq$ Tìm kiếm (mặc định toàn bộ vs lọc theo từ khóa).
\end{{itemize}}
""")
    return "\n".join(blocks)


def phieu_specs(kind, codes, actors="NV (lập), QL (duyệt)"):
    t, s, x, f, v = codes
    name = f"phiếu {kind}"
    extra_them = ""
    if kind == "nhập":
        extra_them = r"""
        \item Chọn NCC, kho nhập, ngày; thêm dòng hàng (SL, đơn giá).
        \item Gửi duyệt; QL duyệt $\rightarrow$ \textbf{tăng} tồn; từ chối $\rightarrow$ tồn không đổi."""
        xoa_note = "Chỉ xóa/hủy khi trạng thái Chờ duyệt hoặc Từ chối; phiếu Đã duyệt không xóa cứng."
        sua_note = "Chỉ sửa khi phiếu còn ``Chờ duyệt'' (hoặc nháp)."
    else:
        extra_them = r"""
        \item Chọn kho xuất, ngày, lý do xuất / ghi chú người nhận (không quản lý danh mục khách hàng).
        \item Thêm dòng hàng; hệ thống \textbf{kiểm tra tồn đủ}. Gửi duyệt; QL duyệt $\rightarrow$ \textbf{giảm} tồn."""
        xoa_note = "Chỉ xóa/hủy khi Chờ duyệt hoặc Từ chối; phiếu Đã duyệt không xóa cứng."
        sua_note = "Chỉ sửa khi phiếu còn ``Chờ duyệt'' (hoặc nháp)."

    return rf"""
\subsection{{{t} -- Lập {name}}}

\begin{{itemize}}[leftmargin=1.5cm]
    \item \textbf{{Tên use case}}: Lập {name}.
    \item \textbf{{Mã}}: {t}.
    \item \textbf{{Tác nhân}}: {actors}.
    \item \textbf{{Mô tả tóm tắt}}: Tạo phiếu mới, thêm chi tiết hàng, gửi duyệt; duyệt mới cập nhật tồn.
    \item \textbf{{Mục tiêu}}: Có phiếu hợp lệ; sau duyệt tồn phản ánh đúng.
    \item \textbf{{Điều kiện trước}}: Đã đăng nhập; đã có kho, hàng (và NCC nếu nhập).
    \item \textbf{{Luồng sự kiện chính}}:
    \begin{{enumerate}}
        \item NV chọn lập {name} (từ {v}).
        {extra_them}
    \end{{enumerate}}
    \item \textbf{{Luồng thay thế}}: Thiếu dòng hàng / tồn không đủ (xuất) / QL từ chối.
\end{{itemize}}

\subsection{{{s} -- Sửa {name}}}

\begin{{itemize}}[leftmargin=1.5cm]
    \item \textbf{{Tên use case}}: Sửa {name}.
    \item \textbf{{Mã}}: {s}.
    \item \textbf{{Tác nhân chính}}: NV, QL.
    \item \textbf{{Mô tả tóm tắt}}: Chỉnh header/chi tiết phiếu khi chưa duyệt.
    \item \textbf{{Điều kiện trước}}: {sua_note}
    \item \textbf{{Luồng sự kiện chính}}: Chọn phiếu $\rightarrow$ Sửa $\rightarrow$ lưu; trạng thái vẫn Chờ duyệt (hoặc nháp).
    \item \textbf{{Luồng thay thế}}: Phiếu Đã duyệt $\rightarrow$ không cho sửa (phải lập phiếu điều chỉnh / kiểm kê nếu cần).
\end{{itemize}}

\subsection{{{x} -- Xóa {name}}}

\begin{{itemize}}[leftmargin=1.5cm]
    \item \textbf{{Tên use case}}: Xóa {name}.
    \item \textbf{{Mã}}: {x}.
    \item \textbf{{Tác nhân chính}}: NV, QL.
    \item \textbf{{Mô tả tóm tắt}}: Hủy/xóa phiếu không còn dùng.
    \item \textbf{{Điều kiện sau}}: Phiếu bị xóa hoặc ``Đã hủy''; tồn không đổi (vì chưa duyệt hoặc đã từ chối).
    \item \textbf{{Luồng sự kiện chính}}: Chọn phiếu $\rightarrow$ Xóa/Hủy $\rightarrow$ xác nhận. {xoa_note}
\end{{itemize}}

\subsection{{{f} -- Tìm kiếm {name}}}

\begin{{itemize}}[leftmargin=1.5cm]
    \item \textbf{{Tên use case}}: Tìm kiếm {name}.
    \item \textbf{{Mã}}: {f}.
    \item \textbf{{Tác nhân chính}}: NV, QL.
    \item \textbf{{Mô tả tóm tắt}}: Lọc phiếu theo mã, ngày, kho, trạng thái{', NCC' if kind=='nhập' else ''}.
    \item \textbf{{Luồng sự kiện chính}}: Nhập điều kiện $\rightarrow$ tìm $\rightarrow$ danh sách kết quả $\rightarrow$ mở chi tiết / sửa / xóa nếu được phép.
\end{{itemize}}

\subsection{{{v} -- Xem danh sách {name}}}

\begin{{itemize}}[leftmargin=1.5cm]
    \item \textbf{{Tên use case}}: Xem danh sách {name}.
    \item \textbf{{Mã}}: {v}.
    \item \textbf{{Tác nhân chính}}: NV, QL.
    \item \textbf{{Mô tả tóm tắt}}: Xem danh sách phiếu (phân trang), điểm vào lập/sửa/xóa/tìm/duyệt.
    \item \textbf{{Luồng sự kiện chính}}: Mở menu phiếu $\rightarrow$ tải danh sách $\rightarrow$ chọn thao tác tiếp ({t}/{s}/{x}/{f} hoặc duyệt trên phiếu chờ).
\end{{itemize}}
"""


# --- Chapter 2 partial rewrite: from overview table through business sections ---
CH2_MID = r"""
\begin{longtable}{|p{4.2cm}|p{8.8cm}|}
\hline
\textbf{Nghiệp vụ} & \textbf{Use case tiêu biểu (Ch.3)} \\
\hline
\endfirsthead
\hline
\textbf{Nghiệp vụ} & \textbf{Use case tiêu biểu (Ch.3)} \\
\hline
\endhead
Quản lý tài khoản & UC03--UC07: Thêm/Sửa/Xóa/Tìm/Xem DS \\
\hline
Quản lý nhà cung cấp & UC08--UC12: Thêm/Sửa/Xóa/Tìm/Xem DS \\
\hline
Quản lý hàng hóa & UC13--UC17: Thêm/Sửa/Xóa/Tìm/Xem DS \\
\hline
Quản lý kho & UC18--UC22: Thêm/Sửa/Xóa/Tìm/Xem DS \\
\hline
Nhập kho & UC23--UC27: Lập/Sửa/Xóa/Tìm/Xem DS phiếu nhập \\
\hline
Xuất kho & UC28--UC32: Lập/Sửa/Xóa/Tìm/Xem DS phiếu xuất \\
\hline
Kiểm kê & UC33 Lập phiếu kiểm kê \\
\hline
Báo cáo tồn kho & UC34 Xem báo cáo nhập xuất tồn \\
\hline
\end{longtable}

\noindent\textit{Chức năng hệ thống (không phải nghiệp vụ)}: Đăng nhập (UC01), Đăng xuất (UC02). \textbf{Không} quản lý danh mục khách hàng trong phạm vi hệ thống.

\section{Nghiệp vụ 1: Quản lý tài khoản}

\textbf{Mô tả}: Quản trị viên duy trì tài khoản, gán vai trò (QTV, QL kho, NV kho). Tách thành năm mục tiêu: thêm, sửa, xóa, tìm, xem danh sách.

\textbf{Người thực hiện}: Quản trị viên.

\textbf{Các thao tác}:
\begin{enumerate}[leftmargin=1.5cm]
    \item \textbf{Xem DS (UC07)}, \textbf{Tìm (UC06)}, \textbf{Thêm (UC03)}, \textbf{Sửa (UC04)}, \textbf{Xóa/khóa (UC05)}.
\end{enumerate}

\textbf{Dữ liệu}: \texttt{NguoiDung}. \textbf{Use case}: UC03--UC07.

\section{Nghiệp vụ 2: Quản lý nhà cung cấp}

\textbf{Mô tả}: Danh mục NCC phục vụ phiếu nhập. Đủ năm thao tác (không gộp một UC ``Quản lý NCC'').

\textbf{Người thực hiện}: NV kho, QL kho.

\textbf{Các thao tác}: UC12 Xem DS; UC11 Tìm; UC08 Thêm; UC09 Sửa; UC10 Xóa (đã có phiếu nhập $\rightarrow$ chỉ ngừng).

\textbf{Dữ liệu}: \texttt{NhaCungCap}. \textbf{Use case}: UC08--UC12.

\section{Nghiệp vụ 3: Quản lý hàng hóa}

\textbf{Mô tả}: Danh mục hàng (mã, tên, nhóm, ĐVT, giá, trạng thái) -- trung tâm hệ thống. Khi \textbf{thêm} hàng, khởi tạo \texttt{TonKho}=0 các kho. \textbf{Sửa} thông tin/giá; \textbf{xóa}/ngừng nếu đã có phiếu; \textbf{tìm} và \textbf{xem DS}.

\textbf{Người thực hiện}: NV kho, QL kho.

\textbf{Các thao tác (mỗi thao tác = một use case)}:
\begin{enumerate}[leftmargin=1.5cm]
    \item \textbf{Xem DS hàng (UC17)}; \textbf{Tìm (UC16)}; \textbf{Thêm (UC13)} (+ khởi tạo tồn); \textbf{Sửa (UC14)}; \textbf{Xóa/ngừng (UC15)}.
\end{enumerate}

\textbf{Dữ liệu}: \texttt{HangHoa}, \texttt{NhomHangHoa}, \texttt{DonViTinh}, \texttt{TonKho}. \textbf{Use case}: UC13--UC17.

\section{Nghiệp vụ 4: Quản lý kho}

\textbf{Mô tả}: Nhiều kho (mã, tên, địa chỉ, phụ trách, trạng thái). Tồn theo cặp (kho, hàng). Đủ thêm/sửa/xóa/tìm/xem DS.

\textbf{Người thực hiện}: QL kho, QTV.

\textbf{Các thao tác}: UC22 Xem DS; UC21 Tìm; UC18 Thêm; UC19 Sửa; UC20 Xóa/ngừng (đã có tồn/phiếu $\rightarrow$ chỉ ngừng).

\textbf{Dữ liệu}: \texttt{Kho}, \texttt{TonKho}. \textbf{Use case}: UC18--UC22.

\section{Nghiệp vụ 5: Nhập kho}

\textbf{Mô tả}: Lập phiếu nhập (NCC, kho, dòng hàng); gửi duyệt; QL duyệt mới \textbf{tăng tồn}. Ngoài lập còn sửa/xóa (khi chưa duyệt), tìm và xem danh sách phiếu.

\textbf{Người thực hiện}: NV (lập/sửa); QL (duyệt).

\textbf{Các thao tác}:
\begin{enumerate}[leftmargin=1.5cm]
    \item \textbf{Xem DS phiếu nhập (UC27)}; \textbf{Tìm (UC26)}; \textbf{Lập (UC23)} gồm gửi duyệt + duyệt; \textbf{Sửa (UC24)} khi Chờ duyệt; \textbf{Xóa/hủy (UC25)} khi chưa duyệt.
\end{enumerate}

\textbf{Dữ liệu}: \texttt{PhieuNhapKho}, \texttt{ChiTietPhieuNhap}, \texttt{TonKho}, \texttt{NhaCungCap}, \texttt{Kho}, \texttt{HangHoa}. \textbf{Use case}: UC23--UC27.

\section{Nghiệp vụ 6: Xuất kho}

\textbf{Mô tả}: Lập phiếu xuất từ kho (lý do xuất / ghi chú người nhận -- \textbf{không} quản lý danh mục khách hàng). Kiểm tra tồn đủ; duyệt mới \textbf{giảm tồn}. Đủ lập/sửa/xóa/tìm/xem DS.

\textbf{Người thực hiện}: NV (lập/sửa); QL (duyệt).

\textbf{Các thao tác}: UC32 Xem DS; UC31 Tìm; UC28 Lập (+ duyệt); UC29 Sửa (Chờ duyệt); UC30 Xóa/hủy (chưa duyệt).

\textbf{Dữ liệu}: \texttt{PhieuXuatKho}, \texttt{ChiTietPhieuXuat}, \texttt{TonKho}, \texttt{Kho}, \texttt{HangHoa}. \textbf{Use case}: UC28--UC32.

\section{Nghiệp vụ 7: Kiểm kê tồn kho}

\textbf{Mô tả}: Đối chiếu tồn thực tế với sổ; duyệt điều chỉnh \texttt{TonKho}.

\textbf{Người thực hiện}: NV (lập); QL (duyệt).

\textbf{Use case tiêu biểu}: UC33 Lập phiếu kiểm kê.

\section{Nghiệp vụ 8: Báo cáo nhập -- xuất -- tồn}

\textbf{Mô tả}: Xem tồn và tổng hợp nhập--xuất--tồn theo kỳ/kho/hàng.

\textbf{Người thực hiện}: QL, QTV.

\textbf{Use case tiêu biểu}: UC34 Xem báo cáo nhập xuất tồn.

\section{Kết luận chương}

\section{Biểu đồ hoạt động (theo nghiệp vụ chính)}

Biểu đồ hoạt động minh họa luồng thực hiện các nghiệp vụ nhập, xuất, kiểm kê (trước khi vào 3 giai đoạn phân tích UML).

\subsection{Nghiệp vụ nhập kho}
\input{diagrams/tex/2.1_activity_nhapkho}

Giải thích sơ đồ: Biểu đồ hoạt động mô tả luồng \textbf{nhập kho} từ lúc bắt đầu đến kết thúc. Các hình chữ nhật là bước xử lý (lập phiếu, nhập NCC/kho, thêm chi tiết hàng). Hình thoi là điểm quyết định: (1) dữ liệu phiếu có hợp lệ không -- nếu không thì báo lỗi và quay lại nhập; (2) quản lý có duyệt không -- nếu duyệt thì cập nhật tồn kho và in/lưu phiếu, nếu từ chối thì thông báo và có thể lập lại. Mũi tên thể hiện thứ tự thực hiện; nhánh ``Không'' quay vòng để sửa sai trước khi đi tiếp.
"""


def patch_chapter2():
    p = CH / "chapter2_mo_ta_nghiep_vu.tex"
    text = p.read_text(encoding="utf-8")
    # Replace from longtable of business mapping through first activity explanation start of xuất
    start = text.index("\\begin{longtable}{|p{4.2cm}|p{8.8cm}|}")
    # Find "###{Nghiệp vụ xuất kho}" after activity nhập
    marker = "\\subsection{Nghiệp vụ xuất kho}"
    end = text.index(marker)
    # Also fix overview sentence
    text = text[:start] + CH2_MID + "\n" + text[end:]
    # Fix xuất section content (remove KH)
    text = text.replace(
        "Khi xuất hàng cho khách hàng hoặc sử dụng nội bộ, nhân viên lập \\textbf{phiếu xuất kho}. Hệ thống \\textbf{kiểm tra tồn đủ} trước khi cho phép thêm dòng hàng. Sau khi quản lý duyệt, tồn kho được \\textbf{giảm} tương ứng.",
        "Khi xuất hàng (bán, sản xuất, nội bộ\\ldots), nhân viên lập \\textbf{phiếu xuất kho}. Ghi nhận kho xuất, lý do/ghi chú người nhận -- \\textbf{không} dùng danh mục khách hàng. Hệ thống \\textbf{kiểm tra tồn đủ}; sau khi QL duyệt, tồn được \\textbf{giảm}.",
    )
    text = text.replace(
        "\\item Nhân viên kho chọn lập phiếu xuất: chọn khách hàng, kho xuất, ngày xuất, lý do xuất.",
        "\\item Nhân viên kho chọn lập phiếu xuất: chọn kho xuất, ngày xuất, lý do xuất / ghi chú người nhận.",
    )
    text = text.replace(
        "\\textbf{Dữ liệu liên quan}: \\texttt{PhieuXuatKho}, \\texttt{ChiTietPhieuXuat}, \\texttt{TonKho}, \\texttt{KhachHang}, \\texttt{Kho}, \\texttt{HangHoa}, \\texttt{LichSuThaoTac}.",
        "\\textbf{Dữ liệu liên quan}: \\texttt{PhieuXuatKho}, \\texttt{ChiTietPhieuXuat}, \\texttt{TonKho}, \\texttt{Kho}, \\texttt{HangHoa}, \\texttt{LichSuThaoTac}.",
    )
    text = text.replace(
        "\\textbf{Use case tiêu biểu}: UC18 Lập phiếu xuất kho (lập + duyệt).",
        "\\textbf{Use case}: UC28--UC32 (Lập/Sửa/Xóa/Tìm/Xem DS phiếu xuất).",
    )
    text = text.replace(
        "\\textbf{Use case tiêu biểu}: UC19 Lập phiếu kiểm kê.",
        "\\textbf{Use case tiêu biểu}: UC33 Lập phiếu kiểm kê.",
    )
    text = text.replace(
        "\\textbf{Use case tiêu biểu}: UC20 Xem báo cáo nhập xuất tồn.",
        "\\textbf{Use case tiêu biểu}: UC34 Xem báo cáo nhập xuất tồn.",
    )
    # Fix overview line
    text = text.replace(
        "Hệ thống phục vụ các nghiệp vụ \\textbf{cốt lõi của kho}: danh mục (tài khoản nội bộ, đối tác, hàng, kho), nhập/xuất, kiểm kê và theo dõi tồn. Bảng ánh xạ sang use case tiêu biểu:",
        "Hệ thống phục vụ nghiệp vụ kho: danh mục (tài khoản, NCC, hàng, kho), nhập/xuất, kiểm kê, báo cáo tồn. Mỗi danh mục/phiếu tách đủ Thêm/Sửa/Xóa/Tìm/Xem DS. \\textbf{Không} có module khách hàng. Bảng ánh xạ:",
    )
    p.write_text(text, encoding="utf-8")
    print("OK chapter2")


def build_chapter3_specs_tail():
    """From UC13 onward (after UC12 NCC), full specs."""
    parts = []
    parts.append(crud_ops(
        "Hàng hóa",
        ("UC13", "UC14", "UC15", "UC16", "UC17"),
        "hàng hóa",
        "NV, QL",
        {"xoa": "Nếu chưa có phiếu: xóa/ngừng; nếu đã có phiếu nhập/xuất: chỉ đánh dấu ngừng sử dụng.",
         "sua": "Có thể sửa tên, giá, nhóm, mô tả; mã hàng thường cố định."},
    ))
    # Override UC13 thêm with ton kho note - already generic OK

    parts.append(crud_ops(
        "Kho",
        ("UC18", "UC19", "UC20", "UC21", "UC22"),
        "kho",
        "QL, QTV",
        {"xoa": "Nếu kho đã có tồn/phiếu: không xóa cứng, chỉ ngừng hoạt động."},
    ))
    parts.append(phieu_specs("nhập", ("UC23", "UC24", "UC25", "UC26", "UC27")))
    parts.append(phieu_specs("xuất", ("UC28", "UC29", "UC30", "UC31", "UC32")))

    parts.append(r"""
\subsection{UC33 -- Lập phiếu kiểm kê}

\begin{itemize}[leftmargin=1.5cm]
    \item \textbf{Tên use case}: Lập phiếu kiểm kê.
    \item \textbf{Mã}: UC33.
    \item \textbf{Tác nhân}: NV (lập), QL (duyệt).
    \item \textbf{Mô tả tóm tắt}: Nhập số lượng thực tế theo kho; duyệt thì gán \texttt{TonKho} = thực tế.
    \item \textbf{Luồng chính}: Chọn kho $\rightarrow$ nạp SL sổ $\rightarrow$ nhập SL thực tế $\rightarrow$ gửi duyệt $\rightarrow$ QL duyệt $\rightarrow$ cập nhật tồn.
\end{itemize}

\subsection{UC34 -- Xem báo cáo nhập xuất tồn}

\begin{itemize}[leftmargin=1.5cm]
    \item \textbf{Tên use case}: Xem báo cáo nhập xuất tồn.
    \item \textbf{Mã}: UC34.
    \item \textbf{Tác nhân}: QL, QTV.
    \item \textbf{Mô tả tóm tắt}: Xem tồn hiện tại hoặc tổng hợp nhập--xuất--tồn theo kỳ/kho/hàng; có thể xuất Excel.
\end{itemize}
""")
    return "\n".join(parts)


def patch_chapter3():
    p = CH / "chapter3_phan_tich_chuc_nang.tex"
    text = p.read_text(encoding="utf-8")

    # Actors
    text = text.replace(
        "Nhân viên kho & Lập phiếu nhập, xuất, kiểm kê; CRUD + tìm/xem DS nhà cung cấp; thêm/tìm hàng hóa; thêm khách hàng. \\\\",
        "Nhân viên kho & Lập/sửa/xóa/tìm/xem phiếu nhập--xuất--kiểm kê; CRUD+tìm/xem DS NCC, hàng hóa. \\\\",
    )
    text = text.replace(
        "Quản lý kho & Duyệt phiếu nhập/xuất/kiểm kê; quản lý danh mục hàng, đối tác, kho; xem báo cáo. \\\\",
        "Quản lý kho & Duyệt phiếu; quản lý NCC, hàng, kho (đủ thêm/sửa/xóa/tìm/xem); xem báo cáo. \\\\",
    )

    # Overview explanation
    text = text.replace(
        "nhóm chức năng mức tổng quát (Đăng nhập/Đăng xuất, Quản lý tài khoản, NCC, KH, hàng hóa, kho, nhập, xuất, kiểm kê, báo cáo tồn)",
        "nhóm chức năng mức tổng quát (Đăng nhập/Đăng xuất, Quản lý tài khoản, NCC, hàng hóa, kho, nhập, xuất, kiểm kê, báo cáo tồn -- \\textbf{không} có khách hàng)",
    )

    # Partner explanation
    text = text.replace(
        "Giải thích sơ đồ: Nhóm nhà cung cấp được \\textbf{phân rã đủ năm mục tiêu}: \\textbf{UC08 Thêm}, \\textbf{UC09 Sửa}, \\textbf{UC10 Xóa}, \\textbf{UC11 Tìm kiếm}, \\textbf{UC12 Xem danh sách NCC} -- minh họa rõ nguyên tắc ``mỗi hành động là một use case'', không gộp thành một oval ``Quản lý NCC''. Bên cạnh đó có \\textbf{UC13 Thêm khách hàng} (mức độ tương tự có thể mở rộng CRUD KH nếu cần). Cả Nhân viên kho và Quản lý kho đều nối tới các UC này vì cả hai vai trò được phép thao tác danh mục đối tác.",
        "Giải thích sơ đồ: Nhóm NCC phân rã đủ năm mục tiêu \\textbf{UC08--UC12} (Thêm/Sửa/Xóa/Tìm/Xem DS). \\textbf{Không} có use case khách hàng. NV và QL đều nối các UC NCC.",
    )

    # Item explanation
    text = text.replace(
        "Giải thích sơ đồ: Ba use case: \\textbf{UC14 Thêm hàng hóa}, \\textbf{UC15 Tìm kiếm hàng hóa} (NV và QL đều dùng), \\textbf{UC16 Thêm kho} (chủ yếu QL). Tách ``thêm'' và ``tìm'' hàng vì mục tiêu khác nhau (ghi nhận danh mục mới vs tra cứu tồn). Thêm kho thuộc nhóm danh mục kho, actor QL/QTV có quyền cao hơn NV ở thao tác này.",
        "Giải thích sơ đồ: Cột trái -- \\textbf{hàng hóa UC13--UC17} (Thêm/Sửa/Xóa/Tìm/Xem DS), NV+QL. Cột phải -- \\textbf{kho UC18--UC22} cùng năm thao tác, chủ yếu QL/QTV. Nguyên tắc: thêm được thì phải sửa/xóa/tìm/xem được.",
    )

    # Inventory explanation
    text = text.replace(
        "Giải thích sơ đồ: Bốn use case nghiệp vụ cốt lõi vận hành kho: \\textbf{UC17 Lập phiếu nhập}, \\textbf{UC18 Lập phiếu xuất}, \\textbf{UC19 Lập phiếu kiểm kê}, \\textbf{UC20 Xem báo cáo nhập xuất tồn}. NV nối tới UC17--UC19 (thao tác lập phiếu); QL nối cả bốn (duyệt + xem báo cáo). UC17--UC19 trong đặc tả có thêm actor phụ QL ở bước duyệt; sơ đồ thể hiện cả hai vai trò tham gia nhóm nhập/xuất/kiểm kê.",
        "Giải thích sơ đồ: \\textbf{Phiếu nhập UC23--UC27} và \\textbf{phiếu xuất UC28--UC32} mỗi nhóm đủ Lập/Sửa/Xóa/Tìm/Xem DS; thêm \\textbf{UC33 Kiểm kê}, \\textbf{UC34 Báo cáo}. NV thao tác lập/sửa phiếu; QL duyệt và xem báo cáo.",
    )

    # Replace UC table
    table = r"""
\begin{longtable}{|p{1.1cm}|p{4.8cm}|p{3.2cm}|p{3.5cm}|}
\hline
\textbf{Mã} & \textbf{Tên use case} & \textbf{Tác nhân} & \textbf{Nhóm} \\
\hline
\endfirsthead
\hline
\textbf{Mã} & \textbf{Tên use case} & \textbf{Tác nhân} & \textbf{Nhóm} \\
\hline
\endhead
UC01 & Đăng nhập & Tất cả & Hệ thống \\
\hline
UC02 & Đăng xuất & Tất cả & Hệ thống \\
\hline
UC03 & Thêm tài khoản & QTV & Tài khoản \\
\hline
UC04 & Sửa tài khoản & QTV & Tài khoản \\
\hline
UC05 & Xóa tài khoản & QTV & Tài khoản \\
\hline
UC06 & Tìm kiếm tài khoản & QTV & Tài khoản \\
\hline
UC07 & Xem danh sách tài khoản & QTV & Tài khoản \\
\hline
UC08 & Thêm nhà cung cấp & NV, QL & NCC \\
\hline
UC09 & Sửa nhà cung cấp & NV, QL & NCC \\
\hline
UC10 & Xóa nhà cung cấp & NV, QL & NCC \\
\hline
UC11 & Tìm kiếm nhà cung cấp & NV, QL & NCC \\
\hline
UC12 & Xem danh sách nhà cung cấp & NV, QL & NCC \\
\hline
UC13 & Thêm hàng hóa & NV, QL & Hàng hóa \\
\hline
UC14 & Sửa hàng hóa & NV, QL & Hàng hóa \\
\hline
UC15 & Xóa hàng hóa & NV, QL & Hàng hóa \\
\hline
UC16 & Tìm kiếm hàng hóa & NV, QL & Hàng hóa \\
\hline
UC17 & Xem danh sách hàng hóa & NV, QL & Hàng hóa \\
\hline
UC18 & Thêm kho & QL, QTV & Kho \\
\hline
UC19 & Sửa kho & QL, QTV & Kho \\
\hline
UC20 & Xóa kho & QL, QTV & Kho \\
\hline
UC21 & Tìm kiếm kho & QL, QTV & Kho \\
\hline
UC22 & Xem danh sách kho & QL, QTV & Kho \\
\hline
UC23 & Lập phiếu nhập kho & NV, QL & Nhập kho \\
\hline
UC24 & Sửa phiếu nhập kho & NV, QL & Nhập kho \\
\hline
UC25 & Xóa phiếu nhập kho & NV, QL & Nhập kho \\
\hline
UC26 & Tìm kiếm phiếu nhập & NV, QL & Nhập kho \\
\hline
UC27 & Xem danh sách phiếu nhập & NV, QL & Nhập kho \\
\hline
UC28 & Lập phiếu xuất kho & NV, QL & Xuất kho \\
\hline
UC29 & Sửa phiếu xuất kho & NV, QL & Xuất kho \\
\hline
UC30 & Xóa phiếu xuất kho & NV, QL & Xuất kho \\
\hline
UC31 & Tìm kiếm phiếu xuất & NV, QL & Xuất kho \\
\hline
UC32 & Xem danh sách phiếu xuất & NV, QL & Xuất kho \\
\hline
UC33 & Lập phiếu kiểm kê & NV, QL & Kiểm kê \\
\hline
UC34 & Xem báo cáo nhập xuất tồn & QL, QTV & Báo cáo \\
\hline
\end{longtable}
"""
    import re
    text = re.sub(
        r"\\begin\{longtable\}\{\|p\{1\.1cm\}\|p\{4\.8cm\}\|p\{3\.2cm\}\|p\{3\.5cm\}\|\}.*?\\end\{longtable\}",
        lambda m: table.strip(),
        text,
        count=1,
        flags=re.S,
    )

    # Cut from UC13 Thêm khách hàng to end of specs - find and replace
    # Keep UC01-UC12 specs, replace from UC13 onward
    idx = text.find("\\subsection{UC13 -- Thêm khách hàng}")
    if idx < 0:
        idx = text.find("\\subsection{UC13 --")
    if idx < 0:
        raise SystemExit("Cannot find UC13 section in chapter3")
    # Find end of file or last part - keep nothing after, append new specs
    # But there might be content after last UC - check
    text = text[:idx] + build_chapter3_specs_tail().lstrip() + "\n"

    # Fix UC13 them hang - enhance with ton kho in generic block is ok

    p.write_text(text, encoding="utf-8")
    print("OK chapter3")


def write_diagrams():
    (DG / "3.4_usecase.tex").write_text(r"""\begin{figure}[H]
\centering
\makebox[\textwidth][c]{%
\begin{tikzpicture}[
    scale=0.85, transform shape,
    actor/.style={circle, draw=black, fill=white, line width=0.8pt, minimum size=0.7cm},
    usecase/.style={ellipse, draw=black, fill=white, line width=0.55pt, minimum width=3.2cm, minimum height=0.65cm, font=\footnotesize, align=center},
    system/.style={rectangle, draw=black!50, dashed, fill=white, line width=0.4pt, inner sep=8pt, rounded corners=3pt}
]
\node[system, minimum width=12.5cm, minimum height=11.5cm] (system) at (0,0.2) {};
\node[font=\bfseries\small] at (0,5.5) {Hệ thống quản lý kho hàng};
\node[font=\scriptsize\itshape] at (0,4.95) {(use case tổng quát -- không có KH)};

\node[usecase] (g1) at (-3.4,3.8) {Đăng nhập / Đăng xuất};
\node[usecase] (g2) at (-3.4,2.5) {Quản lý tài khoản};
\node[usecase] (g3) at (-3.4,1.2) {Quản lý nhà cung cấp};
\node[usecase] (g5) at (-3.4,-0.1) {Quản lý hàng hóa};
\node[usecase] (g6) at (-3.4,-1.4) {Quản lý kho};

\node[usecase] (g7) at (3.4,3.8) {Nhập kho};
\node[usecase] (g8) at (3.4,2.5) {Xuất kho};
\node[usecase] (g9) at (3.4,1.2) {Kiểm kê};
\node[usecase] (g10) at (3.4,-0.1) {Báo cáo tồn kho};

\node[actor, label=below:{\scriptsize\bfseries Quản trị viên}] (admin) at (-7.4,2.0) {};
\node[actor, label=below:{\scriptsize\bfseries Quản lý kho}] (qlk) at (7.4,2.0) {};
\node[actor, label=below:{\scriptsize\bfseries Nhân viên kho}] (nvk) at (0,-3.2) {};

\draw (admin) -- (g1); \draw (admin) -- (g2); \draw (admin) -- (g6); \draw (admin) -- (g10);
\draw (qlk) -- (g1); \draw (qlk) -- (g3); \draw (qlk) -- (g5); \draw (qlk) -- (g6);
\draw (qlk) -- (g7); \draw (qlk) -- (g8); \draw (qlk) -- (g9); \draw (qlk) -- (g10);
\draw (nvk) -- (g1); \draw (nvk) -- (g3); \draw (nvk) -- (g5);
\draw (nvk) -- (g7); \draw (nvk) -- (g8); \draw (nvk) -- (g9);
\end{tikzpicture}}
\caption{Sơ đồ use case tổng quát (nhóm chức năng)}
\label{fig:usecase-tongquat}
\end{figure}
""", encoding="utf-8")

    (DG / "3.6_usecase_partner_management.tex").write_text(r"""\begin{figure}[H]
\centering
\makebox[\textwidth][c]{%
\begin{tikzpicture}[
    scale=0.85, transform shape,
    actor/.style={circle, draw=black, fill=white, line width=0.8pt, minimum size=0.7cm},
    usecase/.style={ellipse, draw=black, fill=white, line width=0.55pt, minimum width=3.6cm, minimum height=0.62cm, font=\scriptsize, align=center},
    system/.style={rectangle, draw=black!50, dashed, fill=white, line width=0.4pt, inner sep=8pt, rounded corners=3pt}
]
\node[system, minimum width=11cm, minimum height=9.5cm] (system) at (0,0.3) {};
\node[font=\bfseries\small] at (0,4.6) {Phân rã: Quản lý nhà cung cấp};

\node[usecase] (uc08) at (0,3.3) {UC08: Thêm NCC};
\node[usecase] (uc09) at (0,2.1) {UC09: Sửa NCC};
\node[usecase] (uc10) at (0,0.9) {UC10: Xóa NCC};
\node[usecase] (uc11) at (0,-0.3) {UC11: Tìm kiếm NCC};
\node[usecase] (uc12) at (0,-1.5) {UC12: Xem danh sách NCC};

\node[actor, label=below:{\scriptsize\bfseries Nhân viên kho}] (nvk) at (-6.2,0.8) {};
\node[actor, label=below:{\scriptsize\bfseries Quản lý kho}] (qlk) at (6.2,0.8) {};
\foreach \u in {uc08,uc09,uc10,uc11,uc12} { \draw (nvk) -- (\u); \draw (qlk) -- (\u); }
\end{tikzpicture}}
\caption{Use case phân rã -- NCC (Thêm/Sửa/Xóa/Tìm/Xem DS)}
\label{fig:usecase-partner-management}
\end{figure}
""", encoding="utf-8")

    (DG / "3.7_usecase_item_management.tex").write_text(r"""\begin{figure}[H]
\centering
\makebox[\textwidth][c]{%
\begin{tikzpicture}[
    scale=0.78, transform shape,
    actor/.style={circle, draw=black, fill=white, line width=0.8pt, minimum size=0.65cm},
    usecase/.style={ellipse, draw=black, fill=white, line width=0.5pt, minimum width=3.3cm, minimum height=0.55cm, font=\scriptsize, align=center},
    system/.style={rectangle, draw=black!50, dashed, fill=white, line width=0.4pt, inner sep=6pt, rounded corners=3pt}
]
\node[system, minimum width=14.5cm, minimum height=9.8cm] (system) at (0,0.2) {};
\node[font=\bfseries\small] at (0,4.7) {Phân rã: Hàng hóa \& Kho};

\node[font=\scriptsize\bfseries] at (-3.3,3.8) {Hàng hóa};
\node[usecase] (h13) at (-3.3,3.0) {UC13: Thêm hàng};
\node[usecase] (h14) at (-3.3,1.9) {UC14: Sửa hàng};
\node[usecase] (h15) at (-3.3,0.8) {UC15: Xóa hàng};
\node[usecase] (h16) at (-3.3,-0.3) {UC16: Tìm hàng};
\node[usecase] (h17) at (-3.3,-1.4) {UC17: Xem DS hàng};

\node[font=\scriptsize\bfseries] at (3.3,3.8) {Kho};
\node[usecase] (k18) at (3.3,3.0) {UC18: Thêm kho};
\node[usecase] (k19) at (3.3,1.9) {UC19: Sửa kho};
\node[usecase] (k20) at (3.3,0.8) {UC20: Xóa kho};
\node[usecase] (k21) at (3.3,-0.3) {UC21: Tìm kho};
\node[usecase] (k22) at (3.3,-1.4) {UC22: Xem DS kho};

\node[actor, label=below:{\scriptsize\bfseries NV / QL}] (nv) at (-7.5,0.8) {};
\node[actor, label=below:{\scriptsize\bfseries QL / QTV}] (ql) at (7.5,0.8) {};
\foreach \u in {h13,h14,h15,h16,h17} { \draw (nv) -- (\u); \draw (ql) -- (\u); }
\foreach \u in {k18,k19,k20,k21,k22} { \draw (ql) -- (\u); }
\end{tikzpicture}}
\caption{Use case phân rã -- Hàng hóa (UC13--17) và Kho (UC18--22)}
\label{fig:usecase-item-management}
\end{figure}
""", encoding="utf-8")

    (DG / "3.8_usecase_inventory_management.tex").write_text(r"""\begin{figure}[H]
\centering
\makebox[\textwidth][c]{%
\begin{tikzpicture}[
    scale=0.72, transform shape,
    actor/.style={circle, draw=black, fill=white, line width=0.8pt, minimum size=0.6cm},
    usecase/.style={ellipse, draw=black, fill=white, line width=0.5pt, minimum width=3.1cm, minimum height=0.5cm, font=\scriptsize, align=center},
    system/.style={rectangle, draw=black!50, dashed, fill=white, line width=0.4pt, inner sep=5pt, rounded corners=3pt}
]
\node[system, minimum width=15cm, minimum height=11cm] (system) at (0,0) {};
\node[font=\bfseries\small] at (0,5.1) {Phân rã: Phiếu nhập / xuất / kiểm kê / báo cáo};

\node[font=\scriptsize\bfseries] at (-3.6,4.2) {Phiếu nhập};
\node[usecase] (n23) at (-3.6,3.5) {UC23: Lập PN};
\node[usecase] (n24) at (-3.6,2.6) {UC24: Sửa PN};
\node[usecase] (n25) at (-3.6,1.7) {UC25: Xóa PN};
\node[usecase] (n26) at (-3.6,0.8) {UC26: Tìm PN};
\node[usecase] (n27) at (-3.6,-0.1) {UC27: Xem DS PN};

\node[font=\scriptsize\bfseries] at (3.6,4.2) {Phiếu xuất};
\node[usecase] (x28) at (3.6,3.5) {UC28: Lập PX};
\node[usecase] (x29) at (3.6,2.6) {UC29: Sửa PX};
\node[usecase] (x30) at (3.6,1.7) {UC30: Xóa PX};
\node[usecase] (x31) at (3.6,0.8) {UC31: Tìm PX};
\node[usecase] (x32) at (3.6,-0.1) {UC32: Xem DS PX};

\node[usecase] (kk) at (-3.6,-1.3) {UC33: Lập kiểm kê};
\node[usecase] (bc) at (3.6,-1.3) {UC34: Xem BC tồn};

\node[actor, label=below:{\scriptsize\bfseries NV kho}] (nv) at (-8,1.2) {};
\node[actor, label=below:{\scriptsize\bfseries QL kho}] (ql) at (8,1.2) {};
\foreach \u in {n23,n24,n25,n26,n27,x28,x29,x30,x31,x32,kk} {
  \draw (nv) -- (\u); \draw (ql) -- (\u);
}
\draw (ql) -- (bc);
\end{tikzpicture}}
\caption{Use case phân rã -- PN (UC23--27), PX (UC28--32), KK (UC33), BC (UC34)}
\label{fig:usecase-inventory-management}
\end{figure}
""", encoding="utf-8")

    (DG / "7.3_ui_navigation.tex").write_text(r"""\begin{figure}[H]
\centering
\makebox[\textwidth][c]{%
\begin{tikzpicture}[
    scale=0.85, transform shape,
    scr/.style={rectangle, draw=black, rounded corners=3pt, minimum width=2.3cm, minimum height=0.9cm, font=\scriptsize\bfseries, align=center, fill=white, line width=0.7pt},
    arrow/.style={-{Stealth[scale=0.65]}, line width=0.5pt}
]
\node[scr, fill=gray!15] (login) at (0,4) {Đăng nhập\\UC01};
\node[scr] (home) at (0,2.3) {Trang chủ};
\node[scr] (hh) at (-5.5,0.7) {Hàng hóa\\UC13--17};
\node[scr] (dt) at (-2.75,0.7) {NCC\\UC08--12};
\node[scr] (kho) at (0,0.7) {Kho\\UC18--22};
\node[scr] (tk) at (2.75,0.7) {Tài khoản\\UC03--07};
\node[scr] (bc) at (5.5,0.7) {Báo cáo\\UC34};
\node[scr] (pn) at (-3.5,-1.3) {Phiếu nhập\\UC23--27};
\node[scr] (px) at (0,-1.3) {Phiếu xuất\\UC28--32};
\node[scr] (kk) at (3.5,-1.3) {Kiểm kê\\UC33};
\draw[arrow] (login) -- (home);
\foreach \n in {hh,dt,kho,tk,bc,pn,px,kk} { \draw[arrow] (home) -- (\n); }
\end{tikzpicture}}
\caption{Sơ đồ điều hướng màn hình chính (theo use case)}
\label{fig:ui-nav}
\end{figure}
""", encoding="utf-8")

    # Activity captions
    for f, cap in [
        ("2.1_activity_nhapkho.tex", "Activity -- UC23 Lập phiếu nhập kho"),
        ("2.2_activity_xuatkho.tex", "Activity -- UC28 Lập phiếu xuất kho"),
        ("2.3_activity_kiemke.tex", "Activity -- UC33 Lập phiếu kiểm kê"),
        ("5.1_sequence_uc05.tex", "Sequence diagram UC13 -- Thêm hàng hóa"),
        ("5.2_sequence_uc06.tex", "Sequence diagram UC16 -- Tìm kiếm hàng hóa"),
        ("5.3_sequence_uc09.tex", "Sequence diagram UC23 -- Lập phiếu nhập kho"),
        ("5.4_sequence_uc10.tex", "Sequence diagram UC28 -- Lập phiếu xuất kho"),
        ("4.4_class_uc05.tex", "Biểu đồ lớp trong ca sử dụng UC13 -- Thêm hàng hóa"),
        ("4.5_class_uc09.tex", "Biểu đồ lớp trong ca sử dụng UC23 -- Lập phiếu nhập kho"),
        ("4.6_class_uc10.tex", "Biểu đồ lớp trong ca sử dụng UC28 -- Lập phiếu xuất kho"),
        ("4.8_activity_uc06.tex", "Activity -- UC13 Thêm hàng hóa"),
        ("4.9_activity_uc07.tex", "Activity -- UC16 Tìm kiếm hàng hóa"),
    ]:
        path = DG / f
        if path.exists():
            t = path.read_text(encoding="utf-8")
            t2 = __import__("re").sub(r"\\caption\{[^}]*\}", rf"\\caption{{{cap}}}", t, count=1)
            path.write_text(t2, encoding="utf-8")
    print("OK diagrams")


def patch_chapter4_5_6_7():
    # ch4
    p = CH / "chapter4_phan_tich_hanh_vi.tex"
    t = p.read_text(encoding="utf-8")
    reps = [
        ("HangHoa & Thông tin mặt hàng & UC14, UC15, phiếu \\\\",
         "HangHoa & Thông tin mặt hàng & UC13--UC17, phiếu \\\\"),
        ("NhomHangHoa & Phân loại hàng & UC14 \\\\",
         "NhomHangHoa & Phân loại hàng & UC13 \\\\"),
        ("DonViTinh & Đơn vị đo (cái, kg\\ldots) & UC14 \\\\",
         "DonViTinh & Đơn vị đo (cái, kg\\ldots) & UC13 \\\\"),
        ("NhaCungCap & Nhà cung cấp & UC08--UC12, UC17 \\\\",
         "NhaCungCap & Nhà cung cấp & UC08--UC12, UC23 \\\\"),
        ("KhachHang & Khách hàng & UC13, UC18 \\\\",
         "PhieuXuatKho & Phiếu xuất (ghi chú người nhận) & UC28--UC32 \\\\"),  # replace KH row - careful
        ("Kho & Kho hàng & UC16, phiếu, tồn \\\\",
         "Kho & Kho hàng & UC18--UC22, phiếu, tồn \\\\"),
        ("TonKho & Số lượng tồn theo kho--hàng & UC14, UC17--UC20 \\\\",
         "TonKho & Số lượng tồn theo kho--hàng & UC13, UC23--UC34 \\\\"),
        ("PhieuNhapKho & Phiếu nhập & UC17 \\\\",
         "PhieuNhapKho & Phiếu nhập & UC23--UC27 \\\\"),
        ("ChiTietPhieuNhap & Dòng hàng trên phiếu nhập & UC17 \\\\",
         "ChiTietPhieuNhap & Dòng hàng trên phiếu nhập & UC23 \\\\"),
        ("PhieuXuatKho & Phiếu xuất & UC18 \\\\",
         "PhieuXuatKho & Phiếu xuất & UC28--UC32 \\\\"),
        ("ChiTietPhieuXuat & Dòng hàng trên phiếu xuất & UC18 \\\\",
         "ChiTietPhieuXuat & Dòng hàng trên phiếu xuất & UC28 \\\\"),
        ("PhieuKiemKe & Phiếu kiểm kê & UC19 \\\\",
         "PhieuKiemKe & Phiếu kiểm kê & UC33 \\\\"),
        ("ChiTietKiemKe & Dòng kiểm kê (thực tế, sổ, chênh) & UC19 \\\\",
         "ChiTietKiemKe & Dòng kiểm kê (thực tế, sổ, chênh) & UC33 \\\\"),
    ]
    for a, b in reps:
        t = t.replace(a, b)

    # Fix double PhieuXuatKho if both KH replace and later created duplicate
    # Remove KhachHang mentions
    t = t.replace("nhà cung cấp, khách hàng, kho", "nhà cung cấp, kho")
    t = t.replace("\\texttt{NhaCungCap} và \\texttt{KhachHang} là danh mục đối tác dùng sau này trên phiếu.",
                  "\\texttt{NhaCungCap} dùng trên phiếu nhập; phiếu xuất dùng ghi chú người nhận (không có lớp khách hàng).")
    t = t.replace("\\texttt{PhieuXuatKho} tương tự nhưng gắn \\texttt{KhachHang}.",
                  "\\texttt{PhieuXuatKho} tương tự phiếu nhập nhưng không gắn NCC/KH -- có trường lý do/ghi chú.")
    t = t.replace("phần cấu trúc cho UC19 và audit", "phần cấu trúc cho UC33 và audit")
    t = t.replace("\\subsection{UC14 -- Thêm hàng hóa}", "\\subsection{UC13 -- Thêm hàng hóa}")
    t = t.replace("dùng cho UC15.", "dùng cho UC16.")
    t = t.replace("Cắt lát cấu trúc cho UC14.", "Cắt lát cấu trúc cho UC13.")
    t = t.replace("\\subsection{UC17 -- Lập phiếu nhập kho}", "\\subsection{UC23 -- Lập phiếu nhập kho}")
    t = t.replace("lớp trung tâm UC17", "lớp trung tâm UC23")
    t = t.replace("\\subsection{UC18 -- Lập phiếu xuất kho}", "\\subsection{UC28 -- Lập phiếu xuất kho}")
    t = t.replace(
        "\\textbf{Lớp tham gia}: \\texttt{NguoiDung}, \\texttt{PhieuXuatKho}, \\texttt{ChiTietPhieuXuat}, \\texttt{KhachHang}, \\texttt{Kho}, \\texttt{HangHoa}, \\texttt{TonKho}.",
        "\\textbf{Lớp tham gia}: \\texttt{NguoiDung}, \\texttt{PhieuXuatKho}, \\texttt{ChiTietPhieuXuat}, \\texttt{Kho}, \\texttt{HangHoa}, \\texttt{TonKho}.",
    )
    t = t.replace(
        "\\textbf{Quan hệ}: tương tự phiếu nhập, thay NhaCungCap bằng KhachHang; TonKho dùng để kiểm tra và giảm số lượng.",
        "\\textbf{Quan hệ}: tương tự phiếu nhập (không có NCC/KH); TonKho kiểm tra và giảm số lượng.",
    )
    t = t.replace("Cấu trúc tương tự UC17 nhưng \\texttt{PhieuXuatKho} gắn \\texttt{KhachHang} thay cho NCC.",
                  "Cấu trúc tương tự UC23; \\texttt{PhieuXuatKho} không gắn khách hàng.")
    t = t.replace("truy vết được khách và kho xuất.", "truy vết được kho xuất và lý do xuất.")
    t = t.replace("KhachHang & MaKH, Ten, DiaChi, SDT, Email, MST & Phục vụ xuất \\\\",
                  "PhieuXuatKho & MaPhieu, MaKho, LyDoXuat, GhiChu, TrangThai & Không dùng MaKH \\\\",)

    # Methods UC numbers
    for a, b in [
        ("UC14.", "UC13."),
        ("UC15.", "UC16."),
        ("(UC14)", "(UC13)"),
        ("(UC17)", "(UC23)"),
        ("(UC18)", "(UC28)"),
        ("(UC19)", "(UC33)"),
        ("UC15, UC20", "UC16, UC34"),
        ("UC17.", "UC23."),
        ("UC18.", "UC28."),
        ("UC19.", "UC33."),
        ("NCC (UC08), KH (UC13) hoặc Kho (UC16)", "NCC (UC08) hoặc Kho (UC18)"),
        ("NCC dùng cho UC09.", "NCC dùng cho UC09; hàng UC14; kho UC19."),
        ("(UC10).", "(UC10); hàng UC15; kho UC20."),
        ("NCC dùng cho UC11.", "NCC UC11; hàng UC16; kho UC21."),
        ("NCC dùng cho UC12.", "NCC UC12; hàng UC17; kho UC22; phiếu UC27/UC32."),
    ]:
        t = t.replace(a, b)

    # Summary methods list
    old_sum = """    \\item \\textbf{UC08}: \\texttt{NhaCungCap.themMoi}; \\textbf{UC09}: \\texttt{capNhat}; \\textbf{UC10}: \\texttt{xoa}/\\texttt{ngungHoatDong}; \\textbf{UC11}: \\texttt{timKiem}; \\textbf{UC12}: \\texttt{layDanhSach}.
    \\item \\textbf{UC13, UC16}: \\texttt{themMoi} trên \\texttt{KhachHang}, \\texttt{Kho}.
    \\item \\textbf{UC14}: \\texttt{HangHoa.themHangHoa} + \\texttt{TonKho.khoiTaoTon}.
    \\item \\textbf{UC15}: \\texttt{HangHoa.timKiem} + \\texttt{TonKho.layTon}.
    \\item \\textbf{UC17}: \\texttt{PhieuNhapKho.lapPhieu / themChiTiet / guiDuyet / duyetPhieu} (+ \\texttt{tangTon}).
    \\item \\textbf{UC18}: tương tự phiếu xuất (+ \\texttt{kiemTraDu}, \\texttt{giamTon}).
    \\item \\textbf{UC19}: \\texttt{PhieuKiemKe.*} + \\texttt{ganTheoKiemKe}.
    \\item \\textbf{UC20}: chủ yếu đọc dữ liệu (\\texttt{layTon}, tổng hợp từ phiếu) -- có thể đặt ở lớp dịch vụ báo cáo khi thiết kế chi tiết."""

    new_sum = """    \\item \\textbf{UC08--UC12}: \\texttt{NhaCungCap} them/sua/xoa/tim/xem DS.
    \\item \\textbf{UC13--UC17}: \\texttt{HangHoa} them (+\\texttt{khoiTaoTon})/sua/xoa/tim/xem DS.
    \\item \\textbf{UC18--UC22}: \\texttt{Kho} them/sua/xoa/tim/xem DS.
    \\item \\textbf{UC23--UC27}: \\texttt{PhieuNhapKho} lập/sửa/xóa/tìm/xem (+ duyệt, \\texttt{tangTon}).
    \\item \\textbf{UC28--UC32}: \\texttt{PhieuXuatKho} tương tự (+ \\texttt{kiemTraDu}, \\texttt{giamTon}).
    \\item \\textbf{UC33}: \\texttt{PhieuKiemKe.*} + \\texttt{ganTheoKiemKe}.
    \\item \\textbf{UC34}: đọc/tổng hợp tồn và phiếu (báo cáo)."""
    t = t.replace(old_sum, new_sum)
    t = t.replace("NguoiDung--Phieu; NhaCungCap--PhieuNhap; KhachHang--PhieuXuat;",
                  "NguoiDung--Phieu; NhaCungCap--PhieuNhap;")

    # HangHoa methods expand
    t = t.replace(
        "\\texttt{themHangHoa(thongTin)} & Lưu hàng mới; gọi khởi tạo tồn kho. UC13. \\\\\n\\hline\n\\texttt{capNhatThongTin(ma, thongTin)} & Sửa tên, giá, nhóm, mô tả\\ldots \\\\\n\\hline\n\\texttt{ngungSuDung(ma)} & Đánh dấu trạng thái ngừng (không xóa cứng nếu đã có phiếu). \\\\\n\\hline\n\\texttt{timKiem(tuKhoa, boLoc)} & Trả về danh sách hàng theo mã/tên/nhóm. UC16. \\\\\n\\hline\n\\texttt{layThongTin(ma)} & Lấy chi tiết một mặt hàng. \\\\",
        "\\texttt{themHangHoa(thongTin)} & Lưu hàng mới; gọi khởi tạo tồn kho. UC13. \\\\\n\\hline\n\\texttt{capNhatThongTin(ma, thongTin)} & Sửa tên, giá, nhóm, mô tả. UC14. \\\\\n\\hline\n\\texttt{ngungSuDung(ma)} / \\texttt{xoa(ma)} & Xóa hoặc ngừng (nếu đã có phiếu). UC15. \\\\\n\\hline\n\\texttt{timKiem(tuKhoa, boLoc)} & Tìm theo mã/tên/nhóm. UC16. \\\\\n\\hline\n\\texttt{layDanhSach()} & Xem DS / phân trang. UC17. \\\\\n\\hline\n\\texttt{layThongTin(ma)} & Lấy chi tiết một mặt hàng. \\\\",
    )

    p.write_text(t, encoding="utf-8")
    print("OK chapter4")

    # ch5
    p5 = CH / "chapter5_phan_tich_tuong_tac.tex"
    t5 = p5.read_text(encoding="utf-8")
    t5 = t5.replace("\\subsection{UC14 -- Thêm hàng hóa}", "\\subsection{UC13 -- Thêm hàng hóa}")
    t5 = t5.replace("\\subsection{UC15 -- Tìm kiếm hàng hóa}", "\\subsection{UC16 -- Tìm kiếm hàng hóa}")
    t5 = t5.replace("So với UC14,", "So với UC13,")
    t5 = t5.replace("\\subsection{UC17 -- Lập phiếu nhập kho}", "\\subsection{UC23 -- Lập phiếu nhập kho}")
    t5 = t5.replace("\\subsection{UC18 -- Lập phiếu xuất kho}", "\\subsection{UC28 -- Lập phiếu xuất kho}")
    t5 = t5.replace("Khác UC17 ở chỗ", "Khác UC23 ở chỗ")
    p5.write_text(t5, encoding="utf-8")
    print("OK chapter5")

    # ch6
    p6 = CH / "chapter6_thiet_ke_lop_chi_tiet.tex"
    t6 = p6.read_text(encoding="utf-8")
    t6 = t6.replace(
        "NhaCungCap 1--n PhieuNhapKho; KhachHang 1--n PhieuXuatKho.",
        "NhaCungCap 1--n PhieuNhapKho; PhieuXuatKho không gắn khách hàng (chỉ ghi chú/lý do).",
    )
    p6.write_text(t6, encoding="utf-8")
    print("OK chapter6")

    # ch7
    p7 = CH / "chapter7_thiet_ke_csdl_va_giao_dien.tex"
    t7 = p7.read_text(encoding="utf-8")
    t7 = t7.replace(
        "KhachHang & KH: mã, tên, địa chỉ, SĐT, email, MST, người liên hệ. \\\\\n",
        "",
    )
    t7 = t7.replace(
        "\\item \\textbf{PhieuXuatKho}: tương tự, thay NCC bằng MaKhachHang, NgayXuat.",
        "\\item \\textbf{PhieuXuatKho}: MaPhieu, MaKho, MaNguoiDung, NgayXuat, LyDoXuat, GhiChu, TongTien, TrangThai (không có MaKhachHang).",
    )
    t7 = t7.replace(
        "Hàng hóa (UC14--UC15), NCC (UC08--UC12), Kho (UC16), Tài khoản (UC03--UC07), Báo cáo tồn (UC20), Phiếu nhập (UC17), Phiếu xuất (UC18), Kiểm kê (UC19).",
        "Hàng hóa (UC13--UC17), NCC (UC08--UC12), Kho (UC18--UC22), Tài khoản (UC03--UC07), Báo cáo (UC34), Phiếu nhập (UC23--UC27), Phiếu xuất (UC28--UC32), Kiểm kê (UC33).",
    )
    t7 = t7.replace(
        "Hàng hóa (UC14, UC15); Nhà cung cấp (UC08--UC12: thêm/sửa/xóa/tìm/xem DS); Khách hàng (UC13); Kho (UC16); Tài khoản (UC03--UC07: thêm/sửa/xóa/tìm/xem DS).",
        "Hàng hóa (UC13--UC17); NCC (UC08--UC12); Kho (UC18--UC22); Tài khoản (UC03--UC07) -- mỗi nhóm đủ thêm/sửa/xóa/tìm/xem DS.",
    )
    t7 = t7.replace(
        "Phiếu nhập (UC17); Phiếu xuất (UC18); Kiểm kê (UC19).",
        "Phiếu nhập (UC23--UC27); Phiếu xuất (UC28--UC32); Kiểm kê (UC33).",
    )
    t7 = t7.replace(
        "Báo cáo nhập--xuất--tồn (UC20):",
        "Báo cáo nhập--xuất--tồn (UC34):",
    )
    p7.write_text(t7, encoding="utf-8")
    print("OK chapter7")

    # ch1 light touch - remove customer as system feature emphasis
    p1 = CH / "chapter1_khao_sat_hien_trang.tex"
    t1 = p1.read_text(encoding="utf-8")
    t1 = t1.replace(
        "Quản lý thông tin nhà cung cấp, khách hàng và các đối tác liên quan.",
        "Quản lý thông tin nhà cung cấp và danh mục hàng/kho.",
    )
    t1 = t1.replace(
        "Hỗ trợ quản lý nhiều kho, nhiều loại hàng hóa và nhiều nhà cung cấp/khách hàng.",
        "Hỗ trợ quản lý nhiều kho, nhiều loại hàng hóa và nhiều nhà cung cấp.",
    )
    t1 = t1.replace(
        "Quản lý nhà cung cấp và khách hàng: thêm, sửa, xóa, tìm kiếm thông tin đối tác.",
        "Quản lý nhà cung cấp, hàng hóa, kho: thêm, sửa, xóa, tìm kiếm, xem danh sách.",
    )
    p1.write_text(t1, encoding="utf-8")
    print("OK chapter1")


def main():
    patch_chapter2()
    patch_chapter3()
    write_diagrams()
    patch_chapter4_5_6_7()
    print("DONE")


if __name__ == "__main__":
    main()
