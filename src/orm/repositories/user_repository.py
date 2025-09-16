from sqlalchemy import select

from bases.repositories import base_user_repository
from dto import user_dto
from orm.models import user_orm


class UserRepository(base_user_repository.BaseUserRepository):
    async def create(self, user_info: user_dto.UserDTO) -> user_dto.UserDTO:
        async with self._session_factory() as session:
            user_orm_ = user_orm.User(
                id=user_info.id,
                full_name=user_info.full_name if user_info.full_name else "",
                sign=user_info.sign,
                company_role=user_info.company_role,
                emoji=user_info.emoji,
            )
            session.add(user_orm_)

            await session.flush()
            await session.commit()

            return user_dto.UserDTO(
                id=user_orm_.id,
                full_name=user_orm_.full_name,
                sign=user_orm_.sign,
                company_role=user_orm_.company_role,
                emoji=user_orm_.emoji,
            )

    async def retrieve(self, id_: int) -> user_dto.UserDTO | None:
        async with self._session_factory() as session:
            query = select(user_orm.User).where(user_orm.User.id == id_)
            result = await session.execute(query)
            user_orm_ = result.scalars().first()

            if user_orm_ is None:
                return None

            return user_dto.UserDTO(
                id=user_orm_.id,
                full_name=user_orm_.full_name,
                sign=user_orm_.sign,
                company_role=user_orm_.company_role,
                emoji=user_orm_.emoji,
            )
