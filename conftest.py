import os
import pytest
from dotenv import load_dotenv

# Load .env from the project root
load_dotenv()

@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL")

@pytest.fixture(scope="session")
def common_headers():
    return {
        "Accept": "application/json",
        "User-Agent": "pytest-api-test/1.0",
        "x-api-key": os.getenv("API_KEY")
    }
