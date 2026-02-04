import pytest
import tempfile
import os
from typer.testing import CliRunner
from app.main import app
from app.services.todo_service import TodoService


runner = CliRunner()


def test_add_command_creates_todo():
    """Test that the add command creates a new todo."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp_file:
        tmp_filename = tmp_file.name

    try:
        # Set up service to use temp file
        import app.main
        original_service = app.main.service
        app.main.service = TodoService(data_file=tmp_filename)

        # Run the add command
        result = runner.invoke(app, [
            "add",
            "--title", "Integration Test Todo",
            "--description", "Test description",
            "--priority", "high"
        ])

        # Check that the command succeeded
        assert result.exit_code == 0
        assert "Todo added successfully!" in result.output

        # Check that the todo was actually saved
        service = TodoService(data_file=tmp_filename)
        todos = service.get_all_todos()
        assert len(todos) == 1
        assert todos[0].title == "Integration Test Todo"
        assert todos[0].description == "Test description"
        assert todos[0].priority == "high"

    finally:
        # Restore original service and cleanup
        app.main.service = original_service
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)


def test_add_command_with_defaults():
    """Test that the add command uses defaults when not specified."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp_file:
        tmp_filename = tmp_file.name

    try:
        # Set up service to use temp file
        import app.main
        original_service = app.main
        app.main.service = TodoService(data_file=tmp_filename)

        # Run the add command with only title
        result = runner.invoke(app, [
            "add",
            "--title", "Minimal Todo"
        ])

        # Check that the command succeeded
        assert result.exit_code == 0
        assert "Todo added successfully!" in result.output

        # Check that the todo was saved with default values
        service = TodoService(data_file=tmp_filename)
        todos = service.get_all_todos()
        assert len(todos) == 1
        assert todos[0].title == "Minimal Todo"
        assert todos[0].priority == "medium"  # Default priority
        assert todos[0].status == "pending"   # Default status

    finally:
        # Restore original service and cleanup
        app.main.service = original_service
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)


def test_list_command_shows_todos():
    """Test that the list command shows todos."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp_file:
        tmp_filename = tmp_file.name

    try:
        # Set up service to use temp file
        import app.main
        original_service = app.main.service
        app.main.service = TodoService(data_file=tmp_filename)

        # Add a couple of todos
        service = TodoService(data_file=tmp_filename)
        service.add_todo(title="First Todo", priority="high")
        service.add_todo(title="Second Todo", priority="low")

        # Run the list command
        result = runner.invoke(app, ["list"])

        # Check that the command succeeded
        assert result.exit_code == 0
        assert "First Todo" in result.output
        assert "Second Todo" in result.output
        assert "high" in result.output
        assert "low" in result.output

    finally:
        # Restore original service and cleanup
        app.main.service = original_service
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)


def test_complete_command_updates_todo():
    """Test that the complete command updates a todo's status."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp_file:
        tmp_filename = tmp_file.name

    try:
        # Set up service to use temp file
        import app.main
        original_service = app.main.service
        app.main.service = TodoService(data_file=tmp_filename)

        # Add a todo
        service = TodoService(data_file=tmp_filename)
        todo = service.add_todo(title="Todo to Complete", priority="medium")

        # Run the complete command
        result = runner.invoke(app, ["complete", todo.id])

        # Check that the command succeeded
        assert result.exit_code == 0
        assert "Todo marked as completed!" in result.output

        # Verify the todo was updated
        updated_todo = service.get_todo_by_id(todo.id)
        assert updated_todo.status == "completed"

    finally:
        # Restore original service and cleanup
        app.main.service = original_service
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)


def test_delete_command_removes_todo():
    """Test that the delete command removes a todo."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp_file:
        tmp_filename = tmp_file.name

    try:
        # Set up service to use temp file
        import app.main
        original_service = app.main.service
        app.main.service = TodoService(data_file=tmp_filename)

        # Add a todo
        service = TodoService(data_file=tmp_filename)
        todo = service.add_todo(title="Todo to Delete", priority="medium")

        # Verify the todo exists
        assert len(service.get_all_todos()) == 1

        # Run the delete command
        result = runner.invoke(app, ["delete", todo.id])

        # Check that the command succeeded
        assert result.exit_code == 0
        assert "Todo deleted successfully!" in result.output

        # Verify the todo was deleted
        assert len(service.get_all_todos()) == 0

    finally:
        # Restore original service and cleanup
        app.main.service = original_service
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)