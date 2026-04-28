from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from database import get_db
from models import Todo, Users
from routers.auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

current_user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(current_user: current_user_dependency, db: Annotated[Session, Depends(get_db)]):
    if current_user.get("role") != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    users = db.query(Users).all()
    return users


@router.get("/todos/all", status_code=status.HTTP_200_OK)
async def get_all_todos(current_user: current_user_dependency, db: Annotated[Session, Depends(get_db)]):
    if current_user.get("role") != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    todos = db.query(Todo).all()
    return todos
