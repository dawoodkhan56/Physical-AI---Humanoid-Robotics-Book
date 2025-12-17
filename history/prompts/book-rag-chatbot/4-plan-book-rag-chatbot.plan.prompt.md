---
id: 4
title: Plan Book RAG Chatbot
stage: plan
date: 2025-12-17
surface: agent
model: Qwen
feature: book-rag-chatbot
branch: 001-book-rag-chatbot
user: User
command: /sp.plan
labels: [plan, physical-ai, rag, chatbot, education]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-book-rag-chatbot/plan.md
  - specs/001-book-rag-chatbot/research.md
  - specs/001-book-rag-chatbot/data-model.md
  - specs/001-book-rag-chatbot/quickstart.md
  - specs/001-book-rag-chatbot/contracts/rag-api.yaml
tests:
  - null
---

## Prompt

Implementation Plan

Setup Project Structure
Initialize Docusaurus book repo.
Create separate backend repo for RAG API.

Generate Book Content
Use AI to expand outline into markdown docs.
Organize in /docs folder.

Build & Deploy Static Book
Configure Docusaurus.
Deploy to GitHub Pages.

Build RAG Backend
Ingestion script: Crawl deployed site or local build, chunk content, embed with OpenAI, store in Qdrant + Neon.
FastAPI endpoints: /ingest, /query (with optional selected_text context).

Embed Chatbot Frontend
Custom Docusaurus component: Chat widget using React.
Integrate text selection handler.
Use OpenAI ChatKit for UI if compatible, else custom fetch to backend.

Testing & Refinements
Test queries, selected-text accuracy.
Update ingestion on content changes.


Tech Stack Details

Docusaurus: Standard config with custom theme/components.
Backend: FastAPI + LangChain (for RAG chain) + OpenAI SDK + Qdrant client + asyncpg for Neon.
Vector Strategy: Chunk by headings/paragraphs (~500 tokens), store source URL for citations.

Milestones

Milestone 1: Static book published.
Milestone 2: RAG backend functional.
Milestone 3: Chatbot embedded and contextual.

## Response snapshot

Successfully completed the implementation plan for the Physical AI & Humanoid Robotics Interactive Book with RAG Chatbot. Created the following artifacts:

1. Implementation plan (plan.md) - Complete technical plan with constitution check
2. Research summary (research.md) - Technical decisions and rationale
3. Data model (data-model.md) - Entity definitions and relationships
4. API contracts (contracts/rag-api.yaml) - OpenAPI specification for RAG backend
5. Quickstart guide (quickstart.md) - Developer onboarding instructions
6. Updated agent context for Qwen

The plan includes a dual project architecture (book frontend + RAG backend), proper data models for book content and interactions, comprehensive API contracts for the RAG functionality, and follows all constitutional principles.

## Outcome

- ✅ Impact: Complete technical implementation plan with all required artifacts
- 🧪 Tests: null
- 📁 Files: specs/001-book-rag-chatbot/plan.md, specs/001-book-rag-chatbot/research.md, specs/001-book-rag-chatbot/data-model.md, specs/001-book-rag-chatbot/quickstart.md, specs/001-book-rag-chatbot/contracts/rag-api.yaml
- 🔁 Next prompts: /sp.tasks
- 🧠 Reflection: Plan is comprehensive and ready for task breakdown

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null