import databases
import ormar
import datetime
import sqlalchemy
from typing import Optional, List
from ormar import post_delete, post_update
from .utils import send_email
from app.config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()

class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Event(ormar.Model):
    class Meta(BaseMeta):
        tablename = "events"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=128, unique=False, nullable=False)
    participants: int = ormar.Integer(default=0, maximum=5000, unique=False, nullable=True)
    date: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    location: str = ormar.String(max_length=128, unique=False, nullable=False)
    venue: str = ormar.String(max_length=128, unique=False, nullable=False)
    created: datetime.datetime = ormar.DateTime(default=datetime.datetime.now)
    
    
class Subscriber(ormar.Model):
    class Meta(BaseMeta):
        tablename = "subscribers"
    
    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=128, unique=False, nullable=False)
    events: Optional[List[Event]] = ormar.ManyToMany(Event)
    
    
@post_update(Event)
async def after_update(sender, instance, **kwargs):
    id = instance.id
    subscribers = Subscriber.objects.filter(events__id__in=[id]).all()
    for subscriber in subscribers:
        send_email(subscriber.email, instance.name)
        
@post_delete(Event)
async def after_delete(sender, instance, **kwargs):
    id = instance.id
    subscribers = Subscriber.objects.filter(events__id__in=[id]).all()
    for subscriber in subscribers:
        send_email(subscriber.email, instance.name)
        

engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)