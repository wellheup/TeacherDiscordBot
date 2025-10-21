import os
import sys

import pytest

# Add the project directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

# Debug statements to ensure path is correct
print(f"Current sys.path: {sys.path}")

from my_flask_app import app


@pytest.fixture(scope="function")
def client():
	with app.test_client() as client:
		yield client
