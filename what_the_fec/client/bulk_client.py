from datetime import date
from enum import Enum
from io import BytesIO
from tempfile import NamedTemporaryFile, TemporaryDirectory, TemporaryFile
from zipfile import ZipFile

from typing import Optional
from pydantic import BaseModel
from urllib3 import PoolManager

class Config(BaseModel):
    base_url: Optional[str] = "https://www.fec.gov/files/bulk-downloads"
    num_connections: Optional[int] = 2


class FileType(str, Enum):
    ALL_CANDIDATES = "weball"
    CONTRIBUTIONS_BY_INVIDUALS = "indiv"
    CONTRIBUTIONS_FROM_COMMITTEES_TO_CANDIDATES_AND_INDEPEDENT_EXPENDITURES = "pas2"


_VALID_CYCLE_MIN = 1982
today_year = date.today().year
if today_year % 2 == 0:
    _VALID_CYCLE_MAX = today_year
else:
    _VALID_CYCLE_MAX = today_year + 1


class BulkClientError(Exception):
    pass


class Client:
    _config: Config
    _conn_pool: PoolManager

    def __init__(self, *, config: Config) -> None:
        if not isinstance(config, Config):
            raise TypeError(f"config should be type bulk_client.Config type(config): {config};")
        
        self._config = config
        self._conn_pool = PoolManager(num_pools=config.num_connections)


    def download_data(self, *, file_type: FileType, cycle_year: int) -> dict[str, bytes]:
        if not isinstance(file_type, FileType):
            raise TypeError(f"file_type should be type FileType type(file_type): {file_type};")

        if not isinstance(cycle_year, int):
            raise TypeError(f"cycle_year should be an integer; type(cycle_year): {cycle_year};")

        if not cycle_year % 2 == 0 and _VALID_CYCLE_MIN <= cycle_year <= _VALID_CYCLE_MAX:
            raise ValueError(f"cycle_year most be an even integer within the range {_VALID_CYCLE_MIN}-{_VALID_CYCLE_MAX}; cycle_year: {cycle_year};")
        
        resp = None
        try:
            resp = self._conn_pool.request("GET", f"{self._config.base_url}/{cycle_year}/{file_type.value}{str(cycle_year)[-2:]}.zip", preload_content=False)

            if resp.status != 200:
                raise BulkClientError(f"download not succcessful; response status: {resp.status}, response content: {resp.data};")

            data_map = {}
            total = 0
            with TemporaryFile() as tf:
                # Citation for the following code:
                # Date: 04/16/2023
                # Copied from /OR/ Adapted from /OR/ Based on:
                # https://stackoverflow.com/questions/17285464/whats-the-best-way-to-download-file-using-urllib3
                # https://stackoverflow.com/questions/1517616/stream-large-binary-files-with-urllib2-to-file
                # https://stackoverflow.com/questions/39983886/python-writing-and-reading-from-a-temporary-file
                chunk_size = (1024 * 1024) * 20 #20 MB so this doesnt take ten years
                while True:
                    bytes_chunk = resp.read(chunk_size)
                    if not bytes_chunk:
                        break
                    tf.write(bytes_chunk)
                tf.seek(0)
                with ZipFile(tf) as zf:
                    for info in zf.infolist():
                        if "by_date" not in info.filename:
                            with zf.open(info.filename) as zfo:
                                while True:
                                    line = zfo.readline()
                                    if not line:
                                        break
                                    total += 1

        finally:
            if resp:
                resp.release_conn()

        return {"bad_fix_me": total}
