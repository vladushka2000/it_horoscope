import datetime
from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.ext import asyncio as async_alchemy

from dto import prediction_dto


class BaseHoroscopeRepository:
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[async_alchemy.AsyncSession]]
    ) -> None:
        self._session_factory = session_factory

    async def create(self, prediction: prediction_dto.PredictionDTO) -> prediction_dto.PredictionDTO:
        raise NotImplementedError()

    async def retrieve_by_user_date(
        self,
        user_id: int,
        date: datetime.date
    ) -> prediction_dto.PredictionDTO | None:
        raise NotImplementedError()
