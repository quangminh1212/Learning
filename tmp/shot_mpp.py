"""Export complete Gantt (1-page A3 PDF) and Network (stitched PDF pages)."""
from __future__ import annotations

import os
import time
from pathlib import Path

import fitz
import pythoncom
import win32com.client
from PIL import Image, ImageChops, ImageDraw, ImageFont

OUT_DIR = Path(
    r"C:\Dev\Learning\VIII.HUST\Quản trị dự án"
    r"\BachMinhQuang_202490077\QLDA_BTCN_202490077_BachMinhQuang"
)
SHOT_DIR = OUT_DIR / "screenshots"
TMP = Path(r"C:\Dev\Learning\tmp\probe")
PJ_DO_NOT_SAVE = 0
pjPaperA3 = 8
pjNoLegend = 0
pjTimescaleWeeks = 3
pjTimescaleDays = 4
pjPDF = 0


def crop_content(im: Image.Image, pad: int = 20, thresh: int = 248) -> Image.Image:
    gray = im.convert("L")
    mask = gray.point(lambda x: 0 if x >= thresh else 255)
    bbox = mask.getbbox()
    if not bbox:
        return im
    l, t, r, b = bbox
    l = max(0, l - pad)
    t = max(0, t - pad)
    r = min(im.width, r + pad)
    b = min(im.height, b + pad)
    return im.crop((l, t, r, b))


def pdf_to_image(pdf: Path, stitch: bool) -> Image.Image:
    doc = fitz.open(pdf)
    if doc.page_count < 1:
        raise RuntimeError(f"empty pdf {pdf}")
    pages = []
    for page in doc:
        pix = page.get_pixmap(dpi=170)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        top = int(im.height * 0.025)
        bot = int(im.height * 0.93)
        pages.append(im.crop((0, top, im.width, bot)))
    if not stitch or len(pages) == 1:
        return crop_content(pages[0])
    w = sum(p.width for p in pages)
    h = max(p.height for p in pages)
    canvas = Image.new("RGB", (w, h), (255, 255, 255))
    x = 0
    for p in pages:
        canvas.paste(p, (x, 0))
        x += p.width
    print("  stitched", len(pages), "pages ->", canvas.size)
    return crop_content(canvas)


def add_header(base: Image.Image, dest: Path, caption: str) -> None:
    header_h = 78
    out = Image.new("RGB", (base.width, base.height + header_h), (255, 255, 255))
    out.paste(base.convert("RGB"), (0, header_h))
    draw = ImageDraw.Draw(out)
    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\times.ttf", 32)
        small = ImageFont.truetype("C:\\Windows\\Fonts\\times.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
        small = font
    left = "202490077 - Bạch Minh Quang"
    right = "Báo cáo thực hành cá nhân"
    draw.text((28, 18), left, fill=(20, 20, 20), font=font)
    bb = draw.textbbox((0, 0), right, font=font)
    draw.text((out.width - (bb[2] - bb[0]) - 28, 18), right, fill=(20, 20, 20), font=font)
    draw.text((28, 52), caption, fill=(70, 70, 70), font=small)
    draw.line([(20, header_h - 2), (out.width - 20, header_h - 2)], fill=(40, 40, 40), width=2)
    out.save(dest, "PNG")
    print("  header", dest.name, out.size)


def gantt_page_setup(app) -> None:
    app.FilePageSetupPage(Portrait=False, PagesTall=1, PagesWide=1, PaperSize=pjPaperA3)
    app.FilePageSetupMargins(Top=0.3, Bottom=0.3, Left=0.3, Right=0.3)
    try:
        app.FilePageSetupLegend(LegendOn=pjNoLegend)
    except Exception:
        pass
    try:
        app.FilePageSetupHeader(Alignment=1, Text="")
        app.FilePageSetupFooter(Alignment=1, Text="")
    except Exception:
        pass
    try:
        app.FilePageSetupView(
            AllSheetColumns=False,
            BestPageFitTimescale=True,
            PrintBlankPages=False,
        )
    except Exception as e:
        print("  gantt viewsetup", e)


def network_page_setup(app) -> None:
    # Do NOT force 1x1 — that yields empty PDFs for Network Diagram.
    app.FilePageSetupPage(Portrait=False, PaperSize=pjPaperA3)
    app.FilePageSetupMargins(Top=0.3, Bottom=0.3, Left=0.3, Right=0.3)
    try:
        app.FilePageSetupLegend(LegendOn=pjNoLegend)
    except Exception:
        pass
    try:
        app.FilePageSetupHeader(Alignment=1, Text="")
        app.FilePageSetupFooter(Alignment=1, Text="")
    except Exception:
        pass


def main() -> None:
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    files = sorted(OUT_DIR.glob("btcn*_5ngay_*.mpp")) + sorted(OUT_DIR.glob("btcn*_7ngay_*.mpp"))
    if len(files) != 10:
        raise SystemExit(f"expected 10 mpp, got {len(files)}")

    pythoncom.CoInitialize()
    os.system("taskkill /IM WINPROJ.EXE /F >NUL 2>&1")
    time.sleep(4)
    app = win32com.client.gencache.EnsureDispatch("MSProject.Application")
    app.Visible = True
    app.DisplayAlerts = False
    app.WindowState = 1
    time.sleep(1)

    try:
        for mpp in files:
            print("===", mpp.name)
            app.FileOpen(str(mpp))
            time.sleep(0.9)
            try:
                app.DisplayProjectSummaryTask = False
            except Exception:
                pass
            try:
                app.HighlightCriticalTasks = True
            except Exception:
                pass

            stem = mpp.stem
            bai, tag = stem.split("_")[0], stem.split("_")[1]
            lich = "5 ngày" if tag == "5ngay" else "7 ngày"

            app.ViewApply("Gantt Chart")
            time.sleep(0.35)
            try:
                app.TableApply("Entry")
            except Exception:
                pass
            try:
                app.SelectTaskColumn("Task Mode")
                app.ColumnDelete()
            except Exception:
                pass
            for newf, pos, wid in (("Finish", 4, 16), ("Predecessors", 5, 12)):
                try:
                    app.TableEdit(
                        Name="Entry",
                        TaskTable=True,
                        NewFieldName=newf,
                        Width=wid,
                        ColumnPosition=pos,
                    )
                    app.TableApply("Entry")
                except Exception as e:
                    print("  addcol", newf, e)
            try:
                app.TimescaleEdit(
                    MajorUnits=pjTimescaleWeeks,
                    MinorUnits=pjTimescaleDays,
                    MajorCount=1,
                    MinorCount=1,
                )
                app.ZoomTimescale(Entire=True)
            except Exception as e:
                print("  timescale", e)
            gantt_page_setup(app)
            gpdf = TMP / f"{stem}_gantt.pdf"
            if gpdf.exists():
                gpdf.unlink()
            app.DocumentExport(Filename=str(gpdf), FileType=pjPDF)
            gimg = pdf_to_image(gpdf, stitch=False)
            gimg = crop_content(gimg, pad=12, thresh=250)
            add_header(
                gimg,
                SHOT_DIR / f"{bai}_{tag}_gantt_202490077_BachMinhQuang.png",
                f"{bai.upper()} | lịch {lich} | Gantt (bảng công việc)",
            )

            if os.environ.get("SKIP_NETWORK") == "1":
                app.FileClose(PJ_DO_NOT_SAVE)
                continue
            app.ViewApply("Network Diagram")
            time.sleep(0.4)
            try:
                app.BoxZoom(Entire=True)
            except Exception:
                pass
            network_page_setup(app)
            npdf = TMP / f"{stem}_net.pdf"
            if npdf.exists():
                npdf.unlink()
            app.DocumentExport(Filename=str(npdf), FileType=pjPDF)
            nimg = pdf_to_image(npdf, stitch=True)
            add_header(
                nimg,
                SHOT_DIR / f"{bai}_{tag}_network_202490077_BachMinhQuang.png",
                f"{bai.upper()} | lịch {lich} | Network Diagram (sơ đồ găng)",
            )

            app.FileClose(PJ_DO_NOT_SAVE)
    finally:
        try:
            app.Quit(PJ_DO_NOT_SAVE)
        except Exception:
            pass
        pythoncom.CoUninitialize()
    print("SHOTS", len(list(SHOT_DIR.glob("*_202490077_BachMinhQuang.png"))))


if __name__ == "__main__":
    main()
