from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID

from app.db.database import get_session
from app.models.todo import Todo, TodoCreate, TodoUpdate, TodoResponse
from app.services.todo_service import (
    create_todo, get_todos, get_todo_by_id, update_todo, delete_todo, toggle_todo_completion
)
from app.core.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[TodoResponse])
def read_todos(
    current_user: dict = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """
    Retrieve todos for the current user.
    """
    todos = get_todos(session=session, user_id=current_user.id)
    return todos


@router.post("/", response_model=TodoResponse)
def create_new_todo(
    todo: TodoCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new todo for the current user.
    """
    # Ensure the todo is associated with the current user
    todo.user_id = current_user.id
    db_todo = create_todo(session=session, todo_create=todo)
    return db_todo


@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo(
    todo_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific todo by ID.
    """
    db_todo = get_todo_by_id(session=session, todo_id=todo_id, user_id=current_user.id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.put("/{todo_id}", response_model=TodoResponse)
def update_existing_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific todo by ID.
    """
    db_todo = get_todo_by_id(session=session, todo_id=todo_id, user_id=current_user.id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    updated_todo = update_todo(session=session, db_todo=db_todo, todo_update=todo_update)
    return updated_todo


@router.delete("/{todo_id}")
def delete_existing_todo(
    todo_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific todo by ID.
    """
    db_todo = get_todo_by_id(session=session, todo_id=todo_id, user_id=current_user.id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    delete_todo(session=session, db_todo=db_todo)
    return {"message": "Todo deleted successfully"}


@router.patch("/{todo_id}/complete")
def toggle_todo_complete(
    todo_id: UUID,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific todo.
    """
    db_todo = get_todo_by_id(session=session, todo_id=todo_id, user_id=current_user.id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    toggled_todo = toggle_todo_completion(session=session, db_todo=db_todo)
    return toggled_todo