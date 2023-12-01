from abc import ABC, abstractmethod
from collections import defaultdict
import json
from typing import Union
from pydantic import BaseModel
from models.base import SavedUser

from models.ins import CreateUser


class UserStorage(ABC):
    @abstractmethod
    def create_user(self, new_user: CreateUser) -> None:
        pass

    @abstractmethod
    def get_user(self, userName: str) -> SavedUser:
        pass

class InMemoryUserStorage(UserStorage):
    def __init__(self) -> None:
        self._users: dict[CreateUser.userName, CreateUser] = defaultdict()
    
    def create_user(self, new_user: CreateUser) -> None:
        user_name = new_user.userName
        if all(user.userName!=user_name for user in self._users.values()):
            self._users[user_name]=new_user

    
    def get_user(self, userName: str) -> Union[SavedUser, None]:
        try:
            return self._users[userName]
        except KeyError:
            return None
        


class InFileUserStorage(UserStorage):
    def __init__(self) -> None:
        self._users: dict[CreateUser.userName, CreateUser] = defaultdict()
    
    def create_user(self, new_user: CreateUser) -> None:
        eventFile = open('D:/programms/проект АиП 2/backend/storage/users.json', 'r')
        users = json.loads(eventFile.read())
        eventFile.close()
        user_name = new_user.userName
        if all(user['userName']!=user_name for user in users.values()):
            users[user_name]=new_user.model_dump()
            with open('D:/programms/проект АиП 2/backend/storage/users.json', 'w') as eventFile:
                print(users)
                eventFile.write(json.dumps(users))

    
    def get_user(self, userName: str) -> SavedUser:
        with open('D:/programms/проект АиП 2/backend/storage/users.json') as eventFile:
            users = json.loads(eventFile.read())
        try:
            current_user = users[userName]
            return SavedUser.model_validate(current_user)
        except KeyError:
            return SavedUser(userName= '', password= '')
    