import json
import unittest
import sys

import pytest


sys.path.append('D:/programms/project AiP/backend')

from storage.events import InFileEventStorage, write_events
from models.base import Date, Event
from models.outs import User

class Write_events_test(unittest.TestCase):
    def test_write_events_correct_data(self):
        with open('D:/programms/project AiP/backend/storage/eventsStorage.json', 'r') as eventFile:
            events = json.loads(eventFile.read())

        write_events(events)
        
        with open('D:/programms/project AiP/backend/storage/eventsStorage.json', 'r') as eventFile:
            new_events = json.loads(eventFile.read())

        self.assertEqual(events, new_events)


class Test_InFileEventStorage(unittest.TestCase):
    event_storage = InFileEventStorage()

    def test_create_event_correct(self):
        events = self.event_storage.get_events(User(userName='test'))
        self.assertEqual(events,  [{'name': 'тестовое событие', 'time': [{'year': 2023, 'month': 12, 'day': 6, 'hour': 23, 'minute': 30}]}])
    
    def test_create_event_incorrecct(self):
        with pytest.raises(AttributeError):
            self.event_storage.get_events({'userName':'test'})

    def test_delete_event(self):
        event = Event(name='dd', time=Date(year=2023, month=2, day=23, hour=2, minute=0))
        user = User(userName='такого пользователя не существует')

        isDelete  = self.event_storage.delete_event(user, event)
        self.assertEqual(isDelete.isDelete, False)

    def test_delete_event_incorrecct(self):
        with pytest.raises(AttributeError):
            self.event_storage.delete_event({'userName':'test'}, 'event')

    def test_get_event_incorrecct(self):
        with pytest.raises(AttributeError):
            self.event_storage.get_events({'userName':'test'})