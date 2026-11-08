@echo off
echo ======================================================================
echo    K.R. MANGALAM UNIVERSITY - DESIGN ^& ANALYSIS OF ALGORITHMS (ETCCDA302)
echo          CAPSTONE ASSIGNMENT: MINI-COURIER PLANNER
echo ======================================================================
echo Launching Mini-Courier Planner Interactive CLI...
echo.
python main.py
if errorlevel 1 (
    echo.
    echo [ERROR] Python failed to launch. Please ensure Python 3.8+ is installed and added to PATH.
    pause
)
