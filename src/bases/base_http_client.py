from __future__ import annotations  # noqa

import abc

from dto import http_dto


class BaseHTTPClient(abc.ABC):
    @abc.abstractmethod
    async def __aenter__(self) -> BaseHTTPClient:
        raise NotImplementedError

    @abc.abstractmethod
    async def __aexit__(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, request: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        raise NotImplementedError

    @abc.abstractmethod
    def post(self, request: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        raise NotImplementedError
