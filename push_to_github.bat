@echo off
title CineMatch - Push to dsa-movie-recommender-project
color 0b
echo ======================================================================
echo    CineMatch - Push to New GitHub Repository
echo    Target: https://github.com/saranshsawal/dsa-movie-recommender-project.git
echo ======================================================================
echo.
echo Staging all files...
git add -A
echo.
echo Committing latest code...
git commit -m "Initial commit for dsa-movie-recommender-project: All features, algorithms, datasets, and tests"
echo.
echo Pushing all files to https://github.com/saranshsawal/dsa-movie-recommender-project.git ...
git push -u origin main --force
echo.
if %ERRORLEVEL% EQU 0 (
    echo ======================================================================
    echo   [SUCCESS] Successfully pushed all files to:
    echo   https://github.com/saranshsawal/dsa-movie-recommender-project
    echo ======================================================================
) else (
    echo ======================================================================
    echo   [NOTE] If GitHub prompts you, click 'Sign in with your browser'.
    echo ======================================================================
)
echo.
pause
