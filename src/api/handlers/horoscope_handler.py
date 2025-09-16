from aiogram import Router, F
from aiogram.types import Message
from dependency_injector.wiring import inject, Provide

from api.handlers import index_handler
from api.tools import filters
from bases.services import gigachat_llm_service, horoscope_service, user_service
from tools.di_containers import service_container

router = Router()


@router.message(F.text.lower() == "хочу предсказание!", filters.RegisteredUserFilter())
@inject
async def cmd_horoscope(
    message: Message,
    user_service_: user_service.UserService = Provide[
        service_container.ServiceContainer.user_service
    ],  # noqa
    horoscope_service_: horoscope_service.HoroscopeService = Provide[
        service_container.ServiceContainer.horoscope_service
    ],  # noqa
    llm_service_: gigachat_llm_service.GigaChatLLMService = Provide[
        service_container.ServiceContainer.gigachat_service
    ],  # noqa
):
    user_id = message.from_user.id
    date = message.date.date()
    user_in_db = await user_service_.get_user(user_id)

    await message.answer(text="🔮")
    await message.answer(text="Предсказываю...")

    horoscope_in_db = await horoscope_service_.get_horoscope(user_id, date)

    if horoscope_in_db:
        return await message.answer(text=horoscope_in_db.predict)

    original_horoscope = await horoscope_service_.get_today_horoscope(user_in_db.sign)
    result = await llm_service_.generate_horoscope(user_in_db, original_horoscope, date)
    await horoscope_service_.save_today_horoscope(user_id, result, date)

    await message.answer(text=result)
    return await index_handler.cmd_start(message)
