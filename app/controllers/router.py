from fastapi import APIRouter, HTTPException, Depends
from app.services.service import service
from app.services.subscriptions import subscriptionsService
from app.controllers.scheme import CreateOrUpdateEvent, ResponseSchema, CreateSubscription
from typing import Optional, List
from .utils import ItemQueryParams

router = APIRouter(prefix="/event", tags=["event"])

@router.get("",  response_model=ResponseSchema)
async def get_events(location: Optional[str] = None, venue: Optional[str] = None, params: ItemQueryParams = Depends()):
    res = await service.get_all(location, venue, params)
    return ResponseSchema(result=res, detail='Succesfully Fetched Data')

@router.get("/{id}", response_model=ResponseSchema)
async def get_event_by_id(id: str):
    res = await service.get_by_id(int(id))
    if not res:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return ResponseSchema(result=res, detail='Succesfully Fetched Data')


@router.put("/${id}")
async def update_event(id: str, event: CreateOrUpdateEvent):
    res = await service.update_event(int(id), event)
    return ResponseSchema(result=res, detail='Succesfully Updated Data')

@router.put("/batch")
async def batch_update_event(events: List[CreateOrUpdateEvent]):
    res = await service.batch_update_events(events)
    return ResponseSchema(result=res, detail='Succesfully Updated Data')

@router.post("")
async def create_event(event: CreateOrUpdateEvent):
    res = await service.create_event(event)
    return ResponseSchema(result=res, detail='Succesfully Created Data')

@router.post("/batch")
async def batch_create_event(events: List[CreateOrUpdateEvent]):
    res = await service.batch_create_events(events)
    return ResponseSchema(result=res, detail='Succesfully Created Data')

@router.delete("/${id}")
async def delete_event(id: str):
    res = await service.delete_event(int(id))
    if not res:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return ResponseSchema(result=res, detail='Succesfully Deleted Data')


@router.delete("batch")
async def delete_event(ids: List[int]):
    res = await service.batch_delete_events(ids)
    if not res:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return ResponseSchema(result=res, detail='Succesfully Deleted Data')
    
    
@router.post("/${id}/subscribe")
async def subscribe(id: str, sub: CreateSubscription):
    res = await subscriptionsService.create_subscription(int(id), sub.email)
    return ResponseSchema(result=res, detail='Succesfully Created Data')
