"""Re-export clean MS Project views for KTTH Buoi 5 report."""
from __future__ import annotations

import os
import time
from pathlib import Path

import fitz
import pythoncom
import win32com.client
from PIL import Image, ImageDraw, ImageFont

MPP = Path(
    r"C:\Dev\Learning\VIII.HUST\Quản trị dự án\BachMinhQuang_202490077"
    r"\KTTH_Buoi5\202490077-BachMinhQuang-K6901-Buoi5-De1.1.mpp"
)
SHOT = MPP.parent / "screenshots"
TMP = Path(r"C:\Dev\Learning\tmp\probe\ktth_buoi5")
PJ_DO_NOT_SAVE = 0
PJ_PDF = 0
PJ_PAPER_A3 = 8
PJ_NO_LEGEND = 0
PJ_TS_WEEKS = 3
PJ_TS_DAYS = 4


def kill() -> None:
    os.system("taskkill /IM WINPROJ.EXE /F >NUL 2>&1")
    time.sleep(2)


def crop_content(im: Image.Image, pad: int = 18, thresh: int = 250) -> Image.Image:
    gray = im.convert("L")
    mask = gray.point(lambda x: 0 if x >= thresh else 255)
    bbox = mask.getbbox()
    if not bbox:
        return im
    l, t, r, b = bbox
    return im.crop((
        max(0, l - pad),
        max(0, t - pad),
        min(im.width, r + pad),
        min(im.height, b + pad),
    ))


def pdf_pages(pdf: Path) -> list[Image.Image]:
    doc = fitz.open(pdf)
    pages = []
    for page in doc:
        pix = page.get_pixmap(dpi=170)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        top = int(im.height * 0.018)
        bot = int(im.height * 0.955)
        pages.append(im.crop((0, top, im.width, bot)))
    return pages


def add_header(base: Image.Image, dest: Path, caption: str) -> None:
    header_h = 72
    out = Image.new("RGB", (base.width, base.height + header_h), (255, 255, 255))
    out.paste(base.convert("RGB"), (0, header_h))
    draw = ImageDraw.Draw(out)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\times.ttf", 28)
        small = ImageFont.truetype(r"C:\Windows\Fonts\times.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
        small = font
    left = "202490077 - Bạch Minh Quang"
    right = "KTTH Buổi 5 — Đề 1.1"
    draw.text((20, 12), left, fill=(20, 20, 20), font=font)
    bb = draw.textbbox((0, 0), right, font=font)
    draw.text((out.width - (bb[2] - bb[0]) - 20, 12), right, fill=(20, 20, 20), font=font)
    draw.text((20, 44), caption, fill=(70, 70, 70), font=small)
    draw.line([(14, header_h - 2), (out.width - 14, header_h - 2)], fill=(40, 40, 40), width=2)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, "PNG")
    print("shot", dest.name, out.size)


def page_setup(app, pages_wide: int = 1, all_cols: bool = False) -> None:
    app.FilePageSetupPage(Portrait=False, PagesTall=1, PagesWide=pages_wide, PaperSize=PJ_PAPER_A3)
    app.FilePageSetupMargins(Top=0.25, Bottom=0.25, Left=0.25, Right=0.25)
    try:
        app.FilePageSetupLegend(LegendOn=PJ_NO_LEGEND)
    except Exception:
        pass
    try:
        app.FilePageSetupHeader(Alignment=1, Text="")
        app.FilePageSetupFooter(Alignment=1, Text="")
    except Exception:
        pass
    try:
        app.FilePageSetupView(
            AllSheetColumns=all_cols,
            BestPageFitTimescale=True,
            PrintBlankPages=False,
        )
    except Exception as e:
        print("  viewsetup", e)


def export_pdf(app, pdf: Path) -> None:
    if pdf.exists():
        pdf.unlink()
    app.DocumentExport(Filename=str(pdf), FileType=PJ_PDF)
    print("pdf", pdf.name, pdf.stat().st_size)


def apply_view(app, names: list[str]) -> None:
    for n in names:
        try:
            app.ViewApply(n)
            print("view", n)
            return
        except Exception:
            continue
    raise RuntimeError(f"view fail {names}")


def apply_table(app, names: list[str]) -> None:
    for n in names:
        try:
            app.TableApply(n)
            print("table", n)
            return
        except Exception:
            continue
    print("WARN table", names)


def set_col_width(app, field: str, width: int, task: bool) -> None:
    try:
        app.TableEdit(Name="", TaskTable=task, FieldName=field, Width=width)
        app.TableApply("")
    except Exception as e:
        print("  width", field, e)


def main() -> None:
    SHOT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    pythoncom.CoInitialize()
    kill()
    app = win32com.client.Dispatch("MSProject.Application")
    app.Visible = True
    app.DisplayAlerts = False
    try:
        app.WindowState = 1
    except Exception:
        pass
    app.FileOpen(str(MPP))
    time.sleep(0.8)
    try:
        app.DisplayProjectSummaryTask = False
    except Exception:
        pass
    try:
        app.HighlightCriticalTasks = True
    except Exception:
        pass

    # --- Gantt: few columns so bars + critical path are readable ---
    apply_view(app, ["Gantt Chart", "Biểu đồ Gantt"])
    apply_table(app, ["Entry", "Nhập"])
    for col in ("Task Mode", "Chế độ tác vụ", "Resource Names", "Cost", "Critical", "Total Slack"):
        try:
            app.SelectTaskColumn(Column=col)
            app.ColumnDelete()
        except Exception:
            pass
    for newf, pos, wid in (("Finish", 4, 14), ("Predecessors", 5, 12), ("Total Slack", 6, 11), ("Critical", 7, 9)):
        try:
            app.TableEdit(Name="Entry", TaskTable=True, NewFieldName=newf, Width=wid, ColumnPosition=pos)
            app.TableApply("Entry")
        except Exception as e:
            print("addcol", newf, e)
    try:
        app.SelectTaskColumn(Column="Name")
        app.ColumnAlignment(Align:=0)
    except Exception:
        pass
    try:
        app.TimescaleEdit(MajorUnits=PJ_TS_WEEKS, MinorUnits=PJ_TS_DAYS, MajorCount=1, MinorCount=1)
        app.ZoomTimescale(Entire=True)
    except Exception as e:
        print("timescale", e)
    page_setup(app, pages_wide=1, all_cols=False)
    gpdf = TMP / "gantt2.pdf"
    export_pdf(app, gpdf)
    gim = crop_content(pdf_pages(gpdf)[0], pad=14)
    add_header(gim, SHOT / "gantt.png", "Gantt | tuần 7 ngày | cột Critical / Total Slack — đường găng A-B-D-G")

    # --- Schedule table: ES/LS slack ---
    apply_table(app, ["Schedule", "Lịch biểu"])
    try:
        app.ZoomTimescale(Entire=True)
    except Exception:
        pass
    page_setup(app, pages_wide=1, all_cols=True)
    spdf = TMP / "schedule.pdf"
    export_pdf(app, spdf)
    sim = crop_content(pdf_pages(spdf)[0], pad=14)
    add_header(sim, SHOT / "schedule.png", "Bảng Schedule | Total Slack = 0 là công việc găng")

    # --- Network ---
    apply_view(app, ["Network Diagram", "Sơ đồ mạng"])
    time.sleep(0.35)
    try:
        app.BoxZoom(Entire=True)
    except Exception:
        pass
    app.FilePageSetupPage(Portrait=False, PaperSize=PJ_PAPER_A3)
    app.FilePageSetupMargins(Top=0.25, Bottom=0.25, Left=0.25, Right=0.25)
    try:
        app.FilePageSetupLegend(LegendOn=PJ_NO_LEGEND)
    except Exception:
        pass
    npdf = TMP / "network2.pdf"
    export_pdf(app, npdf)
    pages = pdf_pages(npdf)
    if len(pages) == 1:
        nim = crop_content(pages[0], pad=12)
    else:
        w = sum(p.width for p in pages)
        h = max(p.height for p in pages)
        canvas = Image.new("RGB", (w, h), (255, 255, 255))
        x = 0
        for p in pages:
            canvas.paste(p, (x, 0))
            x += p.width
        nim = crop_content(canvas, pad=12)
    add_header(nim, SHOT / "network.png", "Network Diagram | hộp đỏ = công việc găng (A-B-D-G)")

    # --- Resource Sheet with wide rate column ---
    apply_view(app, ["Resource Sheet", "Bảng tài nguyên"])
    apply_table(app, ["Entry", "Nhập"])
    for field, wid in (
        ("Name", 18),
        ("Type", 12),
        ("Material Label", 12),
        ("Max Units", 10),
        ("Std. Rate", 18),
        ("Standard Rate", 18),
        ("Đơn giá chuẩn", 18),
    ):
        set_col_width(app, field, wid, task=False)
    page_setup(app, pages_wide=1, all_cols=True)
    rpdf = TMP / "resources2.pdf"
    export_pdf(app, rpdf)
    rim = crop_content(pdf_pages(rpdf)[0], pad=14)
    add_header(rim, SHOT / "resources.png", "Resource Sheet | Work / Material / Cost và đơn giá")

    # Resource Cost table
    apply_table(app, ["Cost", "Chi phí"])
    page_setup(app, pages_wide=1, all_cols=True)
    rcpdf = TMP / "resource_cost.pdf"
    export_pdf(app, rcpdf)
    rcim = crop_content(pdf_pages(rcpdf)[0], pad=14)
    add_header(rcim, SHOT / "resource_cost.png", "Resource Cost | tổng chi phí theo từng nguồn lực")

    # --- Task Sheet Cost ---
    apply_view(app, ["Task Sheet", "Bảng tác vụ"])
    apply_table(app, ["Cost", "Chi phí"])
    for field, wid in (("Name", 28), ("Total Cost", 16), ("Cost", 16)):
        set_col_width(app, field, wid, task=True)
    page_setup(app, pages_wide=1, all_cols=True)
    cpdf = TMP / "cost2.pdf"
    export_pdf(app, cpdf)
    cim = crop_content(pdf_pages(cpdf)[0], pad=14)
    add_header(cim, SHOT / "cost.png", "Task Sheet — Cost | tổng chi phí từng công việc (VND)")

    # --- Task Sheet with Resource Names ---
    apply_table(app, ["Entry", "Nhập"])
    try:
        app.TableEdit(Name="Entry", TaskTable=True, NewFieldName="Resource Names", Width=42, ColumnPosition=6)
        app.TableApply("Entry")
    except Exception as e:
        print("resnames", e)
    page_setup(app, pages_wide=1, all_cols=True)
    apdf = TMP / "assign.pdf"
    export_pdf(app, apdf)
    aim = crop_content(pdf_pages(apdf)[0], pad=14)
    add_header(aim, SHOT / "assign.png", "Gán nguồn lực | Resource Names trên từng công việc")

    try:
        app.FileClose(PJ_DO_NOT_SAVE)
        app.Quit(PJ_DO_NOT_SAVE)
    except Exception:
        pass
    pythoncom.CoUninitialize()
    print("DONE shots")


if __name__ == "__main__":
    main()
