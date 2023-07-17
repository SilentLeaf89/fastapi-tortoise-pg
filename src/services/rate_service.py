# mypy: no-disallow-untyped-decorators
# pylint: disable=E0611,E0401

import datetime
from functools import lru_cache
from uuid import UUID

from fastapi import Depends, HTTPException
from tortoise.exceptions import IntegrityError

from models.insurance import Rate
from models import RateIn_Pydantic, Rate_Pydantic
from core.get_logger import logger
from schemas.rate import (
    RateDeleteMessage,
    RateCalculateSingleMessage,
    DateRates,
    RatesMultipleAddMessage,
    RateCalculateMultipleMessage,
)
from schemas.position import MultiDayPositions
from services.event_service import EventService, get_event_service


class RateService:
    def __init__(self, history_service: EventService) -> None:
        self.history_service = history_service

    async def get(self, rate_id: UUID) -> Rate_Pydantic:
        logger.debug(
            "[RateService][get] - trying to get rate by id %s", rate_id)
        result = await Rate_Pydantic.from_queryset_single(Rate.get(id=rate_id))
        if not result:
            logger.debug("[RateService][get] - rate %s not found", rate_id)
            raise HTTPException(
                status_code=404,
                detail="Rate {} not found".format(rate_id)
                )
        logger.info("[RateService][get] - rate found")
        return result

    async def get_all(self) -> list[Rate_Pydantic]:
        logger.debug("[RateService][get_all] - Trying to get all rates")
        result = await Rate_Pydantic.from_queryset(Rate.all())
        if not result:
            logger.debug("[RateService][get_all] - rates not found")
            raise HTTPException(
                status_code=404,
                detail="Rates not found"
                )
        logger.info("[RateService][get_all] - %s rates found", len(result))
        return result

    async def add(self, new_rate: RateIn_Pydantic) -> Rate_Pydantic:
        logger.debug(
            "[RateService][add] - trying to add rate for %s on %s",
            new_rate.cargo_type, new_rate.date
        )
        rate = await Rate.create(**new_rate.dict(exclude_unset=True))

        logger.info("[RateService][add] - new rate added for %s on %s",
                    new_rate.cargo_type, new_rate.date)
        return await Rate_Pydantic.from_tortoise_orm(rate)

    async def add_multiple(self, data: DateRates) -> RatesMultipleAddMessage:
        logger.debug(
            "[RateService][add_multiple] - trying to add rates from json"
        )

        await self._create_rates_from_data(data)

        logger.info(
            "[RateService][add_multiple] - added rates successfully"
        )
        return RatesMultipleAddMessage(
            **{"msg": "added insurance rates successfully"})

    async def update(self, rate_id: UUID, rate: RateIn_Pydantic,) -> Rate_Pydantic:
        logger.debug(
            "[RateService][update] - trying to update rate %s",
            rate_id,
        )
        await Rate.filter(id=rate_id).update(**rate.dict(exclude_unset=True))
        logger.info("[RateService][update] - rate updated")
        return await Rate_Pydantic.from_queryset_single(Rate.get(id=rate_id))

    async def delete(self, rate_id: UUID) -> RateDeleteMessage:
        logger.debug(
            "[RateService][delete] - trying to delete rate %s",
            rate_id,
        )
        deleted_rate = await Rate.filter(id=rate_id).delete()
        if not deleted_rate:
            raise HTTPException(
                status_code=404,
                detail="Rate {} not found".format(rate_id)
                )
        logger.info("[RateService][delete] - rate deleted")
        return RateDeleteMessage(
            msg="Rate {} deleted successfully".format(rate_id)
            )

    async def calculate_single(
            self,
            date: datetime.date,
            cargo_type: str,
            declared_value: float,
            ) -> RateCalculateSingleMessage:
        logger.debug(
            """[RateService][calculate_single] - trying to calculate the cost
            of insurance for the %s and %s with a %s""",
            date, cargo_type, declared_value
        )
        rate_info = await Rate.filter(
            date=date, cargo_type=cargo_type).first().values("rate")
        if not rate_info:
            raise HTTPException(
                status_code=404,
                detail="Insurance rate for {} was not found".format(date)
                )
        current_rate = rate_info["rate"]
        cost = round(float(current_rate) * declared_value, 2)
        rate = await Rate.filter(
            date=date, cargo_type=cargo_type).first()
        await self.history_service.add(
            rate=rate,
            date=date,
            cargo_type=cargo_type,
            declared_value=declared_value,
            cost=cost,
            )
        logger.info(
            "[RateService][calculate_single] - Calculated cost of insurance"
        )
        return RateCalculateSingleMessage(**{"cost_of_insurance": cost})

    async def calculate_multiple(
            self, positions: MultiDayPositions
            ) -> RateCalculateMultipleMessage:
        logger.debug(
            """[RateService][calculate_multiple] - trying to calculate the cost
            of insurance from %s""", positions
        )

        total_cost = await self._calculate_cost(positions)

        logger.info(
            "[RateService][calculate_multiple] - Calculated cost of insurance"
        )
        return RateCalculateMultipleMessage(**{"total_cost": total_cost})

    async def _create_rates_from_data(self, data: DateRates) -> None:
        logger.debug(
            "[RateService][_create_rates_from_data] - start create"
        )
        date_rates = data.__root__
        for date in date_rates.keys():
            for position in date_rates[date]:
                try:
                    await Rate.create(
                        date=date,
                        cargo_type=position.cargo_type,
                        rate=position.rate
                    )
                except IntegrityError:
                    raise HTTPException(
                        status_code=400,
                        detail="Rate for date {} already exists".format(date)
                        )
        logger.debug(
            "[RateService][_create_rates_from_data] - create succesful"
        )

    async def _calculate_cost(self, positions: MultiDayPositions) -> float:
        logger.debug("[RateService][_calculate_cost] - start calculate")
        total_cost = 0
        date_positions = positions.__root__
        for date in date_positions.keys():
            for position in date_positions[date]:
                rate_in_date = await Rate.filter(
                    date=date,
                    cargo_type=position.cargo_type
                ).first().values("rate")
                if not rate_in_date:
                    raise HTTPException(
                        status_code=404,
                        detail="Rate not found for {} in {}".format(
                            position.cargo_type, date)
                    )

                cost = round(
                    float(rate_in_date["rate"]) * position.declared_value, 2)

                rate = await Rate.filter(
                    date=date, cargo_type=position.cargo_type).first()
                await self.history_service.add(
                    rate=rate,
                    date=date,
                    cargo_type=position.cargo_type,
                    declared_value=position.declared_value,
                    cost=cost,
                    )

                total_cost += cost
        logger.debug("[RateService][_calculate_cost] - calculated done")
        return total_cost


@lru_cache
def get_rate_service(
        history_service: EventService = Depends(get_event_service)
        ) -> RateService:
    rate_service = RateService(history_service)
    return rate_service
