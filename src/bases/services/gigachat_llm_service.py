import abc
import datetime

from dto import user_dto


class GigaChatLLMService(abc.ABC):
    @abc.abstractmethod
    async def generate_horoscope(
        self,
        user: user_dto.UserDTO,
        english_horoscope: str,
        date: datetime.date
    ) -> str:
        raise NotImplementedError
