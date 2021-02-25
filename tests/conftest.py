import os

import dotenv
import pytest

dotenv.load_dotenv(dotenv_path=dotenv.find_dotenv())

TOKEN_WORKSPACE = os.environ["DATABRICKS_TOKEN_WORKSPACE"]
TOKEN_SQL_ANALYTICS = os.environ["DATABRICKS_TOKEN_SQL_ANALYTICS"]
USER = os.environ["DATABRICKS_USER"]
PASSWORD = os.environ["DATABRICKS_PASSWORD"]
HOST = os.environ["DATABRICKS_HOST"]
HTTP_PATH_WORKSPACE = os.environ["DATABRICKS_HTTP_PATH_WORKSPACE"]
HTTP_PATH_SQL_ANALYTICS = os.environ["DATABRICKS_HTTP_PATH_SQL_ANALYTICS"]
ODBC_DRIVER_PATH = os.environ["DATABRICKS_ODBC_DRIVER_PATH"]


@pytest.fixture
def token_workspace():
    return TOKEN_WORKSPACE


@pytest.fixture
def token_sql_analytics():
    return TOKEN_SQL_ANALYTICS


@pytest.fixture
def user():
    return USER


@pytest.fixture
def password():
    return PASSWORD


@pytest.fixture
def host():
    return HOST


@pytest.fixture
def http_path_workspace():
    return HTTP_PATH_WORKSPACE


@pytest.fixture
def http_path_sql_analytics():
    return HTTP_PATH_SQL_ANALYTICS


@pytest.fixture
def odbc_driver_path():
    return ODBC_DRIVER_PATH
