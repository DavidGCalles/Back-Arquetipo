import pytest
from unittest.mock import patch, mock_open, MagicMock
from app.services.db import DBManager
from config import Config, LOGGER

@pytest.fixture
def db_manager():
    return DBManager()

def test_check_coherence_sqlite(db_manager):
    with patch('builtins.open', mock_open(read_data="CREATE TABLE test (id INTEGER PRIMARY KEY);")), \
         patch.object(db_manager, 'get_db_connection', return_value=MagicMock()) as mock_conn:
        mock_cursor = mock_conn.return_value.cursor.return_value
        assert db_manager.check_coherence() is True
        mock_cursor.executescript.assert_called_once()

def test_check_coherence_sqlite_rpi(db_manager):
    db_manager.db_type = "sqlite-rpi"
    with patch('builtins.open', mock_open(read_data="CREATE TABLE test (id INTEGER PRIMARY KEY);")), \
         patch.object(db_manager, 'get_db_connection', return_value=MagicMock()) as mock_conn:
        mock_cursor = mock_conn.return_value.cursor.return_value
        assert db_manager.check_coherence() is True
        mock_cursor.executescript.assert_called_once()

def test_check_coherence_mysql(db_manager):
    db_manager.db_type = "mysql"
    with patch('builtins.open', mock_open(read_data="CREATE TABLE test (id INT PRIMARY KEY);")), \
         patch.object(db_manager, 'get_db_connection', return_value=MagicMock()) as mock_conn:
        mock_cursor = mock_conn.return_value.cursor.return_value
        assert db_manager.check_coherence() is True
        mock_cursor.execute.assert_called()

def test_reset_db_settings(db_manager):
    db_manager.reset_db_settings("mysql")
    assert db_manager.db_type == "mysql"

def test_get_db_connection_sqlite(db_manager):
    with patch('sqlite3.connect', return_value=MagicMock()) as mock_connect:
        connection = db_manager.get_db_connection()
        assert connection is not None
        mock_connect.assert_called_once_with(db_manager.db_settings["DB_HOST"])

def test_get_db_connection_mysql(db_manager):
    db_manager.db_type = "mysql"
    db_manager.db_settings = Config.DB_TYPES["mysql"]
    LOGGER.debug("Test DB settings: %s", db_manager.db_settings)
    with patch('mysql.connector.connect', return_value=MagicMock()) as mock_connect:
        connection = db_manager.get_db_connection()
        assert connection is not None
        mock_connect.assert_called_once_with(
            host=db_manager.db_settings["DB_HOST"],
            port=db_manager.db_settings["DB_PORT"],
            database=db_manager.db_settings["DB_NAME"],
            user=db_manager.db_settings["DB_USER"],
            password=db_manager.db_settings["DB_PASSWORD"],
            charset='utf8mb4',
            collation='utf8mb4_general_ci'
        )