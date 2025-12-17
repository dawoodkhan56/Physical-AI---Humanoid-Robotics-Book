import asyncio
import os
from pathlib import Path
import re
from qdrant_client import QdrantClient
from qdrant_client.http import models
import openai
from dotenv import load_dotenv

load_dotenv()

# Initialize clients
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if QDRANT_API_KEY:
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
else:
    qdrant_client = QdrantClient(url=QDRANT_URL)

openai.api_key = OPENAI_API_KEY


def extract_title_from_md(content):
    """Extract title from markdown content"""
    # Look for the first H1 in the markdown
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1)
    return "Untitled"


def chunk_content(content: str, chunk_size: int = 512, overlap: int = 50):
    """Split content into overlapping chunks"""
    paragraphs = content.split('\n\n')
    
    chunks = []
    current_chunk = ""
    current_size = 0
    
    for paragraph in paragraphs:
        # Estimate size (simplified - counting words)
        paragraph_size = len(paragraph.split())
        
        if current_size + paragraph_size > chunk_size and current_chunk:
            # Save the current chunk
            chunks.append(current_chunk.strip())
            
            # Start a new chunk with overlap
            # Use the last few sentences as overlap
            sentences = current_chunk.split('. ')
            if len(sentences) > 1:
                overlap_part = '. '.join(sentences[-min(2, len(sentences)):])
                current_chunk = overlap_part + " " + paragraph
                current_size = len(current_chunk.split())
            else:
                current_chunk = paragraph
                current_size = paragraph_size
        else:
            # Add the paragraph to the current chunk
            if current_chunk:
                current_chunk += "\n\n" + paragraph
            else:
                current_chunk = paragraph
            current_size += paragraph_size
    
    # Add the last chunk if it has content
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    # If no chunks created (content too small), return the entire content as one chunk
    if not chunks:
        chunks = [content]
    
    return chunks


async def process_markdown_file(file_path: Path):
    """Process a single markdown file and add to vector database"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title = extract_title_from_md(content)
    
    # Create URL from file path (relative to docs folder)
    relative_path = file_path.relative_to(Path.cwd())
    url = str(relative_path).replace('\\', '/').replace('website/docs/', '/docs/').replace('.md', '')
    
    # Chunk the content
    chunks = chunk_content(content)
    
    print(f"Processing {file_path.name}: {len(chunks)} chunks")
    
    # Process each chunk
    points = []
    for i, chunk in enumerate(chunks):
        if chunk.strip():  # Only process non-empty chunks
            try:
                # Create embedding
                embedding_response = await openai.Embedding.acreate(
                    input=chunk,
                    model="text-embedding-ada-002"
                )
                embedding = embedding_response['data'][0]['embedding']
                
                # Create Qdrant point
                point_id = f"{url}_chunk_{i}"
                
                points.append(models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "content": chunk,
                        "title": title,
                        "url": url,
                        "page": url.split('/')[-1],
                        "chunk_id": i
                    }
                ))
            except Exception as e:
                print(f"Error processing chunk {i} of {file_path.name}: {e}")
    
    if points:
        # Upload to Qdrant
        qdrant_client.upsert(
            collection_name="book_content",
            points=points
        )
        print(f"Uploaded {len(points)} points for {file_path.name}")
    
    return len(points)


async def main():
    """Main function to process all markdown files"""
    # Find all markdown files in the docs directory
    docs_path = Path("website/docs")
    if not docs_path.exists():
        print(f"Docs directory {docs_path} not found. Looking for files in current directory...")
        md_files = list(Path(".").rglob("*.md"))
    else:
        md_files = list(docs_path.rglob("*.md"))
    
    print(f"Found {len(md_files)} markdown files to process")
    
    total_points = 0
    for i, file_path in enumerate(md_files, 1):
        print(f"\nProcessing file {i}/{len(md_files)}: {file_path}")
        try:
            points_count = await process_markdown_file(file_path)
            total_points += points_count
            print(f"Completed {file_path.name}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"\nIngestion completed! Total points uploaded: {total_points}")


if __name__ == "__main__":
    asyncio.run(main())