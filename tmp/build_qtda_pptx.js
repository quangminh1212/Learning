const pptxgen = require("./node_modules/pptxgenjs");
const path = require("path");

const RED = "C81028";
const REDD = "9D1D1F";
const GOLD = "F0C008";
const INK = "1A1A1A";
const MUTED = "5C5C5C";
const LINE = "E8D9DC";
const PAPER = "FDFAFB";
const WHITE = "FFFFFF";
const PINK = "F8E9EC";
const GREEN = "E7F4EC";
const OK = "1F7A4D";
const EVEN = "FBF8F8";
const FACE = "Calibri";
const LOGO = path.join(__dirname, "../VIII.HUST/Quản trị dự án/slide/hust-logo.png");
const OUT = path.join(__dirname, "../VIII.HUST/Quản trị dự án/slide/slide-thuyet-trinh.pptx");

const pres = new pptxgen();
pres.defineLayout({ name: "WIDE16", width: 13.333, height: 7.5 });
pres.layout = "WIDE16";
pres.title = "Nhóm 1 — QL hàng hóa và kho bãi sản phẩm thời trang";
pres.author = "Nhóm 1 · CNTT20261_N01";
pres.subject = "Bài tập lớn Quản trị dự án";

function hdr(slide, kicker, title) {
  slide.addText(kicker.toUpperCase(), {
    x: 0.4, y: 0.16, w: 12.5, h: 0.26,
    fontSize: 11, bold: true, color: RED, fontFace: FACE, margin: 0, charSpacing: 1.2
  });
  slide.addText(title, {
    x: 0.4, y: 0.4, w: 12.5, h: 0.4,
    fontSize: 24, bold: true, color: INK, fontFace: FACE, margin: 0
  });
}

function foot(slide, n, extra) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.4, y: 7.16, w: 12.53, h: 0.015, fill: { color: LINE }, line: { color: LINE, width: 0 }
  });
  slide.addText(extra || "Nhóm 1 · CNTT20261_N01", {
    x: 0.4, y: 7.2, w: 9.2, h: 0.22, fontSize: 10, color: MUTED, fontFace: FACE, margin: 0
  });
  slide.addText("Trang " + n + " / 15", {
    x: 10.3, y: 7.2, w: 2.63, h: 0.22, fontSize: 10, color: MUTED, align: "right", fontFace: FACE, margin: 0
  });
}

function box(slide, x, y, w, h, fill, line) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    fill: { color: fill || WHITE },
    line: { color: line || LINE, width: 1 },
    rectRadius: 0.08
  });
}

function kpi(slide, x, y, w, h, num, lab) {
  box(slide, x, y, w, h);
  slide.addText(num, {
    x, y: y + 0.08, w, h: h * 0.52,
    fontSize: 20, bold: true, color: RED, align: "center", valign: "middle", fontFace: FACE, margin: 0
  });
  slide.addText(lab, {
    x: x + 0.06, y: y + h * 0.55, w: w - 0.12, h: h * 0.38,
    fontSize: 11, color: MUTED, align: "center", valign: "top", fontFace: FACE, margin: 0
  });
}

function chip(slide, x, y, w, h, title, sub, fill, color) {
  box(slide, x, y, w, h, fill || WHITE);
  const runs = [{ text: title, options: { bold: true, breakLine: !!sub } }];
  if (sub) runs.push({ text: sub, options: { fontSize: 10, color: MUTED } });
  slide.addText(runs, {
    x: x + 0.08, y, w: w - 0.16, h,
    fontSize: 12, color: color || INK, align: "center", valign: "middle", fontFace: FACE, margin: 0
  });
}

function th(t) {
  return { text: t, options: { fill: { color: RED }, color: WHITE, bold: true, fontSize: 11, fontFace: FACE, valign: "middle", margin: 4 } };
}
function td(t, i, extra) {
  return { text: String(t), options: Object.assign({ fontSize: 11, fontFace: FACE, color: INK, valign: "middle", fill: { color: i % 2 ? EVEN : WHITE }, margin: 4 }, extra || {}) };
}

function flow(slide, x, y, w, h, steps) {
  const n = steps.length;
  const arrow = 0.18;
  const gap = 0.04;
  const sw = (w - (n - 1) * (arrow + gap)) / n;
  steps.forEach((s, i) => {
    const sx = x + i * (sw + arrow + gap);
    box(slide, sx, y, sw, h);
    slide.addText(String(i + 1), {
      x: sx, y: y + 0.04, w: sw, h: 0.2,
      fontSize: 10, bold: true, color: RED, align: "center", fontFace: FACE, margin: 0
    });
    slide.addText(s, {
      x: sx + 0.04, y: y + 0.22, w: sw - 0.08, h: h - 0.28,
      fontSize: 11, bold: true, color: INK, align: "center", valign: "top", fontFace: FACE, margin: 0
    });
    if (i < n - 1) {
      slide.addText("→", {
        x: sx + sw, y, w: arrow + gap, h,
        fontSize: 14, bold: true, color: RED, align: "center", valign: "middle", fontFace: FACE, margin: 0
      });
    }
  });
}

function tbl(slide, rows, x, y, w, h, colW) {
  slide.addTable(rows, {
    x, y, w, h, colW,
    border: [{ pt: 0, color: WHITE }, { pt: 0.5, color: LINE }, { pt: 0, color: WHITE }, { pt: 0, color: WHITE }],
    fontFace: FACE, color: INK, valign: "middle"
  });
}

// ── 1 Cover ──────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 7.45, h: 7.5, fill: { color: RED }, line: { color: RED, width: 0 } });
  s.addImage({ path: LOGO, x: 0.45, y: 0.38, w: 0.72, h: 0.72 });
  s.addText("ĐẠI HỌC BÁCH KHOA HÀ NỘI", {
    x: 1.28, y: 0.42, w: 5.9, h: 0.28, fontSize: 11, bold: true, color: GOLD, fontFace: FACE, margin: 0, charSpacing: 0.8
  });
  s.addText("Trường Công nghệ Thông tin và Truyền thông", {
    x: 1.28, y: 0.7, w: 5.9, h: 0.32, fontSize: 13, bold: true, color: WHITE, fontFace: FACE, margin: 0
  });
  box(s, 0.45, 1.32, 2.55, 0.32, "7A5C00", "7A5C00");
  s.addText("Bài tập lớn · CNTT20261_N01", {
    x: 0.45, y: 1.32, w: 2.55, h: 0.32, fontSize: 11, bold: true, color: GOLD, align: "center", valign: "middle", fontFace: FACE, margin: 0
  });
  s.addText("Hệ thống quản lý hàng hóa và kho bãi sản phẩm thời trang", {
    x: 0.45, y: 1.8, w: 6.55, h: 1.15, fontSize: 26, bold: true, color: WHITE, fontFace: FACE, margin: 0
  });
  s.addText("Quản lý dự án xây dựng hệ thống · Báo cáo phân tích và thiết kế", {
    x: 0.45, y: 2.98, w: 6.55, h: 0.35, fontSize: 13, color: "FFE8EA", fontFace: FACE, margin: 0
  });
  [["Thay thế", "Sổ sách + Excel rời"], ["Trung tâm", "Kho hàng hóa"], ["Đơn vị tồn", "SP + màu + size"]].forEach((c, i) => {
    const x = 0.45 + i * 2.25;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
      x, y: 3.55, w: 2.12, h: 1.15, fill: { color: REDD }, line: { color: "E8A0A8", width: 1 }, rectRadius: 0.08
    });
    s.addText(c[0].toUpperCase(), { x, y: 3.68, w: 2.12, h: 0.28, fontSize: 11, bold: true, color: GOLD, align: "center", fontFace: FACE, margin: 0 });
    s.addText(c[1], { x: x + 0.08, y: 3.98, w: 1.96, h: 0.55, fontSize: 14, bold: true, color: WHITE, align: "center", fontFace: FACE, margin: 0 });
  });
  [["Thời gian", "01/09/2026 – 31/03/2027"], ["Kinh phí", "408.196.650 VNĐ"], ["GVHD", "ThS. Lê Thị Hoa"]].forEach((m, i) => {
    const x = 0.45 + i * 2.3;
    s.addText(m[0].toUpperCase(), { x, y: 6.55, w: 2.2, h: 0.22, fontSize: 10, bold: true, color: GOLD, fontFace: FACE, margin: 0, charSpacing: 0.8 });
    s.addText(m[1], { x, y: 6.78, w: 2.2, h: 0.32, fontSize: 13, bold: true, color: WHITE, fontFace: FACE, margin: 0 });
  });

  s.addText("NHÓM 1 · LỚP K6901 CNTT VB2CQ", {
    x: 7.7, y: 0.38, w: 5.2, h: 0.24, fontSize: 11, bold: true, color: RED, fontFace: FACE, margin: 0, charSpacing: 0.8
  });
  s.addText("Thành viên", { x: 7.7, y: 0.64, w: 5.2, h: 0.36, fontSize: 22, bold: true, color: INK, fontFace: FACE, margin: 0 });
  const members = [
    ["TA", RED, "Bùi Tuấn Anh · 202490032", "Giám đốc dự án, Phân tích nghiệp vụ"],
    ["QL", GOLD, "Bùi Quốc Luýt · 202490069", "Trưởng nhóm kỹ thuật, Lập trình Back-end"],
    ["QM", RED, "Vũ Quang Minh · 202490071", "Lập trình Back-end"],
    ["MQ", GOLD, "Bạch Minh Quang · 202490077", "Thiết kế UI/UX, Lập trình Front-end"],
    ["BT", RED, "Phạm Đoàn Bảo Thiên · 202490090", "Thiết kế CSDL, Kiểm thử"]
  ];
  members.forEach((m, i) => {
    const y = 1.1 + i * 0.78;
    s.addShape(pres.shapes.OVAL, { x: 7.7, y: y + 0.08, w: 0.42, h: 0.42, fill: { color: m[1] }, line: { color: m[1], width: 0 } });
    s.addText(m[0], { x: 7.7, y: y + 0.08, w: 0.42, h: 0.42, fontSize: 10, bold: true, color: m[1] === GOLD ? INK : WHITE, align: "center", valign: "middle", fontFace: FACE, margin: 0 });
    s.addText(m[2], { x: 8.25, y, w: 4.65, h: 0.32, fontSize: 14, bold: true, color: INK, fontFace: FACE, margin: 0 });
    s.addText(m[3], { x: 8.25, y: y + 0.3, w: 4.65, h: 0.28, fontSize: 11, color: MUTED, fontFace: FACE, margin: 0 });
  });
  box(s, 7.7, 5.05, 5.2, 2.05);
  s.addText("Bộ hồ sơ · 5 tài liệu", { x: 7.85, y: 5.15, w: 4.9, h: 0.3, fontSize: 13, bold: true, color: INK, fontFace: FACE, margin: 0 });
  flow(s, 7.85, 5.52, 4.9, 1.4, ["Khảo sát", "PTTK", "WBS", "Kinh phí", "Chất lượng"]);
}

// ── 2 Hồ sơ ──────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  hdr(s, "Bộ hồ sơ Nhóm 1", "Năm tài liệu và sáu chương PTTK");
  const kpis = [["19", "Yêu cầu chức năng"], ["11", "Yêu cầu phi chức năng"], ["19", "Use case có đặc tả"], ["15", "Bảng CSDL"], ["10", "Màn hình"]];
  kpis.forEach((k, i) => kpi(s, 0.4 + i * 2.58, 0.92, 2.48, 0.85, k[0], k[1]));
  tbl(s, [
    [th("#"), th("Tài liệu"), th("Nội dung")],
    [td("1", 0), td("Báo cáo khảo sát hiện trạng", 0), td("Bối cảnh, quy trình kho, vấn đề khách hàng", 0)],
    [td("2", 1), td("Báo cáo phân tích và thiết kế hệ thống", 1), td("FR, NFR, QT, use case, kiến trúc, CSDL, giao diện", 1)],
    [td("3", 0), td("Bảng phân rã công việc và tôn chỉ dự án", 0), td("Danh sách công việc, tiến độ, phân công, tôn chỉ", 0)],
    [td("4", 1), td("Bảng dự toán kinh phí", 1), td("Chi phí thực hiện", 1)],
    [td("5", 0), td("Kế hoạch quản lý chất lượng", 0), td("Kiểm soát chất lượng từng giai đoạn", 0)]
  ], 0.4, 1.9, 12.53, 2.45, [0.7, 4.8, 7.03]);
  box(s, 0.4, 4.5, 12.53, 2.5);
  s.addText("Báo cáo PTTK — 6 chương", { x: 0.55, y: 4.58, w: 12.2, h: 0.3, fontSize: 14, bold: true, color: INK, fontFace: FACE, margin: 0 });
  flow(s, 0.55, 4.95, 12.23, 1.15, ["Khảo sát hiện trạng", "Phân tích yêu cầu", "Phân tích", "Kiến trúc & triển khai", "Thiết kế chi tiết", "Kết luận"]);
  [["4 biểu đồ tuần tự"], ["4 biểu đồ hoạt động"], ["2 biểu đồ trạng thái"]].forEach((c, i) => {
    chip(s, 0.55 + i * 4.15, 6.22, 4.0, 0.62, c[0]);
  });
  foot(s, 2, "Nhóm 1 · CNTT20261_N01 · Chủ trì: Bùi Tuấn Anh · 5 TV · 07 tháng");
}

// ── 3 Đặc thù ────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  hdr(s, "Báo cáo khảo sát · 1.1 – 1.5", "Đặc thù ngành và đối tượng");
  box(s, 0.4, 0.95, 6.15, 4.55);
  s.addText("Đặc thù thời trang quần áo", { x: 0.55, y: 1.05, w: 5.85, h: 0.32, fontSize: 14, bold: true, color: INK, fontFace: FACE, margin: 0 });
  const dt = [
    ["Nhiều màu + size", "1 SP → nhiều biến thể"],
    ["Mẫu mã thay đổi thường xuyên", "Nhập từ nhiều NCC"],
    ["Xuất cửa hàng + online", "Tồn theo từng biến thể"],
    ["Đổi trả / lỗi / thanh lý", "Cần truy vết tình trạng"]
  ];
  dt.forEach((c, i) => {
    const x = 0.55 + (i % 2) * 2.95;
    const y = 1.5 + Math.floor(i / 2) * 1.85;
    chip(s, x, y, 2.85, 1.7, c[0], c[1]);
  });
  box(s, 6.75, 0.95, 6.18, 4.55);
  s.addText("Hiện tại: Excel + sổ sách rời", { x: 6.9, y: 1.05, w: 5.88, h: 0.32, fontSize: 14, bold: true, color: INK, fontFace: FACE, margin: 0 });
  const pr = ["Tồn không realtime", "Sai sót nhập / xuất", "Khó truy vết lịch sử", "Khó quản lý biến thể", "File không đồng nhất", "Báo cáo thủ công"];
  pr.forEach((c, i) => {
    const x = 6.9 + (i % 2) * 2.95;
    const y = 1.5 + Math.floor(i / 2) * 1.25;
    chip(s, x, y, 2.85, 1.12, c, null, PINK, REDD);
  });
  const actors = [["Quản lý", "Hàng, kho, NV, báo cáo"], ["NV kho", "Nhập, xuất, kiểm kê"], ["NV bán hàng", "Đơn bán, yêu cầu xuất"], ["Nhà cung cấp", "Cung cấp hàng hóa"], ["Khách hàng", "Mua / đổi trả"]];
  actors.forEach((a, i) => kpi(s, 0.4 + i * 2.58, 5.65, 2.48, 1.35, a[0], a[1]));
  foot(s, 3);
}

// ── 4 Quy trình ──────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  hdr(s, "Báo cáo khảo sát · 1.2", "Sáu quy trình vận hành kho");
  const procs = [
    ["Nhập hàng", ["Nhận hàng NCC", "Kiểm SL / màu / size", "Đối chiếu đơn / HĐ", "Ghi nhận nhập", "Sắp xếp vị trí", "Cập nhật tồn"]],
    ["Xuất hàng", ["Yêu cầu xuất", "Kiểm tồn", "Lấy hàng", "Kiểm sản phẩm", "Ghi nhận xuất", "Cập nhật tồn"]],
    ["Kiểm kê", ["Đếm thực tế", "Đối chiếu sổ", "Chênh lệch", "Điều chỉnh", "Báo cáo"]],
    ["Đổi trả", ["Tiếp nhận", "Kiểm tình trạng", "Đủ ĐK nhập?", "Cập nhật tồn", "Ghi nguyên nhân"]]
  ];
  procs.forEach((p, i) => {
    const y = 0.92 + i * 1.28;
    box(s, 0.4, y, 12.53, 1.2);
    s.addText(p[0], { x: 0.55, y: y + 0.04, w: 12.2, h: 0.26, fontSize: 13, bold: true, color: INK, fontFace: FACE, margin: 0 });
    flow(s, 0.55, y + 0.32, 12.23, 0.8, p[1]);
  });
  chip(s, 0.4, 6.08, 6.15, 0.92, "Chuyển kho (phụ) · UC-3.4", "Kho tổng ⇄ cửa hàng: xuất đi → xác nhận nhận");
  chip(s, 6.78, 6.08, 6.15, 0.92, "Hủy hàng (phụ) · UC-3.8", "Hàng lỗi/hỏng — trừ tồn sau khi Quản lý duyệt");
  foot(s, 4, "Nhóm 1 · CNTT20261_N01 · Khảo sát tại kho tổng và kho cửa hàng");
}

// ── 5 AT01 ───────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  hdr(s, "Báo cáo khảo sát · 1.3 – 2.2", "Biến thể AT01 và mười vấn đề");
  box(s, 0.4, 0.92, 5.9, 6.08);
  s.addText("Áo thun AT01 · tồn theo màu × size", { x: 0.55, y: 1.02, w: 5.6, h: 0.3, fontSize: 14, bold: true, color: INK, fontFace: FACE, margin: 0 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 2.15, y: 1.5, w: 2.4, h: 0.42, fill: { color: RED }, line: { color: RED, width: 0 }, rectRadius: 0.08 });
  s.addText("Áo thun AT01", { x: 2.15, y: 1.5, w: 2.4, h: 0.42, fontSize: 13, bold: true, color: WHITE, align: "center", valign: "middle", fontFace: FACE, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 1.55, y: 1.92, w: 3.6, h: 0.02, fill: { color: RED }, line: { color: RED, width: 0 } });
  s.addShape(pres.shapes.RECTANGLE, { x: 1.55, y: 1.92, w: 0.02, h: 0.28, fill: { color: RED }, line: { color: RED, width: 0 } });
  s.addShape(pres.shapes.RECTANGLE, { x: 5.13, y: 1.92, w: 0.02, h: 0.28, fill: { color: RED }, line: { color: RED, width: 0 } });
  [["Đen", 0.7], ["Trắng", 3.7]].forEach((c) => {
    box(s, c[1], 2.22, 2.3, 0.4, WHITE, RED);
    s.addText(c[0], { x: c[1], y: 2.22, w: 2.3, h: 0.4, fontSize: 13, bold: true, color: INK, align: "center", valign: "middle", fontFace: FACE, margin: 0 });
  });
  const leaves = [
    [0.55, "S", "1.000"], [1.45, "M", "1.500"], [2.35, "L", "800"],
    [3.55, "S", "1.200"], [4.55, "M", "2.000"]
  ];
  leaves.forEach((l) => {
    box(s, l[0], 2.85, 0.85, 0.85);
    s.addText(l[1], { x: l[0], y: 2.9, w: 0.85, h: 0.28, fontSize: 11, color: MUTED, align: "center", fontFace: FACE, margin: 0 });
    s.addText(l[2], { x: l[0], y: 3.18, w: 0.85, h: 0.42, fontSize: 16, bold: true, color: RED, align: "center", fontFace: FACE, margin: 0 });
  });
  s.addChart(pres.charts.BAR, [{
    name: "Tồn", labels: ["Đen/S", "Đen/M", "Đen/L", "Trắng/S", "Trắng/M"], values: [1000, 1500, 800, 1200, 2000]
  }], {
    x: 0.55, y: 3.9, w: 5.6, h: 2.85, barDir: "bar",
    chartColors: [RED, REDD, "E25A3A", GOLD, "D4A406"],
    showValue: true, showLegend: false, showTitle: false,
    catAxisLabelColor: MUTED, valAxisLabelColor: MUTED,
    valGridLine: { color: "F3E6E9", size: 0.5 }, catGridLine: { style: "none" },
    chartArea: { fill: { color: WHITE } }
  });

  box(s, 6.5, 0.92, 6.43, 6.08);
  s.addText("Vấn đề → nhu cầu hệ thống", { x: 6.65, y: 1.02, w: 6.13, h: 0.3, fontSize: 14, bold: true, color: INK, fontFace: FACE, margin: 0 });
  const map = [
    ["Dữ liệu phân tán", "Tập trung một hệ thống"],
    ["Khó quản lý biến thể", "Tồn theo màu và size"],
    ["Sai lệch tồn kho", "Tự cập nhật khi nhập/xuất"],
    ["Khó truy vết", "Lịch sử nhập, xuất, điều chỉnh"],
    ["Tìm kiếm chậm", "Tìm kiếm và lọc"],
    ["Khó kiểm kê", "Kiểm kê và điều chỉnh"],
    ["Báo cáo thủ công", "Tự động tổng hợp"],
    ["Khó kiểm soát NV", "Phân quyền người dùng"],
    ["Hàng sắp hết", "Cảnh báo tồn thấp"],
    ["Hàng tồn lâu", "Theo dõi thời gian tồn"]
  ];
  map.forEach((r, i) => {
    const y = 1.4 + i * 0.54;
    box(s, 6.65, y, 2.85, 0.48, PINK);
    s.addText(r[0], { x: 6.72, y, w: 2.71, h: 0.48, fontSize: 11, bold: true, color: REDD, valign: "middle", fontFace: FACE, margin: 0 });
    s.addText("→", { x: 9.5, y, w: 0.35, h: 0.48, fontSize: 14, bold: true, color: GOLD, align: "center", valign: "middle", fontFace: FACE, margin: 0 });
    box(s, 9.88, y, 2.85, 0.48, GREEN);
    s.addText(r[1], { x: 9.95, y, w: 2.71, h: 0.48, fontSize: 11, bold: true, color: "145A38", valign: "middle", fontFace: FACE, margin: 0 });
  });
  foot(s, 5);
}

// ── 6 QT + biểu mẫu ──────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  hdr(s, "Báo cáo khảo sát · 2.4 – 3.1", "Kho trung tâm · QT · 13 biểu mẫu");
  box(s, 0.4, 0.92, 12.53, 1.35);
  s.addText("Chuỗi chức năng cốt lõi", { x: 0.55, y: 0.98, w: 12.2, h: 0.26, fontSize: 13, bold: true, color: INK, fontFace: FACE, margin: 0 });
  flow(s, 0.55, 1.28, 12.23, 0.88, ["Sản phẩm", "Biến thể", "Nhập kho", "Xuất kho", "Tồn kho", "Kiểm kê", "Đổi trả", "Báo cáo"]);
  const qt = [
    ["QT-01 · Tồn ≥ 0", "(kho, biến thể) — không âm"],
    ["QT-02 · Phiếu Hoàn thành", "Mới được đổi tồn"],
    ["QT-03 · Chênh lệch", "Thực tế − hệ thống · QL duyệt"],
    ["QT-04 · Đổi trả", "Hàng tốt → kho bán; lỗi ≠ tồn bán"],
    ["QT-05 · Phân loại tồn", "0 / ≤ min / > min"],
    ["QT-06 · Công thức NXT", "Cuối = Đầu + Nhập − Xuất ± ĐC"]
  ];
  qt.forEach((c, i) => {
    const x = 0.4 + (i % 3) * 4.18;
    const y = 2.4 + Math.floor(i / 3) * 0.78;
    chip(s, x, y, 4.05, 0.7, c[0], c[1]);
  });
  tbl(s, [
    [th("STT"), th("Biểu mẫu"), th("Nghiệp vụ"), th("STT"), th("Biểu mẫu"), th("Nghiệp vụ")],
    [td("1", 0), td("Phiếu nhập kho", 0), td("Nhập hàng", 0), td("8", 0), td("Báo cáo tồn kho", 0), td("Quản lý tồn kho", 0)],
    [td("2", 1), td("Phiếu xuất kho", 1), td("Xuất hàng", 1), td("9", 1), td("Báo cáo nhập kho", 1), td("Nhập kho", 1)],
    [td("3", 0), td("Phiếu kiểm kê kho", 0), td("Kiểm kê", 0), td("10", 0), td("Báo cáo xuất kho", 0), td("Xuất kho", 0)],
    [td("4", 1), td("Phiếu điều chỉnh tồn kho", 1), td("Điều chỉnh", 1), td("11", 1), td("Báo cáo nhập – xuất – tồn", 1), td("Tổng hợp biến động", 1)],
    [td("5", 0), td("Phiếu đổi/trả hàng", 0), td("Đổi trả", 0), td("12", 0), td("Báo cáo kiểm kê", 0), td("Kiểm kê kho", 0)],
    [td("6", 1), td("Phiếu chuyển kho", 1), td("Chuyển kho", 1), td("13", 1), td("Báo cáo biến động hàng hóa", 1), td("Truy xuất lịch sử", 1)],
    [td("7", 0), td("Phiếu hủy hàng", 0), td("Hủy hàng", 0), td("", 0), td("7 phiếu + 6 báo cáo", 0, { bold: true }), td("Đủ 13 biểu mẫu", 0)]
  ], 0.4, 4.05, 12.53, 2.95, [0.7, 3.1, 2.4, 0.7, 3.4, 2.23]);
  foot(s, 6);
}

// ── 7 Charter ────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  hdr(s, "Tôn chỉ dự án", "Project Charter · CNTT20261_N01");
  [["Ngày bắt đầu", "01/09/2026"], ["Ngày kết thúc", "31/03/2027"], ["Giám đốc dự án", "Bùi Tuấn Anh"], ["Quyết định khởi công", "Số 01 · 31/07/2026"]].forEach((k, i) => {
    kpi(s, 0.4 + i * 3.23, 0.92, 3.13, 1.05, k[1], k[0]);
  });
  box(s, 0.4, 2.12, 6.2, 4.88);
  s.addText("Mô tả dự án", { x: 0.55, y: 2.22, w: 5.9, h: 0.3, fontSize: 14, bold: true, color: INK, fontFace: FACE, margin: 0 });
  const kv = [
    ["Tên", "QL hàng hóa và kho bãi sản phẩm thời trang"],
    ["Chủ đầu tư", "Doanh nghiệp thời trang (đơn vị khảo sát)"],
    ["Kinh phí", "408.196.650 VNĐ"],
    ["Quản trị viên", "Bùi Tuấn Anh"],
    ["Quy mô", "Phần mềm vừa · 5 thành viên · 07 tháng"]
  ];
  kv.forEach((r, i) => {
    const y = 2.6 + i * 0.38;
    s.addText(r[0], { x: 0.6, y, w: 1.7, h: 0.34, fontSize: 12, color: MUTED, fontFace: FACE, margin: 0 });
    s.addText(r[1], { x: 2.3, y, w: 4.1, h: 0.34, fontSize: 12, color: INK, fontFace: FACE, margin: 0 });
  });
  [["Bàn giao 31/03/2027"], ["Tuân thủ ngân sách"], ["Phiếu = giao dịch nguyên tử"], ["Thẻ kho chỉ thêm · ≥ 5 năm"]].forEach((c, i) => {
    const x = 0.55 + (i % 2) * 3.0;
    const y = 4.6 + Math.floor(i / 2) * 1.05;
    chip(s, x, y, 2.9, 0.95, c[0]);
  });
  box(s, 6.8, 2.12, 6.13, 4.88);
  s.addText("Kiến trúc 3 tầng", { x: 6.95, y: 2.22, w: 5.83, h: 0.3, fontSize: 14, bold: true, color: INK, fontFace: FACE, margin: 0 });
  [["C81028", "ReactJS / TypeScript   Chrome, Edge   Tablet 10\"   Máy quét mã"],
   ["9D1D1F", "REST API   Java 21   Spring Boot 3"],
   ["7A5C00", "PostgreSQL 16   Docker   Nginx"]].forEach((ly, i) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.95, y: 2.6 + i * 0.55, w: 5.83, h: 0.48, fill: { color: ly[0] }, line: { color: ly[0], width: 0 }, rectRadius: 0.06 });
    s.addText(ly[1], { x: 6.95, y: 2.6 + i * 0.55, w: 5.83, h: 0.48, fontSize: 12, bold: true, color: WHITE, align: "center", valign: "middle", fontFace: FACE, margin: 0 });
  });
  [["Tra cứu tồn < 2s", "50.000 biến thể · 100 user"], ["NXT tháng < 10s", ""], ["RBAC · bcrypt · HTTPS", "Phiên 30 phút"], ["Sẵn sàng 99%", "7h–22h · backup 4h"]].forEach((c, i) => {
    const x = 6.95 + (i % 2) * 2.95;
    const y = 4.4 + Math.floor(i / 2) * 1.15;
    chip(s, x, y, 2.85, 1.05, c[0], c[1] || null);
  });
  foot(s, 7);
}

// ── 8 Scope ──────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  hdr(s, "Tôn chỉ dự án", "Mục tiêu cụ thể và phạm vi");
  [["< 1%", "Sai lệch tồn sau kiểm kê"], ["0", "Tồn âm, kể cả xuất đồng thời"], ["Vài giây", "Truy vết thẻ kho 1 biến thể"], ["< 1 phút", "Báo cáo NXT tháng (trước: 1 ngày)"], ["Auto", "Cảnh báo hết / sắp hết"]].forEach((g, i) => {
    kpi(s, 0.4 + i * 2.58, 0.92, 2.48, 1.2, g[0], g[1]);
  });
  box(s, 0.4, 2.28, 6.2, 4.72);
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 2.28, w: 6.2, h: 0.08, fill: { color: OK }, line: { color: OK, width: 0 } });
  s.addText("In-Scope", { x: 0.55, y: 2.45, w: 2.2, h: 0.28, fontSize: 12, bold: true, color: OK, fontFace: FACE, margin: 0 });
  const inn = ["Phân tích · thiết kế · code · test", "Tài khoản + phân quyền", "SP, biến thể, NCC, kho, vị trí", "Nhập · xuất · chuyển · hủy", "Kiểm kê + điều chỉnh (duyệt)", "Đổi trả tại kho", "Tra cứu · cảnh báo · thẻ kho", "Excel đầu kỳ · đào tạo · bàn giao"];
  inn.forEach((c, i) => {
    const x = 0.55 + (i % 2) * 2.95;
    const y = 2.82 + Math.floor(i / 2) * 1.0;
    chip(s, x, y, 2.85, 0.9, c);
  });
  box(s, 6.8, 2.28, 6.13, 4.72);
  s.addShape(pres.shapes.RECTANGLE, { x: 6.8, y: 2.28, w: 6.13, h: 0.08, fill: { color: RED }, line: { color: RED, width: 0 } });
  s.addText("Out-of-Scope", { x: 6.95, y: 2.45, w: 2.4, h: 0.28, fontSize: 12, bold: true, color: RED, fontFace: FACE, margin: 0 });
  const out = ["POS · thanh toán · HĐĐT", "Đơn đặt NCC · công nợ", "Kế toán giá vốn · định khoản", "Sàn TMĐT · vận chuyển", "CSKH · khuyến mãi", "App di động riêng", "Mua tablet / máy quét"];
  out.forEach((c, i) => {
    const x = 6.95 + (i % 2) * 2.9;
    const y = 2.82 + Math.floor(i / 2) * 1.0;
    chip(s, x, y, 2.8, 0.9, c, null, PINK, REDD);
  });
  foot(s, 8);
}

// ── 9 Tổ chức ────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  hdr(s, "Tôn chỉ · WBS", "Tổ chức dự án và phân công");
  box(s, 0.4, 0.92, 6.2, 2.55);
  s.addText("Sơ đồ tổ chức", { x: 0.55, y: 0.98, w: 5.9, h: 0.26, fontSize: 13, bold: true, color: INK, fontFace: FACE, margin: 0 });
  box(s, 2.15, 1.28, 2.7, 0.52);
  s.addText("Ban Giám đốc", { x: 2.15, y: 1.28, w: 2.7, h: 0.28, fontSize: 12, bold: true, color: INK, align: "center", fontFace: FACE, margin: 0 });
  s.addText("Khách hàng · DN thời trang", { x: 2.15, y: 1.52, w: 2.7, h: 0.24, fontSize: 10, color: MUTED, align: "center", fontFace: FACE, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 3.48, y: 1.8, w: 0.03, h: 0.18, fill: { color: RED }, line: { color: RED, width: 0 } });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 1.9, y: 1.98, w: 3.2, h: 0.52, fill: { color: RED }, line: { color: RED, width: 0 }, rectRadius: 0.06 });
  s.addText("Bùi Tuấn Anh", { x: 1.9, y: 1.98, w: 3.2, h: 0.28, fontSize: 12, bold: true, color: WHITE, align: "center", fontFace: FACE, margin: 0 });
  s.addText("Giám đốc dự án · PT nghiệp vụ", { x: 1.9, y: 2.24, w: 3.2, h: 0.22, fontSize: 10, color: "FFE8EA", align: "center", fontFace: FACE, margin: 0 });
  const org = [["Bùi Quốc Luýt", "Tech Lead · BE"], ["Vũ Quang Minh", "Lập trình BE"], ["Bạch Minh Quang", "UI/UX · FE"], ["Phạm Đoàn Bảo Thiên", "CSDL · Kiểm thử"]];
  org.forEach((o, i) => {
    const x = 0.55 + i * 1.5;
    box(s, x, 2.62, 1.42, 0.7);
    s.addText(o[0], { x, y: 2.64, w: 1.42, h: 0.36, fontSize: 10, bold: true, color: INK, align: "center", fontFace: FACE, margin: 0 });
    s.addText(o[1], { x, y: 2.98, w: 1.42, h: 0.28, fontSize: 9, color: MUTED, align: "center", fontFace: FACE, margin: 0 });
  });
  box(s, 6.8, 0.92, 6.13, 2.55);
  s.addText("Ngày-người theo giai đoạn · EST chốt 221,83", { x: 6.95, y: 0.98, w: 5.83, h: 0.26, fontSize: 13, bold: true, color: INK, fontFace: FACE, margin: 0 });
  s.addChart(pres.charts.BAR, [{
    name: "Ngày-người", labels: ["A", "B", "C", "D", "E", "F"], values: [27.13, 41.07, 29.88, 69.3, 41.07, 13.38]
  }], {
    x: 6.9, y: 1.22, w: 5.9, h: 2.15, barDir: "bar",
    chartColors: [RED], showValue: true, showLegend: false,
    catAxisLabelColor: MUTED, valAxisLabelColor: MUTED,
    valGridLine: { color: "F3E6E9", size: 0.5 }, catGridLine: { style: "none" },
    chartArea: { fill: { color: WHITE } }
  });
  tbl(s, [
    [th("Thành viên"), th("A"), th("B"), th("C"), th("D"), th("E"), th("F"), th("Tổng")],
    [td("Bùi Tuấn Anh", 0), td("12,28", 0), td("11,00", 0), td("4,22", 0), td("5,68", 0), td("7,88", 0), td("2,20", 0), td("43,27", 0)],
    [td("Bùi Quốc Luýt", 1), td("8,07", 1), td("10,08", 1), td("0", 1), td("19,43", 1), td("9,17", 1), td("2,20", 1), td("48,95", 1)],
    [td("Vũ Quang Minh", 0), td("0", 0), td("8,80", 0), td("3,48", 0), td("18,15", 0), td("8,07", 0), td("3,48", 0), td("41,98", 0)],
    [td("Bạch Minh Quang", 1), td("2,38", 1), td("4,58", 1), td("13,38", 1), td("13,57", 1), td("7,88", 1), td("2,20", 1), td("44,00", 1)],
    [td("Phạm Đoàn Bảo Thiên", 0), td("4,40", 0), td("6,60", 0), td("8,80", 0), td("12,47", 0), td("8,07", 0), td("3,30", 0), td("43,63", 0)],
    [td("Tổng", 1, { bold: true }), td("27,13", 1, { bold: true }), td("41,07", 1, { bold: true }), td("29,88", 1, { bold: true }), td("69,30", 1, { bold: true }), td("41,07", 1, { bold: true }), td("13,38", 1, { bold: true }), td("221,83", 1, { bold: true })]
  ], 0.4, 3.6, 12.53, 2.55, [3.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.43]);
  chip(s, 0.4, 6.28, 4.05, 0.72, "QA chéo trong nhóm", "Không tách bộ phận QA riêng");
  chip(s, 4.64, 6.28, 4.05, 0.72, "Hệ số nhân công", "Chủ trì 0,75 · TV chính 0,45");
  chip(s, 8.88, 6.28, 4.05, 0.72, "PERT 201,67 + buffer 20,17", "Lương cơ sở 2.530.000 VNĐ");
  foot(s, 9);
}

// ── 10 WBS Gantt ─────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  hdr(s, "WBS", "Sáu giai đoạn · Task 1–52");
  box(s, 0.4, 0.92, 12.53, 2.05);
  s.addChart(pres.charts.BAR, [{
    name: "Ngày-người", labels: ["A 01/09–25/09", "B 26/09–20/11", "C 21/11–25/12", "D 26/12–15/02", "E 16/02–15/03", "F 16/03–31/03"],
    values: [27.13, 41.07, 29.88, 69.3, 41.07, 13.38]
  }], {
    x: 0.5, y: 1.0, w: 12.33, h: 1.88, barDir: "bar",
    chartColors: [RED, REDD, "C45C18", RED, REDD, GOLD],
    showValue: true, showLegend: false,
    catAxisLabelColor: MUTED, valAxisLabelColor: MUTED,
    valGridLine: { color: "F3E6E9", size: 0.5 }, catGridLine: { style: "none" },
    chartArea: { fill: { color: WHITE } }
  });
  tbl(s, [
    [th("GĐ"), th("Thời gian"), th("Task"), th("Sản phẩm"), th("Phụ thuộc")],
    [td("A", 0), td("01/09 – 25/09/2026", 0), td("1–8", 0), td("Báo cáo khảo sát & đặc tả yêu cầu", 0), td("5 sau 1–4; 8 sau 7", 0)],
    [td("B", 1), td("26/09 – 20/11/2026", 1), td("9–17", 1), td("Báo cáo PTTK (UML)", 1), td("Sau Task 8", 1)],
    [td("C", 0), td("21/11 – 25/12/2026", 0), td("18–25", 0), td("Lược đồ CSDL; thiết kế UI/UX", 0), td("Sau Task 17", 0)],
    [td("D", 1), td("26/12 – 15/02/2027", 1), td("26–39", 1), td("Mã nguồn & module chạy được", 1), td("Sau Task 20", 1)],
    [td("E", 0), td("16/02 – 15/03/2027", 0), td("40–47", 0), td("Báo cáo kiểm thử", 0), td("Sau 39; UAT sau 41–45", 0)],
    [td("F", 1), td("16/03 – 31/03/2027", 1), td("48–52", 1), td("Cấu hình · nghiệm thu · hướng dẫn · bàn giao", 1), td("Sau Task 47", 1)]
  ], 0.4, 3.1, 12.53, 2.85, [0.7, 2.5, 1.1, 5.4, 2.83]);
  chip(s, 0.4, 6.1, 4.05, 0.9, "Task 30 · Dịch vụ tồn kho", "Khóa dòng · thẻ kho chỉ thêm");
  chip(s, 4.64, 6.1, 4.05, 0.9, "Task 42 · Xuất đồng thời", "Không tồn âm · NFR-04");
  chip(s, 8.88, 6.1, 4.05, 0.9, "Task 49 · Convert Excel", "Danh mục + tồn đầu kỳ");
  foot(s, 10);
}

// ── 11 Kinh phí ──────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  hdr(s, "Bảng dự toán kinh phí", "Tổng 408.196.650 VNĐ");
  box(s, 0.4, 0.92, 6.2, 6.08);
  s.addChart(pres.charts.DOUGHNUT, [{
    name: "Kinh phí",
    labels: ["Công lao động 70%", "Vật tư, thiết bị 18%", "Chi khác 12%"],
    values: [285396650, 73800000, 49000000]
  }], {
    x: 0.55, y: 1.2, w: 5.9, h: 5.4,
    chartColors: [RED, REDD, GOLD],
    showPercent: true, showLegend: true, legendPos: "b",
    chartArea: { fill: { color: WHITE } }
  });
  box(s, 6.8, 0.92, 6.13, 6.08);
  s.addText("Công lao động · hệ số × EST chốt", { x: 6.95, y: 1.02, w: 5.83, h: 0.3, fontSize: 14, bold: true, color: INK, fontFace: FACE, margin: 0 });
  tbl(s, [
    [th("Họ tên"), th("Nhiệm vụ"), th("Hệ số"), th("Ngày công")],
    [td("Bùi Tuấn Anh", 0), td("Chủ trì", 0), td("0,75", 0), td("43,27", 0)],
    [td("Bùi Quốc Luýt", 1), td("TV chính", 1), td("0,45", 1), td("48,95", 1)],
    [td("Vũ Quang Minh", 0), td("TV chính", 0), td("0,45", 0), td("41,98", 0)],
    [td("Bạch Minh Quang", 1), td("TV chính", 1), td("0,45", 1), td("44,00", 1)],
    [td("Phạm Đoàn Bảo Thiên", 0), td("TV chính", 0), td("0,45", 0), td("43,63", 0)]
  ], 6.95, 1.4, 5.83, 2.7, [2.4, 1.3, 0.9, 1.23]);
  s.addText("Lương cơ sở 2.530.000 VNĐ · Người lập: Bùi Tuấn Anh · 25/07/2026", {
    x: 6.95, y: 4.2, w: 5.83, h: 0.28, fontSize: 11, color: MUTED, fontFace: FACE, margin: 0
  });
  kpi(s, 6.95, 4.6, 1.85, 2.15, "285,4 tr", "Công lao động · 70%");
  kpi(s, 8.92, 4.6, 1.85, 2.15, "221,83", "Ngày-người EST chốt");
  kpi(s, 10.88, 4.6, 1.85, 2.15, "2,53 tr", "Lương cơ sở");
  foot(s, 11);
}

// ── 12 Thiết bị ──────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  hdr(s, "Bảng dự toán kinh phí", "Thiết bị và chi khác theo giai đoạn");
  box(s, 0.4, 0.92, 12.53, 2.15);
  s.addText("Chi phí ngoài nhân công theo giai đoạn (triệu)", { x: 0.55, y: 0.98, w: 12.2, h: 0.26, fontSize: 13, bold: true, color: INK, fontFace: FACE, margin: 0 });
  s.addChart(pres.charts.BAR, [{
    name: "Triệu VNĐ", labels: ["A 9,5", "B 19,5", "C 17,1", "D 32,0", "E 22,6", "F 22,1"],
    values: [9.5, 19.5, 17.1, 32, 22.6, 22.1]
  }], {
    x: 0.5, y: 1.22, w: 12.33, h: 1.72, barDir: "bar",
    chartColors: [RED], showValue: true, showLegend: false,
    catAxisLabelColor: MUTED, valAxisLabelColor: MUTED,
    valGridLine: { color: "F3E6E9", size: 0.5 }, catGridLine: { style: "none" },
    chartArea: { fill: { color: WHITE } }
  });
  box(s, 0.4, 3.22, 6.2, 3.78);
  s.addText("Thiết bị · 73.800.000", { x: 0.55, y: 3.32, w: 5.9, h: 0.28, fontSize: 14, bold: true, color: INK, fontFace: FACE, margin: 0 });
  tbl(s, [
    [th("GĐ"), th("Hạng mục"), th("Thành tiền")],
    [td("A", 0), td("Thuê laptop khảo sát × 2", 0), td("4.000.000", 0)],
    [td("B", 1), td("Thuê máy nhóm × 10 (2 tháng)", 1), td("15.000.000", 1)],
    [td("C", 0), td("Thuê máy + Figma Pro", 0), td("9.100.000", 0)],
    [td("D", 1), td("Thuê máy + Cloud + máy quét", 1), td("21.000.000", 1)],
    [td("E", 0), td("Thuê máy + Cloud test + tablet", 0), td("11.600.000", 0)],
    [td("F", 1), td("Thuê máy + app/DB/storage/.vn", 1), td("13.100.000", 1)]
  ], 0.55, 3.68, 5.9, 3.15, [0.7, 3.5, 1.7]);
  box(s, 6.8, 3.22, 6.13, 3.78);
  s.addText("Chi khác · 49.000.000", { x: 6.95, y: 3.32, w: 5.83, h: 0.28, fontSize: 14, bold: true, color: INK, fontFace: FACE, margin: 0 });
  tbl(s, [
    [th("GĐ"), th("Nội dung"), th("Số tiền")],
    [td("A", 0), td("VPP + đi lại kho", 0), td("5.500.000", 0)],
    [td("B", 1), td("In đặc tả + workshop QT", 1), td("4.500.000", 1)],
    [td("C", 0), td("Duyệt prototype + OT CSDL", 0), td("8.000.000", 0)],
    [td("D", 1), td("Tem SKU + OT dịch vụ tồn", 1), td("11.000.000", 1)],
    [td("E", 0), td("UAT kho + OT sửa lỗi", 0), td("11.000.000", 0)],
    [td("F", 1), td("In TL + đào tạo + OT Excel", 1), td("9.000.000", 1)]
  ], 6.95, 3.68, 5.83, 3.15, [0.7, 3.4, 1.73]);
  foot(s, 12);
}

// ── 13 Chất lượng ────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  hdr(s, "Kế hoạch quản lý chất lượng · Bảng 1", "Tám mục tiêu chất lượng");
  [["< 1%", "Sai lệch tồn UAT"], ["0", "Tồn âm (NFR-04)"], ["100%", "Thẻ kho gắn phiếu"], ["< 10s", "NXT tháng (NFR-02)"]].forEach((k, i) => {
    kpi(s, 0.4 + i * 3.23, 0.92, 3.13, 0.95, k[0], k[1]);
  });
  tbl(s, [
    [th("STT"), th("Mục tiêu"), th("Chỉ tiêu"), th("Cách kiểm tra")],
    [td("1", 0), td("Tồn kho chính xác", 0), td("Sai lệch < 1% sau kiểm kê thử", 0), td("Kiểm kê thử 1 kho cửa hàng (UAT)", 0)],
    [td("2", 1), td("Không xuất vượt tồn", 1), td("0 tồn âm, kể cả xuất đồng thời", 1), td("NFR-04; CHECK so_luong ≥ 0", 1)],
    [td("3", 0), td("Truy vết đầy đủ", 0), td("100% đổi tồn có thẻ kho; không sửa/xóa", 0), td("Đối chiếu thẻ kho ↔ tồn; thử API", 0)],
    [td("4", 1), td("Báo cáo nhanh và đúng", 1), td("NXT < 10s; đúng QT-06", 1), td("NFR-02; đối chiếu dữ liệu mẫu", 1)],
    [td("5", 0), td("Cảnh báo tồn thấp", 0), td("100% đúng Hết / Sắp hết / Bình thường", 0), td("Biên: 0, = min, = min + 1", 0)],
    [td("6", 1), td("Quản lý biến thể", 1), td("100% màu × size; không trùng SKU", 1), td("Áo size chữ, quần size số", 1)],
    [td("7", 0), td("Hàng tồn lâu", 0), td("100% quá ngưỡng có trong báo cáo", 0), td("Test case ngày nhập khác nhau", 0)],
    [td("8", 1), td("An toàn & phân quyền", 1), td("100% đúng ma trận; 0 lỗ hổng Critical", 1), td("Từng vai trò; NFR-06, NFR-07", 1)]
  ], 0.4, 2.02, 12.53, 3.85, [0.7, 2.6, 5.0, 4.23]);
  [["100%", "Cảnh báo đúng QT-05"], ["SKU", "Không trùng · tồn độc lập"], ["100%", "Hàng tồn lâu đúng ngày"], ["0", "Lỗ hổng Critical"]].forEach((k, i) => {
    kpi(s, 0.4 + i * 3.23, 6.02, 3.13, 0.98, k[0], k[1]);
  });
  foot(s, 13, "Nhóm 1 · CNTT20261_N01 · Chuyển từ mục 1.3.1 PTTK thành chỉ tiêu nghiệm thu");
}

// ── 14 Mốc ───────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: PAPER };
  hdr(s, "Kế hoạch quản lý chất lượng", "Sáu nội dung · sáu mốc · bảy chỉ số");
  const ms = [
    ["M1", "25/09/2026", "Chốt yêu cầu"],
    ["M2", "20/11/2026", "Chốt PTTK"],
    ["M3", "25/12/2026", "Chốt CSDL + UI"],
    ["M4", "15/02/2027", "Xong lập trình"],
    ["M5", "15/03/2027", "Xong kiểm thử"],
    ["M6", "31/03/2027", "Nghiệm thu"]
  ];
  s.addShape(pres.shapes.RECTANGLE, { x: 1.2, y: 1.18, w: 10.9, h: 0.04, fill: { color: RED }, line: { color: RED, width: 0 } });
  ms.forEach((m, i) => {
    const x = 0.4 + i * 2.15;
    box(s, x, 0.92, 2.05, 1.35);
    s.addShape(pres.shapes.OVAL, { x: x + 0.85, y: 1.05, w: 0.28, h: 0.28, fill: { color: RED }, line: { color: WHITE, width: 2 } });
    s.addText(m[0], { x, y: 1.38, w: 2.05, h: 0.28, fontSize: 16, bold: true, color: INK, align: "center", fontFace: FACE, margin: 0 });
    s.addText(m[1], { x, y: 1.64, w: 2.05, h: 0.22, fontSize: 11, color: MUTED, align: "center", fontFace: FACE, margin: 0 });
    s.addText(m[2], { x, y: 1.86, w: 2.05, h: 0.28, fontSize: 12, bold: true, color: INK, align: "center", fontFace: FACE, margin: 0 });
  });
  tbl(s, [
    [th("#"), th("Nội dung"), th("Chỉ tiêu"), th("Phụ trách")],
    [td("1", 0), td("Quản lý yêu cầu", 0), td("10 vấn đề có FR; 100% 19 FR → UC", 0), td("Bùi Tuấn Anh + DN", 0)],
    [td("2", 1), td("Quản lý thiết kế", 1), td("19 UC; CSDL chống tồn âm; 10 MH duyệt", 1), td("Bùi Quốc Luýt + DN", 1)],
    [td("3", 0), td("Kiểm soát lập trình", 0), td("100% PR review; unit test tồn ≥ 80%", 0), td("Bùi Quốc Luýt + nhóm", 0)],
    [td("4", 1), td("Kiểm thử phần mềm", 1), td("100% FR có TC; ≥ 95% đạt; 0 tồn âm", 1), td("Phạm Đoàn Bảo Thiên", 1)],
    [td("5", 0), td("Quản lý lỗi", 0), td("0 Blocker/Critical trước NT (1/2/3 ngày)", 0), td("Luýt + Thiên", 0)],
    [td("6", 1), td("Nghiệm thu & bàn giao", 1), td("Tồn đầu kỳ khớp 100%; TL đủ 3 vai trò", 1), td("Bùi Tuấn Anh + DN", 1)]
  ], 0.4, 2.42, 12.53, 3.2, [0.6, 3.0, 6.1, 2.83]);
  [["100%", "Truy vết FR · mỗi mốc"], ["100%", "PR review · tuần (D)"], ["≥ 80%", "Unit test tồn · mỗi build"], ["≥ 95%", "Test case đạt · tuần (E)"]].forEach((k, i) => {
    kpi(s, 0.4 + i * 3.23, 5.78, 3.13, 1.22, k[0], k[1]);
  });
  foot(s, 14);
}

// ── 15 Cảm ơn ────────────────────────────────────────────
{
  const s = pres.addSlide();
  s.background = { color: RED };
  s.addImage({ path: LOGO, x: 0.5, y: 0.35, w: 0.7, h: 0.7 });
  s.addText("ĐẠI HỌC BÁCH KHOA HÀ NỘI", {
    x: 1.35, y: 0.4, w: 8, h: 0.26, fontSize: 11, bold: true, color: GOLD, fontFace: FACE, margin: 0, charSpacing: 0.8
  });
  s.addText("Trường CNTT&TT · Nhóm 1", {
    x: 1.35, y: 0.68, w: 8, h: 0.3, fontSize: 14, bold: true, color: WHITE, fontFace: FACE, margin: 0
  });
  s.addText("Xin cảm ơn", { x: 0.5, y: 1.2, w: 12.3, h: 0.7, fontSize: 40, bold: true, color: WHITE, fontFace: FACE, margin: 0 });
  s.addText("THẢO LUẬN", { x: 0.5, y: 1.88, w: 12.3, h: 0.3, fontSize: 14, bold: true, color: GOLD, fontFace: FACE, margin: 0, charSpacing: 2 });
  [["Kho trung tâm", "Tồn theo biến thể màu × size"], ["Bàn giao", "31/03/2027 · 408,2 triệu"], ["PTTK 6.1", "19 FR · 11 NFR · 19 UC · 15 bảng · 10 MH"]].forEach((c, i) => {
    const x = 0.5 + i * 4.2;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.32, w: 4.02, h: 0.95, fill: { color: REDD }, line: { color: "E8A0A8", width: 1 }, rectRadius: 0.08 });
    s.addText(c[0].toUpperCase(), { x, y: 2.4, w: 4.02, h: 0.28, fontSize: 11, bold: true, color: GOLD, align: "center", fontFace: FACE, margin: 0 });
    s.addText(c[1], { x: x + 0.1, y: 2.7, w: 3.82, h: 0.45, fontSize: 13, bold: true, color: WHITE, align: "center", fontFace: FACE, margin: 0 });
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: 3.45, w: 6.05, h: 3.45, fill: { color: REDD }, line: { color: "E8A0A8", width: 1 }, rectRadius: 0.08 });
  s.addText("Hạn chế (6.2)", { x: 0.65, y: 3.55, w: 5.75, h: 0.32, fontSize: 14, bold: true, color: GOLD, fontFace: FACE, margin: 0 });
  const lim = ["Chưa nối POS / sàn TMĐT", "Chưa đơn NCC / công nợ", "Chưa tồn theo lô / vị trí", "Giá nhập, chưa BQ / FIFO", "UI phác thảo, chưa test user thật"];
  lim.forEach((c, i) => {
    const x = 0.65 + (i === 4 ? 0 : (i % 2) * 2.9);
    const y = 3.95 + Math.floor(i / 2) * 0.9;
    const w = i === 4 ? 5.75 : 2.8;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.8, fill: { color: "8A1018" }, line: { color: "8A1018", width: 0 }, rectRadius: 0.06 });
    s.addText(c, { x, y, w, h: 0.8, fontSize: 12, color: WHITE, align: "center", valign: "middle", fontFace: FACE, margin: 0 });
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.75, y: 3.45, w: 6.08, h: 3.45, fill: { color: REDD }, line: { color: "E8A0A8", width: 1 }, rectRadius: 0.08 });
  s.addText("Hướng phát triển (6.3)", { x: 6.9, y: 3.55, w: 5.78, h: 0.32, fontSize: 14, bold: true, color: GOLD, fontFace: FACE, margin: 0 });
  const fut = ["API xuất / đổi trả tự động", "Phân hệ đặt hàng NCC", "Tồn vị trí + lô + giá vốn", "App quét mã offline tạm", "Dự báo mùa + điều chuyển tồn lâu"];
  fut.forEach((c, i) => {
    const x = 6.9 + (i === 4 ? 0 : (i % 2) * 2.9);
    const y = 3.95 + Math.floor(i / 2) * 0.9;
    const w = i === 4 ? 5.78 : 2.8;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h: 0.8, fill: { color: "8A1018" }, line: { color: "8A1018", width: 0 }, rectRadius: 0.06 });
    s.addText(c, { x, y, w, h: 0.8, fontSize: 12, color: WHITE, align: "center", valign: "middle", fontFace: FACE, margin: 0 });
  });
  s.addText("CNTT20261_N01 · K6901 CNTT VB2CQ · GVHD ThS. Lê Thị Hoa · Hà Nội, tháng 9 năm 2026", {
    x: 0.5, y: 7.05, w: 12.3, h: 0.28, fontSize: 12, color: "FFD6DA", fontFace: FACE, margin: 0
  });
}

pres.writeFile({ fileName: OUT }).then(() => {
  console.log("wrote", OUT);
}).catch((e) => {
  console.error(e);
  process.exit(1);
});
