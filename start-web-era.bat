@echo off
echo Starting AI To-Do App - Web Era...

REM Start backend server in a separate window
start cmd /k "cd backend && python start_server.py"

REM Give backend a moment to start
timeout /t 3 /nobreak >nul

REM Start frontend server in a separate window
start cmd /k "cd frontend && npm run dev"

echo Servers started. Close this window to stop the servers.
pause