import os
import sys
import pytest
from my_flask_app import app

# Ensure the project directory is in the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from my_flask_app import app

@pytest.fixture
def client():
	with app.test_client() as client:
		yield client