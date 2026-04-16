import os
import sys

import pytest
from dotenv import load_dotenv

# Add the project directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# Load .env before importing anything that needs DATABASE_URL
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env")))

from my_flask_app import app


@pytest.fixture(scope="function")
def client():
        with app.test_client() as client:
                yield client
