import pytest
from httpx import AsyncClient
from asyncpg.pool import Pool
from asgi_lifespan import LifespanManager
from .fake_asyncpg_pool import FakeAsyncPGPool
from fastapi import FastAPI
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
from app.controllers.scheme import CreateOrUpdateEvent
from app.services.service import Service


### Test Setup - Begin ###
 
@pytest.fixture
def app() -> FastAPI:
    from app.main import app  # local import for testing purpose

    return app

@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initialized_app,
        base_url="http://localhost:8000",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client
        
@pytest.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        app.state.pool = await FakeAsyncPGPool.create_pool(app.state.pool)
        yield app
        
@pytest.fixture
def pool(initialized_app: FastAPI) -> Pool:
    return initialized_app.state.pool
 
@pytest.fixture
def new_event():
    return CreateOrUpdateEvent(
        name="13 bday",
        participants=13,
        date=1698065198,
        location="Tel Aviv",
        venue="Beit Hasmachot"
    )
    
@pytest.fixture
def new_service():
    return Service()
    
### Test Setup - End ###
 
class TestEventRoutes:
    @pytest.mark.asyncio
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.get("/event", json={})
        assert res.status_code != HTTP_404_NOT_FOUND
        
    @pytest.mark.asyncio
    async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post("/event", json={""})
        assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY
 
 
class TestCreateEvents:
    @pytest.mark.asyncio
    async def test_valid_input_creates_event(
        self, app: FastAPI, client: AsyncClient, new_event: CreateOrUpdateEvent
    ) -> None:
        res = await client.post(
            "/event", json=new_event.dict()
        )
        assert res.status_code == HTTP_201_CREATED
 
        created_event = CreateOrUpdateEvent(**res.json())
        assert created_event == new_event
        
class TestService:
    @pytest.mark.asyncio
    async def test_create_event(
        self, app: FastAPI, new_service: Service, new_event: CreateOrUpdateEvent
    ) -> None:
        res = await new_service.create_event(new_event)
        
        assert res.name == "13 bday"