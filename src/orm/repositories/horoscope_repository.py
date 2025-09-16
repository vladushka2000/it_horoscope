import datetime

from sqlalchemy import select

from bases.repositories import base_horoscope_repository
from dto import prediction_dto
from orm.models import prediction_orm


class HoroscopeRepository(base_horoscope_repository.BaseHoroscopeRepository):
    async def create(self, prediction: prediction_dto.PredictionDTO) -> prediction_dto.PredictionDTO:
        async with self._session_factory() as session:
            prediction_orm_ = prediction_orm.Prediction(
                id=prediction.id,
                user_id=prediction.user_id,
                date=prediction.date,
                predict=prediction.predict
            )
            session.add(prediction_orm_)

            await session.flush()
            await session.commit()

            return prediction_dto.PredictionDTO(
                id=prediction_orm_.id,
                user_id=prediction_orm_.user_id,
                date=prediction_orm_.date,
                predict=prediction_orm_.predict
            )

    async def retrieve_by_user_date(
        self,
        user_id: int,
        date: datetime.date
    ) -> prediction_dto.PredictionDTO | None:
        async with self._session_factory() as session:
            query = select(prediction_orm.Prediction).where(
                prediction_orm.Prediction.user_id == user_id,
                prediction_orm.Prediction.date == date
            )
            result = await session.execute(query)
            prediction_orm_ = result.scalars().first()

            if prediction_orm_ is None:
                return None

            return prediction_dto.PredictionDTO(
                id=prediction_orm_.id,
                user_id=prediction_orm_.user_id,
                date=prediction_orm_.date,
                predict=prediction_orm_.predict
            )
