## Setting up Neon and Qdrant for the RAG Chatbot

This guide will walk you through setting up the required cloud services for the RAG (Retrieval-Augmented Generation) chatbot functionality.

### 1. Setting up Neon Serverless Postgres

Neon is a serverless PostgreSQL platform that provides instant branching and other powerful features.

#### Step 1: Create a Neon Account
1. Go to https://neon.tech/
2. Sign up for a free account using your email or GitHub
3. Verify your email address

#### Step 2: Create a Project
1. In the Neon dashboard, click "New Project"
2. Choose a project name (e.g., "physical-ai-book")
3. Select your preferred region
4. Keep the default settings and click "Create Project"

#### Step 3: Get Connection Details
1. After the project is created, go to the "Connection Details" section
2. Note down the connection string, which will look like:
   `postgresql://username:password@ep-xxxx.us-east-1.aws.neon.tech/neondb?sslmode=require`
3. Save this connection string for later use

#### Step 4: Create Required Tables
Once your application connects to Neon, it will create the necessary tables automatically. The main table will store metadata about document chunks such as:
- content_id
- title
- url
- page
- chunk_id
- embedding_id
- created_at

### 2. Setting up Qdrant Cloud

Qdrant is a vector similarity search engine that will store the embeddings of our book content.

#### Step 1: Create a Qdrant Account
1. Go to https://qdrant.tech/
2. For cloud version, visit https://cloud.qdrant.io/
3. Sign up for a free account

#### Step 2: Create a Cluster
1. In the Qdrant Cloud dashboard, click "Create Cluster"
2. Choose the "Free" plan (which provides 100MB storage, sufficient for initial setup)
3. Select your preferred region
4. Give your cluster a name (e.g., "physical-ai-book")
5. Click "Create"

#### Step 3: Get Connection Details
1. Once the cluster is created, you'll see its details
2. Note down the URL (e.g., https://your-cluster.europe-west3-4.gcp.cloud.qdrant.io:6333)
3. In the "API Keys" section, create a new API key and copy it
4. Save both the URL and API key for later use

#### Step 4: Configure Collection
In your application code, you'll create a collection called "book_content" with:
- Vector size: 1536 (to match OpenAI embeddings)
- Distance function: Cosine similarity

### 3. Environment Configuration

Create a `.env` file in the backend directory with the following information:

```env
OPENAI_API_KEY=your_openai_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
NEON_DB_URL=your_neon_postgres_connection_string_here
```

### 4. Important Security Notes

- Never commit the `.env` file to version control
- Regenerate API keys if they are exposed
- Use different keys for development and production
- Regularly rotate your API keys

Once these services are set up, you can run the ingestion script to populate your vector database with the book content.