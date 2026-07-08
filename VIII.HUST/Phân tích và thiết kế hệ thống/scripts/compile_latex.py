import subprocess
import os
import time

# Set the working directory
work_dir = r"c:\Dev\Learning\VIII.HUST\Phân tích và thiết kế hệ thống\BaoCao\diagrams\pdf"
os.chdir(work_dir)

lualatex = r"C:\Users\GHC\AppData\Roaming\TinyTeX\bin\windows\lualatex.exe"

print(f"Working directory: {os.getcwd()}")
print(f"Compiling pdf_3.1_bfd.tex...")

# Delete old PDF and aux files
for ext in ['.pdf', '.aux', '.log']:
    file_path = "pdf_3.1_bfd" + ext
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted {file_path}")

# Delete the target PDF
if os.path.exists("3.1_bfd.pdf"):
    os.remove("3.1_bfd.pdf")
    print("Deleted 3.1_bfd.pdf")

# Wait a moment
time.sleep(0.5)

# Run and save output to file
with open(r"c:\Dev\Learning\latex_output.txt", "w", encoding="utf-8", errors="ignore") as f:
    result = subprocess.run([lualatex, "-interaction=nonstopmode", "pdf_3.1_bfd.tex"], 
                           stdout=f, stderr=subprocess.STDOUT, text=True)

print(f"Return code: {result.returncode}")
print("Output saved to c:\Dev\Learning\latex_output.txt")

# Check if PDF was created
if os.path.exists("3.1_bfd.pdf"):
    size = os.path.getsize("3.1_bfd.pdf")
    print(f"PDF created successfully: {size} bytes")
else:
    print("PDF was not created!")
