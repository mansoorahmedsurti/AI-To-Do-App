import uuid
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict


@dataclass
class Todo:
    """
    Todo entity representing a task with title, description, priority, and status.
    """
    id: str
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    status: str = "pending"
    created_at: str = None
    updated_at: str = None

    def __post_init__(self):
        """Validate and initialize default values."""
        # Set ID if not provided
        if not self.id:
            self.id = str(uuid.uuid4())

        # Set timestamps if not provided
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at

        # Validate required fields
        self._validate()

    def _validate(self):
        """Validate the Todo object according to business rules."""
        # Validate title
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Title is required")
        if len(self.title) > 255:
            raise ValueError("Title must be 255 characters or less")

        # Validate priority
        valid_priorities = ["low", "medium", "high"]
        if self.priority not in valid_priorities:
            raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")

        # Validate status
        valid_statuses = ["pending", "completed"]
        if self.status not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")

        # Validate description length
        if self.description and len(self.description) > 1000:
            raise ValueError("Description must be 1000 characters or less")

    def mark_completed(self):
        """Mark the todo as completed."""
        self.status = "completed"
        self.updated_at = datetime.now().isoformat()

    def update(self, **kwargs):
        """Update the todo with new values."""
        for field, value in kwargs.items():
            if hasattr(self, field):
                if field == "title":
                    # Re-validate title if it's being updated
                    if value is not None and len(value) > 255:
                        raise ValueError("Title must be 255 characters or less")
                elif field == "priority":
                    # Re-validate priority if it's being updated
                    valid_priorities = ["low", "medium", "high"]
                    if value is not None and value not in valid_priorities:
                        raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
                elif field == "status":
                    # Re-validate status if it's being updated
                    valid_statuses = ["pending", "completed"]
                    if value is not None and value not in valid_statuses:
                        raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")

                setattr(self, field, value)

        self.updated_at = datetime.now().isoformat()

    def to_dict(self):
        """Convert the Todo object to a dictionary."""
        return asdict(self)