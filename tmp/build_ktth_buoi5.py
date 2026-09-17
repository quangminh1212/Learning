"""KTTH Buoi 5 / De 1.1 — MS Project 7-day calendar + resources."""
from __future__ import annotations

import os
import time
from datetime import datetime
from pathlib import Path

import pythoncom
import win32com.client
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(
    r"C:\Dev\Learning\VIII.HUST\Quản trị dự án\BachMinhQuang_202490077"
)
STEM = "202490077-BachMinhQuang-K6901-Buoi5-De1.1"
OUT_DIR = ROOT / "KTTH_Buoi5"
MPP = OUT_DIR / f"{STEM}.mpp"
SHOT = OUT_DIR / "screenshots"
TMP = Path(r"C:\Dev\Learning\tmp\probe\ktth_buoi5")

START = datetime(2026, 9, 15, 8, 0)
AUTHOR = "Bach Minh Quang"
MSSV = "202490077"
SUFFIX = "_202490077_BachMinhQuang"

PJ_DO_NOT_SAVE = 0
PJ_SUNDAY = 1
PJ_SATURDAY = 7
PJ_FIXED_DURATION = 1
PJ_WORK = 0
PJ_MATERIAL = 1
PJ_COST = 2
PJ_PDF = 0
PJ_PAPER_A3 = 8
PJ_NO_LEGEND = 0
PJ_TS_WEEKS = 3
PJ_TS_DAYS = 4

TASKS = [
    # letter, days, preds (letters), work units, materials {name: qty}, costs [name]
    ("A", 25, [], {"Chủ nhiệm": 0.3, "Thành viên": 0.4, "Kỹ thuật viên": 0.3},
     {"Giấy A3": 5, "Máy in màu": 2}, []),
    ("B", 20, ["A"], {"Chủ nhiệm": 0.2, "Thành viên": 0.4, "Kỹ thuật viên": 0.4},
     {"Đăng bài": 3}, ["Công tác phí"]),
    ("C", 18, [], {"Chủ nhiệm": 0.3, "Thành viên": 0.4, "Kỹ thuật viên": 0.3},
     {}, ["Hội thảo"]),
    ("D", 23, ["B", "C"], {"Chủ nhiệm": 0.3, "Thành viên": 0.4, "Kỹ thuật viên": 0.3},
     {"Đăng bài": 4}, ["Hội thảo"]),
    ("E", 19, [], {"Chủ nhiệm": 0.3, "Thành viên": 0.4, "Kỹ thuật viên": 0.3},
     {}, ["Công tác phí"]),
    ("G", 25, ["E", "D"], {"Chủ nhiệm": 0.3, "Thành viên": 0.4, "Kỹ thuật viên": 0.3},
     {"Giấy A3": 1}, ["Hội thảo", "Nghiệm thu"]),
]

WORK_RATES = {
    "Chủ nhiệm": 180_000,
    "Thành viên": 155_000,
    "Kỹ thuật viên": 100_000,
}
MATERIALS = {
    "Giấy A3": (135_000, "Ram"),
    "Máy in màu": (5_500_000, "Cái"),
    "Đăng bài": (35_000_000, "Bài"),
}
COST_RATES = {
    "Công tác phí": 45_000_000,
    "Hội thảo": 95_000_000,
    "Nghiệm thu": 150_000_000,
}


def kill_project() -> None:
    os.system("taskkill /IM WINPROJ.EXE /F >NUL 2>&1")
    time.sleep(2)


def com_set(obj, attr, value) -> None:
    try:
        setattr(obj, attr, value)
    except Exception as exc:
        print(f"  warn set {attr}={value!r}: {exc}")


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


def crop_content(im: Image.Image, pad: int = 16, thresh: int = 248) -> Image.Image:
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


def pdf_to_image(pdf: Path, stitch: bool = False) -> Image.Image:
    import fitz

    doc = fitz.open(pdf)
    if doc.page_count < 1:
        raise RuntimeError(f"empty pdf {pdf}")
    pages = []
    for page in doc:
        pix = page.get_pixmap(dpi=160)
        im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        top = int(im.height * 0.02)
        bot = int(im.height * 0.94)
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
    return crop_content(canvas)


def add_header(base: Image.Image, dest: Path, caption: str) -> None:
    header_h = 78
    out = Image.new("RGB", (base.width, base.height + header_h), (255, 255, 255))
    out.paste(base.convert("RGB"), (0, header_h))
    draw = ImageDraw.Draw(out)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\times.ttf", 30)
        small = ImageFont.truetype(r"C:\Windows\Fonts\times.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
        small = font
    left = "202490077 - Bạch Minh Quang"
    right = "KTTH Buổi 5 — Đề 1.1"
    draw.text((24, 16), left, fill=(20, 20, 20), font=font)
    bb = draw.textbbox((0, 0), right, font=font)
    draw.text((out.width - (bb[2] - bb[0]) - 24, 16), right, fill=(20, 20, 20), font=font)
    draw.text((24, 50), caption, fill=(70, 70, 70), font=small)
    draw.line([(16, header_h - 2), (out.width - 16, header_h - 2)], fill=(40, 40, 40), width=2)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, "PNG")
    print("  shot", dest.name, out.size)


def page_setup(app, pages_wide: int = 1) -> None:
    app.FilePageSetupPage(Portrait=False, PagesTall=1, PagesWide=pages_wide, PaperSize=PJ_PAPER_A3)
    app.FilePageSetupMargins(Top=0.3, Bottom=0.3, Left=0.3, Right=0.3)
    try:
        app.FilePageSetupLegend(LegendOn=PJ_NO_LEGEND)
    except Exception:
        pass
    try:
        app.FilePageSetupHeader(Alignment=1, Text="")
        app.FilePageSetupFooter(Alignment=1, Text="")
    except Exception:
        pass


def export_view(app, pdf: Path, png: Path, caption: str, stitch: bool = False, pages_wide: int = 1) -> None:
    if pdf.exists():
        pdf.unlink()
    page_setup(app, pages_wide=pages_wide)
    time.sleep(0.25)
    app.DocumentExport(Filename=str(pdf), FileType=PJ_PDF)
    print("  pdf", pdf.name, pdf.stat().st_size)
    img = pdf_to_image(pdf, stitch=stitch)
    add_header(img, png, caption)


def apply_view(app, names: list[str]) -> str | None:
    for name in names:
        try:
            app.ViewApply(name)
            print("  view", name)
            return name
        except Exception:
            continue
    print("  WARN view fail", names)
    return None


def apply_table(app, names: list[str]) -> str | None:
    for name in names:
        try:
            app.TableApply(name)
            print("  table", name)
            return name
        except Exception:
            continue
    print("  WARN table fail", names)
    return None


def build(app) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SHOT.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    if MPP.exists():
        try:
            MPP.unlink()
        except PermissionError:
            kill_project()
            time.sleep(1)
            MPP.unlink()

    app.FileNew()
    time.sleep(0.6)
    proj = app.ActiveProject
    try:
        app.NewTasksCreatedAsScheduled = True
    except Exception:
        pass

    make_7day_calendar(app, proj)
    try:
        app.ProjectSummaryInfo(
            Title=STEM,
            Subject="KTTH Buoi 5 - De 1.1 - lich 7 ngay",
            Author=AUTHOR,
            Company="HUST SOICT",
            Manager=AUTHOR,
            Comments=f"MSSV {MSSV} - {AUTHOR} - Lop K6901 - Buoi 5 - De 1.1",
            Start=START,
            Calendar="7 Days",
        )
    except Exception as exc:
        print("ProjectSummaryInfo warn:", exc)

    com_set(proj, "CurrencyCode", "VND")
    com_set(proj, "CurrencySymbol", "₫")
    com_set(proj, "CurrencyDigits", 0)
    try:
        proj.CurrencySymbolPosition = 3
    except Exception:
        pass
    com_set(proj, "HoursPerDay", 8)
    com_set(proj, "HoursPerWeek", 56)
    com_set(proj, "DaysPerMonth", 30)
    try:
        proj.Calendar = "7 Days"
    except Exception:
        com_set(proj, "Calendar", "7 Days")

    for i in range(proj.Tasks.Count, 0, -1):
        t = proj.Tasks(i)
        if t is not None:
            try:
                t.Delete()
            except Exception:
                pass

    res_map = {}
    for name, rate in WORK_RATES.items():
        r = proj.Resources.Add(name)
        com_set(r, "Type", PJ_WORK)
        com_set(r, "StandardRate", f"{rate}/h")
        com_set(r, "OvertimeRate", "0/h")
        com_set(r, "MaxUnits", 5.0)
        try:
            r.Calendar = "7 Days"
        except Exception:
            pass
        res_map[name] = r
        print("work", name, rate)

    for name, (rate, unit) in MATERIALS.items():
        r = proj.Resources.Add(name)
        com_set(r, "Type", PJ_MATERIAL)
        com_set(r, "StandardRate", rate)
        com_set(r, "MaterialLabel", unit)
        res_map[name] = r
        print("mat", name, rate, unit)

    for name, cost in COST_RATES.items():
        r = proj.Resources.Add(name)
        com_set(r, "Type", PJ_COST)
        com_set(r, "Notes", f"Don gia {cost:,} VND / lan su dung".replace(",", "."))
        res_map[name] = r
        print("cost", name, cost)

    task_map = {}
    for letter, days, _preds, _w, _m, _c in TASKS:
        name = f"{letter}{SUFFIX}"
        t = proj.Tasks.Add(name)
        com_set(t, "Manual", False)
        com_set(t, "Type", PJ_FIXED_DURATION)
        try:
            t.EffortDriven = False
        except Exception:
            pass
        t.Duration = f"{days}d"
        task_map[letter] = t
        print(f"task ID={t.ID} {name} {days}d")

    for letter, _days, preds, _w, _m, _c in TASKS:
        t = task_map[letter]
        for p in preds:
            t.TaskDependencies.Add(task_map[p])
            print(f"  pred {letter} <- {p}")

    for letter, _days, _preds, work_u, mats, costs in TASKS:
        t = task_map[letter]
        for rname, units in work_u.items():
            asn = t.Assignments.Add(ResourceID=res_map[rname].ID)
            asn.Units = units
            print(f"  work {letter} {rname} {units}")
        for rname, qty in mats.items():
            asn = t.Assignments.Add(ResourceID=res_map[rname].ID)
            asn.Units = qty
            print(f"  mat {letter} {rname} {qty}")
        for rname in costs:
            asn = t.Assignments.Add(ResourceID=res_map[rname].ID)
            amount = COST_RATES[rname]
            try:
                asn.Cost = amount
            except Exception as exc:
                print("  cost assign warn", rname, exc)
                try:
                    t.Cost1 = (t.Cost1 or 0) + amount
                except Exception:
                    pass
            print(f"  cost {letter} {rname} {amount}")

    try:
        app.DisplayProjectSummaryTask = True
        proj.ProjectSummaryTask.Name = STEM
    except Exception:
        pass
    try:
        app.HighlightCriticalTasks = True
    except Exception:
        pass

    print("\n=== VERIFY IN PROJECT ===")
    try:
        cal = proj.Calendar
        print("Calendar", getattr(cal, "Name", cal))
    except Exception as exc:
        print("Calendar warn", exc)
    print("Start", proj.ProjectStart, "Finish", proj.ProjectFinish)
    try:
        print("Summary duration", proj.ProjectSummaryTask.Duration)
        print("Summary cost", proj.ProjectSummaryTask.Cost)
    except Exception as exc:
        print("summary warn", exc)
    for t in proj.Tasks:
        if t is None:
            continue
        print(
            f"  ID={t.ID} crit={t.Critical} slack={t.TotalSlack} "
            f"dur={t.Duration} start={t.Start} finish={t.Finish} "
            f"cost={t.Cost} res={t.ResourceNames} name={t.Name}"
        )
    print("Resources:")
    for r in proj.Resources:
        if r is None:
            continue
        print(f"  {r.ID} {r.Name} type={r.Type} rate={r.StandardRate} cost={r.Cost}")

    app.FileSaveAs(str(MPP))
    time.sleep(0.3)
    print("saved", MPP, MPP.stat().st_size)


def add_gantt_columns(app) -> None:
    apply_table(app, ["Entry", "Nhập"])
    for col in ("Task Mode", "Chế độ tác vụ", "Task mode"):
        try:
            app.SelectTaskColumn(Column=col)
            app.ColumnDelete()
            break
        except Exception:
            continue
    for newf, pos, wid in (
        ("Finish", 4, 14),
        ("Predecessors", 5, 10),
        ("Resource Names", 6, 28),
        ("Cost", 7, 14),
        ("Total Slack", 8, 10),
        ("Critical", 9, 8),
    ):
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


def export_shots(app) -> None:
    apply_view(app, ["Gantt Chart", "Biểu đồ Gantt"])
    time.sleep(0.3)
    add_gantt_columns(app)
    try:
        app.TimescaleEdit(
            MajorUnits=PJ_TS_WEEKS,
            MinorUnits=PJ_TS_DAYS,
            MajorCount=1,
            MinorCount=1,
        )
        app.ZoomTimescale(Entire=True)
    except Exception as e:
        print("  timescale", e)
    try:
        app.FilePageSetupView(AllSheetColumns=True, BestPageFitTimescale=True, PrintBlankPages=False)
    except Exception as e:
        print("  gantt viewsetup", e)
    export_view(
        app,
        TMP / "gantt.pdf",
        SHOT / "gantt.png",
        "Gantt | lịch 7 ngày | công việc găng tô đỏ",
        pages_wide=1,
    )

    apply_view(app, ["Network Diagram", "Sơ đồ mạng"])
    time.sleep(0.4)
    try:
        app.BoxZoom(Entire=True)
    except Exception:
        pass
    app.FilePageSetupPage(Portrait=False, PaperSize=PJ_PAPER_A3)
    app.FilePageSetupMargins(Top=0.3, Bottom=0.3, Left=0.3, Right=0.3)
    try:
        app.FilePageSetupLegend(LegendOn=PJ_NO_LEGEND)
    except Exception:
        pass
    npdf = TMP / "network.pdf"
    if npdf.exists():
        npdf.unlink()
    app.DocumentExport(Filename=str(npdf), FileType=PJ_PDF)
    print("  pdf", npdf.name, npdf.stat().st_size)
    nimg = pdf_to_image(npdf, stitch=True)
    add_header(nimg, SHOT / "network.png", "Network Diagram | lịch 7 ngày | đường găng")

    apply_view(app, ["Resource Sheet", "Bảng tài nguyên"])
    time.sleep(0.3)
    apply_table(app, ["Entry", "Nhập"])
    export_view(
        app,
        TMP / "resources.pdf",
        SHOT / "resources.png",
        "Resource Sheet | loại Work / Material / Cost và đơn giá",
    )

    apply_view(app, ["Gantt Chart", "Biểu đồ Gantt"])
    time.sleep(0.25)
    apply_table(app, ["Cost", "Chi phí"])
    try:
        app.ZoomTimescale(Entire=True)
    except Exception:
        pass
    export_view(
        app,
        TMP / "cost.pdf",
        SHOT / "cost.png",
        "Bảng Cost | chi phí từng công việc (VND)",
    )

    apply_view(app, ["Task Usage", "Sử dụng tác vụ", "Task Usage"])
    time.sleep(0.3)
    export_view(
        app,
        TMP / "usage.pdf",
        SHOT / "usage.png",
        "Task Usage | gán nguồn lực cho từng công việc",
        stitch=True,
        pages_wide=1,
    )


def main() -> None:
    pythoncom.CoInitialize()
    kill_project()
    try:
        app = win32com.client.gencache.EnsureDispatch("MSProject.Application")
    except Exception:
        app = win32com.client.Dispatch("MSProject.Application")
    app.Visible = True
    app.DisplayAlerts = False
    try:
        app.WindowState = 1
    except Exception:
        pass
    try:
        app.FileClose(PJ_DO_NOT_SAVE)
    except Exception:
        pass
    try:
        build(app)
        export_shots(app)
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
    print("DONE", MPP)


if __name__ == "__main__":
    main()
