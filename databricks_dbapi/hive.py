"""Provide a function to create a Hive connection to a Databricks cluster."""
import base64
import sys

from pyhive import hive
from pyhive.exc import *  # Make all exceptions visible in this module per PEP 249
from thrift.transport import THttpClient

PY_MAJOR = sys.version_info[0]

# PEP 249 module globals
apilevel = hive.apilevel
threadsafety = hive.threadsafety
paramstyle = hive.paramstyle


def connect(host, port=443, database="default", http_path=None, token=None, user=None, password=None, **kwargs):
    """Create a pyhive-driven DBAPI connection to Databricks workspace cluster.

    Create a DBAPI connection to a Databricks cluster, which can be used to generate
    DBAPI cursor(s). Provide an ``http_path`` from the cluster's JDBC/ODBC connection
    details.

    For authentication, provide either a ``token`` OR both a ``user`` and ``password``.
    Token authentication is strongly recommended over passwords.

    The simplest connection requires providing args ``host``, ``http_path``, and
    ``token``.

    :param str host: the server hostname from the cluster's JDBC/ODBC connection page.
    :param int port: the port number from the cluster's JDBC/ODBC connection page.
    :param str database: the database to use
    :param str http_path: the HTTP Path as shown in the cluster's JDBC/ODBC connection
        page.
    :param str token: a Databricks API token.
    :param str user: a Databricks user name.
    :param str password: the corresponding Databricks user's password.
    :param dict kwargs: keyword arguments passed to ``hive.connect``
    """
    if token is not None:
        auth = "token:%s" % token
    elif user is not None and password is not None:
        auth = "%s:%s" % (user, password)
    else:
        raise ValueError("Missing arguments. Must provide either token or user/password.")

    # https://kb.databricks.com/python/python-2-eol.html
    if PY_MAJOR < 3:
        auth = base64.standard_b64encode(auth)
    else:
        auth = base64.standard_b64encode(auth.encode()).decode()

    if http_path is not None:
        url = "https://%s:%s/%s" % (host, port, http_path)
    else:
        raise ValueError("Missing arguments. Must provide either cluster or http_path.")

    transport = THttpClient.THttpClient(url)
    transport.setCustomHeaders({"Authorization": "Basic %s" % auth})

    return hive.connect(database=database, thrift_transport=transport, **kwargs)
