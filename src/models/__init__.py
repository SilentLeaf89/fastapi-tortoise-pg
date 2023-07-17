from tortoise import Tortoise
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from .insurance import Rate, Event


Tortoise.init_models(["models"], "models")

Rate_Pydantic = pydantic_model_creator(Rate, name="Rate_Pydantic")
RateIn_Pydantic = pydantic_model_creator(
    Rate, name="RateIn", exclude_readonly=True)


Event_Pydantic = pydantic_model_creator(Event, name="History_Pydantic")
Event_In_Pydantic = pydantic_model_creator(
    Event, name="HistoryIn", exclude_readonly=True)
