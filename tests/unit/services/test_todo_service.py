import pytest
import tempfile
import os
from app.services.todo_service import TodoService
from app.models.todo import Todo


def test_add_todo_creates_new_todo():
    """Test that add_todo creates a new todo and saves it to file."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp_file:
        tmp_filename = tmp_file.name

    try:
        service = TodoService(data_file=tmp_filename)

        # Initially the file should be empty
        assert len(service.get_all_todos()) == 0

        # Add a new todo
        new_todo = service.add_todo(
            title="Test Todo",
            description="Test Description",
            priority="high"
        )

        # Verify the returned todo has correct values
        assert new_todo.title == "Test Todo"
        assert new_todo.description == "Test Description"
        assert new_todo.priority == "high"
        assert new_todo.status == "pending"
        assert new_todo.id is not None

        # Verify the todo was saved to the file
        all_todos = service.get_all_todos()
        assert len(all_todos) == 1
        assert all_todos[0].title == "Test Todo"
        assert all_todos[0].description == "Test Description"
        assert all_todos[0].priority == "high"

    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)


def test_add_todo_default_values():
    """Test that add_todo uses default values when not specified."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp_file:
        tmp_filename = tmp_file.name

    try:
        service = TodoService(data_file=tmp_filename)

        # Add a new todo with only required fields
        new_todo = service.add_todo(title="Minimal Todo")

        # Verify defaults were applied
        assert new_todo.title == "Minimal Todo"
        assert new_todo.priority == "medium"  # Default
        assert new_todo.status == "pending"   # Default
        assert new_todo.description is None   # Default

        # Verify the todo was saved
        all_todos = service.get_all_todos()
        assert len(all_todos) == 1
        saved_todo = all_todos[0]
        assert saved_todo.title == "Minimal Todo"
        assert saved_todo.priority == "medium"
        assert saved_todo.status == "pending"

    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)


def test_get_all_todos():
    """Test retrieving all todos from the file."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp_file:
        tmp_filename = tmp_file.name

    try:
        service = TodoService(data_file=tmp_filename)

        # Initially, there should be no todos
        assert len(service.get_all_todos()) == 0

        # Add multiple todos
        service.add_todo(title="First Todo", priority="low")
        service.add_todo(title="Second Todo", priority="high")
        service.add_todo(title="Third Todo", priority="medium")

        # Retrieve all todos
        all_todos = service.get_all_todos()

        # Verify we have 3 todos
        assert len(all_todos) == 3

        # Verify the todos have the correct titles
        titles = [todo.title for todo in all_todos]
        assert "First Todo" in titles
        assert "Second Todo" in titles
        assert "Third Todo" in titles

    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)


def test_get_todo_by_id_found():
    """Test retrieving a specific todo by its ID."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp_file:
        tmp_filename = tmp_file.name

    try:
        service = TodoService(data_file=tmp_filename)

        # Add a todo
        original_todo = service.add_todo(title="Find Me", priority="high")

        # Retrieve by ID
        retrieved_todo = service.get_todo_by_id(original_todo.id)

        # Verify the todo was found and matches
        assert retrieved_todo is not None
        assert retrieved_todo.id == original_todo.id
        assert retrieved_todo.title == "Find Me"
        assert retrieved_todo.priority == "high"

    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)


def test_get_todo_by_id_not_found():
    """Test retrieving a non-existent todo by its ID."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp_file:
        tmp_filename = tmp_file.name

    try:
        service = TodoService(data_file=tmp_filename)

        # Try to retrieve a non-existent todo
        retrieved_todo = service.get_todo_by_id("non-existent-id")

        # Verify None was returned
        assert retrieved_todo is None

    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)


def test_mark_completed():
    """Test marking a todo as completed."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp_file:
        tmp_filename = tmp_file.name

    try:
        service = TodoService(data_file=tmp_filename)

        # Add a todo
        original_todo = service.add_todo(title="To Complete", status="pending")

        # Verify initial status
        retrieved_todo = service.get_todo_by_id(original_todo.id)
        assert retrieved_todo.status == "pending"

        # Mark as completed
        result = service.mark_completed(original_todo.id)

        # Verify the operation was successful
        assert result is True

        # Verify the status was updated
        updated_todo = service.get_todo_by_id(original_todo.id)
        assert updated_todo.status == "completed"

    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)


def test_mark_completed_non_existent():
    """Test marking a non-existent todo as completed."""
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as tmp_file:
        tmp_filename = tmp_file.name

    try:
        service = TodoService(data_file=tmp_filename)

        # Try to mark a non-existent todo as completed
        result = service.mark_completed("non-existent-id")

        # Verify the operation failed
        assert result is False

    finally:
        # Clean up the temporary file
        if os.path.exists(tmp_filename):
            os.remove(tmp_filename)