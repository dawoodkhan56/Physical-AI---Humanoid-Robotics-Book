@echo off
REM Script to start the FastAPI backend server

echo Starting the Physical AI & Humanoid Robotics Book RAG API...

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo Warning: Virtual environment not found. Make sure you've created it with 'python -m venv venv'
)

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
    pip install -r requirements.txt
    echo Dependencies installed
) else (
    echo Warning: requirements.txt not found
)

REM Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000