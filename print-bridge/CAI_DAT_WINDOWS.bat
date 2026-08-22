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
  for %%P in ("%LocalAppData%\Microsoft\WindowsApps\python.exe" "%ProgramFiles%\Python313\python.exe" "%ProgramFiles%\Python312\python.exe" "%ProgramFiles%\Python311\python.exe") do (
    if exist %%~P set "PY_CMD=%%~P"
  )
)

if not defined PY_CMD (
  echo Khong tim thay Python tren may.
  echo Hay mo Command Prompt va thu: python --version
  echo Neu Python da cai ma van loi, hay mo lai may roi chay file nay lan nua.
  pause
  exit /b 1
)

echo Da tim thay Python: %PY_CMD%
set "TARGET=%LOCALAPPDATA%\971RelaxCourt\AutoPrint"
if not exist "%TARGET%" mkdir "%TARGET%"
copy /Y "%~dp0971_print_bridge.py" "%TARGET%\971_print_bridge.py" >nul
(
 echo @echo off
 echo cd /d "%TARGET%"
 echo "%PY_CMD%" "%TARGET%\971_print_bridge.py"
) > "%TARGET%\START_AUTO_PRINT.bat"
set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
copy /Y "%TARGET%\START_AUTO_PRINT.bat" "%STARTUP%\971 Relax Court Auto Print.bat" >nul
echo.
echo Da cai dat xong. Chuong trinh se tu chay moi khi Windows khoi dong.
echo Dang mo Auto Print ngay bay gio...
start "971 Relax Court Auto Print" "%TARGET%\START_AUTO_PRINT.bat"
echo.
echo Neu Windows Firewall hoi, chon Allow access / Cho phep.
pause
