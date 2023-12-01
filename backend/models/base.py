from pydantic import BaseModel

class Date(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int

class Event(BaseModel):
    name: str
    time: Date

class SavedUser(BaseModel):
    userName: str
    password: str

class SavedEvent(BaseModel):
    name:str
    time: list[Date]