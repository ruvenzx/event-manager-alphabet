from app.db.db import Subscriber
from ormar.exceptions import NoMatch
from .service import service
class SubscriptionsService():
    
    async def get_by_id(self, id: int) -> Subscriber:
    ### Gets an item by id ###
        try:
            result = await Subscriber.objects.get(id=id)
            return result
        except NoMatch:
            return None
        
    async def find_by_email(self, email) -> Subscriber:
    ### Find by email ###
        try:
            result = await Subscriber.objects.filter(email=email).get()
            return result
        except NoMatch:
            return None
    
    async def create_subscription(self, event_id: int, email: str) -> Subscriber:
    ### Creates Event in db ###
        already_subscribed = await self.find_by_email(email)
        if already_subscribed:
            event = service.get_by_id(event_id)
            already_subscribed.events.append(event)
            await Subscriber.update(id=already_subscribed.id)
            return await self.get_by_id(already_subscribed.id)
        else:    
            result = await Subscriber.objects.create(email=email)
            return await self.get_by_id(result.id)
    

subscriptionsService = SubscriptionsService()