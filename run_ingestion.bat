@echo off
REM Script to run the content ingestion pipeline for the RAG system

echo Setting up the Physical AI & Humanoid Robotics Book content in the vector database...

REM Navigate to the backend directory
cd backend

REM Make sure environment variables are set
if not defined OPENAI_API_KEY (
    echo OPENAI_API_KEY environment variable is not set
    echo Please set it before running this script
    pause
    exit /b 1
)

if not defined QDRANT_URL (
    echo QDRANT_URL environment variable is not set
    echo Please set it before running this script
    pause
    exit /b 1
)

if not defined QDRANT_API_KEY (
    echo QDRANT_API_KEY environment variable is not set
    echo Please set it before running this script
    pause
    exit /b 1
)

echo Running the content ingestion pipeline...

python ingest_pipeline.py

echo.
echo Ingestion pipeline completed.
echo You can now start the backend API server with: start_server.bat
pause