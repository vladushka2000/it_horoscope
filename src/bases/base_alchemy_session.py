import abc
from contextlib import AbstractContextManager, asynccontextmanager

from sqlalchemy.ext import asyncio as async_alchemy


class BaseAlchemySession(abc.ABC):
    def __init__(self, pg_host: str) -> None:
        self._pg_host = pg_host

    @abc.abstractmethod
    @asynccontextmanager
    def __call__(self) -> AbstractContextManager[async_alchemy.AsyncSession]:
        raise NotImplementedError
