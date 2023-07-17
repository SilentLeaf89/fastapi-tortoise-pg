from typing import Dict
import datetime

from pydantic import Field

from schemas.base import Base


class PositionPerDay(Base):
    cargo_type: str = Field(min_length=1)
    declared_value: float = Field(ge=0)


class MultiDayPositions(Base):
    __root__: Dict[datetime.date, list[PositionPerDay]]
