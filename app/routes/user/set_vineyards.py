from fastapi import APIRouter, Depends, HTTPException
from app.database.tables.vineyard import Vineyard
from app.schemas.vineyard import InputVineyards
from app.database.tables.user import User
from sqlalchemy.orm import selectinload
from app.database import get_session
from sqlalchemy.future import select

router = APIRouter()


@router.post("/setVineyards")
async def set_vineyards(input_data: InputVineyards, db_session=Depends(get_session)):
    query = select(User).where(User.token == input_data.token).limit(1).options(selectinload(User.vineyards))
    user = (await db_session.execute(query)).first()

    if not user:
        raise HTTPException(status_code=422, detail="Login or password is bad")
    user = user[0]

    for vineyard in user.vineyards:
        user.vineyards.remove(vineyard)

    for vineyard in input_data.vineyards:
        user.vineyards.append(Vineyard(value=vineyard))

    db_session.add(user)
    await db_session.commit()

    return "OK"
