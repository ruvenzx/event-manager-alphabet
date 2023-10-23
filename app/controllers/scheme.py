from pydantic import BaseModel
from typing import TypeVar, Optional

T = TypeVar('T')

# Assuming Update mechanism is not partial and FE / API users will send whole entity to update it. #
# Also, assuming date is much more convinient sent in epoch time (milliseconds), thus float. #
class CreateOrUpdateEvent(BaseModel):
    id: Optional[str] = None
    name: str
    participants: int
    date: float
    location: str
    venue: str

# Generic Response
class ResponseSchema(BaseModel):
    detail: str
    result: Optional[T] = None