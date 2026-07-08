@echo off
setlocal enabledelayedexpansion

set "LUALATEX=C:\Users\GHC\AppData\Roaming\TinyTeX\bin\windows\lualatex.exe"

echo Working directory: %CD%
echo.

for %%f in (*.tex) do (
    echo Compiling %%f...
    "%LUALATEX%" -interaction=nonstopmode "%%f"
    if exist "%%~nf.pdf" (
        echo   Success: %%~nf.pdf created
    ) else (
        echo   Failed: PDF not created
    )
    echo.
)

echo Compilation complete
pause