from typing import Annotated

from config import setting
from db.db import get_async_session
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from models.users import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix=f"{setting.BASE_URI}/tests",
    redirect_slashes=False,
    tags=["tests"],
)


@router.get("")
async def get_tests(
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    stmt = select(User).filter_by(api_key="test")
    res = await session.execute(stmt)
    row = res.scalars().one_or_none()
    if row is not None:
        print(row)
        return {"result": True}
    raise HTTPException(status_code=404, detail={"result": False})
