from pydantic import BaseModel

class User(BaseModel):
    userName: str

class Token(BaseModel):
    token: str

class CreateEventMessage(BaseModel):
    message:str

class IsDelete(BaseModel):
    isDelete: bool