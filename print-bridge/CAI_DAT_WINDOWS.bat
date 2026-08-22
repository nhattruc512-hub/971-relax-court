@echo off
chcp 65001 >nul
title 971 Relax Court - Cai dat Auto Print
cd /d "%~dp0"
echo ==========================================
echo   971 RELAX COURT - CAI DAT AUTO PRINT
echo ==========================================
echo.

set "PY_CMD="
where py >nul 2>nul
if not errorlevel 1 set "PY_CMD=py"
if not defined PY_CMD (
  where python >nul 2>nul
  if not errorlevel 1 set "PY_CMD=python"
)
if not defined PY_CMD (
  for %%P in ("%LocalAppData%\Microsoft\WindowsApps\python.exe" "%ProgramFiles%\Python314\python.exe" "%ProgramFiles%\Python313\python.exe" "%ProgramFiles%\Python312\python.exe" "%ProgramFiles%\Python311\python.exe") do (
    if exist %%~P set "PY_CMD=%%~P"
  )
)

if not defined PY_CMD (
  echo Khong tim thay Python tren may.
  echo Hay mo Command Prompt va thu: python --version
  pause
  exit /b 1
)

echo Da tim thay Python: %PY_CMD%
set "TARGET=%LOCALAPPDATA%\971RelaxCourt\AutoPrint"
if not exist "%TARGET%" mkdir "%TARGET%"

set "BRIDGE_SRC=%~dp0971_print_bridge.py"
set "BRIDGE_DST=%TARGET%\971_print_bridge.py"

if exist "%BRIDGE_SRC%" (
  copy /Y "%BRIDGE_SRC%" "%BRIDGE_DST%" >nul
) else (
  echo Khong thay 971_print_bridge.py trong thu muc tai ve.
  echo Dang tu tai Print Bridge tu GitHub...
  powershell -NoProfile -ExecutionPolicy Bypass -Command "try { Invoke-WebRequest -UseBasicParsing 'https://raw.githubusercontent.com/nhattruc512-hub/971-relax-court/main/print-bridge/971_print_bridge.py' -OutFile '%BRIDGE_DST%'; exit 0 } catch { Write-Host $_; exit 1 }"
  if errorlevel 1 (
    echo.
    echo KHONG TAI DUOC FILE PRINT BRIDGE.
    echo Kiem tra Internet roi chay lai CAI_DAT_WINDOWS.bat.
    pause
    exit /b 1
  )
)

if not exist "%BRIDGE_DST%" (
  echo Loi: file 971_print_bridge.py van chua ton tai sau khi cai dat.
  pause
  exit /b 1
)

(
 echo @echo off
 echo cd /d "%TARGET%"
 echo "%PY_CMD%" "%BRIDGE_DST%"
 echo pause
) > "%TARGET%\START_AUTO_PRINT.bat"

set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
copy /Y "%TARGET%\START_AUTO_PRINT.bat" "%STARTUP%\971 Relax Court Auto Print.bat" >nul

echo.
echo Da cai dat xong. Chuong trinh se tu chay moi khi Windows khoi dong.
echo Dang mo Auto Print ngay bay gio...
start "971 Relax Court Auto Print" "%TARGET%\START_AUTO_PRINT.bat"
echo.
echo Neu Windows Firewall hoi, chon Allow access / Cho phep.
echo Neu cua so Auto Print hien "Printer: 192.168.1.199:9100" la da thanh cong.
pause
