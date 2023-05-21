import abc

from sqlalchemy import Connection

from what_the_fec.storage.config import StorageConfig
from what_the_fec.storage.mysql.config import MySQLConfig
from what_the_fec.storage.mysql.db import init as mysql_init


class DB(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_conn(self) -> Connection:
        raise NotImplementedError


def init(config: StorageConfig):
    if not isinstance(config, StorageConfig):
        raise TypeError(
            f"all configurations must subclass StorageConfig; type(config): {config};"
        )

    if isinstance(config, MySQLConfig):
        mysql_init(config=config)
    else:
        raise NotImplementedError("storage backend not implemented")
