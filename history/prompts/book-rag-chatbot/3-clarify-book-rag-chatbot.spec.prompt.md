---
id: 3
title: Clarify Book RAG Chatbot
stage: spec
date: 2025-12-17
surface: agent
model: Qwen
feature: book-rag-chatbot
branch: 001-book-rag-chatbot
user: User
command: /sp.clarify
labels: [clarification, physical-ai, rag, chatbot, education]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-book-rag-chatbot/spec.md
tests:
  - null
---

## Prompt

Project Specification: Physical AI & Humanoid Robotics Interactive Book High-Level Requirements: Create a comprehensive online book titled Physical AI & Humanoid Robotics: Bridging Digital Brains and Physical Bodies. Structure mirrors the provided outline: Quarter Overview, Modules 1-4, Why Physical AI Matters, Learning Outcomes, Weekly Breakdown, Assessments, Hardware Requirements (with options), Architecture Summary. Content: Educational markdown pages with explanations, code snippets (ROS 2 Python, URDF examples, etc.), diagrams, and hands-on exercises. Platform: Docusaurus site for navigation, search, versioning, and dark mode. Deployment: GitHub repository with GitHub Pages enabled for free hosting. Integrated Feature: Embedded RAG chatbot that: Answers questions based on the entire book content. Supports contextual queries on user-selected text (e.g., highlight paragraph → "Ask about this"). Uses retrieval-augmented generation to ground responses in book content only (no hallucinations outside scope). Tech Constraints: Use Spec-Kit Plus for workflow. AI generation via Claude Code or equivalent. RAG Stack: OpenAI for embeddings/LLM, Qdrant for vector search, Neon Postgres for chunk metadata (e.g., page URLs, titles), FastAPI for API. Frontend: Custom Docusaurus plugin/component for chat UI (React-based, with text selection listener). No paid heavy infrastructure; leverage free tiers. Functional Requirements: Book Navigation: Sidebar with modules/weeks. Interactive Elements: Code blocks with copy buttons; Mermaid diagrams for architectures. Chatbot UI: Floating widget or dedicated page; supports streaming responses. Selected-Text Query: JavaScript listener captures window.getSelection(), sends highlighted text + question as context. Ingestion Pipeline: Script to crawl built Docusaurus site, chunk markdown/HTML, embed, store in Qdrant + Postgres. Non-Functional Requirements: Performance: Fast retrieval (<1s), streaming chat. Accessibility: Responsive, keyboard-navigable. Security: API keys server-side only. Maintainability: Separate frontend/backend repos if needed.

## Response snapshot

Successfully completed 5 clarifications for the Physical AI & Humanoid Robotics Interactive Book with RAG Chatbot feature specification:
1. External service availability: Show user-friendly error message and offer to try again later
2. Rate limiting: Limit users to 10 chat queries per hour to prevent abuse and manage costs
3. Observability: Log all user interactions with the chatbot for monitoring and debugging purposes
4. Data retention: Retain user interaction logs for 30 days to support debugging and analytics
5. Content updates: Automatically reprocess content when book pages are updated to keep RAG index current

The spec now includes a Clarifications section and has been updated with 5 new functional requirements (FR-013 through FR-017) addressing operational concerns, data handling, and system behavior.

## Outcome

- ✅ Impact: Added critical operational and data handling requirements to the specification
- 🧪 Tests: null
- 📁 Files: specs/001-book-rag-chatbot/spec.md
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: Specification is now ready for planning with clear operational requirements

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null