from typing import Dict, Any

from aiogram import types
from aiogram.filters import Filter
from aiogram.types import Message
from dependency_injector.wiring import inject, Provide

from bases.services import user_service
from tools import emoji_checker
from tools.di_containers import service_container


class HtmlEmojiFilter(Filter):
    async def __call__(self, message: types.Message, **kwargs) -> bool:
        if not message.text:
            return False

        return emoji_checker.is_emoji(message.text)


class RegisteredUserFilter(Filter):
    @inject
    async def __call__(
        self,
        message: Message,
        with_message: bool = True,
        user_service_: user_service.UserService = Provide[
            service_container.ServiceContainer.user_service
        ],
        **kwargs
    ) -> bool:
        user_id = message.from_user.id
        user_in_db = await user_service_.get_user(user_id)

        if with_message and user_in_db is None:
            await message.answer(
                text="Кажется мы еще не знакомы...\nЗарегистрируйся по кнопке ниже",
            )

        return user_in_db is not None


async def check_filter(filter_obj: Filter, message: Message, data: Dict[str, Any] = None) -> bool:
    if data is None:
        data = {}

    if hasattr(filter_obj, '__call__'):
        result = await filter_obj(message, data)
        return bool(result)

    return await filter_obj(message, data)
