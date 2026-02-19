"""
Conftest for API integration tests that mock the database.
Override the autouse database fixture to avoid requiring a live DB.
"""
import pytest
from unittest.mock import MagicMock


@pytest.fixture(autouse=True)
def setup_database_for_test(event_loop):
    """
    Override the parent conftest's database setup.
    API integration tests mock the database, so no real DB connection needed.
    """
    yield
