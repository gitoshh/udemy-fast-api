from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from models import Users
from routers.auth import get_current_user
from database import get_db
from passlib.context import CryptContext
from schemas import PasswordChangeRequest

router = APIRouter(prefix="/users", tags=["users"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
current_user_dependency = Annotated[dict, Depends(get_current_user)];
db_dependency = Annotated[Users, Depends(get_db)]


@router.get("/")
async def get_me(current_user: current_user_dependency, db: db_dependency):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db.query(Users).filter(Users.id == current_user["user_id"]).first()

@router.post("/update/password")
async def update_password(current_user: current_user_dependency, db: db_dependency, password_change: PasswordChangeRequest):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user = db.query(Users).filter(Users.id == current_user["user_id"]).first()
    if not bcrypt_context.verify(password_change.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid current password")
    user.hashed_password = bcrypt_context.hash(password_change.new_password)
    db.commit()
    return user
