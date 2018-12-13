"""Provide a function to create a Hive connection to a Databricks cluster."""
import base64
import sys

from pyhive import hive
from thrift.transport import THttpClient


PY_MAJOR = sys.version_info[0]


def connect(host, cluster=None, http_path=None, token=None, user=None, password=None):
    """Create a Hive DBAPI connection to an interactive Databricks cluster.

    Create a DBAPI connection to a Databricks cluster, which can be used to generate
    DBAPI cursor(s). Provide either a cluster name OR an http_path from the cluster's
    JDBC/ODBC connection details. If using Azure, http_path is required. On
    instantiation, http_path is prioritized over cluster.

    For authentication, provide either a token OR both a user and password. Token
    authentication is strongly preferred.

    :param str host: the server hostname from the cluster's JDBC/ODBC connection page.
    :param str cluster: the cluster unique name or alias.
    :param str http_path: the HTTP Path as shown in the cluster's JDBC/ODBC connection
        page. Required if using Azure platform.
    :param str token: a Databricks API token.
    :param str user: a Databricks user name.
    :param str password: the corresponding Databricks user's password.
    """
    if token is not None:
        auth = "token:%s" % token
    elif user is not None and password is not None:
        auth = "%s:%s" % (user, password)
    else:
        raise ValueError(
            "Missing arguments. Must provide either token or user/password."
        )

    if PY_MAJOR < 3:
        auth = base64.standard_b64encode(auth)
    else:
        auth = base64.standard_b64encode(auth.encode()).decode()

    if http_path is not None:
        url = "https://%s:443/%s" % (host, http_path)
    elif cluster is not None:
        url = "https://%s:443/sql/protocolv1/o/0/%s" % (host, cluster)
    else:
        raise ValueError(
            "Missing arguments. Must provide either cluster or http_path."
        )

    transport = THttpClient.THttpClient(url)
    transport.setCustomHeaders({"Authorization": "Basic %s" % auth})

    return hive.connect(thrift_transport=transport)
