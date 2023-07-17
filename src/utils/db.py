def construct_db_url(
    user: str,
    password: str,
    host: str,
    port: int,
    database: str,
    sync_mode: bool = False,
):
    if sync_mode:
        driver = "psycopg://"
    else:
        driver = "asyncpg://"
    return "".join(
        [driver, user, ":", password, "@", host, ":", str(port), "/", database]
    )
