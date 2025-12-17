# Physical AI & Humanoid Robotics Book

This repository contains the complete implementation of the "Physical AI & Humanoid Robotics: Bridging Digital Brains and Physical Bodies" book project with an integrated RAG (Retrieval-Augmented Generation) chatbot.

## Project Overview

This project implements a comprehensive educational resource about Physical AI and Humanoid Robotics with the following key components:

1. **Docusaurus-based Book**: A complete online book with chapters covering ROS 2, Gazebo simulation, NVIDIA Isaac, and Vision-Language-Action systems
2. **RAG-Based Chatbot**: An AI-powered assistant integrated into the book that can answer questions about the content using OpenAI embeddings and Qdrant vector database
3. **Modern Architecture**: Using FastAPI for the backend, React for the frontend, and cloud-native technologies

## Architecture

### Frontend (Docusaurus)
- Hosted on GitHub Pages
- Custom chatbot component with text selection handler
- Responsive design with modern UI/UX

### Backend (FastAPI)
- `/api/chat` - Main chat endpoint with retrieval-augmented generation
- `/api/search` - Semantic search functionality
- `/api/query` - Advanced query with filtering
- `/api/ingest` - Content ingestion endpoint
- `/api/pages` - List indexed pages
- `/api/stats` - System statistics

### Data Layer
- Qdrant vector database for content embeddings
- OpenAI for generating embeddings and responses
- Optional Neon Postgres for metadata (if needed)

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js and npm (v20 or higher)
- OpenAI API key
- Qdrant account (free tier available)

### Quick Setup with npm

The project now includes npm scripts to run both backend and frontend simultaneously:

```bash
# Install dependencies
npm install
npm run install

# Set up backend environment
npm run setup-backend

# Run both servers simultaneously (frontend on port 3000, backend on port 8000)
npm start
```

### Manual Setup

#### 1. Clone the repository
```bash
git clone <repository-url>
cd Physical-AI---Humanoid-Robotics-Book
```

#### 2. Set up the backend
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys and connection strings
```

#### 3. Populate the vector database
```bash
# Run the ingestion script to process book content
python ingest_pipeline.py
```

#### 4. Set up and run the frontend
```bash
# Navigate to website directory
cd website

# Install dependencies
npm install

# Start the development server (with proxy to backend)
npm run start
```

## Available Scripts

The project root has npm scripts to manage both components:

- `npm run dev` - Run both frontend and backend simultaneously
- `npm run backend` - Run only the backend server
- `npm run frontend` - Run only the frontend server
- `npm run setup-backend` - Create Python virtual env and install deps
- `npm start` - Alias for `npm run dev` (run both servers)
- `npm run build` - Build the frontend for production

## Chatbot Fix

If you were experiencing HTTP 404 errors with the chatbot, this has been resolved by:
1. Adding a proxy configuration in `docusaurus.config.ts` to forward API requests from the frontend (port 3000) to the backend (port 8000)
2. Correcting the npm scripts to properly start both servers
3. Ensuring the backend is accessible during development

## Features

### Book Content
- Comprehensive modules covering ROS 2, Gazebo, Isaac Sim, and VLA systems
- Practical examples and code snippets
- Hardware requirements and setup guides
- Capstone project integrating all concepts

### RAG Chatbot
- Natural language queries about book content
- Text selection feature (select text and ask about it)
- Context-aware responses
- Source citations for fact-checking
- Streaming responses for better UX

### Technical Features
- Semantic search with vector similarity
- Content ingestion pipeline
- Error handling and logging
- Responsive UI design
- Modern security practices

## Deployment

### GitHub Pages
The book is configured for deployment to GitHub Pages. The workflow is set up in `.github/workflows/deploy.yml`.

### Backend Deployment
The FastAPI backend can be deployed to:
- Vercel
- Render
- Any platform supporting Python applications

## Contributing

Feel free to contribute to this project by:
1. Reporting issues
2. Submitting pull requests
3. Suggesting new features or improvements
4. Improving documentation

## License

This work is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0). See the LICENSE file for more details.

## About

This project was developed as part of the Panaversity initiative to create educational resources for Physical AI and Humanoid Robotics. The integration of modern AI techniques with robotics education represents a new approach to teaching embodied intelligence.

For more information about Panaversity and our other projects, visit [panaversity.com](https://panaversity.com).