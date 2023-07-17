import datetime
from typing import Dict

from pydantic import Field

from schemas.base import Base


class RateDeleteMessage(Base):
    msg: str


class RatesMultipleAddMessage(Base):
    msg: str


class RateCalculateSingleMessage(Base):
    cost_of_insurance: float = Field(ge=0)


class RateCalculateMultipleMessage(Base):
    total_cost: float


class RateRow(Base):
    cargo_type: str = Field(min_length=1)
    rate: float = Field(ge=0)


class DateRates(Base):
    __root__: Dict[datetime.date, list[RateRow]]
