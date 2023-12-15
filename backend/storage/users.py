import json

from abc import ABC, abstractmethod
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
    def get_user(self, user_name: str) -> SavedUser:
        """
        Retrieve user information based on the username.

        :param user_name: The username of the user to retrieve.
        :type user_name: str
        :return: User information if found, or an empty SavedUser if not found.
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

        event_file = open('storage/usersStorage.json', 'r')
        users = json.loads(event_file.read())
        event_file.close()
        user_name = new_user.userName
        if all(user['userName'] != user_name for user in users.values()):
            users[user_name] = new_user.model_dump()
            with open('storage/usersStorage.json', 'w') as event_file:
                event_file.write(json.dumps(users))

    def get_user(self, user_name: str) -> SavedUser:
        """
        Retrieve user information based on the username.

        :param user_name: The username of the user to retrieve.
        :type user_name: str
        :returns: User information if found, or an empty SavedUser if not found.
        :rtype: SavedUser
        """

        with open('storage/usersStorage.json') as event_file:
            users = json.loads(event_file.read())

        current_user = users.get(user_name)
        if current_user:
            return SavedUser.model_validate(current_user)
        else:
            return SavedUser(userName='', password='')
