"""
Service layer for Todo operations.
Handles business logic for CRUD operations on todos.
"""

from typing import List, Optional, Dict, Any
from ..models.todo import Todo
from ..utils.file_utils import (
    load_json_file,
    save_json_file,
    append_to_json_file,
    update_json_item_by_id,
    delete_from_json_file_by_id
)
from .. import DEFAULT_DATA_FILE


class TodoService:
    """Service class for handling todo business logic."""

    def __init__(self, data_file: str = DEFAULT_DATA_FILE):
        """
        Initialize the TodoService.

        Args:
            data_file: Path to the JSON file for storing todos
        """
        self.data_file = data_file

    def add_todo(self, title: str, description: Optional[str] = None,
                 priority: str = "medium", status: str = "pending") -> Todo:
        """
        Add a new todo.

        Args:
            title: Title of the todo
            description: Description of the todo
            priority: Priority level ('low', 'medium', 'high')
            status: Status ('pending', 'completed')

        Returns:
            Created Todo object
        """
        # Create a new Todo instance
        todo = Todo(
            id="",  # Will be generated automatically
            title=title,
            description=description,
            priority=priority,
            status=status
        )

        # Convert to dict and save to file
        todo_dict = todo.to_dict()

        # Append to JSON file
        append_to_json_file(self.data_file, todo_dict)

        return todo

    def get_all_todos(self) -> List[Todo]:
        """
        Get all todos.

        Returns:
            List of Todo objects
        """
        data = load_json_file(self.data_file)
        todos = []

        for item in data:
            # Create Todo object without validation to avoid issues with data loading
            todo = Todo(
                id=item.get("id"),
                title=item.get("title", ""),
                description=item.get("description"),
                priority=item.get("priority", "medium"),
                status=item.get("status", "pending"),
                created_at=item.get("created_at"),
                updated_at=item.get("updated_at")
            )
            todos.append(todo)

        return todos

    def get_todo_by_id(self, todo_id: str) -> Optional[Todo]:
        """
        Get a specific todo by its ID.

        Args:
            todo_id: ID of the todo

        Returns:
            Todo object if found, None otherwise
        """
        data = load_json_file(self.data_file)

        for item in data:
            if item.get("id") == todo_id:
                # Create Todo object
                todo = Todo(
                    id=item.get("id"),
                    title=item.get("title", ""),
                    description=item.get("description"),
                    priority=item.get("priority", "medium"),
                    status=item.get("status", "pending"),
                    created_at=item.get("created_at"),
                    updated_at=item.get("updated_at")
                )
                return todo

        return None

    def update_todo(self, todo_id: str, **updates) -> bool:
        """
        Update a todo with the given ID.

        Args:
            todo_id: ID of the todo to update
            **updates: Fields to update

        Returns:
            True if the todo was found and updated, False otherwise
        """
        # Get existing todo
        existing_todo = self.get_todo_by_id(todo_id)
        if not existing_todo:
            return False

        # Update the todo object
        existing_todo.update(**updates)

        # Save updated todo back to file
        updated_dict = existing_todo.to_dict()
        return update_json_item_by_id(self.data_file, todo_id, updated_dict)

    def delete_todo(self, todo_id: str) -> bool:
        """
        Delete a todo with the given ID.

        Args:
            todo_id: ID of the todo to delete

        Returns:
            True if the todo was found and deleted, False otherwise
        """
        return delete_from_json_file_by_id(self.data_file, todo_id)

    def mark_completed(self, todo_id: str) -> bool:
        """
        Mark a todo as completed.

        Args:
            todo_id: ID of the todo to mark as completed

        Returns:
            True if the todo was found and updated, False otherwise
        """
        return self.update_todo(todo_id, status="completed")