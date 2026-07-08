import urllib.request
import subprocess
import os
import sys
import shutil

# MiKTeX portable URL
url = "https://miktex.org/download/ctan/systems/win32/miktex/portable/miktex-portable-23.10-x64.exe"
output = r"C:\Dev\Learning\miktex-portable-installer.exe"
install_dir = r"C:\Dev\Learning\miktex-portable"

print(f"Downloading MiKTeX portable from {url}...")
try:
    # Download
    urllib.request.urlretrieve(url, output)
    print(f"Downloaded to {output}")
    print(f"File size: {os.path.getsize(output)} bytes")
    
    # Install portable
    print(f"Installing to {install_dir}...")
    if os.path.exists(install_dir):
        shutil.rmtree(install_dir)
    
    # Run installer
    result = subprocess.run([output, "--portable", f"--user-install={install_dir}"], 
                          capture_output=True, text=True)
    print(f"Installer return code: {result.returncode}")
    if result.stdout:
        print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    print("Installation complete!")
    
    # Find lualatex
    bin_dir = os.path.join(install_dir, "texmfs", "install", "miktex", "bin", "x64")
    if os.path.exists(bin_dir):
        print(f"lualatex should be in: {bin_dir}")
        print(f"Add this to your PATH")
    else:
        print(f"Bin directory not found at {bin_dir}")
        # Try to find it
        for root, dirs, files in os.walk(install_dir):
            if "lualatex.exe" in files:
                print(f"Found lualatex.exe at: {os.path.join(root, 'lualatex.exe')}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
