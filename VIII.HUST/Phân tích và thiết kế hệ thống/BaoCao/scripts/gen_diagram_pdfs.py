"""Generate a separate PDF for each TikZ diagram in diagrams/."""
import os
import shutil
import subprocess
import sys

# Resolve project root (parent of scripts/)
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


def clean_output_dir():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def compile_diagram(tex_name):
    name = tex_name[:-4]
    input_rel = os.path.relpath(
        os.path.join(DIAGRAMS_DIR, tex_name), OUTPUT_DIR
    ).replace("\\", "/")

    wrapper_name = f"pdf_{name}.tex"
    wrapper_path = os.path.join(OUTPUT_DIR, wrapper_name)
    with open(wrapper_path, "w", encoding="utf-8") as f:
        f.write(WRAPPER_TEMPLATE.format(input_path=input_rel))

    result = subprocess.run(
        ["lualatex", "-interaction=nonstopmode", "-halt-on-error", wrapper_name],
        cwd=OUTPUT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        print(f"FAILED {name}")
        print(result.stdout[-500:])
        return False

    generated_pdf = os.path.join(OUTPUT_DIR, f"pdf_{name}.pdf")
    final_pdf = os.path.join(OUTPUT_DIR, f"{name}.pdf")
    if os.path.exists(generated_pdf):
        shutil.move(generated_pdf, final_pdf)
        print(f"OK -> {name}.pdf")
        return True
    print(f"PDF not found for {name}")
    return False


def clean_temp_files():
    for f in os.listdir(OUTPUT_DIR):
        if f.startswith("pdf_") or f.endswith((".aux", ".log", ".out", ".toc", ".lof")):
            try:
                os.remove(os.path.join(OUTPUT_DIR, f))
            except Exception:
                pass


def main():
    files = sorted([f for f in os.listdir(DIAGRAMS_DIR) if f.endswith(".tex")])
    print(f"Found {len(files)} diagram files")

    clean_output_dir()

    ok = 0
    failed = 0
    for fname in files:
        if compile_diagram(fname):
            ok += 1
        else:
            failed += 1

    clean_temp_files()
    print(f"Done: {ok} OK, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
