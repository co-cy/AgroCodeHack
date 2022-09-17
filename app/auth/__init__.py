from fastapi_jwt import JwtAccessBearer
from app.config import JWTConfig

access_security = JwtAccessBearer(**JWTConfig())
