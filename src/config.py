from os import getenv
from urllib.parse import quote_plus

from pydantic import BaseModel
from pathlib import Path
from yaml import safe_load


def read_yaml(path):
    with open(path, 'r') as stream:
        data = safe_load(stream)

    return data


__PATH_CORE_CONFIG: str = getenv(
    'APP_CONFIG',
    r'config.yaml'
)


class PostgresDB(BaseModel):
    dbname: str
    host: str
    login: str
    port: int
    password: str


class RedisDB(BaseModel):
    host: str
    port: int


class Settings(BaseModel):
    pg: PostgresDB
    redis: RedisDB
    stock: Path = Path(__file__).parent.resolve() / 'simple_images'

conf_data = read_yaml(__PATH_CORE_CONFIG)
config: Settings = Settings(**conf_data)

DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(
    config.pg.login, quote_plus(config.pg.password),
    config.pg.host, config.pg.port, config.pg.dbname
)
