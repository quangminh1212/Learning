import os, time
from pathlib import Path
import fitz, pythoncom, win32com.client
from PIL import Image

mpp = Path(r"C:\Dev\Learning\VIII.HUST\Quản trị dự án\BachMinhQuang_202490077\QLDA_BTCN_202490077_BachMinhQuang\btcn1_5ngay_202490077_BachMinhQuang.mpp")
out = Path(r"C:\Dev\Learning\tmp\probe\gantt_custom.png")
pythoncom.CoInitialize()
os.system("taskkill /IM WINPROJ.EXE /F >NUL 2>&1"); time.sleep(3)
app = win32com.client.gencache.EnsureDispatch("MSProject.Application")
app.Visible=True; app.DisplayAlerts=False
app.FileOpen(str(mpp)); time.sleep(0.8)
app.ViewApply("Gantt Chart"); time.sleep(0.3)
app.TableEdit(Name="BTCN", TaskTable=True, Create=True, OverwriteExisting=True, FieldName="Name", Width=40)
for fld, w in (("Duration", 10), ("Start", 14), ("Finish", 14), ("Predecessors", 12)):
    app.TableEdit(Name="BTCN", TaskTable=True, NewFieldName=fld, Width=w)
app.TableApply("BTCN")
app.TimescaleEdit(MajorUnits=3, MinorUnits=4, MajorCount=1, MinorCount=1)
app.ZoomTimescale(Entire=True)
app.FilePageSetupPage(Portrait=False, PagesTall=1, PagesWide=1, PaperSize=8)
app.FilePageSetupMargins(Top=0.3, Bottom=0.3, Left=0.3, Right=0.3)
app.FilePageSetupLegend(LegendOn=0)
pdf = Path(r"C:\Dev\Learning\tmp\probe\gantt_custom.pdf")
if pdf.exists(): pdf.unlink()
app.DocumentExport(Filename=str(pdf), FileType=0)
doc=fitz.open(pdf)
print("pages", doc.page_count)
pix=doc[0].get_pixmap(dpi=180)
Image.frombytes("RGB",(pix.width,pix.height),pix.samples).save(out)
print("saved", out, pix.width, pix.height)
app.FileClose(0); app.Quit(0)
pythoncom.CoUninitialize()
