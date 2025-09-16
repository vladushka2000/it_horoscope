from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.ext import asyncio as async_alchemy

from dto import user_dto


class BaseUserRepository:
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[async_alchemy.AsyncSession]]
    ) -> None:
        self._session_factory = session_factory

    async def create(self, user_info: user_dto.UserDTO) -> user_dto.UserDTO:
        raise NotImplementedError()

    async def retrieve(self, id_: int) -> user_dto.UserDTO | None:
        raise NotImplementedError()
