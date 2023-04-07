from what_the_fec.storage.config import StorageConfig


class MySQLConfig(StorageConfig):
    db_user: str
    db_password: str
    db_hostname: str
    db_port: int
    db_name: str
    pool_connections: int
