from pydantic import Field
from pydantic_settings import BaseSettings

from tools import const


class AppConfig(BaseSettings):
    tg_token: str = Field(title="Токен Telegram")
    stage: const.Stage = Field(title="Ландшафт", default=const.Stage.DEV)


app_config = AppConfig()
