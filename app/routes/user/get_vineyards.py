from fastapi import APIRouter, Depends, HTTPException
from app.database.tables.vineyard import Vineyard
from app.schemas.vineyard import Token
from app.database.tables.user import User
from sqlalchemy.orm import selectinload
from app.database import get_session
from sqlalchemy.future import select

router = APIRouter()


@router.post("/getVineyards")
async def get_vineyards(input_data: Token, db_session=Depends(get_session)):
    # TODO: парсить jwt и вытаскивать его id
    # TODO: поменять запрос
    # TODO: вынести в отдельную функцию
    query = select(User).where(User.token == input_data.token).limit(1).options(selectinload(User.vineyards))
    user = (await db_session.execute(query)).first()

    if not user:
        raise HTTPException(status_code=422, detail="Login or password is bad")

    return [value.value for value in user[0].vineyards]
