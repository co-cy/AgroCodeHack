from pyliteconf import Config as _Config


class DatabaseConfig(_Config):
    _dialect = "mysql+asyncmy"
    _user = "agrohack"
    _password = "agrohack"
    _db_url = "79.120.76.23:3306/agrohack_del_19_09"

    url = f"{_dialect}://{_user}:{_password}@{_db_url}"


class JWTConfig(_Config):
    secret_key = "agro_code_hack"


class UvicornConfig(_Config):
    host = "0.0.0.0"
    port = 6969
