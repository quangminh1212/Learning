from pathlib import Path
import os
import re
import sys


ANSWERS = {
    "de1.tex": [
        "B", "BDE", "CD", "AE", "B", "F", "C", "E", "D", "B",
        "F", "BCD", "EF", "ABC", "CD", "BCD", "ACE", "ABE", "C", "D",
    ],
    "de2.tex": [
        "A", "BC", "DE", "BCD", "A", "C", "B", "F", "D", "B",
        "AC", "ABCEF", "CEF", "ABCE", "BCD", "BCD", "ABCD", "ABD", "ACDE", "CD",
    ],
}

ANSWER_SECTION = r"\section*{ĐÁP ÁN VÀ LỜI GIẢI THAM KHẢO}"
QUESTION_BLOCK_RE = re.compile(
    r"\\begin\{(pa|itemize)\}(\[[^\]]*\])?(.*?)\\end\{\1\}", re.S
)
OPTION_RE = re.compile(
    r"(?m)^(\s*(?:\\([A-F])|\\item\[([A-F])\.\])\s+)(.*)$"
)


def prepare_update(path: Path, answers: list[str]) -> tuple[str, int]:
    original = path.read_text(encoding="utf-8")
    question_source, marker, _answer_source = original.partition(ANSWER_SECTION)
    if not marker:
        raise ValueError(f"{path.name}: answer section marker not found; file left unchanged")

    blocks = [
        match for match in QUESTION_BLOCK_RE.finditer(question_source)
        if OPTION_RE.search(match.group(3))
    ]
    if len(blocks) != len(answers):
        raise RuntimeError(
            f"{path.name}: found {len(blocks)} multiple-choice blocks; "
            f"expected {len(answers)}; file left unchanged"
        )

    chunks = []
    position = 0
    for question_index, match in enumerate(blocks):
        chunks.append(question_source[position:match.start()])
        correct = set(answers[question_index])
        present = {
            option.group(2) or option.group(3)
            for option in OPTION_RE.finditer(match.group(3))
        }
        if not correct or not correct.issubset(present):
            raise RuntimeError(
                f"{path.name}: question {question_index + 1} answer labels "
                f"{''.join(sorted(correct))} do not match options "
                f"{''.join(sorted(present))}; file left unchanged"
            )

        def bold_correct(option_match: re.Match[str]) -> str:
            prefix = option_match.group(1)
            letter = option_match.group(2) or option_match.group(3) or ""
            content = option_match.group(4)
            if letter not in correct or content.lstrip().startswith(r"{\bfseries "):
                return prefix + content
            return prefix + r"{\bfseries " + content + "}"

        body = OPTION_RE.sub(bold_correct, match.group(3))
        opening = r"\begin{" + match.group(1) + "}" + (match.group(2) or "")
        chunks.append(opening + body + r"\end{" + match.group(1) + "}")
        position = match.end()

    chunks.append(question_source[position:])
    updated = "".join(chunks) + ANSWER_SECTION + _answer_source
    return updated, len(blocks)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")

    root = Path(__file__).resolve().parent
    updates = []
    for filename, answers in ANSWERS.items():
        path = root / filename
        updated, count = prepare_update(path, answers)
        updates.append((path, updated, count))

    for path, updated, _count in updates:
        original = path.read_text(encoding="utf-8")
        if updated == original:
            continue
        temporary = path.with_suffix(path.suffix + ".tmp")
        try:
            with temporary.open("w", encoding="utf-8", newline="") as stream:
                stream.write(updated)
            os.replace(temporary, path)
        finally:
            if temporary.exists():
                temporary.unlink()

    for path, _updated, count in updates:
        print(f"{path.name}: {count} questions processed")


if __name__ == "__main__":
    main()
