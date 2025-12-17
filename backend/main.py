from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import openai
from google.generativeai import configure, GenerativeModel
import google.generativeai as genai
import asyncpg
from qdrant_client import QdrantClient
from qdrant_client.http import models
import logging
import os
from dotenv import load_dotenv
import asyncio
from contextlib import asynccontextmanager
import tiktoken

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables to hold clients
qdrant_client = None
neon_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    global qdrant_client, neon_pool

    # Initialize Qdrant client
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if qdrant_api_key:
        qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    else:
        qdrant_client = QdrantClient(url=qdrant_url)

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

    # Initialize Neon Postgres connection pool if needed
    neon_db_url = os.getenv("NEON_DB_URL")
    if neon_db_url:
        try:
            neon_pool = await asyncpg.create_pool(neon_db_url)
            logger.info("Connected to Neon Postgres")
        except Exception as e:
            logger.error(f"Failed to connect to Neon Postgres: {e}")
            neon_pool = None

    yield

    # Shutdown
    if neon_pool:
        await neon_pool.close()

app = FastAPI(
    title="Book RAG Chatbot API",
    description="RAG chatbot for Physical AI & Humanoid Robotics book",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class IngestRequest(BaseModel):
    content: str
    title: str
    url: str
    page: str

# Configuration
# Check which AI provider to use
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")  # Can be "openai" or "gemini"

if AI_PROVIDER == "openai":
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")
    openai.api_key = OPENAI_API_KEY
elif AI_PROVIDER == "gemini":
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("Please set the GEMINI_API_KEY environment variable")
    genai.configure(api_key=GEMINI_API_KEY)
    # Initialize the Gemini model
    gemini_model = genai.GenerativeModel('gemini-pro')
else:
    raise ValueError("AI_PROVIDER must be either 'openai' or 'gemini'")

# Set embedding model based on provider
if AI_PROVIDER == "openai":
    EMBEDDING_MODEL = "text-embedding-ada-002"
else:
    EMBEDDING_MODEL = "models/embedding-001"  # Google's embedding model


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Prepare context for the query
        query_context = request.selected_text or request.messages[-1].content

        if not query_context.strip():
            raise HTTPException(status_code=400, detail="Query context is empty")

        # Retrieve relevant content from vector store
        retrieved_docs = await retrieve_relevant_content(query_context)

        # Formulate system prompt with context
        context_str = format_retrieved_content(retrieved_docs)

        if context_str.strip() == "":
            system_prompt = """
            You are an AI assistant for the Physical AI & Humanoid Robotics book.
            Your purpose is to help students understand the content of the book.

            Currently I don't have specific content to reference, but I'm here to help
            with general questions about Physical AI and Humanoid Robotics based on
            my training. Please ask your question and I'll do my best to provide
            accurate and educational information.

            Keep your answers accurate, concise, and educational.
            """
        else:
            system_prompt = f"""
            You are an AI assistant for the Physical AI & Humanoid Robotics book.
            Your purpose is to help students understand the content of the book.

            Use only the following context to answer questions. Do not make up information:
            {context_str}

            If the context doesn't contain relevant information to answer the question,
            say "I don't have enough information from the book content to answer that question.
            Please refer to the relevant chapter."

            Keep your answers accurate, concise, and educational. Reference the source
            material when possible.
            """

        # Get response from the appropriate AI provider
        if AI_PROVIDER == "openai":
            # Prepare messages for OpenAI API
            openai_messages = [
                {"role": "system", "content": system_prompt},
            ]

            # Add conversation history (limit to last 10 messages to manage context)
            conversation_history = request.messages[-10:]  # Limit context
            for msg in conversation_history:
                openai_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            # Get response from OpenAI
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",  # or gpt-4 if available
                messages=openai_messages,
                temperature=0.3,
                max_tokens=1000,
                timeout=30  # Add timeout
            )

            ai_response = response.choices[0].message['content']
        else:  # Gemini provider
            # Combine system prompt and user query for Gemini
            full_query = f"{system_prompt}\n\nUser query: {request.messages[-1].content}"

            # Generate response using Gemini
            response = await gemini_model.generate_content_async(full_query)
            ai_response = response.text

        # Extract sources for response
        sources = extract_sources(retrieved_docs)

        return ChatResponse(
            response=ai_response,
            sources=sources
        )

    except openai.error.APIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=502, detail="External API error")
    except openai.error.AuthenticationError:
        logger.error("OpenAI authentication failed")
        raise HTTPException(status_code=500, detail="Authentication error")
    except openai.error.RateLimitError:
        logger.error("OpenAI rate limit exceeded")
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


async def create_embedding(text: str):
    """Create embedding for text using the selected AI provider"""
    try:
        if AI_PROVIDER == "openai":
            embedding_response = await openai.Embedding.acreate(
                input=text,
                model=EMBEDDING_MODEL,
                timeout=30
            )
            return embedding_response['data'][0]['embedding']
        else:  # Gemini provider - using Google's embedding service
            # Use the Google AI embedding model
            import google.generativeai as genai
            result = genai.embed_content(
                model="models/embedding-001",  # Google's embedding model
                content=[text],
                task_type="RETRIEVAL_QUERY"
            )
            # Return the first embedding from the result
            return result['embedding'][0]
    except Exception as e:
        logger.error(f"Error creating embedding: {e}")
        raise

async def retrieve_relevant_content(query: str, top_k: int = 5):
    """Retrieve relevant content chunks from the vector store"""
    try:
        # Validate input
        if not query or not query.strip():
            logger.warning("Empty query provided to retrieve_relevant_content")
            return []

        # Generate embedding for the query
        query_embedding = await create_embedding(query)

        # Search in Qdrant
        search_results = qdrant_client.search(
            collection_name="book_content",
            query_vector=query_embedding,
            limit=top_k
        )

        # Get the content and metadata for the top results
        retrieved_docs = []
        for result in search_results:
            # Validate payload structure
            payload = result.payload
            retrieved_docs.append({
                "content": payload.get("content", ""),
                "title": payload.get("title", ""),
                "url": payload.get("url", ""),
                "page": payload.get("page", ""),
                "score": result.score
            })

        logger.info(f"Retrieved {len(retrieved_docs)} documents for query: {query[:50]}...")
        return retrieved_docs
    except openai.error.APIError as e:
        logger.error(f"OpenAI API error during retrieval: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error retrieving content: {e}")
        return []


def format_retrieved_content(docs):
    """Format retrieved documents for context"""
    if not docs:
        return ""

    formatted = []
    for doc in docs:
        formatted.append(f"""
        Source: {doc['title']} (URL: {doc['url']})
        Page: {doc['page']}
        Content: {doc['content']}
        Relevance Score: {doc['score']:.3f}
        """)
    return "\n\n".join(formatted)


def extract_sources(docs):
    """Extract unique sources from retrieved documents"""
    if not docs:
        return []

    sources = []
    seen_sources = set()

    for doc in docs:
        # Create a unique identifier for each document
        source_key = f"{doc['title']}_{doc['url']}_{doc['page']}"
        if source_key not in seen_sources:
            source_info = {
                "title": doc['title'],
                "url": doc['url'],
                "page": doc['page'],
                "relevance_score": doc['score']
            }
            sources.append(source_info)
            seen_sources.add(source_key)

    return sources


@app.post("/api/ingest")
async def ingest_content(request: IngestRequest):
    """Ingest content into the vector database"""
    try:
        # Validate input
        if not request.content or len(request.content.strip()) == 0:
            raise HTTPException(status_code=400, detail="Content cannot be empty")

        if not request.title or len(request.title.strip()) == 0:
            raise HTTPException(status_code=400, detail="Title cannot be empty")

        if not request.url or len(request.url.strip()) == 0:
            raise HTTPException(status_code=400, detail="URL cannot be empty")

        # Chunk the content
        chunks = chunk_content(request.content)

        if not chunks:
            logger.warning(f"No content to ingest for URL: {request.url}")
            return {"message": "No content to ingest"}

        # Process each chunk
        points = []
        failed_chunks = 0

        for i, chunk in enumerate(chunks):
            if not chunk.strip():
                continue  # Skip empty chunks

            try:
                # Create embedding using the appropriate provider
                embedding = await create_embedding(chunk)

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
            except openai.error.APIError as e:
                logger.error(f"OpenAI API error for chunk {i} of {request.url}: {e}")
                failed_chunks += 1
                continue  # Continue with other chunks
            except Exception as e:
                logger.error(f"Error processing chunk {i} of {request.url}: {e}")
                failed_chunks += 1
                continue  # Continue with other chunks

        if points:
            # Upload to Qdrant
            qdrant_client.upsert(
                collection_name="book_content",
                points=points
            )

        success_count = len(chunks) - failed_chunks
        message = f"Successfully ingested {success_count} of {len(chunks)} content chunks"
        if failed_chunks > 0:
            message += f" (failed to process {failed_chunks} chunks)"

        logger.info(message)
        return {"message": message, "successful_chunks": success_count, "failed_chunks": failed_chunks}

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except openai.error.AuthenticationError:
        logger.error("OpenAI authentication failed during ingestion")
        raise HTTPException(status_code=500, detail="Authentication error")
    except openai.error.RateLimitError:
        logger.error("OpenAI rate limit exceeded during ingestion")
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    except Exception as e:
        logger.error(f"Unexpected error in ingestion: {e}")
        raise HTTPException(status_code=500, detail="Ingestion failed")


def chunk_content(content: str, chunk_size: int = 500, overlap: int = 50):
    """
    Split content into overlapping chunks using token-aware approach to maintain semantic coherence.
    This helps preserve context and meaning across chunk boundaries for better retrieval.
    """
    if not content.strip():
        return []

    try:
        # Use tiktoken to encode content into tokens for more accurate chunking
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens = encoding.encode(content)

        chunks = []
        start_idx = 0

        while start_idx < len(tokens):
            # Calculate end index
            end_idx = start_idx + chunk_size

            # If we're near the end, take the rest
            if end_idx > len(tokens):
                end_idx = len(tokens)

            # Decode tokens back to text
            chunk_tokens = tokens[start_idx:end_idx]
            chunk_text = encoding.decode(chunk_tokens)

            # Add to chunks if meaningful content
            if chunk_text.strip():
                chunks.append(chunk_text)
            else:
                # If no meaningful content, skip this chunk and advance
                start_idx = end_idx
                continue

            # Move start index forward, with overlap
            start_idx = end_idx - overlap if overlap < end_idx else end_idx

            # Ensure we don't get stuck in an infinite loop
            if start_idx <= 0 or start_idx >= len(tokens):
                break

        # Filter out very small chunks (less than 10 tokens worth of content)
        filtered_chunks = [chunk for chunk in chunks if len(chunk.strip()) > 20]

        return filtered_chunks

    except Exception as e:
        # Fallback to simple splitting if tokenization fails
        logger.warning(f"Tokenization-based chunking failed: {e}. Falling back to simple splitting.")

        # Simple sentence-based splitting
        sentences = content.split('. ')
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Add period back if it was removed in splitting
            if not sentence.endswith('.') and not sentence.endswith('?') and not sentence.endswith('!'):
                sentence += '. '
            else:
                sentence += ' '

            # Check if adding sentence exceeds length
            if len(current_chunk + sentence) > chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += sentence

        # Add the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # Filter very small chunks
        filtered_chunks = [chunk for chunk in chunks if len(chunk.strip()) > 20]
        return filtered_chunks


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Book RAG Chatbot API"}


@app.get("/")
async def root():
    return {"message": "Welcome to the Physical AI & Humanoid Robotics Book RAG API"}

# Import and include advanced endpoints router
try:
    from advanced_endpoints import router as advanced_router
    app.include_router(advanced_router)
    logger.info("Advanced endpoints loaded successfully")
except ImportError as e:
    logger.warning(f"Could not load advanced endpoints: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)