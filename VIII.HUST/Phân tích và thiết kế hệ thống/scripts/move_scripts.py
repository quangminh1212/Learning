import shutil
import os

def move_scripts_to_scripts_folder():
    """Di chuyển tất cả script Python vào thư mục scripts"""
    
    # Thư mục đích
    scripts_folder = r'C:\Dev\Learning\VIII.HUST\Phân tích và thiết kế hệ thống\scripts'
    
    # Các script cần di chuyển
    scripts_to_move = [
        'add_pdf_diagrams.py',
        'convert_latex_to_word.py',
        'convert_pdf_to_images.py',
        'create_blackwhite_diagrams.py',
        'create_complete_word.py',
        'verify_blackwhite.py',
        'verify_complete_doc.py',
        'verify_converted_diagrams.py',
        'verify_word_conversion.py'
    ]
    
    moved_count = 0
    for script in scripts_to_move:
        source = os.path.join(r'C:\Dev\Learning', script)
        destination = os.path.join(scripts_folder, script)
        
        if os.path.exists(source):
            try:
                shutil.move(source, destination)
                print(f"Moved: {script}")
                moved_count += 1
            except Exception as e:
                print(f"Failed to move {script}: {e}")
        else:
            print(f"Not found: {script}")
    
    print(f"Total scripts moved: {moved_count}/{len(scripts_to_move)}")

if __name__ == '__main__':
    move_scripts_to_scripts_folder()
