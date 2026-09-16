"""Create BachMinhQuang 202490077 MS Project files from the sample BTCN structure."""
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

# WeekDay constants in MS Project
PJ_SUNDAY = 1
PJ_SATURDAY = 7
PJ_DO_NOT_SAVE = 0

# Match sample: btcn1 keeps 5-day Standard; btcn2-5 use 7-day (weekends working).
PROJECTS = [
    {
        "stem": "btcn1_202490077_BachMinhQuang",
        "calendar7": False,
        "tasks": [
            ("A", "2d", ""),
            ("B", "1d", "1"),
            ("C", "1d", ""),
            ("D", "1d", "2,3"),
            ("G", "3d", ""),
            ("H", "3d", "4,5"),
            ("F", "2d", ""),
            ("I", "2d", "6,7"),
        ],
    },
    {
        "stem": "btcn2_202490077_BachMinhQuang",
        "calendar7": True,
        "tasks": [
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
    },
    {
        "stem": "btcn3_202490077_BachMinhQuang",
        "calendar7": True,
        "tasks": [
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
    },
    {
        "stem": "btcn4_202490077_BachMinhQuang",
        "calendar7": True,
        "tasks": [
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
    },
    {
        "stem": "btcn5_202490077_BachMinhQuang",
        "calendar7": True,
        "tasks": [
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
    },
]


def kill_project() -> None:
    os.system("taskkill /IM WINPROJ.EXE /F >NUL 2>&1")
    time.sleep(2)


def make_7day_calendar(app, proj) -> None:
    """Copy Standard into '7 Days' and mark Sat/Sun as working."""
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


def build_one(app, spec: dict) -> Path:
    stem = spec["stem"]
    out = OUT_DIR / f"{stem}.mpp"
    if out.exists():
        out.unlink()

    app.FileNew()
    time.sleep(0.6)
    proj = app.ActiveProject
    try:
        app.NewTasksCreatedAsScheduled = True
    except Exception:
        pass

    make_7day_calendar(app, proj)
    cal_name = "7 Days" if spec["calendar7"] else "Standard"
    try:
        app.ProjectSummaryInfo(
            Title=stem,
            Subject=f"QLDA BTCN {stem}",
            Author=AUTHOR,
            Company="HUST SOICT",
            Manager=AUTHOR,
            Comments=f"MSSV {MSSV} - {AUTHOR}",
            Start=START,
            Calendar=cal_name,
        )
    except Exception as exc:
        print("  ProjectSummaryInfo warn:", exc)
        try:
            proj.ProjectStart = START
        except Exception as exc2:
            print("  ProjectStart warn:", exc2)

    # Remove any placeholder task Project may create on FileNew.
    for i in range(proj.Tasks.Count, 0, -1):
        t = proj.Tasks(i)
        if t is not None:
            try:
                t.Delete()
            except Exception:
                pass

    added = []
    for letter, duration, preds in spec["tasks"]:
        name = f"{letter}{SUFFIX}"
        task = proj.Tasks.Add(name)
        try:
            task.Manual = False
        except Exception:
            pass
        task.Duration = duration
        added.append((task, name, duration, preds))
        print(f"  add ID={task.ID} UID={task.UniqueID} {name} {duration}")

    for task, name, duration, preds in added:
        if not preds:
            continue
        try:
            for pid in str(preds).replace(";", ",").split(","):
                pid = pid.strip()
                if not pid:
                    continue
                pred_task = proj.Tasks(int(pid))
                task.TaskDependencies.Add(pred_task)
            print(f"  pred {name} <- {preds} ok")
        except Exception as exc:
            print(f"  pred FAIL {name} <- {preds}: {exc}")
            raise

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
    time.sleep(0.3)
    app.FileClose(PJ_DO_NOT_SAVE)
    print("saved", out, "size", out.stat().st_size)
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
        for spec in PROJECTS:
            print("===", spec["stem"], "7day=" + str(spec["calendar7"]))
            created.append(build_one(app, spec))
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

    print("DONE", len(created), "files")
    for p in created:
        print(" ", p)


if __name__ == "__main__":
    main()
