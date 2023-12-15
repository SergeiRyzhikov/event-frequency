from abc import ABC, abstractmethod
from collections import defaultdict
import json
from typing import Union
from models.base import SavedUser
from models.ins import CreateUser


class UserStorage(ABC):
    """
    Abstract base class for user storage.

    This class defines the interface for managing user data.
    Subclasses should implement the methods to create and retrieve user data.
    """

    @abstractmethod
    def create_user(self, new_user: CreateUser) -> None:
        """
        Create a new user.

        :param new_user: User information to be created.
        :type new_user: CreateUser
        """
        pass

    @abstractmethod
    def get_user(self, userName: str) -> SavedUser:
        """
        Retrieve user information based on the username.

        :param userName: The username of the user to retrieve.
        :type userName: str
        :return: User information if found, or empty SavedUser if not found.
        :rtype: SavedUser
        """
        pass

class InFileUserStorage(UserStorage):
    """
    Implementation of UserStorage that stores user data in a JSON file.
    """
    def create_user(self, new_user: CreateUser) -> None:
        """
        Create a new user and store it in the JSON file.

        :param new_user: User information to be created.
        :type new_user: CreateUser
        """
        eventFile = open('storage/usersStorage.json', 'r')
        users = json.loads(eventFile.read())
        eventFile.close()
        user_name = new_user.userName
        if all(user['userName']!=user_name for user in users.values()):
            users[user_name]=new_user.model_dump()
            with open('storage/usersStorage.json', 'w') as eventFile:
                print(users)
                eventFile.write(json.dumps(users))

    
    def get_user(self, userName: str) -> SavedUser:
        """
        Retrieve user information based on the username.

        :param userName: The username of the user to retrieve.
        :type userName: str
        :returns: User information if found, or empty SavedUser if not found.
        :rtype: SavedUser
        """
        with open('storage/usersStorage.json') as eventFile:
            users = json.loads(eventFile.read())
        
        current_user = users.get(userName)
        if current_user:
            return SavedUser.model_validate(current_user)
        else:
            return SavedUser(userName= '', password= '')