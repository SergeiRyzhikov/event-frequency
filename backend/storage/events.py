from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Union
import json

from models.outs import User
from models.base import Event, SavedEvent


def write_events(events):
    with open('D:/programms/проект АиП 2/backend/storage/events.json', 'w') as eventFile:
        eventFile.write(json.dumps(events))

class EventStorage(ABC):
    @abstractmethod
    def create_event(self, user: User, event: Event) -> None:
        pass

    @abstractmethod
    def get_events(self, user: User) -> Union[dict, None]:
        pass

    @abstractmethod
    def delete_event(self, user: User) -> bool:
        pass

class InMemoryEventStorage(EventStorage):
    def __init__(self) -> None:
        self._events: dict[User.userName, list[SavedEvent]] = defaultdict()
    
    def create_event(self, user: User, event: Event) -> None:
        user_name = user.userName
        try: 
            all_events = self._events[user_name]
            for i in range(len(all_events)):
                if all_events[i]['name']==event.name:
                    print(event.name)
                    all_events[i]['time'].append(event.time)
                    break
            else:
                all_events.append({'name':event.name, 'time':[event.time]})
        except KeyError:
            self._events[user_name] = [{'name':event.name, 'time':[event.time]}]
            
    def get_events(self, user: User, event: Event) -> Union[list[SavedEvent], None]:
        try:
            return self._events[user.userName]
        except:
            return None
        
class InFileEventStorage(EventStorage):
    def __init__(self) -> None:
        self._events: dict[User.userName, list[SavedEvent]] = defaultdict()

    
    def create_event(self, user: User, event: Event) -> None:
        eventFile = open('D:/programms/проект АиП 2/backend/storage/events.json', 'r')
        events = json.loads(eventFile.read())
        eventFile.close()

        user_name = user.userName
        try: 
            all_events = events[user_name]
            for i in range(len(all_events)):
                if all_events[i]['name']==event.name:
                    print(event.name)
                    all_events[i]['time'].append(event.time.model_dump())
                    break
            else:
                all_events.append({'name':event.name, 'time':[event.time.model_dump()]})
        except KeyError:
            events[user_name] = [{'name':event.name, 'time':[event.time.model_dump()]}]
            
        write_events(events)
            
    def get_events(self, user: User) -> Union[list[SavedEvent], None]:
        with open('D:/programms/проект АиП 2/backend/storage/events.json') as eventFile:
            events = json.loads(eventFile.read())
        try:
            return events[user.userName]
        except KeyError:
            return None
        
    def delete_event(self, user: User, event: Event) -> bool:

        with open('D:/programms/проект АиП 2/backend/storage/events.json') as eventFile:
            events = json.loads(eventFile.read())

        try:
            user_events =  events[user.userName]
        except KeyError:
            return False
        
        for t, user_event in enumerate(user_events):
            if user_event['name']==event.name:
                date1 = user_event['time']
                date2 = event.time
                for i in range(len(date1)):
                    if date1[i]==date2.model_dump():
                        if len(date1)==1:
                            events[user.userName].pop(t)
                        else:
                            events[user.userName][t]['time'].pop(i)
                        write_events(events)
                        
                        return True
        return False
