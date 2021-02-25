"""Provide a function to create an ODBC connection to a Databricks cluster."""
import pyodbc
from pyodbc import *  # Make globals and exceptions visible in this module per PEP 249


def connect(
    host,
    port=443,
    database="default",
    http_path=None,
    token=None,
    user=None,
    password=None,
    driver_path=None,
    **kwargs,
):
    """Create an ODBC DBAPI connection to a Databricks workspace or SQL Analytics cluster.

    Create a DBAPI connection to a Databricks cluster, which can be used to generate
    DBAPI cursor(s). Provide an ``http_path`` from the cluster's
    JDBC/ODBC connection details.

    For authentication, provide either a ``token`` OR both a ``user`` and ``password``.
    Token authentication is strongly recommended over passwords.

    The simplest connection requires providing args ``host``, ``http_path``,
    ``token``, and the ODBC ``driver_path``.  The default path on Mac OSX is likely:
    ``/Library/simba/spark/lib/libsparkodbc_sbu.dylib``

    :param str host: the server hostname from the cluster's JDBC/ODBC connection page.
    :param int port: the port number from the cluster's JDBC/ODBC connection page.
    :param str database: the database to use
    :param str http_path: the HTTP Path as shown in the cluster's JDBC/ODBC connection
        page. Required if using Azure platform.
    :param str token: a Databricks API token.
    :param str user: a Databricks user name.
    :param str password: the corresponding Databricks user's password.
    :param str driver_path: the absolute path to the ODBC driver.
    :param dict kwargs: keyword args passed to ``pyodbc.connect``
    """
    if driver_path is None:
        raise ValueError("Driver path must be provided.")

    if token is not None:
        user = "token"
        password = token
    elif user is not None and password is not None:
        pass
    else:
        raise ValueError("Missing arguments. Must provide either token or user/password.")

    connection_string = (
        f"Driver={driver_path};Database={database};Host={host};"
        f"Port={port};httpPath={http_path};UID={user};PWD={password};"
        "transportMode=http;ssl=1;AuthMech=8;SparkServerType=3;ThriftTransport=1"
    )

    # autocommit is required
    return pyodbc.connect(connection_string, autocommit=True, **kwargs)
