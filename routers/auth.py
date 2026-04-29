from fastapi import APIRouter, status, Depends, HTTPException
from ..schemas import CreateUserRequest, TokenResponse
from ..models import Users
from passlib.context import CryptContext
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from jose import jwt, JWTError

from datetime import datetime, timedelta, timezone

JWT_SECRET = "d1a2bc5dc70b3cb2c97c741fd44df58c03c93a18aded95f3f184807b79ce7b69"
JWT_ALGORITHM = "HS256"


router = APIRouter(prefix="/auth", tags=["auth"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(db: db_dependency, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if user is None:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: Optional[str] = payload.get("sub")
        user_id: Optional[int] = payload.get("id")
        role: Optional[str] = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return {
            "username": username,
            "user_id": user_id,
            "role": role,
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")



@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, user_request: CreateUserRequest):
    # Override the password to hashed password
    user = Users(
        email=user_request.email,
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        hashed_password=bcrypt_context.hash(user_request.password),
        role=user_request.role,
        phone_number=user_request.phone_number,
    )
    db.add(user)
    db.commit()
    return user

@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return user


@router.post("/token", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def create_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenResponse:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token = create_access_token(user.username, user.id, user.role, timedelta(minutes=30))
    return TokenResponse(access_token=access_token, token_type="bearer")
