"""
Setup and testing script for Neon Postgres and Qdrant vector database.

This script helps verify that your Neon and Qdrant services are properly configured
and accessible before running the full application.
"""

import os
import asyncio
import asyncpg
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get configuration from environment
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
NEON_DB_URL = os.getenv("NEON_DB_URL")

async def test_neon_connection():
    """Test connection to Neon Postgres database"""
    print("Testing Neon Postgres connection...")
    
    if not NEON_DB_URL:
        print("❌ NEON_DB_URL not found in environment variables")
        return False
        
    try:
        # Create a connection pool
        pool = await asyncpg.create_pool(NEON_DB_URL)
        
        # Test the connection with a simple query
        async with pool.acquire() as conn:
            result = await conn.fetchval("SELECT version();")
            print(f"✅ Connected to Neon Postgres: {result.split(',')[0]}")
        
        # Close the pool
        await pool.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to Neon: {e}")
        return False

def test_qdrant_connection():
    """Test connection to Qdrant vector database"""
    print("Testing Qdrant connection...")
    
    if not QDRANT_URL:
        print("❌ QDRANT_URL not found in environment variables")
        return False
    
    if not QDRANT_API_KEY:
        print("❌ QDRANT_API_KEY not found in environment variables")
        return False
    
    try:
        # Initialize Qdrant client
        if QDRANT_API_KEY:
            client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        else:
            client = QdrantClient(url=QDRANT_URL)
        
        # Test connection by trying to list collections
        collections = client.get_collections()
        print(f"✅ Connected to Qdrant. Available collections: {[c.name for c in collections.collections]}")
        
        # Check if our expected collection exists
        collection_name = "book_content"
        collection_exists = any(c.name == collection_name for c in collections.collections)
        
        if collection_exists:
            print(f"✅ Collection '{collection_name}' exists")
            collection_info = client.get_collection(collection_name)
            print(f"   Points: {collection_info.points_count}")
            print(f"   Vector size: {collection_info.config.params.vectors.size}")
        else:
            print(f"ℹ️  Collection '{collection_name}' does not exist (this is normal for first setup)")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to connect to Qdrant: {e}")
        return False

def create_qdrant_collection():
    """Create the required Qdrant collection if it doesn't exist"""
    print("Creating Qdrant collection if needed...")
    
    if not QDRANT_URL or not QDRANT_API_KEY:
        print("❌ QDRANT_URL or QDRANT_API_KEY not found in environment variables")
        return False
    
    try:
        if QDRANT_API_KEY:
            client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        else:
            client = QdrantClient(url=QDRANT_URL)
        
        # Check if collection exists
        collection_name = "book_content"
        collection_exists = False
        try:
            client.get_collection(collection_name)
            collection_exists = True
        except:
            collection_exists = False
        
        if not collection_exists:
            # Create collection with appropriate vector size for OpenAI embeddings (1536)
            client.recreate_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
            )
            print(f"✅ Created Qdrant collection '{collection_name}' with 1536-dim vectors")
        else:
            print(f"✅ Qdrant collection '{collection_name}' already exists")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create Qdrant collection: {e}")
        return False

async def main():
    print("🔍 Testing Cloud Service Configuration")
    print("=" * 50)
    
    # Test Neon connection
    neon_ok = await test_neon_connection()
    
    print()
    
    # Test Qdrant connection
    qdrant_ok = test_qdrant_connection()
    
    print()
    
    # Create Qdrant collection if needed
    collection_ok = create_qdrant_collection()
    
    print()
    print("=" * 50)
    
    if neon_ok and qdrant_ok and collection_ok:
        print("✅ All services are properly configured!")
        print("\nYou can now run the backend application with `python -m uvicorn main:app`")
    else:
        print("❌ Some services are not properly configured.")
        print("\nPlease check your environment variables and service configurations.")
        print("Make sure you have set:")
        print("- OPENAI_API_KEY")
        print("- QDRANT_URL")
        print("- QDRANT_API_KEY")
        print("- NEON_DB_URL (optional, only needed if using metadata storage)")

if __name__ == "__main__":
    asyncio.run(main())