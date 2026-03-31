import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Чтобы переменные подтягивались при запуске вне контейнера
from dotenv import load_dotenv
load_dotenv()


DB_USER = os.getenv("DATABASE_USERNAME")
DB_PASS = os.getenv("DATABASE_PASSWORD")
DB_HOST = os.getenv("DATABASE_HOST")
DB_NAME = os.getenv("DATABASE_NAME")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# создаём движок
engine = create_async_engine(DATABASE_URL, echo=True)

# создаём сессию
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# базовый класс для моделей
Base = declarative_base()


async def get_db():
    async with async_session_maker() as session:
        yield session