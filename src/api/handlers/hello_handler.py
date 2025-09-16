from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from dependency_injector.wiring import inject, Provide

from api.handlers import index_handler
from api.states import registration_state
from api.tools import filters, keyboards
from bases.services import user_service
from dto import user_dto
from tools import const
from tools.di_containers import service_container

router = Router()


@router.message(F.text.lower() == "регистрация")
@inject
async def cmd_hello(
    message: Message,
    state: FSMContext,
    user_service_: user_service.UserService = Provide[
        service_container.ServiceContainer.user_service
    ],  # noqa
):
    user_id = message.from_user.id
    user_in_db = await user_service_.get_user(user_id)

    if user_in_db is not None:
        user_message_part = f", {user_in_db.full_name}" if user_in_db.full_name else ""

        await message.answer(text="👋")
        await message.answer(text=f"Привет{user_message_part}!!")

        return

    await message.answer(
        text="Для начала выбери свой знак зодиака ✨",
        reply_markup=keyboards.make_keyboard([sign.value for sign in const.Sign], is_column=True)
    )
    await state.set_state(registration_state.Registration.choosing_sign)


@router.message(registration_state.Registration.choosing_sign, F.text.in_(const.Sign))
async def sign_chosen(message: Message, state: FSMContext):
    await state.update_data(sign=message.text)
    await message.answer(
        text=f"Ты {message.text.lower()}!\n"
             f"Теперь определимся с твоей должностью 💼",
        reply_markup=keyboards.make_keyboard([role.value for role in const.CompanyRole], is_column=True)
    )
    await state.set_state(registration_state.Registration.choosing_company_role)


@router.message(registration_state.Registration.choosing_sign)
async def sign_chosen_incorrectly(message: Message):
    await message.answer(
        text="Я не знаю такого знака зодиака...\n"
             "Выбери один из вариантов из списка:",
        reply_markup=keyboards.make_keyboard([sign.value for sign in const.Sign], is_column=True)
    )


@router.message(registration_state.Registration.choosing_company_role, F.text.in_(const.CompanyRole))
async def role_chosen(message: Message, state: FSMContext):
    await state.update_data(company_role=message.text)
    await message.answer(
        text=f"Ого, {message.text.lower()}!\n"
             f"Осталось понять, какое emoji тебе больше подходит. Просто отправь свой любимый смайлик!",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(registration_state.Registration.choosing_emoji)


@router.message(registration_state.Registration.choosing_company_role)
async def role_chosen_incorrectly(message: Message):
    await message.answer(
        text="Интересная роль, но я не знаю такой...\n"
             "Выбери один из вариантов из списка:",
        reply_markup=keyboards.make_keyboard([role.value for role in const.CompanyRole], is_column=True)
    )


@router.message(
    registration_state.Registration.choosing_emoji,
    filters.HtmlEmojiFilter()
)
@inject
async def emoji_chosen(
    message: Message,
    state: FSMContext,
    user_service_: user_service.UserService = Provide[
        service_container.ServiceContainer.user_service
    ],  # noqa
):
    await state.update_data(emoji=message.text)
    await message.answer(
        text="Вот мы и познакомились! 🎉",
        reply_markup=ReplyKeyboardRemove()
    )

    user_data = await state.get_data()
    user = user_dto.UserDTO(
        id=message.from_user.id,
        full_name=message.from_user.full_name,
        sign=user_data["sign"],
        company_role=user_data["company_role"],
        emoji=user_data["emoji"]
    )

    await user_service_.create_user(user)
    await state.clear()

    await index_handler.cmd_start(message)


@router.message(registration_state.Registration.choosing_emoji)
async def emoji_chosen_incorrectly(message: Message):
    await message.answer(
        text="Не могу найти такой emoji...\n"
             "Попробуй еще раз...",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.text.lower() == "профиль", filters.RegisteredUserFilter())
@inject
async def cmd_profile(
    message: Message,
    user_service_: user_service.UserService = Provide[
        service_container.ServiceContainer.user_service
    ],  # noqa
):
    user_id = message.from_user.id
    user_in_db = await user_service_.get_user(user_id)

    await message.answer(
        text=f"Твои данные:\n"
             f"👤Имя - {user_in_db.full_name}\n"
             f"{user_in_db.sign.value} - твой знак зодиака\n"
             f"💼 Должность - {user_in_db.company_role.value}\n"
             f"{user_in_db.emoji} - твое личное emoji\n"
    )

    await index_handler.cmd_start(message)
