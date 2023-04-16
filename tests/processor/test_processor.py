from what_the_fec.client.bulk_client import Client as BulkClient, Config as BulkClientConfig
from what_the_fec.processor.processor import Config, Processor

# NOTE: test just used to run code not even close to any decent tests in here.
def test_download_data():
    client = BulkClient(config=BulkClientConfig())
    processor = Processor(bulk_client=client, config=Config(min_cycle_year=2020))
    print(processor.process())
    assert True