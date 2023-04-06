from pydantic import BaseModel


class StorageConfig(BaseModel):
    pool_connections: int
