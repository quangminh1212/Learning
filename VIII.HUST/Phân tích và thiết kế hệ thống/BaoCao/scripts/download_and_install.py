import urllib.request
import subprocess
import os
import sys

url = "https://miktex.org/download/ctan/systems/win32/miktex/setup/windows-x64/basic-miktex-23.10-x64.exe"
output = r"C:\Dev\Learning\miktex-installer.exe"
install_dir = r"C:\Dev\Learning\miktex-portable"

print(f"Downloading MiKTeX from {url}...")
try:
    urllib.request.urlretrieve(url, output)
    print(f"Downloaded to {output}")
    
    print(f"Installing MiKTeX to {install_dir}...")
    subprocess.run([output, "--portable", f"--user-install={install_dir}"], check=True)
    print("Installation complete!")
    
    # Add to PATH
    bin_dir = os.path.join(install_dir, "texmfs", "install", "miktex", "bin", "x64")
    print(f"Add {bin_dir} to your PATH")
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
