#!/usr/bin/env python3
"""
CLI application for managing todos.
"""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from .services.todo_service import TodoService
from .models.todo import Todo

# Initialize Typer app
app = typer.Typer()

# Initialize console
console = Console()

# Default service instance
service = TodoService()


@app.command()
def add(
    title: str = typer.Option(..., "--title", "-t", help="Title of the todo"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Description of the todo"),
    priority: str = typer.Option("medium", "--priority", "-p", help="Priority of the todo (low, medium, high)")
):
    """
    Add a new todo.
    """
    # Validate priority
    if priority not in ["low", "medium", "high"]:
        rprint(f"[red]Error: Priority must be one of 'low', 'medium', or 'high'[/red]")
        raise typer.Exit(code=1)

    try:
        # Create new todo
        new_todo = service.add_todo(
            title=title,
            description=description,
            priority=priority
        )

        # Display success message
        panel = Panel(
            f"[green]✓ Todo added successfully![/green]\n\n"
            f"[bold]ID:[/bold] {new_todo.id}\n"
            f"[bold]Title:[/bold] {new_todo.title}\n"
            f"[bold]Priority:[/bold] {new_todo.priority}\n"
            f"[bold]Status:[/bold] {new_todo.status}",
            title="Todo Added",
            border_style="green"
        )
        console.print(panel)

    except ValueError as e:
        rprint(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(code=1)
    except Exception as e:
        rprint(f"[red]Unexpected error: {str(e)}[/red]")
        raise typer.Exit(code=1)


@app.command()
def list(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status (pending, completed)"),
    priority: Optional[str] = typer.Option(None, "--priority", "-p", help="Filter by priority (low, medium, high)")
):
    """
    List all todos.
    """
    try:
        todos = service.get_all_todos()

        # Apply filters if provided
        if status:
            if status not in ["pending", "completed"]:
                rprint(f"[red]Error: Status must be 'pending' or 'completed'[/red]")
                raise typer.Exit(code=1)
            todos = [todo for todo in todos if todo.status == status]

        if priority:
            if priority not in ["low", "medium", "high"]:
                rprint(f"[red]Error: Priority must be 'low', 'medium', or 'high'[/red]")
                raise typer.Exit(code=1)
            todos = [todo for todo in todos if todo.priority == priority]

        # Create a table to display todos
        table = Table(title="Todos")
        table.add_column("ID", style="dim", width=36)
        table.add_column("Title", min_width=15)
        table.add_column("Priority", justify="center")
        table.add_column("Status", justify="center")
        table.add_column("Created At", style="dim")

        for todo in todos:
            # Color code based on priority
            if todo.priority == "high":
                priority_text = f"[red]{todo.priority}[/red]"
            elif todo.priority == "medium":
                priority_text = f"[yellow]{todo.priority}[/yellow]"
            else:  # low
                priority_text = f"[blue]{todo.priority}[/blue]"

            # Color code based on status
            if todo.status == "completed":
                status_text = f"[green]{todo.status}[/green]"
            else:
                status_text = f"[yellow]{todo.status}[/yellow]"

            table.add_row(
                todo.id[:8] + "...",  # Truncate ID for readability
                todo.title,
                priority_text,
                status_text,
                todo.created_at.split("T")[0]  # Just the date part
            )

        if todos:
            console.print(table)
        else:
            console.print("[italic]No todos found.[/italic]")

    except Exception as e:
        rprint(f"[red]Error listing todos: {str(e)}[/red]")
        raise typer.Exit(code=1)


@app.command()
def complete(
    todo_id: str = typer.Argument(..., help="ID of the todo to mark as completed")
):
    """
    Mark a todo as completed.
    """
    try:
        result = service.mark_completed(todo_id)

        if result:
            rprint(f"[green]✓ Todo marked as completed![/green]")

            # Show the updated todo
            updated_todo = service.get_todo_by_id(todo_id)
            if updated_todo:
                panel = Panel(
                    f"[bold]ID:[/bold] {updated_todo.id}\n"
                    f"[bold]Title:[/bold] {updated_todo.title}\n"
                    f"[bold]Status:[/bold] [green]{updated_todo.status}[/green]",
                    title="Updated Todo",
                    border_style="green"
                )
                console.print(panel)
        else:
            rprint(f"[red]✗ Todo with ID '{todo_id}' not found.[/red]")
            raise typer.Exit(code=1)

    except Exception as e:
        rprint(f"[red]Error completing todo: {str(e)}[/red]")
        raise typer.Exit(code=1)


@app.command()
def delete(
    todo_id: str = typer.Argument(..., help="ID of the todo to delete")
):
    """
    Delete a todo.
    """
    try:
        # Show the todo before deletion
        todo_to_delete = service.get_todo_by_id(todo_id)
        if todo_to_delete:
            panel = Panel(
                f"[bold]ID:[/bold] {todo_to_delete.id}\n"
                f"[bold]Title:[/bold] {todo_to_delete.title}\n"
                f"[bold]Priority:[/bold] {todo_to_delete.priority}\n"
                f"[bold]Status:[/bold] {todo_to_delete.status}",
                title="Deleting Todo",
                border_style="red"
            )
            console.print(panel)

        result = service.delete_todo(todo_id)

        if result:
            rprint(f"[green]✓ Todo deleted successfully![/green]")
        else:
            rprint(f"[red]✗ Todo with ID '{todo_id}' not found.[/red]")
            raise typer.Exit(code=1)

    except Exception as e:
        rprint(f"[red]Error deleting todo: {str(e)}[/red]")
        raise typer.Exit(code=1)


@app.command()
def update(
    todo_id: str = typer.Argument(..., help="ID of the todo to update"),
    title: Optional[str] = typer.Option(None, "--title", "-t", help="New title for the todo"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="New description for the todo"),
    priority: Optional[str] = typer.Option(None, "--priority", "-p", help="New priority for the todo (low, medium, high)"),
    status: Optional[str] = typer.Option(None, "--status", "-s", help="New status for the todo (pending, completed)")
):
    """
    Update a todo.
    """
    try:
        # Prepare update data
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
        if priority is not None:
            if priority not in ["low", "medium", "high"]:
                rprint(f"[red]Error: Priority must be 'low', 'medium', or 'high'[/red]")
                raise typer.Exit(code=1)
            update_data['priority'] = priority
        if status is not None:
            if status not in ["pending", "completed"]:
                rprint(f"[red]Error: Status must be 'pending' or 'completed'[/red]")
                raise typer.Exit(code=1)
            update_data['status'] = status

        # Check if any update data was provided
        if not update_data:
            rprint(f"[yellow]Warning: No update parameters provided.[/yellow]")
            return

        result = service.update_todo(todo_id, **update_data)

        if result:
            rprint(f"[green]✓ Todo updated successfully![/green]")

            # Show the updated todo
            updated_todo = service.get_todo_by_id(todo_id)
            if updated_todo:
                panel = Panel(
                    f"[bold]ID:[/bold] {updated_todo.id}\n"
                    f"[bold]Title:[/bold] {updated_todo.title}\n"
                    f"[bold]Priority:[/bold] {updated_todo.priority}\n"
                    f"[bold]Status:[/bold] {updated_todo.status}",
                    title="Updated Todo",
                    border_style="green"
                )
                console.print(panel)
        else:
            rprint(f"[red]✗ Todo with ID '{todo_id}' not found.[/red]")
            raise typer.Exit(code=1)

    except ValueError as e:
        rprint(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(code=1)
    except Exception as e:
        rprint(f"[red]Error updating todo: {str(e)}[/red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()