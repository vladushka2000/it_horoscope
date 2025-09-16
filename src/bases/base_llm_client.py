from __future__ import annotations  # noqa

import abc
import json
import logging
from typing import Optional, Dict, List

import httpx
import openai

logger = logging.getLogger(__name__)


class BaseLLMClient(abc.ABC):
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.max_tokens = max_tokens
        self.client: Optional[openai.AsyncOpenAI] = None

    async def __aenter__(self) -> BaseLLMClient:
        self.client = openai.AsyncOpenAI(
            http_client=httpx.AsyncClient(verify=False),
            api_key=self.api_key,
            base_url=self.base_url
        )

        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        if not self.client:
            raise ValueError("Клиент не инициализирован")

        await self.client.close()
        self.client = None

    def set_api_key(self, key: str) -> None:
        self.api_key = key

    async def chat(
        self,
        prompt: str,
        system_message: Optional[str] = None,
        history: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.2,
        top_p: float = 1.0,
    ) -> str:
        logger.info("Инициализирован запрос в клиент OpenAI")

        if not self.client:
            raise ValueError("Клиент OpenAI не инициализирован")

        messages = []

        if system_message:
            messages.append(
                {
                    "role": "system",
                    "content": f"{system_message}",
                }
            )

        if history:
            messages.extend(history)

        messages.append({"role": "user", "content": prompt})

        params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
            "response_format": {"type": "text"},
        }

        if self.max_tokens:
            params["max_tokens"] = self.max_tokens

        try:
            response = await self.client.chat.completions.create(**params)
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Произошла ошибка: {e}")

            return {"error": str(e), "type": "API_ERROR"}
