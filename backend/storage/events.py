import json
from typing import Union
from abc import ABC, abstractmethod

from models.outs import IsDelete, User
from models.base import Event, SavedEvent

def write_events(events: list[SavedEvent]) -> None:
    """ 
    Write events in file

    :param events: The events to write in file 
    :type url: list[SavedEvent]
    """
    with open('storage/eventsStorage.json', 'w') as eventFile:
        eventFile.write(json.dumps(events))

class EventStorage(ABC):
    """
    Abstract base class for event storage.

    This class defines the interface for managing event data.
    Subclasses should implement methods to create, retrieve, and delete events.
    """

    @abstractmethod
    def create_event(self, user: User, event: Event) -> None:
        """
        Create a new event and associate it with the user.

        :param user: User for whom the event is created.
        :type user: User
        :param event: Event information to be created.
        :type event: Event
        """
        pass

    @abstractmethod
    def get_events(self, user: User) -> Union[dict, None]:
        """
        Retrieve a list of events associated with the user.

        :param user: User for whom events are retrieved.
        :type user: User
        :returns: A list of user's events, or None if no events are found.
        :rtype: list[SavedEvent] or None
        """
        pass

    @abstractmethod
    def delete_event(self, user: User) -> IsDelete:
        """
        Delete an event associated with the user.

        :param user: User for whom the event is deleted.
        :type user: User
        :param event: Event information to be deleted.
        :type event: Event
        :returns: IsDelete object indicating whether the event is deleted.
        :rtype: IsDelete
        """
        pass
        
class InFileEventStorage(EventStorage):
    """
    Implementation of EventStorage that stores event data in a JSON file.
    """

    def create_event(self, user: User, event: Event) -> None:
        """
        Create a new event and associate it with the user, then store it in the JSON file.

        :param user: User for whom the event is created.
        :type user: User
        :param event: Event information to be created.
        :type event: Event
        """
        eventFile = open('storage/eventsStorage.json', 'r')
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
        """
        Retrieve a list of events associated with the user from the JSON file.

        :param user: User for whom events are retrieved.
        :type user: User
        :returns: A list of user's events, or None if no events are found.
        :rtype: list[SavedEvent] or None
        """
        with open('storage/eventsStorage.json') as eventFile:
            events = json.loads(eventFile.read())

        return events.get(user.userName)

        
    def delete_event(self, user: User, event: Event) -> IsDelete:
        """
        Delete an event associated with the user from the JSON file.

        :param user: User for whom the event is deleted.
        :type user: User
        :param event: Event information to be deleted.
        :type event: Event
        :returns: IsDelete object indicating whether the event is deleted.
        :rtype: IsDelete
        """
        with open('storage/eventsStorage.json') as eventFile:
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