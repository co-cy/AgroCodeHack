from app.schemas.user.create_user import CreateUser
from app.database.tables.user import User
from fastapi import APIRouter, Depends
from app.database import get_session
from sqlalchemy.future import select
from fastapi import HTTPException

router = APIRouter()


@router.post("/reg")
@router.post("/registration")
async def registration(user_info: CreateUser, db_session=Depends(get_session)):
    login = user_info.login

    query = select(User).where(User.login == login).limit(1)
    find_user = (await db_session.scalars(query))

    if any(find_user):
        raise HTTPException(status_code=422, detail="Login is not unique")

    new_user = User(login=login, password=user_info.password)

    db_session.add(new_user)
    await db_session.commit()

    return new_user
