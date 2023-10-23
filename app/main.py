import asyncio
from fastapi import FastAPI
from app.controllers.router import router
from app.db.db import database
from app.services.scheduler import runner
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

description = """

You will be able to:

* **Create Events** (_implemented_).
* **Read Events** (_implemented_).
* **Update Events** (_implemented_).
* **Delete Events** (_implemented_).
"""

limiter = Limiter(key_func=get_remote_address, application_limits=["10/5seconds"])

app = FastAPI(title="EventManager",
    description=description,
    summary="A Home Excercise",
    version="0.0.1",)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware) ## Rate-limit all request

@app.get("/")
async def read_root():
    return {"message": "I Am Alive!"}


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    asyncio.create_task(runner.run_main())

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

app.include_router(router)