"""Apply a simple on-screen Gantt table and 7-month timescale."""
import os
import time
from datetime import datetime
from pathlib import Path

import pythoncom
import win32com.client

MPP = Path(r"C:\Dev\Learning\VIII.HUST\Quản trị dự án\Nhóm 1\ke-hoach-du-an.mpp")


def kill():
    os.system("taskkill /IM WINPROJ.EXE /F >NUL 2>&1")
    time.sleep(2)


def main():
    pythoncom.CoInitialize()
    kill()
    app = win32com.client.gencache.EnsureDispatch("MSProject.Application")
    app.Visible = True
    app.DisplayAlerts = False
    app.FileOpen(str(MPP))
    time.sleep(0.8)
    app.ViewApply("Gantt Chart")
    app.TableEdit(
        Name="KeHoach",
        TaskTable=True,
        Create=True,
        OverwriteExisting=True,
        FieldName="Name",
        Width=38,
    )
    for fld, w in (
        ("Duration", 9),
        ("Start", 12),
        ("Finish", 12),
        ("Resource Names", 20),
        ("Cost", 13),
    ):
        app.TableEdit(Name="KeHoach", TaskTable=True, NewFieldName=fld, Width=w)
    app.TableApply("KeHoach")
    try:
        app.TimescaleEdit(MajorUnits=2, MinorUnits=3, MajorCount=1, MinorCount=1)
    except Exception as exc:
        print("timescale warn", exc)
    try:
        app.ZoomTimescale(datetime(2026, 9, 1), datetime(2027, 3, 31))
        print("zoom dated")
    except Exception as exc:
        print("zoom positional warn", exc)
        app.ZoomTimescale(Entire=True)
    try:
        app.HighlightCriticalTasks = True
    except Exception:
        pass
    app.FileSave()
    time.sleep(0.3)
    proj = app.ActiveProject
    pst = proj.ProjectSummaryTask
    print("saved", MPP.stat().st_size, "finish", pst.Finish, "cost", pst.Cost, "res", proj.Resources.Count)
    app.FileClose(0)
    app.Quit(0)
    pythoncom.CoUninitialize()


if __name__ == "__main__":
    main()
