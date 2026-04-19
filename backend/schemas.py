from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
# Auth schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Task schemas
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    owner_id: int

model_config = ConfigDict(from_attributes=True)