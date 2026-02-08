# Phase 1: Quickstart Guide

## Prerequisites
- Python 3.13 or higher
- pip package manager

## Installation
```bash
# Clone the repository
git clone <repo-url>
cd <repo-name>

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
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
python -m app.main add --title "My Task" --priority high

# List all todos
python -m app.main list

# Complete a todo
python -m app.main complete <todo-id>

# Delete a todo
python -m app.main delete <todo-id>

# Update a todo
python -m app.main update <todo-id> --title "Updated Task" --priority medium
```

## Configuration
- Data file location: `data/todos.json` (can be overridden with --data-file option)
- Default priority: "medium"
- Date format: ISO 8601

## Development
```bash
# Run tests
pytest

# Run linting (if configured)
python -m flake8 app/

# Run the application directly
python -m app.main --help
```

## Troubleshooting
- If getting "command not found" errors, ensure you're running from the project root
- If data persistence fails, check that the `data/` directory exists and is writable
- For dependency issues, try clearing node_modules and reinstalling: `rm -rf node_modules && npm install`