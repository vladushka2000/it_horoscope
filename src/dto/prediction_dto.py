import datetime
import uuid

from pydantic import Field

from bases import base_dto


class PredictionDTO(base_dto.BaseDTO):
    id: uuid.UUID = Field(title="ID предсказания")
    user_id: int = Field(title="ID пользователя")
    date: datetime.date = Field(title="День предсказания")
    predict: str = Field(title="Предсказание")
