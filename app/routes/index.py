from app.database import get_session, AsyncSession
from app.database.tables.user import User
from fastapi import APIRouter, Depends
from sqlalchemy.future import select

router = APIRouter()


@router.get("/")
async def index(db_session: AsyncSession = Depends(get_session)):
    all_user = await db_session.execute(select(User))
    return all_user.scalars().all()
