# schemas.py
from pydantic import BaseModel

# User schema
class User(BaseModel):
    id: int
    username: str

# Create post schema (input)
class PostCreate(BaseModel):
    text: str

# Output schema (response)
class Post(BaseModel):
    id: int
    text: str
    owner_id: int

# Like schema
class Like(BaseModel):
    post_id: int
    user_id: int

# Comment schema
class Comment(BaseModel):
    post_id: int
    user_id: int
    text: str
