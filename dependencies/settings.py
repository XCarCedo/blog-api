from fastapi import Depends
from typing import Annotated
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    secret: str
    alg: str
    access_exp_min: int

    model_config = SettingsConfigDict(env_file="settings.env")

@lru_cache
def get_settings() -> Settings:
    return Settings

SettingsDep = Annotated[Settings, Depends(get_settings)]