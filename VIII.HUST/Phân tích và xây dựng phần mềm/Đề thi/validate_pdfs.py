import fitz
from pathlib import Path

checks = [
    (Path('de1.pdf'), 5, True, False, True),
    (Path('de2.pdf'), 6, True, True, False),
    (Path('Đề 1') / 'De1_go_lai.pdf', 5, True, False, True),
    (Path('Đề 2') / 'De2_go_lai.pdf', 6, True, True, False),
]
ok = True
for path, expected_pages, has_answer, has_image, has_system_prompt in checks:
    doc = fitz.open(path)
    text = '\n'.join(page.get_text() for page in doc)
    images = sum(len(page.get_images(full=True)) for page in doc)
    result = {
        'pages': len(doc),
        'answer': 'ĐÁP ÁN' in text,
        'essay': ('Đặt Vé' in text) or ('Đặt vé' in text),
        'system_prompt': 'System prompt' in text,
        'images': images,
    }
    print(str(path).encode('unicode_escape').decode(), result)
    ok = ok and len(doc) == expected_pages and result['answer'] == has_answer and result['essay'] and (result['system_prompt'] == has_system_prompt) and ((images > 0) == has_image)
raise SystemExit(0 if ok else 1)
