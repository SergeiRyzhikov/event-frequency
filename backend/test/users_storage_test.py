import json
import random
import unittest
import sys

import pytest



sys.path.append('D:/programms/project AiP/backend')

from storage.users import InFileUserStorage
from models.base import Date, Event, SavedUser
from models.outs import User
from models.ins import CreateUser


class Test_InFileUserStorage(unittest.TestCase):

    user_storage = InFileUserStorage()

    def test_get_user_correct(self):
        user = self.user_storage.get_user('test')
        self.assertEqual(user,  SavedUser(userName='test', password='testtest'))

    def test_get_user_not_exists(self):
        user = self.user_storage.get_user('этого пользователя не существует')
        self.assertEqual(user,  SavedUser(userName='', password=''))

    def test_get_user_incorrect(self):
        with pytest.raises(TypeError):
            self.user_storage.get_user([1488])
       
    
    def test_create_user_correct(self):
        user_name_random = str(random.randint(100000, 10000000))
        self.user_storage.create_user(CreateUser(userName=user_name_random, password='123456'))
        
        self.assertEqual(self.user_storage.get_user(user_name_random),  SavedUser(userName=user_name_random, password='123456'))
    
    def test_create_user_incorrect(self):
        with pytest.raises(AttributeError):
            self.user_storage.create_user({'userName':'пользователь вот такой', 'password':'123456'})
        