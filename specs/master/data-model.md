# Data Model

## Todo Entity

### Fields
- **id** (string/uuid): Unique identifier for the todo
- **title** (string): The main title/description of the todo (required)
- **description** (string): Additional details about the todo (optional)
- **priority** (string): Priority level (values: "low", "medium", "high") - defaults to "medium"
- **status** (string): Completion status (values: "pending", "completed") - defaults to "pending"
- **createdAt** (Date string): Timestamp when the todo was created (ISO 8601 format)
- **updatedAt** (Date string): Timestamp when the todo was last modified (ISO 8601 format)

### Validation Rules
- title: Required, minimum length 1 character, maximum length 255 characters
- description: Optional, maximum length 1000 characters
- priority: Must be one of "low", "medium", "high"
- status: Must be one of "pending", "completed"
- createdAt: Must be a valid ISO 8601 date string, defaults to current timestamp
- updatedAt: Must be a valid ISO 8601 date string, defaults to current timestamp

### State Transitions
- From "pending" to "completed": When user marks todo as complete
- From "completed" to "pending": When user reopens completed todo

### JSON Format Example
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, bread, eggs, fruits",
  "priority": "high",
  "status": "pending",
  "createdAt": "2026-02-04T16:00:00.000Z",
  "updatedAt": "2026-02-04T16:00:00.000Z"
}
```

### Storage Format
Todos are stored in an array within a JSON file (default: `data/todos.json`):
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, bread, eggs, fruits",
    "priority": "high",
    "status": "pending",
    "createdAt": "2026-02-04T16:00:00.000Z",
    "updatedAt": "2026-02-04T16:00:00.000Z"
  }
]
```