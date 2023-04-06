import abc

from sqlalchemy import Connection

from what_the_fec.storage.config import StorageConfig
from what_the_fec.storage.sqlite.config import SqliteConfig
from what_the_fec.storage.sqlite.db import init as sqlite_init


class DB(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_conn(self) -> Connection:
        raise NotImplementedError


def init(config: StorageConfig):
    if not isinstance(config, StorageConfig):
        raise TypeError(
            f"all configurations must subclass StorageConfig; type(config): {config};"
        )

    if isinstance(config, SqliteConfig):
        sqlite_init(config=config)
    else:
        raise NotImplementedError("storage backend not implemented")
