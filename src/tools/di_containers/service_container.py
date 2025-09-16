from dependency_injector import containers, providers

from bases.services import (
    horoscope_service as base_horoscope_service,
    gigachat_llm_service,
    user_service as base_user_service
)
from services import (
    horoscope_service as horoscope_service_,
    gigachat_service as gigachat_service_,
    user_service as user_service_
)


class ServiceContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["api"])

    horoscope_service: base_horoscope_service.HoroscopeService = providers.Factory(
        horoscope_service_.HoroscopeService
    )
    user_service: base_user_service.UserService = providers.Factory(user_service_.UserService)
    gigachat_service: gigachat_llm_service.GigaChatLLMService = providers.Factory(
        gigachat_service_.GigaChatService
    )
