from enum import Enum
from pydantic import BaseModel

class OrderBy(str, Enum):
    date = "date"
    participants = "participants"
    created = "created"


class ItemQueryParams(BaseModel):
    order_by: OrderBy = OrderBy.date
    descending: bool = False