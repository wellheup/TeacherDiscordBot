import logging
import os
import sys

import pytest

from my_flask_app import app

# Ensure the project directory is in the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from my_flask_app import app


@pytest.fixture(scope="function")
def client():
    with app.test_client() as client:
        yield client


logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(scope="function")
def resource():
    resource = open_some_resource()
    try:
        logging.debug("Resource opened")
        yield resource
    finally:
        resource.close()
        logging.debug("Resource closed")
