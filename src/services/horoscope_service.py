import datetime
import logging
import uuid
from http import HTTPStatus

from dependency_injector.wiring import Provide, inject

from bases import base_http_client
from bases.repositories import base_horoscope_repository
from bases.services import horoscope_service
from dto import http_dto, prediction_dto, user_dto
from tools import const
from tools.di_containers import integration_container, alchemy_container

logger = logging.getLogger(__name__)


class HoroscopeService(horoscope_service.HoroscopeService):
    @inject
    async def get_today_horoscope(
        self,
        sign: const.Sign,
        http_client: base_http_client.BaseHTTPClient = Provide[
            integration_container.IntegrationContainer.http_client
        ],  # noqa
    ) -> str:
        logger.info("Получение гороскопа")

        async with http_client as client:
            response = await client.get(
                http_dto.HTTPRequestDTO(
                    url="https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily",
                    headers={
                        "Accept": "application/json"
                    },
                    query_params={
                        "sign": const.horoscope_integration_signs[sign],
                        "day": "TODAY"
                    }
                )
            )

            if response.status != HTTPStatus.OK:
                raise ValueError("Не удалось получить гороскоп")

            return response.payload["data"]["horoscope_data"]

    @inject
    async def save_today_horoscope(
        self,
        user_id: int,
        horoscope: str,
        date: datetime.date,
        horoscope_repository: base_horoscope_repository.BaseHoroscopeRepository = Provide[
            alchemy_container.AlchemyContainer.horoscope_repository
        ]  # noqa
    ) -> None:
        prediction = prediction_dto.PredictionDTO(
            id=uuid.uuid4(),
            user_id=user_id,
            date=date,
            predict=horoscope
        )
        await horoscope_repository.create(prediction)

    @inject
    async def get_horoscope(
        self,
        user_id: int,
        date: datetime.date,
        horoscope_repository: base_horoscope_repository.BaseHoroscopeRepository = Provide[
            alchemy_container.AlchemyContainer.horoscope_repository
        ]  # noqa
    ) -> prediction_dto.PredictionDTO | None:
        return await horoscope_repository.retrieve_by_user_date(user_id=user_id, date=date)
