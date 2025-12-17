# Quickstart Guide: Physical AI & Humanoid Robotics Interactive Book

## Overview
This guide will help you set up and run the Physical AI & Humanoid Robotics Interactive Book with RAG Chatbot locally. The project consists of two main components:
1. A Docusaurus-based book frontend
2. A FastAPI-based RAG backend

## Prerequisites
- Node.js 18+ (for Docusaurus)
- Python 3.11+ (for FastAPI backend)
- Docker (for local development of backend services)
- An OpenAI API key
- Accounts for Qdrant Cloud and Neon Postgres (or local alternatives)

## Backend Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Physical-AI---Humanoid-Robotics-Book
```

### 2. Setup Backend Environment
```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the `backend` directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
NEON_DATABASE_URL=your_neon_database_url_here
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=3600  # 1 hour in seconds
LOG_LEVEL=INFO
SECRET_KEY=your_secret_key_for_sessions
```

### 4. Start the Backend Service
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the backend server
uvicorn src.api.main:app --reload --port 8000
```
The backend will be available at `http://localhost:8000`.

## Frontend Setup

### 1. Navigate to the Book Directory
```bash
cd book  # From the project root
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Docusaurus
Update `docusaurus.config.js` with the backend API URL:
```js
module.exports = {
  // ... other config
  themeConfig: {
    // ... other theme config
    backendApiUrl: 'http://localhost:8000',  // For development
    // backendApiUrl: 'https://api.physical-ai-book.com',  // For production
  },
};
```

### 4. Run the Development Server
```bash
npm start
```
The book will be available at `http://localhost:3000`.

## Testing the RAG Chatbot

1. Make sure both the backend and frontend are running
2. Navigate to any page in the book
3. Select some text and click the "Ask about this" button that appears
4. Alternatively, ask a general question about the book content

## Running the Ingestion Pipeline

To populate the RAG system with book content:

1. Ensure your backend API is running
2. Run the ingestion script:

```bash
# From the backend directory with virtual environment activated
python -m src.scripts.ingest_book_content --book-path ../book/docs
```

## Docker Setup (Optional)

For easier local development, you can use the provided Docker configuration:

```bash
# From the project root
docker-compose up --build
```

This will start both the backend and any required services (like a local Qdrant instance if needed).

## API Documentation

Once the backend is running, you can access the interactive API documentation at:
- `http://localhost:8000/docs` - Swagger UI
- `http://localhost:8000/redoc` - ReDoc

## Troubleshooting

### Common Issues

1. **Backend not connecting to Qdrant/Neon**: Verify your API keys and connection strings in the `.env` file
2. **Rate limiting too restrictive**: Adjust `RATE_LIMIT_REQUESTS` in the environment variables
3. **Chatbot not appearing**: Verify that `backendApiUrl` is correctly set in `docusaurus.config.js`
4. **Content not found in RAG responses**: Run the ingestion pipeline again to ensure content is properly indexed

## Next Steps

- Implement authentication for better user tracking (beyond IP-based rate limiting)
- Set up automated content synchronization when book content updates
- Add support for custom user queries beyond the book content
- Implement analytics dashboard for content usage
- Set up CI/CD for automatic deployment