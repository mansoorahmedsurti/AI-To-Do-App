# CLI API Contract

## Commands

### `add`
Adds a new todo to the list.

#### Syntax
```
todo add --title <title> [--description <description>] [--priority <priority>]
```

#### Parameters
- `--title`: Required. The title of the todo item.
- `--description`: Optional. Additional details about the todo.
- `--priority`: Optional. Priority level (low|medium|high). Defaults to "medium".

#### Exit Codes
- 0: Success
- 1: Error (invalid parameters, file I/O error)

#### Examples
```
todo add --title "Buy groceries"
todo add --title "Meeting prep" --priority high --description "Prepare slides for quarterly review"
```

### `list`
Displays all todos in a formatted table.

#### Syntax
```
todo list [--status <status>] [--priority <priority>]
```

#### Parameters
- `--status`: Optional. Filter by status (pending|completed). Show all if not specified.
- `--priority`: Optional. Filter by priority (low|medium|high). Show all if not specified.

#### Exit Codes
- 0: Success
- 1: Error (file I/O error)

#### Examples
```
todo list
todo list --status pending
todo list --priority high
```

### `complete`
Marks a todo as completed.

#### Syntax
```
todo complete <id>
```

#### Parameters
- `<id>`: Required. The ID of the todo to mark as completed.

#### Exit Codes
- 0: Success
- 1: Error (todo not found, file I/O error)
- 2: Warning (todo already completed)

#### Examples
```
todo complete 550e8400-e29b-41d4-a716-446655440000
```

### `delete`
Removes a todo from the list.

#### Syntax
```
todo delete <id>
```

#### Parameters
- `<id>`: Required. The ID of the todo to delete.

#### Exit Codes
- 0: Success
- 1: Error (todo not found, file I/O error)

#### Examples
```
todo delete 550e8400-e29b-41d4-a716-446655440000
```

### `update`
Updates properties of an existing todo.

#### Syntax
```
todo update <id> [--title <title>] [--description <description>] [--priority <priority>] [--status <status>]
```

#### Parameters
- `<id>`: Required. The ID of the todo to update.
- `--title`: Optional. New title for the todo.
- `--description`: Optional. New description for the todo.
- `--priority`: Optional. New priority level (low|medium|high).
- `--status`: Optional. New status (pending|completed).

#### Exit Codes
- 0: Success
- 1: Error (todo not found, invalid parameters, file I/O error)

#### Examples
```
todo update 550e8400-e29b-41d4-a716-446655440000 --priority high
todo update 550e8400-e29b-41d4-a716-446655440000 --title "Updated title" --status completed
```

## Data Contract

### File Format
Todos are stored in a JSON file with an array of todo objects:

```json
[
  {
    "id": "string (UUID)",
    "title": "string (1-255 chars)",
    "description": "string (0-1000 chars) | null",
    "priority": "string (low|medium|high)",
    "status": "string (pending|completed)",
    "createdAt": "string (ISO 8601 date)",
    "updatedAt": "string (ISO 8601 date)"
  }
]
```

### File Location
Default: `./data/todos.json` (relative to execution directory)
Customizable via `--data-file` option in future versions.

## Error Handling
All commands return appropriate exit codes to indicate success or failure.
Error messages are written to stderr.
Success messages are written to stdout.