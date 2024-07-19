import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from report.routers import report_endpoints
from report.services.consumer import PikaConsumer


async def startup():
    loop = asyncio.get_event_loop()
    task = loop.create_task(pika_consumer.consume(loop))
    await task


app = FastAPI()
pika_consumer = PikaConsumer()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(report_endpoints.router, prefix="/report")
app.add_event_handler("startup", startup)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8200, reload=True)
