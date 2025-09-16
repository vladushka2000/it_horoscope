from pydantic import Field
from pydantic_settings import BaseSettings


class IntegrationConfig(BaseSettings):
    horoscope_url: str = Field(title="Хост API гороскопа", default="https://horoscope-app-api.vercel.app/api/v1")


integration_config = IntegrationConfig()
