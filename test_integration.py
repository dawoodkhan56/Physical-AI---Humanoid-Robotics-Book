"""
Integration test script for the RAG chatbot system.
This script tests the full integration between the Docusaurus frontend and FastAPI backend.
"""
import asyncio
import aiohttp
import time
import sys
from pathlib import Path

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "backend"))

async def test_backend_connection():
    """Test if the backend API is running and accessible"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:8000/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Backend is running: {data}")
                    return True
                else:
                    print(f"❌ Backend health check failed with status {response.status}")
                    return False
    except aiohttp.ClientConnectorError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False

async def test_chat_endpoint():
    """Test the chat endpoint with a simple query"""
    try:
        async with aiohttp.ClientSession() as session:
            # Prepare a simple test request
            test_payload = {
                "messages": [
                    {"role": "user", "content": "What is Physical AI?"}
                ],
                "selected_text": "",
                "context": {
                    "current_page": "/docs/intro",
                    "current_section": "Introduction"
                }
            }
            
            async with session.post("http://localhost:8000/api/chat", json=test_payload) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Chat endpoint working. Response preview: {data['response'][:100]}...")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Chat endpoint failed with status {response.status}: {error_text}")
                    return False
    except Exception as e:
        print(f"❌ Error testing chat endpoint: {e}")
        return False

async def test_search_endpoint():
    """Test the search endpoint"""
    try:
        async with aiohttp.ClientSession() as session:
            # Prepare a test search request
            test_payload = {
                "text": "embodied intelligence",
                "top_k": 3
            }
            
            async with session.post("http://localhost:8000/api/search", json=test_payload) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Search endpoint working. Found {len(data['results'])} results")
                    if data['results']:
                        print(f"   First result preview: {data['results'][0]['content'][:100]}...")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Search endpoint failed with status {response.status}: {error_text}")
                    return False
    except Exception as e:
        print(f"❌ Error testing search endpoint: {e}")
        return False

async def test_ingestion_endpoint():
    """Test the ingestion endpoint (if needed)"""
    try:
        async with aiohttp.ClientSession() as session:
            # Prepare a test ingestion request
            test_payload = {
                "content": "Physical AI refers to artificial intelligence systems that function in reality and comprehend physical laws.",
                "title": "Test Content",
                "url": "/test/content",
                "page": "test"
            }
            
            async with session.post("http://localhost:8000/api/ingest", json=test_payload) as response:
                if response.status in [200, 201]:
                    data = await response.json()
                    print(f"✅ Ingestion endpoint working: {data}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ Ingestion endpoint failed with status {response.status}: {error_text}")
                    return False
    except Exception as e:
        print(f"❌ Error testing ingestion endpoint: {e}")
        return False

async def run_integration_tests():
    """Run all integration tests"""
    print("🔍 Running RAG Chatbot Integration Tests")
    print("="*60)
    
    start_time = time.time()
    
    # Test 1: Backend connection
    print("\n1. Testing backend connection...")
    backend_ok = await test_backend_connection()
    
    if not backend_ok:
        print("\n❌ Backend is not accessible. Please start the backend server first:")
        print("   cd backend")
        print("   python -m uvicorn main:app --reload")
        return False
    
    # Test 2: Chat endpoint
    print("\n2. Testing chat endpoint...")
    chat_ok = await test_chat_endpoint()
    
    # Test 3: Search endpoint
    print("\n3. Testing search endpoint...")
    search_ok = await test_search_endpoint()
    
    # Test 4: Ingestion endpoint
    print("\n4. Testing ingestion endpoint...")
    ingestion_ok = await test_ingestion_endpoint()
    
    total_time = time.time() - start_time
    
    print("\n" + "="*60)
    print("📊 INTEGRATION TEST RESULTS")
    print("="*60)
    print(f"Backend connection: {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"Chat endpoint: {'✅ PASS' if chat_ok else '❌ FAIL'}")
    print(f"Search endpoint: {'✅ PASS' if search_ok else '❌ FAIL'}")
    print(f"Ingestion endpoint: {'✅ PASS' if ingestion_ok else '❌ FAIL'}")
    print(f"Total execution time: {total_time:.2f}s")
    
    all_passed = backend_ok and chat_ok and search_ok and ingestion_ok
    print(f"\nOverall result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    if all_passed:
        print("\n🎉 The RAG chatbot system is properly integrated!")
        print("\nTo test the full functionality:")
        print("1. Make sure your backend is running on http://localhost:8000")
        print("2. Start your Docusaurus site with: npm run start")
        print("3. Visit any page and use the chatbot in the bottom-right corner")
        print("4. Try asking questions about the book content")
        
    return all_passed

if __name__ == "__main__":
    success = asyncio.run(run_integration_tests())
    sys.exit(0 if success else 1)