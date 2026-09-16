import os, time
from pathlib import Path
import fitz, pythoncom, win32com.client

mpp = Path(r"C:\Dev\Learning\VIII.HUST\Quản trị dự án\BachMinhQuang_202490077\QLDA_BTCN_202490077_BachMinhQuang\btcn1_5ngay_202490077_BachMinhQuang.mpp")
mpp3 = Path(r"C:\Dev\Learning\VIII.HUST\Quản trị dự án\BachMinhQuang_202490077\QLDA_BTCN_202490077_BachMinhQuang\btcn3_7ngay_202490077_BachMinhQuang.mpp")
OUT = Path(r"C:\Dev\Learning\tmp\probe")
pythoncom.CoInitialize()
os.system("taskkill /IM WINPROJ.EXE /F >NUL 2>&1")
time.sleep(2)
app = win32com.client.gencache.EnsureDispatch("MSProject.Application")
app.Visible = True
app.DisplayAlerts = False
for path, tag in ((mpp, "b1"), (mpp3, "b3")):
    app.FileOpen(str(path))
    time.sleep(0.8)
    app.ViewApply("Network Diagram")
    time.sleep(0.4)
    try:
        app.BoxZoom(Entire=True)
    except Exception as e:
        print("zoom", e)
    try:
        app.FilePageSetupPage(Portrait=False, PagesTall=1, PagesWide=1, PaperSize=8)
        app.FilePageSetupMargins(Top=0.3, Bottom=0.3, Left=0.3, Right=0.3)
        app.FilePageSetupLegend(LegendOn=0)
        app.FilePageSetupHeader(Alignment=1, Text="")
        app.FilePageSetupFooter(Alignment=1, Text="")
        print(tag, "pagesetup ok")
    except Exception as e:
        print(tag, "pagesetup", e)
    pdf = OUT / f"{tag}_net.pdf"
    try:
        app.DocumentExport(Filename=str(pdf), FileType=0)
        print(tag, "pdf size", pdf.stat().st_size if pdf.exists() else 0)
        doc = fitz.open(pdf)
        print(tag, "pages", doc.page_count)
        if doc.page_count:
            pix = doc[0].get_pixmap(dpi=160)
            pix.save(str(OUT / f"{tag}_net.png"))
            print(tag, "png", pix.width, pix.height)
            if doc.page_count > 1:
                pix = doc[doc.page_count-1].get_pixmap(dpi=120)
                pix.save(str(OUT / f"{tag}_net_last.png"))
    except Exception as e:
        print(tag, "export", e)
    app.FileClose(0)
app.Quit(0)
pythoncom.CoUninitialize()
