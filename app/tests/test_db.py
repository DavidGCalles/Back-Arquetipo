import pytest
from unittest.mock import patch, MagicMock
from app.services.db import DBManager
from config import Config, LOGGER

@pytest.fixture
def db_manager():
    return DBManager()

def test_get_db_connection_sqlite(db_manager):
    with patch('sqlite3.connect', return_value=MagicMock()) as mock_connect:
        connection = db_manager.get_db_connection("sqlite")
        assert connection is not None
        mock_connect.assert_called_once_with(db_manager.db_configs["sqlite"]["DB_HOST"])

def test_get_db_connection_mysql(db_manager):
    with patch('mysql.connector.connect', return_value=MagicMock()) as mock_connect:
        connection = db_manager.get_db_connection("mysql")
        assert connection is not None
        db_settings = db_manager.db_configs["mysql"]
        mock_connect.assert_called_once_with(
            host=db_settings["DB_HOST"],
            port=db_settings["DB_PORT"],
            database=db_settings["DB_NAME"],
            user=db_settings["DB_USER"],
            password=db_settings["DB_PASSWORD"],
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )

def test_get_db_connection_unsupported(db_manager):
    connection = db_manager.get_db_connection("unsupported_db")
    assert connection is None

def test_get_db_connection_not_found(db_manager):
    connection = db_manager.get_db_connection("not_found_db")
    assert connection is None