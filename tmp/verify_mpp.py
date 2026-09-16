import os
import glob
import jpype

jdk = r"C:\Program Files\Microsoft\jdk-17.0.18.8-hotspot"
os.environ["JAVA_HOME"] = jdk
jvm = os.path.join(jdk, "bin", "server", "jvm.dll")
import mpxj  # noqa: F401
if not jpype.isJVMStarted():
    jpype.startJVM(jvm)

from org.mpxj.reader import UniversalProjectReader

src = r"C:\Dev\Learning\VIII.HUST\Quản trị dự án\BachMinhQuang_202490077\QLDA_BTCN_202490077_BachMinhQuang"
expected_finish = {
    "btcn1": "2026-09-25T17:00",
    "btcn2": "2026-10-08T17:00",
    "btcn3": "2026-10-26T17:00",
    "btcn4": "2026-10-21T17:00",
    "btcn5": "2026-10-05T17:00",
}
expected_dur = {
    "btcn1": "9.0d",
    "btcn2": "24.0d",
    "btcn3": "42.0d",
    "btcn4": "37.0d",
    "btcn5": "21.0d",
}
reader = UniversalProjectReader()
ok = True
for name in sorted(os.listdir(src)):
    if not name.endswith(".mpp"):
        continue
    path = os.path.join(src, name)
    project = reader.read(path)
    props = project.getProjectProperties()
    cal = str(props.getDefaultCalendar())
    cal_name = props.getDefaultCalendar().getName() if props.getDefaultCalendar() else None
    start = str(props.getStartDate())
    finish = str(props.getFinishDate())
    key = name.split("_")[0]
    print("=" * 70)
    print(name)
    print("calendar", cal_name)
    print("start", start, "finish", finish)
    sat = None
    if props.getDefaultCalendar() is not None:
        print("cal dump first 400:", cal[:400].replace("\n", " | "))
    print("TASKS:")
    summary_dur = None
    crit = []
    for t in project.getTasks():
        if t is None:
            continue
        preds = []
        rels = t.getPredecessors()
        if rels is not None:
            for r in rels:
                src_t = r.getPredecessorTask()
                pred_id = src_t.getID() if src_t is not None else "?"
                preds.append(str(pred_id))
        print(
            f"  {t.getID()}\t{t.getName()}\t{t.getDuration()}\t{t.getStart()}\t{t.getFinish()}\t"
            f"pred={','.join(preds)}\tcrit={t.getCritical()}\tslack={t.getTotalSlack()}"
        )
        if t.getID() == 0:
            summary_dur = str(t.getDuration())
        elif t.getCritical() and not t.getSummary():
            # letter before first underscore
            nm = str(t.getName())
            crit.append(nm.split("_")[0] if "_" in nm else nm)
    exp_f = expected_finish[key]
    exp_d = expected_dur[key]
    print("summary duration", summary_dur, "expected", exp_d)
    print("finish expected", exp_f)
    print("critical", "-".join(crit))
    if "BuiQuocLuyt" in name or "202490069" in name:
        print("FAIL leftover sample identity in filename")
        ok = False
    for t in project.getTasks():
        if t and t.getName() and ("BuiQuocLuyt" in str(t.getName()) or "0069" in str(t.getName()) or "202490069" in str(t.getName())):
            print("FAIL leftover sample identity in task", t.getName())
            ok = False
        if t and t.getName() and t.getID() != 0:
            n = str(t.getName())
            if "0077_BachMinhQuang" not in n:
                print("FAIL task name missing student tag", n)
                ok = False
    if str(finish) != exp_f:
        print("FAIL finish", finish, "!=", exp_f)
        ok = False
    if summary_dur != exp_d:
        print("FAIL duration", summary_dur, "!=", exp_d)
        ok = False
    if not start.startswith("2026-09-15"):
        print("FAIL start", start)
        ok = False

print("\nOVERALL", "OK" if ok else "FAILED")
