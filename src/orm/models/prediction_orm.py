import datetime
import uuid
from typing import Optional

from sqlalchemy import ForeignKey, Date, Text, Index
from sqlalchemy.orm import Mapped, mapped_column

from bases import base_alchemy_model


class Prediction(base_alchemy_model.Base):
    __tablename__ = "predictions"
    __table_args__ = (
        Index(
            "idx_user_date",
            "user_id",
            "date",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, comment="ID предсказания")
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", comment="ID пользователя", ondelete="CASCADE")
    )
    date: Mapped[datetime.date] = mapped_column(
        Date, default=lambda: datetime.datetime.now(datetime.UTC).date(), comment="День предсказания"
    )
    predict: Mapped[str] = mapped_column(Text, comment="Предсказание")
