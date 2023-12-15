from fastapi import FastAPI, HTTPException
from typing import Union
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from models.base import SavedEvent
from storage.events import InFileEventStorage
from models.ins import CreateEvent, CreateToken, CreateUser, DeleteEvent
from models.outs import IsDelete, Token, User, CreateEventMessage
from storage.users import InFileUserStorage


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
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
    """
    Get user information based on a provided authentication token.

    :param token: The authentication token
    :type token: Token
    :returns: User information associated with the token
    :rtype: User
    """
    return User(userName=token.token[8:])

# Регистриция
@app.post('/api/users', response_model=User)
def create_user(user: CreateUser):
    """
    Create a new user.

    :param user: User information for registration.
    :type user: CreateUser
    :returns: Newly created user.
    :rtype: User
    :raises HTTPException 400: If the user already exists.
    """
    print(userStorage.get_user(user.userName))
    if userStorage.get_user(user.userName).userName:
        raise HTTPException(400, f'user already exists')
    else:
        userStorage.create_user(user)
        return user
    
# авторизация
@app.post('/api/users/token', response_model=Token)
def get_token(user: CreateToken):
    """
    Authenticate a user and return an authentication token.

    :param user: User credentials for authentication.
    :type user: CreateToken
    :returns: Authentication token if authentication is successful.
    :rtype: Token
    :raises HTTPException 404: If the username or password is incorrect.
    """
    u = userStorage.get_user(user.userName)
    if u.userName:
        if u.password == user.password:
            return  Token(token= f'token - {user.userName}')
        else:
            raise HTTPException(404, 'password is incorrect')
    else:
        raise HTTPException(404, 'username is incorrect')

        
@app.post('/api/users/me', response_model=User) 
def get_user(token:Token):
    """
    Get user information based on the provided authentication token.

    :param token: The authentication token.
    :type token: Token
    :returns: User information associated with the token.
    :rtype: User
    """
    user =  get_user_from_token(token)
    return user

@app.post('/api/create_event', response_model=CreateEventMessage) 
def create_event(item: CreateEvent):
    """
    Create a new event for a user.

    :param item: Event information to be created.
    :type item: CreateEvent
    :returns: A message indicating the success of event creation.
    :rtype: CreateEventMessage
    """
    user_name =  get_user_from_token(item.token)
    eventStorage.create_event(user_name, item.event)
    
    return CreateEventMessage(message='all cool')

@app.post('/api/events/me', response_model = Union[List[SavedEvent], None]) 
def get_events(token:Token):
    """
    Get a list of events associated with the user.

    :param token: The authentication token.
    :type token: Token
    :returns: A list of user's events, or None if no events are found.
    :rtype: list or None
    """
    
    user_name =  get_user_from_token(token)

    events = eventStorage.get_events(user_name)

    return events

@app.post('/api/delete_event', response_model = IsDelete) 
def delete_event(item: DeleteEvent):
    """
    Delete an event associated with the user.

    :param item: Information about the event to be deleted.
    :type item: DeleteEvent
    :returns: True if the event is deleted, False otherwise.
    :rtype: IsDelete
    """
    user_name =  get_user_from_token(item.token)
    isDelete = eventStorage.delete_event(user_name, item.event)

    return isDelete