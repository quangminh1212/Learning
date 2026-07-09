from pathlib import Path
import re

base = Path(r"C:\Dev\Learning\VIII.HUST\Phân tích và thiết kế hệ thống\BaoCao")
files = list((base / "chapters").glob("*.tex")) + list((base / "diagrams" / "tex").glob("*.tex"))


def renumber(text: str) -> str:
    # Protect UC01-03
    text = re.sub(r"\bUC0([123])\b", r"__KEEP\1__", text)
    # UC16..UC04 -> UC20..UC08 (+4)
    for old in range(16, 3, -1):
        new = old + 4
        text = re.sub(rf"\bUC{old:02d}\b", f"__NEW{new:02d}__", text)
    text = re.sub(r"__KEEP([123])__", r"UC0\1", text)
    text = re.sub(r"__NEW(\d{2})__", r"UC\1", text)
    return text


changed = []
for f in files:
    old = f.read_text(encoding="utf-8")
    new = renumber(old)
    if new != old:
        f.write_text(new, encoding="utf-8")
        changed.append(f.name)

print("Updated", len(changed), "files:")
for n in sorted(changed):
    print(" ", n)
