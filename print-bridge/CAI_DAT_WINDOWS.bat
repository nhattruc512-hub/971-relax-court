@echo off
chcp 65001 >nul
title 971 Relax Court - Cai dat Auto Print
cd /d "%~dp0"
echo ==========================================
echo   971 RELAX COURT - CAI DAT AUTO PRINT
echo ==========================================
echo.
where py >nul 2>nul
if errorlevel 1 (
  echo Chua co Python tren may.
  echo Hay cai Python 3 tu Microsoft Store hoac python.org, sau do chay lai file nay.
  pause
  exit /b 1
)
set "TARGET=%LOCALAPPDATA%\971RelaxCourt\AutoPrint"
if not exist "%TARGET%" mkdir "%TARGET%"
copy /Y "%~dp0971_print_bridge.py" "%TARGET%\971_print_bridge.py" >nul
(
 echo @echo off
 echo cd /d "%TARGET%"
 echo py "%TARGET%\971_print_bridge.py"
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
