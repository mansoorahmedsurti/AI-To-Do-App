<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 2.0.0
Modified principles: All principles updated for AI-Powered Todo Chatbot project
Added sections: New architecture requirements section
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/phr-template.prompt.md ⚠ pending
Follow-up TODOs: None
-->

# AI-Powered Todo Chatbot Constitution
<!-- AI-powered conversational todo management system -->

## Core Principles

### I. Conversational Interface First
Every feature must be accessible through natural language interaction; All user interactions designed for chat-based input/output; Natural language processing capabilities integrated throughout the system

### II. MCP-Server Centric Architecture
All tools exposed via standardized MCP protocol; Centralized tool server using Official MCP Python SDK; State management through MCP-conformant interfaces

### III. OpenAI Agent Integration
Leverage OpenAI Agents SDK for intelligent processing; Agent must consume MCP-exposed tools; Conversation flow orchestrated by AI agent with human oversight

### IV. Stateless API Design
All endpoints must be stateless; Conversation state persisted in database via Conversation and Message tables; No session-based state management in API layer

### V. Full Stack Modern Architecture
Frontend: Next.js 16+ with OpenAI ChatKit; Backend: FastAPI with PostgreSQL; MCP Server: Python SDK; Authentication: Better Auth integration maintained

### VI. Tool Standardization
Standardized tool contracts with consistent signatures: user_id, specific parameters; All 5 required tools implemented: add_task, list_tasks, complete_task, delete_task, update_task; Type-safe tool definitions with proper error handling

### VII. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced; Integration tests cover MCP server, agent communication, and frontend-backend flow

## Technology Requirements

### Frontend Stack
- Framework: Next.js 16+ (App Router)
- UI Library: Tailwind CSS
- Chat Interface: OpenAI ChatKit
- Authentication: Better Auth client integration
- State Management: React Context API with proper TypeScript typing

### Backend Stack
- Framework: FastAPI
- ORM: SQLModel with PostgreSQL
- Authentication: Better Auth integration
- MCP Server: Official MCP Python SDK
- OpenAI Integration: OpenAI Agents SDK
- Type Safety: Full TypeScript and Python type hint coverage

### Database Schema
- User table: Existing from Phase 2 with authentication support
- Todo table: Existing from Phase 2 with proper relationships maintained
- Conversation table: Tracks chat sessions with user_id, created_at, updated_at
- Message table: Stores individual messages with role, content, timestamp, linked to conversation
- Proper indexing on foreign keys and frequently queried fields

### API Design
- RESTful design for standard endpoints
- Stateful chat endpoint: POST /api/chat with conversation persistence
- Proper authentication headers maintained across all endpoints
- Consistent error response format with appropriate HTTP status codes

## Development Workflow
- Spec-Driven Development: Write spec first → Generate plan → Create tasks → Implement via Claude Code
- Feature Branch Strategy: Isolate Phase 3 work in dedicated branches
- Integration Points: Ensure seamless integration between existing Phase 2 and new Phase 3 components
- Code Quality: Maintain consistent TypeScript and Python code standards
- Documentation: Inline documentation for MCP tools and API endpoints

## Governance
All changes must comply with this constitution; Amendments require documentation and team approval; Complexity must be justified with clear benefits; Use CLAUDE.md for runtime development guidance; All pull requests must verify constitutional compliance before merging

**Version**: 2.0.0 | **Ratified**: 2026-02-08 | **Last Amended**: 2026-02-08
