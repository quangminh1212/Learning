from docx import Document
import sys

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        return f'Error: {str(e)}'

reference_doc = r'C:\Dev\Learning\VIII.HUST\Phân tích và thiết kế hệ thống\request\TaiLieuMau\Nhóm 3_Phân tích&Thiết kế hệ thống quản lý du học sinh bậc đại học của trung tâm tư vấnn du học FlyHigh (2).docx'
current_doc = r'C:\Dev\Learning\VIII.HUST\Phân tích và thiết kế hệ thống\request\Bai Tap Lon\Nhóm 3\Nhóm 3_Phân tích&Thiết kế hệ thống quản lý du học sinh bậc đại học của trung tâm tư vấnn du học FlyHigh.docx'

print('=== EXTRACTING TEXT FROM DOCUMENTS ===')
reference_text = extract_text_from_docx(reference_doc)
current_text = extract_text_from_docx(current_doc)

# Save the extracted texts to files for comparison
with open(r'C:\Dev\Learning\reference_text.txt', 'w', encoding='utf-8') as f:
    f.write(reference_text)

with open(r'C:\Dev\Learning\current_text.txt', 'w', encoding='utf-8') as f:
    f.write(current_text)

print('=== Text files saved ===')
print('Reference text saved to: reference_text.txt')
print('Current text saved to: current_text.txt')
print(f'Reference document length: {len(reference_text)} characters')
print(f'Current document length: {len(current_text)} characters')
