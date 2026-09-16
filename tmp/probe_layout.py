import os, time, ctypes
from ctypes import wintypes
from pathlib import Path
import pythoncom, win32com.client, win32con, win32gui
from PIL import Image

MPP = Path(r"C:\Dev\Learning\VIII.HUST\Quản trị dự án\BachMinhQuang_202490077\QLDA_BTCN_202490077_BachMinhQuang\btcn1_5ngay_202490077_BachMinhQuang.mpp")
OUT = Path(r"C:\Dev\Learning\tmp\probe")
PW = 2

class BIH(ctypes.Structure):
    _fields_ = [("biSize", wintypes.DWORD),("biWidth", ctypes.c_long),("biHeight", ctypes.c_long),
                ("biPlanes", wintypes.WORD),("biBitCount", wintypes.WORD),("biCompression", wintypes.DWORD),
                ("biSizeImage", wintypes.DWORD),("biXPelsPerMeter", ctypes.c_long),("biYPelsPerMeter", ctypes.c_long),
                ("biClrUsed", wintypes.DWORD),("biClrImportant", wintypes.DWORD)]
class BI(ctypes.Structure):
    _fields_ = [("bmiHeader", BIH), ("bmiColors", wintypes.DWORD * 3)]

def cap(hwnd, path):
    l,t,r,b = win32gui.GetWindowRect(hwnd)
    w,h = r-l, b-t
    u,g = ctypes.windll.user32, ctypes.windll.gdi32
    dc = u.GetWindowDC(hwnd)
    mem = g.CreateCompatibleDC(dc)
    bmp = g.CreateCompatibleBitmap(dc, w, h)
    g.SelectObject(mem, bmp)
    u.PrintWindow(hwnd, mem, PW)
    bmi = BI(); bmi.bmiHeader.biSize=ctypes.sizeof(BIH); bmi.bmiHeader.biWidth=w; bmi.bmiHeader.biHeight=-h
    bmi.bmiHeader.biPlanes=1; bmi.bmiHeader.biBitCount=32
    buf = ctypes.create_string_buffer(w*h*4)
    g.GetDIBits(mem, bmp, 0, h, buf, ctypes.byref(bmi), 0)
    Image.frombuffer("RGB",(w,h),buf,"raw","BGRX",0,1).copy().save(path)
    g.DeleteObject(bmp); g.DeleteDC(mem); u.ReleaseDC(hwnd, dc)
    print("saved", path.name, w, h)

pythoncom.CoInitialize()
os.system("taskkill /IM WINPROJ.EXE /F >NUL 2>&1"); time.sleep(2)
app = win32com.client.gencache.EnsureDispatch("MSProject.Application")
app.Visible=True; app.DisplayAlerts=False; app.WindowState=1
app.FileOpen(str(MPP)); time.sleep(1)
app.ViewApply("Network Diagram"); time.sleep(0.4)
found=[]
def cb(hwnd,_):
    if win32gui.IsWindowVisible(hwnd) and "project" in win32gui.GetWindowText(hwnd).lower():
        l,t,r,b=win32gui.GetWindowRect(hwnd); found.append(((r-l)*(b-t), hwnd))
    return True
win32gui.EnumWindows(cb, None)
hwnd=sorted(found, reverse=True)[0][1]
win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE); time.sleep(0.5)
try:
    app.CommandBars.ExecuteMso("MinimizeRibbon")
except Exception:
    pass
try:
    app.TimelineFormat(Minimized=True)
except Exception:
    pass

for scheme, name in [(0,"fromleft"), (4,"critfirst"), (5,"centerleft")]:
    try:
        app.BoxLayout(LayoutScheme=scheme)
        print("scheme", scheme, "ok")
    except Exception as e:
        print("scheme", scheme, e)
        continue
    try:
        app.SelectAll()
        app.BoxZoom(Entire=True)
        print("  zoom entire")
    except Exception as e:
        print("  zoom", e)
    time.sleep(0.7)
    cap(hwnd, OUT / f"net_scheme_{name}.png")

app.FileClose(0); app.Quit(0)
pythoncom.CoUninitialize()
