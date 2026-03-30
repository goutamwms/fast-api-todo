from fastapi import APIRouter, Depends
from app.models.todo import CreateTodo
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.schema.todo_schema import TodoSchema
from sqlalchemy import select


router = APIRouter(prefix="/todos")


@router.get("/")
def index(db: Annotated[Session, Depends(get_db)]):
    todos = db.query(TodoSchema).all()
    return {"message": "todos", "items": todos}


@router.get("/getAll")
def allTodos(db: Annotated[Session, Depends(get_db)]):
    stmt = select(TodoSchema.id, TodoSchema.content, TodoSchema.is_completed)
    todos = db.execute(stmt).mappings().all()
    return {"message": "todos", "items": todos}


@router.post("/")
def store(item: CreateTodo, db: Annotated[Session, Depends(get_db)]):
    todo = TodoSchema(content=item.content, is_completed=item.is_completed)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {"message": "storing todos", "dump_item": item.model_dump(), "item": todo}


@router.get("/{id}")
def show(id: int, db: Annotated[Session, Depends(get_db)]):
    todo = db.query(TodoSchema).filter(TodoSchema.id == id).first()
    return {"message": "getiing a todo", "item": todo}


@router.put("/{id}")
def update(id: int, item: CreateTodo, db: Annotated[Session, Depends(get_db)]):
    todo = db.query(TodoSchema).filter(TodoSchema.id == id).first()
    if not todo:
        return {"message": "No record found"}

    todo.content = item.content
    todo.is_completed = item.is_completed
    db.commit()
    db.refresh(todo)
    return {"message": "Todo updated", "item": todo}


@router.delete("/{id}")
def delete(id: int, db: Annotated[Session, Depends(get_db)]):
    todo = db.query(TodoSchema).filter(TodoSchema.id == id).first()
    if not todo:
        return {"message": "No record found"}

    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}
