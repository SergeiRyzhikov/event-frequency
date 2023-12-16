import json
import random
import unittest

from fastapi.testclient import TestClient
import pytest

from storage.events import InFileEventStorage, write_events
from models.base import Date, Event, SavedUser
from models.outs import User, Token
from storage.users import InFileUserStorage
from models.ins import CreateUser
from main import get_user_from_token, app

client = TestClient(app)

def test_create_user_correct_data():
    userName = f'{random.randint(10000000000, 1000000000000000000)}'
    data = {'userName': userName, 'password': '12345678'}
    response = client.post('/api/users', json=data)

    assert response.status_code == 200
    assert response.json() == {'userName': userName}


def test_create_user_exists():
    data = {'userName': 'sergei', 'password': '12345678'}
    response = client.post('/api/users', json=data)

    assert response.status_code == 400
    assert response.json() == {'detail': 'User sergei already exists'}


def test_get_token_correct_data():
    data = {'userName': 'sergei', 'password': 'string'}
    response = client.post('/api/users/token', json=data)

    assert response.status_code == 200
    assert response.json() == {'token': 'token - sergei'}


def test_get_token_incorrect_username():
    data = {'userName': 'АНАТОЛИЙ', 'password': 'string'}
    response = client.post('/api/users/token', json=data)

    assert response.status_code == 404
    assert response.json() == {'detail': 'username is incorrect'}


def test_get_token_incorrect_password():
    data = {'userName': 'sergei', 'password': 'incorrect'}
    response = client.post('/api/users/token', json=data)

    assert response.status_code == 404
    assert response.json() == {'detail': 'password is incorrect'}


def test_get_user_correct_data():
    data = {'token': 'token - sergei'}
    response = client.post('/api/users/me', json=data)

    assert response.status_code == 200
    assert response.json() == {'userName': 'sergei'}


def test_get_events_correct_data():
    data = {'token': 'token - test'}
    data_check = [{'name': 'тестовое событие', "time": [{'year': 2023, 'month': 12, 'day': 6, 'hour': 23, 'minute': 30}]}]
    response = client.post('/api/events/me', json={'token': 'token - test'})

    assert response.status_code == 200
    assert response.json() == data_check


def test_get_user_incorrect_data():
    data = {'whatblin': 'token - sergei'}
    response = client.post('/api/users/me', json=data)

    assert response.status_code == 422


def test_create_event_correct_data():
    response = client.post('/api/create_event', json={'token': {'token': 'token - sergei'}, 'event': {'name': 'плакал', 'time': {'year': 2000, 'month': 12, 'day': 25, 'hour': 23, 'minute': 0}}})

    assert response.status_code == 200
    assert response.json() == {'message': 'all cool'}


def test_create_event_incorrect_data():
    response = client.post('/api/create_event', json={'tn': {'token': 'token - sergei'}, 'time': {'year': 2000, 'month': 12, 'day': 25, 'hour': 23, 'minute': 0}})

    assert response.status_code == 422


def test_delete_event_correct_data_positive():
    response = client.post('/api/delete_event', json={'token': {'token': 'token - sergei'}, 'event': {'name': 'плакал', 'time': {'year': 2000, 'month': 12, 'day': 25, 'hour': 23, 'minute': 0}}})

    assert response.status_code == 200
    assert response.json() == {'isDelete': True}


def test_delete_event_correct_data_negative():
    response = client.post('/api/delete_event', json={'token': {'token': 'token - sergei'}, 'event': {'name': 'плакал', 'time': {'year': 1900, 'month': 12, 'day': 25, 'hour': 23, 'minute': 0}}})

    assert response.status_code == 200
    assert response.json() == {'isDelete': False}


def test_delete_event_incorrect_data():
    response = client.post('/api/delete_event', json={'pppppp': {'token': 'token - sergei'}, 'event': {'name': 'плакал', 'time': {'year': 1900, 'month': 12, 'day': 25, 'hour': 23, 'minute': 0}}})

    assert response.status_code == 422


class Get_user_from_token_test(unittest.TestCase):

    def test_get_user_from_token_correct(self):
        self.assertEqual(get_user_from_token(Token(token='token - sergei')), User(userName='sergei'))

    def test_get_user_from_token_incorrect(self):
        self.assertEqual(get_user_from_token(Token(token='')), User(userName=''))

    def test_attribute_error(self):
        with pytest.raises(AttributeError):
            self.assertEqual(get_user_from_token('token - sergei'), User(userName=''))


class Write_events_test(unittest.TestCase):

    def test_write_events_correct_data(self):
        with open('storage/eventsStorage.json', 'r') as eventFile:
            events = json.loads(eventFile.read())

        write_events(events)

        with open('storage/eventsStorage.json', 'r') as eventFile:
            new_events = json.loads(eventFile.read())

        self.assertEqual(events, new_events)


class Test_InFileEventStorage(unittest.TestCase):

    event_storage = InFileEventStorage()

    def test_create_event_correct(self):
        events = self.event_storage.get_events(User(userName='test'))
        self.assertEqual(events, [{'name': 'тестовое событие', 'time': [{'year': 2023, 'month': 12, 'day': 6, 'hour': 23, 'minute': 30}]}])

    def test_create_event_incorrecct(self):
        with pytest.raises(AttributeError):
            self.event_storage.get_events({'userName': 'test'})

    def test_delete_event(self):
        event = Event(name='dd', time=Date(year=2023, month=2, day=23, hour=2, minute=0))
        user = User(userName='такого пользователя не существует')

        isDelete = self.event_storage.delete_event(user, event)
        self.assertEqual(isDelete.isDelete, False)

    def test_delete_event_incorrecct(self):
        with pytest.raises(AttributeError):
            self.event_storage.delete_event({'userName': 'test'}, 'event')

    def test_get_event_incorrecct(self):
        with pytest.raises(AttributeError):
            self.event_storage.get_events({'userName': 'test'})


class Test_InFileUserStorage(unittest.TestCase):

    user_storage = InFileUserStorage()

    def test_get_user_correct(self):
        user = self.user_storage.get_user('test')
        self.assertEqual(user, SavedUser(userName='test', password='testtest'))

    def test_get_user_not_exists(self):
        user = self.user_storage.get_user('этого пользователя не существует')
        self.assertEqual(user, SavedUser(userName='', password=''))

    def test_get_user_incorrect(self):
        with pytest.raises(TypeError):
            self.user_storage.get_user([1488])

    def test_create_user_correct(self):
        user_name_random = str(random.randint(100000, 10000000))
        self.user_storage.create_user(CreateUser(userName=user_name_random, password='123456'))

        self.assertEqual(self.user_storage.get_user(user_name_random), SavedUser(userName=user_name_random, password='123456'))

    def test_create_user_incorrect(self):
        with pytest.raises(AttributeError):
            self.user_storage.create_user({'userName': 'пользователь вот такой', 'password': '123456'})
