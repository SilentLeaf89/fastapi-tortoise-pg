from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from tortoise.contrib.fastapi import register_tortoise

from api.v1 import rate, history
from core.config import TORTOISE_ORM, project_settings


app = FastAPI(
    title=project_settings.PROJECT_NAME,
    # Адрес swagger-а
    docs_url="/api/openapi",
    # Адрес документации в формате OpenAPI
    openapi_url="/api/openapi.json",
    # Замена стандартного JSON-сереализатора на более шуструю версию
    default_response_class=ORJSONResponse,
)

register_tortoise(app, config=TORTOISE_ORM)

app.include_router(rate.router, prefix="/api/v1/rate")
app.include_router(history.router, prefix="/api/v1/history")
