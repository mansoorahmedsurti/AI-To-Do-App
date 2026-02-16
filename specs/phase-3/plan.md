# Phase 3 Plan: AI-Powered Todo Chatbot

## 1. System Architecture

### Overview
The system will implement a conversational interface for managing todos using OpenAI's agents and MCP (Model Context Protocol) server. The architecture follows a layered approach:

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend       │    │   OpenAI Agent   │    │   MCP Server    │
│   (Next.js)     │◄──►│   (FastAPI)      │◄──►│   (OpenAI SDK)   │◄──►│   (Python SDK)  │
│                 │    │                  │    │                  │    │                 │
│ Chat Interface  │    │ POST /api/chat   │    │ Agent Logic      │    │ 5 Todo Tools    │
│ OpenAI ChatKit  │    │ Conversation API │    │ Context Mgmt     │    │ State Handling  │
└─────────────────┘    └──────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Database      │
                       │ (PostgreSQL)    │
                       │                 │
                       │ Users, Todos,   │
                       │ Conversations,  │
                       │ Messages        │
                       └─────────────────┘
```

### Component Flow
1. **Frontend**: Next.js app with OpenAI ChatKit for natural language interaction
2. **Backend**: FastAPI server exposing `/api/chat` endpoint that handles conversation state
3. **Agent**: OpenAI Agent SDK processes natural language and calls MCP tools
4. **MCP Server**: Python SDK-based server exposing 5 todo management tools
5. **Database**: PostgreSQL storing users, todos, conversations, and messages

## 2. Database Schema Changes

### New Models (SQLModel)

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid

# Conversation Model
class Conversation(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
    user: "User" = Relationship(back_populates="conversations")

# Message Model
class Message(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id")
    role: str  # "user", "assistant", "tool"
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_calls: Optional[str] = None  # JSON string of tool calls
    tool_responses: Optional[str] = None  # JSON string of tool responses
    
    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")

# Extend existing User model to include conversations
class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    todos: List[Todo] = Relationship(back_populates="user")
    conversations: List[Conversation] = Relationship(back_populates="user")
```

### Migration Strategy
1. Add `conversations` and `messages` tables to existing PostgreSQL schema
2. Maintain backward compatibility with existing `users` and `todos` tables
3. Use Alembic for database migrations

## 3. API Endpoint Definition

### POST /api/chat
Handles conversational requests and manages conversation state.

#### Request Body
```json
{
  "message": "Add a meeting with John tomorrow at 10am",
  "conversation_id": "optional-conversation-id", // null for new conversation
  "user_id": "authenticated-user-id"
}
```

#### Response
```json
{
  "conversation_id": "generated-or-existing-conversation-id",
  "response": "I've added a meeting with John for tomorrow at 10am.",
  "timestamp": "2026-02-08T10:30:00Z",
  "status": "success"
}
```

#### Implementation Details
- Validates user authentication via JWT
- Creates new conversation if none provided
- Stores user message in database
- Calls OpenAI Agent with conversation context
- Stores agent response in database
- Returns response to frontend

### Additional Endpoints
- `GET /api/conversations` - List user's conversations
- `GET /api/conversations/{id}` - Get specific conversation
- `DELETE /api/conversations/{id}` - Delete conversation

## 4. MCP Tool Definitions

### Tool 1: add_task
**Purpose**: Add a new task to the user's todo list
**Input**:
```json
{
  "user_id": "uuid-string",
  "title": "string",
  "description": "string",
  "due_date": "optional ISO date string",
  "priority": "optional enum (low, medium, high)"
}
```
**Output**:
```json
{
  "success": true,
  "task_id": "uuid-string",
  "message": "Task added successfully"
}
```

### Tool 2: list_tasks
**Purpose**: Retrieve user's tasks with optional filtering
**Input**:
```json
{
  "user_id": "uuid-string",
  "status": "optional enum (pending, completed)",
  "limit": "optional integer",
  "offset": "optional integer"
}
```
**Output**:
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "string",
      "description": "string",
      "status": "enum (pending, completed)",
      "priority": "enum (low, medium, high)",
      "created_at": "ISO date string",
      "due_date": "optional ISO date string"
    }
  ],
  "total_count": "integer"
}
```

### Tool 3: complete_task
**Purpose**: Mark a task as completed
**Input**:
```json
{
  "user_id": "uuid-string",
  "task_id": "uuid-string"
}
```
**Output**:
```json
{
  "success": true,
  "message": "Task marked as completed"
}
```

### Tool 4: delete_task
**Purpose**: Remove a task from the user's list
**Input**:
```json
{
  "user_id": "uuid-string",
  "task_id": "uuid-string"
}
```
**Output**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

### Tool 5: update_task
**Purpose**: Modify an existing task
**Input**:
```json
{
  "user_id": "uuid-string",
  "task_id": "uuid-string",
  "title": "optional string",
  "description": "optional string",
  "status": "optional enum (pending, completed)",
  "priority": "optional enum (low, medium, high)",
  "due_date": "optional ISO date string"
}
```
**Output**:
```json
{
  "success": true,
  "message": "Task updated successfully"
}
```

## 5. Implementation Approach

### Phase 1: Infrastructure Setup
1. Set up MCP server with Python SDK
2. Implement 5 core todo tools
3. Create database models for conversations/messages

### Phase 2: Agent Integration
1. Integrate OpenAI Agent SDK
2. Configure agent to use MCP tools
3. Implement conversation context management

### Phase 3: Backend API
1. Create `/api/chat` endpoint
2. Implement conversation state management
3. Add conversation history endpoints

### Phase 4: Frontend Integration
1. Integrate OpenAI ChatKit
2. Connect to backend chat API
3. Implement conversation history UI

## 6. Security Considerations
- All MCP tool calls must validate user identity
- Conversation data must be isolated by user_id
- Rate limiting on chat endpoints
- Input sanitization for natural language processing