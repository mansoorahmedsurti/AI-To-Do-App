import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional


def load_json_file(file_path: str) -> List[Dict[Any, Any]]:
    """
    Load data from a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        List of dictionaries representing the data

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    path = Path(file_path)

    # Create the file if it doesn't exist
    if not path.exists():
        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        # Initialize with an empty array
        save_json_file(file_path, [])
        return []

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip()

        # Handle empty file
        if not content:
            return []

        data = json.loads(content)

        # Ensure data is a list
        if not isinstance(data, list):
            raise ValueError(f"Expected a list in {file_path}, got {type(data).__name__}")

        return data


def save_json_file(file_path: str, data: List[Dict[Any, Any]]) -> None:
    """
    Save data to a JSON file.

    Args:
        file_path: Path to the JSON file
        data: List of dictionaries to save

    Raises:
        TypeError: If the data is not JSON serializable
    """
    path = Path(file_path)

    # Create parent directories if they don't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def append_to_json_file(file_path: str, item: Dict[Any, Any]) -> None:
    """
    Append an item to a JSON file containing an array.

    Args:
        file_path: Path to the JSON file
        item: Dictionary to append
    """
    data = load_json_file(file_path)
    data.append(item)
    save_json_file(file_path, data)


def update_json_item_by_id(file_path: str, item_id: str, updated_item: Dict[Any, Any]) -> bool:
    """
    Update an item in a JSON file by its ID.

    Args:
        file_path: Path to the JSON file
        item_id: ID of the item to update
        updated_item: New item data

    Returns:
        True if the item was found and updated, False otherwise
    """
    data = load_json_file(file_path)

    for i, item in enumerate(data):
        if item.get('id') == item_id:
            data[i] = updated_item
            save_json_file(file_path, data)
            return True

    return False


def delete_from_json_file_by_id(file_path: str, item_id: str) -> bool:
    """
    Delete an item from a JSON file by its ID.

    Args:
        file_path: Path to the JSON file
        item_id: ID of the item to delete

    Returns:
        True if the item was found and deleted, False otherwise
    """
    data = load_json_file(file_path)

    initial_length = len(data)
    data = [item for item in data if item.get('id') != item_id]

    if len(data) < initial_length:
        save_json_file(file_path, data)
        return True

    return False