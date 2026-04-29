from pydantic import BaseModel, Field


class TodoRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    priority: int = Field(ge=1, le=5)
    completed: bool = False


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    completed: bool

    model_config = {"from_attributes": True}

class CreateUserRequest(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=1, max_length=100)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1, max_length=100)
    role: str = Field(min_length=1, max_length=50)
    phone_number: str = Field(min_length=9, max_length=50)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    phone_number: str

    model_config = {"from_attributes": True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class PasswordChangeRequest(BaseModel):
    current_password: str = Field(min_length=1, max_length=100)
    new_password: str = Field(min_length=1, max_length=100)
