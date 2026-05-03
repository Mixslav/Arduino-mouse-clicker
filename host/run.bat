@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set "PYEXE="

REM 1. Is Python already on PATH?
python --version >nul 2>&1
if !errorlevel! equ 0 set "PYEXE=python"

REM 2. Or in our standard per-user install location?
if "!PYEXE!"=="" (
    set "LOCAL_PY=%LocalAppData%\Programs\Python\Python312\python.exe"
    if exist "!LOCAL_PY!" set "PYEXE=!LOCAL_PY!"
)

REM 3. Otherwise download + install it silently.
if "!PYEXE!"=="" (
    echo.
    echo Python not found. Will download and install Python 3.12 ^(~30 MB^).
    echo You may see a Windows SmartScreen or antivirus prompt -- click "Run" / "Allow".
    echo.
    pause

    set "PY_URL=https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe"
    set "PY_INSTALLER=%TEMP%\python-3.12.7-amd64.exe"

    echo Downloading Python installer...
    curl -L -o "!PY_INSTALLER!" "!PY_URL!"
    if not exist "!PY_INSTALLER!" (
        echo.
        echo ERROR: Download failed. Check your internet connection.
        pause
        exit /b 1
    )

    echo Installing Python ^(silent, per-user, no admin needed^)...
    "!PY_INSTALLER!" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0

    set "PYEXE=%LocalAppData%\Programs\Python\Python312\python.exe"
    if not exist "!PYEXE!" (
        echo.
        echo ERROR: Python install did not complete.
        pause
        exit /b 1
    )

    del "!PY_INSTALLER!" 2>nul
    echo Python installed.
)

REM 4. Make sure pyserial + pynput are present.
"!PYEXE!" -c "import serial, pynput" >nul 2>&1
if !errorlevel! neq 0 (
    echo Installing Python packages ^(pyserial, pynput^)...
    "!PYEXE!" -m pip install --quiet --upgrade pip
    "!PYEXE!" -m pip install --quiet -r requirements.txt
    if !errorlevel! neq 0 (
        echo.
        echo ERROR: Failed to install Python packages.
        pause
        exit /b 1
    )
)

REM 5. Run.
echo.
echo Starting mouse clicker. Press Ctrl+C or close this window to quit.
echo.
"!PYEXE!" clicker.py
pause
