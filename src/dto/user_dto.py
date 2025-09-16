from typing import Optional

from pydantic import Field

from bases import base_dto
from tools import const


class UserDTO(base_dto.BaseDTO):
    id: int = Field(title="ID пользователя")
    full_name: Optional[str] = Field(title="Полное имя", default=None)
    sign: const.Sign = Field(title="Знак зодиака")
    company_role: const.CompanyRole = Field(title="Роль в компании")
    emoji: str = Field(title="HTML-код emoji")
