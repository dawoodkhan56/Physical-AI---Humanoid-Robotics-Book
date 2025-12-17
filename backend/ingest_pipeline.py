"""
Enhanced ingestion pipeline for processing book content and storing it in Qdrant vector database.
This script extracts content from all markdown files in the Docusaurus docs directory,
chunks them, generates embeddings using OpenAI, and stores them in Qdrant.
"""
import asyncio
import os
import sys
from pathlib import Path
import re
from typing import List, Tuple
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Import libraries (will fail gracefully if not available)
try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    import openai
    import tiktoken
except ImportError as e:
    logger.error(f"Missing required packages: {e}")
    logger.error("Please install the requirements: pip install -r requirements.txt")
    sys.exit(1)

# Initialize clients
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY is not set in environment variables")
    sys.exit(1)

if not QDRANT_URL:
    logger.error("QDRANT_URL is not set in environment variables")
    sys.exit(1)

openai.api_key = OPENAI_API_KEY

if QDRANT_API_KEY:
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY, timeout=60)
else:
    qdrant_client = QdrantClient(url=QDRANT_URL, timeout=60)


def extract_title_from_md(content: str) -> str:
    """Extract title from markdown content"""
    # Look for the first H1 in the markdown
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Untitled"


def chunk_content(content: str, max_tokens: int = 500, overlap_tokens: int = 50) -> List[str]:
    """
    Split content into overlapping chunks based on tokens rather than words for better semantic coherence.
    """
    if not content.strip():
        return []
    
    # Use tiktoken to encode content into tokens
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(content)
    
    chunks = []
    start_idx = 0
    
    while start_idx < len(tokens):
        # Calculate end index
        end_idx = start_idx + max_tokens
        
        # If we're near the end, take the rest
        if end_idx > len(tokens):
            end_idx = len(tokens)
        
        # Decode tokens back to text
        chunk_tokens = tokens[start_idx:end_idx]
        chunk_text = encoding.decode(chunk_tokens)
        
        # Add to chunks if not empty
        if chunk_text.strip():
            chunks.append(chunk_text)
        
        # Move start index forward, with overlap
        start_idx = end_idx - overlap_tokens if overlap_tokens < end_idx else end_idx
        
        # Ensure we don't get stuck in an infinite loop
        if start_idx <= start_idx - max_tokens + overlap_tokens:
            break
    
    return chunks


async def create_embedding(text: str) -> List[float]:
    """Create embedding for text using OpenAI API with retry logic"""
    max_retries = 3
    retry_delay = 1  # seconds
    
    for attempt in range(max_retries):
        try:
            response = await openai.Embedding.acreate(
                input=text,
                model="text-embedding-ada-002"
            )
            return response['data'][0]['embedding']
        except Exception as e:
            logger.warning(f"Embedding attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise e
            # Wait before retry
            await asyncio.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
    
    raise Exception("Failed to create embedding after retries")


async def process_markdown_file(file_path: Path, base_path: Path) -> int:
    """Process a single markdown file and add to vector database"""
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Extract title
        title = extract_title_from_md(content)
        if not title or title.lower() == "untitled":
            title = file_path.stem.replace('-', ' ').replace('_', ' ').title()

        # Create URL from file path relative to docs
        relative_path = file_path.relative_to(base_path)
        url = f"/docs/{str(relative_path).replace(file_path.suffix, '')}"
        
        # Clean up URL to ensure proper format
        url = url.replace('\\', '/').replace('//', '/')

        # Extract page name from URL
        page = url.split('/')[-1] or url.split('/')[-2] or file_path.stem

        # Chunk the content
        chunks = chunk_content(content)
        
        if not chunks:
            logger.warning(f"No content to process in {file_path}")
            return 0

        logger.info(f"Processing {file_path.name}: {len(chunks)} chunks")
        
        # Process each chunk
        points = []
        successful_chunks = 0
        
        for i, chunk in enumerate(chunks):
            if not chunk.strip():
                continue
                
            try:
                # Create embedding
                embedding = await create_embedding(chunk)
                
                # Create Qdrant point
                point_id = f"{file_path.name}_chunk_{i}"
                
                points.append(models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "content": chunk,
                        "title": title,
                        "url": url,
                        "page": page,
                        "chunk_id": i,
                        "file_path": str(file_path)
                    }
                ))
                
                successful_chunks += 1
                
                # Print progress every 10 chunks
                if (i + 1) % 10 == 0:
                    logger.info(f"Processed {i + 1}/{len(chunks)} chunks for {file_path.name}")
                    
            except Exception as e:
                logger.error(f"Error processing chunk {i} of {file_path.name}: {e}")
                continue  # Continue with next chunk even if one fails

        if points:
            # Upload to Qdrant
            try:
                qdrant_client.upsert(
                    collection_name="book_content",
                    points=points
                )
                logger.info(f"Uploaded {len(points)} points for {file_path.name}")
            except Exception as e:
                logger.error(f"Failed to upload points for {file_path.name}: {e}")
                return 0

        return successful_chunks
        
    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        return 0


async def create_collection():
    """Create the Qdrant collection if it doesn't exist"""
    try:
        # Check if collection exists
        collections = qdrant_client.get_collections()
        collection_exists = any(c.name == "book_content" for c in collections.collections)
        
        if not collection_exists:
            # Create collection with appropriate vector size for OpenAI embeddings (1536)
            qdrant_client.recreate_collection(
                collection_name="book_content",
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )
            logger.info("Created Qdrant collection 'book_content'")
        else:
            logger.info("Qdrant collection 'book_content' already exists")
            
        return True
    except Exception as e:
        logger.error(f"Failed to create Qdrant collection: {e}")
        return False


async def main():
    """Main function to process all markdown files and ingest content"""
    # Verify connection to Qdrant
    try:
        qdrant_client.get_collections()
        logger.info("Connected to Qdrant successfully")
    except Exception as e:
        logger.error(f"Failed to connect to Qdrant: {e}")
        return
    
    # Create collection if needed
    if not await create_collection():
        logger.error("Failed to create Qdrant collection")
        return
    
    # Define the path to look for markdown files
    docs_path = Path("website/docs")
    if not docs_path.exists():
        logger.error(f"Docs directory {docs_path} does not exist")
        # Try alternative paths
        possible_paths = [Path("docs"), Path("website"), Path(".")]
        for path in possible_paths:
            if path.exists() and any(path.glob("*.md")):
                docs_path = path
                logger.info(f"Using alternative docs path: {docs_path}")
                break
        else:
            logger.error("Could not find a directory with markdown files")
            return

    # Find all markdown files in the docs directory
    md_files = list(docs_path.rglob("*.md"))
    
    if not md_files:
        logger.error(f"No markdown files found in {docs_path}")
        # Try to find markdown files recursively from current directory
        md_files = list(Path(".").rglob("*.md"))
        logger.info(f"Found {len(md_files)} markdown files in total project")
    
    logger.info(f"Found {len(md_files)} markdown files to process")

    # Process files
    total_chunks = 0
    processed_files = 0
    failed_files = 0
    
    for i, file_path in enumerate(md_files, 1):
        try:
            logger.info(f"\nProcessing file {i}/{len(md_files)}: {file_path}")
            chunks_count = await process_markdown_file(file_path, docs_path)
            if chunks_count > 0:
                total_chunks += chunks_count
                processed_files += 1
            else:
                failed_files += 1
            logger.info(f"Progress: {i}/{len(md_files)} files processed")
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            failed_files += 1

    # Final summary
    logger.info("="*50)
    logger.info("INGESTION COMPLETED!")
    logger.info(f"Total files processed: {processed_files}")
    logger.info(f"Failed files: {failed_files}")
    logger.info(f"Total chunks ingested: {total_chunks}")
    
    # Verify ingestion by checking collection info
    try:
        collection_info = qdrant_client.get_collection("book_content")
        logger.info(f"Final collection size: {collection_info.points_count} points")
    except Exception as e:
        logger.error(f"Could not get collection info: {e}")


if __name__ == "__main__":
    # Run the asyncio event loop
    asyncio.run(main())