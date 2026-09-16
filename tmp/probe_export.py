"""Probe MS Project export methods on one file."""
from __future__ import annotations

import os
import time
from pathlib import Path

import pythoncom
import win32com.client

MPP = Path(
    r"C:\Dev\Learning\VIII.HUST\Quản trị dự án"
    r"\BachMinhQuang_202490077\QLDA_BTCN_202490077_BachMinhQuang"
    r"\btcn1_5ngay_202490077_BachMinhQuang.mpp"
)
OUT = Path(r"C:\Dev\Learning\tmp\probe")
PJ_DO_NOT_SAVE = 0
pjScreen, pjPrinter, pjGIF = 0, 1, 2
pjLayoutAutomatic, pjLayoutTopDownCriticalFirst = 1, 4
pjLayoutCenteredFromLeft = 5
pjTimescaleWeeks, pjTimescaleDays = 3, 4
pjCopyPictureScale, pjInches = 2, 0


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pythoncom.CoInitialize()
    os.system("taskkill /IM WINPROJ.EXE /F >NUL 2>&1")
    time.sleep(2)
    app = win32com.client.gencache.EnsureDispatch("MSProject.Application")
    app.Visible = True
    app.DisplayAlerts = False
    app.WindowState = 1
    app.FileOpen(str(MPP))
    time.sleep(1)
    try:
        app.DisplayProjectSummaryTask = False
    except Exception:
        pass
    try:
        app.CommandBars.ExecuteMso("MinimizeRibbon")
        print("ribbon minimized")
    except Exception as e:
        print("ribbon", e)

    # --- Network ---
    app.ViewApply("Network Diagram")
    time.sleep(0.5)
    try:
        app.BoxLayout(
            LayoutMode=pjLayoutAutomatic,
            LayoutScheme=pjLayoutTopDownCriticalFirst,
            ShowSummaryTasks=False,
            RowSpacing=20,
            ColumnSpacing=30,
        )
        print("boxlayout ok")
    except Exception as e:
        print("boxlayout", e)
    try:
        app.BoxZoom(Entire=True)
        print("boxzoom entire ok")
    except Exception as e:
        print("boxzoom", e)
    time.sleep(0.8)

    gif1 = str(OUT / "net_printer.gif")
    try:
        app.EditCopyPicture(
            Object=pjGIF,
            ForPrinter=True,
            Filename=gif1,
            ScaleOption=pjCopyPictureScale,
            MaxImageWidth=24,
            MaxImageHeight=14,
            MeasurementUnits=pjInches,
        )
        print("net gif printer", os.path.getsize(gif1) if os.path.exists(gif1) else "MISSING")
    except Exception as e:
        print("net gif printer FAIL", e)

    gif2 = str(OUT / "net_screen.gif")
    try:
        app.EditCopyPicture(
            Object=pjScreen,
            ForPrinter=False,
            Filename=gif2,
            ScaleOption=pjCopyPictureScale,
            MaxImageWidth=24,
            MaxImageHeight=14,
            MeasurementUnits=pjInches,
        )
        print("net gif screen", os.path.getsize(gif2) if os.path.exists(gif2) else "MISSING")
    except Exception as e:
        print("net gif screen FAIL", e)

    pdfn = str(OUT / "net.pdf")
    try:
        app.DocumentExport(Filename=pdfn, FileType=0)
        print("net pdf", os.path.getsize(pdfn) if os.path.exists(pdfn) else "MISSING")
    except Exception as e:
        print("net pdf FAIL", e)

    # --- Gantt ---
    app.ViewApply("Gantt Chart")
    time.sleep(0.5)
    try:
        app.TableApply("Entry")
    except Exception:
        pass
    try:
        app.SelectTaskColumn("Task Mode")
        app.ColumnDelete()
    except Exception as e:
        print("col del", e)
    for field, width in (("Name", 36), ("Duration", 11), ("Start", 16), ("Finish", 16), ("Predecessors", 14)):
        try:
            app.TableEdit(Name="Entry", TaskTable=True, FieldName=field, Width=width)
            app.TableApply("Entry")
        except Exception as e:
            print("table", field, e)
    try:
        app.TimescaleEdit(MajorUnits=pjTimescaleWeeks, MinorUnits=pjTimescaleDays, MajorCount=1, MinorCount=1)
        print("timescale weeks/days ok")
    except Exception as e:
        print("timescale", e)
    try:
        app.ZoomTimescale(Entire=True)
        print("zoomtimescale entire ok")
    except Exception as e:
        print("zoomtimescale", e)
    time.sleep(0.8)

    gif3 = str(OUT / "gantt_printer.gif")
    proj = app.ActiveProject
    try:
        app.EditCopyPicture(
            Object=pjGIF,
            ForPrinter=True,
            FromDate=proj.ProjectStart,
            ToDate=proj.ProjectFinish,
            Filename=gif3,
            ScaleOption=pjCopyPictureTimescale if False else pjCopyPictureScale,
            MaxImageWidth=24,
            MaxImageHeight=10,
            MeasurementUnits=pjInches,
        )
        print("gantt gif", os.path.getsize(gif3) if os.path.exists(gif3) else "MISSING")
    except Exception as e:
        print("gantt gif FAIL", e)

    pdfg = str(OUT / "gantt.pdf")
    try:
        app.DocumentExport(Filename=pdfg, FileType=0, FromDate=proj.ProjectStart, ToDate=proj.ProjectFinish)
        print("gantt pdf", os.path.getsize(pdfg) if os.path.exists(pdfg) else "MISSING")
    except Exception as e:
        print("gantt pdf FAIL", e)

    print("files", list(OUT.iterdir()))
    app.FileClose(PJ_DO_NOT_SAVE)
    app.Quit(PJ_DO_NOT_SAVE)
    pythoncom.CoUninitialize()


if __name__ == "__main__":
    main()
