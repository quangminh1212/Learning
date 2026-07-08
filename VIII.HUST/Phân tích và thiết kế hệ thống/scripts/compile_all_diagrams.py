import subprocess
import os
import time
import sys
import shutil

# Set the working directory
work_dir = r"C:\Dev\Learning\VIII.HUST\Phân tích và thiết kế hệ thống\BaoCao\diagrams\tex"

try:
    os.chdir(work_dir)
    print(f"Working directory: {os.getcwd()}")
except Exception as e:
    print(f"Error changing directory: {e}")
    sys.exit(1)

lualatex = r"C:\Users\GHC\AppData\Roaming\TinyTeX\bin\windows\lualatex.exe"

try:
    # Get all .tex files
    tex_files = [f for f in os.listdir('.') if f.endswith('.tex')]
    tex_files.sort()
    print(f"Found {len(tex_files)} .tex files to compile")
except Exception as e:
    print(f"Error listing files: {e}")
    sys.exit(1)

print(f"Found {len(tex_files)} .tex files to compile")

success_count = 0
fail_count = 0

for tex_file in tex_files:
    base_name = tex_file.replace('.tex', '')
    print(f"\nCompiling {tex_file}...")
    
    # Delete old PDF and aux files
    for ext in ['.pdf', '.aux', '.log']:
        file_path = base_name + ext
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"  Deleted {file_path}")
    
    # Wait a moment
    time.sleep(0.2)
    
    # Run lualatex
    try:
        result = subprocess.run([lualatex, "-interaction=nonstopmode", tex_file], 
                               capture_output=True, text=True, timeout=30, shell=True)
        
        if result.returncode == 0 and os.path.exists(f"{base_name}.pdf"):
            size = os.path.getsize(f"{base_name}.pdf")
            print(f"  ✓ PDF created successfully: {size} bytes")
            success_count += 1
        else:
            print(f"  ✗ Failed to create PDF")
            print(f"  Return code: {result.returncode}")
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}")
            fail_count += 1
    except subprocess.TimeoutExpired:
        print(f"  ✗ Compilation timed out")
        fail_count += 1
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        fail_count += 1

print(f"\n{'='*50}")
print(f"Compilation complete: {success_count} succeeded, {fail_count} failed")
print(f"{'='*50}")