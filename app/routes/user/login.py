from app.schemas.user.login_user import LoginUser
from app.database.tables.user import User
from fastapi import APIRouter, Depends
from app.database import get_session
from sqlalchemy.future import select
from app.auth import access_security
from fastapi import HTTPException

router = APIRouter()


@router.post("/login")
async def login(user_info: LoginUser, db_session=Depends(get_session)):
    query = select(User).where(User.login == user_info.login, User.password == user_info.password)
    find_user = (await db_session.scalars(query)).first()

    if not find_user:
        raise HTTPException(status_code=422, detail="Login or password is bad")

    new_user: User = find_user
    new_user.token = access_security.create_access_token({
        "login": new_user.login,
        "password": new_user.password
    })

    db_session.add(new_user)
    await db_session.commit()

    return new_user
