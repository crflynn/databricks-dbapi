from sqlalchemy.connectors.pyodbc import PyODBCConnector

from databricks_dbapi import odbc
from databricks_dbapi.sqlalchemy_dialects.base import DatabricksDialectBase


class DatabricksPyodbcDialect(DatabricksDialectBase, PyODBCConnector):
    name = b"databricks"
    driver = b"pyodbc"

    @classmethod
    def dbapi(cls):
        return odbc

    def create_connect_args(self, url):
        elements, kwargs = super().create_connect_args(url=url)
        # we use user (following PEP249 guidelines), pyodbc uses username
        kwargs["user"] = kwargs.pop("username")
        return elements, kwargs
