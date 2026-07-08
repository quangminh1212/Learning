from pdf2docx import Converter
import os

def convert_pdf_to_word():
    # Sử dụng đường dẫn tương đối và thay đổi thư mục làm việc
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    pdf_file = os.path.join(project_dir, "BaoCao", "main.pdf")
    output_file = os.path.join(project_dir, "BaoCao", "BaoCao_QuanLyKho_Full.docx")
    
    print(f"Converting {pdf_file} to {output_file}...")
    print(f"PDF file exists: {os.path.exists(pdf_file)}")
    
    if not os.path.exists(pdf_file):
        print(f"ERROR: PDF file not found at {pdf_file}")
        return None
    
    try:
        cv = Converter(pdf_file)
        cv.convert(output_file, start=0, end=None)
        cv.close()
        print(f"Successfully converted to {output_file}")
        return output_file
    except Exception as e:
        print(f"Error converting PDF to Word: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    convert_pdf_to_word()