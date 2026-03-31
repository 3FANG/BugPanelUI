from typing import Union
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

# Импортируем модели, чтобы SQAlchemy знал про них
# В противном случае, таблицы не будут созданы
from src import models
from src.router import users, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Application starting up...")
    
    yield  # This separates startup from shutdown
    
    # Shutdown logic
    print("Application shutting down...")


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(reports.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}