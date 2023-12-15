from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Union
import json

from models.outs import IsDelete, User
from models.base import Event, SavedEvent


def write_events(events: list[SavedEvent]) -> None:
    """ 
    Write events in file

    :param events: The events to write in file 
    :type url: list[SavedEvent]
    :returns: -
    :rtype: None
    """
    with open('D:/programms/project AiP/backend/storage/eventsStorage.json', 'w') as eventFile:
        eventFile.write(json.dumps(events))

class EventStorage(ABC):
    @abstractmethod
    def create_event(self, user: User, event: Event) -> None:
        pass

    @abstractmethod
    def get_events(self, user: User) -> Union[dict, None]:
        pass

    @abstractmethod
    def delete_event(self, user: User) -> IsDelete:
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
        eventFile = open('D:/programms/project AiP/backend/storage/eventsStorage.json', 'r')
        events = json.loads(eventFile.read())
        eventFile.close()

        all_events = events.get(user.userName)

        if all_events:
            all_events = events[user.userName]
            for i in range(len(all_events)):
                if all_events[i]['name']==event.name:
                    all_events[i]['time'].append(event.time.model_dump())
                    break
            else:
                all_events.append({'name':event.name, 'time':[event.time.model_dump()]})
        else:
            events[user.userName] = [{'name':event.name, 'time':[event.time.model_dump()]}]
            
        write_events(events)
            
    def get_events(self, user: User) -> Union[list[SavedEvent], None]:
        with open('D:/programms/project AiP/backend/storage/eventsStorage.json') as eventFile:
            events = json.loads(eventFile.read())

        return events.get(user.userName)

        
    def delete_event(self, user: User, event: Event) -> IsDelete:

        with open('D:/programms/project AiP/backend/storage/eventsStorage.json') as eventFile:
            events = json.loads(eventFile.read())
        user_events =  events.get(user.userName)
        if not user_events:
            return IsDelete(isDelete=False)
        
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
                        
                        return IsDelete(isDelete=True)
        return IsDelete(isDelete=False)
