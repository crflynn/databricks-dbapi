from databricks_dbapi import hive
from databricks_dbapi.sqlalchemy_dialects.base import DatabricksDialectBase


class DatabricksPyhiveDialect(DatabricksDialectBase):
    name = b"databricks"
    driver = b"pyhive"

    @classmethod
    def dbapi(cls):
        return hive

    def create_connect_args(self, url):
        kwargs = {
            "host": url.host,
            "port": url.port or 443,
            "user": url.username,
            "password": url.password,
            "database": url.database or "default",
        }

        if url.query is not None and "http_path" in url.query:
            kwargs["http_path"] = url.query["http_path"]

        kwargs.update(url.query)
        return [], kwargs
