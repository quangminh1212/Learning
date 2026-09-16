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
expected_dur = {"btcn1": "9.0d", "btcn2": "24.0d", "btcn3": "42.0d", "btcn4": "37.0d", "btcn5": "21.0d"}
expected_finish = {
    ("btcn1", "5ngay"): "2026-09-25T17:00",
    ("btcn1", "7ngay"): "2026-09-23T17:00",
    ("btcn2", "5ngay"): "2026-10-16T17:00",
    ("btcn2", "7ngay"): "2026-10-08T17:00",
    ("btcn3", "5ngay"): "2026-11-11T17:00",
    ("btcn3", "7ngay"): "2026-10-26T17:00",
    ("btcn4", "5ngay"): "2026-11-04T17:00",
    ("btcn4", "7ngay"): "2026-10-21T17:00",
    ("btcn5", "5ngay"): "2026-10-13T17:00",
    ("btcn5", "7ngay"): "2026-10-05T17:00",
}
expected_crit = {
    "btcn1": "A-B-D-H-I",
    "btcn2": "B-E-F-H-I-J",
    "btcn4": "A-C-G-H-I-K-N",
    "btcn5": "B-D-H-K",
}
reader = UniversalProjectReader()
ok = True
files = sorted(glob.glob(os.path.join(src, "btcn*.mpp")))
print("count", len(files))
for path in files:
    name = os.path.basename(path)
    parts = name.split("_")
    key, tag = parts[0], parts[1]
    project = reader.read(path)
    props = project.getProjectProperties()
    cal = props.getDefaultCalendar()
    cal_name = cal.getName() if cal else None
    finish = str(props.getFinishDate())
    summary_dur = None
    crit = []
    for t in project.getTasks():
        if t is None:
            continue
        if t.getID() == 0:
            summary_dur = str(t.getDuration())
        elif t.getCritical() and not t.getSummary():
            nm = str(t.getName())
            crit.append(nm.split("_")[0])
        if t.getID() != 0 and "0077_BachMinhQuang" not in str(t.getName()):
            print("FAIL name", t.getName())
            ok = False
    crit_s = "-".join(crit)
    exp_f = expected_finish[(key, tag)]
    exp_d = expected_dur[key]
    want_cal = "7 Days" if tag == "7ngay" else "Standard"
    print(f"{name}: cal={cal_name} dur={summary_dur} finish={finish} crit={crit_s}")
    if cal_name != want_cal:
        print("  FAIL calendar", cal_name, "!=", want_cal)
        ok = False
    if summary_dur != exp_d:
        print("  FAIL duration", summary_dur, "!=", exp_d)
        ok = False
    if finish != exp_f:
        print("  FAIL finish", finish, "!=", exp_f)
        ok = False
    if key in expected_crit and crit_s != expected_crit[key]:
        # btcn3 has two parallel critical paths; MS Project marks all TF=0
        if key != "btcn3":
            print("  FAIL crit", crit_s, "!=", expected_crit[key])
            ok = False
    if key == "btcn3":
        need = {"A", "D", "G", "F", "K", "L", "N", "P"}
        if not need.issubset(set(crit)):
            print("  FAIL btcn3 crit missing", need - set(crit))
            ok = False

print("OVERALL", "OK" if ok else "FAILED")
