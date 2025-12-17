# Data Model: Physical AI & Humanoid Robotics Interactive Book with RAG Chatbot

## Entities

### Book Page
**Description**: Educational content organized by the book's structure, containing text, code snippets, diagrams, and interactive elements.

**Fields**:
- `id` (string, required): Unique identifier for the page
- `title` (string, required): Title of the page
- `module` (string, required): Module identifier this page belongs to
- `week` (string, optional): Week identifier if applicable
- `url` (string, required): URL path for navigation
- `content` (string, required): The actual markdown/html content
- `metadata` (object, optional): Additional metadata like tags, keywords
- `created_at` (datetime, required): When the page was created
- `updated_at` (datetime, required): When the page was last updated

**Relationships**:
- One-to-many with Content Chunk (a page can be chunked into multiple content chunks)
- Belongs to Module (contained within a module)

### Chat Session
**Description**: Interaction between user and the RAG-powered chatbot, including the conversation history, user queries, and AI responses grounded in book content.

**Fields**:
- `id` (string, required): Unique identifier for the session
- `user_id` (string, optional): Identifier for the user (may be IP or anonymous ID)
- `created_at` (datetime, required): When the session started
- `updated_at` (datetime, required): Last interaction timestamp
- `messages` (array, required): List of message objects in the conversation
- `active` (boolean, required): Whether the session is currently active

**Message Object**:
- `id` (string, required): Unique identifier for the message
- `type` (enum: 'user', 'assistant', required): Type of message
- `content` (string, required): The message content
- `timestamp` (datetime, required): When the message was created
- `context` (object, optional): Context including selected text if applicable

### Content Chunk
**Description**: Segments of book content processed by the RAG system for retrieval and generation, stored with metadata in the vector database and SQL metadata store.

**Fields**:
- `id` (string, required): Unique identifier for the chunk
- `page_id` (string, required): Reference to the source book page
- `content` (string, required): The chunked content (500 tokens or less)
- `embedding` (vector, required): Vector representation for similarity search
- `chunk_index` (integer, required): Position of this chunk within the original page
- `metadata` (object, required): Additional metadata including source URL and title
- `created_at` (datetime, required): When the chunk was created
- `updated_at` (datetime, required): When the chunk was last updated

**Relationships**:
- Belongs to Book Page (originates from a specific page)
- Many-to-one with Book Page

### User Query
**Description**: Questions submitted by users to the chatbot, either general questions or contextual queries related to highlighted text.

**Fields**:
- `id` (string, required): Unique identifier for the query
- `session_id` (string, required): Reference to the chat session
- `content` (string, required): The user's question
- `selected_text` (string, optional): Text that was selected when the query was made
- `timestamp` (datetime, required): When the query was submitted
- `processed` (boolean, required): Whether the query has been processed
- `response_id` (string, optional): Reference to the response if already generated

**Relationships**:
- Belongs to Chat Session (part of a specific session)
- Many-to-one with Chat Session

## Validation Rules

### Book Page Validation
- Title must be between 5 and 200 characters
- URL must follow the format `/module-X/page-title` where X is the module number
- Content must contain at least 100 characters
- Module field must reference an existing module
- Updated_at must be greater than or equal to created_at

### Chat Session Validation
- User_id can be null for anonymous sessions but should be tracked by IP
- Created_at must be in the past
- Session cannot be active for more than 24 hours without interaction
- Messages array must not exceed 50 entries

### Content Chunk Validation
- Content must be between 50 and 500 tokens
- Chunk_index must be 0 or greater
- Page_id must reference an existing book page
- Embedding must be a valid vector representation
- Cannot have overlapping content with other chunks from the same page

### User Query Validation
- Content must be between 5 and 2000 characters
- Session_id must reference an active session
- Selected_text cannot exceed 1000 characters
- Cannot submit more than 10 queries per hour per user (rate limit)

## State Transitions

### Chat Session States
1. `created`: Session initiated
2. `active`: User has started asking questions
3. `inactive`: No user activity for more than 1 hour
4. `completed`: Session ended by user or system due to timeout

### Content Chunk States
1. `pending`: Content identified but not yet processed
2. `processing`: Chunk is being created and embedded
3. `ready`: Chunk is available for retrieval
4. `outdated`: Chunk needs to be regenerated due to source content changes

## Indexes and Performance Considerations

### Book Page
- Index on `module` and `url` for fast navigation
- Full-text search index on `content` for search functionality

### Chat Session
- Index on `user_id` and `updated_at` for session management
- Index on `active` status for cleanup operations

### Content Chunk
- Index on `page_id` for linking to source pages
- Vector index on `embedding` for similarity search
- Index on `updated_at` for content freshness checks

### User Query
- Index on `session_id` and `timestamp` for chronological ordering
- Index on `processed` status for processing queue management