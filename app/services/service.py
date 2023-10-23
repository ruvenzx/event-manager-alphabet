import datetime
from typing import List
from app.db.db import Event
from ormar.exceptions import NoMatch
from app.controllers.scheme import CreateOrUpdateEvent

class Service():
    
    async def get_all(self, location=None, venue=None, params=None) -> List[Event]:
        ### Gets all events in db ###
        ### Sorry for dumb implementation - could not make both filters work altogether ###
        query = Event.objects
        if params:
            order_column = params.order_by
            if params.descending:
                order_column = '-' + order_column
            query = Event.objects.order_by(order_column)
        if location:
            if venue:
                query = query.filter(location=location, venue=venue)
            else:
                query = query.filter(location=location)
        elif venue:
            if location:
                query = query.filter(location=location, venue=venue)
            else:
                query = query.filter(venue=venue)
        
        return await query.all()
    
            
    async def get_by_ids(self, ids: List[int]) -> List[Event]:
        ### Gets items by their ids ###
            try:
                result = await Event.objects.filter(id__in=ids).all()
                return result
            except NoMatch:
                return None
            
    
    async def get_by_id(self, id: int) -> Event:
        ### Gets an item by id ###
        try:
            result = await Event.objects.get(id=id)
            return result
        except NoMatch:
            return None
        
    
    async def create_event(self, event: CreateOrUpdateEvent) -> Event:
    ### Creates Event in db ###
        result = await Event.objects.create(name=event.name, location=event.location, venue=event.venue, date=datetime.datetime.fromtimestamp(event.date), participants=event.participants)
        return await self.get_by_id(result.id)
    
    
    async def batch_create_events(self, events) -> List[Event]:
    ### Batch creates events in db ###
        result = await Event.objects.bulk_create(events)
        ids = list(map(lambda element: result.id))
        return self.get_by_ids(ids)
    
        
    async def batch_update_events(self, events) -> List[Event]:
    ### Batch updates events in db ###
        ids = [int(event.id) for event in events]
        stored_events = await self.get_by_ids(ids)
        event_dict = {int(x.id): x for x in events}
        for event in stored_events:
            selected_object = event_dict.get(event.id)
            if selected_object:
                print(event)
                event.name = selected_object.name
                event.location = selected_object.location
                event.venue = selected_object.venue
                event.date = datetime.datetime.fromtimestamp(selected_object.date)
                event.participants = selected_object.participants
        await Event.objects.bulk_update(stored_events)
        return await self.get_by_ids(ids)
    
    
    async def update_event(self, id: int, event: CreateOrUpdateEvent) -> Event:
    ### Updates Event in db ###
        await Event.objects.filter(id=id).update(name=event.name, location=event.location, venue=event.venue, date=datetime.datetime.fromtimestamp(event.date), participants=event.participants)
        
        return await self.get_by_id(id)
    
    
    async def batch_delete_events(self, ids: List[int]) -> List[Event]:
        ### Deletes items by their ids ###
        result = await self.get_by_ids(ids)
        
        if result:
            Event.objects.filter(id__in=ids).delete()
            return result
        else:
            return None
        
    
    async def delete_event(self, id: int) -> Event:
    ### Deletes Event in db ###
        result = await self.get_by_id(id)
        
        if result:
            await Event.objects.delete(id=id)
            return result
        else:
            return None
            
service = Service()