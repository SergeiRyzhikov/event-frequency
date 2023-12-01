from fastapi import FastAPI, HTTPException
from typing import Union
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from models.base import SavedEvent
from storage.events import InFileEventStorage
from models.ins import CreateEvent, CreateToken, CreateUser, DeleteEvent
from models.outs import Token, User, CreateEventMessage
from storage.users import InFileUserStorage


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


userStorage = InFileUserStorage()

eventStorage = InFileEventStorage()


def get_user_from_token(token: Token)->User:
    return User(userName=token.token[8:])

@app.get('/')
def get_text():
    return 'hello world'


# Регистриция
@app.post('/api/users', response_model=User)
def create_user(user: CreateUser):
    print(userStorage.get_user(user.userName))
    if userStorage.get_user(user.userName).userName:
        raise HTTPException(404, f'user already exists ')
    else:
        userStorage.create_user(user)
        return user
    
# авторизация
@app.post('/api/users/token', response_model=Token)
def get_token(user: CreateToken):
    u = userStorage.get_user(user.userName)
    if u.userName:
        if u.password == user.password:
            return  Token(token= f'token - {user.userName}')
        else:
            raise HTTPException(404, 'password is incorrect')
    else:
        raise HTTPException(404, f'username is incorrect{u}')

        
@app.post('/api/users/me', response_model=User) 
def get_user(token:Token):
    user =  get_user_from_token(token)
    return user

@app.post('/api/create_event', response_model=CreateEventMessage) 
def create_event(item: CreateEvent):
    user_name =  get_user_from_token(item.token)
    eventStorage.create_event(user_name, item.event)
    
    return {'message': 'all cool'}

@app.post('/api/events/me', response_model = Union[List[SavedEvent], None]) 
def get_events(token:Token):
    
    user_name =  get_user_from_token(token)

    events = eventStorage.get_events(user_name)

    return events

@app.post('/api/delete_event', response_model = bool) 
def delete_event(item: DeleteEvent):
    
    user_name =  get_user_from_token(item.token)
    isDelete = eventStorage.delete_event(user_name, item.event)

    return isDelete