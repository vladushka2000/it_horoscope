from dependency_injector import containers, providers

from bases import base_alchemy_session
from bases.repositories import base_horoscope_repository, base_user_repository
from config import pg_config
from orm import alchemy_session
from orm.repositories import (
    horoscope_repository as horoscope_repository_,
    user_repository as user_repository_
)


class AlchemyContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["services"])

    session: base_alchemy_session.BaseAlchemySession = providers.Factory(
        alchemy_session.AlchemySession, pg_host=pg_config.pg_config.postgres_dsn
    )
    horoscope_repository: base_horoscope_repository.BaseHoroscopeRepository = providers.Factory(
        horoscope_repository_.HoroscopeRepository,
        session_factory=session
    )
    user_repository: base_user_repository.BaseUserRepository = providers.Factory(
        user_repository_.UserRepository,
        session_factory=session
    )
