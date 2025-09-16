from dependency_injector import containers, providers

from bases import base_llm_client
from config import llm_config
from llm_clients import gigachat_client


class LLMContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["services"])

    gigachat_client: base_llm_client.BaseLLMClient = providers.Factory(
        gigachat_client.GigaChatClient,
        api_key=llm_config.llm_config.llm_api_key,
        base_url=llm_config.llm_config.llm_api_base,
        model=llm_config.llm_config.llm_model_name
    )
