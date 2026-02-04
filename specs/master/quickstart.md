# Quickstart Guide

## Prerequisites
- Node.js 18 or higher
- npm or yarn package manager

## Installation
```bash
# Clone the repository
git clone <repo-url>
cd <repo-name>

# Install dependencies
npm install
```

## Setup
```bash
# Create the data directory
mkdir -p data

# Initialize with empty todos file (optional)
echo "[]" > data/todos.json
```

## Usage
```bash
# Add a new todo
node src/cli/index.js add --title "My Task" --priority high

# List all todos
node src/cli/index.js list

# Complete a todo
node src/cli/index.js complete <todo-id>

# Delete a todo
node src/cli/index.js delete <todo-id>

# Update a todo
node src/cli/index.js update <todo-id> --title "Updated Task" --priority medium
```

## Configuration
- Data file location: `data/todos.json` (can be overridden with --data-file option)
- Default priority: "medium"
- Date format: ISO 8601

## Development
```bash
# Run tests
npm test

# Run linting
npm run lint

# Build (if applicable)
npm run build
```

## Troubleshooting
- If getting "command not found" errors, ensure you're running from the project root
- If data persistence fails, check that the `data/` directory exists and is writable
- For dependency issues, try clearing node_modules and reinstalling: `rm -rf node_modules && npm install`