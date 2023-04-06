from what_the_fec.storage.config import StorageConfig


class SqliteConfig(StorageConfig):
    pool_connections: int
