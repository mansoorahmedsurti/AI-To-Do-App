"""
Constants for the Todo CLI application.
"""

# Valid values
VALID_PRIORITIES = ["low", "medium", "high"]
VALID_STATUSES = ["pending", "completed"]

# File paths
DEFAULT_DATA_FILE = "data/todos.json"

# Error messages
ERROR_MESSAGES = {
    "TITLE_REQUIRED": "Title is required",
    "INVALID_PRIORITY": "Priority must be one of: low, medium, high",
    "INVALID_STATUS": "Status must be one of: pending, completed",
    "TODO_NOT_FOUND": "Todo not found",
    "TITLE_TOO_LONG": "Title must be 255 characters or less",
    "DESC_TOO_LONG": "Description must be 1000 characters or less"
}