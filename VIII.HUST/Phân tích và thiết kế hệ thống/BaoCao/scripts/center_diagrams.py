"""Wrap every standalone tikzpicture in diagrams/ with \makebox[\textwidth][c]{...}."""
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DIAGRAMS_DIR = os.path.join(BASE_DIR, "diagrams")


def center_diagrams():
    count = 0
    for fname in sorted(os.listdir(DIAGRAMS_DIR)):
        if not fname.endswith(".tex"):
            continue
        path = os.path.join(DIAGRAMS_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Skip if already centered or if it uses resizebox (sequence diagrams)
        if r"\makebox[\textwidth][c]{" in content:
            continue
        if r"\resizebox{\textwidth}{!}{%" in content:
            continue

        lines = content.splitlines()
        new_lines = []
        in_tikz = False
        for line in lines:
            m_begin = re.match(r"^(\s*)\\begin\{tikzpicture\}", line)
            m_end = re.match(r"^(\s*)\\end\{tikzpicture\}", line)
            if m_begin and not in_tikz:
                indent = m_begin.group(1)
                new_lines.append(indent + r"\makebox[\textwidth][c]{%")
                new_lines.append(line)
                in_tikz = True
            elif m_end and in_tikz:
                indent = m_end.group(1)
                new_lines.append(line)
                new_lines.append(indent + "}")
                in_tikz = False
            else:
                new_lines.append(line)

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines))
        count += 1
        print(f"Centered {fname}")

    print(f"Done: {count} files updated")
    return 0


if __name__ == "__main__":
    sys.exit(center_diagrams())
