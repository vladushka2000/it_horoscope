import abc
import datetime

from dto import prediction_dto
from tools import const


class HoroscopeService(abc.ABC):
    @abc.abstractmethod
    async def get_today_horoscope(self, sign: const.Sign) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def save_today_horoscope(self, user_id: int, horoscope: str, date: datetime.date) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_horoscope(self, user_id: int, date: datetime.date) -> prediction_dto.PredictionDTO | None:
        raise NotImplementedError
