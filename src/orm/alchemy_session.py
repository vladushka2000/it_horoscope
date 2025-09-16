from contextlib import AbstractContextManager, asynccontextmanager
from functools import cached_property

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from bases import base_alchemy_session


class AlchemySession(base_alchemy_session.BaseAlchemySession):
    def _build_engine(self) -> AsyncEngine:
        return create_async_engine(str(self._pg_host))

    @cached_property
    def _get_session_factory(self) -> sessionmaker:
        session_factory = sessionmaker(  # noqa
            autocommit=False,
            autoflush=False,
            bind=self._build_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )

        return session_factory

    @asynccontextmanager
    async def __call__(self) -> AbstractContextManager[AsyncSession]:
        db = self._get_session_factory()

        try:
            yield db
        finally:
            await db.close()
