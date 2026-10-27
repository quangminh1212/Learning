import re
import sys
import unicodedata
from pathlib import Path

import fitz


ANSWERS = {
    "de1.pdf": [
        "B", "BDE", "CD", "AE", "B", "F", "C", "E", "D", "B",
        "F", "BCD", "EF", "ABC", "CD", "BCD", "ACE", "ABE", "C", "D",
    ],
    "de2.pdf": [
        "A", "BC", "DE", "BCD", "A", "C", "B", "F", "D", "B",
        "A", "ABC", "CEF", "ABCE", "CD", "BCD", "ACD", "ABD", "AC", "D",
    ],
}


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text).split())


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

    ok = True
    for filename, answers in ANSWERS.items():
        path = Path(filename)
        doc = fitz.open(path)
        pages = [page.get_text() for page in doc]
        text = normalize(" ".join(pages))
        question_numbers = {
            int(number)
            for number in re.findall(r"Câu\s*(\d{1,2})\s*[.:]", text)
        }
        answer_checks = {
            f"Q{index}": bool(
                re.search(
                    rf"Câu\s*{index}\s*:\s*{re.escape(','.join(letters))}(?![A-F])",
                    text,
                )
            )
            for index, letters in enumerate(answers, start=1)
        }
        is_de1 = filename == "de1.pdf"
        required = (
            ["BookingPage", "BookingController", "ScreeningRoom", "HẾT"]
            if is_de1
            else [
                "ManHinhDatVe", "khachDaDenQuay", "huyDatVe",
                "minusHours(2)", "minusMinutes(30)", "80%", "HẾT",
                "triển khai vật lý cuối cùng",
                "một design class riêng cho mỗi protocol/interface/API",
                "hành vi/cấu trúc", "address dạng chuỗi tự",
            ]
        )
        result = {
            "pages": len(doc),
            "all_20_questions": set(range(1, 21)).issubset(question_numbers),
            "all_20_answer_keys_match": all(answer_checks.values()),
            "answer_heading": "ĐÁP ÁN VÀ LỜI GIẢI THAM KHẢO" in text,
            "system_prompt_count": text.count("System prompt"),
            "required_content": {item: item in text for item in required},
            "no_literal_ewpage": "ewpage" not in text,
        }
        expected_prompt_count = 2 if is_de1 else 1
        passed = (
            result["pages"] == 6
            and result["all_20_questions"]
            and result["all_20_answer_keys_match"]
            and result["answer_heading"]
            and result["system_prompt_count"] == expected_prompt_count
            and all(result["required_content"].values())
            and result["no_literal_ewpage"]
        )
        print(f"{filename}: {result}; {'PASS' if passed else 'FAIL'}")
        ok = ok and passed
        doc.close()

    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
