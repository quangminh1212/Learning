"""Create 5-day and 7-day MS Project files for BTCN 1-5."""
from __future__ import annotations

import os
import time
from datetime import datetime
from pathlib import Path

import pythoncom
import win32com.client

OUT_DIR = Path(
    r"C:\Dev\Learning\VIII.HUST\Quản trị dự án"
    r"\BachMinhQuang_202490077\QLDA_BTCN_202490077_BachMinhQuang"
)
START = datetime(2026, 9, 15, 8, 0)
SUFFIX = "_0077_BachMinhQuang"
AUTHOR = "Bach Minh Quang"
MSSV = "202490077"
PJ_SUNDAY = 1
PJ_SATURDAY = 7
PJ_DO_NOT_SAVE = 0

TASKS = {
    1: [
        ("A", "2d", ""),
        ("B", "1d", "1"),
        ("C", "1d", ""),
        ("D", "1d", "2,3"),
        ("G", "3d", ""),
        ("H", "3d", "4,5"),
        ("F", "2d", ""),
        ("I", "2d", "6,7"),
    ],
    2: [
        ("A", "2d", ""),
        ("B", "1d", ""),
        ("C", "3d", ""),
        ("D", "2d", "3"),
        ("E", "8d", "2"),
        ("F", "9d", "5"),
        ("G", "12d", "4"),
        ("H", "3d", "1,6,7"),
        ("I", "1d", "8"),
        ("J", "2d", "9"),
    ],
    3: [
        ("A", "3d", ""),
        ("B", "4d", ""),
        ("C", "4d", ""),
        ("D", "5d", "1"),
        ("G", "5d", "4"),
        ("H", "9d", "1"),
        ("F", "7d", "2,5"),
        ("I", "6d", "3"),
        ("K", "3d", "7"),
        ("L", "10d", "7"),
        ("M", "9d", "7,8"),
        ("N", "7d", "6,9"),
        ("P", "12d", "10,11,12"),
    ],
    4: [
        ("A", "3d", ""),
        ("B", "2d", ""),
        ("C", "4d", "1"),
        ("D", "2d", "1"),
        ("G", "3d", "3"),
        ("H", "6d", "2,4,5"),
        ("F", "9d", "3"),
        ("I", "5d", "6"),
        ("K", "6d", "8"),
        ("L", "5d", "8"),
        ("M", "7d", "7,9,10"),
        ("N", "10d", "7,9"),
    ],
    5: [
        ("A", "2d", ""),
        ("B", "6d", ""),
        ("C", "3d", "1"),
        ("D", "4d", "2,3"),
        ("G", "5d", "1"),
        ("H", "5d", "4,5"),
        ("F", "4d", "4"),
        ("I", "7d", "2,3"),
        ("K", "6d", "6,7"),
        ("L", "6d", "8"),
    ],
}


def kill_project() -> None:
    os.system("taskkill /IM WINPROJ.EXE /F >NUL 2>&1")
    time.sleep(2)


def make_7day_calendar(app, proj) -> None:
    names = [proj.BaseCalendars(i).Name for i in range(1, proj.BaseCalendars.Count + 1)]
    if "7 Days" not in names:
        try:
            app.BaseCalendarCreate("7 Days", "Standard")
        except Exception:
            app.BaseCalendarCreate("7 Days")
    cal = proj.BaseCalendars("7 Days")
    monday = cal.WeekDays(2)
    for weekday in (PJ_SATURDAY, PJ_SUNDAY):
        day = cal.WeekDays(weekday)
        day.Working = True
        try:
            day.Shift1.Start = monday.Shift1.Start
            day.Shift1.Finish = monday.Shift1.Finish
            day.Shift2.Start = monday.Shift2.Start
            day.Shift2.Finish = monday.Shift2.Finish
        except Exception as exc:
            print("  shift warn", weekday, exc)


def build_one(app, bai: int, calendar7: bool) -> Path:
    tag = "7ngay" if calendar7 else "5ngay"
    stem = f"btcn{bai}_{tag}_202490077_BachMinhQuang"
    out = OUT_DIR / f"{stem}.mpp"
    if out.exists():
        out.unlink()

    app.FileNew()
    time.sleep(0.5)
    proj = app.ActiveProject
    try:
        app.NewTasksCreatedAsScheduled = True
    except Exception:
        pass

    make_7day_calendar(app, proj)
    cal_name = "7 Days" if calendar7 else "Standard"
    try:
        app.ProjectSummaryInfo(
            Title=stem,
            Subject=f"QLDA BTCN {bai} lich {tag}",
            Author=AUTHOR,
            Company="HUST SOICT",
            Manager=AUTHOR,
            Comments=f"MSSV {MSSV} - {AUTHOR} - {tag}",
            Start=START,
            Calendar=cal_name,
        )
    except Exception as exc:
        print("  ProjectSummaryInfo warn:", exc)

    for i in range(proj.Tasks.Count, 0, -1):
        t = proj.Tasks(i)
        if t is not None:
            try:
                t.Delete()
            except Exception:
                pass

    added = []
    for letter, duration, preds in TASKS[bai]:
        name = f"{letter}{SUFFIX}"
        task = proj.Tasks.Add(name)
        try:
            task.Manual = False
        except Exception:
            pass
        task.Duration = duration
        added.append((task, name, preds))
        print(f"  add ID={task.ID} {name} {duration}")

    for task, name, preds in added:
        if not preds:
            continue
        for pid in str(preds).replace(";", ",").split(","):
            pid = pid.strip()
            if pid:
                task.TaskDependencies.Add(proj.Tasks(int(pid)))
        print(f"  pred {name} <- {preds}")

    try:
        app.DisplayProjectSummaryTask = True
        proj.ProjectSummaryTask.Name = stem
    except Exception:
        pass
    try:
        app.HighlightCriticalTasks = True
    except Exception:
        pass

    app.FileSaveAs(str(out))
    time.sleep(0.25)
    app.FileClose(PJ_DO_NOT_SAVE)
    print("saved", out.name, out.stat().st_size)
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pythoncom.CoInitialize()
    kill_project()
    try:
        app = win32com.client.gencache.EnsureDispatch("MSProject.Application")
    except Exception:
        app = win32com.client.Dispatch("MSProject.Application")
    app.Visible = True
    app.DisplayAlerts = False
    try:
        app.FileClose(PJ_DO_NOT_SAVE)
    except Exception:
        pass

    created = []
    try:
        for bai in range(1, 6):
            for calendar7 in (False, True):
                tag = "7ngay" if calendar7 else "5ngay"
                print("===", f"btcn{bai}", tag)
                created.append(build_one(app, bai, calendar7))
    finally:
        try:
            app.FileClose(PJ_DO_NOT_SAVE)
        except Exception:
            pass
        try:
            app.Quit(PJ_DO_NOT_SAVE)
        except Exception:
            pass
        pythoncom.CoUninitialize()

    # Remove old unsuffixed files so only 5ngay/7ngay remain.
    for old in OUT_DIR.glob("btcn*_202490077_BachMinhQuang.mpp"):
        if "_5ngay_" not in old.name and "_7ngay_" not in old.name:
            old.unlink()
            print("removed old", old.name)

    print("DONE", len(created), "files")
    for p in created:
        print(" ", p.name)


if __name__ == "__main__":
    main()
