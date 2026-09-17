"""Export Gantt PDF/PNG of the Nhóm 1 MPP for visual QA."""
import os
import time
from pathlib import Path

import pythoncom
import win32com.client

MPP = Path(r"C:\Dev\Learning\VIII.HUST\Quản trị dự án\Nhóm 1\ke-hoach-du-an.mpp")
OUT = Path(r"C:\Dev\Learning\tmp\nhom1_gantt.pdf")
PNG = Path(r"C:\Dev\Learning\tmp\nhom1_gantt.png")
PJ_DO_NOT_SAVE = 0


def kill():
    os.system("taskkill /IM WINPROJ.EXE /F >NUL 2>&1")
    time.sleep(2)


def main():
    pythoncom.CoInitialize()
    kill()
    app = win32com.client.Dispatch("MSProject.Application")
    app.Visible = True
    app.DisplayAlerts = False
    app.FileOpen(str(MPP))
    time.sleep(1)
    proj = app.ActiveProject
    try:
        app.ViewApply("Gantt Chart")
    except Exception:
        pass
    try:
        app.TableApply("Entry")
    except Exception:
        pass
    try:
        app.ZoomTimescale(Entire=True)
    except Exception as exc:
        print("zoom warn", exc)
    try:
        app.HighlightCriticalTasks = True
    except Exception:
        pass
    if OUT.exists():
        OUT.unlink()
    app.DocumentExport(Filename=str(OUT), FileType=0)
    print("pdf", OUT, OUT.stat().st_size)
    app.FileClose(PJ_DO_NOT_SAVE)
    app.Quit(PJ_DO_NOT_SAVE)
    pythoncom.CoUninitialize()

    import fitz
    from PIL import Image

    doc = fitz.open(OUT)
    print("pages", doc.page_count)
    page = doc[0]
    pix = page.get_pixmap(dpi=140)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    im.save(PNG)
    print("png", PNG, im.size)


if __name__ == "__main__":
    main()
