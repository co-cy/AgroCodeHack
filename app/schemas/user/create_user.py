from pydantic import BaseModel, validator


class CreateUser(BaseModel):
    login: str
    password: str

    @validator("login")
    def validator_login(cls, login: str):
        if 128 < len(login) < 1:
            raise ValueError("Login length is not within [1, 128]")

        return login

    @validator("password")
    def validator_password(cls, password: str):
        if 128 < len(password) < 1:
            raise ValueError("Password length is not within [1, 128]")

        return password
