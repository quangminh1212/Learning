import os
import subprocess

# Check common LaTeX paths
paths = [
    r"C:\Program Files\MiKTeX\miktex\bin\x64",
    r"C:\Program Files (x86)\MiKTeX\miktex\bin\x64",
    r"C:\texlive\2024\bin\windows",
    r"C:\texlive\2023\bin\windows",
    r"C:\Dev\Learning\miktex-portable\texmfs\install\miktex\bin\x64",
]

for path in paths:
    if os.path.exists(path):
        print(f"Found: {path}")
        lualatex = os.path.join(path, "lualatex.exe")
        if os.path.exists(lualatex):
            print(f"  lualatex.exe exists")
            try:
                result = subprocess.run([lualatex, "--version"], 
                                      capture_output=True, text=True, timeout=5)
                print(f"  Version: {result.stdout[:100]}")
            except:
                pass
    else:
        print(f"Not found: {path}")

# Check PATH
print("\nChecking PATH:")
env_path = os.environ.get("PATH", "")
for p in env_path.split(os.pathsep):
    if "tex" in p.lower() or "latex" in p.lower():
        print(f"  {p}")
