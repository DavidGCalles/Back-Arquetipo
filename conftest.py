import sys
import os
import pytest
from app.dao.generic_dao import BaseDAO
from app.services.db import DBManager

# Add the app directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

@pytest.fixture
def dao():
    """Fixture to create a new DAO for each test function."""
    # Setup: create a new DAO with an in-memory SQLite database
    db_manager = DBManager()
    db_manager.db_configs["sqlite"]["DB_HOST"] = ":memory:"
    connection = db_manager.get_db_connection("sqlite")
    dao = BaseDAO("sqlite", connection=connection)
    # Create the table for the tests
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE item (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT)")
    connection.commit()
    yield dao
    # Teardown: close the connection
    connection.close()
