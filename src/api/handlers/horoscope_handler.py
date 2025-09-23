from aiogram import Router, F
from aiogram.types import Message
from dependency_injector.wiring import inject, Provide

from api.tools import filters, keyboards
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
    is_registered = await filters.RegisteredUserFilter()(message, with_message=False)

    user_id = message.from_user.id
    date = message.date.date()
    user_in_db = await user_service_.get_user(user_id)

    await message.answer(text="🔮")
    await message.answer(text="Посмотрим, что говорят звезды...")

    horoscope_in_db = await horoscope_service_.get_horoscope(user_id, date)

    if horoscope_in_db:
        await message.answer(text=horoscope_in_db.predict)

        return await message.answer(
            text="С тобой был бот IT-гороскопа\nВозвращайся завтра 😉",
            reply_markup=keyboards.get_main_inline_keyboard(is_registered=is_registered)
        )

    original_horoscope = await horoscope_service_.get_today_horoscope(user_in_db.sign)
    result = await llm_service_.generate_horoscope(user_in_db, original_horoscope, date)
    await horoscope_service_.save_today_horoscope(user_id, result, date)
    await message.answer(text=result)

    return await message.answer(
        text="С тобой был бот IT-гороскопа\nВозвращайся завтра 😉",
        reply_markup=keyboards.get_main_inline_keyboard(is_registered=is_registered)
    )
