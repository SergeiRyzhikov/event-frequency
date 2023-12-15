import random
import unittest
from fastapi.testclient import TestClient


import sys

sys.path.append('D:/programms/проект АиП 2/backend')

from main import app, get_user_from_token

client = TestClient(app)

def test_create_user_correct_data():
    userName = f'{random.randint(10000000000, 1000000000000000000)}'
    response = client.post('/api/users', json={'userName': userName, 'password': '12345678'})
    assert response.status_code == 200
    assert response.json() == {'userName': userName}

def test_create_user_exists():
    response = client.post('/api/users', json={'userName': 'sergei', 'password': '12345678'})
    
    assert response.status_code == 400
    assert response.json() == {'detail': 'user already exists'}
    
def test_get_token_correct_data():
    response = client.post('/api/users/token', json={'userName': 'sergei', 'password': 'string'})
    
    assert response.status_code == 200
    assert response.json() == {'token': 'token - sergei'}

def test_get_token_incorrect_username():
    response = client.post('/api/users/token', json={'userName': 'АНАТОЛИЙ', 'password': 'string'})
    
    assert response.status_code == 404
    assert response.json() == {'detail': 'username is incorrect'}
     
def test_get_token_incorrect_password():
    response = client.post('/api/users/token', json={'userName': 'sergei', 'password': 'incorrect'})
    
    assert response.status_code == 404
    assert response.json() == {'detail': 'password is incorrect'}
     
def test_get_user_correct_data():
    response = client.post('/api/users/me', json={'token': 'token - sergei'})
    
    assert response.status_code == 200
    assert response.json() == {'userName': 'sergei'}

def test_get_events_correct_data():
    response = client.post('/api/events/me', json={'token': 'token - test'})

    assert response.status_code == 200
    assert response.json() == [{'name': 'тестовое событие', "time": [{"year": 2023, "month": 12, "day": 6, "hour": 23, "minute": 30}]}]

def test_get_user_incorrect_data():
    response = client.post('/api/users/me', json={'whatblin': 'token - sergei'})
    
    assert response.status_code == 422
    
def test_create_event_correct_data():
    response = client.post('/api/create_event', json={'token': {'token': 'token - sergei'}, 'event':{'name':'плакал', 'time': {'year': 2000, 'month': 12, 'day': 25, 'hour': 23, 'minute': 0}}})
    
    assert response.status_code == 200
    assert response.json() == {'message': 'all cool'}
    
def test_create_event_incorrect_data():
    response = client.post('/api/create_event', json={'tn': {'token': 'token - sergei'}, 'time': {'year': 2000, 'month': 12, 'day': 25, 'hour': 23, 'minute': 0}})
    
    assert response.status_code == 422
    
def test_delete_event_correct_data_positive():
    response = client.post('/api/delete_event', json={'token': {'token': 'token - sergei'}, 'event':{'name':'плакал', 'time': {'year': 2000, 'month': 12, 'day': 25, 'hour': 23, 'minute': 0}}})

    assert response.status_code == 200
    assert response.json() == {'isDelete': True}

def test_delete_event_correct_data_negative():
    response = client.post('/api/delete_event', json={'token': {'token': 'token - sergei'}, 'event':{'name':'плакал', 'time': {'year': 1900, 'month': 12, 'day': 25, 'hour': 23, 'minute': 0}}})

    assert response.status_code == 200
    assert response.json() == {'isDelete': False}

def test_delete_event_incorrect_data():
    response = client.post('/api/delete_event', json={'pppppp': {'token': 'token - sergei'}, 'event':{'name':'плакал', 'time': {'year': 1900, 'month': 12, 'day': 25, 'hour': 23, 'minute': 0}}})

    assert response.status_code == 422

class Get_user_from_token_test(unittest.TestCase):
    def get_user_from_token_correct(self):
        self.assertEqual(get_user_from_token('token - sergei'), 'sergei')

    def get_user_from_token_incorrect(self):
        self.assertEqual(get_user_from_token(''), None)
