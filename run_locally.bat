@echo off
title CineMatch - Movie Recommendation Platform
echo ============================================================
echo Starting CineMatch Local Web Server...
echo ============================================================
echo Opening http://localhost:8000 in your default browser...
start http://localhost:8000/
echo.
echo Server running at http://127.0.0.1:8000/
echo Press Ctrl+C in this window to stop the server anytime.
echo.
python -m http.server 8000 --bind 127.0.0.1
pause
