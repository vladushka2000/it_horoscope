import abc

from dto import user_dto


class UserService(abc.ABC):
    @abc.abstractmethod
    async def create_user(self, user: user_dto.UserDTO) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_user(self, user_id: int) -> user_dto.UserDTO:
        raise NotImplementedError