from what_the_fec.client.bulk_client import Client, Config, FileType


def test_download_data():
    client = Client(config=Config())
    data = client.download_data(file_type=FileType.ALL_CANDIDATES, cycle_year=2022)
    assert type(data["weball22.txt"]) == type(b"") 