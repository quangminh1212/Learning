from docx import Document

def verify_updated_document():
    updated_doc = Document(r'C:\Dev\Learning\VIII.HUST\Phân tích và thiết kế hệ thống\request\Bai Tap Lon\Nhóm 3\Nhóm 3_Phân tích&Thiết kế hệ thống quản lý du học sinh bậc đại học của trung tâm tư vấnn du học FlyHigh_UPDATED.docx')
    
    text_content = []
    for para in updated_doc.paragraphs:
        text_content.append(para.text)
    
    full_text = '\n'.join(text_content)
    
    # Kiểm tra các phần đã thêm
    checks = {
        'PHÂN CÔNG CÔNG VIỆC': 'PHÂN CÔNG CÔNG VIỆC' in full_text,
        'Khảo sát hiện trạng': 'Khảo sát hiện trạng' in full_text,
        'Thực trạng quy trình quản lý': 'Thực trạng quy trình quản lý' in full_text,
        'Mục tiêu của hệ thống': 'Mục tiêu của hệ thống' in full_text,
        'PHẦN 3: THIẾT KẾ HỆ THỐNG': 'PHẦN 3: THIẾT KẾ HỆ THỐNG' in full_text,
        'Biểu đồ usecase tổng quát': 'Biểu đồ usecase tổng quát' in full_text,
        'Biểu đồ usecase phân rã': 'Biểu đồ usecase phân rã' in full_text,
        'Đặc tả usecase': 'Đặc tả usecase' in full_text,
        'UC01: Quản lý account nhân viên': 'UC01: Quản lý account nhân viên' in full_text,
        'UC13: Xem thống kê': 'UC13: Xem thống kê' in full_text,
        'Phân tích cấu trúc': 'Phân tích cấu trúc' in full_text,
        'Phân tích hành vi': 'Phân tích hành vi' in full_text,
        'Biểu đồ lớp': 'Biểu đồ lớp' in full_text,
        'Biểu đồ trình tự': 'Biểu đồ trình tự' in full_text
    }
    
    with open(r'C:\Dev\Learning\verification_results.txt', 'w', encoding='utf-8') as f:
        f.write('VERIFICATION RESULTS\n')
        f.write('===================\n\n')
        f.write(f'Total paragraphs: {len(text_content)}\n')
        f.write(f'Total characters: {len(full_text)}\n\n')
        
        f.write('SECTION CHECKS:\n')
        for section, present in checks.items():
            status = 'PRESENT' if present else 'MISSING'
            f.write(f'{section}: {status}\n')
        
        f.write('\nALL SECTIONS PRESENT: ' + str(all(checks.values())) + '\n')
        
        f.write('\nDOCUMENT STRUCTURE:\n')
        for i, line in enumerate(text_content[:30]):  # First 30 lines
            if line.strip():
                f.write(f'{i+1}: {line[:80]}\n')
    
    print('Verification completed!')
    print('Results saved to verification_results.txt')
    
    # Print summary
    print('\nSUMMARY:')
    for section, present in checks.items():
        status = '✓' if present else '✗'
        print(f'{status} {section}')
    
    if all(checks.values()):
        print('\n✓ All sections successfully added!')
    else:
        print('\n✗ Some sections are still missing')

if __name__ == '__main__':
    verify_updated_document()
