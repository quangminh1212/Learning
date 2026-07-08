@echo off
echo Downloading MiKTeX installer...
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://miktex.org/download/ctan/systems/win32/miktex/setup/windows-x64/basic-miktex-23.10-x64.exe', 'C:\Dev\Learning\miktex-installer.exe')"
echo Download complete.
echo Installing MiKTeX...
C:\Dev\Learning\miktex-installer.exe --portable --user-install=C:\Dev\Learning\miktex-portable
echo Installation complete.
