# Phase 3: AI-Powered Todo Chatbot Specification

## Overview
This document specifies the requirements for implementing a Natural Language Interface for the existing to-do application. The application will allow users to manage their tasks through natural language interactions using OpenAI's agents and MCP (Model Context Protocol) tools.

## Mission
Create a conversational interface that allows users to manage their to-dos through natural language while maintaining all existing functionality and integrating seamlessly with the current authentication system.

## User Stories

### Story 1: As a user, I want to add tasks using natural language
- So that I can quickly create new todos without navigating through forms
- Given I am logged in to the application
- When I type "Add a task to buy groceries"
- Then the system should parse the intent and create a new todo with title "buy groceries"

### Story 2: As a user, I want to list my tasks using natural language
- So that I can quickly check what I need to do
- Given I am logged in to the application
- When I type "What do I have to do?"
- Then the system should return all pending tasks in a readable format

### Story 3: As a user, I want to complete tasks using natural language
- So that I can mark tasks as done without clicking checkboxes
- Given I am logged in to the application
- When I type "I'm done with the meeting"
- Then the system should identify the task and mark it as completed

### Story 4: As a user, I want to receive confirmation for my actions
- So that I know the system understood and processed my request
- Given I have issued a command to the chatbot
- When the system processes my request
- Then it should respond with a confirmation message like "Okay, I've added 'Buy Milk' to your list"

### Story 5: As a user, I want to receive helpful error messages
- So that I understand when something goes wrong
- Given I have issued an invalid command or referenced a non-existent task
- When the system encounters an error
- Then it should respond with a helpful message like "I couldn't find task #3"

## Functional Requirements

### 1. Intent Detection
- The system must detect user intent from natural language input
- Supported intents: ADD_TASK, LIST_TASKS, COMPLETE_TASK, DELETE_TASK, UPDATE_TASK
- The system must extract relevant parameters from the input (task titles, descriptions, etc.)

### 2. Action Confirmation
- The system must always confirm successful actions with clear messages
- Confirmation messages must include relevant details about the action taken
- The system must use natural language that feels conversational

### 3. Error Handling
- The system must gracefully handle invalid commands
- The system must provide helpful error messages when tasks aren't found
- The system must handle cases where natural language parsing fails

### 4. Natural Language Commands
- "Add a task to buy groceries" -> Calls `add_task` with title "buy groceries"
- "Add a high priority task to call mom" -> Calls `add_task` with title "call mom" and priority "high"
- "What do I have to do?" -> Calls `list_tasks(status='pending')`
- "Show me completed tasks" -> Calls `list_tasks(status='completed')`
- "I'm done with the meeting" -> Calls `complete_task` for the identified task
- "Remove the doctor appointment" -> Calls `delete_task` for the identified task
- "Update the project deadline to Friday" -> Calls `update_task` for the identified task

### 5. State Management
- The server must be stateless for each request
- Every request must load conversation history from PostgreSQL
- The agent must process the current input with historical context
- The new response must be saved to the database after processing

## Technical Requirements

### 1. Agent Behavior
- Must detect intent (Add vs Delete vs Query vs Update vs Complete)
- Must always confirm actions with natural language responses
- Must handle errors gracefully with user-friendly messages
- Must maintain conversation context across multiple exchanges

### 2. Database Requirements
- Conversation history must be loaded for each request
- New messages must be saved after each exchange
- User isolation must be maintained through user_id
- Efficient querying for conversation history

### 3. API Requirements
- POST /api/chat endpoint must be stateless
- Request must include user_id and conversation_id
- Response must include updated conversation context
- Proper error handling and status codes

## Acceptance Criteria

### AC-001: Intent Detection
- [ ] Given a user inputs "Add a task to buy groceries", when the system processes the input, then it should correctly identify the ADD_TASK intent and extract "buy groceries" as the task title

### AC-002: Action Confirmation
- [ ] Given a user adds a task via natural language, when the system processes the request, then it should respond with a confirmation message like "Okay, I've added 'Buy Milk' to your list"

### AC-003: List Tasks Functionality
- [ ] Given a user inputs "What do I have to do?", when the system processes the input, then it should return all pending tasks in a readable format

### AC-004: Complete Task Functionality
- [ ] Given a user inputs "I'm done with the meeting", when the system processes the input, then it should identify the correct task and mark it as completed

### AC-005: Error Handling
- [ ] Given a user inputs "Mark task #999 as complete", when the system processes the input, then it should respond with "I couldn't find task #999"

### AC-006: State Management
- [ ] Given a user sends a chat message, when the system processes the request, then it should load conversation history from the database, process the input, and save the new message to the database

### AC-007: Authentication
- [ ] Given an unauthenticated user tries to access the chat endpoint, when they make a request, then the system should return a 401 Unauthorized response

### AC-008: Natural Language Processing
- [ ] Given a user inputs a complex command like "Add a high priority task to schedule a meeting with the team for tomorrow", when the system processes the input, then it should create a task with title "schedule a meeting with the team", priority "high", and due date "tomorrow"

## Example Dialogues

### Dialogue 1: Adding Tasks
```
User: "Add a task to buy groceries"
Assistant: "Okay, I've added 'buy groceries' to your to-do list."
```

### Dialogue 2: Listing Tasks
```
User: "What do I have to do?"
Assistant: "Here are your pending tasks:
1. Buy groceries
2. Call mom
3. Finish project report"
```

### Dialogue 3: Completing Tasks
```
User: "I'm done with the meeting"
Assistant: "Okay, I've marked 'Team meeting' as completed."
```

### Dialogue 4: Error Handling
```
User: "Mark task #999 as complete"
Assistant: "I couldn't find task #999. Could you check the task number and try again?"
```

### Dialogue 5: Complex Commands
```
User: "Add a high priority task to schedule a meeting with the team for tomorrow"
Assistant: "Okay, I've added 'Schedule a meeting with the team for tomorrow' to your to-do list with high priority."
```

### Dialogue 6: Updating Tasks
```
User: "Change the deadline for the project report to Friday"
Assistant: "Okay, I've updated the due date for 'Project report' to Friday."
```

### Dialogue 7: Deleting Tasks
```
User: "Remove the reminder to call the dentist"
Assistant: "Okay, I've removed 'Call the dentist' from your to-do list."
```

### Dialogue 8: Mixed Conversation
```
User: "Add a task to water the plants"
Assistant: "Okay, I've added 'Water the plants' to your to-do list."

User: "What do I have to do?"
Assistant: "Here are your pending tasks:
1. Buy groceries
2. Water the plants
3. Call mom"

User: "I'm done with watering the plants"
Assistant: "Okay, I've marked 'Water the plants' as completed."
```

## Non-Functional Requirements

### Performance
- Chat response time < 3 seconds for 95% of requests
- Support for 100+ concurrent conversations
- Efficient database queries for conversation history

### Security
- All MCP tool calls must validate user identity
- Conversation data must be isolated by user
- Input sanitization for natural language processing
- Protection against prompt injection attacks

### Reliability
- 99.9% uptime for chat functionality
- Graceful error handling when AI services are unavailable
- Data backup and recovery for conversation history

## Constraints
- Must maintain backward compatibility with existing features
- MCP tools must use the official Python SDK
- All user data must remain properly isolated
- Natural language processing must be reliable and accurate
- Server must be stateless with database-backed conversation history