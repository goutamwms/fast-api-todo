from fastapi import APIRouter, Depends
from app.models.todo import CreateTodo
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.schema.todo_schema import TodoSchema


router = APIRouter(prefix="/todo")


@router.get("/")
def index(db: Annotated[Session, Depends(get_db)]):
    todos = db.query(TodoSchema).all()
    return {"message": "todos", "items": todos}


@router.post("/")
def store(item: CreateTodo, db: Annotated[Session, Depends(get_db)]):
    todo = TodoSchema(content=item.content, is_completed=item.is_completed)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {"message": "storing todos", "dump_item": item.model_dump(), "item": todo}
