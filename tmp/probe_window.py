"""Capture btcn1 and btcn3 windows after correct zoom APIs."""
from __future__ import annotations

import ctypes
import os
import time
from ctypes import wintypes
from pathlib import Path

import pythoncom
import win32com.client
import win32con
import win32gui
from PIL import Image

OUT = Path(r"C:\Dev\Learning\tmp\probe")
MPP_DIR = Path(
    r"C:\Dev\Learning\VIII.HUST\Quản trị dự án"
    r"\BachMinhQuang_202490077\QLDA_BTCN_202490077_BachMinhQuang"
)
PJ_DO_NOT_SAVE = 0
PW_RENDERFULLCONTENT = 2
pjTimescaleWeeks, pjTimescaleDays = 3, 4


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", ctypes.c_long),
        ("biHeight", ctypes.c_long),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", ctypes.c_long),
        ("biYPelsPerMeter", ctypes.c_long),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD),
    ]


class BITMAPINFO(ctypes.Structure):
    _fields_ = [("bmiHeader", BITMAPINFOHEADER), ("bmiColors", wintypes.DWORD * 3)]


def capture_hwnd(hwnd: int, path: Path) -> None:
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    w, h = right - left, bottom - top
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    hwnd_dc = user32.GetWindowDC(hwnd)
    mem_dc = gdi32.CreateCompatibleDC(hwnd_dc)
    hbmp = gdi32.CreateCompatibleBitmap(hwnd_dc, w, h)
    gdi32.SelectObject(mem_dc, hbmp)
    user32.PrintWindow(hwnd, mem_dc, PW_RENDERFULLCONTENT)
    bmi = BITMAPINFO()
    bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.bmiHeader.biWidth = w
    bmi.bmiHeader.biHeight = -h
    bmi.bmiHeader.biPlanes = 1
    bmi.bmiHeader.biBitCount = 32
    buf = ctypes.create_string_buffer(w * h * 4)
    gdi32.GetDIBits(mem_dc, hbmp, 0, h, buf, ctypes.byref(bmi), 0)
    img = Image.frombuffer("RGB", (w, h), buf, "raw", "BGRX", 0, 1).copy()
    gdi32.DeleteObject(hbmp)
    gdi32.DeleteDC(mem_dc)
    user32.ReleaseDC(hwnd, hwnd_dc)
    img.save(path, "PNG")
    print("saved", path.name, img.size)


def find_hwnd() -> int:
    found = []

    def cb(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetParent(hwnd) == 0:
            title = win32gui.GetWindowText(hwnd)
            if "project" in title.lower() or "WINPROJ" in win32gui.GetClassName(hwnd).upper():
                l, t, r, b = win32gui.GetWindowRect(hwnd)
                found.append(((r - l) * (b - t), hwnd, title))
        return True

    win32gui.EnumWindows(cb, None)
    found.sort(reverse=True)
    print("hwnd", hex(found[0][1]), found[0][2], found[0][0])
    return found[0][1]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pythoncom.CoInitialize()
    os.system("taskkill /IM WINPROJ.EXE /F >NUL 2>&1")
    time.sleep(2)
    app = win32com.client.gencache.EnsureDispatch("MSProject.Application")
    app.Visible = True
    app.DisplayAlerts = False
    app.WindowState = 1
    try:
        app.CommandBars.ExecuteMso("MinimizeRibbon")
    except Exception:
        pass

    for stem in ("btcn1_5ngay_202490077_BachMinhQuang", "btcn3_7ngay_202490077_BachMinhQuang"):
        app.FileOpen(str(MPP_DIR / f"{stem}.mpp"))
        time.sleep(1)
        try:
            app.DisplayProjectSummaryTask = False
        except Exception:
            pass
        hwnd = find_hwnd()
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        time.sleep(0.3)

        # Gantt
        app.ViewApply("Gantt Chart")
        time.sleep(0.4)
        try:
            app.HighlightCriticalTasks = True
            app.CommandBars.ExecuteMso("CriticalTasks")
        except Exception:
            pass
        try:
            app.TableApply("Entry")
            app.SelectTaskColumn("Task Mode")
            app.ColumnDelete()
        except Exception:
            pass
        for field, width in (("Name", 38), ("Duration", 12), ("Start", 16)):
            try:
                app.TableEdit(Name="Entry", TaskTable=True, FieldName=field, Width=width)
                app.TableApply("Entry")
            except Exception:
                pass
        try:
            app.TimescaleEdit(MajorUnits=pjTimescaleWeeks, MinorUnits=pjTimescaleDays, MajorCount=1, MinorCount=1)
        except Exception as e:
            print("timescale", e)
        try:
            app.ZoomTimescale(Entire=True)
            print(stem, "gantt zoom entire")
        except Exception as e:
            print("zoom", e)
        time.sleep(0.8)
        capture_hwnd(hwnd, OUT / f"{stem}_gantt.png")

        # Network
        app.ViewApply("Network Diagram")
        time.sleep(0.5)
        try:
            app.HighlightCriticalTasks = True
        except Exception:
            pass
        try:
            app.BoxZoom(Entire=True)
            print(stem, "boxzoom entire")
        except Exception as e:
            print("boxzoom", e)
        time.sleep(0.8)
        capture_hwnd(hwnd, OUT / f"{stem}_network.png")

        # clipboard picture
        try:
            app.EditCopyPicture(Object=0, ForPrinter=False)
            from PIL import ImageGrab
            clip = ImageGrab.grabclipboard()
            print("clipboard", type(clip), getattr(clip, "size", None))
            if clip is not None:
                clip.save(OUT / f"{stem}_network_clip.png")
        except Exception as e:
            print("clipboard", e)

        app.FileClose(PJ_DO_NOT_SAVE)

    app.Quit(PJ_DO_NOT_SAVE)
    pythoncom.CoUninitialize()


if __name__ == "__main__":
    main()
