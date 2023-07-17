from datetime import datetime

import psycopg
import pytest_asyncio

from tests.config.settings import dsn


@pytest_asyncio.fixture
async def insert_test_multiple_rate():
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
                        "2023-07-15",
                        "Wood",
                        0.001,
                    ),
                )

                await acur.execute(
                    """INSERT INTO "rate"
                    (id, created_at, modified_at, date, cargo_type, rate)
                    VALUES (%s, %s, %s, %s, %s, %s);""",
                    (
                        "c2b9c859-9803-4d60-9a06-956f33ffec48",
                        datetime.utcnow(),
                        datetime.utcnow(),
                        "2023-07-16",
                        "Steel",
                        0.003,
                    ),
                )

                await acur.execute(
                    """INSERT INTO "rate"
                    (id, created_at, modified_at, date, cargo_type, rate)
                    VALUES (%s, %s, %s, %s, %s, %s);""",
                    (
                        "c2b9c859-9803-4d60-9a06-956f33ffec49",
                        datetime.utcnow(),
                        datetime.utcnow(),
                        "2023-07-16",
                        "Cooper",
                        0.002,
                    ),
                )

                await acur.execute(
                    """INSERT INTO "rate"
                    (id, created_at, modified_at, date, cargo_type, rate)
                    VALUES (%s, %s, %s, %s, %s, %s);""",
                    (
                        "c2b9c859-9803-4d60-9a06-956f33ffec50",
                        datetime.utcnow(),
                        datetime.utcnow(),
                        "2023-07-17",
                        "Chocolate",
                        0.005,
                    ),
                )
    return inner
