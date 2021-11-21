from app import database
from pydantic import BaseSettings


class Settings(BaseSettings):
    # s n tvr vl pdr ele checa n lst d vrs d ambiente d stm p ver s tm algum vl,s n tvr da erro
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str  # p nss json webtokens
    algorithm: str  # q v assinar nss token
    access_token_expire_minutes: int

    class Config:
        env_file = '.env'


settings = Settings()
