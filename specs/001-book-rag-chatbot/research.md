# Research Summary: Physical AI & Humanoid Robotics Interactive Book with RAG Chatbot

## Technical Decisions & Rationale

### 1. Dual Project Architecture: Book Frontend + RAG Backend
**Decision**: Implement as two separate projects - a Docusaurus-based book frontend and a FastAPI-based RAG backend.

**Rationale**: This separation aligns with the stated requirement for "Separate frontend/backend repos if needed" from the original specification. It provides several benefits:
- Independent deployment cycles for content updates vs. backend improvements
- Better security isolation (API keys kept in backend only)
- Scalability - backend can be scaled independently of static content
- Clear separation of concerns

**Alternatives considered**:
- Single unified project: Would mix static content with dynamic backend logic
- Client-side RAG: Would expose API keys and be inefficient

### 2. Vector Database Strategy
**Decision**: Use Qdrant for vector storage and Neon Postgres for metadata storage.

**Rationale**: This combination matches the requirement in the original specification and constitution:
- Qdrant Cloud Free Tier: Specifically mentioned in constitution for vector storage
- Neon Serverless Postgres: For metadata storage as specified
- Both support free-tier usage which is required per constraints

**Alternatives considered**:
- Pinecone: More expensive, not mentioned in constitution
- Chroma: Self-hosted, more complex setup
- Weaviate: Additional learning curve, not constitutionally specified

### 3. Frontend Text Selection Implementation
**Decision**: Implement text selection handler using JavaScript's `window.getSelection()` API combined with a custom "Ask about this" button that appears on text selection.

**Rationale**: This approach is lightweight, works across browsers, and provides the required functionality of allowing users to ask questions about selected text without disrupting their reading flow. It's simpler than complex annotation systems while still meeting requirements.

**Alternatives considered**:
- Right-click context menu: Might conflict with browser context menus
- Always-visible floating button: Would take more UI space
- Double-click to select: Less discoverable than visible button

### 4. Content Chunking Strategy
**Decision**: Use a combination of semantic chunking by headings/paragraphs and token-based chunking (maximum ~500 tokens per chunk).

**Rationale**: This approach balances retrieval accuracy with context preservation:
- Semantic boundaries help maintain conceptual coherence
- Token limit prevents chunks from becoming too large
- Allows for proper citations to specific parts of the book
- Aligns with best practices for RAG systems

**Alternatives considered**:
- Fixed character count: Would break semantically meaningful sections
- Complete pages as chunks: Would be too large and imprecise
- Sentence-level chunks: Would be too granular, potentially losing context

### 5. Rate Limiting Implementation
**Decision**: Implement rate limiting at the API level using a sliding window approach with 10 queries per hour per user based on IP address with potential future user account identification.

**Rationale**: This directly implements the requirement from the clarifications phase (limit users to 10 chat queries per hour to prevent abuse and manage costs). The IP-based approach provides basic protection without requiring user accounts, though future enhancement could include actual user accounts for more precise tracking.

**Alternatives considered**:
- No rate limiting: Would violate the clarifications agreement
- Per-session limiting: Would be less effective against abuse
- Time-based blocking: Would be less user-friendly than just limiting frequency

### 6. Error Handling Strategy
**Decision**: Implement graceful degradation when external AI services are unavailable, showing user-friendly error messages and offering to try again later.

**Rationale**: This directly addresses the requirement from clarifications: "Show user-friendly error message and offer to try again later". Ensures good user experience even during service disruptions while being transparent about what's happening.

**Alternatives considered**:
- Silent failure: Would confuse users
- Immediate retry: Could cause performance issues
- Complete fallback mode: Not feasible without AI service

### 7. Content Update Strategy
**Decision**: Implement automatic reprocessing of content when book pages are updated to keep the RAG index current.

**Rationale**: This satisfies the requirement from clarifications: "Automatically reprocess content when book pages are updated to keep RAG index current". This ensures the chatbot always has access to the most recent content without manual intervention.

**Alternatives considered**:
- Manual reprocessing: Would require manual intervention each time
- Scheduled reprocessing: Might have outdated information between schedules
- No updates: Would cause outdated responses over time

### 8. Logging and Observability
**Decision**: Log all user interactions with the chatbot as required by the clarifications agreement.

**Rationale**: This directly implements the requirement: "Log all user interactions with the chatbot for monitoring and debugging purposes". This allows for operational readiness, debugging, and analytics while meeting the retention requirement of 30 days.

**Alternatives considered**:
- No logging: Would violate the clarifications agreement
- Limited logging: Would not meet monitoring requirements
- Full system logging: Would include unnecessary data

### 9. Data Retention Policy
**Decision**: Implement 30-day retention for user interaction logs to support debugging and analytics.

**Rationale**: This directly implements the requirement from clarifications: "Retain user interaction logs for 30 days to support debugging and analytics". This provides sufficient time for analysis while respecting privacy concerns.

**Alternatives considered**:
- Longer retention: Would hold data longer than necessary
- Shorter retention: Would limit debugging capabilities
- Indefinite retention: Would not respect privacy expectations

### 10. Docusaurus Integration Strategy
**Decision**: Create a custom Docusaurus React component for the chatbot widget that communicates with the backend API.

**Rationale**: This allows tight integration with the Docusaurus-based book while keeping the RAG logic separate in the backend. The component can be embedded into Docusaurus pages and will handle the UI aspects while making API calls to the backend for RAG processing.

**Alternatives considered**:
- External iframe: Would be harder to integrate with text selection
- Separate application: Would require navigation away from book content
- Server-side rendering: Would be more complex and less interactive