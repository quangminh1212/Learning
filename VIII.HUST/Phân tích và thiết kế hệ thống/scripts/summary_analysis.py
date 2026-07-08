from docx import Document

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        return f'Error: {str(e)}'

def analyze_missing_sections(ref_text, curr_text):
    ref_lines = ref_text.split('\n')
    curr_lines = curr_text.split('\n')
    
    missing_sections = []
    
    # Key sections that should be present based on reference
    key_sections = [
        "PHÂN CÔNG CÔNG VIỆC",
        "Khảo sát hiện trạng", 
        "Thực trạng quy trình quản lý hiện tại và các hạn chế",
        "Biểu đồ usecase tổng quát",
        "Biểu đồ usecase phân rã", 
        "Đặc tả usecase",
        "Phân tích cấu trúc",
        "Phân tích hành vi",
        "Biểu đồ lớp",
        "Biểu đồ trình tự"
    ]
    
    for section in key_sections:
        if section not in curr_text:
            missing_sections.append(section)
    
    return missing_sections

def analyze_structure_differences(ref_text, curr_text):
    ref_lines = ref_text.split('\n')
    curr_lines = curr_text.split('\n')
    
    analysis = {
        'ref_total_lines': len(ref_lines),
        'curr_total_lines': len(curr_lines),
        'ref_non_empty': len([l for l in ref_lines if l.strip()]),
        'curr_non_empty': len([l for l in curr_lines if l.strip()]),
        'missing_usecase_details': False,
        'missing_class_diagrams': False,
        'missing_sequence_diagrams': False,
        'missing_analysis_sections': False
    }
    
    # Check for specific content
    usecase_keywords = ['UC01', 'UC02', 'UC03', 'UC04', 'UC05', 'UC06', 'UC07', 'UC08', 'UC09', 'UC10', 'UC11', 'UC12', 'UC13']
    class_diagram_keywords = ['Biểu đồ lớp', 'class diagram', 'Class']
    sequence_diagram_keywords = ['Biểu đồ trình tự', 'sequence diagram', 'Sequence']
    
    ref_usecase_count = sum(1 for keyword in usecase_keywords if keyword in ref_text)
    curr_usecase_count = sum(1 for keyword in usecase_keywords if keyword in curr_text)
    
    if curr_usecase_count < ref_usecase_count:
        analysis['missing_usecase_details'] = True
    
    if 'Biểu đồ lớp' not in curr_text:
        analysis['missing_class_diagrams'] = True
    
    if 'Biểu đồ trình tự' not in curr_text:
        analysis['missing_sequence_diagrams'] = True
        
    if 'Phân tích cấu trúc' not in curr_text or 'Phân tích hành vi' not in curr_text:
        analysis['missing_analysis_sections'] = True
    
    return analysis

reference_doc = r'C:\Dev\Learning\VIII.HUST\Phân tích và thiết kế hệ thống\request\TaiLieuMau\Nhóm 3_Phân tích&Thiết kế hệ thống quản lý du học sinh bậc đại học của trung tâm tư vấnn du học FlyHigh (2).docx'
current_doc = r'C:\Dev\Learning\VIII.HUST\Phân tích và thiết kế hệ thống\request\Bai Tap Lon\Nhóm 3\Nhóm 3_Phân tích&Thiết kế hệ thống quản lý du học sinh bậc đại học của trung tâm tư vấnn du học FlyHigh.docx'

print('=== ANALYZING DOCUMENT DIFFERENCES ===')
reference_text = extract_text_from_docx(reference_doc)
current_text = extract_text_from_docx(current_doc)

missing_sections = analyze_missing_sections(reference_text, current_text)
structure_analysis = analyze_structure_differences(reference_text, current_text)

# Save summary to file
with open(r'C:\Dev\Learning\comparison_summary.txt', 'w', encoding='utf-8') as f:
    f.write('=== COMPARISON SUMMARY ===\n\n')
    
    f.write('STRUCTURAL DIFFERENCES:\n')
    f.write(f'Reference document: {structure_analysis["ref_total_lines"]} total lines, {structure_analysis["ref_non_empty"]} non-empty lines\n')
    f.write(f'Current document: {structure_analysis["curr_total_lines"]} total lines, {structure_analysis["curr_non_empty"]} non-empty lines\n')
    f.write(f'Difference: {structure_analysis["ref_total_lines"] - structure_analysis["curr_total_lines"]} lines\n\n')
    
    f.write('MISSING SECTIONS:\n')
    if missing_sections:
        for section in missing_sections:
            f.write(f'- {section}\n')
    else:
        f.write('No major sections missing\n')
    f.write('\n')
    
    f.write('CONTENT ANALYSIS:\n')
    f.write(f'Missing Usecase details: {structure_analysis["missing_usecase_details"]}\n')
    f.write(f'Missing Class Diagrams: {structure_analysis["missing_class_diagrams"]}\n')
    f.write(f'Missing Sequence Diagrams: {structure_analysis["missing_sequence_diagrams"]}\n')
    f.write(f'Missing Analysis Sections: {structure_analysis["missing_analysis_sections"]}\n')
    f.write('\n')
    
    f.write('DETAILED MISSING CONTENT:\n')
    
    # Check for specific missing content
    if 'PHÂN CÔNG CÔNG VIỆC' not in current_text:
        f.write('- PHÂN CÔNG CÔNG VIỆC section is missing\n')
    
    if 'Khảo sát hiện trạng' not in current_text:
        f.write('- Khảo sát hiện trạng section is missing\n')
        
    if 'Thực trạng quy trình quản lý hiện tại và các hạn chế' not in current_text:
        f.write('- Thực trạng quy trình quản lý hiện tại và các hạn chế section is missing\n')
    
    if 'Quản lý thông tin học viên phân tán' not in current_text:
        f.write('- Details about分散管理学员信息的问题 are missing\n')
    
    if 'Khó khăn trong việc theo dõi hạn chót' not in current_text:
        f.write('- Details about deadline tracking difficulties are missing\n')
    
    if 'Theo dõi tài chính nhập nhằng' not in current_text:
        f.write('- Details about financial tracking issues are missing\n')
    
    if 'Mất kết nối thông tin sau khi bay' not in current_text:
        f.write('- Details about post-departure information disconnect are missing\n')
    
    if 'Công tác báo cáo, thống kê chậm trễ' not in current_text:
        f.write('- Details about delayed reporting and statistics are missing\n')
    
    if 'Biểu đồ usecase tổng quát' not in current_text:
        f.write('- Biểu đồ usecase tổng quát section is missing\n')
    
    if 'Biểu đồ usecase phân rã' not in current_text:
        f.write('- Biểu đồ usecase phân rã section is missing\n')
    
    if 'Đặc tả usecase' not in current_text:
        f.write('- Đặc tả usecase section is missing\n')
    
    if 'Phân tích cấu trúc' not in current_text:
        f.write('- Phân tích cấu trúc section is missing\n')
    
    if 'Phân tích hành vi' not in current_text:
        f.write('- Phân tích hành vi section is missing\n')
    
    # Check for specific UC sections
    for uc_num in range(1, 14):
        uc_label = f'UC{uc_num:02d}'
        if uc_label in reference_text and uc_label not in current_text:
            f.write(f'- {uc_label} usecase details are missing\n')
    
    # Check for diagram sections
    diagram_sections = [
        'Biểu đồ lớp trong ca sử dụng UC01',
        'Biểu đồ trình tự cho ca sử dụng UC01'
    ]
    
    for diagram in diagram_sections:
        if diagram in reference_text and diagram not in current_text:
            f.write(f'- {diagram} section is missing\n')
    
    f.write('\nRECOMMENDATIONS:\n')
    f.write('1. Add the missing PHÂN CÔNG CÔNG VIỆC section at the beginning\n')
    f.write('2. Add the Khảo sát hiện trạng section with current state analysis\n')
    f.write('3. Include detailed analysis of current management limitations\n')
    f.write('4. Add Biểu đồ usecase tổng quát and Biểu đồ usecase phân rã sections\n')
    f.write('5. Include detailed usecase specifications (UC01-UC13)\n')
    f.write('6. Add Phân tích cấu trúc section with class diagrams\n')
    f.write('7. Add Phân tích hành vi section with sequence diagrams\n')
    f.write('8. Ensure all business operations are documented with the same level of detail\n')

print('=== Comparison summary saved to comparison_summary.txt ===')
print('=== Key findings ===')
print(f'Missing sections: {len(missing_sections)}')
print(f'Structural difference: {structure_analysis["ref_total_lines"] - structure_analysis["curr_total_lines"]} lines')
print(f'Missing usecase details: {structure_analysis["missing_usecase_details"]}')
print(f'Missing class diagrams: {structure_analysis["missing_class_diagrams"]}')
print(f'Missing sequence diagrams: {structure_analysis["missing_sequence_diagrams"]}')
print(f'Missing analysis sections: {structure_analysis["missing_analysis_sections"]}')
