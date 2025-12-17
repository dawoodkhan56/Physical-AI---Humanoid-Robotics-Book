---
sidebar_position: 11
title: RAG Chatbot Integration
---

# RAG Chatbot Integration

## Overview

The integrated RAG (Retrieval-Augmented Generation) chatbot is a key feature of this interactive book, providing students with an AI-powered assistant that can answer questions about the book's content. This chatbot uses OpenAI's models, Qdrant for vector storage, Neon Postgres for metadata management, and FastAPI for the backend API, all designed to be resource-efficient and free-tier friendly.

## Architecture

The RAG chatbot system consists of three main components:

### Frontend (Docusaurus Integration)
- Custom React component embedded in the Docusaurus book
- Text selection handler for contextual queries
- Streaming response interface
- Clean, accessible UI that matches the book's theme

### Backend (FastAPI Server)
- Ingestion pipeline to process book content
- Query endpoint with retrieval and generation capabilities
- Integration with OpenAI API for embeddings and generation
- Qdrant client for vector search
- Neon Postgres client for metadata storage

### Data Pipeline
- Document parsing and chunking
- Embedding generation using OpenAI models
- Vector storage in Qdrant
- Metadata storage in Neon Postgres

## Frontend Implementation

### Chatbot Component

```jsx
// src/components/BookChatbot.jsx
import React, { useState, useRef, useEffect } from 'react';
import { useLocation } from '@docusaurus/router';

const BookChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef(null);
  const location = useLocation();
  
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };
  
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  // Listen for text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      if (selection.toString().trim() !== '') {
        setSelectedText(selection.toString());
      }
    };
    
    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);
  
  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;
    
    const userMessage = { role: 'user', content: input };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);
    
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: newMessages,
          selected_text: selectedText,
          context: {
            current_page: location.pathname,
            current_section: document.title
          }
        })
      });
      
      if (!response.ok) throw new Error('Failed to get response');
      
      const data = await response.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.' 
      }]);
    } finally {
      setIsLoading(false);
      setSelectedText(''); // Clear selection after sending
    }
  };
  
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };
  
  const askAboutSelection = () => {
    if (selectedText) {
      setInput(`Explain this: "${selectedText}"`);
    }
  };
  
  return (
    <div className={`chatbot-container ${isOpen ? 'open' : 'closed'}`}>
      {!isOpen ? (
        <button 
          className="chatbot-toggle"
          onClick={() => setIsOpen(true)}
          aria-label="Open chatbot"
        >
          💬
        </button>
      ) : (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <h3>Book Assistant</h3>
            <button 
              className="chatbot-close"
              onClick={() => setIsOpen(false)}
              aria-label="Close chatbot"
            >
              ×
            </button>
          </div>
          
          {selectedText && (
            <div className="selection-quick-action">
              <button onClick={askAboutSelection}>
                Ask about selected text: "{selectedText.substring(0, 30)}..."
              </button>
            </div>
          )}
          
          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <p>Hello! I'm your Physical AI & Humanoid Robotics assistant.</p>
                <p>Ask me questions about the content, or select text and click the button to ask about it.</p>
              </div>
            ) : (
              messages.map((msg, index) => (
                <div key={index} className={`message ${msg.role}`}>
                  <div className="message-content">{msg.content}</div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="message assistant">
                <div className="message-content">Thinking...</div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          
          <div className="chatbot-input">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question about Physical AI & Humanoid Robotics..."
              disabled={isLoading}
              rows={2}
            />
            <button 
              onClick={sendMessage} 
              disabled={!input.trim() || isLoading}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default BookChatbot;
```

### CSS Styling

```css
/* src/css/chatbot.css */
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.chatbot-toggle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: none;
  background: var(--ifm-color-primary);
  color: white;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
}

.chatbot-window {
  width: 350px;
  height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid #e0e0e0;
}

.chatbot-header {
  background: var(--ifm-color-primary);
  color: white;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chatbot-header h3 {
  margin: 0;
  font-size: 16px;
}

.chatbot-close {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.selection-quick-action {
  background: #f5f5f5;
  padding: 8px;
  border-bottom: 1px solid #e0e0e0;
}

.selection-quick-action button {
  background: #e3f2fd;
  border: 1px solid #2196f3;
  color: #1976d2;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.chatbot-messages {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.welcome-message {
  color: #666;
  font-style: italic;
  text-align: center;
  padding: 20px 0;
}

.message {
  max-width: 80%;
  padding: 10px 15px;
  border-radius: 18px;
  line-height: 1.4;
}

.message.user {
  background: var(--ifm-color-primary);
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}

.message.assistant {
  background: #f0f0f0;
  color: #333;
  align-self: flex-start;
  border-bottom-left-radius: 4px;
}

.chatbot-input {
  padding: 15px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  gap: 10px;
}

.chatbot-input textarea {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 18px;
  padding: 10px 15px;
  resize: none;
  font-size: 14px;
  max-height: 100px;
}

.chatbot-input button {
  background: var(--ifm-color-primary);
  color: white;
  border: none;
  border-radius: 18px;
  padding: 10px 20px;
  cursor: pointer;
  font-weight: 500;
}

.chatbot-input button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}
```

## Backend Implementation

### FastAPI Backend

```python
# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import openai
import asyncpg
from qdrant_client import QdrantClient
from qdrant_client.http import models
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Book RAG Chatbot API")

# Pydantic models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    selected_text: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[Dict[str, Any]]] = None

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
NEON_DB_URL = os.getenv("NEON_DB_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize clients
qdrant_client = QdrantClient(url=QDRANT_URL)
openai.api_key = OPENAI_API_KEY

@app.on_event("startup")
async def startup_event():
    # Initialize the Qdrant collection if it doesn't exist
    try:
        qdrant_client.get_collection("book_content")
    except:
        # Create collection if it doesn't exist
        qdrant_client.recreate_collection(
            collection_name="book_content",
            vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),  # 1536 for text-embedding-ada-002
        )
        logger.info("Initialized Qdrant collection")

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Prepare context for the query
        query_context = request.selected_text or request.messages[-1].content
        
        # Retrieve relevant content from vector store
        retrieved_docs = await retrieve_relevant_content(query_context)
        
        # Formulate system prompt with context
        system_prompt = f"""
        You are an AI assistant for the Physical AI & Humanoid Robotics book. 
        Your purpose is to help students understand the content of the book.
        
        Use only the following context to answer questions. Do not make up information:
        {format_retrieved_content(retrieved_docs)}
        
        If the context doesn't contain relevant information to answer the question, 
        say "I don't have enough information from the book content to answer that question. 
        Please refer to the relevant chapter."
        
        Keep your answers accurate, concise, and educational. Reference the source 
        material when possible.
        """
        
        # Prepare messages for OpenAI API
        openai_messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        # Add conversation history
        for msg in request.messages:
            openai_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Get response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4 if available
            messages=openai_messages,
            temperature=0.3,
            max_tokens=1000
        )
        
        ai_response = response.choices[0].message['content']
        
        # Extract sources for response
        sources = extract_sources(retrieved_docs)
        
        return ChatResponse(
            response=ai_response,
            sources=sources
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def retrieve_relevant_content(query: str, top_k: int = 5):
    """Retrieve relevant content chunks from the vector store"""
    # Generate embedding for the query
    embedding_response = openai.Embedding.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_embedding = embedding_response['data'][0]['embedding']
    
    # Search in Qdrant
    search_results = qdrant_client.search(
        collection_name="book_content",
        query_vector=query_embedding,
        limit=top_k
    )
    
    # Get the content and metadata for the top results
    retrieved_docs = []
    for result in search_results:
        retrieved_docs.append({
            "content": result.payload["content"],
            "title": result.payload.get("title", ""),
            "url": result.payload.get("url", ""),
            "page": result.payload.get("page", ""),
            "score": result.score
        })
    
    return retrieved_docs

def format_retrieved_content(docs):
    """Format retrieved documents for context"""
    formatted = []
    for doc in docs:
        formatted.append(f"""
        Source: {doc['title']} ({doc['url']})
        Content: {doc['content']}
        """)
    return "\n\n".join(formatted)

def extract_sources(docs):
    """Extract unique sources from retrieved documents"""
    sources = set()
    for doc in docs:
        source_info = {
            "title": doc['title'],
            "url": doc['url'],
            "relevance_score": doc['score']
        }
        source_key = f"{doc['title']}_{doc['url']}"
        if source_key not in [s['title'] + '_' + s['url'] for s in sources]:
            sources.add(source_info)
    
    return list(sources)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Ingestion endpoint for processing book content
class IngestRequest(BaseModel):
    content: str
    title: str
    url: str
    page: str

@app.post("/api/ingest")
async def ingest_content(request: IngestRequest):
    """Ingest content into the vector database"""
    try:
        # Chunk the content
        chunks = chunk_content(request.content)
        
        # Process each chunk
        points = []
        for i, chunk in enumerate(chunks):
            # Create embedding
            embedding_response = openai.Embedding.create(
                input=chunk,
                model="text-embedding-ada-002"
            )
            embedding = embedding_response['data'][0]['embedding']
            
            # Create Qdrant point
            points.append(models.PointStruct(
                id=f"{request.url}_chunk_{i}",
                vector=embedding,
                payload={
                    "content": chunk,
                    "title": request.title,
                    "url": request.url,
                    "page": request.page,
                    "chunk_id": i
                }
            ))
        
        # Upload to Qdrant
        qdrant_client.upsert(
            collection_name="book_content",
            points=points
        )
        
        return {"message": f"Successfully ingested {len(chunks)} content chunks"}
        
    except Exception as e:
        logger.error(f"Error in ingestion: {e}")
        raise HTTPException(status_code=500, detail="Ingestion failed")

def chunk_content(content: str, chunk_size: int = 512, overlap: int = 50):
    """Split content into overlapping chunks"""
    words = content.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks
```

### Environment Configuration

```bash
# backend/.env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url  # e.g., https://your-cluster.europe-west3-4.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key
NEON_DB_URL=your_neon_postgres_connection_string
```

## Integration with Docusaurus

### Adding the Component to Docusaurus

```js
// src/theme/Layout/index.js
import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import BookChatbot from '@site/src/components/BookChatbot';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import { useLocation } from '@docusaurus/router';

export default function Layout(props) {
  const { siteConfig } = useDocusaurusContext();
  const location = useLocation();
  
  // Show chatbot on all pages except the chatbot page itself if it exists
  const showChatbot = !location.pathname.includes('/chat');
  
  return (
    <>
      <OriginalLayout {...props} />
      {showChatbot && <BookChatbot />}
    </>
  );
}
```

### API Route Setup

```js
// docusaurus.config.js
module.exports = {
  // ... other config
  plugins: [
    // ... other plugins
    [
      '@docusaurus/plugin-client-redirects',
      {
        redirects: [
          {
            to: '/docs/intro', 
            from: '/chat',  // Prevent conflicting routes
          },
        ],
      },
    ],
  ],
  themeConfig: {
    // ... other theme config
  }
};
```

## Deployment Considerations

### Backend Deployment Options

1. **Vercel**:
   - Good for serverless functions
   - Automatic scaling
   - Easy integration with frontend

2. **Render**:
   - Simple container deployment
   - Free tier available
   - Good for FastAPI apps

3. **Self-hosted**:
   - More control over resources
   - Required for custom Qdrant setup
   - More complex setup and maintenance

### Resource Optimization

1. **Caching**: Implement Redis for caching frequent queries
2. **Rate Limiting**: Add rate limiting to control API costs
3. **Embedding Caching**: Cache embeddings to avoid recomputation
4. **Compression**: Compress responses for faster delivery

This RAG chatbot system provides students with an interactive way to engage with the book content, offering contextual answers based on the material while supporting both general questions and specific text selections. The architecture is designed to be cost-effective and scalable, leveraging free-tier services where possible.