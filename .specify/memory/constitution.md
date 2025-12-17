<!--
Sync Impact Report:
Version change: 0.1.0 → 1.0.0
List of modified principles: [PRINCIPLE_1_NAME] → Spec-Driven Development, [PRINCIPLE_2_NAME] → AI-Assisted Creation, [PRINCIPLE_3_NAME] → Theme Fidelity, [PRINCIPLE_4_NAME] → Educational Excellence, [PRINCIPLE_5_NAME] → Technical Stack, [PRINCIPLE_6_NAME] → Quality Standards
Added sections: Technical Stack, Quality Standards, Ethical & Practical Guardrails
Removed sections: None
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# Physical AI & Humanoid Robotics Book Constitution

## Core Principles

### Spec-Driven Development
All content creation, code generation, and implementation must follow a strict spec-driven workflow using Spec-Kit Plus slash commands (/sp.specify, /sp.plan, /sp.task, /sp.implement) to ensure structured, traceable, and high-quality outputs.

### AI-Assisted Creation
Leverage advanced AI coding agents (e.g., Claude Code for agentic coding tasks) to generate content, markdown, and code. Prioritize accuracy, educational value, and practical applicability.

### Theme Fidelity
Content must strictly adhere to "Physical AI & Humanoid Robotics: AI Systems in the Physical World – Embodied Intelligence." Emphasize bridging digital AI with physical bodies, using tools like ROS 2, Gazebo, NVIDIA Isaac, and Vision-Language-Action models.

### Educational Excellence
Target advanced students/capstone level. Include clear learning outcomes, hands-on projects, hardware recommendations, and real-world considerations (e.g., sim-to-real transfer, computational demands).

### Technical Stack
Book: Docusaurus v3+ for static site generation, deployed to GitHub Pages.
RAG Chatbot: Backend with FastAPI, OpenAI embeddings/generation (via Agents/ChatKit SDK where applicable), vector storage in Qdrant Cloud Free Tier, metadata storage in Neon Serverless Postgres. Frontend embedded in Docusaurus using custom React components or ChatKit embeds.
Separation: Frontend files in Docusaurus src/components; Backend in separate repo/directory with FastAPI structure.

### Quality Standards
Markdown: Clean, consistent formatting with code blocks, diagrams (via Mermaid), and tables.
Inclusivity: Clear explanations, progressive difficulty, assessments.
RAG Features: Chatbot must support full-book queries and selected-text queries (via client-side highlight capture and context passing).
Version Control: Git-based, with clear history.
Deployment: Free-tier friendly, no high costs.

## Ethical & Practical Guardrails
Focus on simulation-first; highlight hardware costs/latency issues; avoid unsubstantiated claims.

## Governance
This constitution serves as the foundational document governing all aspects of the Physical AI & Humanoid Robotics Book project. All subsequent development, documentation, and implementation activities must align with these principles.

Amendments to this constitution must undergo a formal review process with clear justification for changes. Any conflicts between project practices and constitutional principles must be resolved in favor of the constitution.

Compliance with these principles will be verified during all project reviews and milestone evaluations.

**Version**: 1.0.0 | **Ratified**: 2025-06-13 | **Last Amended**: 2025-12-17
