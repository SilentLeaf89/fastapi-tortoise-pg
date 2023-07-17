import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Base(BaseModel):
    class Config:
        populate_by_name = True
