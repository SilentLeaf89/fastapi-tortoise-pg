from typing import Annotated
from fastapi import APIRouter, Depends, Query

from services.event_service import EventService, get_event_service
from models import Event_Pydantic


router = APIRouter()


@router.get("/", response_model=list[Event_Pydantic], tags=["History"])
async def get_all_rates(
    event_service: EventService = Depends(get_event_service),
    page_number: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1)] = 50,
) -> list[Event_Pydantic]:
    """
    Get all history of events.

    This endpoint retrieves all available events.

    Returns:
    - A list of `Event_Pydantic` instances representing all events.

    Raises:
    - `HTTPException(404)`: If no one events.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    return await event_service.get_all(page_number, page_size)
