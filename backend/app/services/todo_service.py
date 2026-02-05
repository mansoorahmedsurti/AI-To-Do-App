from typing import List, Optional
from sqlmodel import Session, select
from app.models.todo import Todo, TodoCreate, TodoUpdate
from uuid import UUID


def create_todo(*, session: Session, todo_create: TodoCreate) -> Todo:
    db_todo = Todo.model_validate(todo_create)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


def get_todos(*, session: Session, user_id: UUID) -> List[Todo]:
    statement = select(Todo).where(Todo.user_id == user_id)
    return session.exec(statement).all()


def get_todo_by_id(*, session: Session, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    return session.exec(statement).first()


def update_todo(*, session: Session, db_todo: Todo, todo_update: TodoUpdate) -> Todo:
    todo_data = todo_update.model_dump(exclude_unset=True)
    db_todo.sqlmodel_update(todo_data)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


def delete_todo(*, session: Session, db_todo: Todo) -> None:
    session.delete(db_todo)
    session.commit()


def toggle_todo_completion(*, session: Session, db_todo: Todo) -> Todo:
    db_todo.completed = not db_todo.completed
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo