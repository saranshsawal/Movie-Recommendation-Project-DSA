@echo off
title CineMatch - Movie Recommendation Platform
color 0a
echo ============================================================
echo   Starting CineMatch Local Web Server
echo   Directory: %~dp0
echo ============================================================
echo.
cd /d "%~dp0"

:: Free any lingering port 8000 process
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do (
    echo Freeing port 8000 (PID: %%a)...
    taskkill /F /PID %%a >nul 2>&1
)

echo Opening http://localhost:8000 in your browser...
start http://localhost:8000/

echo.
echo ============================================================
echo   Server is running at: http://localhost:8000/
echo   Press Ctrl+C in this window to stop the server anytime.
echo ============================================================
echo.
python -m http.server 8000 --bind 127.0.0.1
pause
