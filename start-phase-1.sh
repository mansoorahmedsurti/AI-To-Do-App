#!/bin/bash
# Script to run the CLI application for Phase 1

echo "Starting AI To-Do App - Phase 1 (CLI)..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found. Make sure Python dependencies are installed globally."
fi

# Run the CLI application
python -m app.main --help

echo ""
echo "To use the CLI application, run commands like:"
echo "  python -m app.main add --title \"My Task\" --priority high"
echo "  python -m app.main list"
echo "  python -m app.main complete <todo-id>"
echo "  python -m app.main delete <todo-id>"
echo "  python -m app.main update <todo-id> --title \"Updated Task\" --priority medium"