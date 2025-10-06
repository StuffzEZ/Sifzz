@echo off
setlocal enabledelayedexpansion

REM Scan for .sfzz files
set "fileCount=0"
for %%f in (*.sfzz) do (
    set /a fileCount+=1
    set "file[!fileCount!]=%%f"
)

if %fileCount%==0 (
    echo No .sfzz files found.
    pause
    exit /b
)

echo Found .sfzz files:
for /l %%i in (1,1,%fileCount%) do (
    echo %%i. !file[%%i]!
)

set /p fileChoice=Enter the number of the .sfzz file to run: 

REM Validate choice
if "%fileChoice%"=="" (
    echo No selection made.
    pause
    exit /b
)
if %fileChoice% lss 1 (
    echo Invalid selection.
    pause
    exit /b
)
if %fileChoice% gtr %fileCount% (
    echo Invalid selection.
    pause
    exit /b
)

set "selectedFile=!file[%fileChoice%]!"

set /p debugFlag=Enable debug mode? (y [RECOMMENDED]/n): 
if /i "%debugFlag%"=="y" (
    python sifzz.py "!selectedFile!" -d
) else (
    python sifzz.py "!selectedFile!"
)