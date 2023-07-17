import datetime
from functools import lru_cache

from fastapi import HTTPException

from core.get_logger import logger
from models import Event_Pydantic
from models.insurance import Rate, Event


class EventService:
    async def add(
            self,
            rate: Rate,
            date: datetime.date,
            cargo_type: str,
            declared_value: float,
            cost: float,
            ) -> Event_Pydantic:
        logger.debug(
            "[EventService][add] - trying to add event for %s on %s",
            cargo_type, date
        )

        event = await Event.create(
            date=date,
            cargo_type=cargo_type,
            rate=rate,
            declared_value=declared_value,
            cost=cost,
            )

        logger.info("[EventService][add] - new rate added for %s on %s",
                    cargo_type, date)
        return await Event_Pydantic.from_tortoise_orm(event)

    async def get_all(
            self,
            page_number: int,
            page_size: int
            ) -> list[Event_Pydantic]:
        offset = (page_number - 1) * page_size
        limit = page_size
        logger.debug("[EventService][get_all] - Trying to get all events")
        result = await Event_Pydantic.from_queryset(
            Event.all().limit(limit).offset(offset))
        if not result:
            logger.debug("[EventService][get_all] - events not found")
            raise HTTPException(
                status_code=404,
                detail="Rates not found"
                )
        logger.info("[EventService][get_all] - %s events found", len(result))
        return result


@lru_cache
def get_event_service() -> EventService:
    event_service = EventService()
    return event_service
