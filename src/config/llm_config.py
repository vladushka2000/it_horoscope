from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings

from tools import const


class LLMConfig(BaseSettings):
    llm_provider: const.LLMProvider = Field(
        description="LLM provider", default=const.LLMProvider.GIGACHAT
    )
    llm_api_key: Optional[str] = Field(description="Токен для LLM", default=None)
    llm_api_base: str = Field(description="Url API, предоставляющего LLM")
    llm_model_name: str = Field(description="Название модели LLM")

    llm_temperature: float = Field(description="Температура", default=0.0)
    llm_top_p_temperature: float = Field(description="Разброс", default=0.9)

    gigachat_auth_key: str = Field(title="Authorization key")


llm_config = LLMConfig()
