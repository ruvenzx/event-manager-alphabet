import databases
import ormar
import datetime
import sqlalchemy

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

engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)