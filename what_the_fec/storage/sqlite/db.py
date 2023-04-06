from sqlalchemy import Connection, create_engine

from what_the_fec.storage.sqlite.config import SqliteConfig


class SqliteDB:
    __slots__ = ("_engine",)

    def __init__(self, config: SqliteConfig) -> None:
        if not isinstance(config, SqliteConfig):
            raise TypeError(
                f"all configurations be an instance of SqliteConfig; type(config): {config};"
            )
        self._engine = create_engine(
            "sqlite:///./sql_app.db",
            connect_args={"check_same_thread": False},
            pool_size=config.pool_connections,
        )

    def get_conn(self) -> Connection:
        with self._engine.connect() as conn:
            yield conn


_SQLITE_DB: SqliteDB


def init(config: SqliteConfig) -> None:
    if not isinstance(config, SqliteConfig):
        raise TypeError(
            f"all configurations be an instance of SqliteConfig; type(config): {config};"
        )
    global _SQLITE_DB
    _SQLITE_DB = SqliteDB(config)

def get_db() -> SqliteDB:
    global _SQLITE_DB
    if _SQLITE_DB is None:
        raise RuntimeError("you must init a SqliteDB before calling this function")
    return _SQLITE_DB
