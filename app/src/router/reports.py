from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src import models, schemas
from src.database import get_db


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/", response_model=List[schemas.ReportResponse])
async def get_reports(db: AsyncSession = Depends(get_db)):
    query = select(models.Report).order_by(models.Report.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{report_id}", response_model=schemas.ReportResponse)
async def get_report(report_id: int, db: AsyncSession = Depends(get_db)):
    query = select(models.Report).where(models.Report.id == report_id)
    result = await db.execute(query)
    report = result.scalar_one_or_none()

    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    return report


@router.post("/", response_model=schemas.ReportResponse)
async def create_report(
    report_create: schemas.ReportCreate,
    db: AsyncSession = Depends(get_db),
    response: Response = None
):
    user_query = select(models.User).where(models.User.account_id == report_create.account_id)
    user_result = await db.execute(user_query)
    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_report = models.Report(**report_create.model_dump())
    db.add(new_report)

    await db.commit()
    await db.refresh(new_report)

    response.status_code = status.HTTP_201_CREATED
    return new_report


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(report_id: int, db: AsyncSession = Depends(get_db)):
    query = select(models.Report).where(models.Report.id == report_id)
    result = await db.execute(query)
    report = result.scalar_one_or_none()

    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    await db.delete(report)
    await db.commit()
    return None