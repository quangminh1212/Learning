import os
import jpype

jdk = r"C:\Program Files\Microsoft\jdk-17.0.18.8-hotspot"
os.environ["JAVA_HOME"] = jdk
jvm = os.path.join(jdk, "bin", "server", "jvm.dll")
import mpxj  # noqa: F401
if not jpype.isJVMStarted():
    jpype.startJVM(jvm)

from org.mpxj.reader import UniversalProjectReader

path = r"C:\Dev\Learning\VIII.HUST\Quản trị dự án\Nhóm 1\ke-hoach-du-an.mpp"
project = UniversalProjectReader().read(path)
props = project.getProjectProperties()
print("title", props.getProjectTitle())
print("start", props.getStartDate())
print("finish", props.getFinishDate())
print("author", props.getAuthor())
print("currency", props.getCurrencySymbol(), props.getCurrencyCode())
print()
print(f"{'ID':>4} OL {'Dur':>10} {'Work':>10} {'Cost':>14} {'Start':16} {'Finish':16} Name")
total_leaf = 0
for t in project.getTasks():
    if t is None:
        continue
    cost = float(t.getCost() or 0)
    print(
        f"{int(t.getID()):4} {t.getOutlineLevel()} "
        f"{str(t.getDuration() or ''):>10} {str(t.getWork() or ''):>10} "
        f"{cost:14,.0f} "
        f"{str(t.getStart())[:16]:16} {str(t.getFinish())[:16]:16} "
        f"{t.getName()}"
    )
    if t.getOutlineLevel() == 2 and not t.getSummary():
        total_leaf += 1

print("leaf count", total_leaf)
print()
print("RESOURCES")
for r in project.getResources():
    if r is None or r.getName() is None:
        continue
    name = str(r.getName())
    print(
        f"  {name:28} type={r.getType()} rate={r.getStandardRate()} "
        f"work={r.getWork()} cost={r.getCost()}"
    )

print("\nPREDS")
for t in project.getTasks():
    if t is None or t.getSummary():
        continue
    preds = t.getPredecessors()
    if preds is None or preds.isEmpty():
        continue
    items = []
    for rel in preds:
        pred = rel.getPredecessorTask()
        items.append(str(pred.getName())[:24])
    print(f"  {t.getName()[:42]:42} <- {', '.join(items)}")
