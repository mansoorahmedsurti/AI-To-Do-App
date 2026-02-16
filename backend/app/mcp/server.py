"""MCP Server for Todo Management Tools"""

import asyncio
from typing import Dict, Any, List
from mcp.server import Server
from mcp.types import TextContent, Tool, CallToolResult, ListToolsResult
import json
import uuid
from sqlmodel import Session, select
from app.db.database import get_session
from app.models.todo import Todo, TodoCreate
from app.models.conversation import Conversation, Message
from app.models.user import User


# Create the server instance globally
server = Server("todo-mcp-server")


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """Return the list of available tools"""
    tools = [
        Tool(
            name="add_task",
            description="Add a new task to the user's todo list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "UUID of the user"},
                    "title": {"type": "string", "description": "Title of the task"},
                    "description": {"type": "string", "description": "Description of the task"},
                    "priority": {"type": "string", "description": "Priority of the task (low, medium, high)", "default": "medium"}
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="Retrieve user's tasks with optional filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "UUID of the user"},
                    "status": {"type": "string", "description": "Filter by status (pending, completed)"}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "UUID of the user"},
                    "task_id": {"type": "string", "description": "UUID of the task to complete"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Remove a task from the user's list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "UUID of the user"},
                    "task_id": {"type": "string", "description": "UUID of the task to delete"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Modify an existing task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "UUID of the user"},
                    "task_id": {"type": "string", "description": "UUID of the task to update"},
                    "title": {"type": "string", "description": "New title for the task"},
                    "description": {"type": "string", "description": "New description for the task"},
                    "status": {"type": "string", "description": "New status for the task (pending, completed)"},
                    "priority": {"type": "string", "description": "New priority for the task (low, medium, high)"},
                    "due_date": {"type": "string", "description": "New due date for the task (ISO format)"}
                },
                "required": ["user_id", "task_id"]
            }
        )
    ]
    return tools


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle all tool calls"""
    try:
        if name == "add_task":
            return await handle_add_task(arguments)
        elif name == "list_tasks":
            return await handle_list_tasks(arguments)
        elif name == "complete_task":
            return await handle_complete_task(arguments)
        elif name == "delete_task":
            return await handle_delete_task(arguments)
        elif name == "update_task":
            return await handle_update_task(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error executing tool {name}: {str(e)}")]


async def handle_add_task(params: Dict[str, Any]) -> List[TextContent]:
    """Handle the add_task tool call"""
    try:
        user_id_str = params["user_id"]
        title = params["title"]
        description = params.get("description", "")
        priority = params.get("priority", "medium")

        # Convert user_id to UUID
        user_id = uuid.UUID(user_id_str)

        # Create the todo using the database session
        with next(get_session()) as session:
            # Verify user exists
            user = session.get(User, user_id)
            if not user:
                return [TextContent(type="text", text="User not found")]

            # Create new todo
            new_todo = Todo(
                title=title,
                description=description,
                priority=priority,
                user_id=user_id,
                completed=False  # Default to not completed
            )

            session.add(new_todo)
            session.commit()
            session.refresh(new_todo)

            response = f"Task '{title}' has been added successfully with ID: {new_todo.id}"
            return [TextContent(type="text", text=response)]

    except Exception as e:
        return [TextContent(type="text", text=f"Error adding task: {str(e)}")]


async def handle_list_tasks(params: Dict[str, Any]) -> List[TextContent]:
    """Handle the list_tasks tool call"""
    try:
        user_id_str = params["user_id"]
        status_filter = params.get("status")

        # Convert user_id to UUID
        user_id = uuid.UUID(user_id_str)

        with next(get_session()) as session:
            # Verify user exists
            user = session.get(User, user_id)
            if not user:
                return [TextContent(type="text", text="User not found")]

            # Build query
            query = select(Todo).where(Todo.user_id == user_id)

            if status_filter:
                completed = status_filter.lower() == "completed"
                query = query.where(Todo.completed == completed)

            todos = session.exec(query).all()

            if not todos:
                response = "No tasks found."
            else:
                task_list = []
                for todo in todos:
                    status = "completed" if todo.completed else "pending"
                    task_list.append(f"- [{todo.id}] {todo.title} ({status}) - Priority: {todo.priority}")

                response = "Your tasks:\n" + "\n".join(task_list)

            return [TextContent(type="text", text=response)]

    except Exception as e:
        return [TextContent(type="text", text=f"Error listing tasks: {str(e)}")]


async def handle_complete_task(params: Dict[str, Any]) -> List[TextContent]:
    """Handle the complete_task tool call"""
    try:
        user_id_str = params["user_id"]
        task_id_str = params["task_id"]

        # Convert IDs to UUID
        user_id = uuid.UUID(user_id_str)
        task_id = uuid.UUID(task_id_str)

        with next(get_session()) as session:
            # Verify user exists
            user = session.get(User, user_id)
            if not user:
                return [TextContent(type="text", text="User not found")]

            # Find and update the task
            todo = session.get(Todo, task_id)
            if not todo:
                return [TextContent(type="text", text=f"Task with ID {task_id} not found")]

            if todo.user_id != user_id:
                return [TextContent(type="text", text="Unauthorized: Task does not belong to user")]

            todo.completed = True
            session.add(todo)
            session.commit()

            response = f"Task '{todo.title}' has been marked as completed."
            return [TextContent(type="text", text=response)]

    except Exception as e:
        return [TextContent(type="text", text=f"Error completing task: {str(e)}")]


async def handle_delete_task(params: Dict[str, Any]) -> List[TextContent]:
    """Handle the delete_task tool call"""
    try:
        user_id_str = params["user_id"]
        task_id_str = params["task_id"]

        # Convert IDs to UUID
        user_id = uuid.UUID(user_id_str)
        task_id = uuid.UUID(task_id_str)

        with next(get_session()) as session:
            # Verify user exists
            user = session.get(User, user_id)
            if not user:
                return [TextContent(type="text", text="User not found")]

            # Find and delete the task
            todo = session.get(Todo, task_id)
            if not todo:
                return [TextContent(type="text", text=f"Task with ID {task_id} not found")]

            if todo.user_id != user_id:
                return [TextContent(type="text", text="Unauthorized: Task does not belong to user")]

            session.delete(todo)
            session.commit()

            response = f"Task '{todo.title}' has been deleted."
            return [TextContent(type="text", text=response)]

    except Exception as e:
        return [TextContent(type="text", text=f"Error deleting task: {str(e)}")]


async def handle_update_task(params: Dict[str, Any]) -> List[TextContent]:
    """Handle the update_task tool call"""
    try:
        user_id_str = params["user_id"]
        task_id_str = params["task_id"]

        # Extract update fields
        title = params.get("title")
        description = params.get("description")
        status = params.get("status")
        priority = params.get("priority")
        due_date = params.get("due_date")

        # Convert IDs to UUID
        user_id = uuid.UUID(user_id_str)
        task_id = uuid.UUID(task_id_str)

        with next(get_session()) as session:
            # Verify user exists
            user = session.get(User, user_id)
            if not user:
                return [TextContent(type="text", text="User not found")]

            # Find the task to update
            todo = session.get(Todo, task_id)
            if not todo:
                return [TextContent(type="text", text=f"Task with ID {task_id} not found")]

            if todo.user_id != user_id:
                return [TextContent(type="text", text="Unauthorized: Task does not belong to user")]

            # Update fields if provided
            if title is not None:
                todo.title = title
            if description is not None:
                todo.description = description
            if status is not None:
                todo.completed = status.lower() == "completed"
            if priority is not None:
                todo.priority = priority
            if due_date is not None:
                # Note: In a real implementation, you'd parse the date properly
                todo.due_date = due_date

            session.add(todo)
            session.commit()

            response = f"Task '{todo.title}' has been updated."
            return [TextContent(type="text", text=response)]

    except Exception as e:
        return [TextContent(type="text", text=f"Error updating task: {str(e)}")]


# Helper function to run the server
async def run_server():
    from mcp.server.stdio import stdio_server
    from mcp.server.models import InitializationOptions
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(run_server())