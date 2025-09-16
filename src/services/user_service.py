from dependency_injector.wiring import inject, Provide

from bases.repositories import base_user_repository
from bases.services import user_service
from dto import user_dto
from tools.di_containers import alchemy_container


class UserService(user_service.UserService):
    @inject
    async def create_user(
        self,
        user: user_dto.UserDTO,
        user_repository: base_user_repository.BaseUserRepository = Provide[
            alchemy_container.AlchemyContainer.user_repository
        ],  # noqa
    ) -> None:
        await user_repository.create(user)

    @inject
    async def get_user(
        self,
        user_id: int,
        user_repository: base_user_repository.BaseUserRepository = Provide[
            alchemy_container.AlchemyContainer.user_repository
        ],  # noqa
    ) -> user_dto.UserDTO:
        return await user_repository.retrieve(user_id)
