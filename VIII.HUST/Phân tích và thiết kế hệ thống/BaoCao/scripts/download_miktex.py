import urllib.request
import os

url = "https://miktex.org/download/ctan/systems/win32/miktex/setup/windows-x64/basic-miktex-23.10-x64.exe"
output = r"C:\Dev\Learning\miktex-installer.exe"

print(f"Downloading from {url}...")
try:
    urllib.request.urlretrieve(url, output)
    print(f"Downloaded to {output}")
except Exception as e:
    print(f"Error: {e}")
