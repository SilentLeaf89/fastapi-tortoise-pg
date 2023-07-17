from datetime import datetime

import psycopg
import pytest_asyncio

from tests.config.settings import dsn


@pytest_asyncio.fixture
async def insert_test_rate():
    async def inner():
        dsn_postgres = "dbname={0} user={1} password={2} host={3} port={4}".format(
            dsn.dbname, dsn.user, dsn.password, dsn.host, dsn.port
        )
        async with await psycopg.AsyncConnection.connect(dsn_postgres) as aconn:
            async with aconn.cursor() as acur:
                await acur.execute(
                    """INSERT INTO "rate"
                    (id, created_at, modified_at, date, cargo_type, rate)
                    VALUES (%s, %s, %s, %s, %s, %s);""",
                    (
                        "c2b9c859-9803-4d60-9a06-956f33ffec47",
                        datetime.utcnow(),
                        datetime.utcnow(),
                        "2023-07-17",
                        "oil",
                        0.001,
                    ),
                )
    return inner
