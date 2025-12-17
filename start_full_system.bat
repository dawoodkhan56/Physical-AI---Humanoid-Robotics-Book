@echo off
REM Script to start both backend and frontend for testing

echo Starting Physical AI & Humanoid Robotics Book - Full System
echo.

REM Start backend server in background
echo Starting backend server...
start "Backend Server" cmd /c "cd backend && uvicorn main:app --reload --port 8000"

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 10

REM Start frontend in background
echo Starting frontend server...
start "Frontend Server" cmd /c "cd website && npm run start"

echo.
echo Both servers started!
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:3000
echo.
echo The chatbot should appear on all book pages.
echo Press any key to stop both servers.
pause

REM Note: This script doesn't actually stop the servers
REM You'll need to manually close the command windows or use Ctrl+C in each