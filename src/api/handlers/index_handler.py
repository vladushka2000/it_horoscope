from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from api.tools import filters, keyboards

router = Router()


@router.message(default_state, F.text.lower() == "отмена")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    await state.set_data({})
    await message.answer(
        text="Нечего отменять",
        reply_markup=ReplyKeyboardRemove()
    )

    await cmd_start(message)


@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )

    await cmd_start(message)


@router.message(CommandStart())
async def cmd_start(message: Message):
    is_registered = await filters.RegisteredUserFilter()(message, with_message=False)

    await message.answer(
        text="Сделаем предсказание на день?)",
        reply_markup=keyboards.get_main_inline_keyboard(is_registered=is_registered),
        parse_mode="Markdown"
    )
