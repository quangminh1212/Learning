from docx import Document
import re

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        return f'Error: {str(e)}'

def get_document_structure(text):
    lines = text.split('\n')
    structure = {
        'total_lines': len(lines),
        'non_empty_lines': len([l for l in lines if l.strip()]),
        'sections': [],
        'headings': []
    }
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped:
            # Detect potential headings (all caps or short lines)
            if stripped.isupper() and len(stripped) < 100:
                structure['headings'].append(f"Line {i+1}: {stripped}")
            # Detect section markers
            if any(keyword in stripped.lower() for keyword in ['phần', 'chương', 'nghiệp vụ', 'mục', 'bước']):
                structure['sections'].append(f"Line {i+1}: {stripped}")
    
    return structure

def compare_documents(ref_text, curr_text):
    ref_lines = ref_text.split('\n')
    curr_lines = curr_text.split('\n')
    
    comparison = {
        'length_difference': len(ref_text) - len(curr_text),
        'line_difference': len(ref_lines) - len(curr_lines),
        'missing_content': [],
        'different_content': [],
        'additional_content': []
    }
    
    # Compare line by line
    max_lines = max(len(ref_lines), len(curr_lines))
    for i in range(max_lines):
        ref_line = ref_lines[i] if i < len(ref_lines) else ""
        curr_line = curr_lines[i] if i < len(curr_lines) else ""
        
        if ref_line and not curr_line:
            comparison['missing_content'].append(f"Line {i+1}: {ref_line[:100]}...")
        elif curr_line and not ref_line:
            comparison['additional_content'].append(f"Line {i+1}: {curr_line[:100]}...")
        elif ref_line != curr_line and ref_line and curr_line:
            comparison['different_content'].append(f"Line {i+1}: REF: {ref_line[:50]}... | CURR: {curr_line[:50]}...")
    
    return comparison

reference_doc = r'C:\Dev\Learning\VIII.HUST\Phân tích và thiết kế hệ thống\request\TaiLieuMau\Nhóm 3_Phân tích&Thiết kế hệ thống quản lý du học sinh bậc đại học của trung tâm tư vấnn du học FlyHigh (2).docx'
current_doc = r'C:\Dev\Learning\VIII.HUST\Phân tích và thiết kế hệ thống\request\Bai Tap Lon\Nhóm 3\Nhóm 3_Phân tích&Thiết kế hệ thống quản lý du học sinh bậc đại học của trung tâm tư vấnn du học FlyHigh.docx'

print('=== EXTRACTING TEXT FROM DOCUMENTS ===')
reference_text = extract_text_from_docx(reference_doc)
current_text = extract_text_from_docx(current_doc)

print('=== DOCUMENT STRUCTURE ANALYSIS ===')
ref_structure = get_document_structure(reference_text)
curr_structure = get_document_structure(current_text)

print(f"\nReference document:")
print(f"- Total lines: {ref_structure['total_lines']}")
print(f"- Non-empty lines: {ref_structure['non_empty_lines']}")
print(f"- Headings found: {len(ref_structure['headings'])}")
print(f"- Sections found: {len(ref_structure['sections'])}")

print(f"\nCurrent document:")
print(f"- Total lines: {curr_structure['total_lines']}")
print(f"- Non-empty lines: {curr_structure['non_empty_lines']}")
print(f"- Headings found: {len(curr_structure['headings'])}")
print(f"- Sections found: {len(curr_structure['sections'])}")

print('\n=== CONTENT COMPARISON ===')
comparison = compare_documents(reference_text, current_text)

print(f"Length difference: {comparison['length_difference']} characters")
print(f"Line difference: {comparison['line_difference']} lines")
print(f"Missing content lines: {len(comparison['missing_content'])}")
print(f"Different content lines: {len(comparison['different_content'])}")
print(f"Additional content lines: {len(comparison['additional_content'])}")

# Save detailed comparison to file
with open(r'C:\Dev\Learning\detailed_comparison.txt', 'w', encoding='utf-8') as f:
    f.write('=== DETAILED COMPARISON ===\n\n')
    f.write(f'Length difference: {comparison["length_difference"]} characters\n')
    f.write(f'Line difference: {comparison["line_difference"]} lines\n\n')
    
    f.write('=== REFERENCE HEADINGS ===\n')
    for heading in ref_structure['headings']:
        f.write(heading + '\n')
    
    f.write('\n=== CURRENT HEADINGS ===\n')
    for heading in curr_structure['headings']:
        f.write(heading + '\n')
    
    f.write('\n=== REFERENCE SECTIONS ===\n')
    for section in ref_structure['sections']:
        f.write(section + '\n')
    
    f.write('\n=== CURRENT SECTIONS ===\n')
    for section in curr_structure['sections']:
        f.write(section + '\n')
    
    f.write('\n=== MISSING CONTENT (First 100) ===\n')
    for item in comparison['missing_content'][:100]:
        f.write(item + '\n')
    
    f.write('\n=== DIFFERENT CONTENT (First 100) ===\n')
    for item in comparison['different_content'][:100]:
        f.write(item + '\n')
    
    f.write('\n=== ADDITIONAL CONTENT (First 50) ===\n')
    for item in comparison['additional_content'][:50]:
        f.write(item + '\n')

print('=== Detailed comparison saved to detailed_comparison.txt ===')
