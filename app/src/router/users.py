import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src import models, schemas
from src.database import get_db


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=List[schemas.UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User))
    return result.scalars().all()


@router.get("/{account_id}", response_model=schemas.UserResponse)
async def get_user(account_id: int, db: AsyncSession = Depends(get_db)):
    query = select(models.User).where(models.User.account_id == account_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/", response_model=schemas.UserResponse)
async def create_user(
    user_create: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
    response: Response = None
):
    ins_stmt = (
        insert(models.User)
        .values(**user_create.model_dump())
        .on_conflict_do_nothing(index_elements=["account_id"])
        .returning(models.User)
    )

    result = await db.execute(ins_stmt)
    new_user = result.scalar_one_or_none()

    if new_user is None:
        logger.warning("User already exists; returning an existing user")
        query = select(models.User).where(models.User.account_id == user_create.account_id)
        result = await db.execute(query)
        new_user = result.scalar_one()
        response.status_code = status.HTTP_200_OK
    else:
        response.status_code = status.HTTP_201_CREATED

    await db.commit()
    return new_user


@router.get("/{account_id}/reports", response_model=List[schemas.ReportResponse])
async def get_user_reports(account_id: int, db: AsyncSession = Depends(get_db)):
    user_query = select(models.User).where(models.User.account_id == account_id)
    user_result = await db.execute(user_query)
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    reports_query = (
        select(models.Report)
        .where(models.Report.account_id == account_id)
        .order_by(models.Report.created_at.desc())
    )
    reports_result = await db.execute(reports_query)
    return reports_result.scalars().all()