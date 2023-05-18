



from itertools import chain
from typing import Optional

from pydantic import BaseModel
from what_the_fec.client.bulk_client import Client as BulkClient, FileType


class Config(BaseModel):
    min_cycle_year: Optional[int] = 2012
    max_cycle_year: Optional[int] = 2024


class Processor:
    _bulk_client: BulkClient
    _config: Config

    def __init__(self, bulk_client: BulkClient, config: Config) -> None:
        if not isinstance(bulk_client, BulkClient):
            raise TypeError(f"bulk_client should be BulkClient; type(bulk_client): {bulk_client};")
        
        if not isinstance(config, Config):
            raise TypeError(f"config should be type processor.Config type(config): {config};")

        self._bulk_client = bulk_client
        self._config = config


    def process(self) -> None:
        # TODO: remove this list later this is just hax to get a rough candidate_record count
        # Citation for the following code:
        # Date: 04/16/2023
        # Copied from /OR/ Adapted from /OR/ Based on:
        # https://stackoverflow.com/questions/20112776/how-do-i-flatten-a-list-of-lists-nested-lists
        data = list(chain(*[self._process_cycle(cycle_year=year) for year in range(self._config.min_cycle_year, self._config.max_cycle_year + 2, 2)]))
        total = 0
        for d in data:
            total += d
        return total
            


    def _process_cycle(self, *, cycle_year):
        return list(self._bulk_client.download_data(file_type=FileType.CONTRIBUTIONS_BY_INVIDUALS, cycle_year=cycle_year).values())
