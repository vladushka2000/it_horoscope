import asyncio
import logging.config

import alembic.config
from aiogram import Bot, Dispatcher

from api.handlers import index_handler, hello_handler, horoscope_handler
from config import app_config, logger_config
from tools import const
from tools.di_containers import (
    alchemy_container,
    integration_container,
    llm_container,
    service_container
)

if app_config.app_config.stage == const.Stage.DEV:
    logging.config.dictConfig(logger_config.get_dev_config())
else:
    logging.config.dictConfig(logger_config.get_prod_config())

alchemy_container.AlchemyContainer()
integration_container.IntegrationContainer()
llm_container.LLMContainer()
service_container.ServiceContainer()

alembic_args = [
    "--raiseerr",
    "upgrade",
    "head",
]


async def main():
    bot = Bot(token=app_config.app_config.tg_token)
    dp = Dispatcher()

    dp.include_router(index_handler.router)
    dp.include_router(hello_handler.router)
    dp.include_router(horoscope_handler.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    alembic.config.main(argv=alembic_args)
    asyncio.run(main())
