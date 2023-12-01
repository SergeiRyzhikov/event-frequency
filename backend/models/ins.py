from pydantic import BaseModel

from models.base import Event

class CreateUser(BaseModel):
    userName: str
    password: str

class Token(BaseModel):
    token: str

class CreateToken(CreateUser):
    pass

class CreateEvent(BaseModel):
    token: Token
    event:  Event

class DeleteEvent(CreateEvent):
    pass
