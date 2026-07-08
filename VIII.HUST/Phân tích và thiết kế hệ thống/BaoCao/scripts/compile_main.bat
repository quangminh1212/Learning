@echo off
pushd "c:\Dev\Learning\VIII.HUST\Phân tích và thiết kế hệ thống\BaoCao"
"C:\Users\GHC\AppData\Roaming\TinyTeX\bin\windows\lualatex.exe" -interaction=nonstopmode main.tex
echo Compilation finished with exit code %errorlevel%
popd
