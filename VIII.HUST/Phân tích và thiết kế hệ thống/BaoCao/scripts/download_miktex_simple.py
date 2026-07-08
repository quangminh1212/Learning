import urllib.request
import os

url = "https://miktex.org/download/ctan/systems/win32/miktex/setup/windows-x64/basic-miktex-23.10-x64.exe"
output = r"C:\Dev\Learning\miktex-installer.exe"

print("Starting download...")
urllib.request.urlretrieve(url, output)
print(f"Downloaded to {output}")
print(f"File size: {os.path.getsize(output)} bytes")
