import requests
import os

url = "https://miktex.org/download/ctan/systems/win32/miktex/setup/windows-x64/basic-miktex-23.10-x64.exe"
output = r"C:\Dev\Learning\miktex-installer.exe"

print(f"Downloading from {url}...")
try:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(output, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded to {output}")
except Exception as e:
    print(f"Error: {e}")
