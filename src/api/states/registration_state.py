from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    setting_name = State()
    choosing_sign = State()
    choosing_company_role = State()
    choosing_emoji = State()
