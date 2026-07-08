@echo off
echo Compiling main.tex...
cd /d "c:\Dev\Learning\VIII.HUST\Phân tích và thiết kế hệ thống\BaoCao"
"C:\Users\GHC\AppData\Roaming\TinyTeX\bin\windows\lualatex.exe" -interaction=nonstopmode main.tex
echo.
echo Done. Exit code: %errorlevel%
pause
