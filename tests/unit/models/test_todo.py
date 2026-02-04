import pytest
from datetime import datetime
from app.models.todo import Todo


def test_create_todo_with_required_fields():
    """Test creating a todo with required fields."""
    todo = Todo(id="123", title="Test Todo")

    assert todo.id == "123"
    assert todo.title == "Test Todo"
    assert todo.priority == "medium"  # Default value
    assert todo.status == "pending"   # Default value
    assert todo.created_at is not None
    assert todo.updated_at is not None


def test_create_todo_with_all_fields():
    """Test creating a todo with all fields specified."""
    todo = Todo(
        id="123",
        title="Test Todo",
        description="Test Description",
        priority="high",
        status="completed",
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00"
    )

    assert todo.id == "123"
    assert todo.title == "Test Todo"
    assert todo.description == "Test Description"
    assert todo.priority == "high"
    assert todo.status == "completed"
    assert todo.created_at == "2023-01-01T00:00:00"
    assert todo.updated_at == "2023-01-01T00:00:00"


def test_title_required_validation():
    """Test that title is required."""
    with pytest.raises(ValueError, match="Title is required"):
        Todo(id="123", title="")


def test_title_length_validation():
    """Test that title cannot exceed 255 characters."""
    long_title = "t" * 256
    with pytest.raises(ValueError, match="Title must be 255 characters or less"):
        Todo(id="123", title=long_title)


def test_priority_validation():
    """Test that priority must be one of the allowed values."""
    with pytest.raises(ValueError, match="Priority must be one of: low, medium, high"):
        Todo(id="123", title="Test", priority="invalid")


def test_status_validation():
    """Test that status must be one of the allowed values."""
    with pytest.raises(ValueError, match="Status must be one of: pending, completed"):
        Todo(id="123", title="Test", status="invalid")


def test_description_length_validation():
    """Test that description cannot exceed 1000 characters."""
    long_description = "d" * 1001
    with pytest.raises(ValueError, match="Description must be 1000 characters or less"):
        Todo(id="123", title="Test", description=long_description)


def test_mark_completed():
    """Test marking a todo as completed."""
    todo = Todo(id="123", title="Test Todo")

    assert todo.status == "pending"

    todo.mark_completed()

    assert todo.status == "completed"
    # The updated_at should be newer than created_at
    assert todo.updated_at >= todo.created_at


def test_update_method():
    """Test updating todo properties."""
    todo = Todo(id="123", title="Original Title", priority="low")

    # Update multiple fields
    todo.update(title="Updated Title", priority="high", description="New description")

    assert todo.title == "Updated Title"
    assert todo.priority == "high"
    assert todo.description == "New description"

    # Verify updated_at changed
    assert todo.updated_at >= todo.created_at


def test_update_with_invalid_values():
    """Test updating with invalid values raises exceptions."""
    todo = Todo(id="123", title="Test Todo")

    # Attempt to update with invalid priority
    with pytest.raises(ValueError, match="Priority must be one of: low, medium, high"):
        todo.update(priority="invalid")

    # Attempt to update with invalid status
    with pytest.raises(ValueError, match="Status must be one of: pending, completed"):
        todo.update(status="invalid")

    # Attempt to update with title that's too long
    with pytest.raises(ValueError, match="Title must be 255 characters or less"):
        todo.update(title="t" * 256)


def test_to_dict_conversion():
    """Test converting Todo object to dictionary."""
    todo = Todo(id="123", title="Test Todo", description="Test Description")

    todo_dict = todo.to_dict()

    assert isinstance(todo_dict, dict)
    assert todo_dict["id"] == "123"
    assert todo_dict["title"] == "Test Todo"
    assert todo_dict["description"] == "Test Description"
    assert todo_dict["priority"] == "medium"
    assert todo_dict["status"] == "pending"
    assert "created_at" in todo_dict
    assert "updated_at" in todo_dict