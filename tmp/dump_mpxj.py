import os
import glob
import jpype

jdk = r"C:\Program Files\Microsoft\jdk-17.0.18.8-hotspot"
os.environ["JAVA_HOME"] = jdk
jvm = os.path.join(jdk, "bin", "server", "jvm.dll")

import mpxj  # noqa: F401  # adds classpath via jpype.addClassPath
if not jpype.isJVMStarted():
    jpype.startJVM(jvm)

from org.mpxj.reader import UniversalProjectReader

src = r"C:\Dev\Learning\VIII.HUST\Quản trị dự án\Mẫu\QLDA_BTCN_202490069_BuiQuocLuyt"
out = r"C:\Dev\Learning\tmp"
os.makedirs(out, exist_ok=True)
reader = UniversalProjectReader()

for name in sorted(os.listdir(src)):
    if not name.endswith(".mpp"):
        continue
    path = os.path.join(src, name)
    print("=" * 80)
    print("FILE", name)
    project = reader.read(path)
    props = project.getProjectProperties()
    lines = []
    def add(k, v):
        lines.append(f"{k}={v}")
        print(f"{k}={v}")
    add("projectTitle", props.getProjectTitle())
    add("name", props.getName())
    add("author", props.getAuthor())
    add("company", props.getCompany())
    add("start", props.getStartDate())
    add("finish", props.getFinishDate())
    add("defaultCalendar", props.getDefaultCalendar())
    add("minutesPerDay", props.getMinutesPerDay())
    add("minutesPerWeek", props.getMinutesPerWeek())
    print("\nCALENDARS:")
    for c in project.getCalendars():
        print(" ", c.getName())
        lines.append(f"CAL={c.getName()}")
    print("\nTASKS:")
    header = "ID\tUniqueID\tOutline\tName\tDuration\tStart\tFinish\tPredecessors\tCritical\tTotalSlack\tWBS"
    print(header)
    lines.append(header)
    for t in project.getTasks():
        if t is None:
            continue
        preds = []
        rels = t.getPredecessors()
        if rels is not None:
            for r in rels:
                src_t = r.getPredecessorTask()
                pred_id = src_t.getID() if src_t is not None else "?"
                lag = r.getLag()
                preds.append(f"{pred_id}{r.getType()}{'' if lag is None else lag}")
        row = "\t".join([
            str(t.getID()),
            str(t.getUniqueID()),
            str(t.getOutlineLevel()),
            str(t.getName()),
            str(t.getDuration()),
            str(t.getStart()),
            str(t.getFinish()),
            ";".join(str(p) for p in preds),
            str(t.getCritical()),
            str(t.getTotalSlack()),
            str(t.getWBS()),
        ])
        print(row)
        lines.append(row)
    out_path = os.path.join(out, name.replace(".mpp", "_mpxj.txt"))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("wrote", out_path)
