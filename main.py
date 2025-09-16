import asyncio
import logging.config
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config import app_config, logger_config
from tools import const

if app_config.app_config.stage == const.Stage.DEV:
    logging.config.dictConfig(logger_config.get_dev_config())
else:
    logging.config.dictConfig(logger_config.get_prod_config())

bot = Bot(token=app_config.app_config.tg_token)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())