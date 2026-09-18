import fs from "node:fs/promises";
import crypto from "node:crypto";
import path from "node:path";
import { pathToFileURL } from "node:url";

const SKILL_DIR = "C:/Users/GHC/.codex/plugins/cache/openai-primary-runtime/presentations/26.909.11809/skills/presentations";
const workspaceDir = "C:/Dev/Learning";
const sourcePath = path.join(workspaceDir, "VIII.HUST/Quản trị dự án/slide/slide-thuyet-trinh.pptx");
const buildDir = path.join(workspaceDir, ".codex-pm-build");
const stagingDir = path.join(workspaceDir, ".codex-finalizer");
const outputDir = path.join(workspaceDir, "output");
await fs.mkdir(buildDir, { recursive: true });
await fs.mkdir(stagingDir, { recursive: true });
await fs.mkdir(outputDir, { recursive: true });

const { importRuntimeModule } = await import(
  pathToFileURL(path.join(SKILL_DIR, "container_tools/runtime_helpers.mjs")).href,
);
const { FileBlob, PresentationFile } = await importRuntimeModule("@oai/artifact-tool");
const { applyPresentationChartFont } = await import(
  pathToFileURL(path.join(SKILL_DIR, "container_tools/artifact_tool_utils.mjs")).href,
);

const presentation = await PresentationFile.importPptx(await FileBlob.load(sourcePath));
const FONT = "Calibri";
const C = {
  red: "#C81028",
  redDark: "#9F0E21",
  redSoft: "#FFF1F3",
  redPale: "#FFF8F9",
  redLine: "#E8D9DC",
  dark: "#1A1A1A",
  gray: "#626262",
  grayLight: "#F6F6F6",
  green: "#237A4B",
  greenPale: "#EEF8F1",
  amber: "#9A6500",
  amberPale: "#FFF7E6",
  white: "#FFFFFF",
};
const transparentLine = { style: "solid", fill: "none", width: 0 };
const solidLine = (fill = C.redLine, width = 1) => ({ style: "solid", fill, width });

function clearSlide(slide, { keepImages = false } = {}) {
  slide.shapes.deleteAll();
  if (!keepImages) {
    for (const item of [...(slide.images.items ?? [])]) slide.images.deleteById(item.id);
  }
  for (const item of [...(slide.tables.items ?? [])]) slide.tables.deleteById(item.id);
  for (const item of [...(slide.charts.items ?? [])]) slide.charts.deleteById(item.id);
  slide.speakerNotes.textFrame.setText("");
}

function addText(slide, value, left, top, width, height, options = {}) {
  const shape = slide.shapes.add({
    geometry: "textbox",
    name: options.name,
    position: { left, top, width, height },
    fill: "none",
    line: transparentLine,
  });
  shape.text = value;
  shape.text.style = {
    typeface: FONT,
    fontSize: options.fontSize ?? 16,
    color: options.color ?? C.dark,
    bold: options.bold ?? false,
    italic: options.italic ?? false,
    alignment: options.alignment ?? "left",
  };
  return shape;
}

function addSurface(slide, left, top, width, height, options = {}) {
  return slide.shapes.add({
    geometry: options.geometry ?? "roundRect",
    name: options.name,
    position: { left, top, width, height },
    fill: options.fill ?? C.white,
    line: options.line ?? solidLine(C.redLine, 1),
    borderRadius: options.radius ?? 10,
  });
}

function addCard(slide, { left, top, width, height, title, body, fill = C.white, titleColor = C.red, bodyColor = C.dark, titleSize = 15, bodySize = 14, titleHeight = 30, padding = 12 }) {
  addSurface(slide, left, top, width, height, { fill });
  addText(slide, title, left + padding, top + 8, width - padding * 2, titleHeight, { fontSize: titleSize, bold: true, color: titleColor });
  if (body) addText(slide, body, left + padding, top + 8 + titleHeight, width - padding * 2, height - titleHeight - 16, { fontSize: bodySize, color: bodyColor });
}

function addMetric(slide, { left, top, width, height, label, value, fill = C.white, labelColor = C.red, valueColor = C.dark, valueSize = 22 }) {
  addSurface(slide, left, top, width, height, { fill });
  addText(slide, label, left + 10, top + 9, width - 20, 20, { fontSize: 12, bold: true, color: labelColor });
  addText(slide, value, left + 10, top + 34, width - 20, height - 42, { fontSize: valueSize, bold: true, color: valueColor });
}

function addHeader(slide, title, subtitle, page, note = "") {
  slide.background.fill = C.white;
  addText(slide, title, 38, 14, 1200, 27, { fontSize: 16, bold: true, color: C.red });
  addText(slide, subtitle, 38, 39, 1200, 36, { fontSize: 22, bold: true, color: C.dark });
  slide.shapes.add({ geometry: "rect", position: { left: 38, top: 682, width: 1203, height: 1.5 }, fill: C.redLine, line: transparentLine });
  addText(slide, "Nhóm 1 · CNTT20261_N01 · Quản trị dự án CNTT", 38, 689, 830, 20, { fontSize: 11, color: C.gray });
  addText(slide, `Trang ${page} / 15`, 988, 689, 252, 20, { fontSize: 11, color: C.gray, alignment: "right" });
  if (note) slide.speakerNotes.textFrame.setText(note);
}

function addBullets(slide, items, left, top, width, height, options = {}) {
  return addText(slide, items.map(item => `• ${item}`).join("\n"), left, top, width, height, { fontSize: options.fontSize ?? 15, color: options.color ?? C.dark });
}

function addTable(slide, values, { left, top, width, height, tracks, fontSize = 12, headerFontSize = 12, bodyFill = C.white, headerFill = C.red, bodyColor = C.dark, headerColor = C.white, banded = true }) {
  const table = slide.tables.add({ rows: values.length, columns: values[0].length, left, top, width, height, values, columnTracks: tracks });
  table.borders.assign({ style: "solid", fill: C.redLine, width: 1 });
  table.cells.block({ row: 0, column: 0, rowCount: 1, columnCount: values[0].length }).assign({
    fill: headerFill,
    textStyle: { typeface: FONT, fontSize: headerFontSize, bold: true, color: headerColor },
  });
  if (values.length > 1) {
    table.cells.block({ row: 1, column: 0, rowCount: values.length - 1, columnCount: values[0].length }).assign({
      fill: bodyFill,
      textStyle: { typeface: FONT, fontSize, color: bodyColor },
    });
    if (banded) {
      for (let r = 2; r < values.length; r += 2) {
        table.cells.block({ row: r, column: 0, rowCount: 1, columnCount: values[0].length }).assign({ fill: C.redPale });
      }
    }
  }
  table.styleOptions = { headerRow: true, bandedRows: banded };
  return table;
}

function addPhaseBar(slide, phases, left, top, width, height = 56) {
  const gap = 8;
  const itemWidth = (width - gap * (phases.length - 1)) / phases.length;
  phases.forEach((phase, index) => {
    const x = left + index * (itemWidth + gap);
    addSurface(slide, x, top, itemWidth, height, { fill: index % 2 ? C.redPale : C.redSoft, radius: 8 });
    addText(slide, phase, x + 6, top + 14, itemWidth - 12, height - 20, { fontSize: 13, bold: true, color: C.red, alignment: "center" });
  });
}

const notes = {
  ch1: "Nguồn kiến thức: C:\\Users\\GHC\\Downloads\\Slide\\Chuong 01 - Cac van de chung.pptx. Dữ liệu dự án: slide-thuyet-trinh.pptx.",
  ch2: "Nguồn kiến thức: C:\\Users\\GHC\\Downloads\\Slide\\Chuong 02 - Du an Cong nghe thong tin.pptx. Dữ liệu dự án: slide-thuyet-trinh.pptx.",
  ch3: "Nguồn kiến thức: C:\\Users\\GHC\\Downloads\\Slide\\Chuong 3_QLDA.pdf. Dữ liệu lịch biểu: slide-thuyet-trinh.pptx.",
  ch4: "Nguồn kiến thức: C:\\Users\\GHC\\Downloads\\Slide\\Chuong 04 - Quan ly thoi gian du an.pptx. Dữ liệu WBS: slide-thuyet-trinh.pptx.",
  ch5: "Nguồn kiến thức: C:\\Users\\GHC\\Downloads\\Slide\\Chuong 05 - Quan ly chi phi du an [Autosaved].pptx. Dữ liệu dự toán: slide-thuyet-trinh.pptx.",
  ch6: "Nguồn kiến thức: C:\\Users\\GHC\\Downloads\\Slide\\Chuong 06 - Quan ly chat luong du an.pptx. Chỉ tiêu chất lượng: slide-thuyet-trinh.pptx.",
  ch7: "Nguồn kiến thức: C:\\Users\\GHC\\Downloads\\Slide\\Chuong 07 - Quan ly nhan luc.pptx. Dữ liệu phân công: slide-thuyet-trinh.pptx.",
  ch8: "Nguồn kiến thức: C:\\Users\\GHC\\Downloads\\Slide\\Chuong 08 - Quan ly rui ro.pptx. Các rủi ro trình bày là đăng ký theo dõi đề xuất cho dự án nhóm 1, không phải kết luận đã xảy ra.",
};

const slides = presentation.slides.items;
if (slides.length !== 15) throw new Error(`Expected 15 source slides, found ${slides.length}`);
slides.forEach((slide, index) => clearSlide(slide, { keepImages: index === 14 }));

// 1. Cover
{
  const slide = slides[0];
  slide.background.fill = C.white;
  const coverBackground = slide.shapes.add({ geometry: "rect", position: { left: 0, top: 0, width: 715, height: 720 }, fill: C.red, line: transparentLine });
  coverBackground.sendToBack();
  const logoBytes = await fs.readFile(path.join(workspaceDir, "VIII.HUST/Quản trị dự án/slide/hust-logo.png"));
  slide.images.add({ blob: logoBytes, contentType: "image/png", alt: "HUST logo", fit: "contain", position: { left: 43.2, top: 36.48, width: 69.12, height: 69.12 } });
  addText(slide, "ĐẠI HỌC BÁCH KHOA HÀ NỘI", 122, 40, 566, 26, { fontSize: 20, bold: true, color: C.white });
  addText(slide, "Trường Công nghệ Thông tin và Truyền thông", 122, 67, 566, 28, { fontSize: 15, color: C.white });
  addText(slide, "BÀI TẬP LỚN · CNTT20261_N01", 42, 128, 260, 28, { fontSize: 14, bold: true, color: C.white });
  addText(slide, "QUẢN TRỊ DỰ ÁN CNTT", 42, 177, 620, 55, { fontSize: 34, bold: true, color: C.white });
  addText(slide, "Dự án xây dựng hệ thống quản lý hàng hóa và kho bãi sản phẩm thời trang", 42, 240, 620, 85, { fontSize: 21, bold: true, color: C.white });
  addText(slide, "Báo cáo áp dụng kiến thức quản trị dự án", 42, 337, 620, 28, { fontSize: 16, color: C.white });
  addMetric(slide, { left: 42, top: 400, width: 190, height: 90, label: "THỜI GIAN", value: "01/09/2026 -\n31/03/2027", fill: C.redDark, labelColor: C.white, valueColor: C.white, valueSize: 15 });
  addMetric(slide, { left: 252, top: 400, width: 190, height: 90, label: "NGÂN SÁCH", value: "408,2\ntriệu VNĐ", fill: C.redDark, labelColor: C.white, valueColor: C.white, valueSize: 18 });
  addMetric(slide, { left: 462, top: 400, width: 190, height: 90, label: "QUY MÔ", value: "5 thành viên\n52 task", fill: C.redDark, labelColor: C.white, valueColor: C.white, valueSize: 17 });
  addText(slide, "TRỌNG TÂM QUẢN LÝ", 42, 535, 250, 22, { fontSize: 12, bold: true, color: C.white });
  addText(slide, "Phạm vi · Thời gian · Chi phí · Chất lượng · Nhân lực · Rủi ro", 42, 560, 620, 45, { fontSize: 15, color: C.white });
  addText(slide, "NHÓM 1 · LỚP K6901 CNTT VB2CQ", 739, 36, 499, 24, { fontSize: 14, bold: true, color: C.red });
  addText(slide, "Thành viên và vai trò", 739, 62, 499, 32, { fontSize: 22, bold: true, color: C.dark });
  const members = [
    ["TA", "Bùi Tuấn Anh · 202490032", "Giám đốc dự án, phân tích nghiệp vụ"],
    ["QL", "Bùi Quốc Luýt · 202490069", "Trưởng nhóm kỹ thuật, back-end"],
    ["QM", "Vũ Quang Minh · 202490071", "Lập trình back-end"],
    ["MQ", "Bạch Minh Quang · 202490077", "UI/UX và front-end"],
    ["BT", "Phạm Đoàn Bảo Thiên · 202490090", "CSDL và kiểm thử"],
  ];
  members.forEach(([initials, name, role], index) => {
    const y = 112 + index * 74;
    addSurface(slide, 739, y, 40, 40, { fill: C.red, line: solidLine(C.red, 1), radius: 20 });
    addText(slide, initials, 739, y + 8, 40, 20, { fontSize: 12, bold: true, color: C.white, alignment: "center" });
    addText(slide, name, 792, y - 6, 446, 28, { fontSize: 15, bold: true, color: C.dark });
    addText(slide, role, 792, y + 22, 446, 23, { fontSize: 13, color: C.gray });
  });
  addSurface(slide, 739, 484, 499, 196, { fill: C.redPale });
  addText(slide, "BỘ HỒ SƠ QUẢN TRỊ", 753, 494, 470, 28, { fontSize: 15, bold: true, color: C.red });
  addPhaseBar(slide, ["Tôn chỉ", "WBS", "Dự toán", "Chất lượng", "Rủi ro"], 753, 540, 470, 82);
  addText(slide, "GVHD: ThS. Lê Thị Hoa", 753, 642, 470, 24, { fontSize: 13, color: C.gray });
  slide.speakerNotes.textFrame.setText("Dữ liệu bìa và nhóm: slide-thuyet-trinh.pptx. Nội dung được định hướng lại theo các chương quản trị dự án trong C:\\Users\\GHC\\Downloads\\Slide.");
}

// 2. Course scope
{
  const slide = slides[1];
  addHeader(slide, "MÔN HỌC VÀ PHẠM VI ÁP DỤNG", "8 lĩnh vực quản lý được vận dụng trong dự án nhóm 1", 2, notes.ch1);
  addCard(slide, { left: 38, top: 92, width: 380, height: 64, title: "Mục tiêu môn học", body: "Nắm phương pháp và kỹ năng quản trị dự án CNTT", fill: C.redSoft, titleSize: 13, bodySize: 13, titleHeight: 20, padding: 10 });
  addCard(slide, { left: 450, top: 92, width: 380, height: 64, title: "Đối tượng quản lý", body: "Công việc, con người, nguồn lực và các bên liên quan", fill: C.redSoft, titleSize: 13, bodySize: 13, titleHeight: 20, padding: 10 });
  addCard(slide, { left: 862, top: 92, width: 379, height: 64, title: "Kết quả hướng tới", body: "Bàn giao đúng phạm vi, thời hạn, ngân sách và chất lượng", fill: C.redSoft, titleSize: 13, bodySize: 13, titleHeight: 20, padding: 10 });
  const fields = [
    ["Tổng thể", "Kết nối các kế hoạch thành một baseline"],
    ["Phạm vi", "Xác định in-scope và out-of-scope"],
    ["Thời gian", "WBS, phụ thuộc, mốc, PERT và Gantt"],
    ["Chi phí", "Ước lượng, ngân sách, CV và CPI"],
    ["Chất lượng", "Tiêu chuẩn, đảm bảo, kiểm soát, nghiệm thu"],
    ["Nhân lực", "Cơ cấu, phân vai, phát triển nhóm"],
    ["Thông tin", "Báo cáo, trao đổi và xác nhận"],
    ["Rủi ro", "Nhận diện, đánh giá, đáp ứng, theo dõi"],
    ["Hợp đồng", "Nguồn cung, dịch vụ và bàn giao"],
  ];
  fields.forEach(([title, body], index) => {
    const col = index % 3;
    const row = Math.floor(index / 3);
    addCard(slide, { left: 38 + col * 412, top: 180 + row * 112, width: col === 2 ? 379 : 380, height: 96, title, body, fill: index % 2 ? C.white : C.redPale, titleSize: 16, bodySize: 14, titleHeight: 26 });
  });
  addSurface(slide, 38, 530, 1203, 112, { fill: C.grayLight });
  addText(slide, "Thông điệp trọng tâm", 54, 548, 250, 24, { fontSize: 15, bold: true, color: C.red });
  addText(slide, "Phần mềm là sản phẩm của dự án. Môn học tập trung vào cách tổ chức, lập kế hoạch, điều phối và kiểm soát để tạo ra sản phẩm đó.", 54, 578, 1145, 44, { fontSize: 18, color: C.dark });
}

// 3. Project nature
{
  const slide = slides[2];
  addHeader(slide, "BẢN CHẤT CỦA DỰ ÁN", "Dự án khác hoạt động nghiệp vụ ở mục tiêu, thời hạn và nguồn lực", 3, notes.ch1);
  addSurface(slide, 38, 92, 580, 270, { fill: C.white });
  addText(slide, "Theo tài liệu môn học", 54, 106, 540, 28, { fontSize: 17, bold: true, color: C.red });
  addBullets(slide, [
    "Tập hợp công việc do nhiều người cùng thực hiện",
    "Tạo ra một sản phẩm hoặc kết quả mới",
    "Có ngày bắt đầu và ngày kết thúc",
    "Có kinh phí và nguồn lực được dự kiến",
    "Được quản lý theo mục tiêu đã thống nhất",
  ], 54, 145, 540, 190, { fontSize: 16 });
  addSurface(slide, 648, 92, 593, 270, { fill: C.redPale });
  addText(slide, "Dự án nhóm 1", 664, 106, 560, 28, { fontSize: 17, bold: true, color: C.red });
  const projectTraits = [
    ["Một lần", "Xây dựng một hệ thống và bộ hồ sơ cụ thể"],
    ["Có thời hạn", "01/09/2026 đến 31/03/2027"],
    ["Có giới hạn", "408.196.650 VNĐ và 5 thành viên"],
    ["Có kết quả", "Bàn giao sản phẩm, tài liệu và nghiệm thu"],
  ];
  projectTraits.forEach(([t, b], i) => addCard(slide, { left: 664 + (i % 2) * 278, top: 145 + Math.floor(i / 2) * 100, width: 264, height: 82, title: t, body: b, fill: C.white, titleSize: 15, bodySize: 13, titleHeight: 22, padding: 10 }));
  addText(slide, "TAM GIÁC RÀNG BUỘC", 38, 394, 300, 26, { fontSize: 15, bold: true, color: C.red });
  addCard(slide, { left: 38, top: 432, width: 270, height: 142, title: "PHẠM VI", body: "Công việc nào thuộc dự án và công việc nào nằm ngoài phạm vi", fill: C.redPale, titleSize: 17, bodySize: 15, titleHeight: 26 });
  addCard(slide, { left: 334, top: 432, width: 270, height: 142, title: "THỜI GIAN", body: "Mốc bắt đầu, kết thúc, phụ thuộc và đường găng", fill: C.redPale, titleSize: 17, bodySize: 15, titleHeight: 26 });
  addCard(slide, { left: 630, top: 432, width: 270, height: 142, title: "CHI PHÍ", body: "Ngân sách được phân bổ theo gói công việc và kiểm soát", fill: C.redPale, titleSize: 17, bodySize: 15, titleHeight: 26 });
  addCard(slide, { left: 926, top: 432, width: 315, height: 142, title: "KẾT QUẢ", body: "Chất lượng phải đáp ứng tiêu chí nghiệm thu của khách hàng", fill: C.redSoft, titleSize: 17, bodySize: 15, titleHeight: 26 });
}

// 4. Lifecycle
{
  const slide = slides[3];
  addHeader(slide, "VÒNG ĐỜI DỰ ÁN", "Từ ý tưởng đến bàn giao và giải phóng nguồn lực", 4, notes.ch2);
  const phases = [
    ["1", "XÂY DỰNG Ý TƯỞNG", "Mục tiêu\nTính khả thi\nNguồn lực và rủi ro"],
    ["2", "PHÁT TRIỂN", "Thành lập nhóm\nWBS và lịch\nNgân sách và kế hoạch"],
    ["3", "THỰC HIỆN", "Huy động nguồn lực\nTriển khai công việc\nTheo dõi và hiệu chỉnh"],
    ["4", "KẾT THÚC", "Bàn giao và ký nhận\nQuyết toán\nLưu hồ sơ, giải phóng nguồn lực"],
  ];
  phases.forEach(([n, title, body], index) => {
    const x = 38 + index * 301;
    addSurface(slide, x, 108, 280, 220, { fill: index % 2 ? C.redPale : C.white });
    addSurface(slide, x + 14, 122, 36, 36, { fill: C.red, line: solidLine(C.red, 1), radius: 18 });
    addText(slide, n, x + 14, 131, 36, 20, { fontSize: 14, bold: true, color: C.white, alignment: "center" });
    addText(slide, title, x + 62, 126, 200, 28, { fontSize: 15, bold: true, color: C.red });
    addText(slide, body, x + 18, 180, 244, 120, { fontSize: 16, color: C.dark });
    if (index < phases.length - 1) slide.shapes.add({ geometry: "rect", position: { left: x + 280, top: 212, width: 21, height: 3 }, fill: C.red, line: transparentLine });
  });
  addText(slide, "CÁC GIAI ĐOẠN DỰ ÁN CNTT", 38, 370, 420, 26, { fontSize: 15, bold: true, color: C.red });
  addPhaseBar(slide, ["Mục tiêu / phạm vi", "Phân tích", "Thiết kế", "Phát triển", "Kiểm thử", "Triển khai"], 38, 410, 1203, 70);
  addSurface(slide, 38, 520, 1203, 105, { fill: C.grayLight });
  addText(slide, "Góc nhìn quản trị", 54, 538, 220, 24, { fontSize: 15, bold: true, color: C.red });
  addText(slide, "Vòng đời cho biết dự án đang ở đâu, cần quyết định gì và bộ hồ sơ nào phải hoàn thành trước khi chuyển sang giai đoạn tiếp theo.", 54, 570, 1145, 38, { fontSize: 18, color: C.dark });
}

// 5. Stakeholders
{
  const slide = slides[4];
  addHeader(slide, "CÁC BÊN LIÊN QUAN", "Xác định sớm ai quyết định, ai cung cấp nguồn lực và ai nhận kết quả", 5, notes.ch1);
  const center = { left: 474, top: 255, width: 332, height: 96 };
  addSurface(slide, 38, 120, 330, 110, { fill: C.redPale });
  addText(slide, "NHÀ TÀI TRỢ / CHỦ ĐẦU TƯ", 54, 136, 300, 24, { fontSize: 15, bold: true, color: C.red });
  addText(slide, "Phê duyệt tôn chỉ, nguồn lực và kết quả", 54, 170, 300, 38, { fontSize: 15, color: C.dark });
  addSurface(slide, 910, 120, 331, 110, { fill: C.redPale });
  addText(slide, "KHÁCH HÀNG / NGƯỜI DÙNG", 926, 136, 300, 24, { fontSize: 15, bold: true, color: C.red });
  addText(slide, "Xác định nhu cầu và xác nhận nghiệm thu", 926, 170, 300, 38, { fontSize: 15, color: C.dark });
  addSurface(slide, 38, 440, 330, 110, { fill: C.redPale });
  addText(slide, "GIÁM ĐỐC DỰ ÁN", 54, 456, 300, 24, { fontSize: 15, bold: true, color: C.red });
  addText(slide, "Lập kế hoạch, điều phối, báo cáo và xử lý thay đổi", 54, 490, 300, 42, { fontSize: 15, color: C.dark });
  addSurface(slide, 910, 440, 331, 110, { fill: C.redPale });
  addText(slide, "ĐỘI DỰ ÁN / NHÀ CUNG CẤP", 926, 456, 300, 24, { fontSize: 15, bold: true, color: C.red });
  addText(slide, "Thực hiện công việc và cung cấp nguồn lực", 926, 490, 300, 42, { fontSize: 15, color: C.dark });
  slide.shapes.add({ geometry: "rect", position: { left: 368, top: 174, width: 108, height: 3 }, fill: C.redLine, line: transparentLine });
  slide.shapes.add({ geometry: "rect", position: { left: 806, top: 174, width: 104, height: 3 }, fill: C.redLine, line: transparentLine });
  slide.shapes.add({ geometry: "rect", position: { left: 368, top: 494, width: 108, height: 3 }, fill: C.redLine, line: transparentLine });
  slide.shapes.add({ geometry: "rect", position: { left: 806, top: 494, width: 104, height: 3 }, fill: C.redLine, line: transparentLine });
  addSurface(slide, center.left, center.top, center.width, center.height, { fill: C.red, line: solidLine(C.red, 1), radius: 14 });
  addText(slide, "DỰ ÁN NHÓM 1", center.left + 18, center.top + 18, center.width - 36, 24, { fontSize: 16, bold: true, color: C.white, alignment: "center" });
  addText(slide, "Quản lý hàng hóa và kho bãi\nsản phẩm thời trang", center.left + 18, center.top + 48, center.width - 36, 38, { fontSize: 16, bold: true, color: C.white, alignment: "center" });
  addSurface(slide, 38, 590, 1203, 54, { fill: C.grayLight });
  addText(slide, "Áp dụng thực tế: DN thời trang là đơn vị khảo sát; Bùi Tuấn Anh là Giám đốc dự án; đội dự án gồm 5 thành viên.", 54, 605, 1168, 24, { fontSize: 16, color: C.dark });
}

// 6. PM role
{
  const slide = slides[5];
  addHeader(slide, "VAI TRÒ GIÁM ĐỐC DỰ ÁN", "Giám đốc dự án là đầu mối chịu trách nhiệm về kế hoạch tổng thể", 6, notes.ch1);
  addSurface(slide, 38, 100, 330, 500, { fill: C.redPale });
  addText(slide, "BÙI TUẤN ANH", 58, 124, 290, 30, { fontSize: 22, bold: true, color: C.red });
  addText(slide, "Giám đốc dự án\nPhân tích nghiệp vụ", 58, 164, 290, 55, { fontSize: 17, color: C.dark });
  addText(slide, "Trách nhiệm chính", 58, 250, 280, 24, { fontSize: 16, bold: true, color: C.red });
  addBullets(slide, ["Lập kế hoạch tổng thể", "Phối hợp các bên liên quan", "Theo dõi thời gian và kinh phí", "Giải quyết vấn đề và thay đổi", "Báo cáo và chuẩn bị nghiệm thu"], 58, 286, 276, 230, { fontSize: 16 });
  addText(slide, "Đầu mối giữa khách hàng, đội dự án và cấp quản lý", 58, 540, 276, 44, { fontSize: 15, bold: true, color: C.red });
  addText(slide, "CÔNG VIỆC CỦA PM THEO VÒNG ĐỜI", 408, 100, 780, 26, { fontSize: 15, bold: true, color: C.red });
  const pmStages = [
    ["KHỞI ĐỘNG", "Công bố tôn chỉ\nXác định mục tiêu"],
    ["LẬP KẾ HOẠCH", "WBS, lịch biểu\nNgân sách, nguồn lực"],
    ["THỰC HIỆN", "Họp và phối hợp\nTháo gỡ vướng mắc"],
    ["KIỂM SOÁT", "Tiến độ, chi phí\nChất lượng, thay đổi"],
    ["KẾT THÚC", "Nghiệm thu\nBàn giao và lưu hồ sơ"],
  ];
  pmStages.forEach(([title, body], index) => {
    const x = 408 + (index % 2) * 400;
    const y = 145 + Math.floor(index / 2) * 122;
    addCard(slide, { left: x, top: y, width: 366, height: 96, title, body, fill: index === 4 ? C.redSoft : C.white, titleSize: 16, bodySize: 15, titleHeight: 24 });
  });
  addSurface(slide, 408, 535, 780, 65, { fill: C.grayLight });
  addText(slide, "Kỹ năng cốt lõi", 426, 551, 160, 22, { fontSize: 15, bold: true, color: C.red });
  addText(slide, "Lập kế hoạch · Giao tiếp · Thương lượng · Ra quyết định · Giải quyết xung đột", 590, 551, 576, 30, { fontSize: 15, color: C.dark });
}

// 7. Charter
{
  const slide = slides[6];
  addHeader(slide, "TÔN CHỈ DỰ ÁN", "Baseline để thống nhất mục tiêu, phạm vi, thời hạn và kinh phí", 7, notes.ch1);
  addMetric(slide, { left: 38, top: 92, width: 280, height: 72, label: "THỜI HẠN", value: "01/09/2026 - 31/03/2027", fill: C.redPale, valueSize: 16 });
  addMetric(slide, { left: 348, top: 92, width: 280, height: 72, label: "NGÂN SÁCH", value: "408.196.650 VNĐ", fill: C.redPale, valueSize: 18 });
  addMetric(slide, { left: 658, top: 92, width: 280, height: 72, label: "GIÁM ĐỐC DỰ ÁN", value: "Bùi Tuấn Anh", fill: C.redPale, valueSize: 18 });
  addMetric(slide, { left: 968, top: 92, width: 273, height: 72, label: "QUY MÔ", value: "5 thành viên · 52 task", fill: C.redPale, valueSize: 16 });
  addTable(slide, [
    ["Thành phần", "Nội dung"],
    ["Mục đích", "Quản lý hàng hóa và kho bãi sản phẩm thời trang"],
    ["Chủ đầu tư", "Doanh nghiệp thời trang tại đơn vị khảo sát"],
    ["Kết quả bàn giao", "Sản phẩm hệ thống, bộ hồ sơ quản trị và biên bản nghiệm thu"],
    ["Thời hạn", "Bàn giao ngày 31/03/2027"],
    ["Ngân sách", "408.196.650 VNĐ, theo dự toán được lập"],
  ], { left: 38, top: 194, width: 760, height: 300, tracks: [{ mode: "fr", value: 1 }, { mode: "fr", value: 2.7 }], fontSize: 14, headerFontSize: 14 });
  addSurface(slide, 830, 194, 411, 300, { fill: C.redPale });
  addText(slide, "TIÊU CHÍ THÀNH CÔNG", 850, 214, 370, 28, { fontSize: 17, bold: true, color: C.red });
  addBullets(slide, ["Bàn giao đúng thời hạn", "Tuân thủ ngân sách", "Phạm vi được phê duyệt", "Chất lượng đáp ứng tiêu chí nghiệm thu", "Hồ sơ và trách nhiệm được xác nhận"], 850, 260, 360, 180, { fontSize: 16 });
  addSurface(slide, 38, 528, 1203, 94, { fill: C.grayLight });
  addText(slide, "Tôn chỉ là điểm tham chiếu", 54, 548, 280, 24, { fontSize: 15, bold: true, color: C.red });
  addText(slide, "Mọi thay đổi lớn phải được xem xét theo ảnh hưởng tới phạm vi, thời gian, chi phí và chất lượng trước khi phê duyệt.", 54, 577, 1148, 34, { fontSize: 17, color: C.dark });
}

// 8. Scope/change
{
  const slide = slides[7];
  addHeader(slide, "QUẢN LÝ PHẠM VI VÀ THAY ĐỔI", "Phạm vi rõ giúp hạn chế mở rộng ngoài kiểm soát", 8, notes.ch2);
  addSurface(slide, 38, 92, 580, 330, { fill: C.greenPale, line: solidLine("#B7DFC5", 1) });
  addText(slide, "IN-SCOPE", 56, 110, 540, 28, { fontSize: 18, bold: true, color: C.green });
  addBullets(slide, [
    "Phân tích, thiết kế, lập trình và kiểm thử",
    "Tài khoản và phân quyền",
    "Sản phẩm, biến thể, nhà cung cấp, kho, vị trí",
    "Nhập, xuất, chuyển, hủy",
    "Kiểm kê và điều chỉnh có phê duyệt",
    "Tra cứu, cảnh báo, thẻ kho",
    "Chuyển đổi Excel đầu kỳ, đào tạo, bàn giao",
  ], 56, 150, 540, 240, { fontSize: 15 });
  addSurface(slide, 661, 92, 580, 330, { fill: C.redPale });
  addText(slide, "OUT-OF-SCOPE", 679, 110, 540, 28, { fontSize: 18, bold: true, color: C.red });
  addBullets(slide, [
    "POS, thanh toán và hóa đơn điện tử",
    "Đơn đặt nhà cung cấp và công nợ",
    "Kế toán giá vốn và định khoản",
    "Sàn thương mại điện tử và vận chuyển",
    "Chăm sóc khách hàng và khuyến mãi",
    "Ứng dụng di động riêng",
    "Mua tablet và máy quét",
  ], 679, 150, 540, 240, { fontSize: 15 });
  addText(slide, "QUY TRÌNH KIỂM SOÁT THAY ĐỔI", 38, 454, 520, 26, { fontSize: 15, bold: true, color: C.red });
  const changeSteps = ["Ghi nhận yêu cầu", "Phân tích ảnh hưởng", "Phê duyệt", "Cập nhật baseline và truyền thông"];
  changeSteps.forEach((step, index) => {
    const x = 38 + index * 301;
    addSurface(slide, x, 500, 280, 94, { fill: index === 2 ? C.redSoft : C.white });
    addSurface(slide, x + 12, 514, 30, 30, { fill: C.red, line: solidLine(C.red, 1), radius: 15 });
    addText(slide, String(index + 1), x + 12, 521, 30, 18, { fontSize: 12, bold: true, color: C.white, alignment: "center" });
    addText(slide, step, x + 54, 520, 204, 42, { fontSize: 15, bold: true, color: C.dark });
    if (index < changeSteps.length - 1) slide.shapes.add({ geometry: "rect", position: { left: x + 280, top: 544, width: 21, height: 3 }, fill: C.redLine, line: transparentLine });
  });
}

// 9. WBS and people
{
  const slide = slides[8];
  addHeader(slide, "WBS VÀ QUẢN LÝ NGUỒN NHÂN LỰC", "WBS biến mục tiêu thành gói công việc có người chịu trách nhiệm", 9, notes.ch7);
  addSurface(slide, 38, 92, 470, 214, { fill: C.redPale });
  addText(slide, "WBS · 6 GIAI ĐOẠN", 56, 110, 430, 26, { fontSize: 17, bold: true, color: C.red });
  const wbs = ["A · Khảo sát và yêu cầu", "B · Phân tích và thiết kế", "C · CSDL và UI/UX", "D · Phát triển", "E · Kiểm thử", "F · Nghiệm thu và bàn giao"];
  wbs.forEach((value, index) => addText(slide, value, 60, 148 + index * 24, 405, 20, { fontSize: 14, color: C.dark }));
  addSurface(slide, 534, 92, 707, 214, { fill: C.white });
  addText(slide, "NGUYÊN TẮC PHÂN BỔ NGUỒN LỰC", 552, 110, 670, 26, { fontSize: 17, bold: true, color: C.red });
  addBullets(slide, ["Phân công theo năng lực và gói công việc", "PM điều phối, Tech Lead dẫn kỹ thuật", "QA chéo trong nhóm, không tách bộ phận QA riêng", "Theo dõi ngày-người và tải công việc theo giai đoạn"], 552, 150, 640, 120, { fontSize: 15 });
  addTable(slide, [
    ["Thành viên", "Vai trò", "Giai đoạn chính", "Ngày-người EST"],
    ["Bùi Tuấn Anh", "PM, nghiệp vụ", "A, B, C, E, F", "43,27"],
    ["Bùi Quốc Luýt", "Tech Lead, back-end", "B, D, E", "48,95"],
    ["Vũ Quang Minh", "Back-end", "B, D, E", "41,98"],
    ["Bạch Minh Quang", "UI/UX, front-end", "A, C, D, E", "44,00"],
    ["Phạm Đoàn Bảo Thiên", "CSDL, kiểm thử", "B, C, E, F", "43,63"],
    ["Tổng", "", "", "221,83"],
  ], { left: 38, top: 330, width: 1203, height: 290, tracks: [{ mode: "fr", value: 1.3 }, { mode: "fr", value: 1.5 }, { mode: "fr", value: 1.2 }, { mode: "fr", value: 0.8 }], fontSize: 13, headerFontSize: 13 });
  addText(slide, "EST chốt: 221,83 ngày-người · hệ số chủ trì 0,75 · thành viên chính 0,45", 38, 635, 1203, 24, { fontSize: 14, color: C.gray });
}

// 10. Schedule
{
  const slide = slides[9];
  addHeader(slide, "QUẢN LÝ THỜI GIAN: WBS, PHỤ THUỘC VÀ MỐC", "WBS là nền để lập lịch và theo dõi tiến độ", 10, notes.ch3);
  addTable(slide, [
    ["GĐ", "Thời gian", "Task", "Sản phẩm", "Phụ thuộc"],
    ["A", "01/09 - 25/09/2026", "1 - 8", "Khảo sát và đặc tả yêu cầu", "5 sau 1 - 4; 8 sau 7"],
    ["B", "26/09 - 20/11/2026", "9 - 17", "Báo cáo PTTK", "Sau Task 8"],
    ["C", "21/11 - 25/12/2026", "18 - 25", "CSDL và thiết kế UI/UX", "Sau Task 17"],
    ["D", "26/12 - 15/02/2027", "26 - 39", "Mã nguồn và module chạy được", "Sau Task 20"],
    ["E", "16/02 - 15/03/2027", "40 - 47", "Báo cáo kiểm thử", "Sau 39; UAT sau 41 - 45"],
    ["F", "16/03 - 31/03/2027", "48 - 52", "Cấu hình, nghiệm thu, bàn giao", "Sau Task 47"],
  ], { left: 38, top: 92, width: 1203, height: 330, tracks: [{ mode: "fixed", value: 62 }, { mode: "fr", value: 1.55 }, { mode: "fixed", value: 80 }, { mode: "fr", value: 1.65 }, { mode: "fr", value: 1.55 }], fontSize: 12, headerFontSize: 12 });
  addMetric(slide, { left: 38, top: 458, width: 280, height: 92, label: "MỐC KIỂM SOÁT", value: "M1 - M6", fill: C.redPale, valueSize: 24 });
  addMetric(slide, { left: 348, top: 458, width: 280, height: 92, label: "PHỤ THUỘC CHÍNH", value: "8 → 17 → 20 → 39 → 47", fill: C.redPale, valueSize: 15 });
  addMetric(slide, { left: 658, top: 458, width: 280, height: 92, label: "THỜI HẠN", value: "31/03/2027", fill: C.redPale, valueSize: 22 });
  addMetric(slide, { left: 968, top: 458, width: 273, height: 92, label: "TỔNG CÔNG VIỆC", value: "Task 1 - 52", fill: C.redPale, valueSize: 21 });
  addSurface(slide, 38, 574, 1203, 52, { fill: C.grayLight });
  addText(slide, "Gantt giúp đọc tiến trình theo thời gian. PERT/CPM giúp phân tích quan hệ trước sau, thời gian dự trữ và đường găng.", 54, 590, 1168, 24, { fontSize: 16, color: C.dark });
}

// 11. PERT / CPM
{
  const slide = slides[10];
  addHeader(slide, "ƯỚC LƯỢNG TIẾN ĐỘ: PERT/CPM", "Ước lượng có cơ sở giúp nhận diện đường găng và thời gian dự trữ", 11, notes.ch3);
  addSurface(slide, 38, 100, 580, 310, { fill: C.redPale });
  addText(slide, "CÔNG THỨC PERT", 58, 122, 520, 28, { fontSize: 18, bold: true, color: C.red });
  addText(slide, "EST = (MO + 4 × ML + MP) / 6", 58, 178, 520, 55, { fontSize: 28, bold: true, color: C.dark, alignment: "center" });
  addText(slide, "MO · thời gian lạc quan\nML · thời gian khả dĩ nhất\nMP · thời gian bi quan", 78, 266, 480, 96, { fontSize: 17, color: C.dark, alignment: "center" });
  addSurface(slide, 661, 100, 580, 310, { fill: C.white });
  addText(slide, "ÁP DỤNG CHO DỰ ÁN NHÓM 1", 681, 122, 540, 28, { fontSize: 18, bold: true, color: C.red });
  addMetric(slide, { left: 681, top: 172, width: 245, height: 88, label: "EST CHỐT", value: "221,83\nngày-người", fill: C.redPale, valueSize: 18 });
  addMetric(slide, { left: 956, top: 172, width: 245, height: 88, label: "PERT", value: "201,67\nngày-người", fill: C.redPale, valueSize: 18 });
  addMetric(slide, { left: 681, top: 282, width: 245, height: 88, label: "BUFFER", value: "20,17\nngày-người", fill: C.redPale, valueSize: 18 });
  addMetric(slide, { left: 956, top: 282, width: 245, height: 88, label: "NGUYÊN TẮC", value: "Gắn với\nnguồn lực", fill: C.redPale, valueSize: 17 });
  addText(slide, "Đường găng là đường dài nhất, có thời gian dự trữ bằng 0 và quyết định thời gian ngắn nhất của dự án.", 38, 448, 1203, 42, { fontSize: 18, bold: true, color: C.dark, alignment: "center" });
  addPhaseBar(slide, ["Khởi động", "Phân tích", "Thiết kế", "Phát triển", "Kiểm thử", "Bàn giao"], 38, 520, 1203, 70);
  addSurface(slide, 38, 612, 1203, 34, { fill: C.grayLight });
  addText(slide, "Ước lượng cần được xem xét lại khi phạm vi, nguồn lực hoặc giả định của dự án thay đổi.", 54, 620, 1168, 20, { fontSize: 14, color: C.gray });
}

// 12. Cost and EVM
{
  const slide = slides[11];
  addHeader(slide, "QUẢN LÝ CHI PHÍ VÀ GIÁ TRỊ THU ĐƯỢC", "Ngân sách được phân bổ theo gói công việc và kiểm soát trong quá trình thực hiện", 12, notes.ch5);
  addTable(slide, [
    ["Khoản mục", "Số tiền", "Tỷ trọng"],
    ["Công lao động", "285,4 triệu VNĐ", "70%"],
    ["Thiết bị", "73,8 triệu VNĐ", "18%"],
    ["Chi khác", "49,0 triệu VNĐ", "12%"],
    ["Tổng", "408,2 triệu VNĐ", "100%"],
  ], { left: 38, top: 104, width: 580, height: 280, tracks: [{ mode: "fr", value: 1.45 }, { mode: "fr", value: 1.45 }, { mode: "fixed", value: 100 }], fontSize: 15, headerFontSize: 14 });
  addMetric(slide, { left: 38, top: 404, width: 180, height: 80, label: "LAO ĐỘNG", value: "285,4 tr\n70%", fill: C.redPale, valueSize: 17 });
  addMetric(slide, { left: 238, top: 404, width: 180, height: 80, label: "THIẾT BỊ", value: "73,8 tr", fill: C.redPale, valueSize: 20 });
  addMetric(slide, { left: 438, top: 404, width: 180, height: 80, label: "CHI KHÁC", value: "49,0 tr", fill: C.redPale, valueSize: 20 });
  addSurface(slide, 38, 512, 580, 112, { fill: C.grayLight });
  addText(slide, "Tổng dự toán", 56, 532, 180, 24, { fontSize: 15, bold: true, color: C.red });
  addText(slide, "408.196.650 VNĐ", 56, 562, 520, 34, { fontSize: 26, bold: true, color: C.dark });
  addTable(slide, [
    ["Chỉ số", "Công thức", "Ý nghĩa"],
    ["BCWS", "Chi phí dự toán của việc đã xếp lịch", "Giá trị theo kế hoạch"],
    ["BCWP", "Chi phí dự toán của việc đã thực hiện", "Giá trị thu được"],
    ["ACWP", "Chi phí thực của việc đã thực hiện", "Mức chi thực tế"],
    ["CV", "BCWP - ACWP", "Âm: vượt dự toán"],
    ["CPI", "BCWP / ACWP", "Nhỏ hơn 1: vượt dự toán"],
  ], { left: 661, top: 104, width: 580, height: 420, tracks: [{ mode: "fixed", value: 76 }, { mode: "fr", value: 1.5 }, { mode: "fr", value: 1.05 }], fontSize: 13, headerFontSize: 13 });
  addSurface(slide, 661, 548, 580, 76, { fill: C.redPale });
  addText(slide, "Kiểm soát theo kỳ", 681, 563, 180, 22, { fontSize: 15, bold: true, color: C.red });
  addText(slide, "Cập nhật BCWS, BCWP, ACWP rồi quyết định điều chỉnh hoặc dùng quỹ dự phòng.", 681, 590, 530, 28, { fontSize: 15, color: C.dark });
}

// 13. Quality
{
  const slide = slides[12];
  addHeader(slide, "QUẢN LÝ CHẤT LƯỢNG", "Chất lượng được lập kế hoạch, đảm bảo và kiểm soát trong suốt vòng đời", 13, notes.ch6);
  addCard(slide, { left: 38, top: 92, width: 380, height: 130, title: "LẬP KẾ HOẠCH", body: "Xác định tiêu chuẩn, metric, lịch kiểm định và vai trò chịu trách nhiệm.", fill: C.redPale, titleSize: 16, bodySize: 15, titleHeight: 25 });
  addCard(slide, { left: 450, top: 92, width: 380, height: 130, title: "ĐẢM BẢO", body: "Đánh giá có hệ thống, review và phòng ngừa để dự án tuân thủ kế hoạch.", fill: C.white, titleSize: 16, bodySize: 15, titleHeight: 25 });
  addCard(slide, { left: 862, top: 92, width: 379, height: 130, title: "KIỂM SOÁT", body: "Kiểm thử, so sánh với tiêu chuẩn, phân tích nguyên nhân và hiệu chỉnh.", fill: C.redPale, titleSize: 16, bodySize: 15, titleHeight: 25 });
  addTable(slide, [
    ["Mục tiêu", "Chỉ tiêu", "Cách kiểm tra"],
    ["Tồn kho chính xác", "Sai lệch < 1% sau kiểm kê thử", "UAT 1 kho cửa hàng"],
    ["Không xuất vượt tồn", "0 tồn âm kể cả xuất đồng thời", "NFR-04; kiểm tra số lượng >= 0"],
    ["Truy vết đầy đủ", "100% đổi tồn có thẻ kho; không sửa/xóa", "Đối chiếu thẻ kho và tồn"],
    ["Báo cáo đúng", "NXT < 10s; đúng QT-06", "Đối chiếu dữ liệu mẫu"],
    ["Cảnh báo tồn thấp", "100% đúng trạng thái", "Biên 0, = min, > min"],
    ["Quản lý biến thể", "100% màu x size; SKU không trùng", "Test áo size chữ, quần size số"],
    ["Hàng tồn lâu", "100% quá ngưỡng trong báo cáo", "Test các ngày nhập khác nhau"],
    ["An toàn và phân quyền", "100% ma trận; 0 lỗ hổng Critical", "Test từng vai trò"],
  ], { left: 38, top: 260, width: 1203, height: 370, tracks: [{ mode: "fr", value: 1.25 }, { mode: "fr", value: 1.65 }, { mode: "fr", value: 1.55 }], fontSize: 11.5, headerFontSize: 12 });
}

// 14. Risk
{
  const slide = slides[13];
  addHeader(slide, "QUẢN LÝ RỦI RO", "Rủi ro được nhận diện, giao chủ trì và cập nhật suốt vòng đời", 14, notes.ch8);
  const riskSteps = ["Xác định", "Đánh giá P / I", "Phòng ngừa và giảm thiểu", "Phê duyệt đáp ứng", "Theo dõi và cập nhật"];
  riskSteps.forEach((step, index) => {
    const x = 38 + index * 241;
    addSurface(slide, x, 92, index === 2 ? 225 : 225, 76, { fill: index === 2 ? C.redSoft : C.redPale });
    addText(slide, `${index + 1}. ${step}`, x + 10, 114, 205, 30, { fontSize: 14, bold: true, color: C.red, alignment: "center" });
    if (index < riskSteps.length - 1) slide.shapes.add({ geometry: "rect", position: { left: x + 225, top: 128, width: 16, height: 3 }, fill: C.redLine, line: transparentLine });
  });
  addText(slide, "Đăng ký rủi ro cần có dấu hiệu cảnh báo, người chịu trách nhiệm và biện pháp đã được phê duyệt.", 38, 194, 1203, 28, { fontSize: 16, color: C.dark, alignment: "center" });
  addTable(slide, [
    ["Rủi ro cần theo dõi", "Dấu hiệu", "Đối phó / giảm thiểu", "Chủ trì", "Chu kỳ"],
    ["Phạm vi hoặc yêu cầu tăng", "Nhiều yêu cầu mới", "Change control, ưu tiên và rebaseline", "PM", "Mỗi mốc"],
    ["Chậm phê duyệt", "Sign-off trễ", "Lịch phê duyệt và nhắc mốc", "PM / khách hàng", "M1 - M2"],
    ["Thiếu hoặc biến động nhân lực", "Phân công lệch, bàn giao chậm", "Backup, chia sẻ tri thức, điều phối tải", "PM / Tech Lead", "Hàng tuần"],
    ["Vượt chi phí hoặc tiến độ", "CV < 0, CPI < 1, trễ mốc", "Review ngân sách, buffer và đường găng", "PM", "Theo kỳ"],
    ["Chất lượng hoặc UAT không đạt", "Test fail, lỗi nghiêm trọng", "QA, phân tích nguyên nhân, re-test", "QM / PM", "M5 - M6"],
  ], { left: 38, top: 240, width: 1203, height: 350, tracks: [{ mode: "fr", value: 1.25 }, { mode: "fr", value: 1.05 }, { mode: "fr", value: 1.55 }, { mode: "fr", value: 0.8 }, { mode: "fr", value: 0.7 }], fontSize: 11.5, headerFontSize: 11.5 });
  addSurface(slide, 38, 610, 1203, 36, { fill: C.grayLight });
  addText(slide, "Theo chương 8: P x I = E. Bảng trên là đăng ký theo dõi đề xuất; điểm số cần được chấm và cập nhật trong các cuộc họp rủi ro.", 54, 619, 1168, 18, { fontSize: 13, color: C.gray });
}

// 15. Closing
{
  const slide = slides[14];
  slide.background.fill = C.red;
  addText(slide, "ĐẠI HỌC BÁCH KHOA HÀ NỘI", 130, 38, 768, 28, { fontSize: 20, bold: true, color: C.white });
  addText(slide, "Trường CNTT&TT · Nhóm 1", 130, 66, 768, 28, { fontSize: 16, color: C.white });
  addText(slide, "KẾT LUẬN", 48, 116, 1180, 48, { fontSize: 34, bold: true, color: C.white });
  addText(slide, "QUẢN TRỊ DỰ ÁN LÀ TRỤC CHÍNH", 48, 170, 1180, 32, { fontSize: 20, bold: true, color: C.white });
  addSurface(slide, 48, 244, 570, 330, { fill: C.redDark, line: solidLine("#D94B5B", 1) });
  addText(slide, "5 ĐIỀU CẦN NHỚ", 66, 264, 520, 26, { fontSize: 17, bold: true, color: C.white });
  addBullets(slide, [
    "Dự án có mục tiêu, phạm vi, thời hạn, kinh phí và nguồn lực",
    "WBS là nền cho lịch biểu và dự toán",
    "PM điều phối bên liên quan và kiểm soát thay đổi",
    "Chất lượng và rủi ro phải được quản lý từ sớm",
    "Bàn giao cần tiêu chí nghiệm thu và xác nhận",
  ], 66, 310, 520, 220, { fontSize: 16, color: C.white });
  addSurface(slide, 662, 244, 570, 330, { fill: C.white, line: solidLine(C.white, 1) });
  addText(slide, "THẢO LUẬN", 682, 264, 520, 26, { fontSize: 17, bold: true, color: C.red });
  addBullets(slide, [
    "Nếu thêm POS vào phạm vi, baseline nào bị ảnh hưởng?",
    "Cần làm gì khi CPI < 1?",
    "Rủi ro nào cần ưu tiên trước M1?",
  ], 682, 312, 520, 150, { fontSize: 17, color: C.dark });
  addText(slide, "Cảm ơn và trao đổi", 682, 500, 520, 30, { fontSize: 20, bold: true, color: C.red, alignment: "center" });
  addText(slide, "52 task · 221,83 ngày-người · 408,2 triệu VNĐ · bàn giao 31/03/2027", 48, 624, 1184, 28, { fontSize: 16, color: C.white, alignment: "center" });
  addText(slide, "CNTT20261_N01 · K6901 CNTT VB2CQ · GVHD ThS. Lê Thị Hoa · Hà Nội, tháng 9 năm 2026", 48, 676, 1184, 24, { fontSize: 12, color: C.white, alignment: "center" });
  slide.speakerNotes.textFrame.setText("Kết luận tổng hợp từ Chương 1 - 8 trong C:\\Users\\GHC\\Downloads\\Slide và dữ liệu dự án nhóm 1.");
}

const candidatePath = path.join(buildDir, "candidate.pptx");
await (await PresentationFile.exportPptx(presentation)).save(candidatePath);

const sourceSha256 = crypto.createHash("sha256").update(await fs.readFile(sourcePath)).digest("hex");
const { finalizePresentation } = await import(pathToFileURL(path.join(SKILL_DIR, "container_tools/artifact_tool_utils.mjs")).href);
const baseName = "slide-thuyet-trinh-quan-tri-du-an-2026-09-18";
let finalPath = path.join(outputDir, `${baseName}.pptx`);
for (let i = 2; await fs.stat(finalPath).then(() => true).catch(() => false); i += 1) finalPath = path.join(outputDir, `${baseName}-v${i}.pptx`);

const requirements = {
  explicitTotalSlideCount: 15,
  requiredNativeTableOwnerSlides: [7, 9, 10, 12, 13, 14],
  requiredNativeChartOwnerSlides: [],
};
const result = await finalizePresentation({
  ...requirements,
  workspaceDir,
  candidatePath,
  finalPath,
  pythonExecutable: "C:/Users/GHC/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe",
  integrityValidatorPath: path.join(SKILL_DIR, "container_tools/inspect_presentation_package_integrity.py"),
  layoutValidatorPath: path.join(SKILL_DIR, "container_tools/inspect_presentation_layout_geometry.py"),
  layoutArgs: [
    "--expected-slide-size-emu", "12191695,6858000",
    "--validate-bullet-geometry",
    "--validate-heading-fit",
    ...requirements.requiredNativeTableOwnerSlides.flatMap(number => ["--require-native-table-slide", String(number)]),
  ],
  requiredNativeTableOwnerSlides: requirements.requiredNativeTableOwnerSlides,
  fontPolicy: { basis: "reference", families: [FONT], referencePath: sourcePath, referenceSha256: sourceSha256 },
  verifyArtifactToolImport: true,
  receiptPath: path.join(stagingDir, `${path.basename(finalPath)}.validation.json`),
});
console.log(JSON.stringify({ candidatePath, finalPath, result }, null, 2));
