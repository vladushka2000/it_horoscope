from typing import Optional

from sqlalchemy import BigInteger, Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column

from bases import base_alchemy_model
from tools import const


class User(base_alchemy_model.Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, comment="ID пользователя")
    full_name: Mapped[Optional[str]] = mapped_column(comment="Полное имя", nullable=True)
    sign: Mapped[const.Sign] = mapped_column(
        SQLEnum(const.Sign), comment="Знак зодиака"
    )
    company_role: Mapped[const.CompanyRole] = mapped_column(
        SQLEnum(const.CompanyRole), comment="Роль в компании"
    )
    emoji: Mapped[str] = mapped_column(String(128), comment="HTML-код emoji")
