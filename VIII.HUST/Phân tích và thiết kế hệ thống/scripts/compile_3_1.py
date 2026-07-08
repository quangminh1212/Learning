import subprocess
import os

tinytex_bin = r"C:\Users\GHC\AppData\Roaming\TinyTeX\bin\windows"
lualatex = os.path.join(tinytex_bin, "lualatex.exe")
diagram_dir = r"c:\Dev\Learning\VIII.HUST\Phân tích và thiết kế hệ thống\BaoCao\diagrams"
pdf_dir = os.path.join(diagram_dir, "pdf")
tex_file = os.path.join(diagram_dir, "3.1_bfd.tex")

print(f"TinyTeX: {tinytex_bin}")
print(f"lualatex: {lualatex}")
print(f"tex_file: {tex_file}")
print(f"pdf_dir: {pdf_dir}")

# Create wrapper
wrapper = r"""\documentclass[12pt]{article}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage[vietnamese]{babel}
\usepackage[margin=1cm]{geometry}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{array}
\usepackage{enumitem}
\usepackage{setspace}
\usepackage{amsmath}
\usepackage{float}
\usepackage{caption}
\usepackage{tikz}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning, calc, fit, backgrounds}
\usepackage{pgf-umlcd}
\usepackage{pgf-umlsd}
\pagestyle{empty}
\begin{document}
\input{../3.1_bfd.tex}
\end{document}
"""

wrapper_path = os.path.join(pdf_dir, "compile_3_1.tex")
with open(wrapper_path, "w", encoding="utf-8") as f:
    f.write(wrapper)

print(f"Wrapper: {wrapper_path}")

# Compile
env = os.environ.copy()
env["PATH"] = tinytex_bin + os.pathsep + env.get("PATH", "")

print("Compiling...")
result = subprocess.run(
    [lualatex, "-interaction=nonstopmode", "-halt-on-error", "compile_3_1.tex"],
    cwd=pdf_dir,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    env=env
)

print(f"Return code: {result.returncode}")
if result.stdout:
    print("STDOUT:", result.stdout[-2000:])
if result.stderr:
    print("STDERR:", result.stderr[-2000:])

# Check for PDF
pdf_output = os.path.join(pdf_dir, "compile_3_1.pdf")
if os.path.exists(pdf_output):
    print(f"PDF generated: {pdf_output}")
    import shutil
    final_pdf = os.path.join(pdf_dir, "3.1_bfd.pdf")
    shutil.move(pdf_output, final_pdf)
    print(f"Moved to: {final_pdf}")
else:
    print("PDF not generated")
