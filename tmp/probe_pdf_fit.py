"""Export Gantt/Network as 1-page landscape A3 PDF then PNG."""
from __future__ import annotations

import os
import time
from pathlib import Path

import fitz
import pythoncom
import win32com.client

MPP_DIR = Path(
    r"C:\Dev\Learning\VIII.HUST\Quản trị dự án"
    r"\BachMinhQuang_202490077\QLDA_BTCN_202490077_BachMinhQuang"
)
OUT = Path(r"C:\Dev\Learning\tmp\probe")
PJ_DO_NOT_SAVE = 0
pjPaperA3 = 8
pjNoLegend = 0
pjTimescaleWeeks, pjTimescaleDays = 3, 4


def pdf_to_png(pdf: Path, png: Path) -> None:
    doc = fitz.open(pdf)
    print(" ", pdf.name, "pages", doc.page_count)
    if doc.page_count == 1:
        pix = doc[0].get_pixmap(dpi=180)
        pix.save(str(png))
        print("  png", png.name, pix.width, pix.height)
        return
    imgs = []
    for page in doc:
        pix = page.get_pixmap(dpi=180)
        imgs.append(pix)
    from PIL import Image
    pil = []
    for pix in imgs:
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        # drop footer ~4%
        h = int(im.height * 0.94)
        t = int(im.height * 0.03)
        pil.append(im.crop((0, t, im.width, h)))
    w = sum(i.width for i in pil)
    h = max(i.height for i in pil)
    canvas = Image.new("RGB", (w, h), (255, 255, 255))
    x = 0
    for i in pil:
        canvas.paste(i, (x, 0))
        x += i.width
    canvas.save(png)
    print("  stitched", png.name, canvas.size, "from", len(pil), "pages")


def setup_page(app) -> None:
    try:
        app.FilePageSetupPage(
            Portrait=False,
            PagesTall=1,
            PagesWide=1,
            PaperSize=pjPaperA3,
        )
        print("  pagesetup 1x1 A3 landscape")
    except Exception as e:
        print("  pagesetup", e)
    try:
        app.FilePageSetupMargins(Top=0.4, Bottom=0.4, Left=0.4, Right=0.4)
    except Exception as e:
        print("  margins", e)
    try:
        app.FilePageSetupLegend(LegendOn=pjNoLegend)
    except Exception as e:
        print("  legend", e)
    try:
        app.FilePageSetupView(AllSheetColumns=True, BestPageFitTimescale=True, PrintBlankPages=False)
    except Exception as e:
        print("  viewsetup", e)
    try:
        app.FilePageSetupHeader(Alignment=1, Text="")
        app.FilePageSetupFooter(Alignment=1, Text="")
    except Exception as e:
        print("  hf", e)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pythoncom.CoInitialize()
    os.system("taskkill /IM WINPROJ.EXE /F >NUL 2>&1")
    time.sleep(2)
    app = win32com.client.gencache.EnsureDispatch("MSProject.Application")
    app.Visible = True
    app.DisplayAlerts = False
    app.WindowState = 1

    for stem in ("btcn1_5ngay_202490077_BachMinhQuang", "btcn3_7ngay_202490077_BachMinhQuang"):
        print("===", stem)
        app.FileOpen(str(MPP_DIR / f"{stem}.mpp"))
        time.sleep(0.8)
        try:
            app.DisplayProjectSummaryTask = False
        except Exception:
            pass
        try:
            app.HighlightCriticalTasks = True
        except Exception:
            pass

        app.ViewApply("Gantt Chart")
        time.sleep(0.3)
        try:
            app.TableApply("Entry")
            app.SelectTaskColumn("Task Mode")
            app.ColumnDelete()
        except Exception:
            pass
        for field, width in (("Name", 40), ("Duration", 12), ("Start", 16), ("Finish", 16), ("Predecessors", 14)):
            try:
                app.TableEdit(Name="Entry", TaskTable=True, FieldName=field, Width=width)
                app.TableApply("Entry")
            except Exception:
                pass
        try:
            app.TimescaleEdit(MajorUnits=pjTimescaleWeeks, MinorUnits=pjTimescaleDays, MajorCount=1, MinorCount=1)
        except Exception:
            pass
        try:
            app.ZoomTimescale(Entire=True)
        except Exception:
            pass
        setup_page(app)
        pdf = OUT / f"{stem}_gantt.pdf"
        app.DocumentExport(Filename=str(pdf), FileType=0)
        pdf_to_png(pdf, OUT / f"{stem}_gantt.png")

        app.ViewApply("Network Diagram")
        time.sleep(0.4)
        try:
            app.BoxZoom(Entire=True)
        except Exception:
            pass
        setup_page(app)
        pdf = OUT / f"{stem}_net.pdf"
        app.DocumentExport(Filename=str(pdf), FileType=0)
        pdf_to_png(pdf, OUT / f"{stem}_net.png")
        app.FileClose(PJ_DO_NOT_SAVE)

    app.Quit(PJ_DO_NOT_SAVE)
    pythoncom.CoUninitialize()


if __name__ == "__main__":
    main()
