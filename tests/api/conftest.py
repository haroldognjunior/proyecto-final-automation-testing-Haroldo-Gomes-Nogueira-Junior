import pytest

from utils.api_client import ApiClient


@pytest.fixture
def api():
    client = ApiClient()
    yield client
    client.close()
