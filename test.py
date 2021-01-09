import os

from sqlalchemy.engine import create_engine

from databricks_dbapi import databricks

TOKEN = os.environ["DATABRICKS_TOKEN"]

USER = os.environ["DATABRICKS_USER"]
PASSWORD = os.environ["DATABRICKS_PASSWORD"]

HOST = os.environ["DATABRICKS_HOST"]
CLUSTER = os.environ["DATABRICKS_CLUSTER"]
HTTP_PATH = os.environ["DATABRICKS_HTTP_PATH"]


def test_token():
    connection = databricks.connect(host=HOST, cluster=CLUSTER, token=TOKEN)
    cursor = connection.cursor()
    print(cursor)


def test_user_password():
    connection = databricks.connect(host=HOST, cluster=CLUSTER, user=USER, password=PASSWORD)
    cursor = connection.cursor()
    print(cursor)


def test_http_path():
    connection = databricks.connect(host=HOST, http_path=HTTP_PATH, token=TOKEN)
    cursor = connection.cursor()
    print(cursor)


def test_sqlalchemy_token():
    engine = create_engine(
        f"databricks+pyhive://token:{TOKEN}@{HOST}:443/default", connect_args={"cluster": f"{CLUSTER}"}
    )
    connection = engine.connect()
    print(connection)


def test_sqlalchemy_user_password():
    engine = create_engine(
        f"databricks+pyhive://{USER}:{PASSWORD}@{HOST}:443/default", connect_args={"cluster": f"{CLUSTER}"}
    )
    connection = engine.connect()
    print(connection)


def test_sqlalchemy_http_path():
    engine = create_engine(
        f"databricks+pyhive://token:{TOKEN}@{HOST}:443/default", connect_args={"http_path": f"{HTTP_PATH}"}
    )
    connection = engine.connect()
    print(connection)
