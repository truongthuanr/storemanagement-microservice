# tests/conftest.py

import pytest
import requests
import config

@pytest.fixture(scope="session")
def product_url():
    return config.PRODUCT_URL

@pytest.fixture(scope="session")
def default_headers():
    return config.HEADERS

# @pytest.fixture
# def test_product_data():
#     return config.TEST_PRODUCT_PAYLOAD.copy()
