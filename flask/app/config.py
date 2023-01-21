from dataclasses import dataclass

from environs import Env


@dataclass
class Config:
    TONAPI_KEY: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int


def load_config():
    env = Env()
    env.read_env()

    return Config(
        TONAPI_KEY=env.str("TONAPI_KEY"),
        REDIS_HOST=env.str("REDIS_HOST"),
        REDIS_PORT=env.int("REDIS_PORT"),
        REDIS_DB=env.int("REDIS_DB")
    )
