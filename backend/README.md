# Physical AI & Humanoid Robotics Book - RAG Backend

This is the backend API for the RAG (Retrieval-Augmented Generation) chatbot integrated into the Physical AI & Humanoid Robotics book. The API serves as the backend for the AI-powered assistant that can answer questions about the book's content.

## Architecture

The backend consists of:
- FastAPI server for handling API requests
- OpenAI integration for embeddings and generation
- Qdrant vector database for content storage and retrieval
- Neon Postgres for metadata management (optional)

## Setup

### Prerequisites
- Python 3.8+
- OpenAI API key
- Qdrant instance (local or cloud)
- (Optional) Neon Postgres database

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your configuration:
```env
OPENAI_API_KEY=your_openai_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
NEON_DB_URL=your_neon_postgres_connection_string_here  # Optional
```

## Running the Server

### Using the start script:
```bash
# On Windows
start_server.bat
```

### Or run directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### `POST /api/chat`
Send a chat message and receive an AI-generated response based on book content.

Request body:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Your question here"
    }
  ],
  "selected_text": "Optional text selected by user",
  "context": {
    "current_page": "/docs/intro",
    "current_section": "Introduction to Physical AI"
  }
}
```

Response:
```json
{
  "response": "AI-generated response",
  "sources": [
    {
      "title": "Page title",
      "url": "/docs/page-url",
      "relevance_score": 0.95
    }
  ]
}
```

### `POST /api/ingest`
Ingest book content into the vector database for retrieval.

Request body:
```json
{
  "content": "Full text content to be ingested",
  "title": "Title of the content",
  "url": "/docs/relative-url",
  "page": "Page identifier"
}
```

### `GET /health`
Check the health status of the API.

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `QDRANT_URL`: URL of your Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant (if using cloud)
- `NEON_DB_URL`: Connection string for Neon Postgres (optional)

## Development

For development, use the `--reload` flag to automatically restart the server when code changes:

```bash
uvicorn main:app --reload
```

### Alternative: Using the root npm commands

From the project root directory, you can use npm to run the backend:

```bash
npm run backend
```

To run both backend and frontend simultaneously:
```bash
npm run dev
```

## Deployment

The backend can be deployed to various platforms:
- Vercel (using serverless functions)
- Render
- AWS, GCP, Azure
- Self-hosted servers

Make sure to properly configure environment variables and use appropriate production databases when deploying.