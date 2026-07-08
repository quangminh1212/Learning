"""Compile a single TikZ diagram to PDF with debug output."""
import os
import shutil
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DIAGRAMS_DIR = os.path.join(BASE_DIR, "diagrams")
OUTPUT_DIR = os.path.join(BASE_DIR, "diagrams", "pdf")

WRAPPER_TEMPLATE = r"""\documentclass[12pt]{{article}}
\usepackage{{fontspec}}
\setmainfont{{Times New Roman}}
\usepackage[vietnamese]{{babel}}
\usepackage[margin=1cm]{{geometry}}
\usepackage{{graphicx}}
\usepackage{{xcolor}}
\usepackage{{booktabs}}
\usepackage{{array}}
\usepackage{{enumitem}}
\usepackage{{setspace}}
\usepackage{{amsmath}}
\usepackage{{float}}
\usepackage{{caption}}
\usepackage{{tikz}}
\usetikzlibrary{{shapes.geometric, arrows.meta, positioning, calc, fit, backgrounds}}
\usepackage{{pgf-umlcd}}
\usepackage{{pgf-umlsd}}
\pagestyle{{empty}}
\begin{{document}}
\input{{{input_path}}}
\end{{document}}
"""

def compile_diagram(tex_name):
    name = tex_name[:-4]
    input_rel = os.path.relpath(
        os.path.join(DIAGRAMS_DIR, tex_name), OUTPUT_DIR
    ).replace("\\", "/")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    wrapper_name = f"pdf_{name}.tex"
    wrapper_path = os.path.join(OUTPUT_DIR, wrapper_name)
    with open(wrapper_path, "w", encoding="utf-8") as f:
        f.write(WRAPPER_TEMPLATE.format(input_path=input_rel))

    print(f"Compiling {tex_name}...")
    print(f"Wrapper: {wrapper_path}")
    
    # Try lualatex
    try:
        result = subprocess.run(
            ["lualatex", "-interaction=nonstopmode", "-halt-on-error", wrapper_name],
            cwd=OUTPUT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        print(f"lualatex return code: {result.returncode}")
        if result.returncode != 0:
            print("STDOUT:", result.stdout[-1000:])
            print("STDERR:", result.stderr[-1000:])
    except FileNotFoundError:
        print("lualatex not found, trying pdflatex...")
        try:
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", wrapper_name],
                cwd=OUTPUT_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            print(f"pdflatex return code: {result.returncode}")
            if result.returncode != 0:
                print("STDOUT:", result.stdout[-1000:])
                print("STDERR:", result.stderr[-1000:])
        except FileNotFoundError:
            print("pdflatex not found either. LaTeX compiler not installed.")
            return False

    generated_pdf = os.path.join(OUTPUT_DIR, f"pdf_{name}.pdf")
    final_pdf = os.path.join(OUTPUT_DIR, f"{name}.pdf")
    if os.path.exists(generated_pdf):
        shutil.move(generated_pdf, final_pdf)
        print(f"OK -> {name}.pdf")
        return True
    print(f"PDF not found for {name}")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python compile_single_debug.py <diagram_name.tex>")
        sys.exit(1)
    tex_name = sys.argv[1]
    if not tex_name.endswith(".tex"):
        tex_name += ".tex"
    success = compile_diagram(tex_name)
    sys.exit(0 if success else 1)
