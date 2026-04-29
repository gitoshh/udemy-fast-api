from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from ..models import Todo, Users
from ..database import get_db
from ..schemas import TodoRequest, TodoResponse

from .auth import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def get_todo_or_404(db: Session, todo_id: int, user_id: int) -> models.Todo:
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).filter(models.Todo.owner_id == user_id).first()
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.get("/", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def read_todos(db: db_dependency) -> list[models.Todo]:
    return db.query(models.Todo).all()


@router.get("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def get_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)) -> models.Todo:
    return get_todo_or_404(db, todo_id, int(user.get("id")))


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest) -> models.Todo:
    todo = models.Todo(**todo_request.model_dump(), owner_id=user.get("id"))
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)) -> None:
    todo = get_todo_or_404(db, todo_id, user.get("id"))
    for key, value in todo_request.model_dump().items():
        setattr(todo, key, value)
    db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)) -> None:
    todo = get_todo_or_404(db, todo_id, user.get("id"))
    db.delete(todo)
    db.commit()
