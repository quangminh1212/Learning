"""Re-export Gantt using default Entry table; do not edit columns."""
from __future__ import annotations

import os
import time
from pathlib import Path

import fitz
import pythoncom
import win32com.client
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(
    r"C:\Dev\Learning\VIII.HUST\Quản trị dự án"
    r"\BachMinhQuang_202490077\QLDA_BTCN_202490077_BachMinhQuang"
)
SHOT_DIR = OUT_DIR / "screenshots"
TMP = Path(r"C:\Dev\Learning\tmp\probe")
pjPaperA3 = 8
pjNoLegend = 0
pjTimescaleWeeks = 3
pjTimescaleDays = 4


def crop_table(im: Image.Image) -> Image.Image:
    g = im.convert("L")
    pix = g.load()
    w, h = im.size
    last = 0
    gap = 0
    for y in range(h):
        dark = sum(1 for x in range(0, w, 6) if pix[x, y] < 245)
        if dark > 12:
            last = y
            gap = 0
        else:
            gap += 1
            if last > 60 and gap > 30:
                break
    return im.crop((0, 0, w, min(h, last + 16)))


def add_header(base: Image.Image, dest: Path, caption: str) -> None:
    header_h = 78
    out = Image.new("RGB", (base.width, base.height + header_h), (255, 255, 255))
    out.paste(base.convert("RGB"), (0, header_h))
    draw = ImageDraw.Draw(out)
    font = ImageFont.truetype("C:\\Windows\\Fonts\\times.ttf", 32)
    small = ImageFont.truetype("C:\\Windows\\Fonts\\times.ttf", 22)
    left = "202490077 - Bạch Minh Quang"
    right = "Báo cáo thực hành cá nhân"
    draw.text((28, 18), left, fill=(20, 20, 20), font=font)
    bb = draw.textbbox((0, 0), right, font=font)
    draw.text((out.width - (bb[2] - bb[0]) - 28, 18), right, fill=(20, 20, 20), font=font)
    draw.text((28, 52), caption, fill=(70, 70, 70), font=small)
    draw.line([(20, header_h - 2), (out.width - 20, header_h - 2)], fill=(40, 40, 40), width=2)
    out.save(dest, "PNG")
    print("  ", dest.name, out.size)


def main() -> None:
    pythoncom.CoInitialize()
    os.system("taskkill /IM WINPROJ.EXE /F >NUL 2>&1")
    time.sleep(3)
    app = win32com.client.gencache.EnsureDispatch("MSProject.Application")
    app.Visible = True
    app.DisplayAlerts = False
    files = sorted(OUT_DIR.glob("btcn*_5ngay_*.mpp")) + sorted(OUT_DIR.glob("btcn*_7ngay_*.mpp"))
    try:
        for mpp in files:
            print("===", mpp.name)
            app.FileOpen(str(mpp))
            time.sleep(0.8)
            try:
                app.DisplayProjectSummaryTask = False
            except Exception:
                pass
            app.ViewApply("Gantt Chart")
            time.sleep(0.3)
            try:
                app.TableEdit(
                    Name="BTCN",
                    TaskTable=True,
                    Create=True,
                    OverwriteExisting=True,
                    FieldName="Name",
                    Width=40,
                )
                for fld, wid in (("Duration", 10), ("Start", 14), ("Finish", 14), ("Predecessors", 12)):
                    app.TableEdit(Name="BTCN", TaskTable=True, NewFieldName=fld, Width=wid)
                app.TableApply("BTCN")
            except Exception as e:
                print("  table", e)
                try:
                    app.TableApply("Entry")
                except Exception:
                    pass
            try:
                app.TimescaleEdit(MajorUnits=pjTimescaleWeeks, MinorUnits=pjTimescaleDays, MajorCount=1, MinorCount=1)
                app.ZoomTimescale(Entire=True)
            except Exception:
                pass
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
            # Do not call FilePageSetupView(BestPageFitTimescale) — it squeezes task-name columns.
            pdf = TMP / (mpp.stem + "_gantt3.pdf")
            if pdf.exists():
                pdf.unlink()
            app.DocumentExport(Filename=str(pdf), FileType=0)
            doc = fitz.open(pdf)
            pix = doc[0].get_pixmap(dpi=180)
            im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            im = crop_table(im)
            bai, tag = mpp.stem.split("_")[0], mpp.stem.split("_")[1]
            lich = "5 ngày" if tag == "5ngay" else "7 ngày"
            add_header(
                im,
                SHOT_DIR / f"{bai}_{tag}_gantt_202490077_BachMinhQuang.png",
                f"{bai.upper()} | lịch {lich} | Gantt (bảng công việc)",
            )
            app.FileClose(0)
    finally:
        try:
            app.Quit(0)
        except Exception:
            pass
        pythoncom.CoUninitialize()


if __name__ == "__main__":
    main()
