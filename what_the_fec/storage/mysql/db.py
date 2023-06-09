from sqlalchemy import Connection, create_engine

from what_the_fec.storage.mysql.config import MySQLConfig


class MySQLDB:
    __slots__ = ("_engine",)

    def __init__(self, config: MySQLConfig) -> None:
        if not isinstance(config, MySQLConfig):
            raise TypeError(
                f"all configurations be an instance of MySQLConfig; type(config): {config};"
            )
        # Citation for the following code:
        # Date: 04/06/2023
        # Copied from /OR/ Adapted from /OR/ Based on:
        # FastAPI/SQLAlchemy documentation examples
        self._engine = create_engine(
            f"mysql+pymysql://{config.db_user}:{config.db_password}@{config.db_hostname}:{config.db_port}/{config.db_name}?charset=utf8mb4",
            pool_size=config.pool_connections,
            pool_pre_ping=True,
        )

    def get_conn(self) -> Connection:
        with self._engine.connect() as conn:
            yield conn


_MYSQL_DB: MySQLDB


def init(config: MySQLConfig) -> None:
    if not isinstance(config, MySQLConfig):
        raise TypeError(
            f"all configurations be an instance of MySQLConfig; type(config): {config};"
        )
    global _MYSQL_DB
    _MYSQL_DB = MySQLDB(config)


def get_db() -> MySQLDB:
    global _MYSQL_DB
    if _MYSQL_DB is None:
        raise RuntimeError("you must init a MySQLDB before calling this function")
    return _MYSQL_DB


def get_db_conn() -> Connection:
    return get_db().get_conn()
