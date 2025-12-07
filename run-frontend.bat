@echo off
echo Starting ArchSense React Frontend...
echo.
cd /d "%~dp0\client"
echo Current directory: %CD%
echo.
echo Installing dependencies...
call npm install
echo.
echo Starting Vite development server...
call npx vite --host 0.0.0.0 --port 8080
pause
