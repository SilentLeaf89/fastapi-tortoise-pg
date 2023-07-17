import datetime
from uuid import UUID

from fastapi import APIRouter, Depends

from models import RateIn_Pydantic, Rate_Pydantic
from schemas.rate import (
    RateDeleteMessage,
    RateCalculateSingleMessage,
    RateCalculateMultipleMessage,
    RatesMultipleAddMessage,
    DateRates
)
from schemas.position import MultiDayPositions
from services.rate_service import RateService, get_rate_service


router = APIRouter()


@router.post("/add/single", response_model=Rate_Pydantic, tags=["Rate"])
async def add_new_rate(
    rate: RateIn_Pydantic,
    rate_service: RateService = Depends(get_rate_service),
) -> Rate_Pydantic:
    """
    Add a new rate.

    This endpoint allows the addition of a new rate based on
    the provided `RateIn_Pydantic` data.

    Parameters:
    - `rate`: An instance of `RateIn_Pydantic` representing the rate
              information to be added.

    Returns:
    - A `Rate_Pydantic` instance representing the newly created rate.

    Raises:
    - `HTTPException(422)`: If error validation in request parameters.
    - `HTTPException(409)`: If rate already exist.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    return await rate_service.add(rate)


@router.post(
        "/add/multiple",
        response_model=RatesMultipleAddMessage,
        tags=["Rate"]
        )
async def add_multiple_rates(
    data_rates: DateRates,
    rate_service: RateService = Depends(get_rate_service),
) -> RatesMultipleAddMessage:
    """
    Add rates from json.

    This endpoint adds information about insurance rates from json

    Parameters:
    - `data_rates`: An instance of `DateRates` representing the rates
                    information to be added.
    Returns:
    - A `RatesMultiAddMessage` - success message, e.g. {"msg": "success"}.

    Raises:
    - `HTTPException(422)`: If error validation in request parameters.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    return await rate_service.add_multiple(data_rates)


@router.get("/", response_model=list[Rate_Pydantic], tags=["Rate"])
async def get_all_rates(
    rate_service: RateService = Depends(get_rate_service),
) -> list[Rate_Pydantic]:
    """
    Get all rates.

    This endpoint retrieves all available rates.

    Returns:
    - A list of `RateResponseModel` instances representing all rates.

    Raises:
    - `HTTPException(404)`: If no one rates.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    return await rate_service.get_all()


@router.get("/{rate_id}", response_model=Rate_Pydantic, tags=["Rate"])
async def get_rate_by_id(
    rate_id: UUID,
    rate_service: RateService = Depends(get_rate_service),
) -> Rate_Pydantic:
    """
    Get rate by ID.

    This endpoint retrieves a rate by its unique identifier (`rate_id`).

    Parameters:
    - `rate_id`: The UUID of the rate.

    Returns:
    - A `RateResponseModel` instance representing the rate with the specified ID.

    Raises:
    - `HTTPException(404)`: If the rate does not exist.
    - `HTTPException(422)`: If uuid is not valid.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    return await rate_service.get(rate_id)


@router.delete("/{rate_id}", response_model=RateDeleteMessage, tags=["Rate"])
async def delete_rate_by_id(
    rate_id: UUID,
    rate_service: RateService = Depends(get_rate_service),
) -> RateDeleteMessage:
    """
    Delete rate by ID.

    This endpoint deletes a rate by its unique identifier (`rate_id`).

    Parameters:
    - `rate_id`: The UUID of the rate to be deleted.

    Returns:
    - `RateDeleteMessage`: A string message indicating
                           the success of the deletion.

    Raises:
    - `HTTPException(404)`: If the rate does not exist.
    - `HTTPException(422)`: If error validation in request parameters.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    return await rate_service.delete(rate_id)


@router.put("/{rate_id}", response_model=Rate_Pydantic, tags=["Rate"])
async def update_rate_by_id(
    rate_id: UUID,
    rate: RateIn_Pydantic,
    rate_service: RateService = Depends(get_rate_service),
) -> Rate_Pydantic:
    """
    Update rate by ID.

    This endpoint updates a rate with the specified
    unique identifier (`rate_id`) based on the provided `Rate_Pydantic` data.

    Parameters:
    - `rate_id`: The UUID of the rate to be updated.
    - `rate`: An instance of `RateIn_Pydantic` representing
              the updated rate information.

    Returns:
    - A `Rate_Pydantic` instance representing the updated rate.

    Raises:
    - `HTTPException(404)`: If the rate does not exist.
    - `HTTPException(422)`: If error validation in request parameters.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    return await rate_service.update(rate_id, rate)


@router.get(
        "/calculate/single",
        response_model=RateCalculateSingleMessage,
        tags=["Calculate"],
        )
async def calculate_single_position(
    date: datetime.date,
    cargo_type: str,
    declared_value: float,
    rate_service: RateService = Depends(get_rate_service),
) -> RateCalculateSingleMessage:
    """
    Calculates the cost of insurance based on the date, type of cargo
    and declared value.
    This endpoint takes into account the insurance rate
    for the specified day and the type of cargo.

    Args:
        date (datetime.date): date on which the calculation is made
        cargo_type (str): cargo type for insurance rate selection
        declared_value (float): declared value of the cargo

    Returns:
    - A `RateSingleCalculateMessage` including the cost of insurance.
        Example {"cost_of_insurance": 12345.67}

    Raises:
    - `HTTPException(404)`: If the rate does not exist.
    - `HTTPException(422)`: If error validation in request parameters.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    return await rate_service.calculate_single(
        date, cargo_type, declared_value)


@router.post(
        "/calculate/multiple",
        response_model=RateCalculateMultipleMessage,
        tags=["Calculate"],
        )
async def calculate_multiple_position(
        positions: MultiDayPositions,
        rate_service: RateService = Depends(get_rate_service),
) -> RateCalculateMultipleMessage:
    """
    Calculates the cost of insurance based on the date, type of cargo
    and declared value.
    This endpoint takes into account the insurance rate
    for the specified day and the type of cargo.

    Args:
        date (datetime.date): date on which the calculation is made
        cargo_type (str): cargo type for insurance rate selection
        declared_value (float): declared value of the cargo

    Returns:
    - A `RateSingleCalculateMessage` including the cost of insurance.
        Example {"cost_of_insurance": 12345.67}

    Raises:
    - `HTTPException(404)`: If the rate does not exist.
    - `HTTPException(422)`: If error validation in request parameters.
    - `HTTPException(500)`: If an internal server error occurs.
    """
    return await rate_service.calculate_multiple(positions)
