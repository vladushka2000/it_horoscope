from __future__ import annotations  # noqa

import json

import httpx

from bases import base_http_client
from dto import http_dto


class HTTPClient(base_http_client.BaseHTTPClient):
    async def __aenter__(self) -> HTTPClient:
        self._client = httpx.AsyncClient(timeout=None, verify=False)

        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        if not self._client:
            raise ValueError("Клиент не инициализирован")

        await self._client.aclose()

    async def get(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        if not self._client:
            raise ValueError("Клиент не инициализирован")

        response = await self._client.get(
            url=request_params.url,
            headers=request_params.headers,
            params=request_params.query_params,
        )

        payload = None

        try:
            payload = response.json()
        except json.decoder.JSONDecodeError:
            payload = response.content

        return http_dto.HTTPResponseDTO(
            status=response.status_code,
            headers=response.headers,
            payload=payload,
        )

    async def post(self, request_params: http_dto.HTTPRequestDTO) -> http_dto.HTTPResponseDTO:
        if not self._client:
            raise ValueError("Клиент не инициализирован")

        response = await self._client.post(
            url=request_params.url,
            headers=request_params.headers,
            params=request_params.query_params,
            json=request_params.payload,
            data=request_params.form_data,
        )

        payload = None

        try:
            payload = response.json()
        except json.decoder.JSONDecodeError:
            payload = response.content

        return http_dto.HTTPResponseDTO(
            status=response.status_code,
            headers=response.headers,
            payload=payload,
        )
