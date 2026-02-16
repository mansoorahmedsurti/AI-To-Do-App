---
id: 2
title: phase3-constitution-update
stage: constitution
date_iso: "2026-02-14"
model: Claude Sonnet 4.5
surface: agent
feature: ai-todo-chatbot
branch: main
user: Administrator
command: "/sp.constitution"
labels:
  - constitution
  - phase3
  - ai-todo-chatbot
  - architecture
spec: null
ticket: null
adr: null
pr: null
files_yaml:
  - .specify/memory/constitution.md
tests_yaml: []
---

## Prompt Text
```
I need to plan **Phase 3: AI-Powered Todo Chatbot** of the Hackathon.
We are evolving the Phase 2 (Next.js + FastAPI + Postgres) app into an Agentic System.

**Phase 3 Goals:**
1.  **Conversational Interface:** Users manage todos via natural language (e.g., "Add a meeting tomorrow").
2.  **MCP Server:** A centralized tool server using the **Official MCP Python SDK**.
3.  **OpenAI Agents SDK:** An agent that consumes the MCP tools.
4.  **Stateless API:** A `POST /api/chat` endpoint that persists state in the DB (`conversations` and `messages` tables).

**Architecture Requirements:**
- **Frontend:** OpenAI ChatKit (integrated into our Next.js app).
- **Backend:** FastAPI.
- **Tools:** The MCP Server must expose 5 tools:
    - `add_task(user_id, title, description)`
    - `list_tasks(user_id, status)`
    - `complete_task(user_id, task_id)`
    - `delete_task(user_id, task_id)`
    - `update_task(user_id, task_id, ...)`
- **Database:** New tables for `Conversation` and `Message` (linked to `User`).

**Output Requirements:**
```

## Response Text
Updated the project constitution to version 2.0.0 for Phase 3, incorporating requirements for the AI-Powered Todo Chatbot with MCP Server, OpenAI Agents SDK, and conversational interface.

## Outcome Impact
Created a comprehensive constitution for Phase 3 that defines core principles for the AI-powered todo chatbot, including MCP-server centric architecture, OpenAI agent integration, and stateless API design.

## Files Summary
- .specify/memory/constitution.md: Updated to version 2.0.0 with new principles for AI-Powered Todo Chatbot project

## Tests Summary
None

## Next Prompts
None

## Reflection Note
The constitution now properly defines the architectural requirements for Phase 3, including MCP server, OpenAI agents, and conversational interface requirements.

## Failure Modes Observed
None

## Next Experiment to Improve Prompt Quality
N/A